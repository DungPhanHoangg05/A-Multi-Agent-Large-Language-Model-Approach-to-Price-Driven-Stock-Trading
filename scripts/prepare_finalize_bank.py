"""Khóa recipe và dựng tài nguyên FIN06 offline, chỉ ghi phiên bản độc lập."""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.finalize_bank_resources import ASSETS, RECIPE, build_recipe, rebuild
from core.unified_contracts import digest, json_bytes
from core.unified_preflight_assets import write_new
from core.unified_protocol import binding, read
from scripts.verify_original_fix_parity import deny_external_network


def manifest(root: Path, assets: dict) -> dict:
    """Tách kết quả số và tình trạng bank tín hiệu trước khi chạy FIN09."""
    bank, queries, regimes = (assets[name] for name in ("bank.json", "query_inputs.json", "regimes.json"))
    return {"version": "finalize_bank_resources_manifest_v1", "FIN06_complete": False,
            "status": "NUMERIC_PASS_SIGNAL_LINEAGE_PENDING", "recipe": binding(root, RECIPE),
            "asset_bindings": [binding(root, ASSETS + name) for name in sorted(assets)],
            "bank_numeric_records": len(bank["records"]), "signal_ready": bank["signal_ready"],
            "signal_pending": bank["signal_pending"], "query_input_count": len(queries),
            "ood_query_count": sum(row["prior_fallback"] is not None for row in queries),
            "query_feature_status": dict(Counter(row["feature"]["status"] for row in queries)),
            "selector_count": len(assets["selectors.json"]), "mt_scaler_fit_count": regimes["mt_scaler"]["fit_count"],
            "bank_signal_slots_to_resolve_FIN09": bank["signal_pending"],
            "signal_release_condition": "Đối soát request/response đúng recipe causal và pin ngân sách trước thu. Missing raw là blocker riêng.",
            "hosted_api_calls": 0, "hmm_student_refit": False, "query_outcomes_computed": False}


def main() -> None:
    """--lock-recipe khóa đầu vào, --check tái dựng để đối soát byte."""
    deny_external_network()
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--lock-recipe", action="store_true")
    modes.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.lock_recipe:
        recipe = build_recipe(ROOT)
        write_new(ROOT / RECIPE, json_bytes({"payload": recipe, "sha256": digest(recipe)}))
        print("Đã khóa recipe FIN06 trước fit.")
        return
    recipe = read(ROOT, RECIPE, True)
    assets = rebuild(ROOT, recipe)
    for name, value in assets.items():
        path, raw = ROOT / ASSETS / name, json_bytes(value)
        if args.check:
            if path.read_bytes() != raw:
                raise ValueError("Tài nguyên FIN06 khác bản tái dựng: " + name)
        else:
            write_new(path, raw)
    result = manifest(ROOT, assets)
    path = ROOT / ASSETS / "manifest.json"
    contents = json_bytes({"payload": result, "sha256": digest(result)})
    if args.check:
        if path.read_bytes() != contents:
            raise ValueError("Manifest FIN06 khác bản tái dựng")
    else:
        write_new(path, contents)
    print(json_bytes(result).decode())


if __name__ == "__main__":
    main()
