"""Nghiệm thu sửa chế độ intraday: gate mới, không ghi đè QA ngày đã khóa trước đó."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime,timezone
import json
import py_compile
import re
import subprocess
import sys
import zipfile

from scripts.serving_acceptance import live
from scripts.serving_acceptance.evidence import binding,runtime

ROOT,DOC = live.ROOT,live.DOC
BASE = '2e330c8c'
PACKAGE = DOC/'serving_timeframe_checks.zip'
RECEIPT = live.RECEIPT
WORK = ROOT/'tmp/f11_timeframes'
PLANS = [('tests/serving_live','test_*.py'),('tests/serving_integration','test_*.py'),
    ('tests/serving_runtime','test_runtime.py'),('tests/serving_runtime','test_resources.py'),('tests/serving_runtime','test_api.py'),
    ('tests/analysis_ui','test_pages.py'),('tests/backtest_ui','test_api.py'),('tests','test_variant_serving.py'),
    ('tests','test_original_fix_parity.py'),('tests','test_unified_experiment.py'),('tests','test_web_json_serialization.py'),
    ('tests','test_realtime_sources.py'),('tests','test_unified_execution_leakage.py'),
    ('tests','test_unified_preflight_leakage.py'),('tests/unified_live','test_leakage.py')]


def historical() -> dict:
    """Gate ngày và nguồn bài báo mới vẫn nguyên byte, chỉ giữ làm lịch sử của phạm vi cũ."""
    result = live.historical()
    path = DOC/'serving_live_checks.zip'
    expected = subprocess.check_output(['git','show',BASE+':docs/plan/week12/serving_live_checks.zip'],cwd=ROOT)
    if path.read_bytes() != expected: raise ValueError('QA daily cũ đã đổi')
    return {**result,'daily_qa_unchanged':binding(expected)}


def run_suite(plan: tuple[str,str]) -> tuple[str,dict]:
    """Suite process riêng và log raw, tránh xung đột tên helper hoặc log stderr PowerShell."""
    folder,pattern = plan
    command = [sys.executable,'-X','utf8','-m','unittest','discover','-s',folder,'-p',pattern,'-v']
    result = subprocess.run(command,cwd=ROOT,capture_output=True)
    raw = result.stdout+b'\n'+result.stderr
    name = folder.replace('/','_')+'_'+pattern.replace('*','all').replace('.py','.log')
    (WORK/name).write_bytes(raw)
    count = re.search(rb'Ran (\d+) tests?',result.stderr)
    return name,{'passed':not result.returncode and bool(count) and bool(re.search(rb'\nOK\s*$',raw)) and b'skipped=' not in raw,
        'tests':int(count[1]) if count else 0,'command':command[1:],'log':binding(raw)}


def run() -> dict:
    """Kiểm đúng provider/caller/PIT mới, không chạy full unit/E2E hoặc API thật."""
    WORK.mkdir(parents=True,exist_ok=True)
    sealed = live.sources(); environment = runtime(ROOT); integrity = historical()
    names = subprocess.check_output(['git','diff',BASE,'--name-only','--','*.py'],cwd=ROOT).decode().splitlines()
    names += subprocess.check_output(['git','ls-files','--others','--exclude-standard','--','*.py'],cwd=ROOT).decode().splitlines()
    compiled = sorted(set(names))
    for name in compiled: py_compile.compile(str(ROOT/name),doraise=True)
    results = {}
    with ThreadPoolExecutor(max_workers=2) as pool:
        for future in as_completed([pool.submit(run_suite,plan) for plan in PLANS]):
            name,row = future.result(); results[name] = row
            print(name,row['passed'],row['tests'],flush=True)
            (WORK/'test_results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    command = ['node','--test','tests/js/analysis_ui.test.mjs']
    result = subprocess.run(command,cwd=ROOT,capture_output=True); raw = result.stdout+b'\n'+result.stderr
    (WORK/'analysis_ui.log').write_bytes(raw); count = re.search(rb'(?:#|\xe2\x84\xb9) tests (\d+)',raw)
    results['analysis_ui.log'] = {'passed':not result.returncode and bool(count),'tests':int(count[1]) if count else 0,'command':command,'log':binding(raw)}
    syntax = ['static/js/analysis/'+name for name in ('common.js','form.js','result.js','view.js','chart.js','timeframe.js','legacy_form.js')]
    for name in syntax: subprocess.run(['node','--check',name],cwd=ROOT,check=True,capture_output=True)
    if not all(row['passed'] for row in results.values()): raise ValueError('Gate timeframe chưa PASS; xem tmp/f11_timeframes')
    if live.sources() != sealed or runtime(ROOT) != environment: raise ValueError('Nguồn/runtime đổi khi kiểm gate')
    checks = {'version':'serving_timeframe_checks_v1','status':'OFFLINE_PASS_BROWSER_PENDING','base_commit':BASE,
        'sources':sealed,'runtime':environment,'historical':integrity,'compiled_python':compiled,'javascript_syntax':syntax,
        'test_suites':results,'recorded_at':datetime.now(timezone.utc).isoformat(),'hosted_llm_calls':0,'market_calls':0,
        'new_hmm_student_bank_training':0,'f11_complete':False,'browser':{'status':'PENDING','desktop':'NOT_RUN','mobile':'NOT_RUN',
            'reason':'BROWSER_HOST_UNAVAILABLE; PRIOR_EDGE_AUTOMATIC_REVIEW_REJECTED'},
        'scope':'SELECTED_REALTIME_CHART_5m_15m_30m_1h_1d_1w_1mo; DAILY_PRIOR_ALPHA_MT; T_PLUS_2_5_SESSIONS'}
    members = {'checks.json':(json.dumps(checks,ensure_ascii=False,indent=2)+'\n').encode()}
    members.update({name:(WORK/name).read_bytes() for name in results})
    members['manifest.json'] = (json.dumps({name:binding(raw) for name,raw in members.items()},indent=2)+'\n').encode()
    with zipfile.ZipFile(PACKAGE,'w',zipfile.ZIP_DEFLATED) as archive:
        for name,raw in members.items(): archive.writestr(name,raw)
    receipt = {'version':'serving_integration_acceptance_v3','status':checks['status'],'base_commit':BASE,
        'checks_package':{'path':PACKAGE.relative_to(ROOT).as_posix(),**binding(PACKAGE.read_bytes())},
        'python_tests':sum(row['tests'] for name,row in results.items() if name!='analysis_ui.log'),
        'dom_tests':results['analysis_ui.log']['tests'],'compiled_python':len(compiled),'javascript_syntax':len(syntax),
        'browser':checks['browser'],'f11_complete':False,'historical':integrity,'scope':checks['scope'],
        'hosted_smoke':'NOT_RUN; FIXTURE_FIRST','previous_daily_qa_preserved':'docs/plan/week12/serving_live_checks.zip'}
    RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    return verify()


def verify() -> dict:
    """Đối soát nguồn/log/runtime hiện hành, không suy browser PASS từ DOM fixture."""
    receipt = json.loads(RECEIPT.read_bytes())
    if binding(PACKAGE.read_bytes()) != {key:receipt['checks_package'][key] for key in ('bytes','sha256')}:
        raise ValueError('QA timeframe khác receipt')
    with zipfile.ZipFile(PACKAGE) as archive:
        manifest = json.loads(archive.read('manifest.json'))
        if set(archive.namelist()) != set(manifest)|{'manifest.json'} or len(archive.namelist()) != len(set(archive.namelist())):
            raise ValueError('Inventory QA timeframe sai')
        for name,expected in manifest.items():
            if binding(archive.read(name)) != expected: raise ValueError('Member QA timeframe khác hash')
        checks = json.loads(archive.read('checks.json'))
    if live.sources()!=checks['sources'] or runtime(ROOT)!=checks['runtime'] or historical()!=checks['historical']:
        raise ValueError('Nguồn/runtime/evidence khác QA timeframe')
    if receipt['f11_complete'] is not False or receipt['status']!='OFFLINE_PASS_BROWSER_PENDING':
        raise ValueError('Chưa có bằng chứng hoàn tất browser F11')
    return {key:receipt[key] for key in ('status','python_tests','dom_tests','compiled_python','javascript_syntax','f11_complete')}
