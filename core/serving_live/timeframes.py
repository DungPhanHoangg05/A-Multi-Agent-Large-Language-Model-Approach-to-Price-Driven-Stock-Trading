"""Khóa nến khung người dùng chọn cùng ngữ cảnh ngày, không đổi mục tiêu T+2.5 thành số nến."""
from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd

from core.historical_evaluation_journal import save
from core.historical_evaluation_scope import SYMBOLS
from core.serving_live.snapshots import VERSION, ZONE, clean
from core.unified_contracts import checksum, digest

TIMEFRAMES = ('5m','15m','30m','1h','1d','1w','1mo')


def market_chart(symbol: str, timeframe: str) -> pd.DataFrame:
    """Tái dùng VCI/KBS, giữ cấu hình lookback và số nến theo khung của form realtime."""
    from core.realtime_loader import fetch_realtime_ohlcv
    frame,error = fetch_realtime_ohlcv(symbol,timeframe,use_cache=False)
    if error or frame.empty: raise ValueError('Không lấy được nến realtime theo khung đã chọn')
    return frame


def chart_frame(source: pd.DataFrame, now: datetime) -> pd.DataFrame:
    """Timestamp VN, OHLCV hợp lệ; không nhận nến tương lai hoặc lặng lẽ cắt bỏ vi phạm."""
    from core.realtime_loader import _clean_realtime_frame
    frame = source.copy(deep=True)
    dates = pd.to_datetime(frame['Datetime'])
    if dates.dt.tz is not None: dates = dates.dt.tz_convert(ZONE).dt.tz_localize(None)
    frame['Datetime'] = dates
    frame = _clean_realtime_frame(frame,'realtime')
    end = pd.Timestamp(now).tz_convert(ZONE).tz_localize(None)
    if frame.empty or (frame.Datetime > end).any():
        raise ValueError('Nến realtime trống hoặc vượt thời điểm capture')
    if (end-frame.Datetime.iloc[-1]).days > 40:
        raise ValueError('Nguồn nến realtime quá cũ')
    return frame


def chart_document(frame: pd.DataFrame) -> dict:
    """Giữ giờ trong nến intraday; không dùng formatter ngày làm mất timestamp."""
    return {'Datetime':frame.Datetime.dt.strftime('%Y-%m-%d %H:%M:%S').tolist(),
            **{name:frame[name].astype(float).tolist() for name in ('Open','High','Low','Close','Volume')}}


def extend_daily(daily: pd.DataFrame, bars: pd.DataFrame, cutoff: str) -> pd.DataFrame:
    """Chỉ tổng hợp phiên đang hình thành khi có nến từ đầu phiên; không nội suy giá/volume."""
    if str(daily.Datetime.iloc[-1].date()) >= cutoff:
        return daily.loc[daily.Datetime <= pd.Timestamp(cutoff)].copy()
    visible = bars.loc[bars.Datetime.dt.strftime('%Y-%m-%d') == cutoff]
    if visible.empty or (visible.Datetime.iloc[0].hour,visible.Datetime.iloc[0].minute) > (9,15):
        raise ValueError('Thiếu nến đầu phiên để tạo daily provisional đúng OHLCV')
    ratio = float(visible.Close.iloc[-1])/float(daily.Close.iloc[-1])
    if not .25 < ratio < 4:
        raise ValueError('Giá intraday và daily khác đơn vị hoặc có biến cố chưa kiểm; không tự rescale')
    row = {'Datetime':pd.Timestamp(cutoff),'Open':float(visible.Open.iloc[0]),'High':float(visible.High.max()),
           'Low':float(visible.Low.min()),'Close':float(visible.Close.iloc[-1]),'Volume':float(visible.Volume.sum())}
    return pd.concat([daily,pd.DataFrame([row])],ignore_index=True)


