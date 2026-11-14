"""Gate scoped cho báo cáo song ngữ tạo cùng inference và chuyển tiếng không mạng."""
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
BASE='6ad73e7a'
PACKAGE=DOC/'serving_bilingual_checks.zip'
WORK=ROOT/'tmp/f11_bilingual'
PLANS=[('tests/analysis_ui','test_*.py'),('tests/serving_live','test_*.py'),('tests/serving_runtime','test_runtime.py'),
    ('tests','test_original_fix_parity.py'),('tests','test_realtime_decision_budget.py'),('tests','test_prior_graph_integration.py'),
    ('tests','test_unified_execution_leakage.py'),('tests','test_unified_preflight_leakage.py'),('tests/unified_live','test_leakage.py')]
NODE_FILES=['tests/js/'+name for name in ('analysis_ui.test.mjs','site_preferences.test.mjs')]


def sources() -> dict:
    result=repair.sources()
    for folder,pattern in PLANS:
        if '*' not in pattern: result[folder+'/'+pattern]=binding((ROOT/folder/pattern).read_bytes())
    for name in NODE_FILES: result[name]=binding((ROOT/name).read_bytes())
    return dict(sorted(result.items()))


def historical() -> dict:
    """Khóa QA 1D trước đó nguyên byte; không nhận gate cũ là đã kiểm renderer mới."""
    result=repair.historical()
    name='docs/plan/week12/serving_daily_analysis_checks.zip'
    expected=subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
    if (ROOT/name).read_bytes()!=expected: raise ValueError('QA 1D trước đó đã đổi')
    report='docs/plan/week12/serving_report_checks.zip'
    previous=subprocess.check_output(['git','show',BASE+':'+report],cwd=ROOT)
    if (ROOT/report).read_bytes()!=previous: raise ValueError('QA report cũ đã đổi')
    locale='docs/plan/week12/serving_language_theme_checks.zip'
    released=subprocess.check_output(['git','show',BASE+':'+locale],cwd=ROOT)
    if (ROOT/locale).read_bytes()!=released: raise ValueError('QA locale cũ đã đổi')
    completion='docs/plan/week12/serving_locale_repair_checks.zip'
    prior=subprocess.check_output(['git','show',BASE+':'+completion],cwd=ROOT)
    if (ROOT/completion).read_bytes()!=prior: raise ValueError('QA dịch trước đã đổi')
    last='docs/plan/week12/serving_report_completion_checks.zip'
    released_last=subprocess.check_output(['git','show',BASE+':'+last],cwd=ROOT)
    if (ROOT/last).read_bytes()!=released_last: raise ValueError('QA completion trước đã đổi')
    return {**result,'daily_analysis_qa_unchanged':binding(expected),'report_qa_unchanged':binding(previous),
        'language_theme_qa_unchanged':binding(released),'locale_repair_qa_unchanged':binding(prior),'report_completion_qa_unchanged':binding(released_last)}


def suite(plan: tuple[str,str]) -> tuple[str,dict]:
    """Chỉ caller/song ngữ/transport bị ảnh hưởng, process/log riêng cho từng nhóm."""
    folder,pattern=plan
    command=[sys.executable,'-X','utf8','-m','unittest','discover','-s',folder,'-p',pattern,'-v']
    done=subprocess.run(command,cwd=ROOT,capture_output=True); raw=done.stdout+b'\n'+done.stderr
    name=folder.replace('/','_')+'_'+pattern.replace('*','all').replace('.py','.log')
    (WORK/name).write_bytes(raw); count=re.search(rb'Ran (\d+) tests?',done.stderr)
    return name,{'passed':not done.returncode and bool(count) and bool(re.search(rb'\nOK\s*$',raw)) and b'skipped=' not in raw,
        'tests':int(count[1]) if count else 0,'command':command[1:],'log':binding(raw)}


