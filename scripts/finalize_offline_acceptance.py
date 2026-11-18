"""Khóa và nghiệm thu đường nghiên cứu finalize bằng fixture cục bộ."""
from __future__ import annotations

import argparse
import hashlib
from importlib.metadata import version
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.finalize_bank_signals import check_bindings
from core.finalize_budget_archive import Archive
from core.finalize_budget_quota import ORG
from core.finalize_serving_resources import FinalizedResources
from core.groq_pacing import tokenizer_cached
from core.historical_evaluation_journal import load, save
from core.unified_contracts import digest, json_bytes
from core.unified_experiment import runtime_identity, source_identity
from core.unified_preflight_assets import write_new
from core.unified_protocol import binding, read
from scripts.finalize_offline_fixture import Cases, capture, replay, require
from scripts.prepare_finalize_api_budget import CONTRACT, LEDGER, check_rows, recorded_usage, study
from scripts.verify_original_fix_parity import deny_external_network

FIN09_SHA256 = "ee82dfe54307b97014e9d9ea088176a33904900ce7ec9a04338fd249cd768048"
RECEIPT = "docs/plan/week12/finalize_offline_acceptance_v1.json"
VERSION = "finalize_offline_acceptance_v1"
GATES = {
    "pit": ("tests", "test_finalize_*leakage.py"),
    "economic": ("tests", "test_account_pnl.py"),
    "recovery": ("tests", "test_unified_execution_*.py"),
    "serving": ("tests/serving_runtime", "test_*.py"),
    "budget": ("tests", "test_groq_pacing.py"),
    "prompt": ("tests", "test_backtest_token_budget.py"),
    "protocol": ("tests", "test_unified_contract_integration.py"),
    "ledger": ("tests", "test_finalize_api_budget.py"),
}


def freeze(root: Path) -> tuple[dict, dict, FinalizedResources]:
    """Đối soát nguồn/runtime/profile trước khi mở journal hoặc fixture transport."""
    frozen = binding(root, LEDGER)
    budget = read(root, LEDGER, True)
    runtime = runtime_identity()
    require(frozen["sha256"] == FIN09_SHA256 and budget["runtime"] == runtime
            and runtime["python"] == "3.13.5" and tokenizer_cached()
            and budget["quota"]["org_slot"] == ORG and budget["attempt_cap_per_slot"] == 3
            and budget["execution_permitted"] is False and budget["bank_new_executions"] == 0
            and budget["billing"] == {"tier_user_attested": "FREE", "paid_allowed": False, "spend_limit_usd": 0},
            "Runtime hoặc kế hoạch FIN09 không khớp scope đã khóa")
    points, _, smoke, config = study(root)
    check_rows(budget["slots"], points, smoke)
    require(config == budget["model_options"], "Model/options không khớp FIN02 và FIN09")
    check_bindings(root, budget["source_bindings"])
    check_bindings(root, budget["quota"]["bank_quota_sources"])
    resources = FinalizedResources(root)
    resources.verify()
    sources = (".python-version", CONTRACT, "scripts/finalize_offline_acceptance.py",
               "scripts/finalize_offline_fixture.py", "scripts/finalize_serving_preview.py",
               "scripts/prepare_finalize_api_budget.py", "scripts/verify_original_fix_parity.py",
               "scripts/run_unified_experiment.py")
    lock = {"version": VERSION, "scope": "OFFLINE_FIXTURE", "org_slot": ORG, "attempt_cap_per_slot": 3,
            "spend_limit_usd": 0, "execution_permitted": False, "budget": frozen,
            "code_sha256": source_identity(root), "entrypoint_bindings": [binding(root, name) for name in sources],
            "resources_sha256": digest(resources.document()), "resource_pin_count": len(resources.pins),
            "runtime": {**runtime, **{name: version(name) for name in
                ("httpx", "jsonschema", "matplotlib", "tiktoken", "hmmlearn", "scikit-learn")}},
            "point_count": len(points), "repeats": budget["repeats"], "model_options": config}
    return lock, budget, resources


def evidence(root: Path, log_dir: Path) -> dict:
    """Giữ số ca, hash log gốc và pin test đã dùng để chấp nhận."""
    groups = {}
    for name, (folder, pattern) in GATES.items():
        raw = (log_dir/f"fin10_{name}.log").read_bytes()
        decoded = raw.decode("utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8")
        matches = re.findall(r"^Ran (\d+) tests? in [\d.]+s\s*\n\s*OK[ \t]*\r?$", decoded, re.M)
        require(len(matches) == 1 and int(matches[0]) > 0, "Nhóm kiểm thử chưa đạt: " + name)
        paths = sorted((root/folder).glob(pattern))
        require(bool(paths), "Thiếu nguồn test: " + name)
        groups[name] = {"count": int(matches[0]), "result": "PASS", "start_dir": folder, "pattern": pattern,
                        "log_sha256": hashlib.sha256(raw).hexdigest(),
                        "sources": [binding(root, path.relative_to(root).as_posix()) for path in paths]}
    return groups


