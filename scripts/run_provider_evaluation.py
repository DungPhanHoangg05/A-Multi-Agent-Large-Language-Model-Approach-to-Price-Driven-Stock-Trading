"""Chạy hoặc đối chiếu ba đợt nghiên cứu Groq/Luna trong namespace riêng."""
from __future__ import annotations

import argparse
import csv
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import sys
import time
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.evaluation_bicl import BiclStudy, bank_records, bind_bank, refresh_bank
from core.evaluation_component import ComponentStudy
from core.evaluation_results import bicl_results, compare, component_results
from core.evaluation_transport import ENDPOINTS, EvaluationCalls, ProviderHTTP, usage_totals
from core.finalize_serving_resources import FinalizedResources
from core.historical_evaluation_journal import load, save
from core.prior_run_lock import PriorRunLock
from core.serving_runtime.quota import Failed, Quota, Unknown
from core.serving_runtime.transport import Calls
from core.unified_contracts import digest, json_bytes
from core.unified_execution import StageBook
from core.unified_experiment import runtime_identity, source_identity
from core.unified_preflight_assets import frames
from core.unified_protocol import CORE4

STUDIES = ("component", "bicl", "followup")
OUTPUT = ROOT / "outputs" / "provider_evaluation"
SOURCES = ("scripts/run_provider_evaluation.py", "scripts/fin12_evaluation.py",
           "scripts/fin12_evaluation_oracle.py", "resources/serving_inputs.zip")
PREVIOUS_QUOTA_SOURCES = {
    "core/groq_pacing.py": "a7a35c7cc99920d150b90535cf4d013d4390812c34bc9f5404e744f9cf4c348d",
    "core/serving_runtime/quota.py": "ff8fb6ca38a9c8e7ce443f52eec1dabd34d9167e9ab78f520638973df35eb1dd",
    "scripts/run_provider_evaluation.py": "09ece882e802c21c6e86e46aa912b4958dc56db30642a9110da5d16211dbec09",
}
PREVIOUS_FINALIZATION_SOURCES = {
    **PREVIOUS_QUOTA_SOURCES,
    "core/evaluation_results.py": "053d6c750749c9c667443ff2420b8dbcde51f32f6ebffc2828018923ec884749",
    "scripts/run_provider_evaluation.py": "db649e80e281ea083e71234690361d5ff08b9e9d85f0a9dbe107d1fc6b1b7ffa",
}
PREVIOUS_BANK_BINDING_SOURCES = {
    **PREVIOUS_FINALIZATION_SOURCES,
    "core/evaluation_bicl.py": "1e8ff43e62272b4c64b8f558008c18925aac0e97eba5dc4a2fa2c0a3a0c02f26",
    "scripts/run_provider_evaluation.py": "723b93113689be5626f182333be3d6553c31118d93548856e6008f8bcd160206",
}
LEGACY_SCHEMA_SOURCES = {
    **PREVIOUS_BANK_BINDING_SOURCES,
    "core/evaluation_transport.py": "6deaa85f8853dec17f1c6e945a13cdd36f0df3fb964c3325f0683e6f094a5922",
    "core/serving_runtime/transport.py": "41f2980370163529d0968e3ccac44873b0d9f7a2ab4478e1c19d0891980711f8",
    "scripts/run_provider_evaluation.py": "9e97f07abdb3aa041c1b61ac9ab68cad65b47e01c7783cb55391f5d0a6433242",
}


def plan(study_name: str, provider: str, sample: int | None) -> tuple[Any, dict, list[dict]]:
    """Lập kế hoạch offline từ manifest, gồm các lượt vision tạo bank riêng."""
    study = ComponentStudy(ROOT) if study_name == "component" else BiclStudy(ROOT, study_name)
    points = study.points
    if sample is not None:
        if study_name == "bicl":
            # Mẫu chi phí chỉ lấy mã ngoài bank để không truy xuất kho tái tạo một phần.
            points = [p for p in points if p["symbol"] not in CORE4]
        if sample > len(points):
            raise ValueError("Số điểm mẫu vượt số điểm khả dụng")
        points = points[:sample]
    history = bank_records(ROOT) if study_name == "bicl" else []
    bank = history[:sample] if sample is not None else history
    if provider != "luna":
        bank = []
    counts = study.call_counts(points)
    if bank:
        counts.update(bank_pattern=len(bank), bank_trend=len(bank))
    identity = {"study": study_name, "provider": provider, "sample_points": sample, "points": points,
                "cohort_sha256": study.source_sha256, "bank_ids": [r["episode_id"] for r in bank],
                "historical_bank_sha256": digest(history) if history else None, "calls_by_role": counts}
    return study, identity, bank


