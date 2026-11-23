"""Đối soát nguồn giá finalize offline; integrity không thay chứng minh PIT lịch sử."""
from __future__ import annotations

import gzip
import hashlib
import io
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from core.backtest_engine import compute_round_trip_net_return
from core.execution_prices import (
    PRICE_COLUMNS, RAW_FIELD_MAP, corporate_action_barriers, load_verified_execution_data,
    raw_point_in_time_snapshot, validate_raw_frame,
)
from core.unified_contracts import day, digest
from core.unified_protocol import binding, read, safe

DIRECTORY = "docs/plan/week12/"
H02 = "outputs/historical_reevaluation/h02_data_r1/"
COMPAT = "outputs/unified_integration/u06_assets_v2/compatibility/execution_prices/"
ASSETS = "outputs/unified_integration/u06_assets_v2/prices/"
SYMBOLS = ("BHN", "CMG", "FPT", "HVN", "MBB", "MWG", "VCB", "VJC", "VNM")
ZONE = "Asia/Ho_Chi_Minh"


def raw_prices(records: list[dict[str, Any]], symbol: str) -> pd.DataFrame:
    """Chọn trường thô có ticker đúng; đổi VND thành nghìn VND một lần, không chọn cột Adjusted."""
    frame = pd.DataFrame(records)
    if symbol not in SYMBOLS or not set(RAW_FIELD_MAP).union({"ticker"}).issubset(frame.columns):
        raise ValueError("Nguồn REST thiếu mã hoặc trường giá thô")
    if not frame.ticker.eq(symbol).all():
        raise ValueError("Response giá lẫn mã cổ phiếu")
    result = frame.loc[:, list(RAW_FIELD_MAP)].rename(columns=RAW_FIELD_MAP).copy()
    result["Datetime"] = pd.to_datetime(result.Datetime, errors="raise")
    dates = pd.DatetimeIndex(result.Datetime)
    if dates.tz is not None or dates.hasnans or dates.has_duplicates or not dates.equals(dates.normalize()):
        raise ValueError("Ngày nguồn REST trùng hoặc không phải ngày phiên")
    for name in ("Open", "High", "Low", "Close", "Reference", "MatchPrice"):
        result[name] = pd.to_numeric(result[name], errors="raise") / 1000.
    result["Volume"] = pd.to_numeric(result.Volume, errors="raise")
    # Giữ cả prefix OHLC lỗi để audit; chỉ validator của prefix đã khóa mới cho phép sử dụng.
    return result.sort_values("Datetime").reset_index(drop=True)


def validate_prefix_availability(frame: pd.DataFrame, cutoff: str, available_at: dict[str, str], *,
                                 session_close_at: dict[str, str]) -> pd.DataFrame:
    """Kiểm rào thời gian với metadata đã xác thực ở caller; không tự tạo availability từ ngày nến."""
    prefix = raw_point_in_time_snapshot(frame, day(cutoff))
    dates = prefix.Datetime.dt.strftime("%Y-%m-%d").tolist()
    if any(name not in available_at or name not in session_close_at for name in dates):
        raise ValueError("Thiếu availability giá hoặc thời điểm hoàn tất phiên đã xác minh")
    for mapping in (available_at, session_close_at):
        if any(type(mapping[name]) is not str or pd.Timestamp(mapping[name]).tzinfo is None for name in dates):
            raise ValueError("Availability và thời điểm hoàn tất phiên phải có múi giờ tường minh")
    stamps = pd.DatetimeIndex(pd.to_datetime([available_at[name] for name in dates], utc=True, errors="raise"))
    close_times = pd.DatetimeIndex(pd.to_datetime([session_close_at[name] for name in dates], utc=True, errors="raise"))
    query = pd.Timestamp(cutoff, tz=ZONE) + pd.Timedelta(hours=15, minutes=30)
    close_dates = close_times.tz_convert(ZONE).tz_localize(None).normalize()
    if (stamps.hasnans or close_times.hasnans or not close_dates.equals(pd.DatetimeIndex(prefix.Datetime))
            or (stamps < close_times).any() or (stamps > query).any()):
        raise ValueError("Availability giá sớm hơn phiên hoàn tất hoặc vượt cutoff")
    # Dtype của phần tương lai không được làm đổi identity của prefix đã nhìn thấy.
    return prefix.astype({name:float for name in PRICE_COLUMNS[1:]})


