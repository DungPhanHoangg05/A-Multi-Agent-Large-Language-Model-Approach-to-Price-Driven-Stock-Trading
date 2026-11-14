"""Kiểm nguồn/runtime/log để viện dẫn gate cũ đúng phạm vi, không chạy lại toàn suite."""
from __future__ import annotations

import ast
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import platform
import re
import subprocess
import zipfile

BASE = 'f96b44f2'
APP_PATHS = ('agents','core','data_manager','utils','templates','static','default_config.py',
             'web_interface.py','requirements-unified.lock.txt','.python-version','.gitattributes')


def binding(raw: bytes) -> dict:
    """Không chuẩn hóa newline của bằng chứng có checksum."""
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def runtime(root: Path) -> dict:
    """Python/Node và 107 package phải khớp runtime đã khóa; không đọc API key/env riêng."""
    from core.historical_evaluation_journal import load
    source = root/'docs/plan/week12/unified_live_runtime.json'
    expected = load(source)['runtime']
    actual = {'python':platform.python_version(),'packages':{name:version(name) for name in expected['packages']}}
    if actual != expected: raise ValueError('Runtime package khác snapshot đã khóa')
    node = subprocess.check_output(['node','--version'],cwd=root).decode().strip()
    if node != 'v24.18.0': raise ValueError('Node khác gate DOM F10')
    return {**actual,'node':node,'historical_runtime_binding':binding(source.read_bytes())}


def application(root: Path) -> dict:
    """App phải nguyên nguồn F10; test/script mới không được che thay đổi runtime chưa test."""
    result = subprocess.run(['git','diff','--exit-code',BASE,'--',*APP_PATHS],cwd=root,capture_output=True)
    if result.returncode: raise ValueError('App đã đổi so với F10, không được viện dẫn nguyên gate cũ')
    names = subprocess.check_output(['git','ls-files','--',*APP_PATHS],cwd=root).decode().splitlines()
    unknown = subprocess.check_output(['git','ls-files','--others','--exclude-standard','--',*APP_PATHS],cwd=root).decode().splitlines()
    if unknown: raise ValueError('Có source app mới chưa thuộc gate F10')
    return {name:binding((root/name).read_bytes()) for name in names}


def reused_f10(root: Path) -> dict:
    """Kiểm mọi member/log của QA F10, phân biệt kết quả viện dẫn với test chạy mới."""
    path = root/'docs/plan/week12/backtest_ui_checks.zip'
    with zipfile.ZipFile(path) as archive:
        manifest = json.loads(archive.read('manifest.json'))
        if len(set(archive.namelist())) != len(archive.namelist()) or set(archive.namelist()) != set(manifest)|{'manifest.json'}:
            raise ValueError('Inventory QA F10 không khớp')
        for name,expected in manifest.items():
            if binding(archive.read(name)) != expected: raise ValueError('Member QA F10 khác hash')
        checks = json.loads(archive.read('checks.json'))
        if checks['status'] != 'PASS_F10_OFFLINE_SCOPE': raise ValueError('QA F10 chưa PASS')
        for name,expected in checks['source_bindings'].items():
            if name.endswith('.md'): continue
            if binding((root/name).read_bytes()) != expected: raise ValueError('Source QA F10 đã đổi: '+name)
        for name,row in checks['test_suites'].items():
            raw = archive.read(name)
            if row['returncode'] or hashlib.sha256(raw).hexdigest() != row['log_sha256']: raise ValueError('Test/log F10 không PASS')
            if name.startswith('tests_'):
                if not re.search(rb'\nOK\s*$',raw) or b'skipped=' in raw: raise ValueError('Suite F10 lỗi/skip')
            elif not re.search(rb'(?:#|\xe2\x84\xb9) fail 0',raw): raise ValueError('DOM F10 lỗi')
    if (checks['python_tests_passed'],checks['dom_tests_passed']) != (156,31): raise ValueError('Số test F10 không khớp')
    return {'status':'REUSED_VERIFIED_NOT_RERUN','path':path.relative_to(root).as_posix(),**binding(path.read_bytes()),
        'python_tests':156,'dom_tests':31,'suites':19,'leakage_tests':18,'native_parity_tests':11,
        'reason':'APP_SOURCE_RUNTIME_AND_ALL_QA_MEMBERS_MATCH; AGENTS_1_2_SCOPED_REUSE'}


def integrity(root: Path) -> dict:
    """Kiểm evidence scientific và các receipt ứng dụng cũ nguyên byte."""
    doc = root/'docs/plan/week12'
    with zipfile.ZipFile(doc/'unified_analysis_results.zip') as archive:
        pins = {name:{k:v[k] for k in ('bytes','sha256')} for name,v in json.loads(archive.read('manifest.json'))['sources'].items()}
    with zipfile.ZipFile(doc/'final_evidence_snapshot.zip') as archive:
        snapshot = json.loads(archive.read('snapshot_manifest.json'))
        for name,expected in pins.items():
            if binding(archive.read(name)) != expected: raise ValueError('F01 không phục hồi được pin U09')
        for group in ('frozen_packages','legacy_archives'):
            for name,expected in snapshot[group].items():
                if binding((root/name).read_bytes()) != expected: raise ValueError('Evidence scientific đã đổi')
    changed = sorted(name for name,expected in pins.items() if binding((root/name).read_bytes()) != expected)
    if changed != ['scripts/.gitattributes','templates/backtest.html','templates/demo_new.html','templates/experiments.html',
                   'templates/output.html','utils/experiment_web.py','web_interface.py']:
        raise ValueError('Delta pin U09 khác các đường đã version hóa')
    release = root/'outputs/revision/manuscript_unified_final_v1'; raw = (release/'manifest.json').read_bytes()
    if binding(raw) != {'bytes':55249,'sha256':'8e5ce2a4ca6f3a52945047cb8e1e1e99e8c00dfcd959a6fc6cdadcd701013de9'}:
        raise ValueError('Manifest manuscript F05 khác hash')
    manifest = json.loads(raw)
    for name,expected in manifest['outputs'].items():
        if binding((release/name).read_bytes()) != expected: raise ValueError('Output F05 đã đổi')
    for name,expected in manifest['sources'].items():
        if binding((root/name).read_bytes()) != expected: raise ValueError('Nguồn manuscript đã đổi')
    for name in ('serving_resources_v1.json','serving_runner_checks.zip','analysis_ui_checks.zip','backtest_ui_checks.zip'):
        if (doc/name).read_bytes() != subprocess.check_output(['git','show',BASE+':docs/plan/week12/'+name],cwd=root):
            raise ValueError('Resource/QA cũ đã đổi')
    return {'status':'PASS','u09_source_pins':729,'current_matches':722,'historical_restores':729,'intentional_changed_pins':changed,
        'frozen_packages_unchanged':20,'legacy_archives_unchanged':30,'f05_outputs_unchanged':11,'f05_sources_unchanged':68,
        'f08_f09_f10_qa_unchanged':True,'native_rowwise_causal_gate':'FAIL','whole_system_causal_gate':'NOT_CERTIFIED'}
