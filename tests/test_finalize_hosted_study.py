"""Kiểm admission FIN11 bằng journal và transport đối chứng, không đọc key thật."""
from __future__ import annotations

from contextlib import redirect_stdout
from copy import deepcopy
from datetime import datetime
import io
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from core.finalize_budget_archive import Archive
from core.finalize_budget_study import MODEL_DECISION, StudyProvider
from core.groq_pacing import MODEL_LIMITS
from core.serving_runtime.quota import Failed, Waiting
from core.serving_runtime.resources import default_models
from scripts.finalize_hosted_study import HostedStudyRunner, check_release, quota_for, verify_balance
from scripts.finalize_offline_fixture import Fixture
from scripts.prepare_finalize_api_budget import study

ROOT = Path(__file__).resolve().parents[1]
DATE = "2023-11-14T22:13:20+00:00"
NOW = datetime.fromisoformat(DATE).timestamp()


def grant_fixture(remaining: int = 200000) -> dict:
    """Thông tin chủ org đối chứng, có local carry cùng cửa sổ."""
    return {"balance": {"org_slot": 1, "tier": "FREE", "observed_at": DATE,
                        "remaining_tokens_24h": dict.fromkeys(MODEL_LIMITS, remaining),
                        "source": "OWNER_ATTESTED_GROQ_CONSOLE"},
            "local_quota": {"observed_at_utc": DATE, "models": {model: {
                "local_estimated_day_tokens_remaining": 199900, "local_estimated_day_requests_remaining": 998}
                for model in MODEL_LIMITS}}}


class HostedStudyTests(unittest.TestCase):
    def test_grant_requires_fresh_free_balance_for_both_models(self) -> None:
        data = grant_fixture()["balance"]
        self.assertEqual(verify_balance(data, NOW), NOW)
        for changed in ({"tier": "DEVELOPER"}, {"org_slot": 2}, {"remaining_tokens_24h": {}}):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                verify_balance({**data, **changed}, NOW)
        with self.assertRaises(ValueError):
            verify_balance(data, NOW+86400)
        owner = {**data, "source": "OWNER_ATTESTED_SUFFICIENT", "remaining_tokens_24h": None}
        self.assertEqual(verify_balance(owner, NOW), NOW)
        with self.assertRaises(ValueError):
            verify_balance({**owner, "remaining_tokens_24h": data["remaining_tokens_24h"]}, NOW)

    def test_seed_keeps_same_budget_across_phases_and_restart(self) -> None:
        grant = grant_fixture(4000)
        with TemporaryDirectory() as directory:
            root = Path(directory)
            smoke = quota_for(root, grant, MODEL_DECISION, lambda: NOW)
            smoke.reserve("smoke-id", "smoke", 3500)
            smoke.finish("smoke-id", "200", 3000)
            research = quota_for(root, grant, MODEL_DECISION, lambda: NOW+62)
            with self.assertRaises(Waiting):
                research.reserve("study-id", "research", 1001)
            research.reserve("study-id", "research", 1000)
            other = deepcopy(grant)
            other["balance"]["remaining_tokens_24h"][MODEL_DECISION] += 1
            with self.assertRaises(ValueError):
                quota_for(root, other, MODEL_DECISION, lambda: NOW+62)

    def test_provider_limits_below_grant_stop_after_raw(self) -> None:
        with TemporaryDirectory() as directory:
            model = quota_for(Path(directory), grant_fixture(), MODEL_DECISION, lambda: NOW)
            model.reserve("attempt-id", "run", 1000)
            with self.assertRaises(Failed):
                model.observe("attempt-id", {"x-ratelimit-limit-tokens": "6000"}, NOW)
            self.assertEqual(model.attempts("run"), 1)

    def test_smoke_real_provider_bindings_checkpoint_and_cold_verify(self) -> None:
        from scripts.verify_original_fix_parity import deny_external_network
        from unittest.mock import patch
        import socket
        import torch
        torch.set_num_threads(1)
        with patch.object(socket.socket, "connect", socket.socket.connect), patch.object(
                socket.socket, "connect_ex", socket.socket.connect_ex), patch.dict("os.environ"):
            deny_external_network()
            release, (budget, resources) = check_release()
            cohort, variants, _, _ = study(ROOT)
            points = [row for row in cohort if row["id"] == budget["smoke_point_id"]]
            provider = StudyProvider(resources, points, default_models(), variants)
            archive = Archive(ROOT)
            fixture = Fixture()
            grant = {**release, **grant_fixture()}
            with TemporaryDirectory() as directory, redirect_stdout(io.StringIO()):
                root = Path(directory)
                runner = HostedStudyRunner(root, grant, budget, cohort, "SMOKE", provider, archive,
                                           fixture.transport, fixture.clock)
                runner.collect(lambda *args: self.fail(f"Quota fixture không nên chờ: {args}"))
                result = runner.seal_phase()
                self.assertEqual(result["forecast_slots"], 8)
                self.assertEqual(result["hosted_attempts"], fixture.attempts)
                self.assertEqual(result["tokens_measured"], 120)
                self.assertEqual(result["outcomes_opened"], 0)
                cold = Fixture(forbid_send=True)
                verifier = HostedStudyRunner(root, grant, budget, cohort, "SMOKE", provider, archive,
                                             cold.transport, cold.clock)
                self.assertEqual(verifier.seal_phase(), result)
                self.assertEqual(cold.attempts, 0)


if __name__ == "__main__":
    unittest.main()
