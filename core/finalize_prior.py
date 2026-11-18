"""Retrieval FIN07 trên khóa OHLCV; giữ gate, công thức và đơn vị lịch sử."""
from __future__ import annotations

from copy import deepcopy
from datetime import date
import math
from typing import Any

import pandas as pd

from core.bayesian_retriever import PREFIX_METRICS, _format_net_return
from core.finalize_ohlcv_keys import PATTERN, PROFILE, TREND, key_at
from core.historical_signals import report_signal
from core.prior_conditional_statistics import conditional_metric
from core.prior_example_selection import DEFAULT_CONFIG, PriceExampleSelector, _select_trace
from core.prior_quality_gate import SPLIT_GATE, _content_views, _readiness
from core.unified_contracts import digest, forecast_only
from core.unified_protocol import CORE4

VARIANTS = ("bayesian_v1", "C2", "A_tp_pool", "B_semantic")
FIELDS = (TREND, PATTERN, "alpha_consensus", "indicator_consensus")
DIRECTIONS = {"BULLISH": "+", "BEARISH": "-", "NEUTRAL": "0"}
LABELS = ("Win", "Trap", "TrendFail", "PatternFail")


def signals(key: dict, alpha: str | None, indicator: str) -> dict:
    """Giữ NA gốc và chỉ nhận bốn chiều đúng namespace của FIN06."""
    if key["profile"] != PROFILE or indicator not in DIRECTIONS or (alpha is not None and alpha not in DIRECTIONS):
        raise ValueError("Sai profile hoặc hướng khóa FIN07")
    if (key["reason"] is None and any(key[k] not in DIRECTIONS for k in (TREND, PATTERN))
            or key["reason"] is not None and any(key[k] is not None for k in (TREND, PATTERN))):
        raise ValueError("Hướng T/P sai trạng thái sẵn sàng")
    return {TREND: key[TREND], PATTERN: key[PATTERN], "alpha_consensus": alpha, "indicator_consensus": indicator}


def query_signals(key: dict, shared: dict) -> dict:
    """Lấy Alpha/Indicator từ upstream chung; báo cáo thị giác không tham gia so khớp."""
    factors = shared["alpha_factors"]
    if len(factors) != 5 or any(r["signal"] not in ("TĂNG", "GIẢM", "TRUNG TÍNH") for r in factors):
        raise ValueError("Retrieval cần đúng năm Alpha causal")
    votes = [r["signal"] for r in factors]
    delta = votes.count("TĂNG") - votes.count("GIẢM")
    alpha = "BULLISH" if delta > 0 else "BEARISH" if delta < 0 else "NEUTRAL"
    indicator = report_signal(shared["indicator_report"], ("Đồng thuận chủ đạo", "Dominant consensus"))
    return signals(key, alpha, indicator)


def statistics(rows: list[dict]) -> dict:
    """Đếm win trên P và false-bullish trên từng tập phát tín hiệu; giữ 0/0 là NA."""
    pairs = [[0, 0] for _ in PREFIX_METRICS]
    for row in rows:
        trend = row["retrieval_key"][TREND] == "BULLISH"
        pattern = row["retrieval_key"][PATTERN] == "BULLISH"
        win = row["y"] == 1
        observed = (True, trend or pattern, trend, pattern)
        success = (win, not win, not win, not win)
        for pair, present, hit in zip(pairs, observed, success):
            pair[0] += int(present and hit)
            pair[1] += int(present)
    return {k: {"numerator": wins, "denominator": count, "rate": wins / count if count else None}
            for k, (wins, count) in zip(PREFIX_METRICS, pairs)}


def conditional(population: list[dict], query: dict, fields: tuple[str, ...]) -> dict:
    """P/C/B cùng cohort; chỉ C dùng likelihood, A phân hoạch T/P."""
    groups: dict[str, list[dict]] = {"population": population, "conditional": [], "background": []}
    for row in population:
        prior = signals(row["retrieval_key"], row["alpha_consensus"], row["indicator_consensus"])
        name = "conditional" if all(prior[k] == query[k] for k in fields) else "background"
        groups[name].append(row)
    raw = {name: statistics(rows) for name, rows in groups.items()}
    return {"fields": list(fields), "groups": {name: [r["episode_id"] for r in rows] for name, rows in groups.items()},
            "metrics": {key: conditional_metric(key, raw["conditional"][key]["numerator"],
                raw["conditional"][key]["denominator"], raw["background"][key]["numerator"],
                raw["background"][key]["denominator"]) for key in PREFIX_METRICS}}


