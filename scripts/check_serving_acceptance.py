"""Gate F11 có trạng thái riêng cho offline và browser; không tự đánh PASS phần chưa quan sát."""
from __future__ import annotations

import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import py_compile
import re
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.serving_acceptance.evidence import BASE,application,binding,integrity,reused_f10,runtime

DOC = ROOT/'docs/plan/week12'
RECEIPT = DOC/'serving_integration_acceptance.json'
PACKAGE = DOC/'serving_integration_checks.zip'
SOURCES = ('scripts/check_serving_acceptance.py','scripts/serve_serving_review.py',
           'scripts/serving_acceptance','tests/serving_integration')


def new_sources() -> dict:
    """Chỉ nguồn của gate và preview mới, không khóa cache hoặc journal review."""
    files = []
    for name in SOURCES:
        path = ROOT/name
        files.extend(p for p in path.rglob('*') if p.is_file() and '__pycache__' not in p.parts) if path.is_dir() else files.append(path)
    files.append(ROOT/'scripts/.gitattributes')
    return {p.relative_to(ROOT).as_posix():binding(p.read_bytes()) for p in sorted(files)}


def verify() -> dict:
    """Receipt là đầu vào machine cho bàn giao; PENDING không được coi là F11 PASS."""
    receipt = json.loads(RECEIPT.read_bytes())
    if binding(PACKAGE.read_bytes()) != receipt['checks_package']: raise ValueError('Gói QA F11 khác receipt')
    with zipfile.ZipFile(PACKAGE) as archive:
        manifest = json.loads(archive.read('manifest.json'))
        if set(archive.namelist()) != set(manifest)|{'manifest.json'}: raise ValueError('Inventory QA F11 khác manifest')
        for name,expected in manifest.items():
            if binding(archive.read(name)) != expected: raise ValueError('Member QA F11 khác hash')
        checks = json.loads(archive.read('checks.json'))
    if (application(ROOT) != checks['app_sources'] or new_sources() != checks['new_sources'] or runtime(ROOT) != checks['runtime']):
        raise ValueError('Nguồn/runtime khác gate F11')
    if integrity(ROOT) != checks['integrity'] or reused_f10(ROOT) != checks['reused_f10']:
        raise ValueError('Evidence hoặc gate viện dẫn đã đổi')
    if receipt['status'] != 'OFFLINE_PASS_BROWSER_PENDING' or receipt['browser']['status'] != 'BLOCKED':
        raise ValueError('Không có bằng chứng cho trạng thái browser này')
    return {'status':receipt['status'],'new_tests':receipt['new_tests'],'reused_python':156,'reused_dom':31,
            'browser':receipt['browser']['status'],'f11_complete':False}


def run() -> dict:
    """Chỉ chạy suite F11 mới; gate F10 giữ nguyên được đối soát thay vì chạy lại156+31."""
    audit = {'app_sources':application(ROOT),'runtime':runtime(ROOT),'integrity':integrity(ROOT),'reused_f10':reused_f10(ROOT)}
    compiled = [name for name in new_sources() if name.endswith('.py')]
    for name in compiled: py_compile.compile(str(ROOT/name),doraise=True)
    command = [sys.executable,'-X','utf8','-m','unittest','discover','-s','tests/serving_integration','-p','test_*.py','-v']
    result = subprocess.run(command,cwd=ROOT,capture_output=True)
    raw = result.stdout+b'\n'+result.stderr
    work = ROOT/'tmp/f11'; work.mkdir(parents=True,exist_ok=True); (work/'acceptance.log').write_bytes(raw)
    count = re.search(rb'Ran (\d+) tests?',result.stderr)
    if result.returncode or not count or not re.search(rb'\nOK\s*$',raw) or b'skipped=' in raw:
        raise ValueError('Suite F11 chưa PASS; xem tmp/f11/acceptance.log')
    browser = {'status':'BLOCKED','observed_at':'2026-11-13','host_error':'The browser access host is unavailable',
        'native_attempt':'Microsoft Edge via computer-use sky.launch_app',
        'automatic_review_error':'Computer Use was not approved to use Microsoft Edge',
        'additional_rejection_reason':None,'desktop':'NOT_RUN','mobile':'NOT_RUN',
        'required_cases':['six_main_choices','advanced_controls','offline_and_new_run','empty_error_partial_completed',
                          'stop_resume','exports','VI_EN','desktop_mobile_layout_keyboard_focus']}
    checks = {'version':'serving_integration_checks_v1','status':'OFFLINE_PASS_BROWSER_PENDING','application_base_commit':BASE,
        'recorded_at':datetime.now(timezone.utc).isoformat(),'new_sources':new_sources(),'compiled_python':compiled,
        'new_tests':int(count[1]),'command':command[1:],'test_returncode':0,'test_log':binding(raw),
        'browser':browser,'hosted_smoke':'NOT_RUN; OFFLINE_SCOPE_NO_DEPLOYMENT','new_hosted_llm_calls':0,'new_market_calls':0,
        'new_hmm_student_bank_training':0,'f11_complete':False,**audit}
    members = {'checks.json':(json.dumps(checks,ensure_ascii=False,indent=2)+'\n').encode(),'acceptance.log':raw}
    members['manifest.json'] = (json.dumps({name:binding(data) for name,data in members.items()},indent=2)+'\n').encode()
    with zipfile.ZipFile(PACKAGE,'w',zipfile.ZIP_DEFLATED) as archive:
        for name,data in members.items(): archive.writestr(name,data)
    receipt = {'version':'serving_integration_acceptance_v1','status':checks['status'],'application_base_commit':BASE,
        'checks_package':binding(PACKAGE.read_bytes()),'new_tests':checks['new_tests'],
        'reused_f10':audit['reused_f10'],'compiled_python':len(compiled),'runtime_packages':len(audit['runtime']['packages']),
        'browser':browser,'hosted_smoke':checks['hosted_smoke'],'f11_complete':False}
    RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    return verify()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Đối soát nghiệm thu F11, không API hosted hoặc toàn suite')
    parser.add_argument('--run',action='store_true',help='Chạy đúng suite F11 mới rồi ghi receipt')
    args = parser.parse_args()
    # Gate cũ giữ để đọc lịch sử; nguồn live đã đổi phải kiểm lại caller thay vì viện dẫn F10.
    from scripts.serving_acceptance import live, timeframes
    receipt = json.loads(RECEIPT.read_bytes())
    result = (timeframes.run() if args.run else timeframes.verify() if receipt['version'] == 'serving_integration_acceptance_v3'
              else live.verify() if receipt['version'] == 'serving_integration_acceptance_v2' else verify())
    print(json.dumps(result,ensure_ascii=False))
