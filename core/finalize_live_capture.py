"""Capture live riêng cho raw VCI, event ledger và lịch VNINDEX sau đóng phiên."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import pandas as pd

from core.causal_alpha import frame_document
from core.execution_prices import RAW_FIELD_MAP, validate_raw_frame
from core.finalize_price_acceptance import ACCEPTANCE
from core.finalize_serving_profile import LIVE_CAPTURE, SCIENTIFIC_STATUS
from core.historical_evaluation_journal import save
from core.realtime_index import CONTRACT, index_document
from core.serving_live.errors import at
from core.serving_live.snapshots import ZONE, clean_market_index
from core.unified_contracts import checksum, digest
from core.unified_protocol import read


def raw_pages(symbol: str, origin: str, cutoff: str) -> tuple[list, list, dict]:
    """Dùng ABI REST VCI đã có trong nguồn raw FIN04, chỉ chạy lúc POST capture."""
    from scripts.verify_execution_price_gate import BASE_URL, EVENT_CODES, fetch_paginated
    start, end = origin.replace("-", ""), cutoff.replace("-", "")
    prices, p_pins = fetch_paginated(f"{BASE_URL}/company/{symbol}/price-history", {"fromDate": start, "toDate": end})
    events, e_pins = fetch_paginated(f"{BASE_URL}/events", {"ticker": symbol, "fromDate": start,
        "toDate": f"{cutoff[:4]}1231", "eventCode": EVENT_CODES})
    return prices, events, {"prices": p_pins, "events": e_pins}


def capture(root: Path, snapshots: Any, symbol: str, owner: str, *, fetch: Callable | None = None) -> dict:
    """Khóa đúng origin, chọn phiên hoàn tất rồi lưu một snapshot owner-bound."""
    from core.finalize_serving_resources import FinalizedResources
    accepted = read(root, ACCEPTANCE, True)
    sources = {r["symbol"]: r for r in accepted["query_sources"]}
    if symbol not in sources or not checksum(owner):
        raise ValueError("Mã hoặc owner ngoài miền finalized live")
    now = snapshots.now().astimezone(ZONE)
    today = pd.Timestamp(now.date())
    market = at("index.validate", clean_market_index, at("index.daily", snapshots.prices, "VNINDEX"), today)
    closed = today - pd.Timedelta(days=int((now.hour, now.minute) < (15, 30)))
    market = market.loc[market.Datetime <= closed]
    if len(market) < 600 or (today-market.Datetime.iloc[-1]).days > 10:
        raise ValueError("Thiếu lịch VNINDEX hoàn tất hoặc dữ liệu đã cũ")
    cutoff = str(market.Datetime.iloc[-1].date())
    origin = sources[symbol]["origin"]
    prices, events, pins = at("prices.daily", fetch or raw_pages, symbol, origin, cutoff)
    source = pd.DataFrame(prices)
    columns = {k: v for k, v in RAW_FIELD_MAP.items() if v != "MatchPrice"}
    if not {*columns, "ticker"}.issubset(source) or not source.ticker.eq(symbol).all():
        raise ValueError("Capture VCI thiếu trường raw hoặc có lẫn mã")
    frame = source[list(columns)].rename(columns=columns).copy()
    frame["Datetime"] = pd.to_datetime(frame.Datetime, errors="raise")
    for name in ("Open", "High", "Low", "Close", "Reference"):
        frame[name] = pd.to_numeric(frame[name], errors="raise") / 1000.
    frame["Volume"] = pd.to_numeric(frame.Volume, errors="raise")
    frame = frame.sort_values("Datetime").reset_index(drop=True)
    validate_raw_frame(frame)
    if not frame.Datetime.between(pd.Timestamp(origin), pd.Timestamp(cutoff)).all():
        raise ValueError("Capture VCI có nến ngoài origin/cutoff")
    if any(row.get("ticker", row.get("organCode")) != symbol for row in events):
        raise ValueError("Ledger live có sự kiện khác mã")
    record = {"version": LIVE_CAPTURE, "owner_scope_sha256": owner, "symbol": symbol, "cutoff": cutoff,
        "captured_at": now.isoformat(), "prices": {**frame_document(frame), "Reference": frame.Reference.astype(float).tolist()},
        "index": index_document(market), "index_contract": CONTRACT, "events": events, "source_receipts": pins,
        "news": [], "source": "VCI_RAW_EXECUTION_FIELDS", "price_unit": "thousand_VND",
        "corporate_actions": "VCI_EVENT_LEDGER_PIT_AVAILABILITY_WITH_REFERENCE_GAPS",
        "calendar_policy": "OBSERVED_VNINDEX; LIVE_T1_T3_PLAN_ONLY", "scientific_status": SCIENTIFIC_STATUS}
    identifier = digest(record)
    resources = FinalizedResources(root, record, identifier)
    resources.verify()
    path = snapshots.path(identifier)
    if not path.exists():
        save(path, record)
    elif snapshots.read(identifier, owner) != record:
        raise ValueError("Capture SHA xung đột")
    return {**snapshots.summary(identifier, record), "capture_version": LIVE_CAPTURE}
