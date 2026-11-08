"""CLI H03 offline: khóa hoặc kiểm protocol, không fit/train/inference/API."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.historical_evaluation_protocol import run


def main() -> None:
    """Báo ma trận đã khóa; release API vẫn thuộc H06."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="Chỉ kiểm byte/ngữ nghĩa/Git, không ghi file.")
    args = parser.parse_args()
    protocol = run(ROOT, verify=args.verify)
    calls = protocol["budget"]["calls"]
    print("Protocol H03: " + protocol["status"])
    print(f"Historical upstream H={calls['historical_upstream_H']}; research calls={calls['research_total']}.")
    print("Chưa cấp quyền gọi API; tiếp tục H04–H06.")


if __name__ == "__main__":
    main()
