"""CLI registry/spec/replay/verify/export offline; chưa có lệnh thu hosted U08."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.bayesian_memory import read_json
from core.unified_contracts import ExperimentSpec, SharedSnapshot, digest, json_bytes
from core.unified_experiment import OfflineResponses, UnifiedRunner, slot_id, verify_run
from core.variant_registry import registry_document
from utils.experiment_io import export_bytes


def replay_bundle(path: Path, expected_sha256: str, root: Path = ROOT) -> dict[str, Any]:
    """Replay prepared assets theo hash công khai, không coi là tái chạy retrieval hoặc HTTP."""
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected_sha256:
        raise ValueError("Bundle không khớp hash được chỉ định")
    bundle = read_json(path)
    if set(bundle) != {"spec", "snapshots", "preparations", "responses", "outcomes"}:
        raise ValueError("Bundle sai fields")
    spec = ExperimentSpec.create(bundle["spec"])
    class PreparedAssets:
        """Nguồn projection đã khóa; runner vẫn dựng lại prompt/schema/policy từ assets."""
        def prepare(self, variant: str, snapshot: SharedSnapshot, dependencies: dict[str, Any], repeat: int) -> dict[str, Any]:
            doc = snapshot.document()
            key = slot_id(doc["point"]["id"], doc["realization"], repeat, variant)
            return bundle["preparations"][key]
    def shared(point: dict[str, Any], realization: int) -> SharedSnapshot:
        doc = bundle["snapshots"][f"{point['id']}/u{realization}"]
        return SharedSnapshot.create(point, realization, doc["payload"], doc["provenance"])
    runner = UnifiedRunner(root, spec, OfflineResponses(bundle["responses"]), input_bundle_sha256=expected_sha256)
    return runner.run(shared, PreparedAssets(), lambda point: bundle["outcomes"][point["id"]])


def main() -> None:
    """Không đọc credential hoặc tạo client ở bất cứ subcommand nào."""
    from scripts.verify_original_fix_parity import deny_external_network
    deny_external_network()
    parser = argparse.ArgumentParser(description="Thí nghiệm thống nhất offline")
    parser.add_argument("--root", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("registry")
    validate = sub.add_parser("validate"); validate.add_argument("spec", type=Path)
    replay = sub.add_parser("replay"); replay.add_argument("bundle", type=Path); replay.add_argument("--sha256", required=True)
    for name in ("verify", "export"):
        command = sub.add_parser(name); command.add_argument("run", type=Path)
        if name == "export":
            command.add_argument("--format", choices=("json", "csv"), default="json")
            command.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "registry":
            result = registry_document()
        elif args.command == "validate":
            spec = ExperimentSpec.create(read_json(args.spec))
            result = {"status": "VALID_SPEC_ONLY", "identity_sha256": digest(spec.identity), "hosted_release": False}
        elif args.command == "replay":
            result = replay_bundle(args.bundle, args.sha256, args.root.resolve())
        else:
            result = verify_run(args.run, root=args.root.resolve())
            if args.command == "export":
                raw, _ = export_bytes(result, args.format)
                if args.output.resolve().is_relative_to((args.root / "outputs").resolve()) and not args.output.resolve().is_relative_to((args.root / "outputs/unified_integration").resolve()):
                    raise ValueError("Không ghi export vào output lịch sử")
                with args.output.open("xb") as handle:
                    handle.write(raw)
                result = {"status": "EXPORTED", "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
        print(json_bytes(result).decode())
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(2, "Không thể xử lý thí nghiệm: " + str(error) + "\n")


if __name__ == "__main__":
    main()
