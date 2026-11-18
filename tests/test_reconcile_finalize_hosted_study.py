"""Đối soát UNKNOWN giữ UUID, giới hạn lần thử và reserve mà không mở client."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from uuid import uuid4

from core.finalize_budget_study import MODEL_DECISION
from core.historical_evaluation_journal import load, save
from core.unified_contracts import digest
from core.unified_execution import StageBook
from scripts.finalize_hosted_quota import quota_for
from scripts.reconcile_finalize_hosted_study import find_attempts, reconcile_not_sent


class ReconcileFinalizeHostedTests(unittest.TestCase):
    def setUp(self) -> None:
        scratch = TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        self.grant = {"org_slot": 1, "balance": {"remaining_tokens_24h": None},
                      "local_quota": {"observed_at_utc": "2026-11-18T00:00:00+00:00",
                                      "models": {MODEL_DECISION: {"local_estimated_day_tokens_remaining": 200000,
                                                                  "local_estimated_day_requests_remaining": 1000}}}}
        save(self.root/"grant.json", self.grant)
        operation = {"grant_sha256": digest(self.grant)}
        save(self.root/"release_v2.json", operation)
        self.slot = "forecast/FPT-2023-07-03/u0/r2/original_common"
        self.request_id = str(uuid4())
        directory = self.root/"research"
        self.book = StageBook(directory/"journal", {"release_sha256": digest(self.grant), "phase": "RESEARCH"})

        def stop(_attempt: str) -> dict:
            raise ValueError("Đối chứng chưa có phản hồi")

        with self.assertRaises(ValueError):
            self.book.execute(self.slot, {}, stop)
        self.stage = load(self.book.path(self.slot))
        self.account = quota_for(self.root, self.grant, MODEL_DECISION, lambda: 1795000000.)
        self.account.reserve(self.request_id, self.book.signature, 1000)
        self.row = {"id": self.request_id, "attempt": self.stage["attempts"][0]["attempt_id"], "slot": self.slot,
                    "body": {"model": MODEL_DECISION}, "status": "UNKNOWN", "response": None,
                    "started_at": 1795000000., "reserved_tokens": 1000}
        self.wire = {"run_id": self.book.signature, "slot": self.slot, "rows": [self.row]}
        self.path = directory/"http"/(digest(self.slot)+".json")
        save(self.path, self.wire)
        budget = {"slots": [{"phase": "RESEARCH", "slot": self.slot, "state": "NEW", "model": MODEL_DECISION}]}
        self.enterContext(patch("scripts.reconcile_finalize_hosted_study.check_release", return_value=({}, (budget, None))))
        self.enterContext(patch("scripts.reconcile_finalize_hosted_study.release_for_grant", return_value=operation))

    def test_records_evidence_and_replays_same_reconciliation_without_mutation(self) -> None:
        self.assertEqual(find_attempts(self.root)[0][2], self.row)
        evidence = "Đối chứng transport xác nhận chưa dispatch"
        result = reconcile_not_sent(self.root, self.request_id, evidence)
        self.assertEqual(result["status"], "NOT_SENT")
        self.assertEqual(load(self.path)["rows"], [{**self.row, "status": "NOT_SENT", "reconciliation_sha256": digest(evidence)}])
        self.assertEqual(load(self.book.path(self.slot)), self.stage)
        self.assertEqual(find_attempts(self.root), [])
        self.assertEqual(reconcile_not_sent(self.root, self.request_id, evidence), result)
        self.assertEqual(self.account.attempts(self.book.signature), 1)

    def test_rejects_missing_evidence_or_wrong_uuid_without_editing_checkpoint(self) -> None:
        for request_id, evidence in ((self.request_id, " "), (str(uuid4()), "Bằng chứng của request khác")):
            with self.assertRaises(ValueError):
                reconcile_not_sent(self.root, request_id, evidence)
        self.assertEqual(load(self.path), self.wire)

    def test_rejects_a_wire_with_a_different_stage_uuid(self) -> None:
        modified = {**self.wire, "rows": [{**self.row, "attempt": str(uuid4())}]}
        save(self.path, modified)
        with self.assertRaises(ValueError):
            reconcile_not_sent(self.root, self.request_id, "Đối chứng đúng UUID HTTP")
        self.assertEqual(load(self.path), modified)


if __name__ == "__main__":
    unittest.main()
