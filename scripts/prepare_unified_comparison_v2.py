"""CLI hoàn thiện U06: assets/restore/freeze/verify offline, không có collect hoặc grant."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.unified_contracts import json_bytes
from core.unified_protocol import seal


def main() -> None:
    """Mặc định không model/client/key; assets và replay-numeric là lệnh offline tường minh."""
    from scripts.verify_original_fix_parity import deny_external_network
    deny_external_network()
    parser = argparse.ArgumentParser(description="Nghiệm thu U06 v2 không inference")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("command", choices=("assets", "package", "freeze", "restore", "verify", "replay-numeric"))
    args = parser.parse_args()
    try:
        from core.unified_preflight import build, package_assets, restore_assets, verify, MANIFEST_V2
        root = args.root.resolve()
        if args.command == "verify":
            result = verify(root)
        elif args.command == "restore":
            result = restore_assets(root)
        elif args.command == "package":
            result = package_assets(root)
        elif args.command == "freeze":
            result = build(root)
            with (root / MANIFEST_V2).open("xb") as handle:
                handle.write(json_bytes(seal(result)) + b"\n")
            result = {"status": result["status"], "api": False}
        else:
            from core.unified_preflight_assets import frozen_alpha_assets, provider_assets, vision_probe, news_assets
            if args.command == "assets":
                frozen_alpha_assets(root)
                provider_assets(root)
                vision_probe(root)
                news_assets(root)
                result = {"status": "ASSETS_PREPARED_NOT_RELEASED", "api": False}
            else:
                from core.unified_preflight_replay import replay_numeric
                result = replay_numeric(root)
        print(json_bytes(result).decode("utf-8"))
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(2, "Không thể xử lý preflight v2: " + str(error) + "\n")


if __name__ == "__main__":
    main()
