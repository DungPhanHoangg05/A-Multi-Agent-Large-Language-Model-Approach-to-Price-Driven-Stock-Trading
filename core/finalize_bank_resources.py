"""Chuẩn bị tài nguyên FIN06 offline theo nguồn giá thô và policy tin đã khóa."""
from __future__ import annotations

from collections import Counter
import io
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import numpy as np
import pandas as pd

from core.backtest_engine import compute_round_trip_net_return
from core.bayesian_memory import validate_historical_task_record
from core.causal_alpha import CONFIG, frame_document, validated_frame
from core.execution_prices import raw_point_in_time_snapshot, load_verified_execution_data
from core.finalize_news import FinalizedNews
from core.finalize_news_release import CORPUS, COVERAGE, check_release
from core.finalize_price_acceptance import ACCEPTANCE, PROFILE, require_accepted_prices
from core.finalize_price_audit import visible_event_dates
from core.finalize_raw_selector import VERSION as SELECTOR_VERSION, fit_raw_selector
from core.historical_evaluation_context import FrozenTimeline
from core.mt_bicl_bank import SOURCE, build_dense_bank, content_hash
from core.mt_bicl_scaler import fit_scaler
from core.pit_price_features import extract_pit_price_features
from core.price_feature_index import build_price_feature_index
from core.regime_detector import MarketRegimeDetector, training_data_hash
from core.unified_contracts import day, digest
from core.unified_protocol import CORE4, binding, read, safe

DIRECTORY = "docs/plan/week12/"
CONTRACT = DIRECTORY + "finalize_comparison_contract.json"
RECIPE = DIRECTORY + "finalize_bank_recipe_v1.json"
ASSETS = "outputs/finalize/bank_resources_v1/"
MODEL = "docs/plan/week11/mt_bicl_replica_full_r1_model.json"
HMM = "data_manager/regime_model.json"
BANK = "data_manager/regime_memory_store.json"
BANK_MANIFEST = "data_manager/regime_memory_store.manifest.json"
LEGACY_QA = "docs/plan/week2/memory_bank_audit.json"
PRODUCER = "finalize_numeric_bank_resources_v1"


def build_recipe(root: Path) -> dict[str, Any]:
    """Khóa recipe và nguồn trước fit. Không nhận cờ PASS do file bên ngoài tự khai."""
    contract = read(root, CONTRACT, True)
    candidate_pin = contract["sources_and_availability"]["candidate_assets"]
    if binding(root, candidate_pin["path"]) != candidate_pin:
        raise ValueError("Manifest U06 khác hợp đồng FIN02")
    manifest = read(root, candidate_pin["path"], True)
    expected = manifest["source_bindings"] | manifest["asset_bindings"]
    model = read(root, MODEL, True)
    model_files = [f"{folder}/{name}" for folder, names in model["artifact_trees"].items() for name in names]
    model_paths = [BANK, BANK_MANIFEST, LEGACY_QA, HMM, MODEL,
                   model["preprocessing"]["regime_models"]["path"], *model_files]
    for path in model_paths:
        if binding(root, path) != expected[path]:
            raise ValueError("Nguồn tài nguyên đã pin bị đổi: " + path)
    fit_contract = contract["fit_and_purge"]
    if any(CONFIG.get(key) != value for key, value in fit_contract["alpha_config"].items()):
        raise ValueError("Tham số selector khác FIN02")
    paths = [CONTRACT, ACCEPTANCE, CORPUS, COVERAGE, candidate_pin["path"], *model_paths,
             "core/finalize_bank_resources.py", "core/finalize_raw_selector.py", "core/causal_alpha.py",
             "core/alpha_compare.py", "core/backtest_engine.py", "core/execution_prices.py", "core/bayesian_memory.py",
             "core/regime_detector.py", "core/mt_bicl_bank.py", "core/mt_bicl_scaler.py", "core/mt_bicl_regimes.py",
             "core/price_feature_index.py", "core/pit_price_features.py", "core/historical_evaluation_context.py",
             "core/finalize_news.py", "core/finalize_news_release.py", "core/finalize_price_acceptance.py",
             "scripts/prepare_finalize_bank.py"]
    return {"version": PRODUCER, "source_bindings": [binding(root, name) for name in paths],
            "price_profile": PROFILE, "selector_version": SELECTOR_VERSION,
            "alpha_config": CONFIG.copy(), "alpha_schedules": fit_contract["schedules_by_symbol"],
            "reserved_ids": sorted(p["id"] for p in contract["domain"]["primary_points"]),
            "prior_fit_end": "2022-12-30", "mt_scaler_fit_end": "2020-12-31",
            "student_seed": 42, "student_step": 3000,
            "selector_delta": "Label fit giá thô giữ cadence/fee/horizon/threshold; loại quyền và phiên không khớp trước oracle.",
            "signal_policy": "Thiếu raw/request từng episode phải khôi phục hoặc cấp lượt thu riêng tại FIN09. Không dùng tín hiệu lịch sử làm bank causal mới. Không áp selector/HMM fit muộn hơn ngày episode để bù tín hiệu/regime.",
            "economic_policy": "Dùng oracle trên chu kỳ đã đáo hạn. Không sinh label cho 102 ID đã reserve.",
            "ood_policy": "NO_SAME_SYMBOL_FROZEN_BANK_OOD -> original_common; thiếu integrity/signal của CORE4 là blocker, không coi là OOD.",
            "query_outcome_allowed": False, "hosted_api_allowed": False}


