import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import os
import time

import httpx
import psycopg
import pytest

from lab.common import EventLog, Purchase, dsn, finite_timeout
from lab.erp import create_app as erp_app
from lab.gateway import create_app as gateway_app
from lab.schedule import Barrier, InvalidSchedule
from lab.store import Store, IdentityConflict


@pytest.fixture()
def lab(tmp_path):
    for database, table in [('authority','operations,grant_balances,grants'),('erp','orders')]:
        with psycopg.connect(dsn(database,'admin'),autocommit=True) as c:
            c.execute('TRUNCATE '+table+' RESTART IDENTITY CASCADE')
            if database=='authority':
                c.execute("INSERT INTO grants VALUES ('G-2026-001','planner-1','COMP-17',ARRAY['SUP-A','SUP-B','SUP-C'],100,'ACTIVE')")
                c.execute("INSERT INTO grant_balances(grant_id) VALUES ('G-2026-001')")
    store=Store(dsn('authority','gw'),EventLog(tmp_path/'decisions.jsonl','gateway','test'))
    erp=erp_app(dsn('erp','erp'),'write','read')
    return store,erp,tmp_path


def request(i='a',quantity=40,**changes):
    return Purchase(operation_id='op-'+i,grant_id='G-2026-001',resource='COMP-17',supplier='SUP-A',quantity=quantity,**changes)


async def invoke(lab, mode='corrected', *, count=1, barrier=False, fault=None, duplicate=False):
    store,erp,path=lab
    hook=Barrier(['op-a','op-b','op-c'],3,EventLog(path/'schedule-events.jsonl','harness','test'),
                 'post_read' if mode=='vulnerable' else 'pre_transaction') if barrier else None
    app=gateway_app(store,{'client':'planner-1','other':'other-subject'},mode,'http://erp','write','read',
                    barrier=hook,transport=httpx.ASGITransport(app=erp),fault=fault)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://gw') as c:
        async def call(i):
            payload=request('a' if duplicate else chr(97+i)).model_dump()
            return await c.post('/purchase',json=payload,headers={'Authorization':'Bearer client','X-Attempt-ID':str(i)})
        if barrier or duplicate:
            return await asyncio.gather(*(call(i) for i in range(count)))
        return [await call(i) for i in range(count)]


def totals(store):
    with psycopg.connect(dsn('erp','admin')) as c:
        destination=c.execute('SELECT COALESCE(sum(quantity),0),count(*) FROM orders').fetchone()
    return store.snapshot('G-2026-001')['charged_quantity'],destination


@pytest.mark.parametrize('mode,barrier,expected',[('vulnerable',False,80),('vulnerable',True,120),('corrected',True,80)])
def test_scenarios(lab,mode,barrier,expected):
    responses=asyncio.run(invoke(lab,mode,count=3,barrier=barrier))
    assert all(r.status_code==200 for r in responses)
    assert sum(r.json()['decision']=='ALLOW' for r in responses)==(3 if expected==120 else 2)
    assert totals(lab[0])==(expected,(expected,3 if expected==120 else 2))
    if mode=='vulnerable' and barrier:
        events=[json.loads(line) for line in (lab[2]/'schedule-events.jsonl').read_text().splitlines()]
        assert [e['observed_charged'] for e in events if e['event']=='arrival']==[0,0,0]


@pytest.mark.parametrize('mode',['vulnerable','corrected'])
def test_concurrent_duplicate_dispatch(lab,mode):
    responses=asyncio.run(invoke(lab,mode,count=8,duplicate=True))
    assert all(r.status_code==200 for r in responses)
    assert totals(lab[0])==(40,(40,1))
    assert lab[0].get('op-a')['state']=='COMMITTED'


@pytest.mark.parametrize('mode',['vulnerable','corrected'])
def test_identity_conflict(lab,mode):
    store,erp,_=lab
    asyncio.run(invoke(lab,mode))
    binding=request(quantity=41).binding('planner-1')
    with pytest.raises(IdentityConflict):
        store.admit(binding,mode,store.snapshot(binding['grant_id']))
    assert totals(store)==(40,(40,1))


