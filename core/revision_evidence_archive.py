"""Đọc, kiểm và khôi phục bằng chứng revision đã lưu trữ nguyên byte."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, Iterator
from zipfile import ZipFile

DIRECTORY = "docs/plan/revision_evidence"


def _relative(name: str) -> str:
    """Chặn đường dẫn tuyệt đối, traversal và alias Windows trong chỉ mục."""
    path = PurePosixPath(name)
    if (not name or path.is_absolute() or "\\" in name or ":" in name
            or any(part in ("", ".", "..") or part.endswith((".", " ")) for part in name.split("/"))):
        raise ValueError("Đường dẫn bằng chứng không an toàn")
    return path.as_posix()


def _target(root: Path, name: str) -> Path:
    """Chỉ cho ghi trong cây đích đã xác định, không đi qua symlink."""
    root = root.resolve()
    path = root / _relative(name)
    if not path.resolve().is_relative_to(root) or any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError("Đích khôi phục thoát thư mục hoặc đi qua symlink")
    return path


def load_index(root: Path) -> dict[str, Any]:
    """Đọc schema và đối soát digest của chỉ mục trước khi dùng đường dẫn."""
    index = json.loads((root / DIRECTORY / "index.json").read_bytes())
    unsigned = {k: v for k, v in index.items() if k != "sha256"}
    raw = json.dumps(unsigned, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    if index.get("schema") != "revision_evidence_archive_v1" or hashlib.sha256(raw).hexdigest() != index.get("sha256"):
        raise ValueError("Chỉ mục bằng chứng sai schema hoặc digest")
    for name in index["files"]:
        _relative(name)
    for name in index["parts"]:
        if _relative(name) != Path(name).name or not name.endswith(".zip"):
            raise ValueError("Tên phần lưu trữ không hợp lệ")
    return index


class EvidenceArchive:
    """Kiểm mỗi phần ZIP trước đọc; không chạy mã hoặc tự khôi phục vào workspace."""

    def __init__(self, root: Path, index: dict[str, Any] | None = None) -> None:
        self.root = root.resolve()
        self.index = index if index is not None else load_index(root)
        self._archives: dict[str, ZipFile] = {}

    def __enter__(self) -> EvidenceArchive:
        return self

    def __exit__(self, *args: object) -> None:
        for archive in self._archives.values():
            archive.close()

    def _archive(self, name: str) -> ZipFile:
        if name not in self._archives:
            binding = self.index["parts"][name]
            path = _target(self.root / DIRECTORY, name)
            digest = hashlib.sha256()
            with path.open("rb") as handle:
                for raw in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(raw)
            if path.stat().st_size != binding["bytes"] or digest.hexdigest() != binding["sha256"]:
                raise ValueError("Phần lưu trữ khác hash: " + name)
            archive = ZipFile(path)
            names = archive.namelist()
            if len(names) != len(set(names)):
                archive.close()
                raise ValueError("Phần lưu trữ có member trùng")
            self._archives[name] = archive
        return self._archives[name]

    def chunks(self, name: str) -> Iterator[bytes]:
        """Đọc từng mảnh đã kiểm hash; kiểm digest toàn tệp ở cuối luồng."""
        row = self.index["files"][_relative(name)]
        digest = hashlib.sha256()
        count = 0
        for chunk in row["chunks"]:
            location = self.index["blobs"][chunk]
            raw = self._archive(location["part"]).read("blobs/" + chunk)
            if len(raw) != location["bytes"] or hashlib.sha256(raw).hexdigest() != chunk:
                raise ValueError("Mảnh bằng chứng khác hash")
            digest.update(raw)
            count += len(raw)
            yield raw
        if count != row["bytes"] or digest.hexdigest() != row["sha256"]:
            raise ValueError("Tệp bằng chứng khác hash: " + name)

    def read(self, name: str) -> bytes:
        """Đọc tệp nhỏ vào RAM sau khi kiểm đủ mọi mảnh và digest toàn tệp."""
        return b"".join(self.chunks(name))

    def verify(self, prefix: str = "") -> int:
        """Đối soát đầy đủ nội dung dưới prefix; không chỉ tin chỉ mục."""
        count = 0
        for name in self.index["files"]:
            if name.startswith(prefix):
                for _ in self.chunks(name):
                    pass
                count += 1
        return count

    def restore(self, directory: str, destination: Path | None = None) -> int:
        """Khôi phục một release theo yêu cầu, từ chối ghi đè tệp đang khác byte."""
        if directory not in self.index["directories"]:
            raise ValueError("Không có release trong chỉ mục")
        prefix = "outputs/revision/" + _relative(directory) + "/"
        selected = [name for name in self.index["files"] if name.startswith(prefix)]
        target_root = self.root if destination is None else destination.resolve()
        self.verify(prefix)
        # Kiểm tất cả đích trước khi ghi để tránh khôi phục dở khi gặp xung đột.
        for name in selected:
            path = _target(target_root, name)
            if path.exists() and (not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != self.index["files"][name]["sha256"]):
                raise ValueError("Không ghi đè tệp khác byte: " + name)
        for name in selected:
            path = _target(target_root, name)
            if path.exists():
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as handle:
                for raw in self.chunks(name):
                    handle.write(raw)
        return len(selected)
