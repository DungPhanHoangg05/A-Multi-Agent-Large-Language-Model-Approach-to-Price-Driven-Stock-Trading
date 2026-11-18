"""Preflight FIN08 và nguồn thực thi chỉ được mở sau forecast barrier."""
from __future__ import annotations

from functools import cached_property
from pathlib import Path
from typing import Any

import pandas as pd

from core.finalize_bank_resources import ASSETS, RECIPE
from core.finalize_bank_signals import check_bindings
from core.finalize_price_acceptance import ACCEPTANCE
from core.finalize_price_audit import visible_event_dates
from core.finalize_serving_profile import LIVE_CAPTURE, RECEIPT, RECEIPT_SHA256, SCIENTIFIC_STATUS, UNAVAILABLE_OUTCOME, VERSION
from core.serving_runtime.resources import END, MAX_POINTS, START
from core.unified_contracts import checksum, digest
from core.unified_protocol import binding, read


class FinalizedResources:
    """Kiểm receipt FIN07 và toàn bộ các pin nguồn kế thừa trước vision."""
    def __init__(self, root: Path, live: dict | None = None, snapshot_id: str | None = None) -> None:
        self.root, self.live, self.snapshot_id = root, live, snapshot_id
        self.version = VERSION + ("/" + LIVE_CAPTURE if live is not None else "/asof")
        self.acceptance = read(root, ACCEPTANCE, True)
        self.receipt = read(root, RECEIPT, True)
        self.numeric = read(root, ASSETS + "manifest.json", True)
        if (binding(root, RECEIPT)["sha256"] != RECEIPT_SHA256 or self.receipt["status"] != "PASS_OFFLINE_FIN07"
                or self.acceptance["result"] != "PASS_OWNER_ATTESTED"):
            raise ValueError("Thiếu receipt FIN07 hoặc nguồn FIN04 đã khóa")
        numeric_recipe = read(root, RECIPE, True)
        pins = [*self.receipt["sources"], *self.acceptance["source_bindings"].values(), *numeric_recipe["source_bindings"],
                self.numeric["recipe"], *self.numeric["asset_bindings"]]
        from core.finalize_deterministic_bank import OUTPUT, RECIPE as KEY_RECIPE
        report = read(root, OUTPUT + "manifest.json", True)
        pins += [report["recipe"], *report["assets"], *read(root, KEY_RECIPE, True)["source_bindings"]]
        self.pins = {}
        for pin in pins:
            path = pin["path"]
            if path in self.pins and self.pins[path] != pin:
                raise ValueError("Nguồn FIN08 có hai pin khác nhau")
            self.pins[path] = pin
        self.sources = {item["symbol"]: item for item in self.acceptance["query_sources"]}
        self.calendar = pd.read_csv(root/self.acceptance["calendar"], parse_dates=["Datetime"])
        if live is not None:
            self._validate_live()

    def verify(self) -> None:
        """Dừng trước transport khi bất kỳ nguồn/receipt đã bind đổi byte."""
        if binding(self.root, RECEIPT)["sha256"] != RECEIPT_SHA256:
            raise ValueError("Receipt FIN07 khác hash")
        check_bindings(self.root, list(self.pins.values()))

    def stock(self, symbol: str) -> pd.DataFrame:
        """Nguồn as-of đầy đủ đúng origin, chỉ caller outcome được đọc giá sau cutoff."""
        item = self.sources[symbol]
        raw = pd.read_csv(self.root/item["raw_csv"], parse_dates=["Datetime"])
        return raw.loc[raw.Datetime >= item["origin"]].reset_index(drop=True)

    @cached_property
    def live_frame(self) -> pd.DataFrame:
        """Dữ liệu raw từ snapshot theo owner; dùng đúng origin và đơn vị FIN04."""
        if self.live is None:
            raise ValueError("Thiếu capture live")
        value = pd.DataFrame(self.live["prices"])
        value["Datetime"] = pd.to_datetime(value.Datetime)
        return value

    @cached_property
    def live_market(self) -> pd.DataFrame:
        """Lịch quan sát thực tại capture, chưa có nến kế hoạch t+1/t+3."""
        from core.realtime_index import index_frame
        return index_frame(self.live["index"])

    def _validate_live(self) -> None:
        """Chấp nhận raw capture cùng origin/giá/lịch overlap; legacy vendor bị chặn."""
        from datetime import datetime
        import numpy as np
        from core.execution_prices import validate_raw_frame
        from core.serving_live.snapshots import ZONE
        live = self.live
        if (live["version"] != LIVE_CAPTURE or digest(live) != self.snapshot_id or live["symbol"] not in self.sources
                or live["source"] != "VCI_RAW_EXECUTION_FIELDS" or live["price_unit"] != "thousand_VND"
                or "chart_timeframe" in live or any(not live["source_receipts"][kind] or
                    any(not checksum(page["response_sha256"]) for page in live["source_receipts"][kind])
                    for kind in ("prices", "events"))):
            raise ValueError("Capture live chưa có dữ liệu thô và receipt phiên")
        captured = datetime.fromisoformat(live["captured_at"])
        if captured.tzinfo is None:
            raise ValueError("Capture thiếu múi giờ")
        local = captured.astimezone(ZONE)
        closed = pd.Timestamp(local.date()) - pd.Timedelta(days=int((local.hour, local.minute) < (15, 30)))
        cutoff = pd.Timestamp(live["cutoff"])
        stock, market = self.live_frame, self.live_market
        validate_raw_frame(stock)
        if (cutoff > closed or (pd.Timestamp(local.date())-cutoff).days > 10 or live["cutoff"] < START
                or stock.Datetime.iloc[-1] != cutoff or market.Datetime.iloc[-1] != cutoff
                or len(stock) < 600 or not pd.DatetimeIndex(stock.Datetime).isin(market.Datetime).all()
                or not np.isfinite(stock.Reference).all() or (stock.Reference <= 0).any()):
            raise ValueError("Live thiếu phiên hoàn tất/tham chiếu hoặc phủ khác cutoff")

        def overlap(capture: pd.DataFrame, pinned: pd.DataFrame, columns: list[str]) -> bool:
            end = min(cutoff, pinned.Datetime.iloc[-1])
            actual = capture.loc[capture.Datetime <= end, columns].reset_index(drop=True)
            expected = pinned.loc[pinned.Datetime <= end, columns].reset_index(drop=True)
            return len(actual) == len(expected) and bool(actual.eq(expected).all(axis=None))

        accepted = self.stock(live["symbol"])
        if (not overlap(stock, accepted, ["Datetime", "Open", "High", "Low", "Close", "Volume", "Reference"])
                or not overlap(market, self.calendar, ["Datetime", "Close"])):
            raise ValueError("Live đổi origin, lịch hoặc giá overlap đã khóa")

    def document(self) -> dict:
        """Identity gồm receipt FIN07, dữ liệu thô, runtime scope và capture owner."""
        sessions = self.calendar.Datetime.dt.strftime("%Y-%m-%d").tolist()
        bindings = {k: {"sha256": pin["sha256"], "bytes": pin["bytes"]} for k, pin in self.pins.items()}
        support = {"symbols": sorted(self.sources), "start_date": START, "end_date": END,
                   "calendar": [value for value in sessions if START <= value <= END], "max_points": MAX_POINTS,
                   "timeframes": ["1d"], "languages": ["vi", "en"], "generation_languages": ["vi"],
                   "profile_version": VERSION, "context_receipt_sha256": RECEIPT_SHA256,
                   "scientific_status": SCIENTIFIC_STATUS, "independent_price_pit_certified": False}
        if self.live is not None:
            live = self.live
            bindings["live_snapshot/" + self.snapshot_id] = {"sha256": self.snapshot_id}
            support.update(symbols=[live["symbol"]], start_date=live["cutoff"], end_date=live["cutoff"],
                           calendar=live["index"]["Datetime"], snapshot_id=self.snapshot_id,
                           calendar_policy=live["calendar_policy"], source=live["source"])
        resources = {role: {"version": VERSION + "/" + role,
                     "sha256": digest({"role": role, "bindings": bindings})}
                     for role in ("prices", "news", "calendar", "bank", "regime", "scaler", "context", "student", "teacher", "facts")}
        return {"version": self.version, "support": support, "resources": resources, "bindings": bindings}

    def points(self, request: dict) -> list[dict]:
        """Chọn lịch đã khóa rồi kiểm từng prefix, khóa T/P và feature trước transport."""
        from core.finalize_ohlcv_keys import key_at
        from core.execution_prices import raw_point_in_time_snapshot
        from core.serving_runtime.resources import Resources
        if request["version"] != VERSION:
            raise ValueError("Lỗi phiên bản finalized")
        support = self.document()["support"]
        if self.live is None:
            points = Resources.points(self, request)
            for point in points:
                point.update(fold="f2026_q3", quality="FINALIZE_RAW_OWNER_ATTESTED")
        else:
            live = self.live
            if (request.get("snapshot_id") != self.snapshot_id or request["symbols"] != [live["symbol"]]
                    or request["start_date"] != live["cutoff"] or request["end_date"] != live["cutoff"]
                    or request["mode"] not in ("analyze", "compare") or "chart_timeframe" in request):
                raise ValueError("Form live khác capture daily")
            points = [{"id": live["symbol"]+"-"+live["cutoff"], "symbol": live["symbol"], "cutoff": live["cutoff"],
                       "fold": "finalize_live_daily", "quality": "FINALIZE_LIVE_RAW_TRANSFER"}]
        frames = {s: self.stock(s) for s in request["symbols"]} if self.live is None else {self.live["symbol"]: self.live_frame}
        calendar = pd.DatetimeIndex((self.calendar if self.live is None else self.live_market).Datetime)
        for point in points:
            symbol, cutoff = point["symbol"], point["cutoff"]
            prefix = raw_point_in_time_snapshot(frames[symbol], cutoff)
            if (symbol not in support["symbols"] or len(prefix) < 600
                    or key_at(prefix, calendar, cutoff)["reason"] is not None):
                raise ValueError("Prefix FIN08 thiếu 600 nến hoặc lịch 45 phiên")
        return points

    def outcome(self, point: dict, frame: pd.DataFrame | None = None) -> dict:
        """Sau barrier, dùng đúng lịch VNINDEX và giá thực thi. Giữ NA có lý do."""
        from core.execution_prices import corporate_action_barriers, validate_raw_frame
        from core.unified_experiment import outcome_from_frame
        if self.live is not None:
            raise ValueError("Capture live không có label t+3")
        symbol, cutoff = point["symbol"], point["cutoff"]
        source = self.sources[symbol]
        identity = self.pins[source["raw_csv"]]["sha256"]
        calendar = pd.DatetimeIndex(self.calendar.Datetime)
        index = calendar.get_loc(pd.Timestamp(cutoff))
        dates = calendar[index:index+4]

        def unavailable(reason: str) -> dict:
            return self.unavailable(point, reason)

        if len(dates) != 4:
            return unavailable("PENDING_EXIT")
        raw = self.stock(symbol) if frame is None else frame
        past = raw.loc[raw.Datetime <= dates[-1]].copy()
        validate_raw_frame(past)
        prices = past.set_index("Datetime")
        if not dates.isin(prices.index).all():
            return unavailable("MISSING_EXECUTION_SESSION")
        cycle = prices.loc[dates].reset_index()
        if (cycle.iloc[1:].Volume <= 0).any():
            return unavailable("NO_MATCHED_VOLUME_AT_EXECUTION")
        days, _ = visible_event_dates(read(self.root, source["event_ledger"])["records"], str(dates[-1].date()))
        barriers = corporate_action_barriers(past, [{"exrightDate": day} for day in days])
        if ((barriers > dates[1]) & (barriers <= dates[-1])).any():
            return unavailable("CORPORATE_ACTION_DURING_HOLDING")
        cycle[["Open", "High", "Low", "Close"]] *= 1000.
        return outcome_from_frame(point, cycle, identity)

    def unavailable(self, point: dict, reason: str) -> dict:
        """Ghi coverage NA riêng, không dùng ròng bằng 0 làm nhãn hoặc payoff giả."""
        source = self.sources[point["symbol"]]["raw_csv"]
        return {"version": UNAVAILABLE_OUTCOME, "point_id": point["id"], "source_sha256": self.pins[source]["sha256"],
                "reason": reason}
