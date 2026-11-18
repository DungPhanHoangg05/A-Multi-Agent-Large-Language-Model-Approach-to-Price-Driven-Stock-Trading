"""Phát hành bank FIN06 xác định và khóa cùng phép chiếu retrieval ở phía query."""
from __future__ import annotations

from collections import Counter
import hashlib
import io
from pathlib import Path
from typing import Any
from zipfile import ZipFile

import pandas as pd

from core.causal_alpha import frame_document, validated_frame
from core.execution_prices import load_verified_execution_data, raw_point_in_time_snapshot
from core.finalize_bank_resources import ASSETS, CONTRACT, RECIPE as NUMERIC_RECIPE, mature_cycles
from core.finalize_bank_signals import check_bindings
from core.finalize_ohlcv_keys import PATTERN, PROFILE, RULES, TREND, key_at
from core.finalize_price_acceptance import ACCEPTANCE, PROFILE as PRICE_PROFILE, require_accepted_prices
from core.unified_contracts import digest
from core.unified_protocol import CORE4, binding, read, safe

ARCHIVE = "docs/plan/week12/finalize_bank_signal_rebuild_v2.zip"
HISTORY = "docs/plan/week12/finalize_bank_collection_plan_v1.json"
RECIPE = "docs/plan/week12/finalize_ohlcv_bank_recipe_v1.json"
OUTPUT = "outputs/finalize/ohlcv_bank_v1/"
VERSION = "finalize_ohlcv_bank_v1"
LEGACY_ARCHIVE_SHA256 = "612bcb8b22d0627cb0f82adf64758d96b9e1123777154d9e1a4c74d75e9a61aa"


def make_recipe(root: Path) -> dict[str, Any]:
    """Khóa công thức và phụ thuộc trước khi tính khóa hoặc so với phản hồi thị giác."""
    sources = (CONTRACT, ACCEPTANCE, NUMERIC_RECIPE, ASSETS + "manifest.json", ARCHIVE, HISTORY,
               "core/finalize_ohlcv_keys.py", "core/finalize_deterministic_bank.py",
               "core/finalize_bank_signals.py", "core/execution_prices.py", "core/historical_signals.py",
               "scripts/prepare_finalize_ohlcv_bank.py", "scripts/verify_finalize_ohlcv_bank.py")
    pins = [binding(root, path) for path in sources]
    archive = next(pin for pin in pins if pin["path"] == ARCHIVE)
    history = read(root, HISTORY, True)
    if archive["sha256"] != LEGACY_ARCHIVE_SHA256 or history["source_archive"] != archive:
        raise ValueError("Gói Alpha/regime/tin lịch sử khác checkpoint đã khóa")
    return {"version": VERSION, "FIN02_amendment": "DETERMINISTIC_BANK_AND_QUERY_RETRIEVAL_KEYS",
            "keys": RULES, "source_bindings": pins, "variants": ["bayesian_v1", "C2", "A_tp_pool", "B_semantic"],
            "shared_key_entrypoint": "core.finalize_ohlcv_keys.key_at",
            "statistics_scope": "SAME_SYMBOL_REGIME_STRICT_EXIT_AND_T_P_AVAILABLE",
            "example_scope": "STATISTICS_POPULATION_WITH_FINITE_T_P_A_I; K_LE_3",
            "sentiment": "FIN05_NULL_EXCLUDED_FROM_TECHNICAL_MATCH",
            "economic_scope": "PIN_NUMERIC_BANK_NO_NEW_LABEL; QUERY_OUTCOMES_CLOSED",
            "upstream_scope": "KEYS_FOR_RETRIEVAL_ONLY; VISION_REPORTS_STILL_FLOW_TO_DECISION",
            "mt_bicl_scope": "SEPARATE_NUMERIC_CONTEXT_CONTRACT", "bank_new_vision_http": 0}


