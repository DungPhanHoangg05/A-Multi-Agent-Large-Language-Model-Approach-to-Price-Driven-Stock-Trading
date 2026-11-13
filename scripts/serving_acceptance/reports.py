"""Gate scoped cho thứ tự BICL và báo cáo Indicator/Alpha, không chạy lại scientific study."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
import json
import py_compile
import re
import subprocess
import sys
import zipfile

from scripts.serving_acceptance import repair
from scripts.serving_acceptance.evidence import binding,runtime

ROOT,DOC,RECEIPT=repair.ROOT,repair.DOC,repair.RECEIPT
BASE='3528891f'
PACKAGE=DOC/'serving_report_checks.zip'
WORK=ROOT/'tmp/f11_reports'
PLANS=[('tests/analysis_ui','test_*.py'),('tests/serving_live','test_progress.py'),
    ('tests','test_web_json_serialization.py'),('tests','test_unified_execution_leakage.py'),
    ('tests','test_unified_preflight_leakage.py'),('tests/unified_live','test_leakage.py')]


def historical() -> dict:
    """Khóa QA 1D trước đó nguyên byte; không nhận gate cũ là đã kiểm renderer mới."""
    result=repair.historical()
    name='docs/plan/week12/serving_daily_analysis_checks.zip'
    expected=subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
    if (ROOT/name).read_bytes()!=expected: raise ValueError('QA 1D trước đó đã đổi')
    return {**result,'daily_analysis_qa_unchanged':binding(expected)}


def suite(plan: tuple[str,str]) -> tuple[str,dict]:
    """Chỉ caller/progress/projection/PIT bị ảnh hưởng, process/log riêng cho từng nhóm."""
    folder,pattern=plan
    command=[sys.executable,'-X','utf8','-m','unittest','discover','-s',folder,'-p',pattern,'-v']
    done=subprocess.run(command,cwd=ROOT,capture_output=True); raw=done.stdout+b'\n'+done.stderr
    name=folder.replace('/','_')+'_'+pattern.replace('*','all').replace('.py','.log')
    (WORK/name).write_bytes(raw); count=re.search(rb'Ran (\d+) tests?',done.stderr)
    return name,{'passed':not done.returncode and bool(count) and bool(re.search(rb'\nOK\s*$',raw)) and b'skipped=' not in raw,
        'tests':int(count[1]) if count else 0,'command':command[1:],'log':binding(raw)}


def run() -> dict:
    """Không đổi giá/prior/LLM/phí; gate tập trung vào luồng hiển thị và leak boundary của tin."""
    WORK.mkdir(parents=True,exist_ok=True)
    sealed=repair.sources(); environment=runtime(ROOT); integrity=historical()
    names=subprocess.check_output(['git','diff',BASE,'--name-only','--','*.py'],cwd=ROOT).decode().splitlines()
    names+=subprocess.check_output(['git','ls-files','--others','--exclude-standard','--','*.py'],cwd=ROOT).decode().splitlines()
    compiled=sorted(set(names))
    for name in compiled: py_compile.compile(str(ROOT/name),doraise=True)
    results={}
    with ThreadPoolExecutor(max_workers=2) as pool:
        for future in as_completed([pool.submit(suite,plan) for plan in PLANS]):
            name,row=future.result(); results[name]=row; print(name,row['passed'],row['tests'],flush=True)
    done=subprocess.run(['node','--test','tests/js/analysis_ui.test.mjs'],cwd=ROOT,capture_output=True)
    raw=done.stdout+b'\n'+done.stderr; (WORK/'analysis_ui.log').write_bytes(raw)
    count=re.search(rb'(?:#|\xe2\x84\xb9) tests (\d+)',raw)
    results['analysis_ui.log']={'passed':not done.returncode and bool(count),'tests':int(count[1]) if count else 0,'log':binding(raw)}
    syntax=['static/js/analysis/'+name for name in ('legacy_form.js','daily_output.js','report.js')]
    for name in syntax: subprocess.run(['node','--check',name],cwd=ROOT,check=True,capture_output=True)
    if not all(row['passed'] for row in results.values()): raise ValueError('Gate báo cáo chưa PASS; xem tmp/f11_reports')
    if repair.sources()!=sealed or runtime(ROOT)!=environment: raise ValueError('Nguồn/runtime đổi trong gate')
    checks={'version':'serving_report_checks_v1','status':'OFFLINE_PASS_BROWSER_PENDING','base_commit':BASE,
        'sources':sealed,'runtime':environment,'historical':integrity,'compiled_python':compiled,'javascript_syntax':syntax,
        'test_suites':results,'market_calls':0,'hosted_llm_calls':0,'f11_complete':False,
        'recorded_at':datetime.now(timezone.utc).isoformat(),
        'scope':'BICL_BEFORE_SELECTED_DECISION; ORIGINAL_FULL_ALPHA_AND_COMMON_SEPARATE; SAFE_MARKDOWN; SNAPSHOT_NEWS_PIT',
        'browser':{'status':'PENDING','desktop':'NOT_RUN','mobile':'NOT_RUN','reason':'BROWSER_HOST_UNAVAILABLE'},
        'not_rerun':'Original/native and scientific adapters unchanged; no full live/provider replay, study, full unit or E2E'}
    members={'checks.json':(json.dumps(checks,ensure_ascii=False,indent=2)+'\n').encode()}
    members.update({name:(WORK/name).read_bytes() for name in results})
    members['manifest.json']=(json.dumps({name:binding(raw) for name,raw in members.items()},indent=2)+'\n').encode()
    with zipfile.ZipFile(PACKAGE,'w',zipfile.ZIP_DEFLATED) as archive:
        for name,raw in members.items(): archive.writestr(name,raw)
    receipt={'version':'serving_integration_acceptance_v6','status':checks['status'],'base_commit':BASE,
        'checks_package':{'path':PACKAGE.relative_to(ROOT).as_posix(),**binding(PACKAGE.read_bytes())},
        'python_tests':sum(row['tests'] for name,row in results.items() if name!='analysis_ui.log'),
        'dom_tests':results['analysis_ui.log']['tests'],'compiled_python':len(compiled),'javascript_syntax':len(syntax),
        'scope':checks['scope'],'browser':checks['browser'],'f11_complete':False,'historical':integrity}
    RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    return verify()


def verify() -> dict:
    """Đối soát nguồn/runtime/historical và từng log; không gọi inference để cập nhật checklist."""
    receipt=json.loads(RECEIPT.read_bytes())
    if binding(PACKAGE.read_bytes())!={key:receipt['checks_package'][key] for key in ('bytes','sha256')}: raise ValueError('QA báo cáo khác receipt')
    with zipfile.ZipFile(PACKAGE) as archive:
        manifest=json.loads(archive.read('manifest.json'))
        if set(archive.namelist())!=set(manifest)|{'manifest.json'}: raise ValueError('Inventory QA báo cáo sai')
        for name,expected in manifest.items():
            if binding(archive.read(name))!=expected: raise ValueError('Member QA báo cáo khác hash')
        checks=json.loads(archive.read('checks.json'))
    if repair.sources()!=checks['sources'] or runtime(ROOT)!=checks['runtime'] or historical()!=checks['historical']: raise ValueError('Nguồn/runtime/evidence khác QA báo cáo')
    if receipt['f11_complete'] is not False or receipt['status']!='OFFLINE_PASS_BROWSER_PENDING': raise ValueError('Chưa có nghiệm thu browser')
    return {key:receipt[key] for key in ('status','python_tests','dom_tests','compiled_python','javascript_syntax','f11_complete')}
