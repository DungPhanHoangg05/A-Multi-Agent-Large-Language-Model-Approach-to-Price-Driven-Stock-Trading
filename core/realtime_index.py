"""VNINDEX chỉ phục vụ lịch/HMM: dùng ngày và Close gốc, không đòi hoặc sửa OHLC không được dùng."""
from __future__ import annotations

from datetime import datetime,timedelta

import numpy as np
import pandas as pd

CONTRACT = 'vnindex_close_v1'


def clean_index(frame: pd.DataFrame, *, daily: bool = True) -> pd.DataFrame:
    """Close hữu hạn/dương và lịch duy nhất; stock OHLCV giữ bộ kiểm riêng nghiêm ngặt."""
    from core.realtime_loader import _normalise_columns
    view = _normalise_columns(frame)
    if view.empty or not {'Datetime','Close'} <= set(view):
        raise ValueError('VNINDEX thiếu ngày hoặc Close')
    view = view[['Datetime','Close']].copy()
    view['Datetime'] = pd.to_datetime(view.Datetime,errors='coerce',format='mixed')
    dates = pd.DatetimeIndex(view.Datetime)
    if dates.hasnans or dates.has_duplicates or dates.tz is not None or (daily and not dates.equals(dates.normalize())):
        raise ValueError('Lịch VNINDEX thiếu, trùng, có timezone hoặc sai khung ngày')
    view['Close'] = pd.to_numeric(view.Close,errors='coerce')
    if not np.isfinite(view.Close.to_numpy(dtype=float)).all() or (view.Close<=0).any():
        raise ValueError('Close VNINDEX không hữu hạn hoặc không dương')
    return view.sort_values('Datetime').reset_index(drop=True)


def fetch_index_history(interval: str = '1d', *, lookback_days: int | None = None,
                        tail: int | None = None) -> tuple[pd.DataFrame,str]:
    """VCI rồi KBS, không cache lẫn với OHLCV; không nội suy hoặc nhân/chia điểm chỉ số."""
    from core.realtime_loader import DATA_SOURCES,INTERVAL_MAP,get_timeframe_cfg,_fetch_from_vnstock
    if interval not in INTERVAL_MAP: return pd.DataFrame(),'Khung VNINDEX không được hỗ trợ'
    config = get_timeframe_cfg(interval)
    days = config['lookback_days'] if lookback_days is None else lookback_days
    rows = config['tail'] if tail is None else tail
    if days<1 or rows<1: return pd.DataFrame(),'Cửa sổ VNINDEX cần là số dương'
    end = datetime.now(); start = end-timedelta(days=days)
    errors = []
    for source in DATA_SOURCES:
        try:
            raw = _fetch_from_vnstock('VNINDEX',start.strftime('%Y-%m-%d'),end.strftime('%Y-%m-%d'),INTERVAL_MAP[interval],source)
            view = clean_index(raw,daily=interval=='1d')
            print(f'[RealtimeIndex] VNINDEX ← vnstock/{source}: {len(view)} nến; hợp đồng Datetime/Close, đơn vị điểm')
            return view.tail(rows).reset_index(drop=True),''
        except ValueError:
            errors.append(source+': dữ liệu ngày/Close không hợp lệ')
        except Exception:
            errors.append(source+': nguồn chưa khả dụng')
    return pd.DataFrame(),'Không lấy được VNINDEX: '+'; '.join(errors)


def index_document(frame: pd.DataFrame) -> dict:
    """JSON ngày/Close nguyên bản; không chế Open/High/Low/Volume cho chỉ số."""
    view = clean_index(frame)
    return {'Datetime':view.Datetime.dt.strftime('%Y-%m-%d').tolist(),'Close':view.Close.astype(float).tolist()}


def index_frame(document: dict) -> pd.DataFrame:
    """Đọc cả snapshot OHLCV cũ và view Close mới; phần model chỉ nhận hai cột cần thiết."""
    return clean_index(pd.DataFrame(document))
