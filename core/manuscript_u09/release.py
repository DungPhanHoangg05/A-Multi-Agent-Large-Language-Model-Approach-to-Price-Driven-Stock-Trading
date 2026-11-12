"""Release U09 cho bài báo: namespace mới, chống ghi đè và cold verify xác định."""
from __future__ import annotations

from importlib.metadata import version
import os
from pathlib import Path
import platform
import shutil
import subprocess
from tempfile import TemporaryDirectory
from typing import Any

from core.manuscript_u09.render import LABELS, render
from core.manuscript_u09.sources import (ACCEPTANCE, PACKAGE, PREFIX, binding, decoded,
    encoded, load, require, safe_name, semantic)

RELEASE = "outputs/revision/u09_manuscript_assets_v1"
INSTALL = "paper/generated/u09"
SOURCES = ("core/manuscript_u09/.gitattributes", "core/manuscript_u09/__init__.py",
    "core/manuscript_u09/sources.py", "core/manuscript_u09/render.py", "core/manuscript_u09/release.py",
    "scripts/manuscript_u09/.gitattributes", "scripts/manuscript_u09/run.py",
    "tests/manuscript_u09/.gitattributes", "tests/manuscript_u09/test_export.py")


def runtime() -> dict[str, Any]:
    """Ghi đúng môi trường render và font; không giả định runtime inference hiện hành."""
    from matplotlib import font_manager
    font = Path(font_manager.findfont("DejaVu Sans", fallback_to_default=False))
    return {"python": platform.python_version(),
        "packages": {name: version(name) for name in ("matplotlib", "numpy", "pillow", "fonttools")},
        "font": {"name": font.name, **binding(font.read_bytes())}}


def sources(root: Path) -> dict[str, Any]:
    """Khóa source generator/test riêng; không đổi manifest 729 pin lịch sử."""
    return {name: binding((root / name).read_bytes()) for name in SOURCES}


def destination(root: Path, release: str) -> Path:
    """Chỉ release mới trực tiếp dưới outputs/revision, không nhận namespace lịch sử."""
    safe_name(release)
    path = root / release
    require(path.resolve().parent == (root / "outputs/revision").resolve()
        and path.name.startswith("u09_manuscript_assets_"), "Release phải dùng namespace u09_manuscript_assets mới")
    require(all(not p.is_symlink() for p in (path, *path.parents)), "Release đi qua symlink")
    return path


def commit(root: Path) -> str:
    """Ghi commit nguồn và source hash riêng, không tự commit hoặc đổi branch."""
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root).decode().strip()


