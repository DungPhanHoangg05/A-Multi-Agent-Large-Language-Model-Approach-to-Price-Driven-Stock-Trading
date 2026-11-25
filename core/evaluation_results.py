"""Chỉ tiêu theo giao thức và báo cáo ghép cặp giữa cấu hình."""
from __future__ import annotations

from collections import defaultdict
from hashlib import sha256
import json
from statistics import mean
from typing import Any

from core.evaluation_bicl import HISTORY
from core.finalize_serving_resources import FinalizedResources
from core.free_pilot_statistics import account
from core.unified_analysis.analysis import analyze, classified, prediction_rows
from core.unified_contracts import digest
from core.unified_experiment import outcome_from_frame, validate_outcome
from core.unified_preflight_assets import PROTOCOL_V2
from core.unified_protocol import git_blob
from scripts.fin12_evaluation import evaluate


def outcomes(points: list[dict], frames: dict, sources: dict[str, str]) -> dict:
    """Tính nhãn và giá T+2.5 sau khi collector đã chốt toàn bộ dự báo."""
    result = {}
    for point in points:
        symbol = point["symbol"]
        outcome = outcome_from_frame(point, frames[symbol], sources[symbol])
        validate_outcome(point, outcome)
        result[point["id"]] = outcome
    return result


def summarize(rows: list[dict], frames: dict, *, complete: set[str] | None = None) -> list[dict]:
    """Tính BA riêng từng execution, lợi nhuận trên từng tài khoản mã/fold."""
    groups = defaultdict(list)
    for row in rows:
        groups[row["panel"], row["method"]].append(row)
    results = []
    for (panel, method), selected in sorted(groups.items()):
        supported = [row for row in selected if complete is None or row["point_id"] in complete]
        executions, accounts = defaultdict(list), defaultdict(list)
        for row in supported:
            execution = row["realization"] if panel == "upstream" else row["repeat"]
            executions[execution].append(row)
            accounts[execution, row["symbol"], row["fold"]].append(row)
        metrics = [classified(group)["balanced_accuracy"] for group in executions.values()]
        profits = [account([{**row, "action": row["final_action"]} for row in group], frames[symbol])["return_pct"]
                   for (_, symbol, _), group in accounts.items()]
        results.append({"panel": panel, "method": method, "forecasts": len(selected),
                        "supported_forecasts": len(supported), "accounts": len(profits),
                        "balanced_accuracy_pct": mean(metrics)*100 if metrics and None not in metrics else None,
                        "mean_account_return_pct": mean(profits) if profits else None,
                        "long_forecasts": sum(row["final_action"] == "LONG" for row in selected),
                        "fallbacks": sum(row["fallback"] for row in selected)})
    return results


def component_results(study: Any, points: list[dict], collected: list[dict], frames: dict) -> tuple[dict, list[dict]]:
    """Đo panel chính, upstream và factorial trên support đã khóa."""
    from core.causal_alpha import frame_document
    selected_outcomes = outcomes(points, frames, {symbol: digest(frame_document(frame)) for symbol, frame in frames.items()})
    rows = [row for value in collected for row in value["rows"]] + study.controls(points)
    predictions = []
    for row in rows:
        outcome = selected_outcomes[row["id"]]
        label = outcome["target"]["label_net"]
        if row.get("label_net", label) != label:
            raise ValueError("Nhãn đối chứng thành phần lệch hợp đồng kinh tế")
        predictions.append({**row, "point_id": row["id"], "date": row["cutoff"], "entry_date": outcome["dates"][1],
                            "exit_date": outcome["dates"][3], "label_net": label, "r_net": outcome["target"]["net_return"]})
    return {"metrics": summarize(predictions, frames), "outcome_sha256": digest(selected_outcomes)}, predictions


