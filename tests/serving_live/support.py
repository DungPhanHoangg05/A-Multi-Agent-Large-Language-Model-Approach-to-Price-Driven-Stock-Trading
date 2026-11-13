"""Nguồn giá mới mô phỏng để kiểm đường live, không gọi thị trường hoặc Groq thật."""
from datetime import datetime
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT),str(ROOT/'tests/serving_runtime')]
# Tên fixture runtime được nạp riêng để không trùng tên module support hiện tại.
import importlib.util
spec = importlib.util.spec_from_file_location('serving_runtime_fixture',ROOT/'tests/serving_runtime/support.py')
runtime = importlib.util.module_from_spec(spec); spec.loader.exec_module(runtime)
Clock, Sender = runtime.Clock, runtime.Sender


def prices(symbol: str) -> pd.DataFrame:
    """Giữ lịch nguồn 2018–2026; nối OHLCV synthetic sau snapshot cũ tới 12/11/2026."""
    if symbol == 'VNINDEX':
        protocol = json.loads((ROOT/'docs/plan/week11/historical_evaluation_protocol.json').read_bytes())['payload']
        frame = pd.read_csv(ROOT/protocol['effective_mt_bicl']['calendar']['source'])
        frame['Datetime'] = pd.to_datetime(frame.Datetime)
        for name in ('Open','High','Low'):
            if name not in frame: frame[name] = frame.Close * (1.01 if name == 'High' else .99 if name == 'Low' else 1.)
        if 'Volume' not in frame: frame['Volume'] = 100000.
    else:
        manifest = json.loads((ROOT/'outputs/unified_integration/u06_assets_v2/frozen_alpha_manifest.json').read_bytes())
        frame = pd.DataFrame(json.loads((ROOT/manifest['causal_sources'][symbol+'/f2026_q3']['prices']).read_bytes()))
        frame['Datetime'] = pd.to_datetime(frame.Datetime)
    frame = frame.loc[frame.Datetime >= '2018-01-02',['Datetime','Open','High','Low','Close','Volume']].copy()
    dates = pd.bdate_range(frame.Datetime.iloc[-1]+pd.Timedelta(days=1),'2026-11-12')
    n = np.arange(1,len(dates)+1,dtype=float)
    close = frame.Close.iloc[-1]*np.exp(.0007*n+.008*np.sin(n*.7))
    opening = close*(1.+.002*np.sin(n*1.2))
    extension = pd.DataFrame({'Datetime':dates,'Open':opening,
        'High':np.maximum(opening,close)*(1.005+.002*np.sin(n*.4)),
        'Low':np.minimum(opening,close)*(.995-.002*np.cos(n*.3)),
        'Close':close,'Volume':np.rint(100000.+80000.*np.random.default_rng(42).uniform(size=len(dates)))})
    return pd.concat([frame,extension],ignore_index=True)


def news(symbol: str, cutoff: str) -> list[dict]:
    """Ba tin có ngày/score xác minh đủ điều kiện, một tin undated bị loại."""
    return [{'date_parsed':'2026-11-09','numeric_score':.2,'scorer':'lexicon'} for _ in range(3)]+[{'date_parsed':None}]


def request(identifier: str, cutoff: str, ids: list[str], *, mode: str = 'analyze', symbol: str = 'MWG') -> dict:
    from core.serving_runtime.resources import default_models
    return {'version':'variant_serving_live_v1','snapshot_id':identifier,'request':{'version':'variant_serving_v1',
        'mode':mode,'variant_ids':ids,'symbols':[symbol],'start_date':cutoff,'end_date':cutoff,
        'timeframe':'1d','language':'vi','repeats':1,'models':default_models()}}


def charts(symbol: str, timeframe: str) -> pd.DataFrame:
    """Nến các khung thật về schema, dữ liệu synthetic tại 10h ngày13/11; không tải thị trường."""
    daily = prices(symbol)
    if timeframe in ('1d','1w','1mo'):
        if timeframe == '1d': return daily.tail(200)
        rule = 'W-MON' if timeframe == '1w' else 'MS'
        return daily.set_index('Datetime').resample(rule,label='left',closed='left').agg(
            {'Open':'first','High':'max','Low':'min','Close':'last','Volume':'sum'}).dropna().reset_index().tail(120)
    minutes = {'5m':5,'15m':15,'30m':30,'1h':60}[timeframe]
    stamps = pd.DatetimeIndex([stamp for day in pd.bdate_range('2026-10-20','2026-11-13')
        for stamp in pd.date_range(day+pd.Timedelta(hours=9),day+pd.Timedelta(hours=14,minutes=45),freq=f'{minutes}min')
        if stamp <= pd.Timestamp('2026-11-13 10:00')])
    n = np.arange(len(stamps),dtype=float)
    close = float(daily.Close.iloc[-1])*(1.+.002*np.sin(n*.4))
    return pd.DataFrame({'Datetime':stamps,'Open':close*.999,'High':close*1.002,'Low':close*.998,
                         'Close':close,'Volume':1000.+np.arange(len(stamps))%100}).tail(250)
