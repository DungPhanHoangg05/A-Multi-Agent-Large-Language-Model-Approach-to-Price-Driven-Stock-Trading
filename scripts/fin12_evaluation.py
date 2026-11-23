"""Đánh giá paired FIN12 với nhãn thực thi có điều kiện và mẫu số khóa trước."""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date
from math import fsum

import numpy as np
import pandas as pd

from core.finalize_serving_profile import OUTCOME_REASONS, UNAVAILABLE_OUTCOME
from core.finalize_serving_resources import FinalizedResources
from core.finalize_deterministic_bank import OUTPUT as BANK
from core.free_pilot_statistics import account, cycle_ratios
from core.unified_analysis.analysis import classified, prediction_rows
from core.unified_analysis.statistics import CONTRASTS, ENDPOINTS, FOLDS, METHODS, bootstrap, effects, estimates, plain
from core.unified_experiment import validate_outcome
from core.unified_protocol import read
from scripts.fin12_evaluation_oracle import check_account, check_contrasts, check_outcomes

UNAVAILABLE = "UNAVAILABLE_INCOMPLETE_EXECUTION_OUTCOMES"
SENSITIVITY = "NONPRIMARY_COMPLETE_ACCOUNT_INTERSECTION"


def execution_outcomes(points: list[dict], resources: FinalizedResources) -> tuple[dict, dict, dict]:
    """Dùng oracle engine ở đúng t+1/t+3, giữ riêng lý do và ngày lịch nếu NA."""
    frames = {symbol: resources.stock(symbol) for symbol in sorted({p["symbol"] for p in points})}
    calendar = pd.DatetimeIndex(resources.calendar.Datetime)
    outcomes, unavailable = {}, {}
    for point in points:
        identifier = point["id"]
        outcome = resources.outcome(point, frames[point["symbol"]])
        if outcome["version"] != UNAVAILABLE_OUTCOME:
            validate_outcome(point, outcome)
            outcomes[identifier] = outcome
            continue
        if outcome["reason"] not in OUTCOME_REASONS or outcome["reason"] == "OFFLINE_FIXTURE_OUTCOME_LOCKED":
            raise ValueError("Lý do NA ngoài hợp đồng thực thi FIN12")
        unavailable[identifier] = outcome
        boundary = calendar.get_loc(pd.Timestamp(point["cutoff"]))
        dates = calendar[boundary:boundary+4].strftime("%Y-%m-%d").tolist()
        outcomes[identifier] = {**outcome, "dates": dates+[None]*(4-len(dates)),
                                "target": {"label_net": None, "net_return": None}}
    known = {p["id"] for p in resources.acceptance["points"] if not p["economic_label_eligible"]}
    if not known <= unavailable.keys():
        raise ValueError("Nhãn FIN12 vượt qua sàng lọc quyền đã khóa trước thu")
    check_outcomes(points, outcomes, frames, calendar)
    return outcomes, unavailable, frames


def account_tables(rows: list[dict], frames: dict) -> tuple[list[dict], list[dict], list[dict]]:
    """Giữ cả 51 tài khoản trong bảng. Chỉ mở NAV nếu đủ hai chu kỳ hợp lệ."""
    groups = defaultdict(list)
    for row in rows:
        groups[(row["method"], row["symbol"], row["fold"], row["repeat"])].append(row)
    accounts, cycles, daily = [], [], []
    for (method, symbol, fold, repeat), group in sorted(groups.items()):
        if len(group) != 2:
            raise ValueError("Tài khoản FIN12 cần đủ hai dự báo theo lịch")
        key = {"method": method, "symbol": symbol, "fold": fold, "repeat": repeat}
        missing = {r["point_id"]: r["outcome_unavailable_reason"] for r in group if r["r_net"] is None}
        if missing:
            accounts.append({**key, "status": UNAVAILABLE, "missing_points": missing, "return_pct": None,
                             "initial_vnd": 50_000_000., "final_vnd": None})
            continue
        entries = [{k: row[k] for k in ("point_id", "date", "entry_date", "exit_date", "r_net")}
                   | {"action": row["final_action"]} for row in group]
        ledger = account(entries, frames[symbol])
        check_account(entries, frames[symbol], ledger)
        accounts.append({**key, "status": "AVAILABLE", "missing_points": {},
                         **{k: v for k, v in ledger.items() if k not in ("dates", "daily_nav_vnd", "cycles")}})
        cycles.extend({**key, **cycle} for cycle in ledger["cycles"])
        daily.extend({**key, "date": date, "nav_vnd": nav} for date, nav in zip(ledger["dates"], ledger["daily_nav_vnd"]))
    return accounts, cycles, daily