def bicl_results(study: Any, points: list[dict], market: dict | FinalizedResources, collected: list[dict],
                 identity: dict, *, sample: bool, http: list[dict]) -> tuple[dict, list[dict]]:
    """Dùng evaluator FIN12/U09 đầy đủ và giữ chế độ mẫu là đo chi phí."""
    from scripts.fin12_evaluation import execution_outcomes

    bundle = {"points": points, "records": [row for value in collected for row in value["records"]],
              "prepared": {k: v for value in collected for k, v in value["prepared"].items()},
              "row_provenance": {}, "input_identity": identity}
    details = None
    if study.followup:
        if not sample:
            details, tables = evaluate(bundle, study.contract, market)
            rows = tables["predictions"]
            metrics = [{"panel": "main", "method": row["method"],
                        "balanced_accuracy_pct": row["primary_balanced_accuracy_pct"],
                        "mean_account_return_pct": row["primary_mean_account_return_pct"],
                        "complete_accounts_balanced_accuracy_pct": row["complete_accounts_balanced_accuracy_pct"],
                        "complete_accounts_mean_account_return_pct": row["complete_accounts_mean_account_return_pct"]}
                       for row in details["summary"]]
            outcome_sha256 = digest(tables["outcomes"])
        else:
            result, unavailable, frames = execution_outcomes(points, market)
            rows, _ = prediction_rows({**bundle, "outcomes": result})
            outcome_sha256 = digest(result)
            complete = {p["id"] for p in points if p["id"] not in unavailable}
    else:
        from core.causal_alpha import frame_document
        frames = market
        result = outcomes(points, frames, {symbol: digest(frame_document(frame)) for symbol, frame in frames.items()})
        outcome_sha256 = digest(result)
        complete = None
        if sample:
            rows, _ = prediction_rows({**bundle, "outcomes": result})
        else:
            protocol = git_blob(study.root, HISTORY, PROTOCOL_V2)
            bundle.update(outcomes=result, protocol=json.loads(protocol), http=http, retired=[],
                          input_identity={**identity, "analysis_protocol_sha256": sha256(protocol).hexdigest()},
                          proof={"limitations": ["PROVIDER_EVALUATION_ON_HISTORICAL_EXPOSED_COHORT"]})
            details, tables = analyze(bundle, frames)
            rows = tables["predictions"]
            metrics = [{"panel": "main", **{key: row[key] for key in
                        ("method", "balanced_accuracy_pct", "mean_account_return_pct")}} for row in details["summary"]]
    predictions = [{**row, "panel": "main",
                    "fallback": row["reason"] in ("FALLBACK_ORIGINAL", "ANCHOR_INVALID_USE_ORIGINAL")
                    or (row["bypass"] and row["reason"] != "REGISTERED_NO_LLM_CONTROL"),
                    "action_changed_from_anchor": (row.get("anchor_action") in ("LONG", "CASH")
                                                   and row["anchor_action"] != row["final_action"])}
                   for row in rows]
    if sample:
        metrics = summarize(predictions, frames, complete=complete)
    else:
        for metric in metrics:
            selected = [r for r in predictions if r["method"] == metric["method"]]
            metric.update(forecasts=len(selected), fallbacks=sum(r["fallback"] for r in selected),
                          long_forecasts=sum(r["final_action"] == "LONG" for r in selected),
                          action_changes_from_anchor=sum(r["action_changed_from_anchor"] for r in selected))
    return {"metrics": metrics, "outcome_sha256": outcome_sha256, "protocol_analysis": details}, predictions


def compare(groq: dict, luna: dict, groq_rows: list[dict], luna_rows: list[dict]) -> dict:
    """Đối chiếu từng slot trước khi tính delta BA, P&L và hai chiều LONG/CASH."""
    def index(rows: list[dict]) -> dict:
        result = {(row["panel"], row["method"], row["point_id"], row["repeat"], row["realization"]): row for row in rows}
        if len(result) != len(rows):
            raise ValueError("Có khóa dự báo ghép cặp bị trùng")
        return result

    def difference(left: dict, right: dict, key: str) -> float | None:
        return right[key] - left[key] if left.get(key) is not None and right.get(key) is not None else None

    left, right = index(groq_rows), index(luna_rows)
    if (groq["outcome_sha256"] != luna["outcome_sha256"] or left.keys() != right.keys()
            or any(left[key]["label_net"] != right[key]["label_net"] for key in left)):
        raise ValueError("Hai cấu hình khác mẫu, nhãn hoặc slot thực nghiệm")
    shifts = defaultdict(list)
    for key in left:
        shifts[key[:2]].append((left[key]["final_action"], right[key]["final_action"]))
    luna_metrics = {(row["panel"], row["method"]): row for row in luna["metrics"]}
    rows = []
    for g in groq["metrics"]:
        key = (g["panel"], g["method"])
        l, actions = luna_metrics[key], shifts[key]
        row = {"panel": key[0], "method": key[1], "matched_forecasts": len(actions),
               "groq_long_to_luna_cash": actions.count(("LONG", "CASH")),
               "groq_cash_to_luna_long": actions.count(("CASH", "LONG")),
               "groq_fallbacks": g["fallbacks"], "luna_fallbacks": l["fallbacks"]}
        for name in ("balanced_accuracy_pct", "mean_account_return_pct", "complete_accounts_balanced_accuracy_pct",
                     "complete_accounts_mean_account_return_pct"):
            if name in g:
                row.update({"groq_" + name: g[name], "luna_" + name: l[name],
                            "luna_minus_groq_" + name: difference(g, l, name)})
        rows.append(row)
    return {"comparison": rows, "usage": {"groq": groq["usage"], "luna": luna["usage"]}}
