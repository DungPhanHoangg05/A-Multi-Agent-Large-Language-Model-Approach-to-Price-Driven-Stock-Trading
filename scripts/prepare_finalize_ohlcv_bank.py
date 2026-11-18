"""Khóa recipe, phát hành và kiểm tái lập bank OHLCV FIN06 offline."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.finalize_deterministic_bank import OUTPUT, RECIPE, VERSION, build, make_recipe, summarize
from core.unified_contracts import digest, json_bytes
from core.unified_preflight_assets import write_new
from core.unified_protocol import binding, read
from scripts.verify_finalize_ohlcv_bank import verify_windows
from scripts.verify_original_fix_parity import deny_external_network


def envelope(payload: dict) -> bytes:
    """Seal artifact theo schema hash đã dùng trong plan."""
    return json_bytes({"payload": payload, "sha256": digest(payload)})


def main() -> None:
    """Khóa trước rồi chạy verifier toàn cohort ở cả lần build và lần check."""
    deny_external_network()
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--lock-recipe", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.lock_recipe:
        write_new(ROOT / RECIPE, envelope(make_recipe(ROOT)))
        print("Đã khóa amendment công thức bank và query trước khi tính khóa.")
        return
    bank, query = build(ROOT, read(ROOT, RECIPE, True))
    verification = verify_windows(ROOT, bank, query)
    support = summarize(bank, query)
    if (support["bank_records"], support["statistics_ready"], support["example_ready"],
            support["alpha_na"], support["sentiment_na"]) != (852, 852, 733, 119, 852):
        raise ValueError("Độ phủ bank xác định khác miền FIN06 đã khóa")
    if support["query_key_reasons"] != {"AVAILABLE": 102}:
        raise ValueError("Khóa OHLCV chưa đủ cho 102 query đã khóa")
    for name, payload in (("bank.json", bank), ("query_keys.json", query)):
        path = ROOT / OUTPUT / name
        raw = envelope(payload)
        if args.check:
            if path.read_bytes() != raw:
                raise ValueError("Artifact khác bản tái dựng: " + name)
        else:
            write_new(path, raw)
    result = {"version": VERSION, "status": "PASS_OFFLINE_FIN06", "FIN06_complete": True,
              "bank_available_for_FIN07": True, "recipe": binding(ROOT, RECIPE),
              "assets": [binding(ROOT, OUTPUT + name) for name in ("bank.json", "query_keys.json")],
              "support": support, "verification": verification, "bank_vision_http": 0,
              "query_outcomes_computed": False}
    path = ROOT / OUTPUT / "manifest.json"
    if args.check:
        if path.read_bytes() != envelope(result):
            raise ValueError("Manifest bank khác bản tái dựng")
    else:
        write_new(path, envelope(result))
    print(json_bytes(result).decode())


if __name__ == "__main__":
    main()
