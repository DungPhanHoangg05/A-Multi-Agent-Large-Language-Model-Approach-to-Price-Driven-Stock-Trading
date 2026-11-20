"""Đánh giá FIN12 từ journal FIN11 đã chốt trong tiến trình offline."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
from tempfile import TemporaryDirectory, gettempdir

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.finalize_serving_profile import method_profile
from core.historical_evaluation_journal import load, save
from core.prior_run_lock import PriorRunLock
from core.unified_analysis.runtime import artifact_bindings
from core.unified_contracts import digest, json_bytes
from core.unified_execution import StageBook
from core.unified_experiment import runtime_identity
from core.unified_protocol import binding, read
from scripts.finalize_hosted_point_reset import archived_resets
from scripts.finalize_hosted_study import RUN, check_release, release_for_grant, verify_operation
from scripts.fin12_evaluation import evaluate
from scripts.prepare_finalize_api_budget import CONTRACT, study

OUTPUT = ROOT/"outputs"/"finalize"/"fin12_v1"
FIN11_RECEIPT_SHA = "dcf3c28a54343b9506e0834a244cc371bced51b8f478155c9ef004cabddb776b"
SOURCES = (
    "scripts/evaluate_finalize_study.py", "scripts/fin12_evaluation.py",
    "scripts/fin12_evaluation_oracle.py", "core/unified_analysis/analysis.py",
    "core/unified_analysis/statistics.py", "core/free_pilot_statistics.py",
    "core/finalize_serving_resources.py", "core/backtest_engine.py", "utils/target_contract.py",
)


def committed_stage(book: StageBook, slot: str) -> tuple[dict, dict]:
    """Chỉ đọc node complete, có cùng identity và hash đầu vào."""
    doc = load(book.path(slot))
    if (len(doc["attempts"]) != 1 or not book.complete(slot)
            or digest(doc["inputs"]) != doc["inputs_sha256"]):
        raise ValueError(f"Stage FIN11 chưa hợp lệ cho FIN12: {slot}")
    return doc["attempts"][0], doc["inputs"]


def accept_forecasts(release: dict, budget: dict, points: list[dict]) -> dict:
    """Đối chiếu đủ cả grid, raw và parent trước khi evaluator đọc outcome."""
    grant = load(RUN/"grant.json")
    verify_operation(RUN, release, release_for_grant(grant, release))
    resets = archived_resets(RUN, grant)
    source = "outputs/finalize/fin11_v1/research/receipt.json"
    receipt_pin = binding(ROOT, source)
    receipt = load(ROOT/source)
    status = load(RUN/"status.json")
    if (receipt_pin["sha256"] != FIN11_RECEIPT_SHA or status["status"] != "PASS_FIN11"
            or status["phases"]["RESEARCH"] != receipt or receipt["outcomes_opened"] != 0
            or receipt["grant_sha256"] != digest(grant)):
        raise ValueError("Thiếu receipt FIN11 đã nghiệm thu")
    directory = RUN/"research"
    identity = load(directory/"journal"/"identity.json")["identity"]
    if (identity["points"] != points or identity["phase"] != "RESEARCH" or identity["repeats"] != 3
            or identity["realizations"] != 1 or identity["release_sha256"] != digest(grant)
            or identity["budget_sha256"] != digest(budget) or identity["epoch"] != receipt["epoch"]):
        raise ValueError("Identity nghiên cứu không đúng FIN09/FIN11")
    book = StageBook(directory/"journal", identity, verify_only=True)
    plans = {row["slot"]: row for row in budget["slots"] if row["phase"] == "RESEARCH"}
    wires = {}
    for path in (directory/"http").glob("*.json"):
        doc = load(path)
        slot = doc["slot"]
        if (path.stem != digest(slot) or doc["run_id"] != book.signature
                or plans[slot]["state"] != "NEW" or not doc["rows"] or doc["rows"][-1]["status"] != 200
                or any(r["slot"] != slot or r["status"] == "UNKNOWN" for r in doc["rows"])):
            raise ValueError(f"Wire chưa đối soát: {slot}")
        wires[slot] = doc["rows"]
    raw = [row for slot in plans for row in wires.get(slot, [])]
    if (len(raw) != receipt["hosted_attempts"] or len({row["id"] for row in raw}) != len(raw)
            or digest([digest(row) for row in raw]) != receipt["raw_attempts_sha256"]):
        raise ValueError("Raw FIN11 khác receipt")
    records, prepared, provenance, checkpoints = [], {}, {}, {}
    for point in points:
        identifier = point["id"]
        checkpoint = load(directory/"points"/f"{identifier}.json")
        if (checkpoint["identity_sha256"] != book.signature or checkpoint["outcomes_opened"] != 0
                or list(checkpoint["points"]) != [identifier] or book.path("outcome/"+identifier).exists()):
            raise ValueError("Checkpoint thiếu seal hoặc outcome đã mở trong journal thu")
        value = checkpoints[identifier] = checkpoint["points"][identifier]
        expected = {slot for slot in plans if slot.startswith(f"forecast/{identifier}/")}
        if set(value["forecasts"]) != expected or len(expected) != 24:
            raise ValueError(f"Thiếu dự báo paired: {identifier}")
        for slot in sorted(expected):
            attempt, inputs = committed_stage(book, slot)
            prep, prep_inputs = committed_stage(book, "prepare/"+slot)
            record = attempt["output"]
            forecast, policy = record["forecast"], record["policy"]
            _, _, _, repeat, method = slot.split("/")
            raw_forecast = forecast["raw"]
            parents = {name: value["forecasts"][f"forecast/{identifier}/u0/{repeat}/{name}"]
                       for name in forecast["dependency_hashes"]}
            paired = {"dependency_hashes": parents, "shared_sha256": value["shared_sha256"]}
            if (digest(record) != value["forecasts"][slot] or prep_inputs != paired
                    or inputs != {**paired, "prepared": prep["output"]}
                    or any(forecast[key] != expected_value for key, expected_value in paired.items())
                    or (forecast["point_id"], forecast["realization"], forecast["repeat"], forecast["variant"])
                    != (identifier, 0, int(repeat[1:]), method) or forecast["profile"] != method_profile(method)
                    or policy["final_action"] not in ("LONG", "CASH")):
                raise ValueError(f"Forecast khác hash, profile hoặc dependency: {slot}")
            if raw_forecast is None:
                if slot in wires or not policy["bypass"] or prep["output"]["request"] is not None:
                    raise ValueError(f"Bypass khác chứng cứ FIN11: {slot}")
                origin = {"response_epoch": None, "response_org": None, "response_model": None}
            else:
                wire = wires[slot][-1]
                if (raw_forecast["source_request_id"] != wire["id"] or raw_forecast["source_sha256"] != digest(wire)
                        or raw_forecast["request_sha256"] != forecast["request_sha256"]
                        or forecast["request_sha256"] != digest(prep["output"]["request"])
                        or wire["attempt"] != attempt["attempt_id"]):
                    raise ValueError(f"Forecast trỏ sai request/raw: {slot}")
                origin = {"response_epoch": receipt["epoch"], "response_org": wire.get("org_slot", 1),
                          "response_model": wire["body"]["model"]}
            prepared[slot] = prep["output"]
            provenance[slot] = {**origin, "forecast_sha256": digest(record), "prepared_sha256": prep["output_sha256"],
                                "response_sha256": raw_forecast["source_sha256"] if raw_forecast else None,
                                "vision_provenance": value["vision"]}
            records.append(record)
    if (len(records) != receipt["forecast_slots"] or len(checkpoints) != receipt["points"]
            or digest({"identity_sha256": book.signature, "points": checkpoints, "outcomes_opened": 0})
            != receipt["checkpoint_sha256"]):
        raise ValueError("Grid hoặc checkpoint hợp nhất khác receipt FIN11")
    return {"points": points, "records": records, "prepared": prepared, "row_provenance": provenance,
            "input_identity": {"fin11": receipt_pin, "fin11_epoch": receipt["epoch"],
                "grant_sha256": digest(grant), "records_sha256": digest(records), "prepared_sha256": digest(prepared),
                "checkpoint_sha256": receipt["checkpoint_sha256"], "raw_attempts_sha256": receipt["raw_attempts_sha256"],
                "archived_points": [record["point_id"] for record in resets],
                "contract": binding(ROOT, CONTRACT), "fin11_release_sha256": digest(release)}}


def calculate(destination: Path) -> dict:
    """Dựng kết quả ở vùng riêng, không ghi vào journal gốc."""
    release, (budget, resources) = check_release()
    points, _, _, _ = study(ROOT)
    bundle = accept_forecasts(release, budget, points)
    contract = read(ROOT, CONTRACT, True)
    bundle["input_identity"].update(sources=[binding(ROOT, path) for path in SOURCES],
        runtime=runtime_identity(), resource_bindings_sha256=digest(resources.document()))
    result, tables = evaluate(bundle, contract, resources)
    destination.mkdir(parents=True, exist_ok=True)
    (destination/"results.json").write_bytes(json_bytes(result))
    for name, rows in tables.items():
        (destination/f"{name}.json").write_bytes(json_bytes(rows))
    return {"status": "FIN12_EVALUATED_OFFLINE", "input_identity": result["input_identity"],
            "coverage": result["coverage"], "oracle": result["oracle"],
            "artifacts": artifact_bindings(destination), "new_api_calls": 0}


def run(mode: str) -> dict:
    """Analyze tạo artifact một lần, verify tái dựng mọi byte trong tiến trình mới."""
    with PriorRunLock(OUTPUT.with_name("fin12_v1_worker"), digest({"namespace": OUTPUT.name, "parent": FIN11_RECEIPT_SHA})):
        receipt_path = OUTPUT/"receipt.json"
        if mode == "analyze":
            if OUTPUT.exists():
                raise ValueError("Artifact FIN12 đã tồn tại, dùng verify")
            with TemporaryDirectory(prefix="fin12-analyze-", dir=OUTPUT.parent) as temporary:
                scratch = Path(temporary).resolve()
                if scratch.parent != OUTPUT.parent.resolve() or not scratch.name.startswith("fin12-analyze-"):
                    raise ValueError("Thư mục phân tích ngoài vùng finalize")
                candidate = scratch/"artifacts"
                receipt = calculate(candidate)
                save(candidate/"receipt.json", receipt)
                candidate.rename(OUTPUT)
                return receipt
        receipt = load(receipt_path)
        if receipt["artifacts"] != artifact_bindings(OUTPUT):
            raise ValueError("Artifact FIN12 khác receipt")
        with TemporaryDirectory(prefix="fin12-verify-") as temporary:
            scratch = Path(temporary).resolve()
            if scratch.parent != Path(gettempdir()).resolve() or not scratch.name.startswith("fin12-verify-"):
                raise ValueError("Thư mục cold verify ngoài vùng tạm")
            if calculate(scratch) != receipt:
                raise ValueError("Cold verify FIN12 khác receipt")
        return {"status": "PASS_FIN12_COLD_REPLAY", "analysis_receipt_sha256": digest(receipt),
                "artifact_count": len(receipt["artifacts"]), "new_api_calls": 0}


def main() -> None:
    """Chặn mạng và chạy đánh giá với runtime đã khóa."""
    from scripts.verify_original_fix_parity import deny_external_network
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("analyze", "verify"))
    args = parser.parse_args()
    deny_external_network()
    print(json_bytes(run(args.mode)).decode(), flush=True)


if __name__ == "__main__":
    main()
