"""Tách checkpoint một điểm FIN11 khi provider đã nhận nhưng không còn raw response."""
from __future__ import annotations

from pathlib import Path
import re

from core.finalize_budget_quota import ATTEMPT_CAP, ORG
from core.historical_evaluation_journal import load, save
from core.prior_run_lock import safe_path, utc_now
from core.unified_contracts import digest
from core.unified_protocol import binding


def reset_directory(root: Path, point: str) -> Path:
    """Đường dẫn bản lưu gắn với đúng một mã và cutoff."""
    if re.fullmatch(r"[A-Z0-9]+-\d{4}-\d{2}-\d{2}", point) is None:
        raise ValueError("ID point FIN11 không hợp lệ")
    return safe_path(root, f"point_resets/{point}")


def point_files(root: Path, point: str) -> tuple[list[dict], list[dict]]:
    """Chọn đúng wire, stage và ảnh theo ID point trong journal."""
    files, rows = [], []
    for folder in ("research/http", "research/journal/slots"):
        for path in sorted((root/folder).glob("*.json")):
            doc = load(path)
            slot = doc["slot"]
            if point not in slot.split("/"):
                continue
            if path.stem != digest(slot):
                raise ValueError("File checkpoint sai khóa slot")
            files.append(binding(root, path.relative_to(root).as_posix()))
            if folder == "research/http":
                if any(row["slot"] != slot for row in doc["rows"]):
                    raise ValueError("Attempt khác slot trong wire")
                rows.extend(doc["rows"])
    images = safe_path(root, f"research/journal/images/{point}")
    for path in sorted(images.glob("*")):
        if not path.is_file() or path.is_symlink():
            raise ValueError("Thư mục ảnh point chứa phần tử ngoài dự kiến")
        files.append(binding(root, path.relative_to(root).as_posix()))
    return files, rows


def verify_manifest(root: Path, grant: dict, path: Path) -> dict:
    """Đọc khóa bản lưu và giới hạn những đường dẫn có thể được tách."""
    doc = load(path/"manifest.json")
    point = doc["point_id"]
    if path != reset_directory(root, point) or doc["grant_sha256"] != digest(grant):
        raise ValueError("Bản lưu point khác grant FIN11")
    for file in doc["files"]:
        name = file["path"]
        if re.fullmatch(r"research/(?:http|journal/slots)/[0-9a-f]{64}\.json", name):
            continue
        parts = name.split("/")
        if len(parts) != 5 or parts[:4] != ["research", "journal", "images", point]:
            raise ValueError("Đường dẫn bản lưu ngoài point FIN11")
    return doc


def archived_resets(root: Path, grant: dict) -> list[dict]:
    """Chỉ chạy lại sau khi toàn bộ manifest đã được tách và xác minh byte."""
    result = []
    for path in sorted(safe_path(root, "point_resets").glob("*/manifest.json")):
        directory = path.parent
        doc = verify_manifest(root, grant, directory)
        if not (directory/"complete.json").is_file() or load(directory/"complete.json") != {"manifest_sha256": digest(doc)}:
            raise ValueError("Đang tách checkpoint point. Chạy lại lệnh reset-point trước khi resume")
        if any(binding(directory, file["path"]) != file for file in doc["files"]):
            raise ValueError("Bản sao checkpoint point đã thay đổi")
        result.append(doc)
    return result


def archive_lost_point(root: Path, grant: dict, budget: dict, point: str, request_id: str) -> dict:
    """Tách đúng điểm đang dở dưới khóa worker và cho phép tiếp tục khi di chuyển bị ngắt."""
    path = reset_directory(root, point)
    if (path/"manifest.json").is_file():
        doc = verify_manifest(root, grant, path)
        if doc["request_id"] != request_id:
            raise ValueError("Point đã được tách với UUID khác")
        if (path/"complete.json").is_file():
            archived_resets(root, grant)
            return doc
    else:
        if any((root/"research"/name).exists() for name in (f"points/{point}.json", "receipt.json")):
            raise ValueError("Point hoặc phase đã chốt kết quả")
        plans = {row["slot"]: row for row in budget["slots"] if row["phase"] == "RESEARCH"
                 and point in row["slot"].split("/")}
        if not plans:
            raise ValueError("Point ngoài ledger nghiên cứu FIN11")
        files, rows = point_files(root, point)
        missing = [row for row in rows if row["status"] == "UNKNOWN"]
        if len(missing) != 1 or missing[0]["id"] != request_id or missing[0].get("response") is not None:
            raise ValueError("UUID không xác nhận đúng response đang thiếu của point")
        counts: dict[str, int] = {}
        for row in rows:
            slot = row["slot"]
            if plans.get(slot, {}).get("state") != "NEW":
                raise ValueError("Attempt ngoài slot gọi mới của FIN09")
            counts[slot] = counts.get(slot, 0)+1
            if counts[slot] >= ATTEMPT_CAP:
                raise ValueError("Slot không còn lần thử để chạy lại trong cap FIN09")
        lost = missing[0]
        doc = {"point_id": point, "request_id": request_id, "slot": lost["slot"], "started_at": lost["started_at"],
               "org_slot": lost.get("org_slot", ORG), "owner_reported_http_status": 200,
               "reason": "OWNER_REPORTED_HTTP_200_WITHOUT_RESPONSE", "archived_at": utc_now(),
               "grant_sha256": digest(grant), "files": files, "attempts_by_slot": counts,
               "archived_attempts": len(rows), "tokens_measured": sum(row.get("usage") or 0 for row in rows),
               "unknown_reserve_tokens": lost["reserved_tokens"]}
        save(path/"manifest.json", doc)
    for file in doc["files"]:
        name = file["path"]
        source, destination = safe_path(root, name), safe_path(path, name)
        if destination.exists():
            if source.exists() or binding(path, name) != file:
                raise ValueError("Bản lưu và checkpoint có nội dung chồng lấn")
            continue
        if binding(root, name) != file:
            raise ValueError("Checkpoint thay đổi trước khi tách")
        if source.suffix == ".json" and point not in load(source)["slot"].split("/"):
            raise ValueError("File không thuộc point được phép tách")
        destination.parent.mkdir(parents=True, exist_ok=True)
        source.rename(destination)
    save(path/"complete.json", {"manifest_sha256": digest(doc)})
    return doc
