"""Bộ lọc hiển thị chỉ dùng metrics đã seal; không đổi cohort hoặc tái bootstrap."""
from __future__ import annotations

import csv
import io
import json
from typing import Any

from core.research_results import ResearchResults, TABLES
from core.serving_registry import MAIN_IDS, ADVANCED_IDS
from core.unified_contracts import json_bytes

CONTROLS = ("CASH_EVERY_CYCLE", "ALWAYS_LONG_EVERY_CYCLE_WITH_FULL_COSTS")
UNITS = {"mean_account_return_pct": "PERCENT_EQUAL_MEAN_SYMBOL_FOLD_ACCOUNTS",
    "balanced_accuracy_pct": "PERCENT_MEAN_PER_REPEAT", "accuracy": "FRACTION_MEAN_PER_REPEAT",
    "mcc": "DIMENSIONLESS_MEAN_PER_REPEAT", "f1_positive": "FRACTION_MEAN_PER_REPEAT",
    "f1_negative": "FRACTION_MEAN_PER_REPEAT", "long_rate": "FRACTION", "effect_pp": "PERCENTAGE_POINTS",
    "return_pct": "PERCENT_PER_SYMBOL_FOLD_REPEAT_ACCOUNT", "strategy_return": "FRACTION_PER_CYCLE",
    "r_net": "FRACTION_MARKET_LABEL", "nav_vnd": "VND_PER_ACCOUNT_EOD",
    "mean_daily_mdd_pct": "PERCENT", "fee_vnd": "VND", "slippage_vnd": "VND", "turnover_vnd": "VND"}
UNITS.update({name: "VND_PER_ACCOUNT" for name in ("mean_fee_vnd", "mean_slippage_vnd", "mean_turnover_vnd",
    "initial_vnd", "final_vnd", "capital_before_vnd", "capital_after_vnd")})
UNITS.update({name: "PERCENT" for name in ("daily_mdd_pct", "cycle_end_mdd_pct", "mean_cycle_end_mdd_pct", "worst_account_daily_mdd_pct")})
UNITS.update({name: "DIMENSIONLESS_PER_CYCLE_NOT_ANNUALIZED" for name in ("cycle_sharpe", "cycle_sortino_lpm2")})
UNITS.update({name: "FRACTION" for name in ("macro_f1", "held_session_fraction", "mean_held_session_fraction")})


