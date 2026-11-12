"""Bảng tài khoản, confusion, coverage, bridge và sensitivity từ forecast đã seal."""
from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

import numpy as np
import pandas as pd

from core.free_pilot_statistics import account, classification, cycle_ratios
from core.unified_contracts import digest
from core.unified_analysis.statistics import (METHODS, VARIANTS, FOLDS, CONTRASTS, ENDPOINTS,
    bootstrap, estimates, effects, plain)


def classified(rows: list[dict]) -> dict[str, Any]:
    """Confusion giữ mẫu số UP/DOWN; F1/BA không xác định giữ null và lý do."""
    p = [r["final_action"] == "LONG" for r in rows]
    y = [r["label_net"] == "UP" for r in rows]
    result = classification(p, y, planned=len(rows))
    negative = classification([not v for v in p], [not v for v in y])["f1_positive"]
    result.update(f1_negative=negative,
        macro_f1=(negative + result["f1_positive"]) / 2. if negative is not None and result["f1_positive"] is not None else None,
        long_rate=float(np.mean(p)) if p else None,
        )
    result["undefined_reasons"] = {key: "ZERO_DENOMINATOR_OR_MISSING_CLASS" for key, value in result.items() if value is None}
    return result


def prediction_rows(bundle: dict) -> tuple[list[dict], dict]:
    """Không gọi provider hoặc policy mới; tách proposal/veto/final từ record active."""
    points = {p["id"]: p for p in bundle["points"]}
    rows, traces = [], {}
    for record in bundle["records"]:
        forecast, policy = record["forecast"], record["policy"]
        point = points[forecast["point_id"]]; outcome = bundle["outcomes"][point["id"]]
        slot = f"forecast/{point['id']}/u0/r{forecast['repeat']}/{forecast['variant']}"
        prepared = bundle["prepared"][slot]; trace = prepared["trace"]; aux = prepared["aux"]
        trace_sha = digest(trace); traces[trace_sha] = trace
        branch = aux.get("branch", {}); utility = branch.get("utility", {})
        numeric_probability = branch.get("probability")
        metadata = trace.get("retrieval", {}).get("metadata", {})
        selected = trace.get("retrieval", {}).get("tasks", [])
        ages = [(pd.Timestamp(point["cutoff"]) - pd.Timestamp(task["exit_date"])).days for task in selected]
        scores = [v["score"] for v in metadata.get("selected_scores", [])]
        raw = forecast["raw"]
        wire = policy.get("wire", {})
        rows.append({"point_id": point["id"], "symbol": point["symbol"], "fold": point["fold"],
            "date": point["cutoff"], "entry_date": outcome["dates"][1], "exit_date": outcome["dates"][3],
            "method": forecast["variant"], "repeat": forecast["repeat"], "realization": 0,
            "label_net": outcome["target"]["label_net"], "r_net": outcome["target"]["net_return"],
            "raw_proposal": policy["raw_proposal"], "final_action": policy["final_action"],
            "reason": policy["reason"], "bypass": policy["bypass"], "llm_response": raw is not None,
            "source_request_id": raw["source_request_id"] if raw else None,
            "shared_sha256": forecast["shared_sha256"], "profile": forecast["profile"],
            "trace_sha256": trace_sha, "trace_reason": trace.get("reason"),
            "anchor_action": wire.get("anchor_action"), "eligible": wire.get("eligible"),
            "fact_assertions_valid": wire.get("fact_assertions_valid"),
            "numeric_probability": numeric_probability, "teacher_probability": utility.get("posterior_mean_theta"),
            "utility_q10": utility.get("q10_U_net_fraction"), "utility_q90": utility.get("q90_U_net_fraction"),
            "effective_K": metadata.get("selected_count", utility.get("K")),
            "prior_mean_age_days": float(np.mean(ages)) if ages else None,
            "prior_mean_similarity": float(np.mean(scores)) if scores else None,
            "prior_regret": None, "prior_regret_reason": "NOT_RECORDED_IN_LOCKED_TRACE"})
    for method, action in ((METHODS[-2], "CASH"), (METHODS[-1], "LONG")):
        for point in bundle["points"]:
            outcome = bundle["outcomes"][point["id"]]
            for repeat in range(3):
                rows.append({"point_id": point["id"], "symbol": point["symbol"], "fold": point["fold"],
                    "date": point["cutoff"], "entry_date": outcome["dates"][1], "exit_date": outcome["dates"][3],
                    "method": method, "repeat": repeat, "realization": 0, "raw_proposal": None,
                    "label_net": outcome["target"]["label_net"], "r_net": outcome["target"]["net_return"],
                    "final_action": action, "reason": "REGISTERED_NO_LLM_CONTROL", "bypass": True,
                    "llm_response": False, "numeric_probability": None, "teacher_probability": None})
    return rows, traces


