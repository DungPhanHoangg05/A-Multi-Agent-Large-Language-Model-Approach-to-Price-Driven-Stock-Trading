"""Đối chiếu lượt Luna với dự báo Groq đã công bố, hoàn toàn ngoại tuyến."""
from __future__ import annotations

import argparse
import csv
from hashlib import sha256
import io
import json
from math import isclose
from pathlib import Path
import re
import sys
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.causal_alpha import frame_document
from core.evaluation_bicl import BiclStudy
from core.evaluation_component import MANIFEST, ComponentStudy, archive
from core.evaluation_results import compare, component_results, outcomes, summarize
from core.evaluation_transport import DECISION
from core.finalize_serving_resources import FinalizedResources
from core.historical_evaluation_journal import load
from core.research_results import ResearchResults
from core.unified_contracts import digest, json_bytes
from core.unified_preflight_assets import frames
from core.unified_protocol import DONOR, git_blob
from scripts.project_finalize_manuscript_tables import RECEIPT_SHA
from scripts.run_provider_evaluation import OUTPUT, STUDIES, plan, print_json

FIN12 = "evidence/fin12_audit.zip"
COMPONENT_COSTS = "outputs/revision/revision_minimal_final_v1/costs.json"
ARCHIVED_USAGE = {"scope": "ARCHIVED_FULL_STUDY", "prompt_tokens": None, "completion_tokens": None,
                  "observed_total_tokens": None, "schema_errors": None, "estimated_cost_usd": None}


def component_archive(study: ComponentStudy, points: list[dict]) -> tuple[dict, list[dict]]:
    """Đọc đúng 375 lượt đã chốt, dùng lại lượt chính được chia sẻ với panel upstream."""
    collected = []
    by_id = {point["id"]: point for point in points}
    for identifier, point in by_id.items():
        jobs = study.jobs[identifier]
        upstream_panel = any(job["phase"] == "upstream" for job in jobs)
        rows = []
        for job in jobs:
            reuse = job["reuse"]
            path = (reuse["path"] if reuse else
                    f"outputs/revision/revision_minimal_v1/shards/org{job['worker']}/decisions/{job['id']}.json")
            raw = git_blob(study.root, DONOR, path)
            old = json.loads(raw)
            if (old["context"] != job["context"] or old["context"]["model"] != DECISION
                    or old["prediction"] not in ("LONG", "SHORT")
                    or (reuse and sha256(raw).hexdigest() != reuse["sha256"])
                    or (not reuse and old["parent"]["prompt_hash"] != job["prompt_hash"])):
                raise ValueError("Dự báo thành phần sai lượt hoặc sai hash: " + job["id"])
            context = job["context"]
            row = {**point, "panel": job["phase"], "method": context["variant"], "repeat": context["repeat"],
                   "realization": context["realization"], "final_action": "LONG" if old["prediction"] == "LONG" else "CASH",
                   "fallback": bool(old["fallback_reason"])}
            rows.append(row)
            if row["panel"] == "main" and upstream_panel:
                rows.append({**row, "panel": "upstream"})
        collected.append({"rows": rows})
    result, predictions = component_results(study, points, collected, frames(study.root))
    costs = archive(study.root, COMPONENT_COSTS)
    sources = [costs["new"], costs["frozen_source"]]
    prompt = sum(group["observed_prompt_tokens"] for group in sources)
    completion = sum(group["observed_completion_tokens"] for group in sources)
    result["usage"] = {
        **ARCHIVED_USAGE,
        "attempts": sum(group["attempts"] for group in sources),
        "prompt_tokens": prompt,
        "completion_tokens": completion,
        "observed_total_tokens": prompt + completion,
        "schema_errors": sum(group["errors_by_category"].get("schema", 0) for group in sources),
    }
    result["archive"] = {"source_commit": DONOR, "manifest": MANIFEST, "usage_source": COMPONENT_COSTS}
    return result, predictions


def verified_fin12(root: Path) -> tuple[dict, list[dict], dict, dict]:
    """Xác minh receipt và checksum từng tệp FIN12 được đọc."""
    with ZipFile(root / FIN12) as bundle:
        raw = bundle.read("receipt.json")
        if sha256(raw).hexdigest() != RECEIPT_SHA:
            raise ValueError("Receipt FIN12 sai hash")
        receipt = json.loads(raw)["payload"]
        objects = []
        for name in ("results.json", "predictions.json", "outcomes.json"):
            raw = bundle.read(name)
            pin = receipt["artifacts"][name]
            if len(raw) != pin["bytes"] or sha256(raw).hexdigest() != pin["sha256"]:
                raise ValueError("Hiện vật FIN12 sai hash: " + name)
            objects.append(json.loads(raw))
    return (*objects, {"package": FIN12, "receipt_sha256": RECEIPT_SHA})