def view(reader: ResearchResults, query: dict[str, str], *, export: bool = False) -> dict[str, Any]:
    """Method/baseline chỉ ẩn hàng; repeat/mã/fold chỉ lọc chi tiết, summary/band giữ full cohort."""
    if set(query) - {"methods", "baseline", "repeat", "symbol", "fold", "table", "offset", "limit"}:
        raise ValueError("Bộ lọc không được hỗ trợ")
    methods = query.get("methods", ",".join((*MAIN_IDS, *ADVANCED_IDS))).split(",")
    if not methods or len(methods) != len(set(methods)) or not set(methods) <= set((*MAIN_IDS, *ADVANCED_IDS, *CONTROLS)):
        raise ValueError("Danh sách phương pháp không hợp lệ")
    baseline = query.get("baseline", "original_fix")
    if baseline not in ("original_fix", "original_common"):
        raise ValueError("Baseline không thuộc hai family U09")
    repeat = query.get("repeat", "all")
    if repeat not in ("all", "0", "1", "2"):
        raise ValueError("Repeat không hợp lệ")
    table = query.get("table", "predictions")
    if table not in TABLES:
        raise ValueError("Bảng không hợp lệ")
    try:
        offset, limit = int(query.get("offset", "0")), int(query.get("limit", "50"))
    except (ValueError, TypeError) as error:
        raise ValueError("Phân trang không hợp lệ") from error
    if offset < 0 or not 1 <= limit <= 200:
        raise ValueError("Phân trang ngoài giới hạn")
    rows = reader.table(table)
    for key in ("symbol", "fold"):
        if query.get(key, "all") not in {"all", *(r[key] for r in rows)}:
            raise ValueError("Mã/fold ngoài support đã seal")
    selected = [r for r in rows if r["method"] in methods and (repeat == "all" or r["repeat"] == int(repeat))
                and all(query.get(k, "all") in ("all", r[k]) for k in ("symbol", "fold"))]
    result = reader.result()
    support = reader.support()
    filters = {"methods": methods, "baseline": baseline, "detail_repeat": repeat,
               "detail_symbol": query.get("symbol", "all"), "detail_fold": query.get("fold", "all")}
    return {"version": "research_results_view_v1", "run_id": reader.provenance()["run_id"],
        "kind": "paper_evidence", "status": "completed", "provenance": reader.provenance(), "filters": filters,
        "units": dict(UNITS), "metric_scope": "FROZEN_FULL_COHORT_MEAN_ALL_THREE_REPEATS",
        "detail_filter_scope": "SYMBOL_FOLD_DETAIL_ONLY; REPEAT_ALSO_SELECTS_SEALED_PER_REPEAT_METRICS; SUMMARY_BANDS_UNCHANGED",
        "support": support, "coverage": result["coverage"], "definitions": result["definitions"],
        "telemetry": result["telemetry"], "limitations": result["limitations"],
        "summary": [r for r in result["summary"] if r["method"] in methods],
        "contrasts": [r for r in result["contrasts"] if r["method"] in methods and r["baseline"] == baseline],
        "bridge": [r for r in result["bridge"] if r["method"] in methods],
        "per_repeat": [r for r in result["per_repeat"] if r["method"] in methods and (repeat == "all" or r["repeat"] == int(repeat))],
        "classification_by_repeat": [r for r in result["classification_by_repeat"] if r["method"] in methods
                                     and (repeat == "all" or r["repeat"] == int(repeat))],
        "details": {"table": table, "total": len(selected), "offset": 0 if export else offset,
                    "frequency": {"predictions": "FORECAST_POINT", "accounts": "SYMBOL_FOLD_REPEAT_ACCOUNT",
                                  "cycles": "PER_TRADE_CYCLE", "daily_nav": "DAILY_EOD_PER_ACCOUNT"}[table],
                    "limit": None if export else limit, "rows": selected if export else selected[offset:offset+limit]},
        "options": {"symbols": sorted({r["symbol"] for r in rows}), "folds": sorted({r["fold"] for r in rows})}}


def csv_cell(value: Any) -> Any:
    """Chặn công thức trong chuỗi, giữ nguyên số âm có kiểu numeric."""
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True)
    if type(value) is str and (value.lstrip().startswith(("=", "+", "-", "@")) or value.startswith(("\t", "\r", "\n"))):
        return "'" + value
    return value


def export_bytes(result: dict[str, Any], format_name: str, table: str = "summary") -> tuple[bytes, str]:
    """Xuất đúng projection cùng provenance/units; CSV không mang công thức thực thi."""
    if format_name == "json":
        return json_bytes(result), "application/json"
    if format_name != "csv" or table not in ("summary", "contrasts", "bridge", "per_repeat", "classification_by_repeat", "details"):
        raise ValueError("Định dạng/bảng export không hợp lệ")
    rows = result["details"]["rows"] if table == "details" else result[table]
    meta = {"run_id": result["run_id"], "package_sha256": result["provenance"]["package_sha256"],
            "receipt_sha256": result["provenance"]["receipt_sha256"], "support_id": result["provenance"]["support_id"],
            "metric_scope": result["metric_scope"], "units_json": result["units"], "filters_json": result["filters"]}
    meta["detail_frequency"] = result["details"]["frequency"]
    columns = list(dict.fromkeys(k for row in rows for k in row)) + list(meta)
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, columns, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({k: csv_cell(v) for k, v in {**row, **meta}.items()})
    return stream.getvalue().encode("utf-8-sig"), "text/csv; charset=utf-8"