def render(branch: str, regime: str, population_count: int, tasks: list[dict], counts: dict,
           condition: dict | None, visible: list[str]) -> str:
    """Hiển thị riêng T/P OHLCV, mẫu số, NA và ví dụ; kiểm trần trước transport."""
    style = {"bayesian_v1": "v1", "C2": "v3", "A_tp_pool": "v3 TP", "B_semantic": "v4"}[branch]
    header = f"[BRPP OHLCV {style}] R={regime}; n={population_count}; k={len(tasks)}"
    lines = [header]
    if condition is None:
        lines.append("; ".join(f"{label}={item['numerator']}/{item['denominator']}" +
            (f"({item['rate']:.1%})" if item["rate"] is not None else "(NA)")
            for label, item in zip(LABELS, counts.values())))
    elif visible:
        lines[0] += f"; nC={len(condition['groups']['conditional'])}"
        values = []
        for label, key in zip(LABELS, PREFIX_METRICS):
            item = condition["metrics"][key]
            count, interval = item["raw_counts"]["conditional"], item["credible_interval"]
            value = "NA" if key not in visible else (f"{count['success_count']}/{count['support_count']}→"
                f"{item['posterior_mean']:.2f}[{interval['lower']:.2f},{interval['upper']:.2f}]")
            values.append(f"{label}={value}")
        lines.extend(("; ".join(values), "C=khớp " + ("T/P" if branch == "A_tp_pool" else "T/P/A/I") +
                      "; mean[CrI95%] là tỷ lệ lịch sử."))
    lines.append("T/P theo OHLCV; +/-/0=tăng/giảm/trung tính; W/L=LONG ròng lịch sử; SHORT=CASH.")
    if branch == "B_semantic" and visible:
        lines.append("Win=LONG ròng dương; Trap/Sai tăng=LONG ròng không dương khi phát tín hiệu tăng.")
    for row in tasks:
        values = signals(row["retrieval_key"], row["alpha_consensus"], row["indicator_consensus"])
        codes = "".join(DIRECTIONS[values[k]] for k in FIELDS)
        lines.append(f"{row['episode_id']} T/P/A/I={codes} {'W' if row['y'] else 'L'} {_format_net_return(row['r_net'] * 100)}")
    prefix = "\n".join(lines)
    if len(prefix) > 600:
        raise ValueError("BRPP OHLCV vượt 600 ký tự")
    return prefix


