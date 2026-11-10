"""Fit/verify/predict/bridge alpha causal offline, không tạo client hoặc sửa artifact cũ."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.bayesian_memory import read_json
from core.causal_alpha import FrozenSelector, fit_selector
from core.causal_bridge import bind_snapshot, decision_payload
from core.unified_contracts import SharedSnapshot, digest, json_bytes


def prices(path: Path) -> Any:
    """Đọc schema OHLCV tường minh, không đoán adjusted/unadjusted hoặc splice nguồn."""
    import pandas as pd
    if path.suffix not in (".csv", ".json"):
        raise ValueError("Nguồn giá causal chỉ nhận CSV/JSON")
    result = pd.read_csv(path) if path.suffix == ".csv" else pd.DataFrame(read_json(path))
    if "Datetime" not in result.columns:
        raise ValueError("Nguồn giá causal thiếu Datetime")
    result["Datetime"] = pd.to_datetime(result.Datetime)
    return result


def write_new(path: Path, value: dict[str, Any]) -> None:
    """Chỉ output mới trong namespace tích hợp hoặc đường dẫn ngoài repo được chỉ định."""
    resolved = path.resolve()
    if resolved.is_relative_to(ROOT) and not resolved.is_relative_to(ROOT / "outputs/unified_integration"):
        raise ValueError("Không ghi causal output vào nguồn hoặc namespace lịch sử")
    with path.open("xb") as handle:
        handle.write(json_bytes(value))


def main() -> None:
    """Mọi subcommand chặn mạng và không mở student/HMM weights."""
    from scripts.verify_original_fix_parity import deny_external_network
    deny_external_network()
    parser = argparse.ArgumentParser(description="Profile causal alpha offline")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("fit", "verify", "predict", "bridge"):
        command = sub.add_parser(name)
        command.add_argument("--prices", required=True, type=Path)
        if name == "fit":
            command.add_argument("--schedule", required=True, type=Path)
        else:
            command.add_argument("--selector", required=True, type=Path)
        if name == "predict":
            command.add_argument("--cutoff", required=True)
        if name == "bridge":
            command.add_argument("--snapshot", required=True, type=Path)
            command.add_argument("--decision", required=True, type=Path)
        if name != "verify":
            command.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        frame = prices(args.prices)
        if args.command == "fit":
            result = fit_selector(frame, read_json(args.schedule))
        else:
            import pandas as pd
            selector = FrozenSelector(read_json(args.selector), frame)
            if args.command == "verify":
                result = {"status": "PASS_REPLAYED_SELECTOR", "selector_sha256": selector.sha256,
                          "scope": "ALPHA_PROFILE_ONLY; NO_WHOLE_SYSTEM_CAUSAL_RELEASE", "hosted_calls": 0}
            elif args.command == "predict":
                result = selector.predict(frame.loc[frame.Datetime <= pd.Timestamp(args.cutoff)], args.cutoff)
            else:
                from core.unified_methods import MethodAdapters
                doc = read_json(args.snapshot)
                base = SharedSnapshot.create(doc["point"], doc["realization"], doc["payload"], doc["provenance"])
                prefix = frame.loc[frame.Datetime <= pd.Timestamp(doc["point"]["cutoff"])]
                bridged = bind_snapshot(base, selector, prefix, hashlib.sha256(args.prices.read_bytes()).hexdigest())
                methods = MethodAdapters(read_json(args.decision))
                before = methods.prepare("original_fix", base, {}, 0)["request"]
                after = methods.prepare("original_fix", bridged, {}, 0)["request"]
                if before != after:
                    raise ValueError("Bridge làm đổi request native")
                result = {"version": "native_causal_bridge_v1", "shared": bridged.document(), "native_request": after,
                    "causal_common_request": methods.prepare("original_common", bridged, {}, 0)["request"],
                    "native_request_unchanged": True, "native_payload_sha256": digest(decision_payload(base, "original_fix")),
                    "causal_payload_sha256": digest(decision_payload(bridged, "original_common")),
                    "scope": "PAIRED_INPUT_REQUEST_BRIDGE_ONLY_NOT_A_HOSTED_EFFECT_ESTIMATE", "hosted_calls": 0}
        if args.command != "verify":
            write_new(args.output, result)
        print(json_bytes({"status": "PASS", "command": args.command, "hosted_calls": 0}).decode())
    except (ValueError, TypeError, KeyError, OSError) as error:
        parser.exit(2, "Không thể xử lý causal profile: " + str(error) + "\n")


if __name__ == "__main__":
    main()
