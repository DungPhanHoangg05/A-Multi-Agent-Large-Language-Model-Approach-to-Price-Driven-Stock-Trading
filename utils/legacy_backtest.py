"""Adapter đọc Full/No-Alpha đã lưu; không đổi No-Alpha thành original_common."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import re
from typing import Any


def path(root: Path, identifier: str) -> Path:
    """Chỉ mở tên file do backtest legacy sinh trong một namespace local cố định."""
    if type(identifier) is not str or not re.fullmatch(r'backtest_[A-Z0-9]{1,12}_\d{8}_\d{4}(?:\d{2})?',identifier):
        raise ValueError('ID backtest legacy không hợp lệ')
    base = root.resolve()/'backtest_result'; target = base/(identifier+'.json')
    if not target.resolve().is_relative_to(base) or base.is_symlink() or target.is_symlink():
        raise ValueError('File legacy thoát namespace')
    return target


def catalog(root: Path) -> list[dict]:
    """File legacy không có owner; danh mục local này giữ nguyên phạm vi ứng dụng cũ."""
    base = root/'backtest_result'
    if not base.exists(): return []
    if base.is_symlink() or not base.resolve().is_relative_to(root.resolve()): raise ValueError('Namespace legacy không hợp lệ')
    rows = []
    for file in sorted(base.glob('backtest_*.json')):
        if file == path(root,file.stem): rows.append({'id':file.stem,'kind':'legacy_backtest','label':file.stem,'status':'legacy_saved'})
    return rows


def read(root: Path, identifier: str) -> dict[str, Any]:
    """Giữ số nguồn, thiếu là null; không chứng nhận lại economics/gate của file lịch sử."""
    target = path(root,identifier)
    if target.stat().st_size > 25_000_000: raise ValueError('File legacy quá lớn')
    raw = target.read_bytes()
    def reject(value: str) -> None: raise ValueError('Legacy có số không hữu hạn')
    source = json.loads(raw,parse_constant=reject)
    if type(source) is not dict or type(source.get('test_points')) is not list or len(source['test_points']) > 5000:
        raise ValueError('Không phải BacktestSummary legacy')
    def number(value: Any) -> float | None:
        return float(value) if type(value) in (int,float) and math.isfinite(value) else None
    summary,rows = [],[]
    for method,suffix in (('legacy_full','full'),('legacy_no_alpha','no_alpha')):
        summary.append({'method':method,'accuracy_pct':number(source.get('acc_'+suffix)),
            'return_pct':number(source.get('pnl_'+suffix)),'cycle_end_mdd_pct':number(source.get('mdd_'+suffix)),
            'n_points':len(source['test_points']),'verification':'LEGACY_DECLARED_NOT_RECERTIFIED'})
        for point in source['test_points']:
            if type(point) is not dict: raise ValueError('Test point legacy không hợp lệ')
            prediction = point.get('pred_'+suffix)
            error = str(point.get('error_'+suffix,''))
            action = ('LONG' if prediction == 'LONG' else 'CASH' if prediction == 'SHORT' else None) if not error else None
            rows.append({'method':method,'date':str(point.get('window_end','')),'raw_prediction':prediction if prediction in ('LONG','SHORT') else None,
                'final_action':action,'net_return_pct':number(point.get('account_return_'+suffix))*100 if action is not None and number(point.get('account_return_'+suffix)) is not None else None,
                'error':error,'decision_source':str(point.get('decision_source_'+suffix,'')),
                'reason':'INVALID_OR_MISSING_NOT_CASH' if action is None else str(point.get('decision_fallback_reason_'+suffix,''))})
    return {'version':'legacy_backtest_adapter_v1','run_id':identifier,'kind':'legacy_backtest','status':'legacy_saved',
        'evaluation_status':'LEGACY_DECLARED_NOT_RECERTIFIED','metric_scope':'LEGACY_FULL_VS_NO_ALPHA_ONLY; NOT_PAIRED_WITH_NEW_RUNS',
        'summary':summary,'predictions':rows,'accounts':[],'daily_nav':[],'cycles':[],'contrasts':[],'per_repeat':[],
        'units':{'return':'PERCENT_AS_RECORDED','accuracy':'PERCENT_AS_RECORDED','net_return_pct':'PERCENT_PER_CYCLE_IF_RECORDED'},
        'provenance':{'source_file':target.name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},
        'limitations':['NO_ALPHA_IS_NOT_ORIGINAL_COMMON','MISSING_DATA_NOT_ZERO','LEGACY_ECONOMIC_CONTRACT_NOT_RECERTIFIED']}
