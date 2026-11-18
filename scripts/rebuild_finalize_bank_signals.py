"""Tạo checkpoint tín hiệu FIN06 offline. Phản hồi thị giác vẫn do FIN09 quản lý."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("MPLBACKEND", "Agg")

from core.finalize_bank_signals import build, rebuild_recipe
from core.unified_contracts import digest, json_bytes
from core.unified_preflight_assets import write_new
from core.unified_protocol import read
from scripts.verify_original_fix_parity import deny_external_network
from threadpoolctl import threadpool_limits

WORK = ROOT / "tmp/fin06_signal_rebuild_v2"
RECIPE_NAME = "recipe.json"


def envelope(value: dict) -> bytes:
    """Đóng dấu byte theo hợp đồng repo."""
    return json_bytes({"payload": value, "sha256": digest(value)})


def main() -> None:
    """Khóa recipe riêng trước build. Checkpoint có thể đối soát và dùng lại khi dừng."""
    deny_external_network()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lock-recipe", action="store_true")
    args = parser.parse_args()
    if args.lock_recipe:
        recipe = rebuild_recipe(ROOT)
        write_new(WORK / RECIPE_NAME, envelope(recipe))
        print("Đã khóa recipe tạo lại tín hiệu offline.")
        return
    recipe = read(WORK, RECIPE_NAME, True)
    lock = WORK / "build.lock"
    handle = os.open(lock, os.O_EXCL | os.O_CREAT | os.O_WRONLY)
    os.close(handle)
    try:
        with threadpool_limits(limits=1):
            report = build(ROOT, WORK, recipe)
        write_new(WORK / "report.json", envelope(report))
        print(json_bytes({k: v for k, v in report.items() if k != "points"}).decode())
    finally:
        lock.unlink()


if __name__ == "__main__":
    main()
