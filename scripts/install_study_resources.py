"""Cài các đầu vào công khai đúng đường dẫn đã ghi trong manifest nghiên cứu."""
from __future__ import annotations

import hashlib
import io
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_SHA256 = "650fe996bd0ecb2f337430319014495ed3925f71d3bc78d11667f535e38acf2c"


def install(root: Path = ROOT) -> int:
    """Đối chiếu gói trước khi ghi, giữ dữ liệu sẵn có và cho phép chạy đồng thời."""
    root = root.resolve()
    raw = (root / "resources/serving_inputs.zip").read_bytes()
    if hashlib.sha256(raw).hexdigest() != PACKAGE_SHA256:
        raise ValueError("Gói đầu vào serving khác SHA-256 của bản phân phối.")
    installed = 0
    with ZipFile(io.BytesIO(raw)) as archive:
        for name in archive.namelist():
            target = root / name
            if not target.resolve().is_relative_to(root) or target.is_symlink():
                raise ValueError(f"Đường dẫn tài nguyên không hợp lệ: {name}")
            payload = archive.read(name)
            if target.is_file():
                if target.read_bytes() != payload:
                    raise ValueError(f"Tệp cục bộ khác nguồn đã khóa: {name}")
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with NamedTemporaryFile(dir=target.parent, delete_on_close=False) as stream:
                stream.write(payload)
                stream.close()
                try:
                    os.link(stream.name, target)
                    installed += 1
                except FileExistsError:
                    if target.read_bytes() != payload:
                        raise ValueError(f"Tài nguyên đồng thời khác nguồn: {name}")
    return installed


if __name__ == "__main__":
    print(f"Đã cài {install()} tệp mới từ gói đầu vào serving.")
