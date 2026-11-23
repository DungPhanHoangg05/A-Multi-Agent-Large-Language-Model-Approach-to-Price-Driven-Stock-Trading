"""Đánh giá backtest serving trên checkpoint đủ common support, tái dùng metric U09."""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from core.free_pilot_statistics import account
from core.unified_analysis.analysis import classified
from core.unified_contracts import day, digest, json_bytes
from core.unified_experiment import validate_outcome
from core.serving_runtime.resources import Resources

VERSION = 'serving_backtest_evaluation_v1'
TABLES = ('predictions','summary','accounts','daily_nav','cycles','contrasts','per_repeat')


def filters(request: dict, plan: list[str], query: dict[str, str]) -> dict:
    """Filter không thay plan/seed/config hoặc nhập support từ run khác."""
    if set(query) - {'methods','baseline','symbol','repeat','start_date','end_date'}:
        raise ValueError('Filter chưa được hỗ trợ')
    methods = query.get('methods',','.join(request['variant_ids'])).split(',')
    if not methods or len(methods) != len(set(methods)) or not set(methods) <= set(plan):
        raise ValueError('Method ngoài execution plan')
    baseline = query.get('baseline','original_fix' if 'original_fix' in plan else 'original_common' if 'original_common' in plan else 'none')
    if baseline != 'none' and (baseline not in ('original_fix','original_common') or baseline not in plan):
        raise ValueError('Baseline chưa được chạy trong job này')
    symbol, repeat = query.get('symbol','all'),query.get('repeat','all')
    if symbol not in ['all',*request['symbols']] or repeat not in ['all',*[str(r) for r in range(request['repeats'])]]:
        raise ValueError('Mã hoặc repeat ngoài request')
    start,end = (day(query.get(k,request[k])) for k in ('start_date','end_date'))
    if not request['start_date'] <= start <= end <= request['end_date']:
        raise ValueError('Cửa sổ filter ngoài request')
    return {'methods':methods,'baseline':baseline,'symbol':symbol,'repeat':repeat,'start_date':start,'end_date':end}


def average(rows: list[dict], key: str) -> float | None:
    """Undefined ở một repeat giữ undefined, không thay bằng zero hoặc bỏ repeat khó."""
    values = [row[key] for row in rows]
    return float(np.mean(values)) if values and all(v is not None for v in values) else None


def prices(root: Path, reservation: dict, outcomes: dict[str, dict], resources: Resources) -> dict[str, pd.DataFrame]:
    """Chỉ gọi sau barrier toàn job; nguồn giá phải khớp resource và outcome đã khóa."""
    resources.verify()
    manifest = resources.document()
    job = reservation['job']
    if digest({'resource_bindings':manifest['bindings'],'points':reservation['points']}) != job['identity']['snapshot_sha256']:
        raise ValueError('Resource snapshot khác job')
    alpha_path = 'outputs/unified_integration/u06_assets_v2/frozen_alpha_manifest.json'
    alpha = json.loads((root/alpha_path).read_bytes())
    result = {}
    for symbol in job['identity']['request']['symbols']:
        source = alpha['causal_sources'][symbol+'/f2026_q3']['prices']
        raw = (root/source).read_bytes()
        if source not in manifest['bindings'] or hashlib.sha256(raw).hexdigest() != manifest['bindings'][source]['sha256']:
            raise ValueError('Giá daily NAV ngoài resource binding')
        frame = pd.DataFrame(json.loads(raw)); frame['Datetime'] = pd.to_datetime(frame.Datetime)
        result[symbol] = frame
        # So nguồn canonical VND sau barrier, không chỉ tin nhãn/P&L trong journal.
        from core.unified_experiment import outcome_from_frame
        vnd = frame.copy(deep=True); vnd[['Open','High','Low','Close']] *= 1000.
        for point in reservation['points']:
            if point['symbol'] == symbol:
                if outcomes[point['id']] != outcome_from_frame(point,vnd,hashlib.sha256(raw).hexdigest()):
                    raise ValueError('Outcome khác giá và oracle canonical')
    return result


