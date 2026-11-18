"""Tái lập kế hoạch thu tín hiệu bank offline từ checkpoint đã khóa."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.finalize_bank_admission import collection_plan
from core.unified_contracts import digest, json_bytes
from core.unified_preflight_assets import write_new
from scripts.verify_original_fix_parity import deny_external_network

PATH = "docs/plan/week12/finalize_bank_collection_plan_v1.json"


def main() -> None:
    """Chỉ ghi no-op plan hoặc so byte, không mở transport."""
    deny_external_network()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    plan = collection_plan(ROOT)
    raw = json_bytes({"payload": plan, "sha256": digest(plan)})
    path = ROOT / PATH
    if args.check:
        if path.read_bytes() != raw:
            raise ValueError("Kế hoạch FIN06 khác bản dựng lại")
    else:
        write_new(path, raw)
    print(json_bytes({key: value for key, value in plan.items() if key not in ("episodes", "slots", "policy")}).decode())


if __name__ == "__main__":
    main()
