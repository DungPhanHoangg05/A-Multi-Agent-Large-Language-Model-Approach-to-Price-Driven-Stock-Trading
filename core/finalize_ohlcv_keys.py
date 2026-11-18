"""Khóa truy xuất FIN06 từ 45 nến PIT, tách khỏi báo cáo thị giác của Decision."""
from __future__ import annotations

from decimal import Decimal, localcontext
import math
from typing import Any

import pandas as pd

from core.historical_signals import snapshot_payload
from core.unified_contracts import day, digest

PROFILE = "ohlcv_retrieval_keys_v1"
WINDOW = 45
PRICE = ("Open", "High", "Low", "Close")
FIELDS = ("Datetime", *PRICE, "Volume")
PATTERN = "pattern_ohlcv_rule"
TREND = "trend_ohlcv_rule"
RULES = {
    "profile": PROFILE, "window_sessions": WINDOW, "calendar": "LAST_45_VERIFIED_VNINDEX_SESSIONS",
    "input": "OHLCV_RAW_THOUSAND_VND; ROW_DATE_LE_CUTOFF; EXACT_SESSION_WINDOW",
    "numeric": "DECIMAL_FROM_STR_PYTHON_SCALAR_PRECISION_40",
    "pattern": {"definition": "Hai thân trái hướng, thân cuối bao phủ toàn bộ và dài hơn thân trước.",
                "body_range_min_fraction": "0.5", "body_range_bound": "INCLUSIVE",
                "no_pattern": "NEUTRAL"},
    "trend": {"definition": "Khoảng cách SMA10/SMA30 và lợi nhuận 10 phiên cùng vượt ngưỡng theo một hướng.",
              "sma_fast": 10, "sma_slow": 30, "momentum_sessions": 10,
              "ratio_band": "0.005", "threshold_bound": "STRICT", "mixed_or_equal": "NEUTRAL"},
    "missing": "NA_WITH_REASON; NO_ZERO_FILL_OR_NEUTRAL_IMPUTATION",
    "classification_fields": [PATTERN, TREND],
}


def technical_key(window: dict[str, list], cutoff: str, sessions: list[str]) -> dict[str, Any]:
    """Cả bank và query gọi đúng hàm này trên snapshot OHLCV của cutoff."""
    day(cutoff)
    if set(window) != set(FIELDS) or any(type(window[k]) is not list for k in FIELDS):
        raise ValueError("Snapshot khóa kỹ thuật cần đúng schema OHLCV")
    dates = [day(d) for d in window["Datetime"]]
    expected = [day(d) for d in sessions]
    if (len(expected) > WINDOW or expected != sorted(set(expected)) or not expected or expected[-1] != cutoff
            or dates != sorted(set(dates)) or any(d > cutoff for d in dates)
            or any(len(window[k]) != len(dates) for k in FIELDS)):
        raise ValueError("Ngày snapshot khóa kỹ thuật không hợp lệ hoặc vượt cutoff")

    reason = None
    if len(expected) < WINDOW or len(dates) < WINDOW:
        reason = "INSUFFICIENT_WINDOW"
    elif dates != expected:
        reason = "SESSION_WINDOW_MISMATCH"
    elif any(value is None or (type(value) is float and not math.isfinite(value))
             for name in FIELDS[1:] for value in window[name]):
        reason = "MISSING_OHLCV"
    if any(type(value) not in (int, float, type(None)) for name in FIELDS[1:] for value in window[name]):
        raise ValueError("OHLCV khóa kỹ thuật cần số Python gốc")
    canonical = {name: [None if type(v) is float and not math.isfinite(v) else v for v in window[name]]
                 for name in FIELDS}
    result = {"profile": PROFILE, "cutoff": cutoff, "window_sha256": digest(canonical),
              "window_rows": len(dates), "reason": reason, PATTERN: None, TREND: None}
    if reason:
        return result

    # Decimal giữ đúng trường hợp bằng ngưỡng từ số VND gốc, không dùng epsilon.
    with localcontext() as context:
        context.prec = 40
        o, h, low, c = ([Decimal(str(v)) for v in window[name]] for name in PRICE)
        if any(not 0 < l <= min(a, b) <= max(a, b) <= u for a, u, l, b in zip(o, h, low, c)) or any(
                v < 0 for v in window["Volume"]):
            raise ValueError("Nến khóa kỹ thuật có giá hoặc khối lượng sai")
        last_body = c[-1] - o[-1]
        previous_body = c[-2] - o[-2]
        p = RULES["pattern"]
        wide = abs(last_body) >= Decimal(p["body_range_min_fraction"]) * (h[-1] - low[-1])
        if wide and previous_body < 0 < last_body and o[-1] <= c[-2] and c[-1] >= o[-2] and last_body > -previous_body:
            result[PATTERN] = "BULLISH"
        elif wide and last_body < 0 < previous_body and o[-1] >= c[-2] and c[-1] <= o[-2] and -last_body > previous_body:
            result[PATTERN] = "BEARISH"
        else:
            result[PATTERN] = "NEUTRAL"
        t = RULES["trend"]
        # Nhân chéo để giữ biên nghiêm ngặt ngay cả khi SMA là thập phân tuần hoàn.
        fast = sum(c[-t["sma_fast"]:]) * t["sma_slow"]
        slow = sum(c[-t["sma_slow"]:]) * t["sma_fast"]
        base = c[-1 - t["momentum_sessions"]]
        band = Decimal(t["ratio_band"])
        upper, lower = 1 + band, 1 - band
        result[TREND] = ("BULLISH" if fast > slow * upper and c[-1] > base * upper else
                         "BEARISH" if fast < slow * lower and c[-1] < base * lower else "NEUTRAL")
    return result


def key_at(frame: pd.DataFrame, calendar: pd.DatetimeIndex, cutoff: str) -> dict[str, Any]:
    """Cắt nguồn trước khi đọc giá/volume và tạo đúng projection dùng chung."""
    timestamp = pd.Timestamp(day(cutoff))
    visible = frame.loc[frame.Datetime <= timestamp, list(FIELDS)].tail(WINDOW)
    sessions = calendar[calendar <= timestamp][-WINDOW:].strftime("%Y-%m-%d").tolist()
    return technical_key(snapshot_payload(visible), cutoff, sessions)