def mature_cycles(rows: list[dict], reserved: set[str], cutoff: str) -> None:
    """Chặn toàn bộ ID reserve và exit >= cutoff trước khi đọc hoặc tạo nhãn."""
    keys = set()
    for row in rows:
        key = f"{row['symbol']}-{day(row['as_of_date'])}"
        if key in reserved or key in keys or not row["as_of_date"] < day(row["exit_date"]) < day(cutoff):
            raise ValueError("Bank trùng ID, chứa query reserve hoặc label chưa đáo hạn")
        keys.add(key)


def history_assets(root: Path, recipe: dict, accepted: dict, market: pd.DataFrame,
                   prices: dict, news: FinalizedNews) -> tuple[dict, dict, dict]:
    """Tái dựng payoff bank, index và scaler trên lịch train, đối chiếu donor lịch sử."""
    rows = read(root, BANK)
    mature_cycles(rows, set(recipe["reserved_ids"]), "2022-12-31")
    legacy = read(root, BANK_MANIFEST)
    audit = read(root, LEGACY_QA)
    bank_pin = binding(root, BANK)
    if (len(rows) != legacy["completed"] or len(rows) != 852 or legacy["bank_sha256"] != bank_pin["sha256"]
            or audit["bank_sha256"] != bank_pin["sha256"] or audit["run_signature"] != legacy["run_signature"]):
        raise ValueError("Membership bank lịch sử khác receipt")
    session_calendar = pd.DatetimeIndex(market.Datetime)
    train_calendar = session_calendar[session_calendar <= pd.Timestamp(recipe["prior_fit_end"])]
    source_rows = {row["symbol"]: row for row in accepted["query_sources"]}
    records, differences, signs = [], [], 0
    for symbol in CORE4:
        frame, events = prices[symbol]
        indexed = frame.set_index("Datetime")
        donor = pd.DataFrame(read(root, source_rows[symbol]["replaces_donor"]))
        donor["Datetime"] = pd.to_datetime(donor.Datetime)
        donor = donor.loc[donor.Datetime <= train_calendar[-1]].set_index("Datetime")
        for row in (r for r in rows if r["symbol"] == symbol):
            validate_historical_task_record(row, frame, events)
            cutoff, entry, exit_date = (row[k] for k in ("as_of_date", "entry_date", "exit_date"))
            positions = train_calendar.get_indexer(pd.to_datetime([cutoff, entry, exit_date]))
            if positions[0] < 0 or tuple(positions - positions[0]) != (0, 1, 3):
                raise ValueError("Nhãn bank không khớp t+1/t+3 trên lịch VNINDEX")
            raw = compute_round_trip_net_return(float(indexed.at[entry, "Open"]), float(indexed.at[exit_date, "Close"]))
            comparison = compute_round_trip_net_return(float(donor.at[entry, "Open"]), float(donor.at[exit_date, "Close"]))
            differences.append(abs(raw - comparison) * 100)
            signs += int((raw > 0) != (comparison > 0))
            snapshot = news.snapshot(symbol, cutoff)
            records.append({**{k: row[k] for k in ("episode_id", "symbol", "as_of_date", "entry_date", "exit_date")},
                            "r_net": raw, "y": int(raw > 0), "legacy_row_sha256": digest(row),
                            "signal_status": "RAW_REQUEST_RESPONSE_UNVERIFIED", "signal_admitted": False,
                            "price_manifest": accepted["bank_source"] + "manifest.json",
                            "news_snapshot_sha256": snapshot["sha256"]})
    membership = [{k: row[k] for k in ("episode_id", "symbol", "as_of_date", "exit_date")} for row in records]
    price_manifest = binding(root, accepted["bank_source"] + "manifest.json")
    provenance = {"bank": {"bank_sha256": bank_pin["sha256"]},
                  "calendar": {"sha256": binding(root, accepted["calendar"])["sha256"]},
                  "prices": {s: {"manifest_sha256": price_manifest["sha256"]} for s in CORE4}}
    index = build_price_feature_index(records=membership, prices=prices, calendar=train_calendar,
                                      source=SOURCE, provenance=provenance)
    if any(identifier.split("-", 1)[1] <= recipe["mt_scaler_fit_end"] for identifier in recipe["reserved_ids"]):
        raise ValueError("Có query reserve trong miền train MT trước khi tính nhãn")
    mt_train = build_dense_bank(prices, train_calendar, end_date=recipe["mt_scaler_fit_end"])
    mature_cycles(mt_train["records"], set(recipe["reserved_ids"]), "2021-01-01")
    scaler = fit_scaler(mt_train, "2021-01-01")
    bank = {"records": records, "membership_sha256": digest(membership), "scope": "NUMERIC_ONLY",
            "counts": dict(Counter(row["symbol"] for row in records)), "max_exit": max(r["exit_date"] for r in records),
            "legacy_signal_journal_path_present": (root / legacy["run_dir"] / "run_manifest.json").is_file(),
            "signal_ready": 0, "signal_pending": len(records), "legacy_model_options": legacy["models"],
            "required_signal_evidence": ["prefix OHLCV và tin FIN05", "request/response và checkpoint theo node",
                                         "recipe Alpha causal đúng ngày episode", "regime model fit đúng prefix episode"],
            "donor_return_differences_gt_1e_8_pp": sum(delta > 1e-8 for delta in differences),
            "donor_max_difference_pp": max(differences), "donor_sign_flips": signs}
    return bank, {"payload": index.payload, "sha256": index.identity}, scaler


