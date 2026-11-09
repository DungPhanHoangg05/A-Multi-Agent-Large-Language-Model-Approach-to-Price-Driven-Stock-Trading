"""Consumer H07/H08 offline: seal chứng cứ, hạch toán pilot và phân tích ghép cặp."""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
import csv
import hashlib
import io
import json
import platform
from pathlib import Path
import subprocess
from typing import Any

import numpy as np
import pandas as pd

from core.free_pilot_assets import DIRECTORY, DOC, INPUTS, PROTOCOL, PilotData
from core.free_pilot_manager import preflight, snapshot
from core.free_pilot_recovery import verify_repaired_decision, valid_decision_reply
from core.free_pilot_runtime import identity
from core.free_pilot_statistics import account, bootstrap, classification, cycle_ratios
from core.historical_evaluation_journal import RunBook, load, save
from core.historical_evaluation_protocol import PRIMARY, CORE4, DONOR, binding, digest
from core.prior_run_lock import safe_path

ACCEPTANCE = DOC / "free_pilot_h07_acceptance.json"
ANALYSIS = DOC / "free_pilot_h08_analysis.json"
OUT = DIRECTORY / "analysis"
SOURCES = ("core/free_pilot_analysis.py", "core/free_pilot_statistics.py", "scripts/analyze_free_pilot.py",
           "tests/test_free_pilot_statistics.py", "tests/test_free_pilot_analysis.py")


def normalized(value: Any) -> Any:
    """Xuất JSON thuần, null cho undefined; không rò NumPy scalar hoặc NaN."""
    if isinstance(value, dict): return {str(k): normalized(v) for k,v in value.items()}
    if isinstance(value, (list,tuple)): return [normalized(v) for v in value]
    if isinstance(value, np.ndarray): return normalized(value.tolist())
    if isinstance(value, np.generic): return normalized(value.item())
    if isinstance(value, float) and not np.isfinite(value): return None
    return value


def verify_binding(root: Path, record: dict) -> None:
    """Không nhận checksum tự khai nếu byte nguồn không khớp."""
    if binding(root, record["path"]) != record:
        raise ValueError("Evidence khác receipt: " + record["path"])


def output(book: RunBook, slot: str) -> tuple[dict, dict]:
    """Chỉ đọc attempt complete có identity/input/output hash hợp lệ."""
    if not book.complete(slot): raise ValueError("Slot chưa complete: " + slot)
    doc = load(book.path(slot))
    if digest(doc["inputs"]) != doc["inputs_sha256"]: raise ValueError("Inputs khác hash")
    return doc["inputs"], doc["attempts"][-1]["output"]


