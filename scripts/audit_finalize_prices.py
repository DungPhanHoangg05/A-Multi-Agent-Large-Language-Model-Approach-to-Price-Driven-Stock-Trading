"""Audit FIN04 từ response đã pin; không thu dữ liệu hoặc sửa nguồn lịch sử."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.finalize_price_audit import audit_prices, require_price_gate
from core.unified_contracts import digest, json_bytes
from core.unified_protocol import read


def main() -> None:
    """Audit có thể thành công trong khi source gate còn chặn; --require-pass dùng cho preflight."""
    from scripts.verify_original_fix_parity import deny_external_network
    deny_external_network()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=Path("docs/plan/week12/finalize_price_audit.json"))
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--require-pass", action="store_true")
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        output = root / args.output
        if not output.resolve().is_relative_to(root) or output.is_symlink() or any(p.is_symlink() for p in output.parents):
            raise ValueError("Đường dẫn audit vượt root hoặc qua symlink")
        report = audit_prices(root)
        if args.check:
            relative = output.relative_to(root).as_posix()
            if read(root, relative, True) != report:
                raise ValueError("Báo cáo audit không còn khớp nguồn")
        else:
            raw = json_bytes({"payload":report,"sha256":digest(report)})
            if output.exists():
                if output.read_bytes() != raw:
                    raise ValueError("Không ghi đè audit khác byte; cần tên/version mới")
            else:
                output.parent.mkdir(parents=True, exist_ok=True)
                with output.open("xb") as handle:
                    handle.write(raw)
        if args.require_pass:
            require_price_gate(root, report)
        print(json_bytes({"status":report["status"],"price_source_gate":report["price_source_gate"],
            "planned_points":report["planned_points"],"admitted_points":report["admitted_points"],
            "query_outcomes_computed":False,"api_calls":0}).decode())
    except (ValueError, TypeError, KeyError, OSError) as error:
        parser.exit(2, "Không thể mở gate giá finalize: " + str(error) + "\n")


if __name__ == "__main__":
    main()
