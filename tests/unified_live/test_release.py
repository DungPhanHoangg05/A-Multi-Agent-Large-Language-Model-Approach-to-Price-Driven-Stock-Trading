"""Kiểm grant mới tách legacy, paid OFF và research chỉ sau đúng hosted smoke."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from core.unified_contracts import digest
from core.unified_live.release import require_release, GRANTS, PREFLIGHT, NAMESPACES, LIMITS


class ReleaseTests(unittest.TestCase):
    """Chỉ stub việc đọc nguồn; không tạo client hoặc đụng grants thật."""
    def setUp(self) -> None:
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.runtime = {"version": "SYNTHETIC_RUNTIME"}
        self.preflight = {"limits": LIMITS, "organizations_independent_user_attested": 5,
                          "metadata": {"all_required_models_listed": True}}
        self.grant = {"status": "SMOKE_RELEASED", "phase": "SMOKE", "api": True, "paid_api_allowed": False,
            "spend_limit_usd": 0, "runtime_sha256": digest(self.runtime), "preflight_sha256": digest(self.preflight),
            "authorization": "USER_REQUEST_CONTINUE_U08_2026_11_10", "namespace": NAMESPACES["SMOKE"], "max_http_attempts": 30}

    def check(self, value: dict, phase: str = "SMOKE") -> tuple:
        """Không kế thừa quyền ngầm từ file release của các đợt trước."""
        with patch("core.unified_live.release.validate_runtime", return_value=self.runtime), \
             patch("core.unified_live.release.anchored", side_effect=lambda _, name: self.preflight if name == PREFLIGHT else value):
            return require_release(self.root, phase)

    def test_exact_smoke_grant_is_accepted(self) -> None:
        runtime, grant = self.check(self.grant)
        self.assertEqual(runtime, self.runtime)
        self.assertEqual(grant, self.grant)

    def test_legacy_revoked_or_pilot_grants_never_authorize_u08(self) -> None:
        for status in ("REVOKED", "PILOT_RELEASED", "RELEASED", "RESEARCH_RELEASED"):
            with self.subTest(status=status), self.assertRaises(ValueError): self.check({**self.grant, "status": status})

    def test_paid_spend_epoch_namespace_and_caps_cannot_be_relaxed(self) -> None:
        for change in ({"paid_api_allowed": True}, {"spend_limit_usd": 1}, {"api": False},
                       {"namespace": NAMESPACES["RESEARCH"]}, {"max_http_attempts": 300}, {"phase": "RESEARCH"}):
            with self.subTest(change=change), self.assertRaises(ValueError): self.check({**self.grant, **change})

    def test_changed_runtime_or_preflight_rejects_before_api(self) -> None:
        for change in ({"runtime_sha256": "0"*64}, {"preflight_sha256": "0"*64}, {"authorization": "OLD_USER_REQUEST"}):
            with self.subTest(change=change), self.assertRaises(ValueError): self.check({**self.grant, **change})

    def test_research_requires_smoke_receipt_and_does_not_fall_back_to_legacy(self) -> None:
        value = {**self.grant, "status": "RESEARCH_RELEASED", "phase": "RESEARCH",
                 "namespace": NAMESPACES["RESEARCH"], "max_http_attempts": 7956}
        with self.assertRaises(FileNotFoundError): self.check(value, "RESEARCH")


if __name__ == "__main__":
    unittest.main()
