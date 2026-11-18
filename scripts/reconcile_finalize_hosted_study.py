"""Kiểm và đối soát attempt UNKNOWN của FIN11 từ bằng chứng cục bộ, không gọi API."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import sys
from uuid import UUID

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.finalize_budget_quota import ATTEMPT_CAP, ORG
from core.historical_evaluation_journal import load, save
from core.prior_run_lock import PriorRunLock, utc_now
from core.serving_runtime.transport import Calls
from core.unified_contracts import digest, json_bytes
from core.unified_execution import StageBook
from scripts.finalize_hosted_point_reset import archive_lost_point, archived_resets
from scripts.finalize_hosted_quota import quota_for
from scripts.finalize_hosted_study import PHASES, RUN, account_grant, check_release, release_for_grant, verify_operation


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


def reconcile_attempt(root: Path, request_id: str, evidence: str, disposition: str) -> dict:
    """Lưu xác nhận đúng UUID, giữ attempt và token reserve trong ledger cũ."""
    if str(UUID(request_id)) != request_id or not evidence.strip() or disposition not in {"NOT_SENT", "RESPONSE_LOST"}:
        raise ValueError("Cần UUID chuẩn và nội dung bằng chứng đối soát")
    grant = load(root/"grant.json")
    release, (budget, _) = check_release()
    operation = release_for_grant(grant, release)
    with PriorRunLock(root/"worker", digest(grant)):
        verify_operation(root, release, operation)
        matches = find_attempts(root, request_id)
        if len(matches) != 1:
            raise ValueError("UUID không thuộc duy nhất một attempt FIN11")
        phase, wire, row = matches[0]
        if row["status"] == disposition and row.get("reconciliation_sha256") == digest(evidence):
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
        if disposition == "NOT_SENT":
            calls = Calls(directory, book.signature, account, sender=None, guard=reject_dispatch)
            calls.reconcile_not_sent(slot, request_id, evidence)
        else:
            prior = sum(record["attempts_by_slot"].get(slot, 0) for record in archived_resets(root, grant))
            if prior+len(wire["rows"]) >= ATTEMPT_CAP:
                raise ValueError("Slot đã hết lần thử trong cap FIN09")
            row.update(status="RESPONSE_LOST", provider_http_status=200, reconciliation_sha256=digest(evidence),
                       reconciliation_source="OWNER_REPORTED_HTTP_200")
            save(directory/"http"/(digest(slot)+".json"), wire)
            status = root/"status.json"
            if not status.exists() or load(status)["status"] == "UNKNOWN_NEEDS_RECONCILIATION":
                save(status, {**summary(phase, row), "status": "SLOT_READY_TO_REPLAY", "at": utc_now()})
        return summary(phase, {**row, "status": disposition})


def reconcile_not_sent(root: Path, request_id: str, evidence: str) -> dict:
    """Đối soát attempt chưa gửi bằng cùng các rào hợp đồng của FIN11."""
    return reconcile_attempt(root, request_id, evidence, "NOT_SENT")


def reject_dispatch() -> None:
    """Chặn reserve và gửi nếu đường đối soát bị gọi sai."""
    raise ValueError("Lệnh đối soát chỉ chạy offline")


def reset_point(root: Path, point: str, request_id: str) -> dict:
    """Tách point đang dở theo xác nhận HTTP 200 của tác giả, không gửi request."""
    if str(UUID(request_id)) != request_id:
        raise ValueError("Cần UUID HTTP hợp lệ")
    grant = load(root/"grant.json")
    release, (budget, _) = check_release()
    operation = release_for_grant(grant, release)
    with PriorRunLock(root/"worker", digest(grant)):
        verify_operation(root, release, operation)
        record = archive_lost_point(root, grant, budget, point, request_id)
        result = {"status": "POINT_READY_TO_REPLAY", "phase": "RESEARCH", "point": point,
                  "archived_attempts": record["archived_attempts"], "manifest_sha256": digest(record)}
        path = root/"status.json"
        if not path.exists() or load(path)["status"] == "UNKNOWN_NEEDS_RECONCILIATION":
            save(path, {**result, "at": utc_now()})
        return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="mode", required=True)
    commands.add_parser("list", help="Liệt kê các UUID đang UNKNOWN")
    not_sent = commands.add_parser("not-sent", help="Xác nhận chưa gửi khi có bằng chứng cho đúng UUID")
    not_sent.add_argument("--request-id", required=True)
    not_sent.add_argument("--evidence", type=Path, required=True, help="File UTF-8 ghi nguồn bằng chứng đối soát")
    lost = commands.add_parser("response-lost", help="Giữ HTTP 200 đã xác nhận và chỉ chạy lại slot thiếu raw")
    lost.add_argument("--request-id", required=True)
    lost.add_argument("--evidence", type=Path, required=True, help="File UTF-8 ghi xác nhận HTTP 200 và việc thiếu raw")
    reset = commands.add_parser("reset-point", help="Tách point đang dở khi đã xác nhận HTTP 200 nhưng thiếu raw")
    reset.add_argument("--request-id", required=True)
    reset.add_argument("--point", required=True)
    reset.add_argument("--http-status", type=int, choices=(200,), required=True, help="HTTP status do tác giả xác nhận")
    args = parser.parse_args()
    if args.mode == "list":
        result = [summary(phase, row) for phase, _, row in find_attempts(RUN)]
    elif args.mode == "not-sent":
        result = reconcile_not_sent(RUN, args.request_id, args.evidence.read_text(encoding="utf-8-sig"))
    elif args.mode == "response-lost":
        result = reconcile_attempt(RUN, args.request_id, args.evidence.read_text(encoding="utf-8-sig"), "RESPONSE_LOST")
    else:
        result = reset_point(RUN, args.point, args.request_id)
    print(json_bytes(result).decode())


if __name__ == "__main__":
    main()
