"""Fixture tổng hợp nhiều point/repeat cho serving backtest, không phải giá thị trường."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT),str(ROOT/'tests/serving_runtime')]
from support import Clock, Provider as BaseProvider, Sender, FixtureResources as BaseResources, original
from core.serving_contracts import ServingRequest
from core.serving_runtime.resources import default_models


def frame() -> pd.DataFrame:
    """Hai chu kỳ không chồng nhau, giá nguồn nghìn VND và nhãn UP sau phí."""
    return pd.DataFrame({'Datetime':pd.bdate_range('2026-07-02',periods=7),
        'Open':[100.]*7,'High':[120.]*7,'Low':[95.]*7,
        'Close':[100.,101.,102.,110.,101.,102.,110.],'Volume':[1000.]*7})


class Resources(BaseResources):
    """Chỉ DI server/test; client không được gửi cờ synthetic để vượt preflight."""
    def document(self) -> dict:
        doc = super().document()
        doc['support']['calendar'] = frame().Datetime.dt.strftime('%Y-%m-%d').tolist()
        return doc


class Provider(BaseProvider):
    """Forecast nguyên adapter native/common; payoff từ oracle sau barrier của runner."""
    def outcome(self, point: dict) -> dict:
        from core.unified_experiment import outcome_from_frame
        self.outcome_count += 1
        data = frame(); data[['Open','High','Low','Close']] *= 1000.
        return outcome_from_frame(point,data,'1'*64)


def spec(variants: list[str] | None = None, repeats: int = 2) -> ServingRequest:
    """Tám slot trên hai point, hai repeat, native/common tường minh."""
    return ServingRequest.create({'version':'variant_serving_v1','mode':'backtest',
        'variant_ids':variants or ['original_fix','original_common'],'symbols':['FPT'],
        'start_date':'2026-07-02','end_date':'2026-07-07','timeframe':'1d','language':'vi','repeats':repeats,'models':default_models()})


def prices(*args: object) -> dict[str,pd.DataFrame]:
    """Tách loader định giá test khỏi model/provider, không tải dữ liệu ngoài."""
    return {'FPT':frame(),'VNM':frame()}


def legacy() -> dict:
    """Số 0 hợp lệ và lỗi SHORT không được suy thành CASH; field secret bị loại khỏi projection."""
    return {'symbol':'FPT','n_tests':2,'pnl_full':0.,'pnl_no_alpha':-1.,'acc_full':50.,'acc_no_alpha':None,
        'mdd_full':0.,'mdd_no_alpha':None,'api_key':'fixture-do-not-export',
        'test_points':[{'window_end':'2026-07-02','pred_full':'SHORT','pred_no_alpha':'LONG','account_return_full':0.,
            'account_return_no_alpha':-.01,'error_full':'','error_no_alpha':''},
            {'window_end':'2026-07-07','pred_full':'SHORT','pred_no_alpha':'N/A','account_return_full':0.,
            'error_full':'=1+1','error_no_alpha':'timeout'}]}