def accept(root: Path) -> tuple[dict, PilotData, list[dict]]:
    """Nghiệm thu bằng hash closure và cold receipt đã PASS; không lặp lại model/API gate."""
    preflight(root)
    directory = root / DIRECTORY
    managed = load(directory / "manager/collection_receipt.json")
    if managed["status"] != "P05_COLD_PASS": raise ValueError("Manager chưa cold PASS")
    verify_binding(root, managed["supervisor"]); verify_binding(root, managed["cold_receipt"])
    if digest(snapshot(directory)) != managed["http_usage_sha256"]: raise ValueError("HTTP/usage đổi sau cold verify")
    cold = load(directory / "pilot_collection_receipt.json")
    book = RunBook(directory, identity(root), verify_only=True)
    if cold["identity"] != identity(root) or cold["run_uuid"] != book.uuid or managed["run_uuid"] != book.uuid:
        raise ValueError("Receipt khác run/model/runtime")
    for folder,key in (("slots","slots"),("usage","usage")):
        actual = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (directory/folder).glob('*.json')}
        if actual != cold[key]: raise ValueError("Tập file khác cold receipt: " + folder)
    units = load(root / INPUTS)["units"]
    if len(units)!=48 or len({u['id'] for u in units})!=48: raise ValueError("Không đủ48 ID")
    expected = {"shared_manifest"}
    for unit in units:
        expected.update({"shared/"+unit['id'],"label/"+unit['id']})
        expected.update("pilot/"+unit['id']+"/"+branch for branch in (*PRIMARY,'Fact_Anchor'))
        expected.update(f"graph/{unit['symbol']}-{unit['date']}/u0/{role}" for role in ('indicator','pattern','trend','full'))
    # Smoke có12 slot riêng, không nhập vào N48.
    actual_research=set()
    for path in (directory/'slots').glob('*.json'):
        doc=load(path)
        if not book.complete(doc['slot']): raise ValueError("Còn pending/unknown")
        if not (doc['slot'].startswith(('smoke/','graph/FPT-2023-06-23/')) or doc['slot']=='shared/smoke_FPT_2023_06_23'):
            actual_research.add(doc['slot'])
    if actual_research != expected: raise ValueError("Research thiếu/thừa slot so48×7")
    _, manifest = output(book,'shared_manifest')
    data=PilotData(root,units)
    forecasts_done=lambda uid: all(book.complete('pilot/'+uid+'/'+b) for b in (*PRIMARY,'Fact_Anchor'))
    rows=[]; prior_details=[]; prompt_max=0; schema_repairs=0
    for unit in units:
        _, shared = output(book,'shared/'+unit['id'])
        if digest(shared)!=manifest['shared'][unit['id']]: raise ValueError("Shared khác seal")
        label_inputs,label=output(book,'label/'+unit['id'])
        if label_inputs != {'unit':unit,'forecast_complete':True}: raise ValueError("Label parent không khớp")
        cutoff=(pd.Timestamp(unit['exit_date'])+pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        actual_label=data.label(unit['symbol'],unit['date'],as_of=cutoff,forecast_done=forecasts_done)
        if actual_label!=label: raise ValueError("Label khác giá/hàm engine")
        outputs={b:output(book,'pilot/'+unit['id']+'/'+b) for b in (*PRIMARY,'Fact_Anchor')}
        original=outputs['Original_common'][1]
        for branch,(parents,result) in outputs.items():
            if parents['shared']!=digest(shared) or parents['org']!=unit['org'] or parents['smoke']:
                raise ValueError("Không cùng shared/org hoặc lẫn smoke")
            response=result['llm']; request=parents['request']
            if response is not None:
                verify_repaired_decision(book,response,branch,fixture=False,request=request)
                prompt_max=max(prompt_max,len(request['messages'][0]['content']))
                if response.get('schema_repair'):
                    from core.free_pilot_recovery import repair_request
                    prompt_max=max(prompt_max,len(repair_request(request)[0]['messages'][0]['content']))
                    schema_repairs+=1
            elif branch in ('Original_common','Fact_Anchor'):
                raise ValueError("Original/anchor thiếu response")
            elif branch=='MT_BICL':
                if not result['policy']['bypass']: raise ValueError("MT thiếu reply mà không bypass")
            else:
                if not parents['prior'].get('fallback') or result['fallback_original_sha256']!=digest(original) or result['final_action']!=original['final_action']:
                    raise ValueError("Fallback không đúng Original")
            if result['final_action'] not in ('LONG','CASH'): raise ValueError("Action invalid")
            policy=result.get('policy',result.get('anchor',{}).get('policy',{}))
            if policy and policy['final_action']!=result['final_action']: raise ValueError("Policy khác action")
            if branch in PRIMARY:
                prior=parents['prior']
                eligible=policy.get('eligible')
                if 'evidence' in prior:
                    eligible=not bool(prior.get('fallback'))
                elif 'retrieval' in prior:
                    eligible=bool(prior['retrieval']['tasks'])
                prior_details.append({'id':unit['id'],'method':branch,'prior':prior,
                    'policy':policy,'anchor_facts_valid':outputs['Fact_Anchor'][1]['anchor']['policy']['fact_assertions_valid']})
                rows.append({'id':unit['id'],'symbol':unit['symbol'],'year':int(unit['date'][:4]),'date':unit['date'],
                    'entry_date':unit['entry_date'],'exit_date':unit['exit_date'],'method':branch,
                    'action':result['final_action'],'r_net':label['r_net'],'y':label['y'],
                    'shared_sha256':digest(shared),'eligible':eligible,
                    'bypass':bool(policy.get('bypass',False)),'policy_reason':policy.get('reason'),
                    'facts_valid':policy.get('fact_assertions_valid') if response is not None else None,'raw_action':policy.get('raw_proposed_action',response['reply']['decision'] if response else None),
                    'anchor_action':policy.get('anchor_action'),'fallback_original':bool(prior.get('fallback',False)),
                    'new_decision_llm':response is not None,'schema_repaired':bool(response and response.get('schema_repair'))})
    records={p.relative_to(directory).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
             for folder in ('slots','usage','http','images') for p in sorted((directory/folder).rglob('*')) if p.is_file()}
    seal={'status':'PASS','scope':'H07_PILOT48_EVIDENCE_SEALED_BEFORE_H08','run_uuid':book.uuid,'records':records}
    seal_path=directory/'h07_collection_manifest.json'
    if seal_path.exists() and load(seal_path)!=seal: raise ValueError("Manifest H07 đã khóa khác byte")
    save(seal_path,seal)
    receipt={'status':'PASS','scope':'H07_PILOT_ONLY_NOT_FULL_1020','run_uuid':book.uuid,'planned_points':48,
             'shared_states':48,'forecast_slots':336,'labels':48,'latest_unknown':0,'paired_shared_pass':True,
             'fresh_label_engine_pass':True,'cold_gate':'REUSED_P05_AFTER_SOURCE_AND_EVIDENCE_HASH_MATCH',
             'manager_receipt':binding(root,DIRECTORY/'manager/collection_receipt.json'),
             'manifest':binding(root,seal_path.relative_to(root)),'identity':identity(root),
             'prompt_max_chars':prompt_max,'schema_repaired_valid_forecasts':schema_repairs,
             'economic_acceptance':'PENDING_EXECUTION_DATA','quality':'VENDOR_SERIES_LIMITED'}
    if (root/ACCEPTANCE).exists() and load(root/ACCEPTANCE)!=receipt: raise ValueError("Receipt nghiệm thu đã khóa khác nguồn")
    save(root/ACCEPTANCE,receipt)
    # Sidecar dẫn toàn gate/stats/examples đã dùng; không dựng lại bank sau outcome.
    (directory/'analysis').mkdir(exist_ok=True)
    save(directory/'analysis/prior_diagnostics.json',{'scope':'FROZEN_JOURNAL_PROOFS','records':prior_details})
    return receipt,data,rows


def telemetry(root: Path) -> dict:
    """Chỉ tính request mới, tách smoke/research/repair; không double-count carry-over."""
    groups={}
    book=RunBook(root/DIRECTORY,identity(root),verify_only=True)
    documents=[load(p) for p in (book.directory/'slots').glob('*.json')]
    by_attempt={a['attempt_id']:doc for doc in documents for a in doc['attempts']}
    for path in sorted((root/DIRECTORY/'usage').glob('org*.json')):
        for row in json.loads(path.read_bytes())['requests']:
            if row.get('carry_over'): continue
            phase='smoke' if row.get('point_id','').startswith('FPT-2023-06-23') else 'research'
            key=phase+'/'+row.get('branch_id','unknown')
            group=groups.setdefault(key,{'requests':0,'http_status':Counter(),'actual_tokens':0,'charged_or_reserved_tokens':0,
                                         'latencies':[],'schema_repair_requests':0,'invalid_decision_200':0})
            group['requests']+=1; group['http_status'][str(row['status'])]+=1
            group['actual_tokens']+=row.get('total_tokens') or 0
            group['charged_or_reserved_tokens']+=row.get('total_tokens') or row['reserved_tokens']
            group['schema_repair_requests']+=int(bool(row.get('pilot_schema_repair')))
            if row.get('latency_seconds') is not None: group['latencies'].append(float(row['latency_seconds']))
            if row['status']==200 and row.get('branch_id') not in ('pattern','trend'):
                slot=by_attempt[row['checkpoint_attempt_id']]
                group['invalid_decision_200']+=int(not valid_decision_reply(book,slot,row))
    for group in groups.values():
        latency=group.pop('latencies')
        group['latency_seconds_sum']=float(sum(latency))
        group['latency_seconds_median']=float(np.median(latency)) if latency else None
        group['latency_seconds_p95']=float(np.quantile(latency,.95)) if latency else None
        group['http_status']=dict(group['http_status'])
    return groups


def runtime_versions() -> dict:
    """Ghi đúng runtime consumer để tránh nhận cold hash từ phiên bản thống kê khác."""
    import matplotlib
    return {'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,'matplotlib':matplotlib.__version__}


def tensor(rows: list[dict]) -> tuple[np.ndarray,np.ndarray,np.ndarray]:
    """Giữ năm×ngày×mã×method chung; không đổi sample theo action hoặc payoff."""
    dates={year:sorted({r['date'] for r in rows if r['year']==year}) for year in (2023,2024)}
    if any(len(v)!=6 for v in dates.values()): raise ValueError("Mỗi năm cần đúng6 selected date")
    a=np.zeros((2,6,4,6),dtype=bool); returns=np.zeros((2,6,4)); truth=np.zeros((2,6,4),dtype=bool)
    seen=set()
    for row in rows:
        y=(2023,2024).index(row['year']); d=dates[row['year']].index(row['date']); s=CORE4.index(row['symbol']); m=PRIMARY.index(row['method'])
        key=y,d,s,m
        if key in seen: raise ValueError("Trùng point/method")
        if any((y,d,s,j) in seen for j in range(6)) and (returns[y,d,s]!=row['r_net'] or truth[y,d,s]!=row['y']):
            raise ValueError("Các phương pháp không cùng nhãn/return point")
        seen.add(key); a[key]=row['action']=='LONG'; returns[y,d,s]=row['r_net']; truth[y,d,s]=row['y']
    if len(seen)!=288: raise ValueError("Không đủ48×6 primary")
    return a,returns,truth


def sensitivities(rows: list[dict]) -> dict:
    """Leave-one-date/symbol-out trên cùng panel; không chọn subgroup thắng để kết luận."""
    result={}
    for dimension in ('date','symbol'):
        result[dimension]=[]
        for excluded in sorted({r[dimension] for r in rows}):
            reduced=[r for r in rows if r[dimension]!=excluded]
            methods={}
            balanced={}
            for method in PRIMARY:
                groups={}
                method_rows=[r for r in reduced if r['method']==method]
                for row in reduced:
                    if row['method']==method: groups.setdefault((row['year'],row['symbol']),[]).append(row)
                methods[method]=float(np.mean([(np.prod([1.+(r['r_net'] if r['action']=='LONG' else 0.) for r in group])-1.)*100. for group in groups.values()]))
                balanced[method]=classification([r['action']=='LONG' for r in method_rows],[r['y'] for r in method_rows])['balanced_accuracy']
            result[dimension].append({'excluded':excluded,'D_pp':{m:methods[m]-methods['Original_common'] for m in PRIMARY[1:]},
                'BA_D_pp':{m:(balanced[m]-balanced['Original_common'])*100. if balanced[m] is not None and balanced['Original_common'] is not None else None for m in PRIMARY[1:]}})
    return result


def write_csv(path: Path, rows: list[dict]) -> None:
    """CSV UTF8, chỉ scalar và tên cột rõ đơn vị; không đổi số liệu để hiển thị."""
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(normalized(rows))


def reference_fix(root: Path, destination: Path) -> dict:
    """Dẫn Full102 riêng bằng blob Git pinned; tuyệt đối không trừ với return pilot48."""
    name='outputs/revision/final_baselines_v1/main_comparison.csv'
    tree=subprocess.check_output(['git','ls-tree',DONOR,name],cwd=root).decode().split()
    blob=tree[2]; raw=subprocess.check_output(['git','cat-file','blob',blob],cwd=root)
    destination.write_bytes(raw)
    full=next(r for r in csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))) if r['variant']=='AS')
    return {'commit':DONOR,'path':name,'blob':blob,'sha256':hashlib.sha256(raw).hexdigest(),
            'n':int(full['n_valid']),'n_symbols':int(full['n_symbols']),'n_accounts':int(full['n_accounts']),
            'accuracy_pct':float(full['accuracy'])*100.,'balanced_accuracy_pct':float(full['balanced_accuracy'])*100.,
            'mean_account_return_pct':float(full['mean_account_net_return_pct']),
            'comparison':'REFERENCE_ONLY_DIFFERENT_COHORT_PROMPT_CAP_OPTIONS; NO_PAIRED_DIFFERENCE'}


