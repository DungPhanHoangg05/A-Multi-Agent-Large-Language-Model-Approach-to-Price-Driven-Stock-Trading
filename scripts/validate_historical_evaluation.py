"""Nghiệm thu H05 offline theo phạm vi, không fit production hoặc gọi API."""

from __future__ import annotations

import argparse
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path
import py_compile
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from core.historical_evaluation_audit import verify_runtime
from core.historical_evaluation_context import ContextBank
from core.historical_evaluation_data import HistoricalData
from core.historical_evaluation_journal import load, save
from core.historical_evaluation_protocol import INPUTS, MODEL, PROTOCOL, binding, digest
from core.historical_evaluation_runner import Regimes

REPORT = Path("docs/plan/week11/historical_evaluation_validation.json")
TESTS = (
    "test_historical_adapter_journal", "test_historical_adapter_leakage",
    "test_historical_adapter_methods", "test_historical_adapter_runner", "test_historical_adapter_transport",
    "test_historical_regime_prefix_leakage", "test_historical_evaluation_protocol",
    "test_historical_evaluation_leakage", "test_historical_evaluation_statistics",
    "test_mt_bicl_adapter_leakage", "test_mt_bicl_features_leakage", "test_mt_bicl_utility",
    "test_historical_validation_leakage",
)
COMPILE = ("scripts/validate_historical_evaluation.py", "tests/test_historical_validation_leakage.py")


def bindings() -> dict:
    """Khóa code/test/helper của nghiệm thu và input/runtime đã dùng, không chứa credential."""
    names = {str(PROTOCOL), str(INPUTS), str(MODEL), "docs/plan/week11/historical_evaluation_runtime.json",
             "outputs/historical_reevaluation/h04_assets/prepared.json", *COMPILE}
    names.update("tests/" + name + ".py" for name in TESTS)
    names.update(str(p.relative_to(ROOT)) for p in (ROOT / "tests").glob("*support.py"))
    names.add("tests/test_regime_features.py")
    return {name: binding(ROOT, name) for name in sorted(names)}


def prefixes(data: HistoricalData) -> list[dict]:
    """Kiểm mỗi artifact đúng prefix/hash và phân loại được tại đúng ngày, không refit."""
    directory = ROOT / "outputs/historical_reevaluation/h04_assets/legacy_regimes"
    regimes = Regimes(data, directory)
    regimes.preflight()
    records = []
    for index, cutoff in enumerate(sorted({r["date"] for r in data.inputs["history"]}), 1):
        path = directory / (cutoff + ".json")
        metadata = load(path)["metadata"]
        records.append({**binding(ROOT, path.relative_to(ROOT)), "date": cutoff,
                        "method": metadata["classification_method"], "regime": regimes.get(cutoff, historical=True)})
        if index % 100 == 0:
            print(f"Đã kiểm {index} prefix HMM lịch sử.", flush=True)
    return records


def audit_contexts(data: HistoricalData) -> dict:
    """Dựng lại toàn grid với query-y bị khóa; chỉ kiểm hợp đồng và frozen forward."""
    expected = load(ROOT / "outputs/historical_reevaluation/h04_assets/prepared.json")["contexts"]
    context = ContextBank(data, lambda _: False)
    rows, forward_count = [], 0
    validate = data.scope.module("mt_bicl_contracts").validate_context
    for index, unit in enumerate(sorted(data.inputs["grid"], key=lambda r: (r["date"], r["symbol"])), 1):
        episode = context.build(unit["symbol"], unit["date"])
        validate(episode)
        if episode["status"] == "AVAILABLE":
            context.predict(episode)
            forward_count += 1
        rows.append({"id": unit["id"], "status": episode["status"], "K": episode["K"], "m": episode["m"],
                     "context_sha256": digest(episode), "ood": unit["symbol"] not in ("FPT", "MWG", "VCB", "VNM"),
                     "reasons": episode["reasons"]})
        if index % 100 == 0:
            print(f"Đã kiểm {index}/1.020 context không có nhãn query.", flush=True)
    if rows != expected:
        raise ValueError("Context H05 khác preview H04 đã khóa")
    return {"count": len(rows), "preview_sha256": digest(rows), "frozen_forwards": forward_count,
            "student_tensor_sha256": context.student.fingerprint, "query_outcomes_opened": False}


def main() -> None:
    """Chỉ ghi PASS khi asset trước/sau, tests và Python thay đổi đều hợp lệ."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="Chỉ đối soát receipt/hash đã neo Git, không chạy lại tests.")
    args = parser.parse_args()
    import torch
    from threadpoolctl import threadpool_limits
    torch.set_num_threads(1)
    with threadpool_limits(limits=1):
        verify_runtime(ROOT)
        data = HistoricalData(ROOT)
        sources = bindings()
        models = prefixes(data)
        if args.verify:
            if (ROOT / REPORT).read_bytes() != subprocess.check_output(["git", "show", "HEAD:" + REPORT.as_posix()], cwd=ROOT):
                raise ValueError("Receipt H05 chưa neo Git hoặc đã đổi byte")
            result = load(ROOT / REPORT)
            if (result["status"] != "PASS" or result["bindings"] != sources or result["prefix_models"] != models
                    or binding(ROOT, result["test_log"]["path"]) != result["test_log"]):
                raise ValueError("Source/input/model khác receipt H05")
            print("H05: RECEIPT_HASH_VERIFIED; không chạy lại tests, không cấp quyền API.")
            return
        contexts = audit_contexts(data)
        for name in COMPILE:
            py_compile.compile(str(ROOT / name), doraise=True)
        suite = unittest.defaultTestLoader.loadTestsFromNames(TESTS)
        log = ROOT / "outputs/historical_reevaluation/h04_assets/h05_validation.log"
        with log.open("w", encoding="utf-8") as handle, redirect_stdout(handle):
            checked = unittest.TextTestRunner(stream=handle, verbosity=2).run(suite)
        canonical = re.sub(r"Ran (\d+) tests in [0-9.]+s", r"Ran \1 tests (thời gian không tham gia checksum)",
                           log.read_text(encoding="utf-8"))
        log.write_text(canonical, encoding="utf-8", newline="\n")
        if not checked.wasSuccessful() or checked.skipped or checked.testsRun == 0:
            raise ValueError("Kiểm thử H05 chưa PASS đầy đủ; xem " + str(log.relative_to(ROOT)))
        verify_runtime(ROOT)
        data.verify_sources()
        if bindings() != sources or any(binding(ROOT, r["path"])["sha256"] != r["sha256"] for r in models):
            raise ValueError("Asset/source thay đổi trong lúc nghiệm thu")
        result = {"version": "historical_h05_validation_v1", "status": "PASS", "bindings": sources,
                  "prefix_models": models, "prefix_count": len(models),
                  "prefix_methods": dict(Counter(r["method"] for r in models)), "contexts": contexts,
                  "test_modules": list(TESTS), "tests_passed": checked.testsRun, "compiled": list(COMPILE),
                  "llm_calls": 0, "production_fit": False, "api_released": False,
                  "test_log": binding(ROOT, log.relative_to(ROOT))}
        if (ROOT / REPORT).exists() and load(ROOT / REPORT) != result:
            raise ValueError("Receipt H05 đã có kết quả khác; cần revision, không ghi đè")
        save(ROOT / REPORT, result)
        print(f"H05: PASS; {checked.testsRun} test, {len(models)} prefix, {contexts['count']} context; API vẫn khóa.")


if __name__ == "__main__":
    main()