def evaluate(reservation: dict, public: dict, outcomes: dict[str, dict], query: dict[str, str],
             price_loader: Any) -> dict[str, Any]:
    """Summary chỉ có khi đủ mọi point/variant/repeat/outcome; filter tính lại cùng cohort."""
    request = public['identity']['request']
    if request['mode'] != 'backtest': raise ValueError('Job không phải backtest')
    selected = filters(request,public['execution_plan'],query)
    points = reservation['points']; by_id = {p['id']:p for p in points}
    for identifier,outcome in outcomes.items():
        if identifier not in by_id: raise ValueError('Outcome ngoài plan')
        validate_outcome(by_id[identifier],outcome)
        count = sum(row['point_id'] == identifier for row in public['rows'])
        if count != len(public['execution_plan'])*request['repeats']:
            raise ValueError('Outcome xuất hiện trước đủ forecast/dependency/repeat')
    chosen = {p['id'] for p in points if selected['start_date'] <= p['cutoff'] <= selected['end_date']
              and selected['symbol'] in ('all',p['symbol'])}
    all_rows = []
    for row in public['rows']:
        outcome = outcomes.get(row['point_id'])
        if row['point_id'] not in chosen or selected['repeat'] not in ('all',str(row['repeat'])): continue
        all_rows.append({**deepcopy(row),'method':row['requested_id'],'date':row['as_of_date'],
            'entry_date':outcome['dates'][1] if outcome else None,'exit_date':outcome['dates'][3] if outcome else None,
            'label_net':outcome['target']['label_net'] if outcome else None,
            'r_net':float(outcome['target']['net_return']) if outcome else None,
            'shared_sha256':public['snapshots'][row['point_id']]['sha256']})
    complete = public['state'] == 'completed' and len(outcomes) == len(points)
    reports = {key:[] for key in TABLES}
    reports['predictions'] = [row for row in all_rows if row['method'] in selected['methods']]
    if complete and chosen:
        frames = price_loader()
        groups = {}
        for row in all_rows:
            groups.setdefault((row['method'],row['symbol'],row['repeat']),[]).append(row)
        for (method,symbol,repeat),group in sorted(groups.items()):
            ledger = account([{**r,'action':r['final_action']} for r in group],frames[symbol])
            key = {'method':method,'symbol':symbol,'repeat':repeat}
            reports['accounts'].append({**key,**{k:v for k,v in ledger.items() if k not in ('dates','daily_nav_vnd','cycles')},
                'undefined_reasons':{k:'ZERO_DENOMINATOR_OR_TOO_FEW_CYCLES' for k in ('cycle_sharpe','cycle_sortino_lpm2') if ledger[k] is None}})
            reports['daily_nav'].extend({**key,'date':date,'nav_vnd':float(nav)} for date,nav in zip(ledger['dates'],ledger['daily_nav_vnd']))
            reports['cycles'].extend({**key,**cycle} for cycle in ledger['cycles'])
        for method in dict.fromkeys(r['method'] for r in all_rows):
            group = [r for r in all_rows if r['method'] == method]
            metrics = []
            for repeat in sorted({r['repeat'] for r in group}):
                rows = [r for r in group if r['repeat'] == repeat]
                metric = classified(rows); metrics.append(metric)
                reports['per_repeat'].append({'method':method,'repeat':repeat,**metric})
            accounts = [a for a in reports['accounts'] if a['method'] == method]
            reports['summary'].append({'method':method,'n_points':len(chosen),'n_forecasts':len(group),'n_accounts':len(accounts),
                'mean_account_return_pct':average(accounts,'return_pct'),
                **{k:average(metrics,k) for k in ('accuracy','balanced_accuracy','mcc','macro_f1','long_rate')},
                **{'mean_'+k:average(accounts,k) for k in ('daily_mdd_pct','cycle_end_mdd_pct','fee_vnd','slippage_vnd','turnover_vnd')},
                'fallback_forecasts':sum(r['fallback_reason'] is not None for r in group),
                'bypass_forecasts':sum(r['bypass_reason'] is not None for r in group),
                'policy_reasons':dict(Counter(r['fallback_reason'] or r['bypass_reason'] or 'RAW_DECISION' for r in group)),
                'undefined_reasons':{k:'UNDEFINED_IN_AT_LEAST_ONE_REPEAT' for k in ('balanced_accuracy','mcc','macro_f1') if average(metrics,k) is None}})
        baseline = next((r for r in reports['summary'] if r['method'] == selected['baseline']),None)
        if baseline is not None:
            reports['contrasts'] = [{'method':r['method'],'baseline':baseline['method'],
                'return_difference_pp':r['mean_account_return_pct']-baseline['mean_account_return_pct'],
                'balanced_accuracy_difference_pp':100*(r['balanced_accuracy']-baseline['balanced_accuracy'])
                    if r['balanced_accuracy'] is not None and baseline['balanced_accuracy'] is not None else None,
                'scope':'SAME_JOB_COMMON_FILTERED_SUPPORT_POINT_ESTIMATE_ONLY; NO_CI_OR_P_VALUE'}
                for r in reports['summary'] if r['method'] in selected['methods'] and r['method'] != baseline['method']]
        for key in TABLES:
            reports[key] = [r for r in reports[key] if r['method'] in selected['methods']]
    repeats = request['repeats'] if selected['repeat'] == 'all' else 1
    result = {'version':VERSION,'kind':'serving_backtest','run_id':public['run_id'],'status':public['state'],
        'worker_alive':public['worker_alive'],'error':public['error'],'retry_at':public.get('retry_at'),
        'progress':public['progress'],'request':request,'execution_plan':public['execution_plan'],'filters':selected,
        'evaluation_status':'COMPLETE' if complete and chosen else 'EMPTY_SUPPORT' if not chosen else 'INCOMPLETE_JOB',
        'coverage':{'planned_points':len(points),'outcome_points':len(outcomes),'filtered_points':len(chosen),
            'filtered_planned_slots':len(chosen)*len(selected['methods'])*repeats,'filtered_complete_slots':len(reports['predictions'])},
        'metric_scope':'FILTERED_COMMON_SUPPORT; MEAN_PER_REPEAT_CLASSIFICATION; MEAN_INDEPENDENT_SYMBOL_REPEAT_ACCOUNTS',
        'units':{'return':'PERCENT_PER_ACCOUNT','r_net':'FRACTION_PER_CYCLE','daily_nav':'VND_DAILY_EOD_PER_ACCOUNT',
                 'accuracy':'FRACTION','drawdown':'PERCENT; DAILY_AND_CYCLE_END_SEPARATE','contrasts':'PERCENTAGE_POINTS'},
        'provenance':{'identity_sha256':public['identity_sha256'],'config_sha256':public['config_sha256'],
            'input_snapshot_sha256':public['identity']['snapshot_sha256'],'support_sha256':public['support_sha256'],
            'source_sha256':public['identity']['config']['source_sha256'],'evaluator_version':VERSION,
            'shared_snapshots':{identifier:public['snapshots'][identifier]['sha256'] for identifier in chosen if identifier in public['snapshots']}},
        'limitations':['EXPLORATORY_NEW_BACKTEST; NOT_U09_PAPER_EVIDENCE','INDEPENDENT_ACCOUNTS_NOT_PORTFOLIO',
                      'NO_ANNUALIZATION_NO_NEW_SIGNIFICANCE_BANDS','NATIVE_CAUSAL_FAIL_WHOLE_SYSTEM_NOT_CERTIFIED'],**reports}
    return json.loads(json_bytes(result))
