"""Khóa protocol đánh giá lịch sử bằng dữ liệu local; không fit hoặc gọi API."""

from __future__ import annotations

from copy import deepcopy
from datetime import date
import hashlib
from importlib.metadata import version
import json
import math
from pathlib import Path
import platform
import subprocess
from typing import Any

import numpy as np
import pandas as pd

from core.historical_asset_readiness import price_view

DIRECTORY = Path("docs/plan/week11")
PROTOCOL = DIRECTORY / "historical_evaluation_protocol.json"
INPUTS = DIRECTORY / "historical_evaluation_inputs.json"
FIX = Path("outputs/historical_reevaluation/inputs/fix")
DONOR_BANK = FIX / "outputs/revision/r1_72h_bank_v2/manifest.json"
GRID = Path("outputs/historical_reevaluation/manifests/candidate_grid.json")
MODEL = DIRECTORY / "mt_bicl_replica_full_r1_model.json"
TELEMETRY = Path("outputs/oos_pilot/api_usage.json")
DONOR = "9efd23f4157e0d3ab8069fccab7dccf03439a714"
CORE4 = ("FPT", "MWG", "VCB", "VNM")
PRIMARY = ("Original_common", "bayesian_v1", "C2", "A_tp_pool", "B_semantic", "MT_BICL")
ABLATIONS = tuple(f"{base}_{mode}" for base in ("C2", "A_tp_pool", "B_semantic")
                  for mode in ("stats_only", "examples_only")) + (
    "Plain_revision", "No_utility", "No_target", "Stats_only")
CONTROLS = ("random", "recent", "similarity")
MODELS = ("openai/gpt-oss-20b", "qwen/qwen3.8-27b")
CODE = ("core/historical_evaluation_protocol.py", "core/historical_evaluation_statistics.py",
        "scripts/prepare_historical_evaluation.py")
METHOD_CODE = (
    "agents/decision_agent.py", "core/backtest_engine.py", "core/bayesian_retriever.py",
    "core/prior_config.py", "core/prior_prompt.py", "core/prior_example_selection.py",
    "core/prior_conditional_statistics.py", "core/prior_quality_gate.py",
    "core/prior_price_similarity.py", "core/price_feature_index.py", "core/pit_price_features.py",
    "core/improvement_prior.py", "core/historical_signals.py", "core/historical_runner.py",
    "core/regime_detector.py", "core/groq_pacing.py", "core/provider_quota.py",
    "core/research_invocation.py", "core/mt_bicl_adapter.py", "core/mt_bicl_tasks.py",
    "core/mt_bicl_stream.py", "core/mt_bicl_regimes.py", "core/mt_bicl_context.py",
    "core/mt_bicl_decision.py", "core/mt_bicl_prompt.py", "core/mt_bicl_policy.py",
    "core/mt_bicl_utility.py", "core/mt_bicl_contracts.py", "core/mt_bicl_teacher.py",
    "core/mt_bicl_student.py", "core/mt_bicl_inputs.py", "core/mt_bicl_scaler.py",
    "core/mt_bicl_features.py", "core/mt_bicl_prompt_limits.py")


def encode(value: Any) -> bytes:
    """Mã hóa JSON hữu hạn, giữ byte LF độc lập cấu hình checkout."""
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2,
                       allow_nan=False) + "\n").encode("utf-8")


def digest(value: Any) -> str:
    """Băm nội dung thay vì hình thức thụt dòng của envelope."""
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def safe(root: Path, name: str | Path) -> Path:
    """Chỉ đọc đường dẫn trong repo, không nhận symlink hoặc credential."""
    relative = Path(name)
    if relative.is_absolute() or ".." in relative.parts or any(p.startswith(".env") for p in relative.parts):
        raise ValueError("Đường dẫn protocol không hợp lệ")
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()) or any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError("Đường dẫn protocol vượt workspace hoặc qua symlink")
    return path


def read(root: Path, name: str | Path, *, envelope: bool = False) -> Any:
    """Kiểm envelope nếu caller yêu cầu, không coi tự băm lại là provenance."""
    value = json.loads(safe(root, name).read_bytes())
    if envelope:
        if set(value) != {"payload", "sha256"} or digest(value["payload"]) != value["sha256"]:
            raise ValueError("Envelope protocol sai checksum")
        return value["payload"]
    return value


