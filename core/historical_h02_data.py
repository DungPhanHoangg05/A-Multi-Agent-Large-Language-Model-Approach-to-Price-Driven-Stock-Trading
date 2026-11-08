"""Snapshot/audit bổ sung H02; không sửa donor, không chứng nhận khả năng khớp lệnh."""

from __future__ import annotations

from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import requests

from core.execution_prices import RAW_FIELD_MAP, corporate_action_barriers, validate_raw_frame
from core.historical_asset_readiness import OUTPUT, PRICES, price_view

SYMBOLS = ("BHN", "CMG", "FPT", "HVN", "MBB", "MWG", "VCB", "VJC", "VNM")
DIRECTORY = OUTPUT / "h02_data_r1"


def digest(data: bytes) -> str:
    """Nhận diện nguyên byte snapshot hoặc HTTP response đã lưu."""
    return hashlib.sha256(data).hexdigest()


def write_new(path: Path, data: bytes) -> None:
    """Resume chỉ đọc lại nguyên byte; không tự sửa hoặc ghi đè evidence."""
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError("Evidence H02 khác byte đã lưu: " + path.name)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(data)


def json_bytes(value: Any) -> bytes:
    """Mã hóa JSON xác định, từ chối nonfinite."""
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()


def acquire_pages(directory: Path, symbol: str, kind: str) -> dict[str, Any]:
    """Giữ response REST gốc theo trang; resume không tải lại trang đã durable."""
    if symbol not in SYMBOLS or kind not in ("prices", "events"):
        raise ValueError("Symbol/nguồn H02 không hợp lệ")
    all_rows, pages, index, total = [], [], 0, None
    while total is None or index < total:
        path = directory / "responses" / f"{symbol}_{kind}_{index}.json.gz"
        meta = path.with_suffix(".meta.json")
        endpoint = (f"company/{symbol}/price-history?fromDate=20200101&toDate=20260930"
                    if kind == "prices" else f"events?ticker={symbol}&fromDate=20190101&toDate=20261231&eventCode=DIV%2CISS%2CAIS%2CMA%2CMOVE%2CNLIS%2COTHE%2CRETU%2CSUSP")
        url = f"https://iq.vietcap.com.vn/api/iq-insight-service/v1/{endpoint}&page={index}&size=1000"
        if path.exists() and meta.exists():
            raw = gzip.decompress(path.read_bytes())
            record = json.loads(meta.read_bytes())
            if record["url"] != url or record["response_sha256"] != digest(raw):
                raise ValueError("Response REST H02 khác receipt")
        elif path.exists() or meta.exists():
            raise ValueError("Trang REST H02 chưa có đủ response/receipt; không tải đè")
        else:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://trading.vietcap.com.vn/"}, timeout=30)
            response.raise_for_status()
            raw = response.content
            record = {"url": url, "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                      "response_sha256": digest(raw), "http_status": response.status_code}
            write_new(path, gzip.compress(raw, mtime=0))
            write_new(meta, json_bytes(record))
        payload = json.loads(raw)
        data = payload.get("data", payload)
        if not isinstance(data, dict) or not isinstance(data.get("content"), list):
            raise ValueError("REST H02 không có content/page contract")
        if data.get("number") != index or type(data.get("totalPages")) is not int:
            raise ValueError("Trang REST H02 không đúng chỉ số")
        if total is not None and total != data["totalPages"]:
            raise ValueError("Số trang REST đổi giữa lượt tải")
        total = data["totalPages"]
        pages.append(record)
        all_rows.extend(data["content"])
        if len(all_rows) > 10000 or total > 10:
            raise ValueError("REST H02 vượt phạm vi snapshot")
        index += 1
    if not all_rows:
        raise ValueError("REST H02 không có dữ liệu")
    return {"pages": pages, "records": all_rows}


def freeze_data(root: Path) -> dict[str, Any]:
    """Tải index và evidence chín mã, đối chiếu ngày/giá/quyền; không sửa dataset cũ."""
    directory = root / DIRECTORY
    manifest = directory / "manifest.json"
    if manifest.exists():
        result = json.loads(manifest.read_bytes())
        for name, expected in result["files"].items():
            if digest((directory / name).read_bytes()) != expected:
                raise ValueError("Snapshot H02 khác manifest: " + name)
        return result
    index_path = directory / "VNINDEX.csv"
    index_meta = directory / "VNINDEX.source.json"
    if not index_path.exists():
        from core.realtime_loader import _fetch_from_vnstock
        from scripts.prepare_historical_data import clean_ohlcv
        # Snapshot bổ sung độc lập, không tải đè prefix2018 đã khóa của model train.
        frame = clean_ohlcv(_fetch_from_vnstock("VNINDEX", "2025-01-01", "2026-09-30", "1D", "VCI"),
                            "VNINDEX", "2025-01-01", "2026-09-30")
        if str(frame["Datetime"].iloc[-1].date()) != "2026-09-30":
            raise ValueError("VNINDEX chưa đủ cutoff cuối")
        write_new(index_path, frame.to_csv(index=False, date_format="%Y-%m-%d", float_format="%.8f", lineterminator="\n").encode())
        write_new(index_meta, json_bytes({"source": "vnstock/VCI", "symbol": "VNINDEX", "price_unit": "index_points",
                  "requested_start": "2025-01-01", "requested_end": "2026-09-30", "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                  "historical_run_snapshot_authenticated": False}))
    if not index_meta.exists():
        raise ValueError("VNINDEX thiếu provenance")
    index_frame = pd.read_csv(index_path)
    old = pd.read_csv(root / "data/historical/VNINDEX.csv")
    index_overlap = old.merge(index_frame, on="Datetime", suffixes=("_old", "_new"), validate="one_to_one")
    index_differences = {column: int((~np.isclose(index_overlap[column+"_old"], index_overlap[column+"_new"], atol=1e-8, rtol=0)).sum())
                         for column in ("Open", "High", "Low", "Close", "Volume")}
    calendar = pd.DatetimeIndex(pd.to_datetime(index_frame["Datetime"]))
    grid = json.loads((root / OUTPUT / "manifests/candidate_grid.json").read_bytes())
    report = []
    for symbol in SYMBOLS:
        try:
            prices = acquire_pages(directory, symbol, "prices")
            events = acquire_pages(directory, symbol, "events")
            frame = pd.DataFrame(prices["records"])
            if not frame["ticker"].eq(symbol).all():
                raise ValueError("REST lẫn mã")
            frame = frame[list(RAW_FIELD_MAP)].rename(columns=RAW_FIELD_MAP)
            frame["Datetime"] = pd.to_datetime(frame["Datetime"]).dt.normalize()
            frame = frame.sort_values("Datetime").reset_index(drop=True)
            for column in ("Open", "High", "Low", "Close", "Reference", "MatchPrice"):
                frame[column] = pd.to_numeric(frame[column], errors="raise") / 1000.
            frame["Volume"] = pd.to_numeric(frame["Volume"], errors="raise")
            validate_raw_frame(frame)
            write_new(directory / f"{symbol}.raw.csv", frame.to_csv(index=False, date_format="%Y-%m-%d", lineterminator="\n").encode())
            write_new(directory / f"{symbol}.events.json", json_bytes(events))
            vendor, _ = price_view((root / OUTPUT / "inputs/fix" / PRICES / f"{symbol}.csv").read_bytes())
            vendor["Datetime"] = pd.to_datetime(vendor.pop("date"))
            merged = vendor.merge(frame, on="Datetime", suffixes=("_vendor", "_raw"), validate="one_to_one")
            unit_grid = [g for g in grid if g["symbol"] == symbol]
            rights = pd.DatetimeIndex(pd.to_datetime([e["exrightDate"] for e in events["records"] if e.get("exrightDate")])).normalize()
            entries = pd.to_datetime([g["entry_date"] for g in unit_grid])
            exits = pd.to_datetime([g["exit_date"] for g in unit_grid])
            spans = (rights.to_numpy()[None, :] > entries.to_numpy()[:, None]) & (rights.to_numpy()[None, :] <= exits.to_numpy()[:, None])
            report.append({"symbol": symbol, "status": "AUDITED_VENDOR_SERIES_LIMITED", "raw_rows": len(frame),
                "overlap_rows": len(merged), "open_differences": int((~np.isclose(merged["Open_vendor"], merged["Open_raw"], atol=1e-8, rtol=0)).sum()),
                "close_differences": int((~np.isclose(merged["Close_vendor"], merged["Close_raw"], atol=1e-8, rtol=0)).sum()),
                "vendor_dates_not_in_index": vendor.loc[~vendor["Datetime"].isin(calendar), "Datetime"].dt.strftime("%Y-%m-%d").tolist(),
                "cycles_with_exright_inside_holding": int(spans.any(axis=1).sum()), "event_records": len(events["records"]),
                "fill_certified": False, "raw_price_unit": "thousand_VND"})
        except (requests.RequestException, ValueError, KeyError) as error:
            report.append({"symbol": symbol, "status": "BLOCKED_DATA", "reason": str(error), "fill_certified": False})
    missing = sorted({g[k] for g in grid for k in ("date", "entry_date", "exit_date")} - set(index_frame["Datetime"]))
    result = {"version": "historical_h02_data_r1", "status": "AUDIT_COMPLETE_WITH_LIMITATIONS", "index_rows": len(index_frame),
              "index_first": str(index_frame["Datetime"].iloc[0]), "index_last": str(index_frame["Datetime"].iloc[-1]),
              "index_overlap_rows": len(index_overlap), "index_overlap_differences": index_differences,
              "index_missing_old_dates_in_overlap": sorted({d for d in old["Datetime"] if d >= index_frame["Datetime"].iloc[0]} - set(index_frame["Datetime"])),
              "grid_dates_missing_in_index": missing, "symbols": report, "economic_acceptance": "PENDING_EXECUTION_DATA",
              "dataset_replaced": False, "files": {p.relative_to(directory).as_posix(): digest(p.read_bytes()) for p in sorted(directory.rglob("*")) if p.is_file()}}
    write_new(manifest, json_bytes(result))
    return result


def complete_audit(root: Path) -> dict[str, Any]:
    """Đối soát supplement trên lịch đầy đủ; giữ manifest acquisition ban đầu nguyên byte."""
    acquisition = freeze_data(root)
    directory = root / DIRECTORY
    old = pd.read_csv(root / "data/historical/VNINDEX.csv")
    new = pd.read_csv(directory / "VNINDEX.csv")
    if any(acquisition["index_overlap_differences"].values()) or acquisition["index_missing_old_dates_in_overlap"]:
        raise ValueError("Không hợp nhất VNINDEX khi overlap khác hoặc thiếu phiên")
    if acquisition["index_overlap_rows"] != len(old.loc[old["Datetime"] >= new["Datetime"].iloc[0]]):
        raise ValueError("Overlap VNINDEX không bao phủ phần giao")
    full = pd.concat([old, new.loc[new["Datetime"] > old["Datetime"].iloc[-1]]], ignore_index=True)
    if full["Datetime"].duplicated().any() or not full["Datetime"].is_monotonic_increasing:
        raise ValueError("Lịch hợp nhất VNINDEX không tăng nghiêm ngặt")
    calendar = pd.DatetimeIndex(pd.to_datetime(full["Datetime"]))
    csv_path = directory / "VNINDEX_2018_2026_verified_overlap.csv"
    write_new(csv_path, full.to_csv(index=False, float_format="%.8f", lineterminator="\n").encode())
    grid = json.loads((root / OUTPUT / "manifests/candidate_grid.json").read_bytes())
    rows = []
    for symbol in SYMBOLS:
        prices, events = acquire_pages(directory, symbol, "prices"), acquire_pages(directory, symbol, "events")
        frame = pd.DataFrame(prices["records"])
        if not frame["ticker"].eq(symbol).all():
            raise ValueError("Raw audit lẫn mã")
        frame = frame[list(RAW_FIELD_MAP)].rename(columns=RAW_FIELD_MAP)
        frame["Datetime"] = pd.to_datetime(frame["Datetime"]).dt.strftime("%Y-%m-%d")
        frame = frame.sort_values("Datetime").reset_index(drop=True)
        for column in ("Open", "High", "Low", "Close", "Reference", "MatchPrice"):
            frame[column] = pd.to_numeric(frame[column], errors="raise") / 1000.
        frame["Volume"] = pd.to_numeric(frame["Volume"], errors="raise")
        write_new(directory / f"{symbol}.raw.csv", frame.to_csv(index=False, lineterminator="\n").encode())
        write_new(directory / f"{symbol}.events.json", json_bytes(events))
        # Áp dụng cùng policy suffix OHLC như donor cho BHN, không sửa nến lỗi.
        view, quality = price_view(frame.rename(columns={"Datetime": "date"}).to_csv(index=False).encode())
        view = view.rename(columns={"date": "Datetime"})
        view["Datetime"] = pd.to_datetime(view["Datetime"])
        validate_raw_frame(view)
        barriers = corporate_action_barriers(view, events["records"]).to_numpy()
        unit_grid = [g for g in grid if g["symbol"] == symbol]
        entry = pd.to_datetime([g["entry_date"] for g in unit_grid]).to_numpy()
        exit_date = pd.to_datetime([g["exit_date"] for g in unit_grid]).to_numpy()
        spans = (barriers[None, :] > entry[:, None]) & (barriers[None, :] <= exit_date[:, None])
        vendor, _ = price_view((root / OUTPUT / "inputs/fix" / PRICES / f"{symbol}.csv").read_bytes())
        vendor["Datetime"] = pd.to_datetime(vendor.pop("date"))
        merged = vendor.merge(view, on="Datetime", suffixes=("_vendor", "_raw"), validate="one_to_one")
        rows.append({"symbol":symbol,"raw_rows":len(frame),"analysis_rows":len(view),"excluded_prefix_rows":quality["excluded_prefix_rows"],
            "raw_price_unit":"thousand_VND","volume_unit":"matched_shares","overlap_rows":len(merged),
            "different_open":int((~np.isclose(merged["Open_vendor"],merged["Open_raw"],atol=1e-8,rtol=0)).sum()),
            "different_close":int((~np.isclose(merged["Close_vendor"],merged["Close_raw"],atol=1e-8,rtol=0)).sum()),
            "events":len(events["records"]),"cycles_with_corporate_barrier":int(spans.any(axis=1).sum()),
            "dates_missing_in_index":view.loc[~view["Datetime"].isin(calendar),"Datetime"].dt.strftime("%Y-%m-%d").tolist(),
            "fill_certified":False,"status":"VENDOR_SERIES_LIMITED"})
    missing = sorted({g[k] for g in grid for k in ("date","entry_date","exit_date")} - set(full["Datetime"]))
    result = {"version":"historical_h02_execution_audit_r1","index_rows":len(full),"index_first":str(full["Datetime"].iloc[0]),
              "index_last":str(full["Datetime"].iloc[-1]),"verified_overlap_rows":acquisition["index_overlap_rows"],
              "index_old_sha256":digest((root/"data/historical/VNINDEX.csv").read_bytes()),
              "index_supplement_sha256":digest((directory/"VNINDEX.csv").read_bytes()),"index_extended_sha256":digest(csv_path.read_bytes()),
              "acquisition_manifest_sha256":digest((directory/"manifest.json").read_bytes()),"grid_dates_missing":missing,
              "index_ready":not missing,"symbols":rows,"economic_acceptance":"PENDING_EXECUTION_DATA",
              "canonical_inputs_modified":False,"old_acquisition_missing_date_scope":"SUPPLEMENT_2025_2026_ONLY_SEE_THIS_FULL_CALENDAR_AUDIT",
              "files":{p.name:digest(p.read_bytes()) for p in sorted(directory.glob("*")) if p.is_file() and p.name not in ("execution_audit.json",)}}
    write_new(directory/"execution_audit.json",json_bytes(result))
    return result