def checkpoint_rows(archive: Path) -> dict[str, dict]:
    """Chỉ nhận provenance đã lưu của Indicator, Alpha, regime và tin."""
    import json

    def payload(raw: bytes) -> dict:
        value = json.loads(raw)
        if set(value) != {"payload", "sha256"} or digest(value["payload"]) != value["sha256"]:
            raise ValueError("Checkpoint lịch sử khác checksum")
        return value

    result = {}
    with ZipFile(archive) as bundle:
        report = payload(bundle.read("report.json"))["payload"]
        model_hashes: dict[str, str] = {}
        for pointer in report["points"]:
            name = pointer["id"]
            record = payload(bundle.read(f"points/{name}.json"))
            row = record["payload"]
            cutoff = row["cutoff"]
            regime = row["regime"]
            if cutoff not in model_hashes:
                model_hashes[cutoff] = hashlib.sha256(bundle.read(f"regimes/VNINDEX-{cutoff}.json")).hexdigest()
            if (record["sha256"] != pointer["sha256"] or name in result or
                    model_hashes[cutoff] != regime["artifact_sha256"] or regime["metadata"]["train_end_date"] != cutoff or
                    regime["state"]["feature_end_date"] > cutoff or regime["state"]["as_of_date"] != cutoff):
                raise ValueError("Checkpoint hoặc model regime khác artifact đã pin")
            if row["alpha"]["value"] is not None and not row["alpha"]["fit_end"] < cutoff:
                raise ValueError("Alpha bank dùng model chưa khóa tại cutoff")
            if row["sentiment"]["available"] or row["sentiment"]["value"] is not None:
                raise ValueError("Nguồn tin khác policy NA của FIN05")
            result[name] = row
    return result


def economic_trace(numeric: dict) -> dict:
    """Sao chép đúng nhãn nguồn FIN06 số để không đọc giá entry/exit trong T/P."""
    fields = ("episode_id", "symbol", "as_of_date", "entry_date", "exit_date", "r_net", "y", "price_manifest",
              "legacy_row_sha256")
    return {key: numeric[key] for key in fields}