def binding(root: Path, name: str | Path) -> dict[str, Any]:
    """Lưu path, kích thước và SHA256 của đúng byte nguồn."""
    raw = safe(root, name).read_bytes()
    return {"path": Path(name).as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def frozen_sources(root: Path) -> dict[str, Any]:
    """Xác minh blob donor trước khi dùng source archive làm đầu vào."""
    receipt = read(root, "outputs/historical_reevaluation/manifests/asset_readiness.json")
    if (receipt["donor_commit"] != DONOR or len(receipt["source_archive"]) != 21
            or len({r["source_path"] for r in receipt["source_archive"]}) != 21):
        raise ValueError("Archive phải đủ21 blob donor duy nhất")
    result = {}
    for row in receipt["source_archive"]:
        if (row["donor_commit"] != DONOR
                or row["archive_path"] != (FIX / row["source_path"]).as_posix()):
            raise ValueError("Donor khác mốc audit")
        raw = safe(root, row["archive_path"]).read_bytes()
        anchored = subprocess.check_output(["git", "show", f"{DONOR}:{row['source_path']}"], cwd=root)
        if raw != anchored or hashlib.sha256(raw).hexdigest() != row["sha256"]:
            raise ValueError("Archive khác blob donor: " + row["source_path"])
        result[row["archive_path"]] = binding(root, row["archive_path"])
    return result


def timeline(root: Path) -> dict[str, Any]:
    """Khóa ID/ngày, lịch history đủ population và panel không đọc payoff."""
    bank = read(root, DONOR_BANK)
    grid = read(root, GRID)
    price_manifest = read(root, FIX / "outputs/revision/r1_prices_v1/manifest.json")
    frames, views = {}, {}
    for row in price_manifest["symbols"]:
        raw = safe(root, FIX / "outputs/revision/r1_prices_v1" / row["path"]).read_bytes()
        if hashlib.sha256(raw).hexdigest() != row["sha256"]:
            raise ValueError("Giá khác manifest donor")
        frame, view = price_view(raw)
        frames[row["symbol"]] = frame
        views[row["symbol"]] = view
    derived, scopes, panel = [], [], []
    for scope in bank["schedule"]:
        symbol, fold = scope["symbol"], scope["fold"]
        days = frames[symbol]["date"].astype(str).to_numpy()
        first, last = scope["test"]
        train, validation = scope["train"], scope["validation"]
        if (first < 599 or last != first + 57 or not train or not validation
                or train != sorted(set(train)) or validation != sorted(set(validation))
                or min(train) < 599 or max(train) + 3 >= min(validation)
                or max(validation) + 3 >= first or last + 3 >= len(days)):
            raise ValueError("Scope thiếu warmup hoặc vi phạm purge")
        scope_rows = []
        for index in range(first, last + 1, 3):
            row = {"id": f"{symbol}_{fold}_{index}", "symbol": symbol, "fold": fold,
                   "suffix_decision_index": index,
                   "raw_decision_index": index + views[symbol]["excluded_prefix_rows"],
                   "date": str(days[index]), "entry_date": str(days[index + 1]),
                   "exit_date": str(days[index + 3]), "core4": symbol in CORE4,
                   "anchor": index in (first, last)}
            scope_rows.append(row)
        if any(a["exit_date"] >= b["entry_date"] for a, b in zip(scope_rows, scope_rows[1:])):
            raise ValueError("Holding span của grid chồng lấn")
        derived.extend(scope_rows)
        # Chọn trước response bằng hash ID; không dùng nhãn hoặc sentiment coverage.
        panel.append(min(scope_rows, key=lambda r: (hashlib.sha256(
            ("upstream-panel-v1|" + r["id"]).encode()).hexdigest(), r["id"]))["id"])
        scopes.append({**deepcopy(scope), "train_max_exit": str(days[max(train) + 3]),
                       "validation_max_exit": str(days[max(validation) + 3])})
    if derived != grid or len(grid) != 1020 or len({r["id"] for r in grid}) != 1020:
        raise ValueError("Grid khác 1.020 ID donor đã audit")
    if (sum(r["core4"] for r in grid) != 480 or sum(r["anchor"] for r in grid) != 102
            or len(scopes) != 51 or len(set(panel)) != 51):
        raise ValueError("Cohort/scope/anchor/panel không đủ support đã đăng ký")
    query_keys = {(r["symbol"], r["date"]): r["id"] for r in grid}
    history = []
    for symbol, frame in sorted(frames.items()):
        days = frame["date"].astype(str).to_numpy()
        cutoff = max(r["date"] for r in grid if r["symbol"] == symbol)
        indices = np.arange(599, len(days) - 3, 3)
        indices = indices[days[indices + 3] < cutoff]
        for index in indices.tolist():
            shared_id = query_keys.get((symbol, str(days[index])))
            history.append({"id": f"{symbol}:{days[index]}", "symbol": symbol,
                            "date": str(days[index]), "entry_date": str(days[index + 1]),
                            "exit_date": str(days[index + 3]), "suffix_decision_index": index,
                            "shared_query_unit": shared_id})
    return {"grid": grid, "scopes": scopes, "panel_ids": sorted(panel), "history": history,
            "history_rule": "CLEAN_SUFFIX_INDEX_599_PLUS_3J; EXIT_STRICTLY_BEFORE_LAST_QUERY_PER_SYMBOL",
            "history_collection": "FULL_POPULATION_NOT_ONLY_SELECTED_K; NO_LEGACY_CACHE_CREDIT",
            "prequential": "HISTORY_CADENCE_MEMBERS_ENTER_ONLY_WHEN_EXIT_LT_QUERY; NO_TEST_GRID_INSERT_OFF_CADENCE",
            "query_history_reuse": "ONLY_SAME_NEW_RUN_REALIZATION0_EXACT_PARENT_SOURCE_OPTIONS_SCHEMA_PAYLOAD"}


def telemetry(root: Path) -> dict[str, Any]:
    """Chỉ xuất aggregate token/latency; không sao chép key, scope hay request ID."""
    ledger = read(root, TELEMETRY)
    result = {"source": binding(root, TELEMETRY),
              "scope": "HISTORICAL_REFERENCE_NOT_MEASUREMENT_OF_NEW_960_CONTRACT", "models": {}}
    for model in MODELS:
        rows = [r for r in ledger["requests"] if r.get("model") == model and r.get("status") == 200
                and all(type(r.get(k)) in (int, float) and math.isfinite(r[k]) and r[k] >= 0
                        for k in ("prompt_tokens", "completion_tokens", "latency_seconds"))]
        if not rows:
            raise ValueError("Thiếu telemetry thành công cho model đã khóa")
        fields = {}
        for key in ("prompt_tokens", "completion_tokens", "latency_seconds"):
            array = np.asarray([r[key] for r in rows], dtype=float)
            fields[key] = {"mean": float(array.mean()), "p95": float(np.quantile(array, .95, method="linear"))}
        result["models"][model] = {"successful_responses": len(rows), "fields": fields,
            "latest_observed_limits": {k: rows[-1].get("rate_limits", {}).get(k) for k in
                ("x-ratelimit-limit-requests", "x-ratelimit-limit-tokens")}}
    return result


def research_calls(inputs: dict[str, Any]) -> dict[str, int]:
    """Đếm executions khoa học, tách retry, bypass, fit và cache hit."""
    grid, anchors, panel = len(inputs["grid"]), sum(r["anchor"] for r in inputs["grid"]), len(inputs["panel_ids"])
    historical = sum(r["shared_query_unit"] is None for r in inputs["history"])
    decision = grid * 7 * 3 + anchors * (len(ABLATIONS) + len(CONTROLS) + 1) * 3 + panel * 2 * 7 * 3
    return {"primary_and_anchor_decision": grid * 7 * 3, "ablation_decision": anchors * len(ABLATIONS) * 3,
            "retrieval_control_decision": anchors * len(CONTROLS) * 3, "duplicate_decision": anchors * 3,
            "extra_panel_decision": panel * 2 * 7 * 3, "decision": decision,
            "query_panel_vision": 2 * (grid + panel * 2), "historical_upstream_H": historical,
            "history_population": len(inputs["history"]),
            "history_shared_query_upstream": len(inputs["history"]) - historical,
            "vision": 2 * (grid + panel * 2 + historical),
            "research_total": decision + 2 * (grid + panel * 2 + historical)}


def history_before(inputs: dict[str, Any], symbol: str, query_date: str) -> list[dict[str, Any]]:
    """Cấp pool trước rank, không cấp cycle exit==query hoặc khác mã."""
    if type(query_date) is not str or date.fromisoformat(query_date).isoformat() != query_date:
        raise ValueError("Ngày query phải là ISO YYYY-MM-DD")
    symbols = {row["symbol"] for row in inputs["grid"]}
    if symbol not in symbols:
        raise ValueError("Mã query không thuộc cohort")
    selected = []
    for row in inputs["history"]:
        if row["symbol"] != symbol:
            continue
        for key in ("date", "entry_date", "exit_date"):
            if type(row[key]) is not str or date.fromisoformat(row[key]).isoformat() != row[key]:
                raise ValueError("History có ngày không chuẩn")
        if not row["date"] < row["entry_date"] <= row["exit_date"]:
            raise ValueError("History sai thứ tự quyết định/entry/exit")
        if row["exit_date"] < query_date:
            selected.append(row)
    return deepcopy(selected)


def budget(inputs: dict[str, Any]) -> dict[str, Any]:
    """Ước lượng tham chiếu và trần dự toán; không coi dự toán là quota tài khoản."""
    calls = research_calls(inputs)
    models = {}
    for model, count, prices in zip(MODELS, (calls["decision"], calls["vision"]), ((.075, .30), (.80, 4.))):
        fields = inputs["telemetry"]["models"][model]["fields"]
        input_mean, output_mean = fields["prompt_tokens"]["mean"], fields["completion_tokens"]["mean"]
        models[model] = {"research_calls": count, "input_usd_per_million": prices[0],
            "output_usd_per_million": prices[1], "reference_input_tokens": math.ceil(count * input_mean),
            "reference_output_tokens": math.ceil(count * output_mean),
            "reference_latency_hours_serial": count * fields["latency_seconds"]["mean"] / 3600,
            "reference_uncached_usd": count * (input_mean * prices[0] + output_mean * prices[1]) / 1e6,
            "planning_input_tokens_per_call": 6500, "completion_reserve_per_call": 960,
            "planning_tokens": count * 7460,
            "planning_uncached_usd": count * (6500 * prices[0] + 960 * prices[1]) / 1e6}
    tokens = sum(v["reference_input_tokens"] + v["reference_output_tokens"] for v in models.values())
    reserve = sum(v["planning_tokens"] for v in models.values())
    nominal = calls["research_total"]
    maximum_attempts = (nominal + 100) * 3 + math.ceil(nominal * .05)
    maximum_cost = 3 * sum(v["planning_uncached_usd"] for v in models.values())
    maximum_cost += (300 + math.ceil(nominal * .05)) * (6500 * .8 + 960 * 4.) / 1e6
    return {"calls": calls, "models": models,
        "pricing_checked_date": "2026-11-08",
        "pricing_sources": ["https://console.groq.com/docs/model/openai/gpt-oss-20b",
                            "https://console.groq.com/docs/model/qwen/qwen3.8-27b"],
        "quota_source": "https://console.groq.com/docs/rate-limits",
        "quota_reference_per_org": {"rpm": 30, "rpd": 1000, "tpm": 8000, "tpd": 200000},
        "organization_count_assumed": 5, "organization_independence_verified": False,
        "quota_account_itpm_otpm_spend_limits": "H06_REQUIRED_NO_LIVE_PREFLIGHT_IN_H03",
        "reference_token_days_5_org_shared_model_quota": math.ceil(tokens / 1000000),
        "planning_token_days_5_org_shared_model_quota": math.ceil(reserve / 1000000),
        "reference_token_days_1_org": math.ceil(tokens / 200000),
        "reference_usd": sum(v["reference_uncached_usd"] for v in models.values()),
        "planning_usd": sum(v["planning_uncached_usd"] for v in models.values()),
        "completion_reserve_is_not_expected_usage": True,
        "cached_token_discount_assumed": False, "deadline_guaranteed": False,
        "http_attempt_cap_per_execution": 3, "all_research_http_attempt_cap": nominal * 3,
        "smoke_control_execution_reserve": 100, "unknown_attempt_reserve": math.ceil(nominal * .05),
        "max_total_http_attempts": maximum_attempts,
        "all_attempts_planning_usd": maximum_cost,
        "all_attempts_planning_token_days_5_org": math.ceil(maximum_attempts * 7460 / 1000000),
        "research_planning_usd_excludes_attempt_reserves": True,
        "attempt_budget_note": "FORMAT_REPAIR_AND_TRANSPORT_RETRY_SHARE_3; UNKNOWN_REPLAY_REQUIRES_UUID_AUDIT",
        "estimated_image_storage_bytes": (len(inputs["grid"]) + 2 * len(inputs["panel_ids"])
                                            + calls["historical_upstream_H"]) * 2 * 512 * 1024,
        "ram_planning_gib": 2, "new_payload_latency_ram_validation": "H06_REQUIRED",
        "feasibility": "MULTIWEEK_FREE_TIER_NO_72H_PROMISE; NO_AUTOMATIC_PAID_PLAN_OR_SAMPLE_REDUCTION"}


def contract(root: Path, inputs: dict[str, Any]) -> dict[str, Any]:
    """Ghi recipe hiệu lực riêng; không sửa protocol đã khóa cho train/các vòng cũ."""
    old = read(root, DIRECTORY / "mt_bicl_protocol.json")
    effective = deepcopy(old)
    effective["economic_contract"].update(lot=None, fractional_shares=True, risk_policy="OFF")
    effective["calendar"]["source"] = "outputs/historical_reevaluation/h02_data_r1/VNINDEX_2018_2026_verified_overlap.csv"
    effective["decision"]["config"]["symbol_order"] = sorted({r["symbol"] for r in inputs["grid"]})
    options = effective["decision"]["config"]["signal_config"]["models"]
    options.update(agent_llm_max_tokens=960, graph_llm_max_tokens=960)
    effective.update(version="historical_mt_bicl_effective_v1", status="SPEC_ONLY",
                     namespace="outputs/historical_reevaluation/run_r1")
    effective["price_manifest_sha256"] = {"donor": binding(root, FIX / "outputs/revision/r1_prices_v1/manifest.json")["sha256"]}
    # Giữ partition đã fit, bỏ nhãn confirmation cũ khỏi cấu hình đánh giá lịch sử mới.
    effective["splits"] = {key: deepcopy(old["splits"][key]) for key in
                           ("train", "checkpoint_selection", "validation")}
    effective["splits"].update(historical_evaluation=[min(r["date"] for r in inputs["grid"]),
                                                     max(r["exit_date"] for r in inputs["grid"])],
                               no_automatic_resplit=True)
    effective["evaluation_scope"] = "EXPOSED_2023_2026_EXPLORATORY_NOT_CONDITIONAL_CONFIRMATION"
    registry = {"Original_common": {"prior": "OFF", "schema": "legacy", "prompt": "common_legacy"},
        "bayesian_v1": {"prior": "bayesian_regime", "prefix": "compact_brpp_v1", "schema": "legacy",
                        "population": "SAME_SYMBOL_K3_SEED42_STRICT_EXIT"}}
    for name, prefix, statistics in (("C2", "compact_brpp_v3", "conditional_disjoint_beta_v1"),
            ("A_tp_pool", "compact_brpp_v3_tp_v1", "conditional_tp_disjoint_beta_v1"),
            ("B_semantic", "compact_brpp_semantic_v1", "conditional_disjoint_beta_v1")):
        registry[name] = {"prefix": prefix, "statistics": statistics, "schema": "legacy",
            "gate": "split_quality_gate_v2", "mode": "full_prior", "shrink_strength": 4.,
            "min_population_count": 20, "min_conditional_count": 5, "max_interval_width": .75,
            "selection": {"w_signal": .5, "half_life_days": 365, "max_prior_age_days": 730,
                          "min_gap_sessions": 5, "min_similarity": .625, "requested_k": 3, "seed": 42},
            "fallback": "ORIGINAL_REQUEST_IF_BOTH_STATS_AND_EXAMPLES_OFF; NO_SYNTHETIC_CASH"}
    registry["MT_BICL"] = {"schema": "anchored", "effective_contract": "effective_mt_bicl",
        "dependencies": ["Original_common", "Fact_Anchor"], "model": binding(root, MODEL),
        "missing_support": "KEEP_VALIDATED_A0_WITH_REASON", "student_failure": "STOP_NO_TEACHER_FALLBACK"}
    return {"version": "historical_evaluation_protocol_v1", "status": "LOCKED_OFFLINE_NOT_RELEASED",
        "namespace": "outputs/historical_reevaluation/run_r1", "inputs": binding(root, INPUTS),
        "authorization": {"api": False, "training": False, "teacher_fit": False, "confirmation": False},
        "cohorts": {"primary": "CORE4", "CORE4": list(CORE4), "EXTENDED": "ALL_1020_SECONDARY",
                    "scope_count": 51, "grid_count": 1020, "anchors": 102, "panel": 51,
                    "fold_order": list(dict.fromkeys(r["fold"] for r in inputs["scopes"])),
                    "BHN": "LAST_3_FOLDS_ONLY_CLEAN_SUFFIX_OFFSET_673"},
        "registry_order": list(PRIMARY), "registry": registry,
        "ablations": list(ABLATIONS), "retrieval_controls": {name: {"base": "bayesian_v1", "mode": name}
                                                              for name in CONTROLS},
        "dependency_only": ["Fact_Anchor"], "offline_only": ["Utility_only", "teacher", "student", "CASH", "always_LONG"],
        "effective_mt_bicl": effective,
        "reference_aliases": {"Original": "Original_common", "A_reference": "A_tp_pool",
                              "additional_execution_for_alias": False},
        "shared_inputs": {"price_series": "SAME_DONOR_SUFFIX_ALL_BRANCHES_NO_SPLICE",
            "news": {"availability": "DATE_ONLY_NEXT_DAY", "lookback_days": 90, "minimum_articles": 3,
                     "peers": [], "scorer_revision": "d7738b85200272f10ba8b048d80236c8c582b581",
                     "content_pit_certified": False, "normalizer_parity": "H04_REQUIRED"},
            "alpha": {"history_bars": 600, "required_factor_rows": 5, "norm": "zscore_tanh", "weights": None},
            "renderer": "DONOR_CHART_CONVENTION_V1_WITH_ALL_FACTOR_NAMES_VALUES_MASKS_H04_PARITY_REQUIRED"},
        "legacy_scaler": {"version": "symbol_fold_standard_v1", "fit": "SCOPE_TRAIN_IDS_FEATURES_ONLY_DDOF0",
                          "freeze": "BEFORE_VALIDATION; SAME_SCALE_QUERY_PRIOR; NO_FUTURE_OR_LABEL_FIT",
                          "zero_std_scale": 1., "missing": "EXAMPLES_OFF_WITH_REASON_NO_IMPUTATION"},
        "legacy_regime": {"historical": "PREFIX_AT_HISTORICAL_CUTOFF",
                          "evaluation": binding(root, "data_manager/regime_model.json"),
                          "evaluation_fit_end": "2022-12-30", "evaluation_refit": False},
        "memory": {"legacy": "FULL_SUFFIX_HISTORY_CADENCE_IN_INPUTS; EXIT_LT_QUERY_BEFORE_RANK",
                   "mt_bicl": "DONOR_SUFFIX_ONLY_NO_SPLICE; CALENDAR_INDEX20_PLUS3J_BLOCK63; FROZEN_2020_SCALER_REGIME; SAME_SYMBOL",
                   "query_y": "READ_ONLY_AFTER_ALL_REQUIRED_FORECASTS_DURABLE_AND_EXIT_LT_NEXT_QUERY",
                   "membership": "D_C_QUERY_IDS_AND_HOLDING_SPANS_DISJOINT; KEEP_K_M_AND_REASON_HASHES",
                   "prequential": True, "violation": "RAISE_VALUEERROR_OR_ASSERTIONERROR"},
        "paired": {"upstream_per_unit_realization": 1, "copy": "DEEP_COPY_EXACT_SHARED_STATE",
                   "execution_order": "CHRONOLOGICAL_UNION_HISTORY_AND_GRID; ORIGINAL_THEN_FACT_ANCHOR_THEN_REVISION",
                   "other_order": "LEFT_ROTATE_BY_GLOBAL_UNIT_INDEX_PLUS_REPEAT_PLUS_REALIZATION",
                   "decision_repeat_ids": [0, 1, 2], "main_realization": 0, "panel_extra_realizations": [1, 2],
                   "duplicate_scope": "ANCHORS_ALL_3_REPEATS_INDEPENDENT_EXECUTION_NO_RESPONSE_CACHE",
                   "controls_and_ablations": "ANCHORS_REALIZATION0_ALL_3_REPEATS",
                   "panel_branches": [*PRIMARY, "Fact_Anchor"], "repeat_summary": "PER_REPEAT_AND_MEAN_NEVER_VOTE_OR_BEST",
                   "panel_role": "SINGLE_UNIT_UPSTREAM_DIAGNOSTIC_EXCLUDED_FROM_PRIMARY_ACCOUNT_RUNS",
                   "legacy_2048_1024_cache_reusable": False},
        "economics": {**effective["economic_contract"], "reset": "PER_SYMBOL_FOLD_BRANCH_REALIZATION_REPEAT",
                      "price_unit": "thousand_VND_CONVERT_TO_VND_ONCE", "quality": "VENDOR_SERIES_LIMITED",
                      "acceptance": "PENDING_EXECUTION_DATA", "corporate_barriers": "KEEP_FLAG_NO_FILL_CERTIFICATION"},
        "inference": {"config": effective["decision"]["config"], "response_schema_location": "inputs.response_schemas",
                      "sdk_effective_temperature": "LOG_CONFIG0_AND_WIRE_VALUE_INCLUDING_1E-8",
                      "prior_chars_inclusive": 600, "prompt_chars_exclusive": 6500,
                      "distill_cap": "UNCHANGED", "vision_max_images": 3, "retry_wrapper": "_invoke_with_retry",
                      "http_attempts_including_format_repair": 3, "unknown": "STOP_KEEP_UUID_AND_RESERVE",
                      "organizations": {"count": 5, "unit_assignment": "1_PLUS_GLOBAL_UNIT_INDEX_MOD5",
                          "same_unit_all_branches_repeats": True, "shared_history_uses_query_org": True,
                          "nonshared_history_assignment": "1_PLUS_GLOBAL_HISTORY_INDEX_MOD5",
                          "quota_stop": "WAIT_SAME_ORG_PROVIDER_RESET_NO_SILENT_KEY_OR_MODEL_SWITCH",
                          "scope_logging": "HMAC_ONLY_NO_CREDENTIAL_IN_ARTIFACTS"},
                      "cache_identity": ["source", "prefix", "news", "renderer", "model", "options", "schema", "payload", "parent"]},
        "statistics": {"primary_contrasts": [name + "-Original_common" for name in PRIMARY[1:]],
            "return_unit": "percentage_points", "estimand": "MEAN_REPEAT_MEAN_6_BLOCKS_MEAN_4_SYMBOLS_PAIRED_RETURN",
            "primary_realization": 0,
            "balanced_accuracy_estimand": "SAME_MACRO_PAIRED_BA_DIFFERENCE_PER_SYMBOL_BLOCK_REPEAT; ANY_UNDEFINED_YIELDS_NULL_FAMILY",
            "extended": "MEAN_BLOCK_MEAN_ELIGIBLE_SYMBOLS_SECONDARY_NO_EXTRA_PRIMARY_CONTRAST",
            "draws": 10000, "seed": 20261107, "rng": "PCG64", "resample": "6_WHOLE_TIME_BLOCKS_WITH_REPLACEMENT",
            "paired_draw_indices": "SAME_ACROSS_SYMBOLS_METHODS_REPEATS_AND_RETURN_BA_FAMILIES",
            "family": "5_CONTRASTS; BA_SEPARATE_FAMILY", "ci": "CENTERED_MAX_ABS_DEVIATION",
            "quantile": .95, "quantile_method": "linear", "ties": "KEEP_ALL_TIES_NO_RANDOM_JITTER",
            "constant_contrast": "ZERO_WIDTH_IF_ENTIRE_FAMILY_CONSTANT; RETAIN_CONSTANT_MEMBERS_IN_FAMILY",
            "undefined_support": "NULL_ENTIRE_FAMILY_INCONCLUSIVE_NO_DROPPING_OR_ZERO_IMPUTATION",
            "target_half_width": {"return_pp": 1., "balanced_accuracy_pp": 3.},
            "low_precision": "KEEP_FIXED_SAMPLE_REPORT_LOW_PRECISION_NO_OUTCOME_DRIVEN_EXTENSION",
            "dependence": "SIX_DEPENDENT_BLOCKS_HISTORICAL_SENSITIVITY_NOT_SUPERIORITY_PROOF",
            "diagnostics": ["leave_one_block_out", "leave_one_symbol_out", "per_repeat", "raw_facts_veto", "student_teacher_gap"]},
        "budget": budget(inputs), "remaining_gates": ["H04_ADAPTER_RUNNER", "H05_SCOPE_TESTS", "H06_FREEZE_SMOKE_QUOTA"],
        "source_bindings": {name: binding(root, name) for name in (*CODE, *METHOD_CODE,
            "docs/plan/week11/mt_bicl_protocol.json", "docs/plan/week11/mt_bicl.schema.json", MODEL.as_posix())},
        "donor_implementation_refs": donor_references(root),
        "runtime": {"python": platform.python_version(), **{name: version(name) for name in
            ("numpy", "pandas", "scipy", "pydantic", "jsonschema", "langchain-core", "langchain-groq", "httpx", "tiktoken")}}}


def donor_references(root: Path) -> dict[str, Any]:
    """Neo mã convention/shared state để H04 port có provenance, không import donor."""
    result = {}
    for name in ("core/revision_common_study.py", "core/revision_minimal_bank.py",
                 "core/revision_execution_final.py", "core/revision_r2_panel.py", "scripts/freeze_revision_prices.py"):
        raw = subprocess.check_output(["git", "show", f"{DONOR}:{name}"], cwd=root)
        oid = subprocess.check_output(["git", "rev-parse", f"{DONOR}:{name}"], cwd=root).decode().strip()
        result[name] = {"commit": DONOR, "blob_oid": oid, "bytes": len(raw),
                        "sha256": hashlib.sha256(raw).hexdigest()}
    return result


def build_inputs(root: Path) -> dict[str, Any]:
    """Đóng băng input/hash, schema response và lịch; không tạo forecast hoặc payoff."""
    from agents.decision_agent import TradeDecisionOutput
    from core.mt_bicl_contracts import wire_schema

    sources = frozen_sources(root)
    model = read(root, MODEL, envelope=True)
    if model["status"] != "COLD_VERIFIED" or model["inference_released"] is not False:
        raise ValueError("Model replica chưa được nghiệm thu đúng phạm vi")
    for directory, files in model["artifact_trees"].items():
        for name, expected in files.items():
            actual = binding(root, Path(directory) / name)
            if any(actual[k] != expected[k] for k in ("bytes", "sha256")):
                raise ValueError("Component model khác manifest nghiệm thu")
    for name, expected in model["receipts"].items():
        actual = binding(root, name)
        if any(actual[k] != expected[k] for k in ("bytes", "sha256")):
            raise ValueError("Receipt model khác manifest nghiệm thu")
    regime_binding = model["preprocessing"]["regime_models"]
    if binding(root, regime_binding["path"]) != regime_binding:
        raise ValueError("Regime replica khác gói frozen")
    legacy = read(root, "data_manager/regime_model.json", envelope=True)
    if legacy["metadata"]["train_end_date"] != "2022-12-30":
        raise ValueError("Model regime legacy khác cutoff trước evaluation")
    audit = read(root, "outputs/historical_reevaluation/h02_data_r1/execution_audit.json")
    index = binding(root, "outputs/historical_reevaluation/h02_data_r1/VNINDEX_2018_2026_verified_overlap.csv")
    if (not audit["index_ready"] or audit["grid_dates_missing"] or audit["canonical_inputs_modified"]
            or index["sha256"] != audit["index_extended_sha256"]):
        raise ValueError("Lịch VNINDEX chưa khớp audit H02")
    for name in (GRID, DONOR_BANK, MODEL, "data_manager/regime_model.json",
                 "outputs/historical_reevaluation/h02_data_r1/execution_audit.json",
                 "outputs/historical_reevaluation/h02_data_r1/VNINDEX_2018_2026_verified_overlap.csv"):
        sources[str(name).replace("\\", "/")] = binding(root, name)
    result = timeline(root)
    result.update(version="historical_evaluation_inputs_v1", donor_commit=DONOR,
                  source_bindings=sources, telemetry=telemetry(root),
                  response_schemas={"legacy": TradeDecisionOutput.model_json_schema(),
                                    "anchored": wire_schema()["$defs"]["reply"]})
    return result


def save_once(root: Path, name: Path, value: dict[str, Any], *, verify: bool) -> None:
    """Không sửa artifact đã seal; cần protocol revision mới nếu đầu vào thay đổi."""
    path = safe(root, name)
    raw = encode({"payload": value, "sha256": digest(value)})
    if path.exists():
        if path.read_bytes() != raw:
            raise ValueError("Artifact đã khóa khác bản tái dựng: " + name.as_posix())
    elif verify:
        raise ValueError("Thiếu artifact đã khóa: " + name.as_posix())
    else:
        with path.open("xb") as handle:
            handle.write(raw)


def run(root: Path, *, verify: bool = False) -> dict[str, Any]:
    """Tái dựng ngữ nghĩa từ nguồn độc lập; tự băm lại file sửa không vượt guard."""
    inputs = build_inputs(root)
    save_once(root, INPUTS, inputs, verify=verify)
    protocol = contract(root, inputs)
    save_once(root, PROTOCOL, protocol, verify=verify)
    if verify:
        for name in (PROTOCOL, INPUTS):
            anchored = subprocess.check_output(["git", "show", "HEAD:" + name.as_posix()], cwd=root)
            if anchored != safe(root, name).read_bytes():
                raise ValueError("Protocol/input chưa neo Git")
    return protocol
