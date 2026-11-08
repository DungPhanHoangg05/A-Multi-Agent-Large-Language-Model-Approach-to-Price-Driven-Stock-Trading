"""Đối soát503/quota của supervisor bằng journal/HTTP fixture, không gọi mạng."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from core.bayesian_memory import atomic_write_json
from core.historical_evaluation_journal import RunBook, load, save
from core.historical_evaluation_protocol import digest
from scripts.run_historical_collection import interruption, phase_result, sync_plan


class SupervisorTests(unittest.TestCase):
    """Chỉ retry bằng chứng đúng UUID, quota chưa dispatch và phase hoàn tất thật."""

    def fixture(self, *, status: int | None = 503, attempts: int = 1) -> tuple:
        temp = TemporaryDirectory(); self.addCleanup(temp.cleanup)
        directory = Path(temp.name)
        book = RunBook(directory, {"scope": "SUPERVISOR_FIXTURE"})
        for index in range(attempts):
            if index:
                book.reconcile(load(book.path("graph/test/pattern"))["attempts"][-1]["attempt_id"], "Fixture authorize")
            with self.assertRaises(RuntimeError):
                book.execute("graph/test/pattern", {"org": 1}, lambda _: (_ for _ in ()).throw(RuntimeError("fixture")))
        doc = load(book.path("graph/test/pattern"))
        rows = []
        if status is not None:
            for a in doc["attempts"]:
                path = directory / "http" / (a["attempt_id"] + ".json")
                raw = {"status": status, "slot": {"checkpoint_attempt_id": a["attempt_id"], "run_signature": book.signature},
                       "request_legacy_body_sha256": "body", "headers": {}}
                save(path, raw)
                rows.append({"id": a["attempt_id"], "checkpoint_attempt_id": a["attempt_id"], "status": status,
                             "run_signature": book.signature, "historical_raw": {"path": path.relative_to(directory).as_posix(),
                             "sha256": hashlib.sha256(path.read_bytes()).hexdigest()},
                             "improvement_audit": {"request": {"canonical_body_sha256": "body"}}})
        ledger = {"requests": rows}
        atomic_write_json(directory / "usage/org1.json", ledger)
        return directory, load(directory / "identity.json"), doc, ledger

    def test_503_requires_durable_raw_and_returns_exact_uuid_with_backoff(self) -> None:
        directory, identity, doc, _ = self.fixture()
        action = interruption(directory, identity, now=100.)
        self.assertEqual(action["attempt_id"], doc["attempts"][-1]["attempt_id"])
        self.assertEqual(action["reason"], "RAW_HTTP503_AUDITED")
        self.assertEqual(action["resume_at"], 130.)

    def test_three_http_attempts_do_not_authorize_fourth(self) -> None:
        directory, identity, _, _ = self.fixture(attempts=3)
        self.assertIsNone(interruption(directory, identity))

    def test_200_and_transport_unknown_are_not_503_recovery(self) -> None:
        directory, identity, _, ledger = self.fixture(status=200)
        self.assertIsNone(interruption(directory, identity))
        ledger["requests"][0]["status"] = "transport_error"
        ledger["requests"][0].pop("historical_raw")
        atomic_write_json(directory / "usage/org1.json", ledger)
        self.assertIsNone(interruption(directory, identity))

    def test_raw_tampering_is_rejected(self) -> None:
        directory, identity, _, ledger = self.fixture()
        (directory / ledger["requests"][0]["historical_raw"]["path"]).write_bytes(b"wrong")
        with self.assertRaises(ValueError): interruption(directory, identity)

    def test_daily_quota_wait_requires_no_current_http_and_fresh_reset_event(self) -> None:
        directory, identity, doc, ledger = self.fixture(status=None)
        started = datetime.fromisoformat(doc["attempts"][-1]["started_at"]).timestamp()
        ledger["last_stop"] = {"reason": "DAILY_QUOTA", "at": started + 1,
                               "resume_not_before_utc": datetime.fromtimestamp(started + 3600, timezone.utc).isoformat()}
        atomic_write_json(directory / "usage/org1.json", ledger)
        action = interruption(directory, identity, now=started + 2)
        self.assertEqual(action["reason"], "PRE_DISPATCH_QUOTA_AUDITED")
        self.assertEqual(action["resume_at"], started + 3602)
        ledger["last_stop"]["at"] = started - 1
        atomic_write_json(directory / "usage/org1.json", ledger)
        self.assertIsNone(interruption(directory, identity))

    def test_quota_of_other_org_cannot_authorize_pending_slot(self) -> None:
        directory, identity, doc, _ = self.fixture(status=None)
        started = datetime.fromisoformat(doc["attempts"][-1]["started_at"]).timestamp()
        ledger = {"requests": [], "last_stop": {"reason": "DAILY_QUOTA", "at": started + 1,
                  "resume_not_before_utc": datetime.fromtimestamp(started + 3600, timezone.utc).isoformat()}}
        atomic_write_json(directory / "usage/org2.json", ledger)
        self.assertIsNone(interruption(directory, identity))

    def test_provider_429_wait_uses_saved_raw_and_retry_until(self) -> None:
        directory, identity, doc, ledger = self.fixture(status=429)
        ledger["requests"][0]["retry_until"] = 5000.
        atomic_write_json(directory / "usage/org1.json", ledger)
        action = interruption(directory, identity, now=100.)
        self.assertEqual(action["reason"], "HTTP429_PROVIDER_WAIT_AUDITED")
        self.assertEqual(action["resume_at"], 5002.)

    def test_partial_exit_zero_is_not_phase_complete(self) -> None:
        with TemporaryDirectory() as folder:
            path = Path(folder) / "log"
            path.write_text(json.dumps({"status": "PARTIAL", "cohort": "CORE4", "completed_units": 1, "planned_units": 480}))
            with self.assertRaises(ValueError): phase_result(path, "CORE4", 480)
            path.write_text('Dòng log\n' + json.dumps({"status": "PHASE_COMPLETE", "cohort": "CORE4", "completed_units": 480, "planned_units": 480}), encoding="utf-8")
            self.assertEqual(phase_result(path, "CORE4", 480)["completed_units"], 480)

    def test_progress_only_changes_owned_marker_and_done_requires_receipt(self) -> None:
        with TemporaryDirectory() as folder, patch('scripts.run_historical_collection.ROOT', Path(folder)):
            root = Path(folder)
            names = ('docs/plan/plan.md', 'docs/plan/week11/README.md', 'docs/plan/week11/historical_reevaluation_plan.md')
            for name in names:
                path = root / name; path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('GIỮ TRƯỚC\n<!-- H07_MANAGED_START -->\ncũ\n<!-- H07_MANAGED_END -->\nGIỮ SAU', encoding='utf-8')
            state = {'state': 'RUNNING', 'updated_at': '2026-11-08T12:00:00Z', 'run_uuid': 'fixture'}
            sync_plan(state)
            for name in names:
                text = (root/name).read_text(encoding='utf-8')
                self.assertTrue(text.startswith('GIỮ TRƯỚC'))
                self.assertTrue(text.endswith('GIỮ SAU'))
                self.assertIn('19:00:00 UTC+7', text)
            state['state'] = 'COMPLETE'
            with self.assertRaises(FileNotFoundError): sync_plan(state)
            self.assertNotIn('COMPLETE', (root/names[0]).read_text(encoding='utf-8'))


if __name__ == "__main__":
    unittest.main()