def complete_grid(rows: list[dict], points: list[dict]) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str]]:
    """Mask cả hai chu kỳ của tài khoản có thiếu nhãn, cùng mask cho mọi so sánh."""
    symbols = sorted({point["symbol"] for point in points})
    groups = defaultdict(list)
    for point in points:
        groups[(point["fold"], point["symbol"])].append(point)
    if len(groups) != 51 or any(len(group) != 2 for group in groups.values()):
        raise ValueError("Cohort không đúng 51 tài khoản ghép cặp")
    slots = {p["id"]: (FOLDS.index(fold), symbols.index(symbol), cycle)
             for (fold, symbol), group in groups.items()
             for cycle, p in enumerate(sorted(group, key=lambda p: p["cutoff"]))}
    a = np.zeros((6, len(symbols), 2, 3, len(METHODS)), dtype=bool)
    returns, valid, seen = np.zeros(a.shape[:3]), np.zeros(a.shape[:3], dtype=bool), set()
    for row in rows:
        place = slots[row["point_id"]]
        slot = (*place, row["repeat"], METHODS.index(row["method"]))
        if slot in seen or row["final_action"] not in ("CASH", "LONG"):
            raise ValueError("Slot dự báo trùng hoặc không có hành động hợp lệ")
        seen.add(slot)
        a[slot] = row["final_action"] == "LONG"
        if row["r_net"] is not None:
            returns[place], valid[place] = row["r_net"], True
    if len(seen) != len(points)*3*len(METHODS):
        raise ValueError("Còn slot ACTION chưa hoàn tất")
    valid &= valid.all(axis=2, keepdims=True)
    return a, returns, valid, symbols


def contrast_results(effect: dict, scope: str) -> list[dict]:
    """Ghi chung family 20 contrast và lý do khi band không xác định."""
    rows = []
    for e, endpoint in enumerate(ENDPOINTS):
        for c, (family, method, baseline) in enumerate(CONTRASTS):
            column = e*len(CONTRASTS)+c
            band = effect["ci95"][column] if effect["ci95"] is not None else [None, None]
            rows.append({"scope": scope, "family": family, "method": method, "baseline": baseline,
                         "endpoint": endpoint, "effect_pp": effect["point"][column],
                         "band95_low_pp": band[0], "band95_high_pp": band[1],
                         "band_status": effect["status"], "band_reasons": effect["reasons"]})
    return rows


