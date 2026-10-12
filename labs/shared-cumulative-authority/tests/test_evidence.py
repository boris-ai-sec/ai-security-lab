import json

import pytest

from lab.common import write_json
from lab.evidence import derive


@pytest.fixture()
def bundle(tmp_path):
    # Synthetic parser fixture only; deliberately 7 units, not an experiment's 80/120 target.
    binding=dict(operation_id='parser-op',grant_id='parser-grant',resource='COMP-17',supplier='SUP-A',quantity=7)
    write_json(tmp_path/'grant.json',dict(grant_id='parser-grant',max_total_quantity=100))
    write_json(tmp_path/'run-manifest.json',dict(run_id='parser-test',purpose='UNIT_FIXTURE',phase='settled',hook='none'))
    write_json(tmp_path/'authority-state.json',dict(initial=dict(operations=[],balances=[dict(charged_quantity=0)]),
        final=dict(operations=[dict(**binding,state='COMMITTED',decision='ALLOW')],balances=[dict(charged_quantity=7)])))
    write_json(tmp_path/'erp-state.json',dict(initial=dict(orders=[]),final=dict(orders=[dict(**binding,order_id=1)])))
    (tmp_path/'requests.jsonl').write_text('\n'.join(json.dumps(dict(event=e,operation_id='parser-op',status_code=200)) for e in ('submitted','response'))+'\n')
    (tmp_path/'decisions.jsonl').write_text(json.dumps(dict(event='decision',operation_id='parser-op',decision='ALLOW',commit_confirmed=True))+'\n')
    (tmp_path/'schedule-events.jsonl').write_text('')
    return tmp_path


def test_independent_measurement_not_expected_total(bundle):
    result=derive(bundle)
    assert result['destination_total']==7 and result['Q']==7
    assert result['allow_count']==1 and result['evidence_complete']


@pytest.mark.parametrize('mutation',['missing','unfinished','timeout','absent_order','wrong_counter','scope'])
def test_evidence_rejects_invalid_bundle(bundle,mutation):
    if mutation=='missing':
        (bundle/'decisions.jsonl').unlink()
    elif mutation=='unfinished':
        path=bundle/'run-manifest.json'; value=json.loads(path.read_text()); value['phase']='started'; write_json(path,value)
    elif mutation=='timeout':
        (bundle/'schedule-events.jsonl').write_text(json.dumps(dict(event='timeout'))+'\n')
    elif mutation in ('absent_order','scope'):
        path=bundle/'erp-state.json'; value=json.loads(path.read_text())
        if mutation=='absent_order':
            value['final']['orders']=[]
        else:
            value['final']['orders'][0]['resource']='COMP-99'
        write_json(path,value)
    else:
        path=bundle/'authority-state.json'; value=json.loads(path.read_text()); value['final']['balances'][0]['charged_quantity']=8; write_json(path,value)
    with pytest.raises(ValueError):
        derive(bundle)
