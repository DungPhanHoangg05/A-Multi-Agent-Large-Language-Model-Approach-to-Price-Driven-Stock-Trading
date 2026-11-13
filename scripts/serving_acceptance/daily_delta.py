"""Chốt lượt nghiệm thu 1D sau khi sửa riêng kỳ vọng nguồn UI cũ; không chạy lại các ca đã PASS."""
from __future__ import annotations

from datetime import datetime,timezone
import json
import py_compile
import re
import subprocess
import sys

from scripts.serving_acceptance import repair as gate
from scripts.serving_acceptance.evidence import binding,runtime


def finalize() -> dict:
    """Ứng dụng nguyên byte sau lượt đầy đủ; chỉ một assertion form lỗi thời và helper đóng gói được đổi."""
    before = json.loads((gate.WORK/'before_test_delta.json').read_bytes())
    sealed = gate.sources(); environment = runtime(gate.ROOT); integrity = gate.historical()
    changed = {name for name in set(sealed)|set(before['sources']) if sealed.get(name)!=before['sources'].get(name)}
    allowed = {'tests/serving_live/test_live_api.py','scripts/serving_acceptance/repair.py','scripts/serving_acceptance/daily_delta.py'}
    if changed != allowed or environment!=before['runtime'] or integrity!=before['historical']:
        raise ValueError('Delta vượt phạm vi assertion/helper; cần kiểm lại code bị ảnh hưởng')
    original = subprocess.check_output(['git','show',gate.BASE+':tests/serving_live/test_live_api.py'],cwd=gate.ROOT)
    if binding(original)!=before['sources']['tests/serving_live/test_live_api.py']: raise ValueError('Test trước delta không khớp base')
    results = json.loads((gate.WORK/'test_results.json').read_bytes())
    failed = [name for name,row in results.items() if not row['passed']]
    failed_name = 'tests_serving_live_test_all.log'
    if len(results)!=len(gate.PLANS) or failed!=[failed_name]: raise ValueError('Lượt trước có lỗi ngoài kỳ vọng đã rà soát')
    for name,row in results.items():
        if binding((gate.WORK/name).read_bytes())!=row['log']: raise ValueError('Log gốc đã đổi')
    old_log = (gate.WORK/failed_name).read_bytes()
    method = 'test_live_form_default_and_result_shell_preserve_source_without_inference'
    if re.findall(rb'^FAIL: (\w+)',old_log,re.M)!=[method.encode()] or b'FAILED (failures=1)' not in old_log:
        raise ValueError('FAIL không thuộc assertion nguồn cũ đã xác định')
    command = [sys.executable,'-X','utf8','-c',
        "import sys,unittest; sys.path.insert(0,'tests/serving_live'); "
        "suite=unittest.defaultTestLoader.loadTestsFromName('test_live_api.LiveApiTests."+method+"'); "
        "result=unittest.TextTestRunner(verbosity=2).run(suite); sys.exit(not result.wasSuccessful())"]
    done = subprocess.run(command,cwd=gate.ROOT,capture_output=True); raw = done.stdout+b'\n'+done.stderr
    name = 'daily_form_assertion_delta.log'; (gate.WORK/name).write_bytes(raw)
    if done.returncode or b'Ran 1 test' not in raw or not re.search(rb'\nOK\s*$',raw): raise ValueError('Ca form sau delta chưa PASS')
    results[name] = {'passed':True,'tests':1,'unique_tests':0,'command':command[1:],'log':binding(raw)}
    dom = (gate.WORK/'analysis_ui.log').read_bytes(); count = re.search(rb'(?:#|\xe2\x84\xb9) tests (\d+)',dom)
    if not count or int(count[1])!=19 or not re.search(rb'(?:#|\xe2\x84\xb9) fail 0',dom): raise ValueError('DOM chưa PASS19')
    results['analysis_ui.log'] = {'passed':True,'tests':19,'command':['node','--test','tests/js/analysis_ui.test.mjs'],'log':binding(dom)}
    names = subprocess.check_output(['git','diff',gate.BASE,'--name-only','--','*.py'],cwd=gate.ROOT).decode().splitlines()
    names += subprocess.check_output(['git','ls-files','--others','--exclude-standard','--','*.py'],cwd=gate.ROOT).decode().splitlines()
    compiled = sorted(set(names))
    for path in compiled: py_compile.compile(str(gate.ROOT/path),doraise=True)
    syntax = ['static/js/analysis/'+name for name in ('form.js','timeframe.js','progress.js','report.js','daily_output.js','legacy_form.js')]
    if gate.sources()!=sealed or runtime(gate.ROOT)!=environment: raise ValueError('Nguồn/runtime đổi trong delta')
    delta = {'status':'PASS_SCOPED_ASSERTION_DELTA','initial_python_tests':103,'initial_failures':1,'rerun_tests':1,
        'resolved_test':method,'unique_python_tests_passed':103,'changed_files':sorted(changed),
        'application_changed_after_full_run':False,'binding_recorded':before['recorded_at'],
        'note':'Lượt đầu 102/103 PASS; một test đòi nguồn latest đã bị xóa. Sửa riêng assertion, chạy lại đúng một ca PASS; không chạy lại 22 ca live hoặc các suite đã PASS.'}
    checks = {'version':'serving_daily_analysis_checks_v1','status':'OFFLINE_PASS_BROWSER_PENDING','base_commit':gate.BASE,
        'sources':sealed,'runtime':environment,'historical':integrity,'compiled_python':compiled,'javascript_syntax':syntax,
        'test_suites':results,'test_delta':delta,'real_market_probe':{'status':'NOT_RUN_UI_SCOPE','market_calls':0,'hosted_llm_calls':0},
        'hosted_llm_calls':0,'new_hmm_student_bank_training':0,'recorded_at':datetime.now(timezone.utc).isoformat(),'f11_complete':False,
        'browser':{'status':'PENDING','desktop':'NOT_RUN','mobile':'NOT_RUN','reason':'BROWSER_HOST_UNAVAILABLE; PRIOR_EDGE_AUTOMATIC_REVIEW_REJECTED'},
        'scope':'REALTIME_1D_ONLY_FORM; ORIGINAL_OVERLAY_AND_RESULT; DURABLE_AGENT_PROGRESS; BICL_POLICY_CONTEXT; MODEL_FIXTURE_ONLY'}
    return gate.publish(checks,results,{'before_test_delta.json':(gate.WORK/'before_test_delta.json').read_bytes(),
                                     'test_live_api_before_delta.py':original})
