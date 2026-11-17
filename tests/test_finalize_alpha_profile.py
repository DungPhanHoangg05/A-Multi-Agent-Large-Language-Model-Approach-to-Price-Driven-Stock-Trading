"""Kiểm profile Native sửa qua bridge/CLI offline, giữ tương thích đường lịch sử."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import pandas as pd

from core.causal_alpha import PROFILE, FrozenSelector, frame_document
from core.causal_bridge import REPAIRED_NATIVE_PROFILE, bind_snapshot, decision_payload
from core.decision_profiles import NATIVE_PROFILE, validate_decision_profile
from core.unified_contracts import digest, json_bytes
from core.unified_methods import native_request, snapshot_from_graph
from causal_profile_support import causal_fixture

ROOT = Path(__file__).resolve().parents[1]


class FinalizeAlphaProfileTests(unittest.TestCase):
    """Đường sửa chỉ mở khi chọn profile; FIN08 sẽ nối ứng dụng và result identity."""

    @classmethod
    def setUpClass(cls) -> None:
        """Chuẩn bị một selector synthetic thật, dùng chung bản đọc giữa các test."""
        cls.directory = TemporaryDirectory()
        cls.addClassCleanup(cls.directory.cleanup)
        cls.fx, _, cls.artifact = causal_fixture(Path(cls.directory.name))
        cls.selector = FrozenSelector(cls.artifact, cls.fx.frame)
        cls.prefix = cls.fx.frame.loc[cls.fx.frame.Datetime <= pd.Timestamp(cls.fx.point["cutoff"])].copy()
        cls.bound = bind_snapshot(cls.fx.snapshot, cls.selector, cls.prefix, cls.fx.source_sha)

    def test_repaired_native_and_all_common_roles_share_alpha_without_mutating_snapshot(self) -> None:
        saved = self.bound.document()
        common = decision_payload(self.bound, "original_common")
        repaired = decision_payload(self.bound, "original_fix", decision_profile=REPAIRED_NATIVE_PROFILE)
        self.assertEqual(repaired, common)
        for variant in ("bayesian_v1", "C2", "A_tp_pool", "B_semantic", "Fact_Anchor", "MT_BICL"):
            self.assertEqual(decision_payload(self.bound, variant), repaired)
        self.assertEqual(decision_payload(self.bound, "original_fix"), decision_payload(self.fx.snapshot, "original_fix"))
        self.assertEqual(decision_payload(self.bound, "original_fix", decision_profile=NATIVE_PROFILE),
                         decision_payload(self.fx.snapshot, "original_fix"))
        repaired["alpha_factors"][0]["value"] = 999.
        self.assertEqual(self.bound.document(), saved)
        json_bytes(common)

    def test_repaired_profile_refuses_missing_projection_unknown_profile_and_wrong_method(self) -> None:
        for snapshot, variant, profile in (
            (self.fx.snapshot, "original_fix", REPAIRED_NATIVE_PROFILE),
            (self.bound, "original_fix", "unregistered_profile"),
            (self.bound, "original_common", REPAIRED_NATIVE_PROFILE),
            (self.bound, "MT_BICL", REPAIRED_NATIVE_PROFILE),
            (self.bound, "original_fix", 1),
        ):
            with self.subTest(variant=variant, profile=profile):
                with self.assertRaises(ValueError):
                    decision_payload(snapshot, variant, decision_profile=profile)
        with self.assertRaises(ValueError):
            validate_decision_profile(REPAIRED_NATIVE_PROFILE)

    def test_native_template_options_and_schema_are_preserved_without_running_native_selector(self) -> None:
        common = decision_payload(self.bound, "original_common")
        repaired = decision_payload(self.bound, "original_fix", decision_profile=REPAIRED_NATIVE_PROFILE)
        protocol = {"decision": self.fx.spec["decision"]}
        with patch("agents.alpha_agent._compute_all_alphas", side_effect=AssertionError("Không chạy selector native")):
            request = native_request(repaired, protocol, 0)
            self.assertEqual(request, native_request(common, protocol, 0))
        legacy = native_request(decision_payload(self.fx.snapshot, "original_fix"), protocol, 0)
        self.assertEqual({k:v for k,v in request.items() if k != "messages"},
                         {k:v for k,v in legacy.items() if k != "messages"})
        self.assertNotEqual(request["messages"], legacy["messages"])
        prompt = request["messages"][0]["content"]
        self.assertLess(len(prompt), 6500)
        self.assertTrue(all(row["alpha_id"] in prompt for row in repaired["alpha_factors"]))
        json_bytes(request)

    def test_future_price_and_source_hash_poison_leave_repaired_native_request_unchanged(self) -> None:
        changed = self.fx.frame.copy()
        changed.loc[changed.Datetime > pd.Timestamp(self.fx.point["cutoff"]), ["Open", "High", "Low", "Close"]] *= 100.
        source_sha = hashlib.sha256(json_bytes(frame_document(changed))).hexdigest()
        prefix = changed.loc[changed.Datetime <= pd.Timestamp(self.fx.point["cutoff"])]
        native = snapshot_from_graph(self.fx.point, 0, self.fx.payload, prefix.tail(600), source_sha, [])
        bound = bind_snapshot(native, self.selector, prefix, source_sha)
        protocol = {"decision": self.fx.spec["decision"]}
        before = native_request(decision_payload(self.bound, "original_fix", decision_profile=REPAIRED_NATIVE_PROFILE), protocol, 0)
        after = native_request(decision_payload(bound, "original_fix", decision_profile=REPAIRED_NATIVE_PROFILE), protocol, 0)
        self.assertNotEqual(self.bound.sha256, bound.sha256)
        self.assertEqual(before, after)

    def test_cli_explicit_repaired_profile_binds_identity_and_keeps_legacy_default(self) -> None:
        root = self.fx.root
        for name, value in (("native.json", self.fx.snapshot.document()), ("decision.json", self.fx.spec["decision"])):
            (root/name).write_bytes(json_bytes(value))
        command = [sys.executable, "-I", "-X", "utf8", str(ROOT/"scripts/manage_causal_profile.py"), "bridge",
            "--prices", str(root/"causal-prices.json"), "--selector", str(root/"causal-selector.json"),
            "--snapshot", str(root/"native.json"), "--decision", str(root/"decision.json")]
        repaired_path, legacy_path = root/"repaired.json", root/"legacy.json"
        subprocess.run([*command, "--native-profile", REPAIRED_NATIVE_PROFILE, "--output", str(repaired_path)],
                       capture_output=True, check=True)
        subprocess.run([*command, "--output", str(legacy_path)], capture_output=True, check=True)
        repaired, legacy = (json.loads(p.read_bytes()) for p in (repaired_path, legacy_path))
        self.assertEqual(repaired["native_profile"], REPAIRED_NATIVE_PROFILE)
        self.assertEqual(repaired["input_profile"], PROFILE)
        self.assertEqual(repaired["version"], "native_causal_bridge_v2")
        self.assertFalse(repaired["native_request_unchanged"])
        self.assertEqual(legacy["version"], "native_causal_bridge_v1")
        self.assertTrue(legacy["native_request_unchanged"])
        self.assertEqual(repaired["shared"], legacy["shared"])
        self.assertEqual(repaired["causal_common_request"], legacy["causal_common_request"])
        self.assertEqual(repaired["legacy_native_request_sha256"], digest(legacy["native_request"]))
        self.assertEqual(repaired["native_payload_sha256"], repaired["causal_payload_sha256"])
        self.assertEqual(repaired["hosted_calls"], 0)
        result = subprocess.run([*command, "--native-profile", "unknown", "--output", str(root/"bad.json")],capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertFalse((root/"bad.json").exists())


if __name__ == "__main__":
    unittest.main()
