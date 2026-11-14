"""Gate F11 sau cập nhật develop/live: kiểm lại caller đổi, giữ gate lịch sử riêng."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import py_compile
import re
import subprocess
import sys
import zipfile

from scripts.serving_acceptance.evidence import binding, runtime

BASE = '6ac5d7ab'
ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT/'docs/plan/week12'
PACKAGE = DOC/'serving_live_checks.zip'
RECEIPT = DOC/'serving_integration_acceptance.json'
WORK = ROOT/'tmp/f11_live'
PLANS = [('tests/serving_live','test_*.py'),('tests/serving_integration','test_*.py'),
    ('tests/serving_runtime','test_runtime.py'),('tests/serving_runtime','test_api.py'),('tests/serving_runtime','test_resources.py'),
    ('tests/analysis_ui','test_pages.py'),('tests/backtest_ui','test_api.py'),('tests/backtest_ui','test_evaluation.py'),
    ('tests','test_variant_serving.py'),('tests','test_unified_experiment.py'),('tests','test_original_fix_parity.py'),
    ('tests','test_web_json_serialization.py'),('tests','test_realtime_sources.py'),('tests','test_unified_execution_leakage.py'),
    ('tests','test_unified_preflight_leakage.py'),('tests/unified_live','test_leakage.py')]


def sources() -> dict:
    """Khóa toàn ứng dụng và các test/caller/gate đã chọn; không bind cache hoặc journal ignored."""
    paths = ['agents','core','data_manager','utils','templates','static','default_config.py','web_interface.py',
        'requirements-unified.lock.txt','.python-version','.gitattributes','scripts/.gitattributes',
        'scripts/check_serving_acceptance.py','scripts/serve_serving_review.py','scripts/serving_acceptance',
        'tests/serving_runtime','tests/serving_live','tests/serving_integration','tests/analysis_ui',
        'tests/backtest_ui','tests/js/analysis_ui.test.mjs']+[folder+'/'+pattern for folder,pattern in PLANS if '*' not in pattern]
    names = subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','--',*paths],cwd=ROOT).decode().splitlines()
    return {name:binding((ROOT/name).read_bytes()) for name in sorted(set(names)) if (ROOT/name).is_file()}


def historical() -> dict:
    """Bằng chứng cũ đã chuyển archive vẫn phải khớp byte; không ép nguồn paper mới giống F05."""
    from core.revision_evidence_archive import EvidenceArchive
    with EvidenceArchive(ROOT) as archive:
        with zipfile.ZipFile(DOC/'final_evidence_snapshot.zip') as package:
            snapshot = json.loads(package.read('snapshot_manifest.json'))
        for group in ('frozen_packages','legacy_archives'):
            for name,expected in snapshot[group].items():
                raw = (ROOT/name).read_bytes() if (ROOT/name).is_file() else archive.read(name)
                if binding(raw) != expected: raise ValueError('Evidence frozen đã đổi')
        prefix = 'outputs/revision/manuscript_unified_final_v1/'
        raw = archive.read(prefix+'manifest.json')
        if binding(raw)['sha256'] != '8e5ce2a4ca6f3a52945047cb8e1e1e99e8c00dfcd959a6fc6cdadcd701013de9':
            raise ValueError('Manifest F05 khác hash')
        manifest = json.loads(raw)
        for name,expected in manifest['outputs'].items():
            if binding(archive.read(prefix+name)) != expected: raise ValueError('Output F05 trong archive khác byte')
        with zipfile.ZipFile(io.BytesIO(archive.read(prefix+'sources.zip'))) as source:
            for name,expected in manifest['sources'].items():
                if binding(source.read(name)) != expected: raise ValueError('Nguồn F05 không khôi phục được')
    preserved = ('serving_resources_v1.json','serving_runner_checks.zip','analysis_ui_checks.zip',
                 'backtest_ui_checks.zip','serving_integration_checks.zip')
    for name in preserved:
        if (DOC/name).read_bytes() != subprocess.check_output(['git','show',BASE+':docs/plan/week12/'+name],cwd=ROOT):
            raise ValueError('Receipt/gói QA lịch sử đã đổi')
    for name in ('outputs/paper/main.pdf','outputs/paper/main_submit.pdf','outputs/paper/manifest.json',
                 'docs/plan/revision_evidence/index.json'):
        if (ROOT/name).read_bytes() != subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT):
            raise ValueError('Bản thảo hoặc archive mới từ develop đã đổi')
    return {'frozen_packages':20,'legacy_archives':30,'f05_outputs_restored_verified':len(manifest['outputs']),
        'f05_sources_restored_verified':len(manifest['sources']),'old_qa_preserved':list(preserved),
        'f10_and_f11_v1':'HISTORICAL_ONLY; CHANGED_CALLERS_RETESTED_NOT_BLINDLY_REUSED',
        'develop_paper_unchanged':True,'native_rowwise_causal_gate':'FAIL','whole_system_causal_gate':'NOT_CERTIFIED'}


def run_suite(plan: tuple[str,str]) -> tuple[str,dict]:
    """Process riêng tránh trùng helper support giữa test suites; giữ stdout/stderr nguyên byte."""
    folder,pattern = plan
    command = [sys.executable,'-X','utf8','-m','unittest','discover','-s',folder,'-p',pattern,'-v']
    result = subprocess.run(command,cwd=ROOT,capture_output=True)
    raw = result.stdout+b'\n'+result.stderr
    name = folder.replace('/','_')+'_'+pattern.replace('*','all').replace('.py','.log')
    (WORK/name).write_bytes(raw)
    count = re.search(rb'Ran (\d+) tests?',result.stderr)
    passed = not result.returncode and bool(count) and bool(re.search(rb'\nOK\s*$',raw)) and b'skipped=' not in raw
    return name,{'passed':passed,'tests':int(count[1]) if count else 0,'command':command[1:],'log':binding(raw)}


def run() -> dict:
    """Chạy đúng các caller/service/PIT bị ảnh hưởng; không toàn unit suite/E2E hoặc hosted API."""
    WORK.mkdir(parents=True,exist_ok=True)
    sealed = sources(); environment = runtime(ROOT); integrity = historical()
    changed = subprocess.check_output(['git','diff',BASE,'--name-only','--','*.py'],cwd=ROOT).decode().splitlines()
    unknown = subprocess.check_output(['git','ls-files','--others','--exclude-standard','--','*.py'],cwd=ROOT).decode().splitlines()
    compiled = sorted(set(changed+unknown))
    for name in compiled: py_compile.compile(str(ROOT/name),doraise=True)
    results = {}
    with ThreadPoolExecutor(max_workers=2) as pool:
        for future in as_completed([pool.submit(run_suite,plan) for plan in PLANS]):
            name,row = future.result(); results[name] = row
            print(name,row['passed'],row['tests'],flush=True)
            (WORK/'test_results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    command = ['node','--test','tests/js/analysis_ui.test.mjs']
    result = subprocess.run(command,cwd=ROOT,capture_output=True); raw = result.stdout+b'\n'+result.stderr
    (WORK/'analysis_ui.log').write_bytes(raw)
    count = re.search(rb'(?:#|\xe2\x84\xb9) tests (\d+)',raw)
    results['analysis_ui.log'] = {'passed':not result.returncode and bool(count),'tests':int(count[1]) if count else 0,'command':command,'log':binding(raw)}
    syntax = ['static/js/analysis/'+name for name in ('common.js','form.js','result.js','view.js','legacy_form.js')]
    for name in syntax: subprocess.run(['node','--check',name],cwd=ROOT,capture_output=True,check=True)
    if not all(row['passed'] for row in results.values()): raise ValueError('Gate chưa PASS; xem tmp/f11_live')
    if sources() != sealed or runtime(ROOT) != environment: raise ValueError('Nguồn/runtime đổi giữa gate')
    browser = {'status':'PENDING','desktop':'NOT_RUN','mobile':'NOT_RUN',
        'reason':'BROWSER_HOST_UNAVAILABLE; PRIOR_EDGE_AUTOMATIC_REVIEW_REJECTED',
        'required':['all_six_latest_analysis','advanced','frozen_reader','empty_error_partial','exports',
                    'stop_resume','VI_EN','desktop_mobile_keyboard_focus']}
    checks = {'version':'serving_live_checks_v1','base_commit':BASE,'sources':sealed,'runtime':environment,
        'historical':integrity,'compiled_python':compiled,'javascript_syntax':syntax,'test_suites':results,
        'recorded_at':datetime.now(timezone.utc).isoformat(),'browser':browser,
        'hosted_llm_calls':0,'market_calls':0,'new_hmm_student_bank_training':0,
        'live_input_fixture':'MWG; 2026-11-12; SIX_SELECTED_ANALYZE_JOBS_AND_ALL_SIX_COMPARE',
        'scope':'DAILY_COMPLETED_SESSION; NOT_INTRADAY; NO_QUERY_OUTCOME; EXPLORATORY',
        'status':'OFFLINE_PASS_BROWSER_PENDING','f11_complete':False}
    members = {'checks.json':(json.dumps(checks,ensure_ascii=False,indent=2)+'\n').encode()}
    members.update({name:(WORK/name).read_bytes() for name in results})
    members['manifest.json'] = (json.dumps({name:binding(raw) for name,raw in members.items()},indent=2)+'\n').encode()
    with zipfile.ZipFile(PACKAGE,'w',zipfile.ZIP_DEFLATED) as archive:
        for name,raw in members.items(): archive.writestr(name,raw)
    receipt = {'version':'serving_integration_acceptance_v2','status':checks['status'],
        'checks_package':{'path':PACKAGE.relative_to(ROOT).as_posix(),**binding(PACKAGE.read_bytes())},
        'base_commit':BASE,'python_tests':sum(row['tests'] for name,row in results.items() if name != 'analysis_ui.log'),
        'dom_tests':results['analysis_ui.log']['tests'],'compiled_python':len(compiled),'javascript_syntax':len(syntax),
        'browser':browser,'historical':integrity,'hosted_smoke':'NOT_RUN; FIXTURE_FIRST',
        'f11_complete':False,'previous_f11_qa_preserved':'docs/plan/week12/serving_integration_checks.zip'}
    RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    return verify()


def verify() -> dict:
    """Chỉ đối soát gói/source/runtime; không biến browser PENDING thành PASS."""
    receipt = json.loads(RECEIPT.read_bytes())
    if binding(PACKAGE.read_bytes()) != {k:receipt['checks_package'][k] for k in ('bytes','sha256')}:
        raise ValueError('QA live khác receipt')
    with zipfile.ZipFile(PACKAGE) as archive:
        manifest = json.loads(archive.read('manifest.json'))
        if set(archive.namelist()) != set(manifest)|{'manifest.json'} or len(set(archive.namelist())) != len(archive.namelist()):
            raise ValueError('Inventory QA live khác manifest')
        for name,expected in manifest.items():
            if binding(archive.read(name)) != expected: raise ValueError('Member QA live khác hash')
        checks = json.loads(archive.read('checks.json'))
    if sources() != checks['sources'] or runtime(ROOT) != checks['runtime'] or historical() != checks['historical']:
        raise ValueError('Nguồn/runtime/evidence khác QA live')
    if receipt['f11_complete'] is not False or receipt['status'] != 'OFFLINE_PASS_BROWSER_PENDING':
        raise ValueError('Chưa có bằng chứng hoàn tất browser F11')
    return {key:receipt[key] for key in ('status','python_tests','dom_tests','compiled_python','javascript_syntax','f11_complete')}
