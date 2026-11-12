"""Khóa nguồn U09, chạy phân tích offline và cold consumer so nguyên byte artifact."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from core.historical_evaluation_journal import load, save
from core.prior_run_lock import PriorRunLock
from core.unified_contracts import digest
from core.unified_live.release import anchored, binding
from core.unified_analysis.inputs import PACKAGE, PACKAGE_SHA, PROTOCOL, accept, frames
from core.unified_analysis.analysis import analyze
from core.unified_analysis.output import write_outputs

DOC = "docs/plan/week12/"
RUNTIME = DOC + "unified_analysis_runtime.json"
CHECKS = DOC + "unified_analysis_checks.json"
ACCEPTANCE = DOC + "unified_analysis_acceptance.json"
DIRECTORY = "outputs/unified_integration/u09_analysis_r1"
FOLDERS = ("core/unified_analysis", "scripts/unified_analysis", "tests/unified_analysis")


def sources(root: Path) -> dict[str, Any]:
    """Pin chỉ module mới; 718 pin cha tiếp tục được đối soát bởi input consumer."""
    return {p.relative_to(root).as_posix(): binding(root, p.relative_to(root).as_posix())
        for folder in FOLDERS for p in sorted((root / folder).rglob("*")) if p.is_file() and "__pycache__" not in p.parts}


def freeze(root: Path) -> dict[str, Any]:
    """Khóa checks trước phân tích, không sửa protocol hoặc dataset khi đã có outcome."""
    from scripts.unified_live.run import create
    checks = load(root / CHECKS)
    pins = sources(root)
    if (checks["status"] != "PASS" or checks["sources"] != pins or checks["failures"] or checks["errors"]
            or checks["skips"] or checks["tests"] != len(set(checks["test_ids"])) or not checks["compiled"]):
        raise ValueError("Checks U09 chưa PASS trên nguồn hiện hành")
    runtime = {"version": "unified_analysis_runtime_v1", "sources": pins, "checks": binding(root, CHECKS),
        "u08_package_sha256": PACKAGE_SHA, "protocol": binding(root, PROTOCOL), "namespace": DIRECTORY,
        "api": False, "training": False, "primary_changes_after_outcomes": False}
    create(root / RUNTIME, runtime)
    path = root / RUNTIME; path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n"))
    return runtime


def require(root: Path) -> dict[str, Any]:
    """Chỉ nhận manifest đã neo Git và protocol v2 nguyên byte."""
    runtime = anchored(root, RUNTIME)
    anchored(root, CHECKS)
    if (runtime["sources"] != sources(root) or runtime["checks"] != binding(root, CHECKS)
            or runtime["protocol"] != binding(root, PROTOCOL) or runtime["u08_package_sha256"] != PACKAGE_SHA
            or runtime["api"] or runtime["training"] or runtime["primary_changes_after_outcomes"]):
        raise ValueError("Nguồn/runtime/protocol U09 đã đổi")
    return runtime


def artifact_bindings(directory: Path) -> dict[str, Any]:
    """Loại run lock/receipt khỏi tập artifact phân tích xác định."""
    return {p.name: {"bytes": p.stat().st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
        for p in sorted(directory.iterdir()) if p.is_file() and p.suffix in (".csv", ".json", ".md", ".svg", ".png")
        and p.name not in ("receipt.json", "run.owner.json", "run.recovery.json")}


def calculate(root: Path, destination: Path) -> dict[str, Any]:
    """Phân tích từ archive đã seal; không ghi vào journal research hoặc frozen assets."""
    bundle = accept(root)
    result, artifacts = analyze(bundle, frames(root, bundle))
    write_outputs(destination, result, artifacts)
    return result


def run(root: Path) -> dict[str, Any]:
    """Chỉ tạo namespace U09 mới; có receipt thì yêu cầu cold verify thay overwrite."""
    runtime = require(root)
    directory = root / DIRECTORY
    if (directory / "receipt.json").exists(): raise ValueError("U09 đã có receipt; dùng verify, không ghi đè evidence")
    directory.mkdir(parents=True, exist_ok=True)
    if artifact_bindings(directory): raise ValueError("Namespace U09 đã có artifact chưa nghiệm thu")
    with PriorRunLock(directory, digest(runtime)):
        result = calculate(root, directory)
        receipt = {"status": "PASS_U09_ANALYSIS", "runtime_sha256": digest(runtime),
            "input_identity": result["input_identity"], "artifacts": artifact_bindings(directory),
            "new_api_calls": 0, "training": False, "cold_replay": "PENDING"}
        save(directory / "receipt.json", receipt)
    return receipt


def verify(root: Path) -> dict[str, Any]:
    """Tiến trình lạnh tái dựng mọi bảng/figure; không tin summary tự khai hoặc receipt thiếu file."""
    runtime = require(root); directory = root / DIRECTORY
    receipt = load(directory / "receipt.json")
    if receipt["runtime_sha256"] != digest(runtime) or receipt["status"] != "PASS_U09_ANALYSIS": raise ValueError("Receipt U09 khác nguồn")
    with PriorRunLock(directory, digest(runtime)), TemporaryDirectory(prefix="u09-cold-") as temporary:
        actual = artifact_bindings(directory)
        if actual != receipt["artifacts"]: raise ValueError("Artifact khác receipt U09")
        result = calculate(root, Path(temporary))
        rebuilt = artifact_bindings(Path(temporary))
        if rebuilt != actual or result["input_identity"] != receipt["input_identity"]:
            raise ValueError("Cold replay U09 không khớp nguyên byte")
        return {"status": "PASS_U09_COLD_REPLAY", "runtime_sha256": digest(runtime),
            "u08_package_sha256": PACKAGE_SHA, "receipt_sha256": digest(receipt),
            "artifact_count": len(actual), "artifacts": actual, "points": 102, "forecast_slots": 2448,
            "new_api_calls": 0, "training": False, "byte_identical": True}
