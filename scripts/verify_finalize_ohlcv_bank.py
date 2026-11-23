"""Verifier độc lập bằng phân số chính xác, chạy trên mọi cửa sổ bank và query FIN06."""
from __future__ import annotations

from fractions import Fraction
import math
from pathlib import Path
from typing import Any

import pandas as pd

from core.execution_prices import load_verified_execution_data
from core.finalize_price_acceptance import ACCEPTANCE
from core.unified_contracts import digest
from core.unified_protocol import CORE4, read, safe


def oracle(window: dict, sessions: list[str]) -> tuple[str | None, str | None, str | None]:
    """Tái dẫn xuất bằng độ dài khoảng và bất đẳng thức nhân chéo nguyên."""
    if min(len(window["Datetime"]), len(sessions)) < 45:
        return "INSUFFICIENT_WINDOW", None, None
    if window["Datetime"] != sessions:
        return "SESSION_WINDOW_MISMATCH", None, None
    columns = ("Open", "High", "Low", "Close", "Volume")
    if any(v is None or not math.isfinite(v) for name in columns for v in window[name]):
        return "MISSING_OHLCV", None, None
    previous = [Fraction(str(window[name][-2])) for name in ("Open", "Close")]
    last = [Fraction(str(window[name][-1])) for name in ("Open", "Close")]
    prior_lo, prior_hi = sorted(previous)
    last_lo, last_hi = sorted(last)
    bar_range = Fraction(str(window["High"][-1])) - Fraction(str(window["Low"][-1]))
    contained = last_lo <= prior_lo and prior_hi <= last_hi and last_hi - last_lo > prior_hi - prior_lo
    pattern = "NEUTRAL"
    if contained and 2 * (last_hi - last_lo) >= bar_range and (previous[1] - previous[0]) * (last[1] - last[0]) < 0:
        pattern = "BULLISH" if last[1] > last[0] else "BEARISH"
    closes = [Fraction(str(p)) for p in window["Close"]]
    scaled_fast = 600 * sum(closes[-10:])
    slow_sum = sum(closes[-30:])
    scaled_end = 200 * closes[-1]
    if scaled_fast > 201 * slow_sum and scaled_end > 201 * closes[-11]:
        trend = "BULLISH"
    elif scaled_fast < 199 * slow_sum and scaled_end < 199 * closes[-11]:
        trend = "BEARISH"
    else:
        trend = "NEUTRAL"
    return None, pattern, trend


def verify_windows(root: Path, bank: dict, query: dict) -> dict[str, Any]:
    """Đọc CSV trực tiếp và kiểm lại mọi khóa, số dòng, span và SHA cửa sổ."""
    accepted = read(root, ACCEPTANCE, True)
    market = pd.read_csv(safe(root, accepted["calendar"]), dtype={"Datetime": str})["Datetime"].tolist()
    sessions = {d: market[max(0, index - 44):index + 1] for index, d in enumerate(market)}
    bank_frames = {s: load_verified_execution_data(root / accepted["bank_source"], s)[0].assign(
        Datetime=lambda data: data.Datetime.dt.strftime("%Y-%m-%d")) for s in CORE4}
    query_frames = {}
    for link in accepted["query_sources"]:
        raw = pd.read_csv(safe(root, link["raw_csv"]), dtype={"Datetime": str})
        query_frames[link["symbol"]] = raw.loc[raw["Datetime"] >= link["origin"]]
    columns = ("Datetime", "Open", "High", "Low", "Close", "Volume")
    counts = {}
    for name, records, frames, date_field in (("bank", bank["records"], bank_frames, "as_of_date"),
                                                ("query", query["records"], query_frames, "cutoff")):
        for row in records:
            cutoff = row[date_field]
            frame = frames[row["symbol"]]
            visible = frame.loc[frame["Datetime"] <= cutoff, list(columns)].tail(45)
            window = {k: visible[k].tolist() if k == "Datetime" else visible[k].astype(float).tolist()
                      for k in columns}
            expected = oracle(window, sessions[cutoff])
            key = row["retrieval_key"]
            if ((key["reason"], key["pattern_ohlcv_rule"], key["trend_ohlcv_rule"]) != expected
                    or key["cutoff"] != cutoff or key["window_rows"] != len(window["Datetime"])
                    or key["window_sha256"] != digest(window)):
                raise ValueError(f"Oracle độc lập không khớp khóa {name}: {row['symbol']} {cutoff}")
        counts[name] = len(records)
    return {"status": "PASS", "oracle": "INDEPENDENT_RATIONAL_CROSS_MULTIPLICATION", "windows_verified": counts}