def freeze(identity: dict, *, legacy_schema: bool = False, previous_bank_binding: bool = False,
           previous_finalization: bool = False, previous_quota: bool = False) -> dict:
    """Khóa cohort, cấu hình, runtime và code điều phối trước khi đọc key."""
    sources = source_identity(ROOT) | {name: sha256((ROOT/name).read_bytes()).hexdigest() for name in SOURCES}
    if previous_quota:
        sources.update(PREVIOUS_QUOTA_SOURCES)
    if previous_finalization:
        sources.update(PREVIOUS_FINALIZATION_SOURCES)
    if previous_bank_binding:
        sources.update(PREVIOUS_BANK_BINDING_SOURCES)
    if legacy_schema:
        sources.update(LEGACY_SCHEMA_SOURCES)
    return {**identity, "runtime": runtime_identity(), "source_sha256": digest(sources)}


def checkpoint_identity(directory: Path, planned: dict) -> tuple[dict, dict | None]:
    """Nhận đúng fingerprint trước các bản sửa, giữ UUID và checkpoint cũ."""
    current = freeze(planned)
    path = directory / "identity.json"
    if not path.exists():
        return current, None
    previous = load(path)["identity"]
    if previous == current:
        return current, None
    previous_quota = freeze(planned, previous_quota=True)
    previous_finalization = freeze(planned, previous_finalization=True)
    previous_binding = freeze(planned, previous_bank_binding=True)
    accepted = (previous_quota, previous_finalization, previous_binding)
    if previous in accepted:
        return previous, None
    if previous != freeze(planned, legacy_schema=True):
        raise ValueError("Checkpoint khác cohort, runtime hoặc nguồn đã khóa")
    if planned["provider"] != "luna":
        return previous, None
    upgrade = {"previous_source_sha256": previous["source_sha256"], "strict_source_sha256": current["source_sha256"],
               "previous_response_format": "json_schema_best_effort", "new_response_format": "json_schema_strict"}
    receipt_path = directory / "schema_upgrade.json"
    if receipt_path.is_file():
        receipt = load(receipt_path)
        if any(receipt == {**upgrade, "strict_source_sha256": old["source_sha256"]} for old in accepted):
            upgrade = receipt
    return previous, upgrade


def print_json(value: Any) -> None:
    """Xuất JSON dễ đọc và dùng được trong PowerShell."""
    print(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), flush=True)


def collect(directory: Path, identity: dict, study: Any, bank: list[dict], calls: EvaluationCalls, book: StageBook) -> dict:
    """Checkpoint từng episode và test point, rồi xuất thống kê với khóa run."""
    points, sample = identity["points"], identity["sample_points"] is not None
    if isinstance(study, ComponentStudy):
        market = frames(ROOT)

        def process(point: dict) -> dict:
            return study.run_point(book, point, calls, market[point["symbol"]])
    else:
        provider = study.provider(calls)
        market = provider.resources if study.followup else provider.prices
        if bank:
            signals = refresh_bank(ROOT, book, calls, bank, study.points)
            if not sample:
                bind_bank(provider, directory, signals)

        def process(point: dict) -> dict:
            return study.run_point(book, provider, point, calls)

    collected = []
    for index, point in enumerate(points, 1):
        collected.append(book.execute("point/" + point["id"], {"point": point}, lambda _: process(point)))
        print(f"Điểm đã chốt {index}/{len(points)} {point['id']}", flush=True)
    return write_results(directory, identity, study, market, collected, book.signature)


def analysis_http(directory: Path, signature: str) -> list[dict]:
    """Chiếu các trường telemetry mà evaluator U09 đọc từ nhật ký đã kiểm."""
    attempts = []
    for path in (directory / "http").glob("*.json"):
        doc = load(path)
        if doc["run_id"] != signature:
            raise ValueError("Nhật ký HTTP khác checkpoint")
        attempts.extend({"status": row["status"], "total_tokens": row["usage"],
                         "reserved_tokens": row["reserved_tokens"]} for row in doc["rows"])
    return attempts


def write_results(directory: Path, identity: dict, study: Any, market: dict | FinalizedResources,
                  collected: list[dict], signature: str) -> dict:
    """Phân tích dự báo đã chốt và ghi kết quả trong cùng namespace của lượt thu."""
    points, sample = identity["points"], identity["sample_points"] is not None
    if isinstance(study, ComponentStudy):
        result, predictions = component_results(study, points, collected, market)
    else:
        http = analysis_http(directory, signature) if not study.followup and not sample else []
        result, predictions = bicl_results(study, points, market, collected, identity, sample=sample, http=http)
    result.update(identity=identity, usage=usage_totals(directory, signature),
                  predictions_sha256=digest(predictions))
    if (directory / "schema_upgrade.json").exists():
        result["schema_upgrade"] = load(directory / "schema_upgrade.json")
    save(directory / "predictions.json", predictions)
    save(directory / "result.json", result)
    return result