def session_cycle(frame: pd.DataFrame, calendar: pd.DatetimeIndex, cutoff: str) -> dict[str, str]:
    """Định vị t+1/t+3 theo lịch phiên; không đọc giá entry/exit hay sinh outcome query."""
    if calendar.tz is not None or calendar.hasnans or calendar.has_duplicates or not calendar.is_monotonic_increasing:
        raise ValueError("Lịch phiên không hợp lệ")
    if not calendar.equals(calendar.normalize()):
        raise ValueError("Lịch phải chứa ngày phiên")
    position = int(calendar.get_indexer([pd.Timestamp(day(cutoff))])[0])
    if position < 0 or position + 3 >= len(calendar):
        raise ValueError("Thiếu phiên query hoặc horizon t+3")
    dates = pd.DatetimeIndex(pd.to_datetime(frame.Datetime, errors="raise"))
    required = calendar[position:position + 4]
    if dates.has_duplicates or not dates.is_monotonic_increasing or not required.isin(dates).all():
        raise ValueError("Cổ phiếu thiếu một phiên trong chu kỳ của lịch thị trường")
    return {"entry_date": str(required[1].date()), "exit_date": str(required[3].date())}


def visible_event_dates(events: list[dict[str, Any]], cutoff: str) -> tuple[list[str], list[dict[str, str]]]:
    """Date-only khả dụng ngày kế; ghi lý do loại rõ ràng, không dùng ngày quyền làm ngày công bố."""
    query = pd.Timestamp(day(cutoff))
    visible, excluded = [], []
    for event in events:
        if not event.get("exrightDate"):
            continue
        published = event.get("publicDate")
        if not published:
            excluded.append({"id": str(event.get("id", "")), "reason": "UNDATED_PUBLICATION"})
            continue
        available = pd.Timestamp(published).normalize() + pd.Timedelta(days=1)
        if pd.isna(available) or available.tzinfo is not None:
            raise ValueError("Ngày công bố sự kiện không hợp lệ")
        exright = day(str(event["exrightDate"])[:10])
        if available > query:
            excluded.append({"id": str(event.get("id", "")), "reason": "PUBLICATION_AFTER_CUTOFF"})
        else:
            visible.append(exright)
    return sorted(set(visible)), excluded