def build(root: Path, recipe: dict) -> tuple[dict, dict]:
    """Tái dựng mọi khóa bank và query từ giá thô, giữ nhãn và tài nguyên fit đã có."""
    if recipe != make_recipe(root):
        raise ValueError("Recipe bank xác định khác byte nguồn đã khóa")
    accepted = require_accepted_prices(root, profile=PRICE_PROFILE)
    numeric_manifest = read(root, ASSETS + "manifest.json", True)
    check_bindings(root, [numeric_manifest["recipe"], *numeric_manifest["asset_bindings"]])
    market = pd.read_csv(safe(root, accepted["calendar"]), parse_dates=["Datetime"])
    calendar = pd.DatetimeIndex(market.Datetime)
    if calendar.has_duplicates or not calendar.is_monotonic_increasing:
        raise ValueError("Lịch phiên bank xác định không hợp lệ")
    numeric = read(root, ASSETS + "bank.json")["records"]
    reserved = set(read(root, NUMERIC_RECIPE, True)["reserved_ids"])
    mature_cycles(numeric, reserved, "2022-12-31")
    index = read(root, ASSETS + "prior_index.json", True)
    membership = {row["episode_id"]: (row["symbol"], row["as_of_date"], row["exit_date"]) for row in numeric}
    if len(membership) != 852 or membership != {
            r["episode_id"]: (r["symbol"], r["as_of_date"], r["exit_date"]) for r in index["records"]}:
        raise ValueError("Membership bank không khớp index giá đã pin")
    points = checkpoint_rows(root / ARCHIVE)
    if set(points) != {key.replace(":", "-") for key in membership}:
        raise ValueError("Checkpoint lịch sử khác tập 852 ID")
    prices = {symbol: load_verified_execution_data(root / accepted["bank_source"], symbol)[0] for symbol in CORE4}
    rows = []
    for row in numeric:
        symbol, cutoff = row["symbol"], row["as_of_date"]
        checkpoint = points[row["episode_id"].replace(":", "-")]
        prefix = raw_point_in_time_snapshot(prices[symbol], cutoff)
        key = key_at(prefix, calendar, cutoff)
        if (checkpoint["episode_id"] != row["episode_id"] or checkpoint["symbol"] != symbol or checkpoint["cutoff"] != cutoff or
                checkpoint["parent"]["prefix_sha256"] != digest(frame_document(validated_frame(prefix))) or
                checkpoint["parent"]["window_sha256"] != key["window_sha256"] or
                checkpoint["parent"]["news_sha256"] != row["news_snapshot_sha256"]):
            raise ValueError("Khóa bank không khớp prefix gốc của checkpoint")
        alpha = checkpoint["alpha"]["value"]
        indicator = checkpoint["indicator"]["value"]
        directions = {"BULLISH", "BEARISH", "NEUTRAL"}
        if (alpha is not None and alpha not in directions) or indicator not in directions:
            raise ValueError("Checkpoint bank có hướng Alpha/Indicator sai")
        ready = key["reason"] is None
        rows.append({**economic_trace(row), "regime": checkpoint["regime"]["state"]["regime_name"],
                     "retrieval_key": key, "alpha_consensus": alpha, "alpha_na_reason": checkpoint["alpha"].get("reason"),
                     "indicator_consensus": indicator, "sentiment": None,
                     "sentiment_na_reason": checkpoint["sentiment"]["reason"],
                     "statistics_ready": ready, "example_ready": ready and alpha is not None,
                     "provenance": {"prefix_sha256": checkpoint["parent"]["prefix_sha256"],
                                    "checkpoint_sha256": digest(checkpoint),
                                    "news_sha256": row["news_snapshot_sha256"],
                                    "regime_model_sha256": checkpoint["regime"]["artifact_sha256"]}})

    query_source = {source["symbol"]: source for source in accepted["query_sources"]}
    frames = {}
    for symbol, source in query_source.items():
        frame = pd.read_csv(io.BytesIO(safe(root, source["raw_csv"]).read_bytes()), parse_dates=["Datetime"])
        frames[symbol] = frame.loc[frame.Datetime >= source["origin"]].copy()
    query = []
    for point in read(root, ASSETS + "query_inputs.json"):
        symbol, cutoff = point["symbol"], point["cutoff"]
        prefix = raw_point_in_time_snapshot(frames[symbol], cutoff)
        sha = digest(frame_document(validated_frame(prefix)))
        if sha != point["price_prefix_sha256"]:
            raise ValueError("Giá query khác prefix đã pin")
        query.append({"id": point["id"], "symbol": symbol, "cutoff": cutoff, "fold": point["fold"],
                      "retrieval_key": key_at(prefix, calendar, cutoff), "price_prefix_sha256": sha,
                      "selector_sha256": point["selector_sha256"], "news_snapshot_sha256": point["news_snapshot_sha256"],
                      "regime": point["regime"]["regime_name"], "prior_fallback": point["prior_fallback"]})
    if len(query) != 102 or {p["id"] for p in query} != reserved:
        raise ValueError("Query keys không khớp 102 ID FIN02")
    return {"version": VERSION, "key_profile": PROFILE, "records": rows}, {"version": VERSION, "records": query}


def summarize(bank: dict, query: dict) -> dict[str, Any]:
    """Tách mẫu thống kê, ví dụ và lý do NA theo mã/regime để FIN07 kiểm gate."""
    groups: dict[str, Counter] = {}
    coverage: Counter = Counter()
    for row in bank["records"]:
        group = groups.setdefault(f"{row['symbol']}/{row['regime']}", Counter())
        group.update(planned=1, statistics_ready=int(row["statistics_ready"]), example_ready=int(row["example_ready"]))
        coverage.update(statistics_ready=int(row["statistics_ready"]), example_ready=int(row["example_ready"]),
                        alpha_na=int(row["alpha_consensus"] is None), sentiment_na=int(row["sentiment"] is None))
    return {**dict(coverage), "bank_records": len(bank["records"]), "query_records": len(query["records"]),
            "query_key_reasons": dict(Counter(r["retrieval_key"]["reason"] or "AVAILABLE" for r in query["records"])),
            "bank_key_reasons": dict(Counter(r["retrieval_key"]["reason"] or "AVAILABLE" for r in bank["records"])),
            "support_by_symbol_regime": {key: dict(counts) for key, counts in groups.items()}}