def cached_result(directory: Path, identity: dict) -> dict | None:
    """Xác minh kết quả đã xuất trước khi dùng lại."""
    path = directory / "result.json"
    if not path.exists():
        return None
    result = load(path)
    if result["identity"] != identity or digest(load(directory / "predictions.json")) != result["predictions_sha256"]:
        raise ValueError("File kết quả hiện tại khác checkpoint")
    return result


def finalize(directory: Path, identity: dict, study: Any) -> dict:
    """Đọc đủ checkpoint đã chốt rồi phân tích ngoại tuyến, không tạo provider."""
    book = StageBook(directory, identity, verify_only=True)
    with PriorRunLock(directory, book.signature):
        cached = cached_result(directory, identity)
        if cached is not None:
            return cached
        collected = [book.execute("point/" + point["id"], {"point": point}, None) for point in identity["points"]]
        if isinstance(study, BiclStudy) and study.followup:
            market = FinalizedResources(study.root)
            market.verify()
        else:
            market = frames(study.root)
        return write_results(directory, identity, study, market, collected, book.signature)


def export(base: Path) -> None:
    """Đọc hai kết quả đã chốt, kiểm cùng mẫu và xuất CSV/JSON ngoại tuyến."""
    reports, forecasts = {}, {}
    for name in ENDPOINTS:
        directory = base / name
        reports[name] = load(directory / "result.json")
        forecasts[name] = load(directory / "predictions.json")
        if (reports[name]["identity"]["provider"] != name
                or digest(forecasts[name]) != reports[name]["predictions_sha256"]):
            raise ValueError("Kết quả khác cấu hình hoặc checksum dự báo")
    g, l = (reports[p]["identity"] for p in ENDPOINTS)
    fields = ("study", "sample_points", "points", "cohort_sha256", "historical_bank_sha256", "source_sha256", "runtime")
    if any(g[key] != l[key] for key in fields):
        raise ValueError("Hai kết quả khác giao thức, runtime hoặc nguồn code")
    output = compare(reports["groq"], reports["luna"], forecasts["groq"], forecasts["luna"])
    (base / "comparison.json").write_bytes(json_bytes(output))
    with (base / "comparison.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        rows = output["comparison"]
        writer = csv.DictWriter(handle, list(dict.fromkeys(key for row in rows for key in row)))
        writer.writeheader()
        writer.writerows(rows)
    print_json({"directory": str(base), "comparison": str(base / "comparison.csv"), "usage": output["usage"]})


def quota(provider: str) -> Quota:
    """Chia sẻ headroom giữa các đợt cùng provider, giữ pacing Free cho Groq."""
    path = OUTPUT / (provider + "-quota.sqlite")
    return Quota(path, limits=None) if provider == "luna" else Quota(path)


def repair_luna_quota(directory: Path, signature: str, ledger: Quota) -> list[str]:
    """Dùng raw cuối của lượt Luna để đối soát mốc chờ đã lưu."""
    latest = max((directory / "http").glob("*.json"), key=lambda path: path.stat().st_mtime_ns, default=None)
    if latest is None:
        return []
    doc = load(latest)
    if doc["run_id"] != signature:
        raise ValueError("Nhật ký HTTP khác checkpoint")
    return ledger.repair_millisecond_deadline(signature, doc["rows"][-1])


def wait_for_provider(until: float) -> None:
    """Chờ trong cùng slot, vẫn nhận được Ctrl+C giữa các lần gửi."""
    remaining = until - time.time()
    print(f"Chờ quota hoặc retry trong {max(0, int(remaining))} giây", flush=True)
    while remaining > 0:
        time.sleep(min(60, remaining))
        remaining = until - time.time()


def run_paid(directory: Path, identity: dict, study: Any, bank: list[dict],
             *, upgrade: dict | None = None) -> None:
    """Chỉ lệnh run khởi tạo HTTP và đọc khóa xác thực."""
    provider = identity["provider"]
    key_name = ENDPOINTS[provider][0]
    key = os.environ.get(key_name, "").strip()
    if not key:
        raise ValueError("Hãy đặt biến môi trường " + key_name)
    with PriorRunLock(directory, digest(identity)):
        book = StageBook(directory, identity)
        cached = cached_result(directory, identity)
        if cached is not None:
            print_json({"directory": str(directory), "usage": cached["usage"], "status": "COMPLETE"})
            return
        if upgrade is not None:
            migration = directory / "schema_upgrade.json"
            if migration.exists() and load(migration) != upgrade:
                raise ValueError("Bản nâng cấp schema khác checkpoint")
            if not migration.exists():
                save(migration, upgrade)
            print("Tiếp tục checkpoint Luna với schema strict cho các lượt mới.", flush=True)
        ledger = quota(provider)
        if provider == "luna" and repair_luna_quota(directory, book.signature, ledger):
            print("Đã sửa mốc chờ quota từ header mili giây của OpenAI.", flush=True)
        sender = ProviderHTTP(provider, key)
        try:
            calls = EvaluationCalls(directory, book.signature, ledger, sender, lambda: None,
                                    provider=provider, wait=wait_for_provider, legacy_schema=upgrade is not None)
            result = collect(directory, identity, study, bank, calls, book)
        finally:
            sender.close()
    print_json({"directory": str(directory), "usage": result["usage"], "status": "COMPLETE"})


def main() -> None:
    """Lệnh offline tách riêng khỏi run có API, resume giữ cùng đường dẫn."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("dry-run", "run", "finalize", "status", "report", "reconcile-not-sent"))
    parser.add_argument("--study", choices=STUDIES, required=True)
    parser.add_argument("--provider", choices=tuple(ENDPOINTS))
    parser.add_argument("--sample-points", type=int, help="Lấy số điểm đầu tiên theo mẫu chi phí đã định")
    parser.add_argument("--run-id", default="v1", help="Tên lượt thu, giữ nguyên khi resume và xuất báo cáo")
    parser.add_argument("--slot", help="Tên slot HTTP cần đối soát")
    parser.add_argument("--request-id", help="UUID của attempt UNKNOWN")
    parser.add_argument("--evidence", help="Bằng chứng nhà cung cấp chưa nhận request")
    args = parser.parse_args()
    if args.command != "report" and not args.provider:
        parser.error("Lệnh này cần --provider")
    if args.sample_points is not None and args.sample_points <= 0:
        parser.error("--sample-points phải dương")
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,39}", args.run_id):
        parser.error("--run-id chỉ nhận chữ, số, gạch nối hoặc gạch dưới")
    mode = "full" if args.sample_points is None else f"sample-{args.sample_points}"
    base = OUTPUT / args.run_id / args.study / mode
    if not base.resolve().is_relative_to((ROOT / "outputs").resolve()):
        parser.error("Thư mục thực nghiệm nằm ngoài outputs")
    try:
        if args.command == "report":
            export(base)
            return
        directory = base / args.provider
        study, planned, bank = plan(args.study, args.provider, args.sample_points)
        if args.command == "dry-run":
            print_json({**{k: v for k, v in planned.items() if k not in ("points", "bank_ids")},
                        "points": len(planned["points"]), "bank_episodes": len(bank),
                        "planned_calls_excluding_retries": sum(planned["calls_by_role"].values()),
                        "conditional_roles": [] if args.study == "component" else
                        ["bayesian_v1", "C2", "A_tp_pool", "B_semantic", "MT_BICL"],
                        "directory": str(directory), "api": False})
            return
        identity, upgrade = checkpoint_identity(directory, planned)
        if args.command == "run":
            run_paid(directory, identity, study, bank, upgrade=upgrade)
        elif args.command == "finalize":
            result = finalize(directory, identity, study)
            print_json({"directory": str(directory), "usage": result["usage"], "status": "COMPLETE", "api": False})
        elif args.command == "status":
            book = StageBook(directory, identity, verify_only=True)
            unknown = []
            for path in (directory / "http").glob("*.json"):
                doc = load(path)
                for row in doc["rows"]:
                    if row["status"] == "UNKNOWN":
                        unknown.append({"slot": doc["slot"], "request_id": row["id"]})
            print_json({"directory": str(directory), "completed_points": sum(book.complete("point/" + p["id"]) for p in identity["points"]),
                        "planned_points": len(identity["points"]),
                        "completed_bank_episodes": sum(book.complete("bank/" + key.replace(":", "-")) for key in identity["bank_ids"]),
                        "planned_bank_episodes": len(identity["bank_ids"]), "unknown_requests": unknown,
                        "schema_upgrade": upgrade,
                        "usage": usage_totals(directory, book.signature), "api": False})
        else:
            if not all((args.slot, args.request_id, args.evidence)):
                parser.error("Cần --slot, --request-id và --evidence")
            with PriorRunLock(directory, digest(identity)):
                book = StageBook(directory, identity, verify_only=True)
                ledger = quota(args.provider)
                journal = Calls(directory, book.signature, ledger, None, lambda: None)
                journal.reconcile_not_sent(args.slot, args.request_id, args.evidence)
                ledger.finish(args.request_id, "NOT_SENT", 0)
            print_json({"directory": str(directory), "status": "NOT_SENT", "api": False})
    except Unknown:
        parser.exit(3, "Trạng thái HTTP chưa rõ. Dùng status để lấy slot và UUID đối soát.\n")
    except (Failed, ValueError, FileNotFoundError) as error:
        parser.exit(2, f"Dừng tại checkpoint. {error}\n")


if __name__ == "__main__":
    main()