def rebuild(root: Path, recipe: dict) -> dict[str, Any]:
    """Tạo artifact số độc lập với query outcome, giữ signal gate chặn khi thiếu nguồn."""
    if recipe != build_recipe(root):
        raise ValueError("Recipe FIN06 không khớp nguồn/runtime producer hiện tại")
    accepted = require_accepted_prices(root, profile=PROFILE)
    coverage = check_release(root)
    corpus = read(root, CORPUS, True)
    news = FinalizedNews(corpus["records"], evidence=corpus["evidence_registry"], root=root)
    market = pd.read_csv(safe(root, accepted["calendar"]), parse_dates=["Datetime"])
    calendar = pd.DatetimeIndex(market.Datetime)
    prices = {s: load_verified_execution_data(root / accepted["bank_source"], s) for s in CORE4}
    bank, index, scaler = history_assets(root, recipe, accepted, market, prices, news)
    model = read(root, MODEL, True)
    checkpoint = model["training"]
    frozen_scalers = model["preprocessing"]["scalers"]
    if (len(frozen_scalers) != 1 or frozen_scalers.get(content_hash(scaler)) != scaler
            or (checkpoint["selected_seed"], checkpoint["selected_step"]) != (recipe["student_seed"], recipe["student_step"])):
        raise ValueError("Scaler train MT hoặc checkpoint student không tái lập theo recipe đã khóa")
    train = market.loc[market.Datetime <= recipe["prior_fit_end"]].copy()
    train_hash = training_data_hash(train)
    hmm = MarketRegimeDetector.load(root / HMM, expected_training_hash=train_hash)
    if hmm.metadata["train_end_date"] != recipe["prior_fit_end"]:
        raise ValueError("HMM prior kết thúc sau hoặc khác ngày fit đã khóa")
    timeline = FrozenTimeline(SimpleNamespace(root=root, history=market, model_manifest=model))
    regimes = {"prior_train_source_sha256": train_hash, "prior_metadata": hmm.metadata,
               "mt_prefixes": sorted(timeline._models), "mt_scaler": scaler,
               "mt_scaler_sha256": content_hash(scaler), "student_checkpoint": checkpoint["selected_checkpoint"]}
    if any(model_date > recipe["prior_fit_end"] for model_date in regimes["mt_prefixes"]):
        raise ValueError("Prefix HMM MT vượt ranh giới train")
    selectors, query = {}, []
    reserved = set(recipe["reserved_ids"])
    for source in accepted["query_sources"]:
        symbol = source["symbol"]
        frame = pd.read_csv(io.BytesIO(safe(root, source["raw_csv"]).read_bytes()), parse_dates=["Datetime"])
        frame = frame.loc[frame.Datetime >= source["origin"]].reset_index(drop=True)
        doc = read(root, source["event_ledger"])
        schedule = recipe["alpha_schedules"][symbol]
        fit_day = str(frame.loc[frame.Datetime < schedule["test_start"], "Datetime"].iloc[-1].date())
        fit_events, _ = visible_event_dates(doc["records"], fit_day)
        selectors[symbol] = fit_raw_selector(frame, [{"exrightDate": date} for date in fit_events], schedule, frozenset(
            p.split("-", 1)[1] for p in reserved if p.startswith(symbol + "-")))
        for point in (p for p in accepted["points"] if p["symbol"] == symbol):
            cutoff = point["cutoff"]
            prefix = raw_point_in_time_snapshot(frame, cutoff)
            sentiment = news.snapshot(symbol, cutoff)
            known_events, _ = visible_event_dates(doc["records"], cutoff)
            feature = extract_pit_price_features(prefix.merge(frame[["Datetime", "Reference"]], on="Datetime", validate="one_to_one"),
                                                 [{"exrightDate": date} for date in known_events], calendar, cutoff, source=SOURCE)
            state = hmm.classify_regime(market.loc[market.Datetime <= cutoff].copy(), cutoff)
            if state["feature_end_date"] > cutoff or point["id"] not in reserved:
                raise ValueError("Preparation query vượt cutoff hoặc thiếu reservation")
            query.append({k: point[k] for k in ("id", "symbol", "cutoff", "fold")} | {
                "price_prefix_sha256": digest(frame_document(validated_frame(prefix))),
                "selector_sha256": selectors[symbol]["sha256"], "feature": feature,
                "regime": state, "news_snapshot_sha256": sentiment["sha256"],
                "prior_fallback": "NO_SAME_SYMBOL_FROZEN_BANK_OOD" if symbol not in CORE4 else None,
                "fallback_variant": "original_common" if symbol not in CORE4 else None})
    if {r["id"]: r["news_snapshot_sha256"] for r in query} != {r["id"]: r["snapshot_sha256"] for r in coverage["points"]}:
        raise ValueError("Query preparation khác tập điểm hoặc snapshot tin FIN05")
    return {"bank.json": bank, "prior_index.json": index, "regimes.json": regimes,
            "selectors.json": selectors, "query_inputs.json": sorted(query, key=lambda row: row["id"])}
