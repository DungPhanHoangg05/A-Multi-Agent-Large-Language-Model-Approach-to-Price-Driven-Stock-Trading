"""Identity, envelope và checkpoint riêng của replica; không thay release hiện hành."""

from __future__ import annotations

import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import platform
import random
import subprocess
from typing import Any

import numpy as np
import torch

from core.mt_bicl_bank import content_hash

NAMESPACE = Path("outputs/bayesian_benchmark/mt_bicl/replicas/full_r1")
PROTOCOL = Path("docs/plan/week11/mt_bicl_replica_full_r1.json")
RECIPE_COMMIT = "00b24679f63d491c15cda6be0bc9a2c412651f93"


def file_hash(path: Path) -> str:
    """Băm streaming để không đọc toàn checkpoint lớn vào RAM."""
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def path_for(root: Path, name: str) -> Path:
    """Chỉ cho artifact trong namespace replica, chặn traversal và symlink."""
    parts = name.split("/")
    if not name or any(part in ("", ".", "..") for part in parts) or ":" in name or "\\" in name:
        raise ValueError("Path replica không hợp lệ")
    base = (root / NAMESPACE).resolve()
    path = root / NAMESPACE / name
    if not path.resolve().is_relative_to(base) or any(p.is_symlink() for p in (path, *path.parents) if p != root.parent):
        raise ValueError("Path replica thoát namespace hoặc qua symlink")
    return path


def read(path: Path) -> Any:
    """Kiểm checksum envelope, không lấy checksum thay cho kiểm provenance ở caller."""
    value = json.loads(path.read_bytes())
    if set(value) != {"payload", "sha256"} or content_hash(value["payload"]) != value["sha256"]:
        raise ValueError("Envelope replica không hợp lệ: " + path.name)
    return value["payload"]


def write(path: Path, payload: Any, *, mutable: bool = False) -> None:
    """Ghi atomic; immutable artifact chỉ resume khi payload giống hệt."""
    if path.exists() and not mutable:
        if read(path) != payload:
            raise ValueError("Không ghi đè artifact replica: " + path.name)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    value = {"payload": payload, "sha256": content_hash(payload)}
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, sort_keys=True, allow_nan=False, separators=(",", ":"))
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


def load_protocol(root: Path) -> dict[str, Any]:
    """Buộc protocol và source đã neo Git trước mọi fit hoặc optimizer production."""
    protocol = json.loads((root / PROTOCOL).read_bytes())
    anchored = subprocess.check_output(["git", "show", "HEAD:" + PROTOCOL.as_posix()], cwd=root)
    if anchored != (root / PROTOCOL).read_bytes():
        raise ValueError("Protocol replica chưa neo Git hoặc bị sửa")
    if (protocol["training"]["model_seeds"] != [17, 42, 73]
            or protocol["training"]["optimizer_steps_per_seed"] != 5000
            or protocol["training"]["checkpoint_every_steps"] != 250
            or protocol["training"]["metric_early_stop"] is not False
            or protocol["authorization"] != {"teacher_fit": True, "student_training": True, "llm_api": False, "historical_evaluation": False}):
        raise ValueError("Protocol replica khác phạm vi đã khóa")
    for name, expected in protocol["source_sha256"].items():
        if file_hash(root / name) != expected:
            raise ValueError("Source replica đã đổi: " + name)
        git_bytes = subprocess.check_output(["git", "show", "HEAD:" + name], cwd=root)
        actual = (root / name).read_bytes()
        if git_bytes != actual and git_bytes != actual.replace(b"\r\n", b"\n"):
            raise ValueError("Source chưa commit: " + name)
    for name, expected in protocol["data_sha256"].items():
        if file_hash(root / name) != expected:
            raise ValueError("Dữ liệu replica đã đổi: " + name)
    if platform.python_version() != "3.13.5":
        raise ValueError("Replica cần Python3.13.5")
    for name, expected in protocol["runtime"].items():
        if version(name) != expected:
            raise ValueError("Runtime replica đã đổi: " + name)
    return protocol


def configure(seed: int, *, cuda: bool) -> torch.device:
    """FP32 deterministic; chỉ CLI người dùng được yêu cầu CUDA production."""
    if os.environ.get("CUBLAS_WORKSPACE_CONFIG") != ":4096:8":
        raise ValueError("Đặt CUBLAS_WORKSPACE_CONFIG=:4096:8 trước CUDA")
    if cuda and not torch.cuda.is_available():
        raise ValueError("Train/pilot production cần CUDA")
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if cuda:
        torch.cuda.manual_seed_all(seed)
    torch.use_deterministic_algorithms(True)
    torch.backends.cudnn.benchmark = False
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    torch.set_float32_matmul_precision("highest")
    torch.set_num_threads(1)
    return torch.device("cuda:0" if cuda else "cpu")


def rng_state() -> dict[str, Any]:
    """Chỉ tensor/primitive để checkpoint đọc bằng weights_only=True."""
    value = np.random.get_state()
    return {"python": random.getstate(), "numpy": {"name": value[0], "keys": torch.tensor(value[1].astype(np.int64)),
            "position": value[2], "has_gauss": value[3], "cached_gaussian": value[4]},
            "torch": torch.get_rng_state(), "cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_initialized() else []}


def restore_rng(value: dict[str, Any]) -> None:
    """Phục hồi sau load optimizer, ngay trước step tiếp theo."""
    random.setstate(value["python"])
    state = value["numpy"]
    np.random.set_state((state["name"], state["keys"].numpy().astype(np.uint32), state["position"], state["has_gauss"], state["cached_gaussian"]))
    torch.set_rng_state(value["torch"].cpu())
    if value["cuda"]:
        torch.cuda.set_rng_state_all([v.cpu() for v in value["cuda"]])


def tree_hash(value: Any) -> str:
    """Băm đầy đủ model/optimizer/RNG, dùng nhận diện checkpoint orphan sau crash."""
    if isinstance(value, torch.Tensor):
        tensor = value.detach().cpu().contiguous()
        return hashlib.sha256(str(tensor.dtype).encode() + str(tuple(tensor.shape)).encode() + tensor.numpy().tobytes()).hexdigest()
    if isinstance(value, dict):
        return content_hash([[str(k), tree_hash(v)] for k, v in sorted(value.items(), key=lambda item: str(item[0]))])
    if isinstance(value, (list, tuple)):
        return content_hash([tree_hash(v) for v in value])
    return content_hash(value)


def save_checkpoint(path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    """Không ghi đè checkpoint; orphan chỉ adopt nếu toàn payload replay trùng."""
    fingerprint = tree_hash(payload)
    if path.exists():
        old = torch.load(path, map_location="cpu", weights_only=True)
        if tree_hash(old) != fingerprint:
            raise ValueError("Checkpoint orphan khác replay")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".tmp")
        torch.save(payload, temporary)
        temporary.replace(path)
    return {"sha256": file_hash(path), "bytes": path.stat().st_size, "payload_sha256": fingerprint}


def load_checkpoint(path: Path, expected: dict[str, Any]) -> dict[str, Any]:
    """Kiểm receipt durable trước deserialize tensor/optimizer."""
    if file_hash(path) != expected["sha256"] or path.stat().st_size != expected["bytes"]:
        raise ValueError("Checkpoint khác receipt")
    value = torch.load(path, map_location="cpu", weights_only=True)
    if tree_hash(value) != expected["payload_sha256"]:
        raise ValueError("Checkpoint khác payload fingerprint")
    return value
