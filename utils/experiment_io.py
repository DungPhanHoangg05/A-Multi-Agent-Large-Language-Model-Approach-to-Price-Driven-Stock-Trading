"""CLI và Web cùng xuất một bảng đã được evaluator xác minh."""
from __future__ import annotations

import csv
import io
from pathlib import Path
import re
from typing import Any

from core.unified_contracts import json_bytes


def run_path(root: Path, identifier: str) -> Path:
    """Chỉ nhận ID run, không nhận đường dẫn tùy ý từ trình duyệt."""
    if type(identifier) is not str or re.fullmatch(r"[A-Za-z0-9_-]{1,100}", identifier) is None:
        raise ValueError("Run ID không hợp lệ")
    base = (root / "outputs/unified_integration").resolve()
    path = base / identifier
    if not path.resolve().is_relative_to(base):
        raise ValueError("Run ID thoát khỏi namespace")
    return path


def export_bytes(result: dict[str, Any], format_name: str) -> tuple[bytes, str]:
    """Giữ null/undefined; CSV là cùng rows với JSON, không tự tính lại metric."""
    if format_name == "json":
        return json_bytes(result), "application/json"
    if format_name != "csv":
        raise ValueError("Định dạng export chỉ có json/csv")
    stream = io.StringIO(newline="")
    rows = result["rows"]
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]) if rows else ["point_id", "variant"])
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8-sig"), "text/csv; charset=utf-8"