def analyze(root: Path, destination: Path | None = None) -> dict:
    """Phân tích đủ panel sau nghiệm thu, không API/train hoặc thay H07 evidence."""
    receipt,data,rows=accept(root)
    dest=destination or root/OUT
    dest.mkdir(parents=True,exist_ok=True)
    frames=data.frames
    accounts=[]; curve=[]; cycles=[]; summaries=[]; stratified=[]
    for method in PRIMARY:
        method_rows=[r for r in rows if r['method']==method]
        for year in (2023,2024):
            for symbol in CORE4:
                group=[r for r in method_rows if r['year']==year and r['symbol']==symbol]
                ledger=account(group,frames[symbol])
                curve.extend({'method':method,'symbol':symbol,'year':year,'date':day,'nav_vnd':nav} for day,nav in zip(ledger['dates'],ledger['daily_nav_vnd']))
                cycles.extend(ledger['cycles'])
                accounts.append({'method':method,'symbol':symbol,'year':year,
                    **{k:v for k,v in ledger.items() if k not in ('dates','daily_nav_vnd','cycles')},
                    **classification([r['action']=='LONG' for r in group],[r['y'] for r in group],planned=6)})
        all_accounts=[r for r in accounts if r['method']==method]
        metrics=classification([r['action']=='LONG' for r in method_rows],[r['y'] for r in method_rows],planned=48)
        summaries.append({'method':method,'mean_account_return_pct':float(np.mean([a['return_pct'] for a in all_accounts])),
            'mean_daily_mdd_pct':float(np.mean([a['daily_mdd_pct'] for a in all_accounts])),
            'worst_account_daily_mdd_pct':max(a['daily_mdd_pct'] for a in all_accounts),
            'long_count':sum(r['action']=='LONG' for r in method_rows),'fallback_original':sum(r['fallback_original'] for r in method_rows),
            'bypass':sum(r['bypass'] for r in method_rows),'eligible':sum(r['eligible'] is True for r in method_rows),
            'facts_invalid':sum(r['facts_valid'] is False for r in method_rows),
            'new_decision_llm':sum(r['new_decision_llm'] for r in method_rows),'schema_repaired':sum(r['schema_repaired'] for r in method_rows),
            **metrics,**cycle_ratios([r['r_net'] if r['action']=='LONG' else 0. for r in method_rows])})
        for dim in ('symbol','year'):
            for value in sorted({r[dim] for r in method_rows}):
                group=[r for r in method_rows if r[dim]==value]
                stratified.append({'method':method,'dimension':dim,'group':value,
                    **classification([r['action']=='LONG' for r in group],[r['y'] for r in group],planned=12 if dim=='symbol' else 24)})
    a,r,y=tensor(rows); intervals=bootstrap(a,r,y)
    base=summaries[0]['mean_account_return_pct']
    for i,summary in enumerate(summaries):
        summary['D_vs_original_pp']=summary['mean_account_return_pct']-base
        summary['D_ci95_pp']=None if i==0 or intervals['return']['ci'] is None else intervals['return']['ci'][i-1]
    source_stats=load(root/DOC/'free_pilot_audit.json')['bank']
    results={'status':'H08_ANALYSIS_COMPLETE','scope':'HISTORICAL_EXPLORATORY_CONDITIONAL_ON_SHARED_REPORTS',
        'run_uuid':receipt['run_uuid'],'points':48,'dates':sorted({x['date'] for x in rows}),'years':[2023,2024],
        'accounts_per_method':8,'primary':list(PRIMARY),'summary':summaries,'accounts':accounts,'stratified':stratified,
        'bootstrap':intervals,'sensitivity':sensitivities(rows),'coverage':{m:dict(Counter(str(x['policy_reason']) for x in rows if x['method']==m)) for m in PRIMARY},
        'MT_raw_anchor_final':dict(Counter(str(x['raw_action'])+'→'+str(x['anchor_action'])+'→'+x['action'] for x in rows if x['method']=='MT_BICL')),
        'telemetry':telemetry(root),'bank_provenance':source_stats,'shared_strata':{'new':48,'reused':0},
        'reference_fix_102':reference_fix(root,dest/'reference_fix_102.csv'),
        'cash_reference':{'mean_account_return_pct':0.,**classification(np.zeros(48,dtype=bool),y.reshape(-1),planned=48)},
        'definitions':{'return':'MEAN_8_SYMBOL_YEAR_ACCOUNTS_NOT_PORTFOLIO','mdd':'EOD_NAV_WITH_INITIAL_CAPITAL',
            'exposure':'3_HELD_SESSIONS_PER_LONG_OVER_FULL_SELECTED_DATE_WINDOW','f1':'POSITIVE_NET_UP_CLASS',
            'turnover':'QUOTED_BUY_PLUS_SELL_NOTIONAL; RATIO_OVER_INITIAL_CAPITAL',
            'sortino':'MEAN_CYCLE_RETURN_OVER_RMS_ALL_CYCLE_NEGATIVE_PART_TARGET0','annualization':None},
        'limitations':['VENDOR_SERIES_LIMITED','PENDING_EXECUTION_DATA','NEWS_CONTENT_PIT_NOT_CERTIFIED',
            'EXPOSED_2023_2024','ONE_LLM_REPEAT_NO_LLM_VARIANCE_ESTIMATE','FROZEN_BAYES_BANK_VS_UPDATING_MT_NUMERIC_CONTEXT',
            'BOOTSTRAP_SMALL_SAMPLE_SENSITIVITY_NOT_SUPERIORITY_OR_COVERAGE_CERTIFICATION']}
    mt=[x for x in rows if x['method']=='MT_BICL']
    anchor_accounts=[]
    for year in (2023,2024):
        for symbol in CORE4:
            group=[{**x,'action':x['anchor_action']} for x in mt if x['year']==year and x['symbol']==symbol]
            anchor_accounts.append(account(group,frames[symbol])['return_pct'])
    results['Fact_Anchor_diagnostic']={'not_primary_family':True,'mean_account_return_pct':float(np.mean(anchor_accounts)),
        'MT_same_final_action_count':sum(x['action']==x['anchor_action'] for x in mt),
        'MT_eligible_changed_raw_proposal_veto_count':sum(x['new_decision_llm'] and x['raw_action'] is not None and
            ('LONG' if x['raw_action']=='LONG' else 'CASH')!=x['action'] for x in mt),
        **classification([x['anchor_action']=='LONG' for x in mt],[x['y'] for x in mt],planned=48)}
    results=normalized(results)
    save(dest/'results.json',results)
    write_csv(dest/'predictions.csv',rows)
    write_csv(dest/'cycles.csv',cycles)
    write_csv(dest/'daily_nav.csv',curve)
    write_csv(dest/'accounts.csv',[{k:v for k,v in x.items() if not isinstance(v,(dict,list))} for x in accounts])
    write_csv(dest/'summary.csv',[{**{k:v for k,v in x.items() if not isinstance(v,(dict,list)) and k!='D_ci95_pp'},
        'D_ci95_low_pp':x['D_ci95_pp'][0] if x['D_ci95_pp'] else None,
        'D_ci95_high_pp':x['D_ci95_pp'][1] if x['D_ci95_pp'] else None} for x in summaries])
    write_csv(dest/'classification_by_group.csv',[{'method':x['method'],'dimension':x.get('dimension','pooled'),
        'group':x.get('group','all'),**{k:v for k,v in x.items() if k in ('n_planned','n_complete','accuracy','balanced_accuracy','mcc','f1_positive','support_up','support_down')},
        'tn':x['confusion_matrix'][0][0],'fp':x['confusion_matrix'][0][1],
        'fn':x['confusion_matrix'][1][0],'tp':x['confusion_matrix'][1][1],
        **{'n_defined_'+k:v for k,v in x['n_defined'].items()}} for x in [*summaries,*stratified]])
    # Copy cùng sidecar vào thư mục recheck để cold consumer so đủ artifact.
    prior_raw=(root/OUT/'prior_diagnostics.json').read_bytes()
    (dest/'prior_diagnostics.json').write_bytes(prior_raw)
    return results


