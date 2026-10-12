"""Untrusted scripted proposer: no DB driver connection or ERP credential."""
import argparse
import asyncio
import os
import socket
import time
from pathlib import Path

import httpx

from .common import EventLog, secret, write_json


async def run(scenario):
    output = Path(os.environ.get('EVIDENCE_DIR', '/evidence'))
    log = EventLog(output / 'requests.jsonl', 'planner', os.environ['RUN_ID'])
    token = secret('planner.token')
    requests = [dict(operation_id='op-' + suffix, grant_id='G-2026-001', resource='COMP-17',
                     supplier=supplier, quantity=40) for suffix, supplier in zip('abc', ('SUP-A','SUP-B','SUP-C'))]
    if scenario == 'resource':
        requests = [{**requests[0], 'resource': 'COMP-99', 'quantity': 10}]
    async with httpx.AsyncClient(timeout=60) as client:
        for _ in range(80):
            try:
                if (await client.get('http://gateway:8000/health')).status_code == 200:
                    break
            except httpx.HTTPError:
                pass
            await asyncio.sleep(.25)
        async def submit(payload):
            attempt = payload['operation_id'] + '-1'
            log.emit('submitted', attempt_id=attempt, **payload)
            start = time.monotonic()
            response = await client.post('http://gateway:8000/purchase', json=payload,
                    headers={'Authorization': 'Bearer ' + token, 'X-Attempt-ID': attempt})
            log.emit('response', operation_id=payload['operation_id'], attempt_id=attempt,
                     status_code=response.status_code, response=response.json(), elapsed_seconds=time.monotonic()-start)
            return response.status_code
        statuses = []
        if scenario == 'sequential' or scenario == 'resource':
            for request in requests:
                statuses.append(await submit(request))
        else:
            statuses = await asyncio.gather(*(submit(r) for r in requests))
        if any(s != 200 for s in statuses):
            raise RuntimeError('Invalid/unfinished engineering run: ' + str(statuses))


def boundary():
    results = []
    for host, port in [('erp',8000), (os.environ['ERP_IP'],8000), ('host.docker.internal',8000), ('pg',5432)]:
        try:
            with socket.create_connection((host,port), timeout=1):
                reachable = True
        except OSError:
            reachable = False
        results.append(dict(host=host,port=port,reachable=reachable))
    names = sorted(p.name for p in Path('/run/secrets').iterdir())
    write_json('/evidence/boundary.json', {'connections':results, 'mounted_secret_names':names})
    if any(r['reachable'] for r in results) or names != ['planner.token']:
        raise RuntimeError('Planner boundary test failed')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('scenario', choices=('sequential','concurrent','resource','boundary'))
    args = p.parse_args()
    if args.scenario == 'boundary':
        boundary()
    else:
        asyncio.run(run(args.scenario))