def capture(store: Any, symbol: str, timeframe: str, owner: str) -> dict:
    """Một capture cho cả chart và daily features; không gọi LLM hoặc tạo payoff query."""
    if symbol not in SYMBOLS or timeframe not in TIMEFRAMES or not checksum(owner):
        raise ValueError('Mã/khung/owner realtime không hợp lệ')
    from core.serving_live.snapshots import frame_document
    from core.realtime_loader import get_timeframe_cfg
    now = store.now().astimezone(ZONE)
    chart = chart_frame(store.charts(symbol,timeframe),now)
    stock,index = clean(store.prices(symbol),pd.Timestamp(now.date())),clean(store.prices('VNINDEX'),pd.Timestamp(now.date()))
    if timeframe in ('5m','15m','30m','1h'):
        cutoff = str(chart.Datetime.iloc[-1].date())
    else:
        # Nhãn tuần/tháng không nói phiên cuối đã quan sát; dùng VNINDEX thực, không đoán ngày nghỉ.
        index_bars = chart_frame(store.charts('VNINDEX','5m'),now)
        cutoff = str(index_bars.Datetime.iloc[-1].date())
        index = extend_daily(index,index_bars,cutoff)
    if str(index.Datetime.iloc[-1].date()) < cutoff:
        index = extend_daily(index,chart_frame(store.charts('VNINDEX','5m'),now),cutoff)
    if str(stock.Datetime.iloc[-1].date()) < cutoff:
        bars = chart if timeframe in ('5m','15m') else chart_frame(store.charts(symbol,'5m'),now)
        stock = extend_daily(stock,bars,cutoff)
    stock,index = stock.loc[stock.Datetime <= cutoff].copy(),index.loc[index.Datetime <= cutoff].copy()
    if (len(stock) < 600 or len(index) < 600 or str(stock.Datetime.iloc[-1].date()) != cutoff
            or str(index.Datetime.iloc[-1].date()) != cutoff or (pd.Timestamp(now.date())-pd.Timestamp(cutoff)).days > 10
            or not pd.DatetimeIndex(stock.Datetime).isin(pd.DatetimeIndex(index.Datetime)).all()):
        raise ValueError('Ngữ cảnh ngày thiếu 600 phiên hoặc không khớp phiên chart')
    if chart.Datetime.iloc[-1].date() > pd.Timestamp(cutoff).date(): raise ValueError('Chart vượt cutoff ngày')
    ratio = float(chart.Close.iloc[-1])/float(stock.Close.iloc[-1])
    if not .25 < ratio < 4:
        raise ValueError('Đơn vị giá chart và daily không nhất quán; không tự nhân/chia đơn vị')
    candles = get_timeframe_cfg(timeframe)['candles']
    if len(chart) < min(candles,35): raise ValueError('Không đủ nến để phân tích khung đã chọn')
    # Giữ nguyên các rào dated/scorer của capture ngày, không tái dùng tin frozen cũ.
    from core.historical_evaluation_data import FrozenNews
    news = []
    for row in store.news(symbol,cutoff):
        if not row.get('date_parsed'): continue
        if pd.Timestamp(row['date_parsed']) > pd.Timestamp(cutoff): raise ValueError('Tin vượt cutoff realtime')
        news.append(row)
    FrozenNews({symbol:news}).get_sentiment_at(symbol,cutoff)
    record = {'version':VERSION,'owner_scope_sha256':owner,'symbol':symbol,'cutoff':cutoff,'captured_at':now.isoformat(),
        'prices':frame_document(stock),'index':frame_document(index),'news':news,
        'chart':chart_document(chart.tail(candles)),'chart_timeframe':timeframe,
        'daily_provisional':cutoff == str(now.date()) and (now.hour,now.minute) < (15,30),
        'calendar_policy':'OBSERVED_VNINDEX; QUERY_T1_T3_WEEKDAY_PLAN_ONLY',
        'price_unit':'thousand_VND','source':'VNSTOCK_VCI_KBS_VENDOR_SERIES_LIMITED',
        'corporate_actions':'LIVE_EVENT_LEDGER_UNAVAILABLE; VENDOR_ADJUSTMENT_RISK',
        'scientific_status':'REALTIME_CHART_DAILY_CONTEXT_TRANSFER; EXPLORATORY_NOT_CERTIFIED'}
    identifier = digest(record); path = store.path(identifier)
    if path.exists(): store.read(identifier,owner)
    else: save(path,record)
    return store.summary(identifier,record)