class FinalizedPrior:
    """Bank đã đối soát từ manifest FIN06, chỉ đọc nhãn sau lọc membership nghiêm ngặt."""
    def __init__(self, rows: list[dict], points: dict[str, dict], selector: PriceExampleSelector, decision: dict,
                 bank_sha256: str, calendar: pd.DatetimeIndex) -> None:
        self.rows, self.points, self.selector = rows, points, selector
        self.decision, self.bank_sha256 = decision, bank_sha256
        self.calendar = calendar

    def select(self, rows: list[dict], query: dict, point: dict) -> tuple[list[dict], dict]:
        """Dùng scaler FIN06, công thức base và policy tuổi/khoảng cách phiên đã khóa."""
        symbol, cutoff, fold = (point[k] for k in ("symbol", "cutoff", "fold"))
        index = self.selector.index
        transformed = index.transform_query(symbol, cutoff, point["feature"], fold_id=fold)
        by_id = {r["episode_id"]: r for r in rows}
        metadata = {"query_feature_status": transformed["feature_status"], "scaler_status": transformed["scaler_status"],
                    "index_sha256": index.identity, "scaler_sha256": transformed["scaler_sha256"], "selected_ids": []}
        if transformed["status"] != "AVAILABLE":
            return [], metadata
        prior = index.prior_features(symbol, cutoff, list(by_id), fold_id=fold)
        trace = []
        for item in prior:
            key = item["episode_id"]
            row = by_id[key]
            record = {k: row[k] for k in ("episode_id", "as_of_date", "exit_date")}
            if item["status"] != "AVAILABLE":
                trace.append({**record, "status": "UNAVAILABLE", "reason_codes": item["feature_reasons"]})
                continue
            values = signals(row["retrieval_key"], row["alpha_consensus"], row["indicator_consensus"])
            matches = sum(values[k] == query[k] for k in FIELDS) / len(FIELDS)
            distance = math.sqrt(math.fsum((a - b) ** 2 for a, b in
                                           zip(transformed["scaled_vector"], item["scaled_vector"])) / 4)
            trace.append({**record, "status": "SCORED", "base_score": .5 * matches + .5 / (1 + distance)})
        ranked, _, selected = _select_trace(trace, self.selector, cutoff, DEFAULT_CONFIG)
        metadata.update(selected_ids=selected, ranking_sha256=digest(ranked))
        return [by_id[key] for key in selected], metadata

    def request(self, branch: str, shared: dict[str, Any], regime: str) -> tuple[dict, dict]:
        """Khóa query từ FIN06; upstream báo cáo vẫn đi nguyên văn vào Common Decision."""
        from core.mt_bicl_prompt import canonical_request
        forecast_only(shared)
        if branch not in VARIANTS:
            raise ValueError("Nhánh ngoài FIN07")
        symbol, cutoff = shared["stock_name"], shared["as_of_date"]
        point = self.points[symbol + "-" + cutoff]
        key = point["retrieval_key"]
        frame = pd.DataFrame(shared["price_prefix"])
        frame["Datetime"] = pd.to_datetime(frame.Datetime)
        if (point["regime"] != regime or str(frame.Datetime.max().date()) != cutoff
                or key != key_at(frame, self.calendar, cutoff)):
            raise ValueError("Query FIN07 khác regime/cutoff đã khóa")
        query = query_signals(key, shared)
        eligible = [r for r in self.rows if r["symbol"] == symbol and r["exit_date"] < cutoff]
        population = [r for r in eligible if r["regime"] == regime and r["statistics_ready"]]
        examples = [r for r in population if r["example_ready"]]
        counts = statistics(population)
        fallback = None
        if symbol not in CORE4:
            fallback = "NO_SAME_SYMBOL_FROZEN_BANK_OOD"
        elif key["reason"] is not None:
            fallback = "QUERY_OHLCV_KEY_UNAVAILABLE"
        elif not population:
            fallback = "NO_SAME_REGIME_MATURE_BANK"
        condition, gate, selection, tasks, visible = None, None, None, [], []
        if fallback is None and branch == "bayesian_v1":
            def rank(row: dict) -> tuple:
                match = signals(row["retrieval_key"], row["alpha_consensus"], row["indicator_consensus"])
                return (-sum(match[k] == query[k] for k in FIELDS),
                        -date.fromisoformat(row["exit_date"]).toordinal(), row["episode_id"])
            tasks = sorted(examples, key=rank)[:3]
        elif fallback is None:
            condition = conditional(population, query, FIELDS[:2] if branch == "A_tp_pool" else FIELDS)
            tasks, selection = self.select(examples, query, point)
            gate = _readiness(len(population), condition["metrics"], selection, SPLIT_GATE)
            view = _content_views(gate, len(tasks))["full_prior"]
            visible = view["visible_metric_ids"]
            tasks = tasks if gate["examples_ready"] else []
            if view["fallback_to_original"]:
                fallback = "INSUFFICIENT_EVIDENCE"
        prefix = "" if fallback else render(branch, regime, len(population), tasks, counts, condition, visible)
        proof = {"branch": branch, "key_profile": PROFILE, "bank_sha256": self.bank_sha256,
                 "query_key": deepcopy(key), "query_signals": query, "fallback": fallback is not None, "reason": fallback,
                 "eligible_count": len(eligible), "population_ids": [r["episode_id"] for r in population],
                 "example_candidate_ids": [r["episode_id"] for r in examples],
                 "counts": counts, "conditional": condition, "gate": gate, "selection": selection,
                 "selected_ids": [r["episode_id"] for r in tasks], "request": {"prefix": prefix}}
        return canonical_request(shared, prefix, self.decision), proof