def method_tables(rows: list[dict], accounts: list[dict], complete_ids: set[str], primary_status: str) -> tuple[list, list, list]:
    """Tách mẫu 102 hành động, nhãn sẵn có và tài khoản hoàn chỉnh trong bảng."""
    summaries, classifications, repeats = [], [], []
    for method in METHODS:
        all_rows = [r for r in rows if r["method"] == method]
        labeled = [r for r in all_rows if r["r_net"] is not None]
        paired = [r for r in labeled if r["point_id"] in complete_ids]
        complete = [row for row in accounts if row["method"] == method and row["status"] == "AVAILABLE"]
        calibration = {}
        for key in ("numeric_probability", "teacher_probability"):
            supported = [r for r in labeled if r.get(key) is not None]
            if any(not 0 <= r[key] <= 1 for r in supported):
                raise ValueError("Xác suất đã ghi ngoài [0,1]")
            calibration[key] = {"n_forecasts": len(supported), "n_points": len({r["point_id"] for r in supported}),
                "brier": fsum((r[key]-(r["label_net"] == "UP"))**2 for r in supported)/len(supported) if supported else None,
                "reason": None if supported else "NO_RECORDED_SUPPORTED_PROBABILITY"}
        for sample, subset in (("AVAILABLE_LABELS", labeled), (SENSITIVITY, paired)):
            for repeat in range(3):
                selected = [r for r in subset if r["repeat"] == repeat]
                classifications.append({"scope": sample, "method": method, "repeat": repeat,
                                        "n_protocol_points": len(all_rows)//3, **classified(selected)})
                for dimension in ("symbol", "fold"):
                    for group in sorted({r[dimension] for r in selected}):
                        classifications.append({"scope": sample, "method": method, "repeat": repeat,
                            "dimension": dimension, "group": group,
                            **classified([r for r in selected if r[dimension] == group])})
        means = []
        for repeat in range(3):
            per_repeat = [r["return_pct"] for r in complete if r["repeat"] == repeat]
            per_repeat_rows = [r for r in paired if r["repeat"] == repeat]
            means.append(fsum(per_repeat)/len(per_repeat))
            repeats.append({"method": method, "repeat": repeat, "scope": SENSITIVITY,
                            "mean_account_return_pct": means[-1],
                            **cycle_ratios([r["r_net"] if r["final_action"] == "LONG" else 0. for r in per_repeat_rows])})
        summaries.append({"method": method, "planned_forecasts": len(all_rows), "labeled_forecasts": len(labeled),
            "planned_accounts_per_repeat": 51, "complete_accounts_per_repeat": len(complete)//3,
            "primary_status": primary_status,
            "long_forecasts": sum(r["final_action"] == "LONG" for r in all_rows),
            "raw_decision_responses": sum(r["llm_response"] for r in all_rows),
            "bypass_forecasts": sum(r["bypass"] for r in all_rows),
            "policy_reasons": dict(Counter(r["reason"] for r in all_rows)),
            "trace_reasons": dict(Counter(str(r.get("trace_reason")) for r in all_rows)),
            "repeat_return_sd_ddof1": float(np.std(means, ddof=1)), "calibration_available_labels": calibration,
            **{"complete_accounts_mean_"+key: fsum(r[key] for r in complete)/len(complete)
               for key in ("daily_mdd_pct", "cycle_end_mdd_pct", "fee_vnd", "slippage_vnd",
                           "turnover_vnd", "turnover_over_initial", "held_session_fraction", "long_count")}})
    return summaries, classifications, repeats


def evaluate(bundle: dict, contract: dict, resources: FinalizedResources) -> tuple[dict, dict]:
    """Dùng chung ledger, confusion, estimand và bootstrap của protocol đã khóa."""
    points = bundle["points"]
    contract_points = contract["domain"]["primary_points"]
    families = [(family, method, contract["families"][family]["baseline"])
                for family in ("system", "method") for method in contract["families"][family]["comparators"]]
    stats = contract["statistics"]
    if (contract_points != [{key: p[key] for key in ("id", "symbol", "cutoff", "fold")} for p in points]
            or contract["method_controls"]["no_llm"] != list(METHODS[-2:]) or families != CONTRASTS
            or (stats["seed"], stats["draws"], stats["block_length"], stats["minimum_joint_finite"])
            != (20261110, 10000, 2, 9500) or stats["fold_order"] != list(FOLDS)
            or stats["endpoints"] != list(ENDPOINTS)):
        raise ValueError("Miền hoặc controls khác protocol FIN02")
    outcomes, unavailable, frames = execution_outcomes(points, resources)
    rows, traces = prediction_rows({**bundle, "outcomes": outcomes})
    exits = {r["episode_id"]: r["exit_date"] for r in read(resources.root, BANK+"bank.json", True)["records"]}
    for row in rows:
        point, method, repeat = row["point_id"], row["method"], row["repeat"]
        slot = f"forecast/{point}/u0/r{repeat}/{method}"
        lineage = bundle["row_provenance"].get(slot, {})
        row.update(lineage, source_price_sha256=outcomes[point]["source_sha256"],
                   outcome_unavailable_reason=unavailable.get(point, {}).get("reason"))
        trace = traces.get(row.get("trace_sha256"), {})
        if "selected_ids" in trace:
            selected = trace["selected_ids"] if not trace["fallback"] else []
            if any(exits[key] >= row["date"] for key in selected):
                raise ValueError("Trace FIN12 có ví dụ chưa đáo hạn theo cutoff")
            ages = [(date.fromisoformat(row["date"])-date.fromisoformat(exits[key])).days for key in selected]
            gate = trace.get("gate") or {}
            row.update(effective_K=len(selected), prior_mean_age_days=fsum(ages)/len(ages) if ages else None,
                       prior_selected_ids=selected, prior_eligible_count=trace["eligible_count"],
                       prior_stats_ready=gate.get("stats_ready"), prior_examples_ready=gate.get("examples_ready"),
                       prior_similarity_reason="NO_SCORES_IN_LOCKED_TRACE" if ages else "NO_EXAMPLES_USED")
    accounts, cycles, daily = account_tables(rows, frames)
    a, r, mask, symbols = complete_grid(rows, points)
    complete_ids = {cycle["point_id"] for cycle in cycles}
    point_return, point_ba = estimates(a, r, mask)
    scope = SENSITIVITY if unavailable else "PRIMARY_REGISTERED_COHORT"
    primary_status = UNAVAILABLE if unavailable else "AVAILABLE"
    summary, classifications, repeats = method_tables(rows, accounts, complete_ids, primary_status)
    for index, method in enumerate(summary):
        method["primary_mean_account_return_pct"] = None if unavailable else float(point_return[0, index])
        method["primary_balanced_accuracy_pct"] = None if unavailable else float(point_ba[0, index])
        method["complete_accounts_mean_account_return_pct"] = float(point_return[0, index])
        method["complete_accounts_balanced_accuracy_pct"] = float(point_ba[0, index])
    effect = bootstrap(a, r, mask)
    oracle = check_contrasts(rows, accounts, complete_ids, point_return[0], point_ba[0], effect)
    primary = effect if not unavailable else {"status": UNAVAILABLE, "reasons": [UNAVAILABLE],
               "point": [None]*20, "ci95": None, "draws": 0, "joint_finite_draws": 0}
    bridges = []
    actions = {(row["point_id"], row["repeat"], row["method"]): row["final_action"] for row in rows}
    for method, baseline in contract["families"]["bridge"]["contrasts"]:
        i, j = METHODS.index(method), METHODS.index(baseline)
        bridges.append({"method": method, "baseline": baseline, "scope": scope,
                        "return_difference_pp": float(point_return[0, i]-point_return[0, j]),
                        "BA_difference_pp": float(point_ba[0, i]-point_ba[0, j]),
                        "same_action_forecasts": sum(actions[p["id"], repeat, method] == actions[p["id"], repeat, baseline]
                                                     for p in points for repeat in range(3)),
                        "matched_action_denominator": len(points)*3})
    core = np.array([symbol in contract["domain"]["secondary_core4"] for symbol in symbols])
    core_mask = mask & core[None, :, None]
    sensitivity = {"scope": scope, "complete_account_intersection": effect,
        "BLOCK_LENGTH_1": bootstrap(a, r, mask, 1), "BLOCK_LENGTH_3": bootstrap(a, r, mask, 3),
        "LEAVE_ONE_FOLD_OUT": {fold: effects(*estimates(a, r, mask, np.delete(np.arange(6), i)[None, :]))[0]
                               for i, fold in enumerate(FOLDS)},
        "LEAVE_ONE_SYMBOL_OUT": {symbol: effects(*estimates(a, r, mask & (np.arange(len(symbols)) != i)[None, :, None]))[0]
                                 for i, symbol in enumerate(symbols)},
        "CORE4_FIXED_SUBSET": {"points": int(core_mask.sum()), "accounts": int(core_mask.sum())//2,
                               **bootstrap(a, r, core_mask)}}
    coverage = {"planned_points": len(points), "forecast_slots": len(bundle["records"]),
                "available_outcomes": len(points)-len(unavailable), "unavailable_outcomes": unavailable,
                "planned_accounts_per_repeat": 51, "complete_accounts_per_repeat": int(mask.sum())//2,
                "complete_account_points": int(mask.sum()), "outcomes_opened_after_forecast_barrier": True}
    result = {"version": "finalize_study_evaluation_v1", "status": "FIN12_EVALUATED_OFFLINE",
              "input_identity": bundle["input_identity"], "coverage": coverage, "oracle": oracle,
              "scope": contract["statistics"]["scope"], "primary_joint_family": primary, "summary": summary,
              "primary_contrasts": contrast_results(primary, "PRIMARY_REGISTERED_COHORT"),
              "complete_account_contrasts": contrast_results(effect, scope), "bridge": bridges,
              "sensitivity": sensitivity, "method_controls": contract["method_controls"],
              "independent_price_pit_certified": resources.acceptance["independent_price_pit_certified"],
              "new_api_calls": 0}
    tables = {"predictions": rows, "outcomes": outcomes, "accounts": accounts, "cycles": cycles, "daily_nav": daily,
              "classification": classifications, "per_repeat": repeats, "prior_traces": traces}
    return plain(result), plain(tables)
