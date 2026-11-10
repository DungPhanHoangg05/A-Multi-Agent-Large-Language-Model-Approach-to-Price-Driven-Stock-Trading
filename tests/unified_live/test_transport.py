"""Kiểm ranh live/mock, cap/repair qua restart và gate trước credential."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import httpx

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests"))
from test_unified_experiment import UnifiedFixture
from scripts.check_unified_execution import control_response
from core.unified_execution_transport import body_for, MockHTTP, Deferred, Exhausted, Uncertain
from core.unified_live.transport import LiveCalls, LiveHTTP
from core.unified_contracts import digest


class LiveTransportTests(unittest.TestCase):
    """Mock rõ mode HOSTED_TEST; gọi constructor live thiếu grant phải dừng trước key/client."""
    def setUp(self) -> None:
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        fixture = UnifiedFixture(self.root)
        request = fixture.methods().prepare("original_common", fixture.snapshot, {}, 0)["request"]
        request["max_tokens"] = 960
        self.body = body_for(request)
        self.identity = {"mode": "HOSTED_TEST", "phase": "SMOKE", "epoch": "TEST_SMOKE", "attempt_cap_total": 30}
        self.now = [2000000000.]
        self.sent = []

    def calls(self, handler: object = None, *, guard: object = None, identity: dict | None = None) -> LiveCalls:
        """Mỗi instance đọc lại ledger thật của fixture, không mock persistence."""
        def send(request: httpx.Request) -> httpx.Response:
            self.sent.append(json.loads(request.content))
            return (handler or control_response)(request)
        return LiveCalls(self.root / "run", identity or self.identity, MockHTTP(send), {i: [] for i in range(1, 6)},
                         lambda: self.now[0], guard or (lambda: None), test_mode=True)

    def test_missing_release_rejects_before_dotenv_or_client(self) -> None:
        with patch("dotenv.dotenv_values", side_effect=AssertionError("Không được đọc key")), \
             patch("httpx.Client", side_effect=AssertionError("Không được tạo client")):
            with self.assertRaises((ValueError, FileNotFoundError)):
                LiveHTTP(self.root, "SMOKE", lambda: None)

    def test_test_sender_cannot_claim_hosted_identity(self) -> None:
        with self.assertRaises(ValueError): self.calls(identity={**self.identity, "mode": "HOSTED"})

    def test_guard_revoked_before_intent_sends_nothing(self) -> None:
        def denied() -> None:
            raise ValueError("Thu hồi grant")
        with self.assertRaises(ValueError): self.calls(guard=denied).call("forecast/p/v", 1, self.body, "attempt")
        self.assertEqual(self.sent, [])
        self.assertFalse((self.root / "run/wire.json").exists())

    def test_model_temperature_and_implicit_sdk_options_rejected(self) -> None:
        for change in ({"model": "other"}, {"temperature": .4}, {"n": True}, {"max_tokens": 1000}, {"seed": 42}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.calls().call("forecast/p/v", 1, {**self.body, **change}, "attempt")
        self.assertEqual(self.sent, [])

    def test_raw200_replay_uses_same_uuid_and_ledger_mode_hosted_test(self) -> None:
        first, row = self.calls().call("forecast/p/v", 1, self.body, "attempt")
        second, replay = self.calls().call("forecast/p/v", 1, self.body, "attempt")
        self.assertEqual(first, second)
        self.assertEqual(row["id"], replay["id"])
        self.assertEqual(len(self.sent), 1)
        self.assertEqual(self.calls().state["identity"]["mode"], "HOSTED_TEST")

    def test_timeout_stays_unknown_after_new_instance(self) -> None:
        def timeout(request: httpx.Request) -> httpx.Response:
            raise httpx.ReadTimeout("CONTROL", request=request)
        with self.assertRaises(Uncertain): self.calls(timeout).call("forecast/p/v", 1, self.body, "attempt")
        with self.assertRaises(Uncertain): self.calls().call("forecast/p/v", 1, self.body, "attempt")
        self.assertEqual(len(self.sent), 1)

    def test_repair_and_transient_share_three_attempt_cap(self) -> None:
        codes = [503, 200, 200]
        def send(request: httpx.Request) -> httpx.Response:
            code = codes.pop(0)
            if code == 503:
                return httpx.Response(503, headers={"retry-after": "12"}, text="retry after 15 seconds")
            if codes:
                return httpx.Response(200, json={"choices": [{"message": {"content": "{}"}}]})
            return control_response(request)
        for _ in range(10):
            try:
                reply, row = self.calls(send).call("forecast/p/v", 1, self.body, "attempt")
                break
            except Deferred as error:
                self.now[0] = error.until + .01
        self.assertEqual(reply["decision"], "SHORT")
        self.assertTrue(row["repair"])
        self.assertEqual(len(self.sent), 3)

    def test_phase_cap_keeps_replay_but_stops_new_http(self) -> None:
        identity = {**self.identity, "attempt_cap_total": 1}
        calls = self.calls(identity=identity)
        calls.call("forecast/p/v", 1, self.body, "attempt")
        calls.call("forecast/p/v", 1, self.body, "attempt")
        with self.assertRaises(Exhausted): calls.call("forecast/p/other", 2, self.body, "attempt2")
        self.assertEqual(len(self.sent), 1)

    def test_restart_cannot_drop_carry_or_change_epoch(self) -> None:
        self.calls().call("forecast/p/v", 1, self.body, "attempt")
        with self.assertRaises(ValueError): self.calls(identity={**self.identity, "epoch": "NEW"})


if __name__ == "__main__":
    unittest.main()
