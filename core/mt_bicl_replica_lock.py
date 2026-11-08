"""Phục hồi metadata khóa trước fit; không nới guard khóa của run đã có kết quả."""

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import subprocess
from typing import Any
from uuid import UUID

from core.mt_bicl_bank import content_hash
from core.mt_bicl_replica_io import NAMESPACE, PROTOCOL, file_hash, path_for, read, write
from core.prior_run_lock import host_boot, lock_handle, process_start, utc_now

OWNER_KEYS = {"host_id", "boot_id", "pid", "process_start_time", "owner_uuid", "acquired_at",
              "run_signature", "owner_state", "released_at"}
PREFIT_FILES = {"inputs/dense_bank.json", "run.lock", "run.owner.json", "run.recovery.json"}


def previous_protocol(root: Path, signature: str, current: dict[str, Any]) -> str:
    """Chỉ nhận signature của protocol đã commit với recipe/data/runtime không đổi."""
    commits = subprocess.check_output(["git", "log", "--all", "--format=%H", "--", PROTOCOL.as_posix()], cwd=root).decode().splitlines()
    for commit in commits:
        value = subprocess.run(["git", "show", f"{commit}:{PROTOCOL.as_posix()}"], cwd=root, capture_output=True, check=False)
        if value.returncode:
            continue
        candidate = json.loads(value.stdout)
        if content_hash(candidate) != signature:
            continue
        old = {k:v for k,v in candidate.items() if k != "source_sha256"}
        new = {k:v for k,v in current.items() if k != "source_sha256"}
        if old != new:
            raise ValueError("Protocol trước khác recipe/data/runtime; cần namespace revision riêng")
        return commit
    raise ValueError("Signature owner không thuộc protocol đã neo Git; không tự sửa metadata")


def require_prefit(directory: Path) -> list[str]:
    """Từ chối cả directory rỗng nếu prepare/pilot/train đã bắt đầu tạo output."""
    files = []
    for path in directory.rglob("*"):
        relative = path.relative_to(directory).as_posix()
        if path.is_symlink():
            raise ValueError("Không phục hồi khóa qua symlink")
        if relative == "lock_history" or relative.startswith("lock_history/"):
            continue
        if path.is_dir():
            if relative != "inputs":
                raise ValueError("Đã có thư mục fit/train; không được đổi signature: " + relative)
        elif relative not in PREFIT_FILES:
            raise ValueError("Đã có artifact ngoài preflight; không được đổi signature: " + relative)
        else:
            files.append(relative)
    return sorted(files)


def repair_pretraining_lock(root: Path, protocol: dict[str, Any]) -> dict[str, Any]:
    """Archive owner released đã chết, dưới OS lock; không fit, xóa lock hay thay state."""
    root = root.resolve()
    directory = root / NAMESPACE
    owner_path, lock_path = path_for(root, "run.owner.json"), path_for(root, "run.lock")
    if not owner_path.exists():
        return {"status":"NO_OWNER_TO_REPAIR"}
    if not lock_path.is_file():
        raise ValueError("Có owner nhưng thiếu run.lock; cần rà soát")
    with lock_path.open("r+b") as handle:
        try:
            lock_handle(handle)
        except OSError:
            raise RuntimeError("Run vẫn giữ khóa OS; không phục hồi metadata đang sống") from None
        files = require_prefit(directory)
        raw = owner_path.read_bytes()
        owner = json.loads(raw)
        if type(owner) is not dict or set(owner) != OWNER_KEYS:
            raise ValueError("Owner không đúng schema; không phục hồi")
        UUID(owner["owner_uuid"])
        host, boot = host_boot()
        if owner["host_id"] != host or owner["owner_state"] != "released":
            raise ValueError("Owner khác host hoặc chưa released; không phục hồi")
        if (type(owner["pid"]) is not int or owner["pid"] < 1
                or type(owner["process_start_time"]) is not str or not owner["process_start_time"]
                or type(owner["boot_id"]) is not str or not owner["boot_id"]):
            raise ValueError("Owner thiếu identity tiến trình")
        dates = []
        for key in ("acquired_at", "released_at"):
            value = owner[key]
            if type(value) is not str or not value.endswith("Z"):
                raise ValueError("Owner thiếu thời điểm acquire/release UTC")
            dates.append(datetime.fromisoformat(value))
        if dates[1] < dates[0]:
            raise ValueError("Owner release trước acquire")
        start = None if owner["boot_id"] != boot else process_start(owner["pid"])
        if start == owner["process_start_time"]:
            raise RuntimeError("Tiến trình owner còn sống; không đổi protocol của owner này")
        signature = content_hash(protocol)
        if owner["run_signature"] == signature:
            return {"status":"LOCK_SIGNATURE_ALREADY_CURRENT"}
        commit = previous_protocol(root, owner["run_signature"], protocol)
        archive = path_for(root, f"lock_history/{owner['owner_uuid']}.owner.original.json")
        receipt = path_for(root, f"lock_history/{owner['owner_uuid']}.migration.json")
        if archive.exists():
            raise ValueError("Archive owner đã tồn tại; không ghi đè bằng chứng")
        # Kiểm hai đường dẫn tuyệt đối trong namespace trước thao tác move trên Windows.
        if (not owner_path.resolve().is_relative_to(directory.resolve())
                or not archive.resolve().is_relative_to(directory.resolve())):
            raise ValueError("Đường dẫn archive owner vượt namespace")
        archive.parent.mkdir(parents=True, exist_ok=True)
        evidence = {"reason":"RELEASED_PREFIT_OWNER_PROTOCOL_SOURCE_UPDATE", "previous_protocol_commit":commit,
            "previous_signature":owner["run_signature"], "current_signature":signature,
            "previous_owner_uuid":owner["owner_uuid"], "owner_byte_sha256":file_hash(owner_path),
            "archive":archive.relative_to(directory).as_posix(), "prefit_files":files, "at":utc_now(),
            "fit_or_train_outputs_present":False, "lock_file_removed":False}
        if receipt.exists():
            pending = read(receipt)
            if {k:v for k,v in pending.items() if k != "at"} != {k:v for k,v in evidence.items() if k != "at"}:
                raise ValueError("Receipt migration khác owner/protocol hiện tại")
        else:
            write(receipt, evidence)
        owner_path.rename(archive)
        if archive.read_bytes() != raw:
            raise ValueError("Archive owner không giữ nguyên byte")
        return {"status":"PREFIT_OWNER_ARCHIVED", "previous_signature":owner["run_signature"],
                "current_signature":signature, "archive":archive.relative_to(root).as_posix()}
