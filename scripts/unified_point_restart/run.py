"""CLI admission theo phản hồi provider, collect dành cho người dùng khởi chạy thủ công."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def main() -> None:
    """Prepare/verify/status hoạt động offline, chỉ collect được mở client sau grant."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "collect", "verify", "status"))
    parser.add_argument("--seal", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "status":
            from core.unified_live.manager import status
            result = status(ROOT, "RESEARCH")
        else:
            from core.unified_point_restart.runtime import prepare, collect, audit
            if args.command == "collect":
                result = collect(ROOT)
            else:
                from scripts.verify_original_fix_parity import deny_external_network
                deny_external_network()
                result = prepare(ROOT) if args.command == "prepare" else audit(ROOT, seal=args.seal)
        print(json.dumps(result, ensure_ascii=False), flush=True)
    except Exception as error:
        parser.exit(2, "Admission provider dừng: " + str(error) + "\n")


if __name__ == "__main__":
    main()