def report(results: dict, destination: Path) -> None:
    """Bảng phương pháp và figure xuất bản; không biến sensitivity interval thành superiority."""
    def number(value: Any, digits: int=3) -> str:
        return 'NA' if value is None else f'{value:.{digits}f}'
    lines=['# H08 — Kết quả pilot48','',
        'Historical exploratory; có điều kiện trên shared reports đã lưu. Một repeat, không ước lượng variance LLM.',
        'Return là bình quân đều tám account mã/năm, không phải portfolio return. Phí/slippage hai chiều; SHORT=CASH.',
        '', '| Phương pháp | Return % | D so Original (đpt) | Band95% D | Accuracy % | BA % | MCC | F1 UP | LONG |',
        '| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |']
    for row in results['summary']:
        ci=row['D_ci95_pp']; band='—' if ci is None else '['+number(ci[0])+'; '+number(ci[1])+']'
        lines.append('| '+' | '.join([row['method'],number(row['mean_account_return_pct']),number(row['D_vs_original_pp']),band,
            number(row['accuracy']*100. if row['accuracy'] is not None else None),
            number(row['balanced_accuracy']*100. if row['balanced_accuracy'] is not None else None),
            number(row['mcc']),number(row['f1_positive']),str(row['long_count'])])+' |')
    lines += ['', 'Band là centered max-deviation cho đủ năm contrast,10.000 circular selected-date draws L2 trong từng năm, seed20261109.',
        'Đây là độ nhạy mẫu nhỏ, chưa chứng nhận simultaneous coverage, superiority hoặc profitability.',
        '', '| Phương pháp | Prior có examples / gate active / MT eligible | Bypass | Fallback Original | Gọi Decision mới | Forecast qua sửa schema |',
        '| --- | ---: | ---: | ---: | ---: | ---: |']
    for row in results['summary']:
        lines.append(f"| {row['method']} | {row['eligible']} | {row['bypass']} | {row['fallback_original']} | {row['new_decision_llm']} | {row['schema_repaired']} |")
    ba=results['bootstrap']['balanced_accuracy']
    anchor=results['Fact_Anchor_diagnostic']
    lines += ['',f"BA family: {ba['joint_finite_draws']}/10000 draw joint finite; mất class/nonfinite {ba['lost_class_or_nonfinite_draws']}; status {ba['status']}.",
        f"MT có {anchor['MT_same_final_action_count']}/48 action cuối trùng Fact_Anchor; numeric veto bác {anchor['MT_eligible_changed_raw_proposal_veto_count']} đề xuất khác a0. Không quy toàn bộ chênh so Original cho student.",
        'CASH diagnostic: return0%, accuracy '+number(results['cash_reference']['accuracy']*100.)+'%, BA50%; nằm ngoài sáu primary/family.',
        '', 'Bốn mã,12 ngày thực, hai block năm. Sharpe/Sortino chu kỳ theo định nghĩa JSON; mọi annualized metric=null.',
        'EOD MDD, exposure, turnover/phí và vốn giữa query có trong accounts.csv, cycles.csv và daily_nav.csv.',
        'Leave-one-date/symbol-out và số liệu per-symbol/year có trong results.json; không chọn subgroup thuận lợi.',
        '', '## Tham chiếu fix riêng', '']
    ref=results['reference_fix_102']
    lines += [f"Full fix: N={ref['n']},9 mã/51 account, return bình quân {number(ref['mean_account_return_pct'])}%, accuracy {number(ref['accuracy_pct'])}%, BA {number(ref['balanced_accuracy_pct'])}%.",
        'Cohort/prompt/cap/options khác pilot48; bridge OFF. Không tính chênh return ghép cặp giữa hai bảng.',
        '', '## Giới hạn', '', 'VENDOR_SERIES_LIMITED; PENDING_EXECUTION_DATA; news content PIT chưa chứng nhận. Bank Bayesian frozen852 có nguồn giá riêng, MT dùng numeric context cập nhật; chênh lệch không chỉ do kiến trúc student.',
        '2023–2024 đã exposed; không suy rộng từ kết quả conditional trên48 điểm sang full1.020 hoặc thị trường/live fills.',
        '', '## Dữ liệu xuất', '', '[Summary](summary.csv), [48 accounts](accounts.csv), [288 predictions](predictions.csv), [cycle ledger](cycles.csv), [EOD NAV](daily_nav.csv), [JSON đầy đủ](results.json).',
        '', '![Band D](return_contrasts.png)', '']
    (destination/'report.md').write_text('\n'.join(lines),encoding='utf-8')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['svg.hashsalt']='free_pilot_h08'
    rows=results['summary'][1:]
    point=np.array([r['D_vs_original_pp'] for r in rows])
    width=results['bootstrap']['return']['half_width']
    fig,ax=plt.subplots(figsize=(9,4.7),layout='constrained')
    ax.errorbar(point,np.arange(5),xerr=width,fmt='o',capsize=5,color='#176b87',markersize=7)
    ax.axvline(0,color='#777777',linewidth=1)
    ax.set_yticks(np.arange(5),[r['method'] for r in rows]); ax.invert_yaxis()
    ax.set_xlabel('D so Original_common (điểm phần trăm return bình quân tám account)')
    ax.set_title('Pilot48 — band mô tả độ nhạy, không chứng nhận superiority')
    ax.grid(axis='x',alpha=.2)
    fig.savefig(destination/'return_contrasts.png',dpi=170)
    fig.savefig(destination/'return_contrasts.svg',metadata={'Date':None})
    plt.close(fig)


def run_analysis(root: Path, destination: Path | None = None) -> dict:
    """Seal source/output H08, đủ artifacts để consumer lạnh tái dựng và đối soát."""
    before=snapshot(root/DIRECTORY)
    dest=destination or root/OUT
    results=analyze(root,dest)
    report(results,dest)
    if snapshot(root/DIRECTORY)!=before: raise ValueError("H08 đã đổi HTTP/usage")
    receipt={'status':'H08_PASS','run_uuid':results['run_uuid'],'h07':binding(root,ACCEPTANCE),
             'sources':{name:binding(root,name) for name in SOURCES},'runtime':runtime_versions(),
             'artifacts':{p.name:binding(root,p.relative_to(root)) for p in sorted(dest.iterdir()) if p.is_file()},
             'new_api_calls':0,'teacher_student_fit':False,'H09':'PENDING'}
    if destination is None: save(root/ANALYSIS,receipt)
    return receipt