def verify_record(doc: dict, lock: dict) -> None:
    """Không nhầm receipt đối chứng với quyền gọi hosted hoặc chứng nhận PIT vendor."""
    sample, cold = doc["fixture"], doc["cold_replay"]
    require(doc["status"] == "PASS_OFFLINE_FIN10" and doc["lock"] == lock
            and doc["execution_permitted"] is False and doc["hosted_requests"] == 0
            and doc["account_free_remaining_confirmed"] is False and doc["independent_price_pit_certified"] is False
            and sample["future_poison"]["prepared_slots_equal"] == 24
            and sample["smoke_stats"]["forecasts"] == 8 and sample["research_stats"]["forecasts"] == 48
            and sample["research_stats"]["vision_reused"] == 2 and sample["research_stats"]["stop_after_raw_preserves_first_uuid"]
            and sample["research_stats"]["completed_slot_missing_raw_blocks_dispatch"]
            and sample["unknown_stats"]["unknown_reserve_preserved"] and sample["unknown_stats"]["manual_uuid_reconciliation"]
            and cold == {"smoke_sha256": digest(sample["smoke"]), "research_sha256": digest(sample["research"]),
                         "fixture_dispatches": 0}, "Receipt khác nguồn hoặc bằng chứng FIN10")
    require(set(doc["gates"]) == set(GATES) and doc["tests_passed"] == sum(g["count"] for g in doc["gates"].values()),
            "Thiếu nhóm kiểm thử áp dụng")
    for name, gate in doc["gates"].items():
        require((gate["start_dir"], gate["pattern"]) == GATES[name] and gate["result"] == "PASS" and gate["count"] > 0,
                "Nguồn hoặc số ca kiểm thử khác FIN10")
        check_bindings(ROOT, gate["sources"])


def main() -> None:
    """Chạy hai tiến trình Python riêng để kiểm cold replay rồi seal bằng chứng."""
    deny_external_network()
    import torch
    torch.set_num_threads(1)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("capture", "replay", "seal", "check"))
    parser.add_argument("--workspace", type=Path, default=ROOT/"tmp"/"fin10_acceptance")
    args = parser.parse_args()
    lock, budget, resources = freeze(ROOT)
    workspace = args.workspace.resolve()
    if args.mode == "check":
        result = read(ROOT, RECEIPT, True)
        verify_record(result, lock)
    elif args.mode == "seal":
        sample = load(workspace/"fixture.json")
        cold = load(workspace/"replay.json")
        require(sample["lock"] == cold["lock"] == lock and cold["fixture_sha256"] == digest(sample["result"]),
                "Nguồn đổi giữa capture, replay và nghiệm thu")
        gates = evidence(ROOT, ROOT/"tmp")
        result = {"version": VERSION, "status": "PASS_OFFLINE_FIN10", "lock": lock, "fixture": sample["result"],
                  "cold_replay": cold["result"], "gates": gates, "tests_passed": sum(g["count"] for g in gates.values()),
                  "execution_permitted": False, "hosted_requests": 0, "account_free_remaining_confirmed": False,
                  "independent_price_pit_certified": False,
                  "release_blockers": ["ACCOUNT_FREE_LIMITS_AND_REMAINING_UNCONFIRMED", "FIN11_HOSTED_GRANT_PENDING"]}
        verify_record(result, lock)
        write_new(ROOT/RECEIPT, json_bytes({"payload": result, "sha256": digest(result)}))
    else:
        cohort, variants, _, _ = study(ROOT)
        archive = Archive(ROOT)
        require(recorded_usage(archive) == budget["historical_usage_by_role"]
                and all(r["old"] == (archive.candidate(r["slot"]) if r["phase"] == "RESEARCH" else None)
                        for r in budget["slots"]), "Tham chiếu archive khác FIN09")
        cases = Cases(resources, archive, lock, budget, cohort, variants, workspace)
        if args.mode == "capture":
            require(not workspace.joinpath("fixture.json").exists(), "Workspace fixture đã có kết quả")
            result = capture(cases)
            save(workspace/"fixture.json", {"lock": lock, "result": result})
        else:
            sample = load(workspace/"fixture.json")
            require(sample["lock"] == lock, "Nguồn capture khác runtime của replay")
            result = replay(cases, sample["result"])
            save(workspace/"replay.json", {"lock": lock, "fixture_sha256": digest(sample["result"]), "result": result})
    print({"mode": args.mode, "sha256": digest(result), "resource_pins": lock["resource_pin_count"], "hosted_requests": 0})


if __name__ == "__main__":
    main()
