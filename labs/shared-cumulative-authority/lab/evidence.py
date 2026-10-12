"""Independent destination reader and offline derivation; no expected totals as measurements."""
import argparse
import json
import os
from pathlib import Path

import httpx
import psycopg
from psycopg.rows import dict_row

from .common import now, secret, dsn, write_json

RAW = ('grant.json','requests.jsonl','decisions.jsonl','authority-state.json',
       'erp-state.json','schedule-events.jsonl','run-manifest.json')


def collect(stage):
    root = Path(os.environ.get('EVIDENCE_DIR', '/evidence'))
    with psycopg.connect(dsn('authority','reader'), autocommit=True, row_factory=dict_row) as c:
        with c.transaction():
            c.execute('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY')
            authority = {'observed_at':now(), 'grants':c.execute('SELECT * FROM grants ORDER BY grant_id').fetchall(),
                         'balances':c.execute('SELECT * FROM grant_balances ORDER BY grant_id').fetchall(),
                         'operations':c.execute('SELECT * FROM operations ORDER BY operation_id').fetchall()}
    with httpx.Client(timeout=5) as client:
        response = client.get('http://erp:8000/orders', params={'grant_id':'G-2026-001'},
                              headers={'Authorization':'Bearer ' + secret('erp.read')})
        response.raise_for_status()
        destination = {'observed_at':now(), 'status_code':response.status_code, **response.json()}
    for filename, value in [('authority-state.json',authority), ('erp-state.json',destination)]:
        path = root / filename
        prior = json.loads(path.read_text()) if path.exists() else {}
        prior[stage] = value
        write_json(path,prior)
    fixture = json.loads(Path('grant.json').read_text())
    if authority['grants'] != [fixture]:
        raise RuntimeError('Independent grant snapshot does not match trusted fixture')
    write_json(root/'grant.json',fixture)


def jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding='utf-8').splitlines() if line]


def derive(root):
    import hashlib
    root = Path(root)
    if any(not (root/f).is_file() for f in RAW):
        raise ValueError('Incomplete required artifacts')
    grant = json.loads((root/'grant.json').read_text())
    authority = json.loads((root/'authority-state.json').read_text())
    erp = json.loads((root/'erp-state.json').read_text())
    manifest = json.loads((root/'run-manifest.json').read_text())
    if manifest.get('phase') != 'settled':
        raise ValueError('Unfinished run')
    if authority['initial']['operations'] or erp['initial']['orders'] or any(b['charged_quantity'] for b in authority['initial']['balances']):
        raise ValueError('Initial state contamination')
    ops = authority['final']['operations']
    quantities = {state:sum(o['quantity'] for o in ops if o['state']==state)
                  for state in ('COMMITTED','RESERVED','PENDING_RECONCILIATION','ADMITTED_UNRESERVED')}
    q = sum(quantities[s] for s in ('COMMITTED','RESERVED','PENDING_RECONCILIATION'))
    charged = authority['final']['balances'][0]['charged_quantity']
    orders = erp['final']['orders']
    d = sum(o['quantity'] for o in orders)
    requests = jsonl(root/'requests.jsonl')
    submitted = {r['operation_id'] for r in requests if r['event']=='submitted'}
    completed = {r['operation_id'] for r in requests if r['event']=='response' and r['status_code']==200}
    if submitted != completed or submitted != {o['operation_id'] for o in ops}:
        raise ValueError('Incomplete operation/response evidence')
    events = jsonl(root/'schedule-events.jsonl')
    if any(e['event'] in ('invalid','timeout') for e in events):
        raise ValueError('Invalid controlled scheduling')
    if manifest['hook'] != 'none':
        arrivals = [e for e in events if e['event']=='arrival']
        releases = [e for e in events if e['event']=='release']
        if len(releases)!=1 or {e['operation_id'] for e in arrivals} != submitted:
            raise ValueError('Missing/invalid barrier evidence')
        if any(e['sequence']>=releases[0]['sequence'] for e in arrivals):
            raise ValueError('Barrier released before arrivals')
    by_id = {o['operation_id']:o for o in ops}
    if len({o['operation_id'] for o in orders}) != len(orders):
        raise ValueError('Duplicate business effect')
    for order in orders:
        op = by_id.get(order['operation_id'])
        if not op or op['decision']!='ALLOW' or any(order[k]!=op[k] for k in ('grant_id','resource','supplier','quantity')):
            raise ValueError('Destination/binding mismatch')
    if any(o['state'] not in ('COMMITTED','DENIED') for o in ops) or quantities['COMMITTED']!=d:
        raise ValueError('Run not settled or destination/accounting mismatch')
    decisions = [e for e in jsonl(root/'decisions.jsonl') if e['event']=='decision']
    if len({e['operation_id'] for e in decisions})!=len(ops) or len(decisions)!=len(ops):
        raise ValueError('Missing/duplicate decision evidence')
    for event in decisions:
        op = by_id[event['operation_id']]
        if event['decision']!=op['decision'] or not event['commit_confirmed']:
            raise ValueError('Decision/persisted operation mismatch')
    if charged != q:
        raise ValueError('Accounting integrity failure')
    result = {'run_id':manifest['run_id'], 'purpose':manifest['purpose'], 'grant_total':grant['max_total_quantity'],
              'allow_count':sum(o['decision']=='ALLOW' for o in ops),
              'deny_count':sum(o['decision']=='DENY' for o in ops), 'destination_total':d,
              'charged_quantity':charged, 'C':quantities['COMMITTED'], 'R':quantities['RESERVED'],
              'U':quantities['PENDING_RECONCILIATION'], 'Q':q,
              'authority_bound_preserved':q<=grant['max_total_quantity'],
              'destination_bound_preserved':d<=grant['max_total_quantity'],
              'destination_relationship_preserved':d<=q<=grant['max_total_quantity'],
              'accounting_consistent':charged==q, 'evidence_complete':True,
              'input_sha256':{f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in RAW},
              'claim_status':'ENGINEERING VERIFICATION ONLY; formal Laboratory gate not performed'}
    write_json(root/'run-summary.json',result)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=('initial','final','derive'))
    args = parser.parse_args()
    if args.stage=='derive':
        derive(os.environ.get('EVIDENCE_DIR','/evidence'))
    else:
        collect(args.stage)
