"""Khôi phục LF/CRLF đúng checksum U07; từ chối mọi khác biệt nội dung thực sự."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import tempfile
from typing import Any
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "docs/plan/week12/unified_execution_checks.zip"
PACKAGE_SHA256 = "c77da519973da453bd0581951421528d9567704a6b8ec17f39a9653cbf3a8d21"


def restore(root: Path, bindings: dict[str, Any], *, write: bool = False) -> dict[str, Any]:
    """Kiểm toàn bộ trước khi ghi; chỉ nhận một biến thể newline có đúng byte/hash đã khóa."""
    root = root.resolve()
    pending = []
    for name, expected in bindings.items():
        rel = PurePosixPath(name)
        path = root.joinpath(*rel.parts)
        if (not name or rel.is_absolute() or ".." in rel.parts or ":" in name or chr(92) in name
                or not path.resolve().is_relative_to(root) or any(p.startswith(".env") for p in rel.parts)
                or any(p.is_symlink() for p in (path, *path.parents))):
            raise ValueError("Đường dẫn nguồn không an toàn")
        raw = path.read_bytes()
        if len(raw) == expected["bytes"] and hashlib.sha256(raw).hexdigest() == expected["sha256"]:
            continue
        lf = raw.replace(b"\r\n", b"\n")
        variants = {lf, lf.replace(b"\n", b"\r\n")}
        matches = [v for v in variants if len(v) == expected["bytes"] and hashlib.sha256(v).hexdigest() == expected["sha256"]]
        if len(matches) != 1:
            raise ValueError("Nguồn khác nội dung đã khóa, không tự sửa: " + name)
        pending.append((path, matches[0]))
    if write:
        for path, raw in pending:
            descriptor, temporary = tempfile.mkstemp(prefix=".u07-newline-", dir=path.parent)
            try:
                with os.fdopen(descriptor, "wb") as stream:
                    stream.write(raw)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temporary, path)
            finally:
                if Path(temporary).exists():
                    Path(temporary).unlink()
    return {"status": "RESTORED_EXACT_CHECKOUT" if write else "CHECKED_NEWLINE_VARIANTS",
            "source_bindings": len(bindings), "newline_changes": len(pending), "api": False}


def main() -> None:
    """Chỉ tin gói U07 đã pin; mặc định dry-run, không stage Git hoặc gọi provider."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    package = ROOT / PACKAGE
    if hashlib.sha256(package.read_bytes()).hexdigest() != PACKAGE_SHA256:
        raise ValueError("Gói U07 khác checksum đã nghiệm thu")
    with zipfile.ZipFile(package) as archive:
        bindings = json.loads(archive.read("source_bindings.json"))
    print(json.dumps(restore(ROOT, bindings, write=args.write), ensure_ascii=False))


if __name__ == "__main__":
    main()
