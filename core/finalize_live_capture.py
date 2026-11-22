"""Capture live riêng cho raw VCI, event ledger và lịch VNINDEX sau đóng phiên."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import pandas as pd

from core.causal_alpha import frame_document
from core.execution_prices import RAW_FIELD_MAP, validate_raw_frame
from core.finalize_serving_profile import LIVE_CAPTURE, SCIENTIFIC_STATUS
from core.historical_evaluation_journal import save
from core.realtime_index import CONTRACT, index_document
from core.serving_live.cafef_news import capture_live_news
from core.serving_live.errors import at
from core.serving_live.snapshots import ZONE, clean_market_index
from core.unified_contracts import checksum, digest


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
    baseline = FinalizedResources(root)
    if symbol not in baseline.sources or not checksum(owner):
        raise ValueError("Mã hoặc owner ngoài miền finalized live")
    now = snapshots.now().astimezone(ZONE)
    today = pd.Timestamp(now.date())
    market = at("index.validate", clean_market_index, at("index.daily", snapshots.prices, "VNINDEX"), today)
    closed = today - pd.Timedelta(days=int((now.hour, now.minute) < (15, 30)))
    market = market.loc[market.Datetime <= closed]
    if len(market) < 600 or (today-market.Datetime.iloc[-1]).days > 10:
        raise ValueError("Thiếu lịch VNINDEX hoàn tất hoặc dữ liệu đã cũ")
    cutoff = str(market.Datetime.iloc[-1].date())
    origin = baseline.sources[symbol]["origin"]
    # Nguồn live có giới hạn độ dài. Chỉ bù phần đầu từ lịch đã khóa và
    # giữ nguyên kiểm tra khớp từng phiên trên toàn bộ phần giao nhau.
    pinned_index = baseline.calendar[["Datetime", "Close"]]
    prefix = pinned_index.loc[pinned_index.Datetime < market.Datetime.iloc[0]]
    if not prefix.empty:
        if int(market.Datetime.le(pinned_index.Datetime.iloc[-1]).sum()) < 600:
            raise ValueError("Thiếu 600 phiên trùng lịch VNINDEX đã khóa để nối lịch live")
        market = pd.concat([prefix, market], ignore_index=True)
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
    news, news_summary, related_news = at('news.fetch', capture_live_news, symbol, now)
    record = {"version": LIVE_CAPTURE, "owner_scope_sha256": owner, "symbol": symbol, "cutoff": cutoff,
        "captured_at": now.isoformat(), "prices": {**frame_document(frame), "Reference": frame.Reference.astype(float).tolist()},
        "index": index_document(market), "index_contract": CONTRACT, "events": events,
        "source_receipts": pins if prefix.empty else {**pins, "index_prefix": baseline.pins[baseline.acceptance["calendar"]]},
        "news": news, "live_news": news_summary, "related_news": related_news,
        "source": "VCI_RAW_EXECUTION_FIELDS", "price_unit": "thousand_VND",
        "corporate_actions": "VCI_EVENT_LEDGER_PIT_AVAILABILITY_WITH_REFERENCE_GAPS",
        "calendar_policy": ("OBSERVED_VNINDEX; LIVE_T1_T3_PLAN_ONLY" if prefix.empty
                            else "PINNED_VNINDEX_PREFIX; OBSERVED_VNINDEX; LIVE_T1_T3_PLAN_ONLY"),
        "scientific_status": SCIENTIFIC_STATUS}
    identifier = digest(record)
    resources = FinalizedResources(root, record, identifier)
    resources.verify()
    path = snapshots.path(identifier)
    if not path.exists():
        save(path, record)
    elif snapshots.read(identifier, owner) != record:
        raise ValueError("Capture SHA xung đột")
    return {**snapshots.summary(identifier, record), "capture_version": LIVE_CAPTURE}
