"""Kết quả tổng hợp cho DOM; schema thật, không dùng làm bằng chứng dự báo thị trường."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT/'tests')]

from core.serving_contracts import ServingRequest, ServingJob, result_document
from core.serving_registry import MAIN_IDS, registry_document
from core.serving_runtime.resources import default_models
from test_variant_serving import config_fixture
from utils.analysis_ui import messages


def fixture(language: str = 'vi') -> dict:
    """Tám slot cùng point, fallback có khai báo và P&L null trong mode compare."""
    spec = ServingRequest.create({'version':'variant_serving_v1','mode':'compare','variant_ids':list(MAIN_IDS),
        'symbols':['MWG'],'start_date':'2026-07-02','end_date':'2026-07-02','timeframe':'1d',
        'language':'vi','repeats':1,'models':default_models()})
    job = ServingJob.create(spec,config_fixture(spec),'8'*64,'9'*64,
                            run_id='12345678-1234-4234-8234-123456789abc')
    rows = []
    details = {}
    point = 'MWG-2026-07-02'
    for variant in job.document()['execution_plan']:
        fallback = variant in ('bayesian_v1','C2','A_tp_pool','B_semantic')
        rows.append({'point_id':point,'symbol':'MWG','as_of_date':'2026-07-02','repeat':0,
            'requested_id':variant,'executed_id':'original_common' if fallback else variant,
            'raw_prediction':None if fallback else 'SHORT','final_prediction':'SHORT','final_action':'CASH',
            'fallback_reason':'FALLBACK_ORIGINAL' if fallback else None,'bypass_reason':'FALLBACK_ORIGINAL' if fallback else None,
            'support':{'manifest_sha256':'3'*64,'status':'declared_fallback' if fallback else 'supported'},
            'net_return_pct':None,'metric_reason':'NOT_EVALUATED'})
        details[f'forecast/{point}/r0/{variant}'] = {'policy':{'reason':'FALLBACK_ORIGINAL' if fallback else 'RAW_DECISION'},
            'raw_reply':None if fallback else {'confidence':'Cao','justification':'Fixture synthetic.'},
            'context':{'trace':{'synthetic_fixture':True},'aux':{}},'shared_sha256':'a'*64}
    data = result_document(job,'completed',sorted({r['executed_id'] for r in rows}),
        {'points_total':1,'points_complete':1,'decision_slots_total':8,'decision_slots_complete':8,'api_attempts':6},rows,None)
    data.update(worker_alive=False,retry_at=None,policy_details=details,
        input_snapshot_scope='SYNTHETIC_FIXTURE',snapshots={point:{'sha256':'a'*64,'provenance':{'price_end':'2026-07-02'},
        'payload':{**{role+'_report':'Báo cáo synthetic.' for role in ('indicator','pattern','trend','alpha','sentiment')},
                   'causal_alpha':{'projection':{'report':'Alpha common synthetic.'}},
                   'price_prefix':{'Datetime':['2026-07-01','2026-07-02'],'Close':[100.,101.]}}}})
    return {'config':{'messages':messages(language),'language':language,'registry':registry_document(),'runId':data['run_id']},'data':data}


if __name__ == '__main__':
    import json
    print(json.dumps(fixture(),ensure_ascii=False))