def tensor(rows: list[dict], points: list[dict]) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str]]:
    """BHN chỉ có ba fold sau; padding không trở thành CASH hoặc account giả."""
    symbols = sorted({p["symbol"] for p in points})
    groups = defaultdict(list)
    for point in points: groups[(point["fold"], point["symbol"])].append(point)
    if len(groups) != 51 or any(len(v) != 2 for v in groups.values()): raise ValueError("Phải đủ 51 account, mỗi account hai query")
    slots = {}
    for (fold, symbol), group in groups.items():
        for cycle, point in enumerate(sorted(group, key=lambda p: p["cutoff"])):
            slots[point["id"]] = (FOLDS.index(fold), symbols.index(symbol), cycle)
    a = np.zeros((6, len(symbols), 2, 3, len(METHODS)), dtype=bool)
    r = np.zeros(a.shape[:3], dtype=float); valid = np.zeros(r.shape, dtype=bool)
    seen = set()
    for row in rows:
        f, s, c = slots[row["point_id"]]; repeat = row["repeat"]; m = METHODS.index(row["method"])
        key = (f, s, c, repeat, m)
        if key in seen or row["final_action"] not in ("LONG", "CASH"): raise ValueError("Trùng slot hoặc action lỗi")
        if valid[f, s, c] and r[f, s, c] != row["r_net"]: raise ValueError("Nhãn khác giữa method/repeat")
        if bool(row["r_net"] > 0) != (row["label_net"] == "UP"): raise ValueError("Nhãn khác net return")
        seen.add(key); a[key] = row["final_action"] == "LONG"; r[f, s, c] = row["r_net"]; valid[f, s, c] = True
    if len(seen) != 102 * 3 * len(METHODS): raise ValueError("Thiếu support theo method/repeat")
    return a, r, valid, symbols