@pytest.mark.parametrize('field,value,reason',[
 ('resource','COMP-99','DENY_RESOURCE_NOT_IN_GRANT'),('supplier','SUP-X','DENY_SUPPLIER_NOT_IN_GRANT'),
 ('grant_id','missing','DENY_UNKNOWN_GRANT'),('subject_id','other','DENY_SUBJECT_NOT_IN_GRANT')])
def test_scope(lab,field,value,reason):
    binding=request().binding('planner-1'); binding[field]=value
    row,fresh=lab[0].admit(binding,'corrected')
    assert row['reason']==reason and row['state']=='DENIED'
    assert totals(lab[0])==(0,(0,0))


def test_inactive_fixture(lab):
    with psycopg.connect(dsn('authority','admin'),autocommit=True) as c:
        c.execute("UPDATE grants SET status='INACTIVE'")
    row,_=lab[0].admit(request().binding('planner-1'),'corrected')
    assert row['reason']=='DENY_GRANT_INACTIVE'


@pytest.mark.parametrize('quantity',[0,-1,True,1.0,'40',None])
def test_strict_quantity(quantity):
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        request(quantity=quantity)


@pytest.mark.parametrize('quantity,decision',[(100,'ALLOW'),(101,'DENY')])
def test_limit_edges(lab,quantity,decision):
    row,_=lab[0].admit(request(quantity=quantity).binding('planner-1'),'corrected')
    assert row['decision']==decision
    assert totals(lab[0])[0]==(quantity if decision=='ALLOW' else 0)


def test_atomic_rollback_no_dispatch(lab):
    def fail():
        raise RuntimeError('Injected before reservation COMMIT')
    lab[0].before_commit=fail
    with pytest.raises(RuntimeError):
        asyncio.run(invoke(lab))
    assert lab[0].get('op-a') is None
    assert totals(lab[0])==(0,(0,0))


def test_row_lock_is_database_lock(lab):
    store=lab[0]
    with psycopg.connect(dsn('authority','admin'),autocommit=True) as holder:
        with holder.transaction():
            holder.execute('SELECT * FROM grant_balances FOR UPDATE')
            with ThreadPoolExecutor(1) as pool:
                future=pool.submit(store.admit,request().binding('planner-1'),'corrected')
                deadline=time.monotonic()+3
                locked=False
                while time.monotonic()<deadline:
                    with psycopg.connect(dsn('authority','admin')) as observer:
                        locked=bool(observer.execute("SELECT 1 FROM pg_stat_activity WHERE usename='gw' AND wait_event_type='Lock'").fetchone())
                    if locked:
                        break
                    time.sleep(.02)
                assert locked and not future.done()
                holder.execute('COMMIT')
                assert future.result(timeout=3)[0]['state']=='RESERVED'


def test_unknown_retained_and_confirmed(lab):
    response=asyncio.run(invoke(lab,fault='lost_response'))[0]
    assert response.json()['state']=='PENDING_RECONCILIATION'
    assert totals(lab[0])==(40,(40,1))
    replacement=Store(lab[0].dsn,lab[0].log)  # New process-equivalent store, same durable persistence.
    assert replacement.get('op-a')['state']=='PENDING_RECONCILIATION'
    with pytest.raises(ValueError):
        replacement.transition('op-a','RELEASED')
    async def observe():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=lab[1]),base_url='http://erp') as reader:
            return (await reader.get('/orders',params={'grant_id':'G-2026-001'},headers={'Authorization':'Bearer read'})).json()['orders'][0]
    order=asyncio.run(observe())
    replacement.transition('op-a','COMMITTED',order)
    replacement.transition('op-a','COMMITTED',order)
    assert totals(replacement)==(40,(40,1))


def test_reserved_restart_and_absence_no_release(lab):
    store=lab[0]
    store.admit(request().binding('planner-1'),'corrected')
    restarted=Store(store.dsn,store.log)
    assert restarted.get('op-a')['state']=='RESERVED'
    restarted.transition('op-a','PENDING_RECONCILIATION')
    assert totals(store)==(40,(0,0))
    with pytest.raises(ValueError):
        restarted.transition('op-a','RELEASED',undispatched_proof=True)
    assert totals(store)==(40,(0,0))


def test_closed_never_dispatched_release_once(lab):
    response=asyncio.run(invoke(lab,fault='no_dispatch'))[0]
    assert response.json()['state']=='RELEASED'
    lab[0].transition('op-a','RELEASED',undispatched_proof=True)
    assert totals(lab[0])==(0,(0,0))


