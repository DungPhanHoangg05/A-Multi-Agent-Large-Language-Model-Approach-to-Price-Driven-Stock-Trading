"""Evaluator version mới, giữ nguyên evaluator và pin của backtest lịch sử."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import pandas as pd

from core.finalize_serving_profile import OUTCOME_REASONS, SCIENTIFIC_STATUS, UNAVAILABLE_OUTCOME, VERSION
from core.finalize_serving_resources import FinalizedResources
from core.serving_runtime.evaluation import evaluate as canonical_evaluate
from core.unified_contracts import checksum, digest


def prices(root: Path, reservation: dict, outcomes: dict[str, dict], resources: FinalizedResources) -> dict[str, pd.DataFrame]:
    """Mở giá tài khoản sau barrier, đồng nhất snapshot và label T+2.5."""
    resources.verify()
    job = reservation["job"]
    points = reservation["points"]
    snapshot = digest({"resource_bindings": resources.document()["bindings"], "points": points})
    if resources.root != root or snapshot != job["identity"]["snapshot_sha256"]:
        raise ValueError("Resource snapshot khác job FIN08")
    frames = {s: resources.stock(s) for s in job["identity"]["request"]["symbols"]}
    for point in points:
        if outcomes[point["id"]] != resources.outcome(point, frames[point["symbol"]]):
            raise ValueError("Outcome khác nguồn FIN08 và oracle canonical")
    return frames


def evaluate(reservation: dict, public: dict, outcomes: dict[str, dict], query: dict[str, str],
             price_loader: Callable[[], Any]) -> dict:
    """Evaluator cũ vẫn tính metric từ outcome hợp lệ; mọi NA giữ incomplete coverage."""
    valid, unavailable = {}, {}
    points = {p["id"] for p in reservation["points"]}
    expected = len(public["execution_plan"]) * public["identity"]["request"]["repeats"]
    for identifier, outcome in outcomes.items():
        if outcome.get("version") != UNAVAILABLE_OUTCOME:
            valid[identifier] = outcome
            continue
        if (identifier not in points or set(outcome) != {"version", "point_id", "source_sha256", "reason"}
                or outcome["point_id"] != identifier or not checksum(outcome["source_sha256"])
                or outcome["reason"] not in OUTCOME_REASONS
                or sum(r["point_id"] == identifier for r in public["rows"]) != expected):
            raise ValueError("Outcome NA sai nguồn, schema hoặc forecast barrier")
        unavailable[identifier] = outcome["reason"]
    result = canonical_evaluate(reservation, public, valid, query, price_loader)
    result["limitations"][-1] = "FINALIZED_PREVIEW_" + SCIENTIFIC_STATUS
    result["provenance"]["serving_profile"] = VERSION
    result["coverage"]["unavailable_outcomes"] = unavailable
    if unavailable and public["state"] == "completed" and result["coverage"]["filtered_points"]:
        result["evaluation_status"] = "UNAVAILABLE_EXECUTION_OUTCOMES"
    return result
