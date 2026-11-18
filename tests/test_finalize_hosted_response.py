"""Kiểm phục hồi phản hồi FIN11 qua lần lỗi và khi đổi org bằng HTTP mock."""
from datetime import datetime, timezone
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import httpx

from core.finalize_budget_study import MODEL_DECISION
from core.historical_evaluation_journal import save
from core.serving_runtime.quota import Unknown
from scripts.finalize_hosted_quota import HostedWire, quota_for
from scripts.finalize_hosted_response import HostedHTTP


NOW = 1795000000.
BODY = {"model": MODEL_DECISION, "messages": [{"role": "user", "content": "Đối chứng"}], "max_completion_tokens": 32}
RAW = {"choices": [{"message": {"content": "Phản hồi đối chứng"}}], "usage": {"total_tokens": 20}}


class InterruptedBody(httpx.SyncByteStream):
    """Có HTTP status nhưng mất kết nối trước khi hoàn tất body."""

    def __iter__(self):
        yield b'{"choices":'
        raise httpx.ReadError("Đối chứng mất body")


class HostedResponseTests(unittest.TestCase):
    def setUp(self) -> None:
        scratch = TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        self.quotas = {}

    def wire(self, org: int, send) -> HostedWire:
        if org not in self.quotas:
            grant = {"org_slot": org, "balance": {"remaining_tokens_24h": None},
                     "local_quota": {"observed_at_utc": datetime.fromtimestamp(NOW, timezone.utc).isoformat(),
                                     "models": {MODEL_DECISION: {"local_estimated_day_tokens_remaining": 200000,
                                                                 "local_estimated_day_requests_remaining": 1000}}}}
            self.quotas[org] = quota_for(self.root, grant, MODEL_DECISION, lambda: NOW)
        client = HostedHTTP.__new__(HostedHTTP)
        client.client = self.enterContext(httpx.Client(transport=httpx.MockTransport(send)))
        return HostedWire(self.root, "run", sender=client, guard=lambda: None, clock=lambda: NOW,
                          org_slot=org, quota_at=self.quotas.__getitem__)

    def test_durable_body_is_recovered_after_restart_on_another_org_without_calling_again(self) -> None:
        def fail_primary(path: Path, value: dict) -> None:
            if path.parent.name == "http" and value["rows"][-1]["status"] == 200:
                raise OSError("Đối chứng crash trước khi thay thế wire chính")
            save(path, value)

        original = self.wire(1, lambda _: httpx.Response(200, json=RAW))
        with patch("core.serving_runtime.transport.save", side_effect=fail_primary), self.assertRaises(OSError):
            original.call("slot", BODY, "stage")
        old_uuid = original._rows("slot")[1][0]["id"]
        resumed = self.wire(2, lambda _: self.fail("Đã có bản lưu body, không được gửi lại"))
        _, wire = resumed.call("slot", BODY, "stage")
        self.assertEqual((wire["id"], wire["org_slot"], wire["usage"]), (old_uuid, 1, 20))
        self.assertEqual(self.quotas[2].attempts("run"), 0)

    def test_confirmed_http_200_with_lost_body_retries_only_that_slot_and_keeps_charge(self) -> None:
        responses = iter([httpx.Response(200, stream=InterruptedBody()), httpx.Response(200, json=RAW)])
        wire = self.wire(1, lambda _: next(responses))
        wire.call("slot", BODY, "stage")
        rows = wire._rows("slot")[1]
        self.assertEqual([r["status"] for r in rows], ["RESPONSE_LOST", 200])
        self.assertEqual(rows[0]["provider_http_status"], 200)
        with self.quotas[1].connect() as db:
            reserved, used = db.execute("SELECT reserve,used FROM attempts WHERE id=?", (rows[0]["id"],)).fetchone()
        self.assertGreater(reserved, 0)
        self.assertIsNone(used)
        self.assertEqual(json.loads(rows[1]["response"]), RAW)

    def test_failure_before_http_status_does_not_get_resent_blindly(self) -> None:
        def fail(_):
            raise httpx.ReadTimeout("Đối chứng chưa có status")

        first = self.wire(1, fail)
        with self.assertRaises(Unknown):
            first.call("slot", BODY, "stage")
        second = self.wire(2, lambda _: self.fail("Thiếu bằng chứng HTTP, không gửi lại"))
        with self.assertRaises(Unknown):
            second.call("slot", BODY, "stage")
        self.assertEqual(self.quotas[2].attempts("run"), 0)


if __name__ == "__main__":
    unittest.main()