class Sources:
    """Chỉ đọc các input đã pin U06; không gọi acquisition có khả năng truy cập mạng."""
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.contract = read(root, DIRECTORY + "finalize_comparison_contract.json", True)
        pin = self.contract["sources_and_availability"]["candidate_assets"]
        if binding(root, pin["path"]) != pin:
            raise ValueError("Manifest nguồn khác contract FIN02")
        self.manifest = read(root, pin["path"], True)
        self.expected = {**self.manifest["source_bindings"], **self.manifest["asset_bindings"]}
        self.bindings: dict[str, dict[str, Any]] = {pin["path"]: pin}

    def raw(self, name: str) -> bytes:
        """Băm trước parse; không chấp nhận đường dẫn ngoài tập bằng chứng được khóa."""
        if name not in self.expected or binding(self.root, name) != self.expected[name]:
            raise ValueError("Input giá khác pin U06 hoặc chưa có nguồn: " + name)
        self.bindings[name] = self.expected[name]
        return safe(self.root, name).read_bytes()

    def document(self, name: str) -> Any:
        """JSON từ byte đã kiểm, không tin cờ PASS tự khai của file ngoài manifest."""
        return json.loads(self.raw(name))

    def pages(self, symbol: str, kind: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Khôi phục response đã lưu đủ trang; kiểm SHA response, URL, ticker và phân trang."""
        if symbol not in SYMBOLS or kind not in ("prices", "events"):
            raise ValueError("Nguồn REST ngoài phạm vi")
        rows, receipts = [], []
        page, total, count, page_size = 0, None, None, None
        while total is None or page < total:
            name = H02 + f"responses/{symbol}_{kind}_{page}.json.gz"
            raw = gzip.decompress(self.raw(name))
            meta = self.document(name.removesuffix(".gz") + ".meta.json")
            endpoint = (f"company/{symbol}/price-history?fromDate=20200101&toDate=20260930" if kind == "prices" else
                f"events?ticker={symbol}&fromDate=20190101&toDate=20261231&eventCode=DIV%2CISS%2CAIS%2CMA%2CMOVE%2CNLIS%2COTHE%2CRETU%2CSUSP")
            url = "https://iq.vietcap.com.vn/api/iq-insight-service/v1/" + endpoint + f"&page={page}&size=1000"
            if meta["response_sha256"] != hashlib.sha256(raw).hexdigest() or meta["url"] != url or meta["http_status"] != 200:
                raise ValueError("Receipt REST không khớp response hoặc URL")
            payload = json.loads(raw)
            data = payload["data"]
            if payload.get("successful") is not True or payload.get("code") != 0:
                raise ValueError("Response REST không thành công")
            if total is None:
                total, count = data["totalPages"], data["totalElements"]
                page_size = data["size"]
            if (type(total) is not int or not 1 <= total <= 10 or type(count) is not int or count < 1
                    or data["number"] != page or data["totalPages"] != total or data["totalElements"] != count
                    or type(page_size) is not int or page_size < 1 or data["size"] != page_size
                    or total != (count + page_size - 1) // page_size
                    or len(data["content"]) != min(data["size"], count - len(rows))
                    or data["last"] is not (page == total - 1)):
                raise ValueError("Nguồn REST thiếu trang hoặc metadata phân trang sai")
            rows.extend(data["content"])
            receipts.append(meta)
            page += 1
        if len(rows) != count:
            raise ValueError("Nguồn REST không đủ số bản ghi")
        if any(row.get("ticker", row.get("organCode")) != symbol for row in rows):
            raise ValueError("Response REST lẫn mã cổ phiếu")
        return rows, receipts


def audit_prices(root: Path) -> dict[str, Any]:
    """Đối soát quote/calendar/events và nhãn bank; không sinh nhãn/query return hoặc thay dataset."""
    source = Sources(root)
    calendar = pd.DatetimeIndex(pd.to_datetime(pd.read_csv(
        io.BytesIO(source.raw(H02 + "VNINDEX_2018_2026_verified_overlap.csv")))["Datetime"]))
    bank = source.document("data_manager/regime_memory_store.json")
    symbols, points, bank_rows = [], [], []
    point_list = source.contract["domain"]["primary_points"]
    if len(bank) != 852 or max(e["exit_date"] for e in bank) >= min(p["cutoff"] for p in point_list):
        raise ValueError("Bank không đủ 852 chu kỳ đã đáo hạn trước query đầu tiên")
    for symbol in SYMBOLS:
        records, receipts = source.pages(symbol, "prices")
        events, event_receipts = source.pages(symbol, "events")
        event_doc = source.document(H02 + symbol + ".events.json")
        if event_doc["records"] != events or event_doc["pages"] != event_receipts:
            raise ValueError("Ledger sự kiện không khớp các trang REST")
        raw = raw_prices(records, symbol)
        if not raw.Datetime.between("2020-01-01", "2026-09-30").all():
            raise ValueError("REST trả ngày ngoài phạm vi nguồn")
        cached = pd.read_csv(io.BytesIO(source.raw(H02 + symbol + ".raw.csv")), parse_dates=["Datetime"])
        if (not raw.Datetime.equals(cached.Datetime)
                or not np.allclose(raw.drop(columns="Datetime"), cached.drop(columns="Datetime"), rtol=0, atol=1e-8)):
            raise ValueError("CSV raw khác các trường thô REST")
        donor = pd.DataFrame(source.document(ASSETS + symbol + ".json"))
        donor["Datetime"] = pd.to_datetime(donor.Datetime)
        candidate = raw.loc[raw.Datetime >= donor.Datetime.iloc[0]].reset_index(drop=True)
        validate_raw_frame(candidate)
        if not candidate.Datetime.equals(donor.Datetime):
            raise ValueError("Lịch raw và query khác nhau, cần amendment trước dùng nguồn mới")
        if not candidate.Datetime.isin(calendar).all():
            raise ValueError("Cổ phiếu có ngày ngoài lịch VNINDEX")
        columns = ("Open", "High", "Low", "Close", "Volume")
        difference = ~np.isclose(candidate.loc[:, columns], donor.loc[:, columns], rtol=0, atol=1e-8)
        latest = max(r["retrieved_at_utc"] for r in receipts)
        symbols.append({"symbol":symbol,"raw_rows":len(raw),"locked_origin":str(candidate.Datetime.iloc[0].date()),
            "excluded_prefix_rows":len(raw)-len(candidate),"candidate_rows":len(candidate),"event_records":len(events),
            "donor_difference_counts":{name:int(difference[:,i].sum()) for i,name in enumerate(columns)},
            "raw_price_unit":"thousand_VND","raw_volume_unit":"matched_shares","raw_basis":"UNADJUSTED_EXECUTION_FIELDS",
            "retrieved_at_utc":latest,"authenticated_as_published_rows":0,
            "price_pit_gate":"NOT_CERTIFIED_NO_AS_PUBLISHED_RECEIPT","event_content_pit_gate":"NOT_CERTIFIED_VENDOR_PUBLIC_DATE_ONLY"})
        for point in [p for p in point_list if p["symbol"] == symbol]:
            cycle = session_cycle(candidate, calendar, point["cutoff"])
            prefix = raw_point_in_time_snapshot(candidate, point["cutoff"])
            known_dates, excluded = visible_event_dates(events, point["cutoff"])
            holding = [d for d in known_dates if cycle["entry_date"] < d <= cycle["exit_date"]]
            blockers = ["PRICE_AS_PUBLISHED_AVAILABILITY_UNVERIFIED","EXCHANGE_CALENDAR_PROVENANCE_UNVERIFIED",
                "EVENT_CONTENT_AVAILABILITY_UNVERIFIED","DONOR_RAW_SOURCE_CHANGE_REQUIRES_RESOURCE_REBUILD"]
            if holding:
                blockers.append("KNOWN_CORPORATE_ACTION_DURING_HOLDING")
            points.append({**point,**cycle,"prefix_rows":len(prefix),"known_event_dates_inside_holding":holding,
                "excluded_event_metadata":len(excluded),"admitted":False,
                "blockers":blockers})
        if symbol in ("FPT", "MWG", "VCB", "VNM"):
            meta = source.document(COMPAT + "manifest.json")
            for part in ("csv", "evidence", "events"):
                source.raw(COMPAT + meta["files"][symbol][part]["file"])
            bank_frame, bank_events = load_verified_execution_data(root / COMPAT, symbol)
            overlap = bank_frame.merge(candidate, on="Datetime", suffixes=("_bank", "_query"), validate="one_to_one")
            quote_diff = {name:int((~np.isclose(overlap[name+"_bank"],overlap[name+"_query"],atol=1e-8,rtol=0)).sum()) for name in columns}
            episodes = [e for e in bank if e["symbol"] == symbol]
            dates = pd.DatetimeIndex(bank_frame.Datetime)
            indices = {name:dates.get_indexer(pd.to_datetime([e[name] for e in episodes])) for name in ("as_of_date","entry_date","exit_date")}
            if any((v < 0).any() for v in indices.values()) or not (indices["entry_date"] == indices["as_of_date"]+1).all() or not (indices["exit_date"] == indices["as_of_date"]+3).all():
                raise ValueError("Nhãn bank không khớp lịch t+1/t+3")
            barriers = corporate_action_barriers(bank_frame, bank_events).to_numpy()
            entry_days,exit_days = dates.to_numpy()[indices["entry_date"]],dates.to_numpy()[indices["exit_date"]]
            rights = np.searchsorted(barriers,exit_days,side="right")-np.searchsorted(barriers,entry_days,side="right")
            volume = bank_frame.Volume.to_numpy()
            no_volume = (volume[indices["entry_date"]] <= 0) | (volume[indices["entry_date"]+1] <= 0) | (volume[indices["exit_date"]] <= 0)
            if rights.any() or no_volume.any():
                raise ValueError("Chu kỳ bank có quyền hoặc thiếu khối lượng, không được sinh nhãn thực thi")
            oracle = np.frompyfunc(compute_round_trip_net_return, 2, 1)
            returns = oracle(bank_frame.Open.to_numpy()[indices["entry_date"]],bank_frame.Close.to_numpy()[indices["exit_date"]]).astype(float)
            expected = np.asarray([e["outcome"]["net_return_pct"]/100 for e in episodes])
            bank_rows.append({"symbol":symbol,"episodes":len(episodes),"raw_overlap_rows":len(overlap),
                "corporate_barrier_cycles":int((rights>0).sum()),"unmatched_volume_cycles":int(no_volume.sum()),
                "bank_h02_quote_difference_counts":quote_diff,"oracle_mismatches_above_1e_10":int((np.abs(returns-expected)>1e-10).sum()),
                "max_abs_oracle_error_fraction":float(np.abs(returns-expected).max())})
    legacy = []
    meta = source.document("data/execution_prices/manifest.json")
    for symbol,item in meta["files"].items():
        for part in ("csv","evidence","events"):
            name = "data/execution_prices/"+item[part]["file"]
            raw = source.raw(name)
            if hashlib.sha256(raw).hexdigest() != item[part]["sha256"]:
                restored = safe(root,COMPAT+item[part]["file"]).read_bytes()
                legacy.append({"path":name,"expected_sha256":item[part]["sha256"],"actual":binding(root,name),
                    "restorable_from":COMPAT+item[part]["file"],"newline_only":raw==restored.replace(b"\r\n",b"\n")})
    return {"version":"finalize_price_audit_v1","status":"AUDIT_COMPLETE_SOURCE_GATE_BLOCKED",
        "price_source_gate":"BLOCKED_PIT_PROVENANCE","contract_sha256":digest(source.contract),
        "parents":[binding(root,DIRECTORY+"finalize_comparison_contract.json")],"source_bindings":source.bindings,
        "symbols":symbols,"points":sorted(points,key=lambda p:(p["cutoff"],p["symbol"])),"bank_oracle":bank_rows,
        "calendar":{"sessions":len(calendar),"first":str(calendar[0].date()),"last":str(calendar[-1].date()),
            "query_cycles_verified":len(points),"source":"OBSERVED_VNINDEX_VERIFIED_OVERLAP","independent_exchange_calendar":False},
        "legacy_manifest_deltas":legacy,"planned_points":len(points),"admitted_points":0,
        "dataset_replaced":False,"query_outcomes_computed":False,"api_calls":0,"training":False,
        "required_evidence":["Snapshot/receipt hoặc hồ sơ nguồn chứng minh phiên bản giá thô đã khả dụng tại cutoff.",
            "Nguồn lịch phiên và event ledger có provenance/availability trong miền đã khóa.",
            "Amendment nguồn/dataset và tái tạo tài nguyên trước query nếu chuyển donor sang raw; không ép parity bằng scale."]}


def require_price_gate(root: Path, report: dict[str, Any]) -> None:
    """Không nhận report tự ký lại thành PASS; đối soát với nguồn rồi giữ gate chặn khi thiếu chứng cứ."""
    if report != audit_prices(root) or report["price_source_gate"] != "PASS":
        raise ValueError("FIN04 chưa có nguồn giá/lịch/sự kiện đáp ứng PIT; không được mở bản cuối")