def run(*, reuse_python: object = None) -> dict:
    """Kiểm song ngữ/caller/checkpoint; không thay giá, prior hoặc phí."""
    WORK.mkdir(parents=True,exist_ok=True)
    sealed=sources(); environment=runtime(ROOT); integrity=historical()
    names=subprocess.check_output(['git','diff',BASE,'--name-only','--','*.py'],cwd=ROOT).decode().splitlines()
    names+=subprocess.check_output(['git','ls-files','--others','--exclude-standard','--','*.py'],cwd=ROOT).decode().splitlines()
    compiled=sorted(set(names))
    for name in compiled: py_compile.compile(str(ROOT/name),doraise=True)
    results={}; reused=None
    if reuse_python is not None:
        # Chỉ sửa test DOM/gate đóng gói mới được giữ log Python vừa PASS.
        from pathlib import Path
        reused=Path(reuse_python).read_bytes(); prior=json.loads(reused)
        changed={name for name in set(sealed)|set(prior['sources']) if sealed.get(name)!=prior['sources'].get(name)}
        allowed={'tests/js/analysis_ui.test.mjs','scripts/serving_acceptance/reports.py'}
        if (prior['version']!='passed_python_scopes_v1' or prior['runtime']!=environment
                or not changed<=allowed): raise ValueError('Không được viện dẫn log Python khi app/test Python/runtime đã đổi')
        expected={folder.replace('/','_')+'_'+pattern.replace('*','all').replace('.py','.log') for folder,pattern in PLANS}
        if set(prior['test_suites'])!=expected: raise ValueError('Các scope Python không khớp')
        for name,row in prior['test_suites'].items():
            raw=(WORK/name).read_bytes(); count=re.search(rb'Ran (\d+) tests?',raw)
            if (not row['passed'] or binding(raw)!=row['log'] or not count or int(count[1])!=row['tests']
                    or not re.search(rb'\nOK\s*$',raw) or b'skipped=' in raw): raise ValueError('Log Python không còn PASS/nguyên byte')
        results=prior['test_suites']
    else:
        with ThreadPoolExecutor(max_workers=2) as pool:
            for future in as_completed([pool.submit(suite,plan) for plan in PLANS]):
                name,row=future.result(); results[name]=row; print(name,row['passed'],row['tests'],flush=True)
    for index,name in enumerate(NODE_FILES):
        done=subprocess.run(['node','--test',name],cwd=ROOT,capture_output=True)
        raw=done.stdout+b'\n'+done.stderr; log='dom_'+str(index)+'.log'; (WORK/log).write_bytes(raw)
        count=re.search(rb'(?:#|\xe2\x84\xb9) tests (\d+)',raw)
        results[log]={'passed':not done.returncode and bool(count),'tests':int(count[1]) if count else 0,'log':binding(raw)}
    syntax=['static/js/display_locale.js','static/js/analysis/view.js']
    for name in syntax: subprocess.run(['node','--check',name],cwd=ROOT,check=True,capture_output=True)
    if not all(row['passed'] for row in results.values()): raise ValueError('Gate báo cáo chưa PASS; xem tmp/f11_bilingual')
    if sources()!=sealed or runtime(ROOT)!=environment: raise ValueError('Nguồn/runtime đổi trong gate')
    checks={'version':'serving_bilingual_checks_v1','status':'OFFLINE_PASS_BROWSER_PENDING','base_commit':BASE,
        'sources':sealed,'runtime':environment,'historical':integrity,'compiled_python':compiled,'javascript_syntax':syntax,
        'test_suites':results,'market_calls':0,'hosted_llm_calls':0,'f11_complete':False,
        'recorded_at':datetime.now(timezone.utc).isoformat(),
        'scope':'BILINGUAL_IN_EXISTING_AGENT_INVOCATIONS; LOCAL_NUMERIC_REPORTS; CANONICAL_POLICY_ISOLATION; STORED_VIEWS_SWITCH_ZERO_NETWORK; TRANSLATION_ROUTE_RETIRED; PAIRED_PIT_UNCHANGED',
        'browser':{'status':'PENDING','desktop':'NOT_RUN','mobile':'NOT_RUN','reason':'BROWSER_HOST_UNAVAILABLE'},
        'not_rerun':'Scoped native parity and six live versions checked; no scientific study, full unit or full E2E'}
    members={'checks.json':(json.dumps(checks,ensure_ascii=False,indent=2)+'\n').encode()}
    if reused is not None:
        checks['python_reuse']={'source_delta':sorted(changed),'evidence':binding(reused),
            'reason':'PYTHON_LOGS_PASS_AND_APP_PYTHON_TESTS_RUNTIME_UNCHANGED; ONLY_DOM_TEST_AND_QA_PACKAGING_CHANGED'}
        members['checks.json']=(json.dumps(checks,ensure_ascii=False,indent=2)+'\n').encode()
        members['python_reuse.json']=reused
    members.update({name:(WORK/name).read_bytes() for name in results})
    members['manifest.json']=(json.dumps({name:binding(raw) for name,raw in members.items()},indent=2)+'\n').encode()
    with zipfile.ZipFile(PACKAGE,'w',zipfile.ZIP_DEFLATED) as archive:
        for name,raw in members.items(): archive.writestr(name,raw)
    receipt={'version':'serving_integration_acceptance_v10','status':checks['status'],'base_commit':BASE,
        'checks_package':{'path':PACKAGE.relative_to(ROOT).as_posix(),**binding(PACKAGE.read_bytes())},
        'python_tests':sum(row['tests'] for name,row in results.items() if not name.startswith('dom_')),
        'dom_tests':sum(row['tests'] for name,row in results.items() if name.startswith('dom_')),'compiled_python':len(compiled),'javascript_syntax':len(syntax),
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
    if sources()!=checks['sources'] or runtime(ROOT)!=checks['runtime'] or historical()!=checks['historical']: raise ValueError('Nguồn/runtime/evidence khác QA báo cáo')
    if receipt['f11_complete'] is not False or receipt['status']!='OFFLINE_PASS_BROWSER_PENDING': raise ValueError('Chưa có nghiệm thu browser')
    return {key:receipt[key] for key in ('status','python_tests','dom_tests','compiled_python','javascript_syntax','f11_complete')}
