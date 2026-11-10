"""CLI U08: prepare/grant tách khỏi collect; status và verify không tạo client."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from core.historical_evaluation_journal import load, save
from core.unified_contracts import digest
from core.unified_live.release import (RUNTIME, PREFLIGHT, GRANTS, LIMITS, NAMESPACES,
    freeze_runtime, history, anchored, validate_runtime)


def create(path: Path, value: dict) -> None:
    """Không overwrite receipt/grant đã neo hoặc đã dùng cho inference."""
    if path.exists() and load(path) != value:
        raise ValueError("Artifact đã có nội dung khác, cần version riêng: " + path.name)
    if not path.exists():
        save(path, value)


def prepare(root: Path, metadata_path: Path) -> dict:
    """Khóa nguồn mới và catalog đã GET; không gọi inference hoặc sửa protocol cũ."""
    metadata = json.loads(metadata_path.read_bytes())
    if (metadata["metadata_requests"] != 5 or metadata["inference_requests"] != 0
            or not metadata["all_required_models_listed"]
            or len({r["credential_hmac"] for r in metadata["rows"]}) != 5
            or any(v["active"] is not True for r in metadata["rows"] for v in r["model_catalog"].values())):
        raise ValueError("Catalog không đủ năm slot/model đang active")
    identifiers = [r["provider_org_sha256"] for r in metadata["rows"] if r["provider_org_sha256"]]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("Catalog báo nhiều key cùng org; không nhân quota")
    age = datetime.now(timezone.utc).timestamp() - datetime.fromisoformat(metadata["observed_at_utc"]).timestamp()
    if not 0 <= age < 86400:
        raise ValueError("Metadata đã cũ hoặc clock không hợp lệ")
    runtime = freeze_runtime(root)
    carry = history(root)
    preflight = {"version": "unified_live_preflight_v1", "metadata": metadata, "limits": LIMITS,
        "organizations_independent_user_attested": 5, "organization_ids_provider_verified": metadata["provider_org_identity_available"],
        "plan": "FREE_USER_ATTESTED", "split_input_output_limits": False, "paid_api_allowed": False,
        "attestation_source": "USER_CONFIRMED_2026_11_10_FIVE_INDEPENDENT_FREE_ORGS_SAME_LIMITS",
        "authorization_request": "USER_REQUEST_CONTINUE_U08_2026_11_10",
        "carry_requests": sum(len(v) for v in carry.values()),
        "carry_charged_or_reserved_tokens": sum(r.get("total_tokens") or r["reserved_tokens"] for rows in carry.values() for r in rows),
        "provider_headers": "VALIDATE_ON_FIRST_RESPONSE_PER_ORG_AND_BEFORE_SUBSEQUENT_ADMISSION",
        "sources": ["https://console.groq.com/docs/models", "https://console.groq.com/docs/rate-limits"],
        "api_inference_before_release": 0, "spend_limit_usd": 0}
    create(root / RUNTIME, runtime)
    create(root / PREFLIGHT, preflight)
    return {"status": "PREPARED_U08_NOT_RELEASED", "points": len(runtime["points"]), "carry_requests": preflight["carry_requests"]}


def grant(root: Path, phase: str) -> dict:
    """Cụ thể hóa quyền người dùng tiếp tục U08, smoke PASS mới được mở research."""
    runtime = validate_runtime(root)
    preflight = anchored(root, PREFLIGHT)
    value = {"version": "unified_live_release_v1", "status": phase + "_RELEASED", "phase": phase,
        "api": True, "paid_api_allowed": False, "spend_limit_usd": 0,
        "authorization": "USER_REQUEST_CONTINUE_U08_2026_11_10",
        "runtime_sha256": digest(runtime), "preflight_sha256": digest(preflight),
        "namespace": NAMESPACES[phase], "max_http_attempts": 30 if phase == "SMOKE" else 7956,
        "legacy_release_inherited": False, "automatic_N_repeat_model_reduction": False}
    if phase == "RESEARCH":
        from core.unified_live.manager import verify_phase
        receipt = verify_phase(root, "SMOKE")
        if receipt["status"] != "PASS_U08_SMOKE":
            raise ValueError("Chưa có smoke PASS")
        value["smoke_receipt_sha256"] = digest(receipt)
    create(root / GRANTS[phase], value)
    return value


def main() -> None:
    """Chỉ lệnh collect mới được tạo client, sau khi toàn bộ grant/source đã neo Git."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "grant", "collect", "verify", "status"))
    parser.add_argument("--phase", choices=("SMOKE", "RESEARCH"), default="SMOKE")
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--seal", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            result = prepare(ROOT, args.metadata)
        elif args.command == "grant":
            result = grant(ROOT, args.phase)
        else:
            from core.unified_live.manager import collect, verify_phase, status
            if args.command == "collect":
                result = collect(ROOT, args.phase)
            elif args.command == "verify":
                from scripts.verify_original_fix_parity import deny_external_network
                deny_external_network()
                result = verify_phase(ROOT, args.phase, seal=args.seal)
            else:
                result = status(ROOT, args.phase)
        print(json.dumps(result, ensure_ascii=False), flush=True)
    except Exception as error:
        parser.exit(2, "U08 dừng: " + str(error) + "\n")


if __name__ == "__main__":
    main()
