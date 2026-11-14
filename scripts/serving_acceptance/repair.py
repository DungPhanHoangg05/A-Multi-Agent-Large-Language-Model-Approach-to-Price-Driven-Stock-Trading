"""Nghiệm thu form realtime 1D, tiến trình từng agent và cửa sổ kết quả Original/BICL."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
import json
import py_compile
import re
import subprocess
import sys
import zipfile

from scripts.serving_acceptance import live,timeframes
from scripts.serving_acceptance.evidence import binding,runtime

ROOT,DOC,RECEIPT = live.ROOT,live.DOC,live.RECEIPT
BASE = '6ba5cfea'
PACKAGE = DOC/'serving_daily_analysis_checks.zip'
WORK = ROOT/'tmp/f11_daily_analysis'
PLANS = [('tests/serving_live','test_*.py'),('tests','test_realtime_decision_budget.py'),('tests','test_realtime_index.py'),
    ('tests','test_realtime_sources.py'),('tests','test_original_fix_parity.py'),('tests','test_decision_prior_integration.py'),
    ('tests','test_bayesian_prompt_budget.py'),('tests/analysis_ui','test_*.py'),('tests','test_web_json_serialization.py'),
    ('tests/serving_integration','test_*.py'),('tests','test_unified_execution_leakage.py'),
    ('tests','test_unified_preflight_leakage.py'),('tests/unified_live','test_leakage.py')]


def sources() -> dict:
    """Gồm test mới ở root và helper lỗi; không khóa ảnh người dùng sinh ngoài phạm vi task."""
    result = live.sources()
    for folder,pattern in PLANS:
        if '*' not in pattern:
            name = folder+'/'+pattern; result[name] = binding((ROOT/name).read_bytes())
    result['tests/.gitattributes'] = binding((ROOT/'tests/.gitattributes').read_bytes())
    return dict(sorted(result.items()))


def historical() -> dict:
    """Giữ nguyên gói đa khung/daily, paper và bằng chứng scientific cũ."""
    result = timeframes.historical()
    name = 'docs/plan/week12/serving_timeframe_checks.zip'
    expected = subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
    if (ROOT/name).read_bytes()!=expected: raise ValueError('QA timeframe lịch sử đã đổi')
    repair_name = 'docs/plan/week12/serving_realtime_repair_checks.zip'
    previous = subprocess.check_output(['git','show',BASE+':'+repair_name],cwd=ROOT)
    if (ROOT/repair_name).read_bytes()!=previous: raise ValueError('QA sửa realtime trước đó đã đổi')
    return {**result,'timeframe_qa_unchanged':binding(expected),'repair_qa_unchanged':binding(previous)}


def suite(plan: tuple[str,str]) -> tuple[str,dict]:
    """Process riêng, log stdout/stderr thô; chỉ chạy các caller liên quan."""
    folder,pattern = plan
    command = [sys.executable,'-X','utf8','-m','unittest','discover','-s',folder,'-p',pattern,'-v']
    done = subprocess.run(command,cwd=ROOT,capture_output=True); raw = done.stdout+b'\n'+done.stderr
    name = folder.replace('/','_')+'_'+pattern.replace('*','all').replace('.py','.log')
    (WORK/name).write_bytes(raw); count = re.search(rb'Ran (\d+) tests?',done.stderr)
    return name,{'passed':not done.returncode and bool(count) and bool(re.search(rb'\nOK\s*$',raw)) and b'skipped=' not in raw,
        'tests':int(count[1]) if count else 0,'command':command[1:],'log':binding(raw)}


def run() -> dict:
    """Chỉ kiểm caller/projection/progress đổi, không gọi Groq hoặc thị trường thật."""
    WORK.mkdir(parents=True,exist_ok=True)
    sealed = sources(); environment = runtime(ROOT); integrity = historical()
    names = subprocess.check_output(['git','diff',BASE,'--name-only','--','*.py'],cwd=ROOT).decode().splitlines()
    names += subprocess.check_output(['git','ls-files','--others','--exclude-standard','--','*.py'],cwd=ROOT).decode().splitlines()
    compiled = sorted(set(names))
    for name in compiled: py_compile.compile(str(ROOT/name),doraise=True)
    results = {}
    with ThreadPoolExecutor(max_workers=2) as pool:
        for future in as_completed([pool.submit(suite,plan) for plan in PLANS]):
            name,row = future.result(); results[name] = row; print(name,row['passed'],row['tests'],flush=True)
            (WORK/'test_results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    command = ['node','--test','tests/js/analysis_ui.test.mjs']
    done = subprocess.run(command,cwd=ROOT,capture_output=True); raw = done.stdout+b'\n'+done.stderr
    (WORK/'analysis_ui.log').write_bytes(raw); count = re.search(rb'(?:#|\xe2\x84\xb9) tests (\d+)',raw)
    results['analysis_ui.log'] = {'passed':not done.returncode and bool(count),'tests':int(count[1]) if count else 0,'command':command,'log':binding(raw)}
    syntax = ['static/js/analysis/'+name for name in ('form.js','timeframe.js','progress.js','report.js','daily_output.js','legacy_form.js')]
    for name in syntax: subprocess.run(['node','--check',name],cwd=ROOT,check=True,capture_output=True)
    if not all(row['passed'] for row in results.values()): raise ValueError('Gate sửa realtime chưa PASS; xem tmp/f11_daily_analysis')
    if sources()!=sealed or runtime(ROOT)!=environment: raise ValueError('Nguồn/runtime đổi khi kiểm gate')
    probe = {'status':'NOT_RUN_UI_SCOPE','market_calls':0,'hosted_llm_calls':0}
    checks = {'version':'serving_daily_analysis_checks_v1','status':'OFFLINE_PASS_BROWSER_PENDING','base_commit':BASE,
        'sources':sealed,'runtime':environment,'historical':integrity,'compiled_python':compiled,'javascript_syntax':syntax,
        'test_suites':results,'real_market_probe':probe,'hosted_llm_calls':0,'new_hmm_student_bank_training':0,
        'recorded_at':datetime.now(timezone.utc).isoformat(),'f11_complete':False,
        'browser':{'status':'PENDING','desktop':'NOT_RUN','mobile':'NOT_RUN','reason':'BROWSER_HOST_UNAVAILABLE; PRIOR_EDGE_AUTOMATIC_REVIEW_REJECTED'},
        'scope':'REALTIME_1D_ONLY_FORM; ORIGINAL_OVERLAY_AND_RESULT; DURABLE_AGENT_PROGRESS; BICL_POLICY_CONTEXT; MODEL_FIXTURE_ONLY'}
    return publish(checks,results)


def publish(checks: dict, results: dict, extras: dict | None = None) -> dict:
    """Đóng gói log nguyên byte, kể cả lần FAIL ban đầu nếu được giải quyết bằng delta đúng phạm vi."""
    members = {'checks.json':(json.dumps(checks,ensure_ascii=False,indent=2)+'\n').encode()}
    members.update({name:(WORK/name).read_bytes() for name in results})
    members.update(extras or {})
    members['manifest.json'] = (json.dumps({name:binding(data) for name,data in members.items()},indent=2)+'\n').encode()
    with zipfile.ZipFile(PACKAGE,'w',zipfile.ZIP_DEFLATED) as archive:
        for name,data in members.items(): archive.writestr(name,data)
    receipt = {'version':'serving_integration_acceptance_v5','status':checks['status'],'base_commit':BASE,
        'checks_package':{'path':PACKAGE.relative_to(ROOT).as_posix(),**binding(PACKAGE.read_bytes())},
        'python_tests':sum(row.get('unique_tests',row['tests']) for name,row in results.items() if name!='analysis_ui.log'),
        'dom_tests':results['analysis_ui.log']['tests'],'compiled_python':len(checks['compiled_python']),'javascript_syntax':len(checks['javascript_syntax']),
        'scope':checks['scope'],'real_market_probe':checks['real_market_probe'],'browser':checks['browser'],'f11_complete':False,'historical':checks['historical']}
    if 'test_delta' in checks: receipt['test_delta'] = checks['test_delta']
    RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    return verify()


def verify() -> dict:
    """Đối soát source/runtime/evidence/log, không dùng probe model giả để chứng nhận dự báo."""
    receipt = json.loads(RECEIPT.read_bytes())
    if binding(PACKAGE.read_bytes())!={key:receipt['checks_package'][key] for key in ('bytes','sha256')}: raise ValueError('QA repair khác receipt')
    with zipfile.ZipFile(PACKAGE) as archive:
        manifest = json.loads(archive.read('manifest.json'))
        if set(archive.namelist())!=set(manifest)|{'manifest.json'} or len(archive.namelist())!=len(set(archive.namelist())): raise ValueError('Inventory QA repair sai')
        for name,expected in manifest.items():
            if binding(archive.read(name))!=expected: raise ValueError('Member QA repair khác hash')
        checks = json.loads(archive.read('checks.json'))
    if sources()!=checks['sources'] or runtime(ROOT)!=checks['runtime'] or historical()!=checks['historical']: raise ValueError('Nguồn/runtime/evidence khác QA repair')
    if receipt['f11_complete'] is not False or receipt['status']!='OFFLINE_PASS_BROWSER_PENDING': raise ValueError('Chưa có gate browser F11')
    return {key:receipt[key] for key in ('status','python_tests','dom_tests','compiled_python','javascript_syntax','f11_complete')}
