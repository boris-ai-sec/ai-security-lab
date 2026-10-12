"""Host-only engineering orchestration. Formal publication execution is a separate Laboratory gate."""
import argparse
import hashlib
import json
import math
import os
import secrets
import shutil
import subprocess
import sys
from pathlib import Path

from .common import finite_timeout, now, write_json
from .evidence import derive, jsonl

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'out'
SPEC = ROOT / 'EXPERIMENT_SPEC_V0.2.md'


def provision_secrets():
    folder = ROOT/'secrets'
    folder.mkdir(exist_ok=True)
    for name in ('admin.pass','gw.pass','reader.pass','erp.pass','erp.write','erp.read','planner.token'):
        path = folder/name
        if not path.exists():
            path.write_text(secrets.token_urlsafe(32),encoding='utf-8')


def command(args, env, capture=False):
    result = subprocess.run(args, cwd=ROOT, env=env, check=True,
                            text=True, capture_output=capture)
    return result.stdout.strip() if capture else None


def compose(args, env, capture=False):
    return command(['docker','compose','-p',env['COMPOSE_PROJECT_NAME'],*args],env,capture)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='action',required=True)
    sub.add_parser('build')
    sub.add_parser('test')
    smoke = sub.add_parser('smoke')
    smoke.add_argument('scenario',choices=('sequential','vulnerable','corrected','resource'))
    smoke.add_argument('--timeout',type=finite_timeout)
    smoke.add_argument('--keep',action='store_true')
    verify = sub.add_parser('verify')
    verify.add_argument('path',type=Path)
    args = parser.parse_args()
    if args.action=='verify':
        print(json.dumps(derive(args.path),indent=2))
        return
    provision_secrets()
    env = os.environ.copy()
    env['COMPOSE_PROJECT_NAME']='habr003-build'
    if args.action=='build':
        compose(['build','gateway'],env)  # One shared image, not concurrent writes to one image tag.
        return
    run_id = ('t' if args.action=='test' else 'e') + secrets.token_hex(3)
    folder = OUT/run_id
    folder.mkdir(parents=True,exist_ok=False)
    env.update(COMPOSE_PROJECT_NAME='habr003-'+run_id, RUN_ID=run_id,
               RUN_OUT=str(folder), TEST_OUT=str(folder))
    mode, hook = 'corrected','none'
    timeout = 10.0  # Provisional first-smoke setting, never a specification constant.
    basis = {'selection':'provisional_first_smoke','formal':False}
    selection_path = OUT/'timeout.json'
    if args.action=='smoke':
        if selection_path.exists():
            selected=json.loads(selection_path.read_text())
            timeout=finite_timeout(selected['seconds'])
            basis={'selection':'prior_smoke_evidence',**selected}
        if args.timeout is not None:
            timeout=args.timeout
            basis={'selection':'explicit_operator_override','formal':False}
        mode = 'vulnerable' if args.scenario in ('sequential','vulnerable') else 'corrected'
        hook = 'post_read' if args.scenario=='vulnerable' else 'pre_transaction' if args.scenario=='corrected' else 'none'
        env['SCENARIO']='sequential' if args.scenario=='sequential' else 'resource' if args.scenario=='resource' else 'concurrent'
    env.update(MODE=mode,HOOK=hook,BARRIER_TIMEOUT=str(timeout))
    manifest={'run_id':run_id,'purpose':'ENGINEERING_TEST' if args.action=='test' else 'ENGINEERING_SMOKE_NOT_FORMAL',
              'phase':'started','started_at':now(),'mode':mode,'hook':hook,'barrier_timeout_seconds':timeout,
              'timeout_basis':basis,'participants':['op-a','op-b','op-c'] if hook!='none' else [],
              'clean_state':'fresh Compose project and PostgreSQL volume','isolation_level':'READ COMMITTED',
              'gateway_workers':1,'spec_sha256':hashlib.sha256(SPEC.read_bytes()).hexdigest(),
              'dependencies':(ROOT/'requirements.lock').read_text(),
              'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in sorted((ROOT/'lab').glob('*.py'))}}
    write_json(folder/'run-manifest.json',manifest)
    try:
        if args.action=='test':
            compose(['up','-d','--wait','pg'],env)
            compose(['run','--rm','setup'],env)
            compose(['run','--rm','--no-deps','tests'],env)
            manifest.update(phase='settled',finished_at=now())
            write_json(folder/'run-manifest.json',manifest)
            print('Engineering test results: '+str(folder))
            return
        compose(['up','-d','--wait','gateway'],env)
        compose(['run','--rm','--no-deps','reader','python','-m','lab.evidence','initial'],env)
        erp_id=compose(['ps','-q','erp'],env,True)
        details=json.loads(command(['docker','inspect',erp_id],env,True))[0]
        erp_ip=next(iter(details['NetworkSettings']['Networks'].values()))['IPAddress']
        compose(['run','--rm','--no-deps','-e','ERP_IP='+erp_ip,'planner','python','-m','lab.planner','boundary'],env)
        compose(['run','--rm','--no-deps','planner'],env)
        compose(['run','--rm','--no-deps','reader','python','-m','lab.evidence','final'],env)
        for name in ('decisions.jsonl','schedule-events.jsonl'):
            path=folder/'gateway'/name
            if path.exists():
                shutil.copyfile(path,folder/name)
            elif name=='schedule-events.jsonl' and hook=='none':
                (folder/name).write_text('',encoding='utf-8')
        shutil.copyfile(folder/'planner'/'requests.jsonl',folder/'requests.jsonl')
        manifest.update(phase='settled',finished_at=now(),
                        images={name:command(['docker','image','inspect',name,'--format','{{.Id}}'],env,True)
                                for name in ('habr003-v01:local','postgres:18.3')},
                        docker_version=command(['docker','version','--format','{{.Server.Version}}'],env,True))
        write_json(folder/'run-manifest.json',manifest)
        result=derive(folder)
        # Expectations are assertions after independent measurements, never inputs to derive().
        expected={'sequential':(2,1,80),'vulnerable':(3,0,120),'corrected':(2,1,80),'resource':(0,1,0)}[args.scenario]
        actual=(result['allow_count'],result['deny_count'],result['destination_total'])
        if actual!=expected or result['charged_quantity']!=expected[2]:
            raise RuntimeError('Engineering acceptance mismatch: '+str(actual))
        if args.scenario=='vulnerable':
            arrivals=[e for e in jsonl(folder/'schedule-events.jsonl') if e['event']=='arrival']
            if len(arrivals)!=3 or any(e['observed_charged']!=0 for e in arrivals):
                raise RuntimeError('Vulnerable stale-read schedule was not observed')
        elapsed=max(r['elapsed_seconds'] for r in jsonl(folder/'requests.jsonl') if r['event']=='response')
        selected=max(5,math.ceil(elapsed*5))
        write_json(selection_path,{'seconds':selected,'basis_run':run_id,'max_response_seconds':elapsed,
                   'rule':'max(5 seconds, ceil(5 * measured response duration)); operational, not canonical',
                   'formal':False})
        print(json.dumps({'engineering_smoke':args.scenario,'evidence':str(folder),
                          'measured_destination':result['destination_total'],'formal_gate':'NOT PERFORMED'},indent=2))
    except BaseException as exc:
        manifest.update(phase='invalid',failure=type(exc).__name__,finished_at=now())
        write_json(folder/'run-manifest.json',manifest)
        # A later verify must reject an invalid manifest, even if a previous summary exists.
        raise
    finally:
        if not getattr(args,'keep',False):
            # Only this newly created, task-owned project/volume is removed. Evidence stays on host.
            compose(['down','--volumes','--remove-orphans'],env)


if __name__=='__main__':
    main()