def analyze(bundle: dict, prices: dict[str, pd.DataFrame]) -> tuple[dict, dict[str, list[dict]]]:
    """Tính một lần trên tensor/ledger; outputs không chứa lựa chọn subgroup theo outcome."""
    rows, traces = prediction_rows(bundle)
    groups = defaultdict(list)
    for row in rows: groups[(row["method"], row["symbol"], row["fold"], row["repeat"])].append(row)
    accounts, daily, cycles = [], [], []
    for (method, symbol, fold, repeat), group in sorted(groups.items()):
        ledger = account([{**row, "action": row["final_action"]} for row in group], prices[symbol])
        key = {"method": method, "symbol": symbol, "fold": fold, "repeat": repeat}
        ratios = {name: "ZERO_DENOMINATOR" for name in ("cycle_sharpe", "cycle_sortino_lpm2") if ledger[name] is None}
        accounts.append({**key, **{k: v for k, v in ledger.items() if k not in ("dates", "daily_nav_vnd", "cycles")},
            "undefined_reasons": ratios})
        daily.extend({**key, "date": date, "nav_vnd": nav} for date, nav in zip(ledger["dates"], ledger["daily_nav_vnd"]))
        cycles.extend({**key, **cycle} for cycle in ledger["cycles"])
    a, r, valid, symbols = tensor(rows, bundle["points"])
    point_return, point_ba = estimates(a, r, valid)
    classifications, stratified, summary, per_repeat = [], [], [], []
    for m, method in enumerate(METHODS):
        selected = [row for row in rows if row["method"] == method]
        metrics = []
        for repeat in range(3):
            subset = [row for row in selected if row["repeat"] == repeat]
            metric = classified(subset); metrics.append(metric)
            classifications.append({"method": method, "repeat": repeat, **metric})
            acc = [v for v in accounts if v["method"] == method and v["repeat"] == repeat]
            per_repeat.append({"method": method, "repeat": repeat, "mean_account_return_pct": float(np.mean([v["return_pct"] for v in acc])),
                "balanced_accuracy_pct": metric["balanced_accuracy"] * 100. if metric["balanced_accuracy"] is not None else None,
                **cycle_ratios([v["r_net"] if v["final_action"] == "LONG" else 0. for v in subset])})
            for dimension in ("symbol", "fold"):
                for value in sorted({row[dimension] for row in subset}):
                    stratified.append({"method": method, "repeat": repeat, "dimension": dimension, "group": value,
                        **classified([row for row in subset if row[dimension] == value])})
        acc = [v for v in accounts if v["method"] == method]
        mean_return = float(np.mean([v["return_pct"] for v in acc]))
        if not np.isclose(mean_return, point_return[0, m], rtol=0, atol=1e-10): raise ValueError("Tensor/ledger primary return lệch")
        def average(field: str) -> float | None:
            values = [v[field] for v in metrics]
            return float(np.mean(values)) if all(v is not None for v in values) else None
        calibration = {}
        for field in ("numeric_probability", "teacher_probability"):
            supported = [v for v in selected if v.get(field) is not None]
            if any(not 0. <= v[field] <= 1. for v in supported): raise ValueError("Numeric probability ngoài [0,1]")
            calibration[field] = {"n_forecasts": len(supported), "n_unique_points": len({v["point_id"] for v in supported}),
                "brier_supported_only": float(np.mean([(v[field] - (v["label_net"] == "UP"))**2 for v in supported])) if supported else None,
                "reason": "ELIGIBLE_NUMERIC_TARGET_ONLY_NO_LLM_CONFIDENCE_MAPPING" if supported else "NO_RECORDED_SUPPORTED_PROBABILITY"}
        summary.append({"method": method, "n_points": 102, "n_forecasts": len(selected), "n_accounts_per_repeat": len(acc)//3,
            "mean_account_return_pct": mean_return, "balanced_accuracy_pct": float(point_ba[0, m]),
            **{key: average(key) for key in ("accuracy", "mcc", "f1_positive", "f1_negative", "macro_f1", "long_rate")},
            "mean_daily_mdd_pct": float(np.mean([v["daily_mdd_pct"] for v in acc])),
            "worst_account_daily_mdd_pct": float(max(v["daily_mdd_pct"] for v in acc)),
            "mean_cycle_end_mdd_pct": float(np.mean([v["cycle_end_mdd_pct"] for v in acc])),
            **{"mean_" + key: float(np.mean([v[key] for v in acc])) for key in ("fee_vnd", "slippage_vnd", "turnover_vnd", "turnover_over_initial", "held_session_fraction")},
            "long_forecasts": sum(v["final_action"] == "LONG" for v in selected),
            "bypass_forecasts": sum(v["bypass"] for v in selected), "raw_decision_responses": sum(v["llm_response"] for v in selected),
            "policy_reasons": dict(Counter(v["reason"] for v in selected)),
            "trace_reasons": dict(Counter(str(v.get("trace_reason")) for v in selected)),
            "repeat_return_sd_ddof1": float(np.std([v["mean_account_return_pct"] for v in per_repeat if v["method"] == method], ddof=1)),
            "calibration": calibration, "annualized_metrics": None})
    primary = bootstrap(a, r, valid)
    contrast_rows = []
    for e, endpoint in enumerate(ENDPOINTS):
        for c, (family, method, baseline) in enumerate(CONTRASTS):
            column = e * 10 + c
            ci = primary["ci95"][column] if primary["ci95"] is not None else None
            contrast_rows.append({"family": family, "method": method, "baseline": baseline, "endpoint": endpoint,
                "effect_pp": primary["point"][column], "band95_low_pp": ci[0] if ci else None,
                "band95_high_pp": ci[1] if ci else None, "band_status": primary["status"], "band_reasons": primary["reasons"]})
    bridge = []
    for left, right in bundle["protocol"]["families"]["bridge"]["contrasts"]:
        i, j = METHODS.index(left), METHODS.index(right)
        bridge.append({"method": left, "baseline": right, "return_difference_pp": float(point_return[0, i] - point_return[0, j]),
            "BA_difference_pp": float(point_ba[0, i] - point_ba[0, j]),
            "same_action_forecasts": int(np.sum((a[..., i] == a[..., j]) & valid[..., None])),
            "n_forecasts": 306, "inference": "DESCRIPTIVE_NO_SUPERIORITY_CLAIM"})
    sensitivity = {"BLOCK_LENGTH_1": bootstrap(a, r, valid, 1), "BLOCK_LENGTH_3": bootstrap(a, r, valid, 3)}
    sensitivity["LEAVE_ONE_FOLD_OUT"] = {fold: plain(effects(*estimates(a, r, valid, np.delete(np.arange(6), i)[None, :]))[0]) for i, fold in enumerate(FOLDS)}
    sensitivity["LEAVE_ONE_SYMBOL_OUT"] = {}
    for i, symbol in enumerate(symbols):
        mask = valid.copy(); mask[:, i] = False
        sensitivity["LEAVE_ONE_SYMBOL_OUT"][symbol] = plain(effects(*estimates(a, r, mask))[0])
    mask = valid.copy()
    for i, symbol in enumerate(symbols):
        if symbol not in bundle["protocol"]["cohort"]["secondary_core4"]: mask[:, i] = False
    sensitivity["CORE4_FIXED_SUBSET"] = {"points": int(mask.sum()), "accounts": int(mask[:, :, 0].sum()), **bootstrap(a, r, mask)}
    result = {"version": "unified_analysis_v1", "status": "PASS_U09_ANALYSIS", "input_identity": bundle["input_identity"],
        "scope": bundle["protocol"]["statistics"]["scope"], "points": 102, "repeats": 3, "accounts_per_repeat": 51,
        "summary": summary, "classification_by_repeat": classifications, "classification_by_group": stratified,
        "per_repeat": per_repeat, "primary_joint_family": primary, "contrasts": contrast_rows, "bridge": bridge,
        "sensitivity": sensitivity, "coverage": {"planned": 2448, "complete": 2448, "failed_active": 0,
            "input_excluded": 0, "source_raw_http_retired": len(bundle["retired"]), "missing_action_bounds": "NOT_REQUIRED_COMPLETE_COHORT"},
        "telemetry": {"http_attempts": len(bundle["http"]), "status_all": dict(Counter(str(v["status"]) for v in bundle["http"])),
            "observed_total_tokens": sum(v.get("total_tokens") or 0 for v in bundle["http"]),
            "unknown_reserve_tokens": sum(v["reserved_tokens"] for v in bundle["http"] if v["status"] == "UNKNOWN"),
            "new_api_calls": 0}, "deferred_panels": bundle["protocol"]["controls"],
        "definitions": {"return": "EQUAL_MEAN_51_SYMBOL_FOLD_ACCOUNTS_AFTER_MEAN_3_REPEAT_ACCOUNTS_NOT_PORTFOLIO",
            "BA": "MEAN_3_PER_REPEAT_POOLED_102_POINT_BALANCED_ACCURACIES",
            "MDD": "FULL_EOD_NAV_FROM_QUERY_TO_LAST_EXIT_WITH_INITIAL_CAPITAL",
            "ratios": bundle["protocol"]["metrics"]["ratios"], "classification_mean": "PER_REPEAT_METRICS_AVERAGED_NOT_POOLED_306_AS_INDEPENDENT"},
        "limitations": bundle["proof"]["limitations"] + ["ONLY_SIX_EXPOSED_TEMPORAL_CLUSTERS", "BHN_ONLY_LAST_THREE_FOLDS", "EXECUTION_VENDOR_DATA_NOT_LIVE_FILL_ACCEPTANCE"]}
    artifacts = {"predictions": rows, "accounts": accounts, "daily_nav": daily, "cycles": cycles,
        "prior_traces": [{"sha256": key, "trace": value} for key, value in sorted(traces.items())]}
    return plain(result), plain(artifacts)