def test_vulnerable_admission_and_accounting_once(lab):
    store=lab[0]; binding=request().binding('planner-1')
    row,_=store.admit(binding,'vulnerable',store.snapshot(binding['grant_id']))
    assert row['state']=='ADMITTED_UNRESERVED' and totals(store)==(0,(0,0))
    async def create_order():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=lab[1]),base_url='http://erp') as c:
            return (await c.post('/orders',json=request().model_dump(),headers={'Authorization':'Bearer write'})).json()
    order=asyncio.run(create_order())
    with ThreadPoolExecutor(4) as pool:
        list(pool.map(lambda _:store.transition('op-a','COMMITTED',order),range(4)))
    assert store.snapshot(binding['grant_id'])['charged_quantity']==40


@pytest.mark.parametrize('failure',['timeout','connection','http500'])
def test_generic_uncertainty_never_releases(lab,failure):
    async def transport(request):
        if failure=='timeout':
            raise httpx.ReadTimeout('Engineering transport fault')
        if failure=='connection':
            raise httpx.ConnectError('Engineering transport fault')
        return httpx.Response(500,json={'detail':'Generic failure'})
    app=gateway_app(lab[0],{'client':'planner-1'},'corrected','http://erp','write','read',
                    transport=httpx.MockTransport(transport))
    async def call():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://gw') as c:
            return await c.post('/purchase',json=request().model_dump(),headers={'Authorization':'Bearer client'})
    response=asyncio.run(call())
    assert response.json()['state']=='PENDING_RECONCILIATION'
    assert totals(lab[0])==(40,(0,0))


def test_timeout_http_classification(lab):
    barrier=Barrier(['op-a','op-b','op-c'],.02,EventLog(lab[2]/'schedule.jsonl','harness','test'),'post_read')
    app=gateway_app(lab[0],{'client':'planner-1'},'vulnerable','http://erp','write','read',barrier=barrier)
    async def call():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app),base_url='http://gw') as c:
            return await c.post('/purchase',json=request().model_dump(),headers={'Authorization':'Bearer client'})
    response=asyncio.run(call())
    assert response.status_code==503 and response.json()['detail']=='INVALID_INSTRUMENTED_RUN'
    assert lab[0].get('op-a') is None and totals(lab[0])==(0,(0,0))


def test_barrier_timeout_not_deny(tmp_path):
    async def run():
        barrier=Barrier(['a','b','c'],.02,EventLog(tmp_path/'schedule.jsonl','harness','test'),'post_read')
        with pytest.raises(InvalidSchedule,match='INVALID_INSTRUMENTED_RUN'):
            await barrier.wait('a','attempt',{'charged_quantity':0,'revision':0})
    asyncio.run(run())
    assert 'DENY' not in (tmp_path/'schedule.jsonl').read_text()


@pytest.mark.parametrize('timeout',['nan','inf',0,-1])
def test_timeout_must_be_finite(timeout):
    with pytest.raises(ValueError):
        finite_timeout(timeout)


def test_erp_readonly_and_duplicates(lab):
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=lab[1]),base_url='http://erp') as c:
            payload=request().model_dump()
            assert (await c.post('/orders',json=payload,headers={'Authorization':'Bearer read'})).status_code==403
            first=await c.post('/orders',json=payload,headers={'Authorization':'Bearer write'})
            second=await c.post('/orders',json=payload,headers={'Authorization':'Bearer write'})
            assert first.json()['order_id']==second.json()['order_id']
            payload['quantity']=41
            assert (await c.post('/orders',json=payload,headers={'Authorization':'Bearer write'})).status_code==409
            assert len((await c.get('/orders',params={'grant_id':'G-2026-001'},headers={'Authorization':'Bearer read'})).json()['orders'])==1
    asyncio.run(run())


def test_database_privileges(lab):
    with psycopg.connect(dsn('authority','gw'),autocommit=True) as c:
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            c.execute('UPDATE grants SET max_total_quantity=200')
    with psycopg.connect(dsn('authority','reader'),autocommit=True) as c:
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            c.execute('UPDATE grant_balances SET charged_quantity=0')
    with pytest.raises(psycopg.OperationalError):
        psycopg.connect(dsn('erp','gw'))
