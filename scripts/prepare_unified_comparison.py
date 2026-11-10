"""CLI khóa/kiểm protocol và preflight offline; không có lệnh mở API."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.unified_contracts import json_bytes
from core.unified_protocol import MANIFEST, PROTOCOL, build, read, safe, seal, verify


def main() -> None:
    """Manifest chỉ tạo mới; verify tái dựng nguồn, không ghi hoặc tạo client."""
    from scripts.verify_original_fix_parity import deny_external_network
    deny_external_network()
    parser = argparse.ArgumentParser(description="Khóa giao thức so sánh và preflight không mạng")
    parser.add_argument("--root", type=Path, default=ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    build_parser = commands.add_parser("build")
    build_parser.add_argument("--output", default=MANIFEST)
    verify_parser = commands.add_parser("verify")
    verify_parser.add_argument("--manifest", default=MANIFEST)
    try:
        args = parser.parse_args()
        root = args.root.resolve()
        if args.command == "build":
            path = safe(root, args.output)
            if args.output != MANIFEST and not path.is_relative_to(root / "outputs/unified_integration"):
                raise ValueError("Manifest mới phải ở namespace thống nhất hoặc đường dẫn protocol chuẩn")
            payload = build(root, read(root, PROTOCOL))
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as handle:
                handle.write(json_bytes(seal(payload)) + b"\n")
            result = {"status": "MANIFEST_CREATED_NOT_RELEASED", "path": args.output,
                "counts": payload["counts"], "api": False}
        else:
            result = verify(root, manifest_path=args.manifest)
        print(json_bytes(result).decode("utf-8"))
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(2, "Không thể khóa/kiểm giao thức: " + str(error) + "\n")


if __name__ == "__main__":
    main()