def build(root: Path, release: str = RELEASE, *, artifact_only: bool = False) -> dict[str, Any]:
    """Sinh một lần; render/validate xong trước khi đặt release và cài namespace paper mới."""
    root = root.resolve()
    folder = destination(root, release)
    installed = root / INSTALL
    require(not folder.exists(), "Release đã có; dùng verify, không ghi đè")
    require(artifact_only or not installed.exists(), "Namespace paper U09 đã có; không ghi đè")
    require(artifact_only or all(not p.is_symlink() for p in (installed, *installed.parents)), "Paper đi qua symlink")
    bundle = load(root)
    outputs = render(bundle)
    installed_names = [name for name in outputs if Path(name).suffix in (".tex", ".png", ".svg")]
    manifest = {"version": "u09_manuscript_assets_v1", "status": "PASS_U09_MANUSCRIPT_ASSETS",
        "study_id": "unified_u08_u09_r1", "generator_source_commit": commit(root),
        "historical_source_commit": bundle["historical_source_commit"], "sources": sources(root),
        "inputs": bundle["input_bindings"], "input_identity": bundle["result"]["input_identity"],
        "acceptance": ACCEPTANCE, "historical_gate": "F01_PASS_U09_COLD_REPLAY_729_SOURCES_15_ARTIFACTS",
        "runtime": runtime(), "outputs": {name: binding(raw) for name, raw in outputs.items()},
        "installation": {"namespace": INSTALL, "enabled": not artifact_only, "members": installed_names},
        "numeric_lineage": "numeric_cells.json",
        "derived_support": {"definition": "COUNT_FROZEN_SHARED_AND_PREDICTIONS_ONLY_NO_NEW_METRICS",
            "predictions": {"package": PACKAGE, "member": PREFIX+"predictions.csv"},
            "shared_slots": "points.json/source_member in pinned U08 archive"},
        "figure": {"input": PREFIX+"contrasts.csv", "units": "percentage_points",
            "rows": "ten predeclared return contrasts; both baselines; original order", "new_resampling": False},
        "method_labels": LABELS, "macro_prefix": "Unified",
        "new_api_calls": 0, "training": False, "metric_reestimation": False,
        "native_rowwise_causal_gate": "FAIL", "whole_system_causal_gate": "NOT_CERTIFIED"}
    manifest["sha256"] = semantic(manifest)
    folder.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".u09-manuscript-", dir=folder.parent) as temporary:
        stage = Path(temporary) / "release"
        for name, raw in outputs.items():
            path = stage / "artifacts" / safe_name(name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        (stage / "manifest.json").write_bytes(encoded(manifest))
        if not artifact_only:
            install_stage = Path(temporary) / "install"
            install_stage.mkdir()
            for name in installed_names:
                shutil.copyfile(stage / "artifacts" / name, install_stage / name)
            installed.parent.mkdir(parents=True, exist_ok=True)
        os.rename(stage, folder)
        if not artifact_only:
            os.rename(install_stage, installed)
    return {"status": manifest["status"], "release": release, "artifacts": len(outputs),
        "installed": len(installed_names) if not artifact_only else 0, "new_api_calls": 0}


def verify(root: Path, release: str = RELEASE) -> dict[str, Any]:
    """Đối soát release, nguồn, runtime, cài đặt và rebuild nguyên byte trong bộ nhớ."""
    root = root.resolve()
    folder = destination(root, release)
    manifest = decoded((folder / "manifest.json").read_bytes())
    unsigned = {key: value for key, value in manifest.items() if key != "sha256"}
    require(semantic(unsigned) == manifest["sha256"], "Manifest release sai self-digest")
    require(manifest["sources"] == sources(root), "Source generator/test đã đổi sau release")
    require(manifest["runtime"] == runtime(), "Runtime/font render khác release")
    expected = manifest["outputs"]
    actual_names = {p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_file()}
    require(actual_names == {"manifest.json", *["artifacts/" + n for n in expected]}, "Release có artifact thừa/thiếu")
    for name, row in expected.items():
        path = folder / "artifacts" / safe_name(name)
        require(binding(path.read_bytes()) == row, "Artifact release đổi: " + name)
    if manifest["installation"]["enabled"]:
        installed = root / INSTALL
        names = manifest["installation"]["members"]
        require({p.relative_to(installed).as_posix() for p in installed.rglob("*") if p.is_file()} == set(names),
            "Paper U09 thừa/thiếu file")
        for name in names:
            require(binding((installed / safe_name(name)).read_bytes()) == expected[name], "Paper U09 khác release: " + name)
    bundle = load(root)
    require(bundle["input_bindings"] == manifest["inputs"]
        and bundle["result"]["input_identity"] == manifest["input_identity"], "Input identity khác release")
    rebuilt = render(bundle)
    require({n: binding(raw) for n, raw in rebuilt.items()} == expected, "Rebuild không khớp nguyên byte")
    return {"status": "PASS_U09_MANUSCRIPT_COLD_REPLAY", "artifacts": len(expected),
        "numeric_cells": len(decoded(rebuilt["numeric_cells.json"])), "byte_identical": True,
        "new_api_calls": 0, "training": False, "metric_reestimation": False}
