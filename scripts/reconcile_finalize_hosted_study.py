"""Kiểm và đối soát attempt UNKNOWN của FIN11 từ bằng chứng cục bộ, không gọi API."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.finalize_budget_quota import ORG
from core.historical_evaluation_journal import load
from core.prior_run_lock import PriorRunLock
from core.serving_runtime.transport import Calls
from core.unified_contracts import digest, json_bytes
from core.unified_execution import StageBook
from scripts.finalize_hosted_quota import quota_for
from scripts.finalize_hosted_study import PHASES, RUN, account_grant, check_release, release_for_grant


def find_attempts(root: Path, request_id: str | None = None) -> list[tuple[str, dict, dict]]:
    """Đọc envelope wire đúng đường dẫn, tìm UNKNOWN hoặc một UUID chính xác."""
    matches = []
    for phase in PHASES:
        for path in (root/phase.lower()/"http").glob("*.json"):
            wire = load(path)
            if path.stem != digest(wire["slot"]):
                raise ValueError("Wire nằm ngoài slot đã khóa")
            for row in wire["rows"]:
                matches_request = row["status"] == "UNKNOWN" if request_id is None else row["id"] == request_id
                if matches_request:
                    matches.append((phase, wire, row))
    return matches


def summary(phase: str, row: dict) -> dict:
    """Chỉ xuất đủ metadata để đối chiếu log nhà cung cấp."""
    started = datetime.fromtimestamp(row["started_at"], timezone.utc)
    return {"phase": phase, "slot": row["slot"], "request_id": row["id"], "org_slot": row.get("org_slot", ORG),
            "model": row["body"]["model"], "started_at": started.isoformat(), "status": row["status"]}


def reconcile_not_sent(root: Path, request_id: str, evidence: str) -> dict:
    """Lưu xác nhận đúng UUID, giữ attempt và token reserve trong ledger cũ."""
    if str(UUID(request_id)) != request_id or not evidence.strip():
        raise ValueError("Cần UUID chuẩn và nội dung bằng chứng chưa gửi")
    grant = load(root/"grant.json")
    release, (budget, _) = check_release()
    operation = release_for_grant(grant, release)
    with PriorRunLock(root/"worker", digest(grant)):
        if load(root/"release_v2.json") != operation:
            raise ValueError("Release vận hành khác grant FIN11")
        matches = find_attempts(root, request_id)
        if len(matches) != 1:
            raise ValueError("UUID không thuộc duy nhất một attempt FIN11")
        phase, wire, row = matches[0]
        if row["status"] == "NOT_SENT" and row.get("reconciliation_sha256") == digest(evidence):
            return summary(phase, row)
        slot, model = row["slot"], row["body"]["model"]
        plan_matches = [p for p in budget["slots"] if (p["phase"], p["slot"]) == (phase, slot)]
        if (row is not wire["rows"][-1] or wire["slot"] != slot or row["status"] != "UNKNOWN"
                or row.get("response") is not None or len(plan_matches) != 1
                or plan_matches[0]["state"] != "NEW" or plan_matches[0]["model"] != model
                or row["id"] == row["attempt"]):
            raise ValueError("Attempt khác slot UNKNOWN cuối hoặc đã có raw")
        directory = root/phase.lower()
        journal = directory/"journal"
        identity = load(journal/"identity.json")["identity"]
        book = StageBook(journal, identity, verify_only=True)
        stage = load(book.path(slot))
        if (identity["release_sha256"] != digest(grant) or identity["phase"] != phase
                or wire["run_id"] != book.signature or stage["signature"] != book.signature
                or stage["run_uuid"] != book.uuid or stage["slot"] != slot or len(stage["attempts"]) != 1
                or stage["attempts"][0]["attempt_id"] != row["attempt"] or stage["attempts"][0]["status"] != "unknown"):
            raise ValueError("UUID HTTP không khớp checkpoint đang chờ")
        account = quota_for(root, account_grant(root, grant, row.get("org_slot", ORG)), model)
        with account.connect() as db:
            known = db.execute("SELECT run, state, reserve FROM attempts WHERE id=?", (request_id,)).fetchone()
        if known != (book.signature, "UNKNOWN", row["reserved_tokens"]):
            raise ValueError("Sổ quota không khớp intent đang đối soát")
        calls = Calls(directory, book.signature, account, sender=None, guard=reject_dispatch)
        calls.reconcile_not_sent(slot, request_id, evidence)
        return summary(phase, {**row, "status": "NOT_SENT"})


def reject_dispatch() -> None:
    """Chặn reserve và gửi nếu đường đối soát bị gọi sai."""
    raise ValueError("Lệnh đối soát chỉ chạy offline")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="mode", required=True)
    commands.add_parser("list", help="Liệt kê các UUID đang UNKNOWN")
    not_sent = commands.add_parser("not-sent", help="Xác nhận chưa gửi khi có bằng chứng cho đúng UUID")
    not_sent.add_argument("--request-id", required=True)
    not_sent.add_argument("--evidence", type=Path, required=True, help="File UTF-8 ghi nguồn bằng chứng đối soát")
    args = parser.parse_args()
    if args.mode == "list":
        result = [summary(phase, row) for phase, _, row in find_attempts(RUN)]
    else:
        result = reconcile_not_sent(RUN, args.request_id, args.evidence.read_text(encoding="utf-8-sig"))
    print(json_bytes(result).decode())


if __name__ == "__main__":
    main()
