import asyncio
import os
from pathlib import Path

import httpx
from fastapi import FastAPI, Header, HTTPException

from .common import EventLog, Purchase, dsn, finite_timeout, secret
from .schedule import Barrier, InvalidSchedule
from .store import IdentityConflict, Store


def create_app(store, tokens, mode, erp_url, write_token, read_token, *, barrier=None,
               transport=None, erp_timeout=5, fault=None):
    if mode not in ('vulnerable', 'corrected'):
        raise ValueError('Invalid mode')
    app = FastAPI()

    def subject(authorization):
        value = tokens.get(authorization.removeprefix('Bearer ')) if authorization else None
        if value is None:
            raise HTTPException(401, 'UNAUTHENTICATED')
        return value

    @app.get('/health')
    def health():
        return {'ok': True}

    @app.get('/operations/{operation_id}')
    async def status(operation_id: str, authorization: str = Header(default='')):
        caller = subject(authorization)
        row = await asyncio.to_thread(store.get, operation_id)
        if not row or row['subject_id'] != caller:
            raise HTTPException(404, 'NOT_FOUND')
        return row

    @app.post('/purchase')
    async def purchase(request: Purchase, authorization: str = Header(default=''),
                       x_attempt_id: str = Header(default='unspecified')):
        caller = subject(authorization)
        binding = request.binding(caller)
        store.log.emit('request_received', attempt_id=x_attempt_id, **binding)
        try:
            existing = await asyncio.to_thread(store.get, request.operation_id)
            if existing:
                from .store import match
                match(existing, binding)
                return {**existing, 'replayed': True}
            observed = None
            if mode == 'vulnerable':
                observed = await asyncio.to_thread(store.snapshot, request.grant_id)
                store.log.emit('authority_read', operation_id=request.operation_id, attempt_id=x_attempt_id,
                               observed_charged=observed['charged_quantity'] if observed else None)
            if barrier:
                await barrier.wait(request.operation_id, x_attempt_id, observed)
            row, fresh = await asyncio.to_thread(store.admit, binding, mode, observed)
            if not fresh or row['decision'] == 'DENY':
                return {**row, 'replayed': not fresh}
            async with httpx.AsyncClient(transport=transport, timeout=erp_timeout) as client:
                if fault == 'no_dispatch':
                    # Trusted engineering hook: this owner never sends POST, and its return closes dispatch.
                    evidence = await client.get(erp_url + '/orders', params={'grant_id': request.grant_id},
                                                headers={'Authorization': 'Bearer ' + read_token})
                    evidence.raise_for_status()
                    if any(o['operation_id'] == request.operation_id for o in evidence.json()['orders']):
                        raise ValueError('No-effect evidence conflicts')
                    if mode != 'corrected':
                        raise ValueError('No-dispatch release test is corrected-only')
                    return await asyncio.to_thread(store.transition, request.operation_id, 'RELEASED',
                                                   undispatched_proof=True)
                response = await client.post(erp_url + '/orders', json=request.model_dump(),
                                             headers={'Authorization': 'Bearer ' + write_token})
                response.raise_for_status()
                order = response.json()
                if fault == 'lost_response':
                    raise httpx.ReadTimeout('Engineering hook discards durable ERP acknowledgement')
                return await asyncio.to_thread(store.transition, request.operation_id, 'COMMITTED', order)
        except InvalidSchedule as exc:
            raise HTTPException(503, str(exc)) from exc
        except IdentityConflict as exc:
            raise HTTPException(409, str(exc)) from exc
        except (httpx.HTTPError, ValueError) as exc:
            current = await asyncio.to_thread(store.get, request.operation_id)
            if current and current['decision'] == 'ALLOW':
                store.log.emit('unknown_outcome', operation_id=request.operation_id, error=type(exc).__name__)
                return await asyncio.to_thread(store.transition, request.operation_id, 'PENDING_RECONCILIATION')
            raise
    return app


def app():
    output = Path(os.environ.get('EVIDENCE_DIR', '/evidence'))
    run_id = os.environ.get('RUN_ID', 'engineering')
    log = EventLog(output / 'decisions.jsonl', 'gateway', run_id)
    hook = os.environ.get('HOOK', 'none')
    mode = os.environ['MODE']
    if hook != 'none' and hook != ('post_read' if mode == 'vulnerable' else 'pre_transaction'):
        raise ValueError('Hook does not match frozen protocol')
    barrier = None if hook == 'none' else Barrier(os.environ['PARTICIPANTS'].split(','),
                       os.environ['BARRIER_TIMEOUT'], EventLog(output / 'schedule-events.jsonl', 'harness-hook', run_id), hook)
    return create_app(Store(dsn('authority', 'gw'), log), {secret('planner.token'): 'planner-1'}, mode,
                      'http://erp:8000', secret('erp.write'), secret('erp.read'), barrier=barrier,
                      erp_timeout=finite_timeout(os.environ.get('ERP_TIMEOUT', '5')),
                      fault=os.environ.get('ENGINEERING_FAULT'))