def bicl_archive(study: BiclStudy, points: list[dict], *, sample: bool) -> tuple[dict, list[dict]]:
    """Dùng dự báo và chỉ tiêu U09/FIN12 đã khóa, giữ NA của FIN12."""
    chosen = {p["id"]: p for p in points}
    complete = None
    if study.followup:
        published, source_rows, registered, provenance = verified_fin12(study.root)
        selected_outcomes = {key: registered[key] for key in chosen}
        usage = dict(ARCHIVED_USAGE)
        if sample:
            resources = FinalizedResources(study.root)
            prices = {symbol: resources.stock(symbol) for symbol in {p["symbol"] for p in points}}
            complete = {key for key, value in selected_outcomes.items() if value["target"]["net_return"] is not None}
    else:
        source = ResearchResults(study.root)
        published, source_rows, provenance = source.result(), source.table("predictions"), source.provenance()
        prices = frames(study.root)
        hashes = {symbol: digest(frame_document(prices[symbol])) for symbol in {p["symbol"] for p in points}}
        selected_outcomes = outcomes(points, prices, hashes)
        usage = {**ARCHIVED_USAGE, **published["telemetry"]}
    predictions = []
    for row in source_rows:
        key = row["point_id"]
        if key not in chosen:
            continue
        outcome, point = selected_outcomes[key], chosen[key]
        expected = outcome["target"]
        actual_return, expected_return = row["r_net"], expected["net_return"]
        matched_return = (actual_return is None if expected_return is None else
                          actual_return is not None and isclose(actual_return, expected_return, abs_tol=1e-12, rel_tol=0))
        if (row["label_net"] != expected["label_net"] or not matched_return or row["final_action"] not in ("LONG", "CASH")
                or (row["symbol"], row["fold"], row["date"], row["entry_date"], row["exit_date"]) !=
                (point["symbol"], point["fold"], point["cutoff"], outcome["dates"][1], outcome["dates"][3])):
            raise ValueError("Dự báo đã công bố khác mẫu hoặc outcome: " + key)
        predictions.append({**row, "panel": "main",
                            "fallback": row["reason"] in ("FALLBACK_ORIGINAL", "ANCHOR_INVALID_USE_ORIGINAL")
                            or (row["bypass"] and row["reason"] != "REGISTERED_NO_LLM_CONTROL")})
    if sample:
        metrics = summarize(predictions, prices, complete=complete)
    else:
        metrics = []
        for entry in published["summary"]:
            method = entry["method"]
            summary = {"panel": "main", "method": method,
                       "fallbacks": sum(row["fallback"] for row in predictions if row["method"] == method)}
            for key in ("balanced_accuracy_pct", "mean_account_return_pct"):
                summary[key] = entry["primary_" + key] if study.followup else entry[key]
                if study.followup:
                    summary["complete_accounts_" + key] = entry["complete_accounts_" + key]
            metrics.append(summary)
    return {"metrics": metrics, "outcome_sha256": digest(selected_outcomes), "archive": provenance, "usage": usage}, predictions


def export_archived(study_name: str, run_id: str, sample: int | None, *, output: Path = OUTPUT) -> dict:
    """Đối chiếu lượt Luna đã chốt với hiện vật Groq, không khởi tạo client."""
    study, planned, _ = plan(study_name, "luna", sample)
    mode = "full" if sample is None else f"sample-{sample}"
    base = output / run_id / study_name / mode
    luna = load(base / "luna" / "result.json")
    luna_predictions = load(base / "luna" / "predictions.json")
    if (any(luna["identity"].get(key) != value for key, value in planned.items())
            or digest(luna_predictions) != luna["predictions_sha256"]):
        raise ValueError("Kết quả Luna khác kế hoạch hoặc checksum dự báo")
    points = planned["points"]
    groq, groq_predictions = (component_archive(study, points) if study_name == "component" else
                              bicl_archive(study, points, sample=sample is not None))
    result = compare(groq, luna, groq_predictions, luna_predictions)
    result.update(groq_archive=groq["archive"], luna_identity=luna["identity"], new_api_calls=0)
    if "schema_upgrade" in luna:
        result["luna_schema_upgrade"] = luna["schema_upgrade"]
    path = base / "luna_vs_archived_groq.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        rows = result["comparison"]
        writer = csv.DictWriter(handle, list(dict.fromkeys(key for row in rows for key in row)))
        writer.writeheader()
        writer.writerows(rows)
    path.with_suffix(".json").write_bytes(json_bytes(result))
    return {"comparison": str(path), "metrics": result["comparison"], "usage": result["usage"], "api": False}


def main() -> None:
    """Xuất báo cáo từ ba nguồn Groq đã lưu và thư mục Luna của đúng lượt thu."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study", required=True, choices=STUDIES)
    parser.add_argument("--run-id", default="v1")
    parser.add_argument("--sample-points", type=int)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,39}", args.run_id):
        parser.error("--run-id chỉ nhận chữ, số, gạch nối hoặc gạch dưới")
    if args.sample_points is not None and args.sample_points <= 0:
        parser.error("--sample-points phải dương")
    try:
        print_json(export_archived(args.study, args.run_id, args.sample_points))
    except (FileNotFoundError, ValueError) as error:
        parser.exit(2, f"Chưa xuất được báo cáo. {error}\n")


if __name__ == "__main__":
    main()
