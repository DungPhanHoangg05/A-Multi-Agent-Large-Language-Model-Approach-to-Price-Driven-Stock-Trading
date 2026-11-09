"""Oracle toán tử, selection train/validation và bridge vào runner chung."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from core import alpha_compare as native
from core.causal_alpha import FrozenSelector, alpha_values, delay, features, fit_selector, handlers, normalize
from core.causal_bridge import CausalSources, bind_snapshot, decision_payload
from core.unified_contracts import ExperimentSpec, SharedSnapshot, digest, json_bytes
from core.unified_experiment import verify_run
from core.unified_methods import MethodAdapters
from causal_profile_support import causal_fixture, schedule, source_frame

ROOT = Path(__file__).resolve().parents[1]


class CausalCommonProfileTests(unittest.TestCase):
    """Chỉ fixture tổng hợp; test kết quả âm/missing và fail-closed thay vì dùng native fallback."""
    def test_normalizer_and_delay_match_independent_prefix_oracles(self) -> None:
        values = pd.Series(np.arange(1., 26.))
        normalized = normalize(values)
        self.assertTrue(normalized.iloc[:19].isna().all())
        expected = np.tanh((20. - np.mean(np.arange(1., 21.))) / np.std(np.arange(1., 21.), ddof=1))
        self.assertAlmostEqual(float(normalized.iloc[19]), float(expected), places=14)
        self.assertTrue(np.isnan(delay(pd.Series([2., 3., 4.])).iloc[0]))
        self.assertEqual(delay(pd.Series([2., 3., 4.])).iloc[1], 2.)
        with self.assertRaises(ValueError): delay(values, -1)
        with self.assertRaises(ValueError): normalize(values, "rank")

    def test_real_volume_missing_and_zero_do_not_become_price_proxy_or_bfill(self) -> None:
        frame = source_frame().iloc[:10].copy()
        frame["Volume"] = [np.nan]*4 + [0., 100., 200., 300., 400., 500.]
        result = features(frame)
        self.assertTrue(result.volume.iloc[:4].isna().all())
        self.assertEqual(result.volume.iloc[4], 0.)
        self.assertTrue(result.log_vol.iloc[:5].isna().all())
        self.assertEqual(result.log_vol.iloc[5], np.log(100.))
        self.assertEqual(result._has_vol.tolist(), [False]*4 + [True]*6)

    def test_formula_namespace_is_isolated_and_wq54_matches_algebra(self) -> None:
        before = native.delay
        identifier = next(key for key, (fn, _) in native.ALPHA_REGISTRY.items() if fn.__name__ == "wq54")
        frame = source_frame().iloc[:100]
        raw = handlers()[identifier](features(frame))
        row = frame.iloc[-1]
        expected = -(row.Low-row.Close)*row.Open**2 / ((row.Low-row.High)*row.Close**2)
        self.assertAlmostEqual(float(raw.iloc[-1]), float(expected), places=13)
        self.assertEqual(len(handlers()), 85)
        self.assertIs(native.delay, before)
        self.assertIsNot(handlers()[identifier].__globals__, native.wq54.__globals__)
        self.assertEqual(native.delay(pd.Series([2., 3., 4.])).iloc[0], 2.)

    def test_selector_uses_canonical_oracle_purges_exit_equal_boundary_and_freezes_five(self) -> None:
        from core.backtest_engine import compute_round_trip_net_return
        frame = source_frame(); plan = schedule(frame)
        with patch("core.backtest_engine.compute_round_trip_net_return", wraps=compute_round_trip_net_return) as oracle:
            artifact = fit_selector(frame, plan)
        self.assertEqual(oracle.call_count, 998)
        payload = artifact["payload"]
        self.assertEqual(len(payload["selected"]), 5)
        self.assertTrue(payload["purged"]["train"])
        self.assertTrue(payload["purged"]["validation"])
        dates = frame.Datetime.dt.strftime("%Y-%m-%d").tolist()
        for split, boundary in (("train", "validation_start"), ("validation", "test_start")):
            for cutoff in payload[split+"_dates"]:
                self.assertLess(dates[dates.index(cutoff) + 3], plan[boundary])
        for selected in payload["selected"]:
            ic = payload["candidates"][selected["alpha_id"]]["train_ic"]
            self.assertEqual(selected["orientation"], 1 if ic >= 0 else -1)
        prediction = FrozenSelector(artifact, frame).predict(frame.iloc[:1101], dates[1100])
        self.assertEqual([r["alpha_id"] for r in prediction["factors"]], [r["alpha_id"] for r in payload["selected"]])
        self.assertNotIn("net_return", prediction)

    def test_resigned_artifact_or_missing_support_cannot_trigger_native_fallback(self) -> None:
        frame = source_frame(); artifact = fit_selector(frame, schedule(frame))
        for malformed in (None, [], {"payload": "bad", "sha256": digest("bad")}):
            with self.assertRaises(ValueError): FrozenSelector(malformed, frame)
        changed = deepcopy(artifact); changed["payload"]["selected"][0]["orientation"] *= -1
        changed["sha256"] = digest(changed["payload"])
        with self.assertRaises(ValueError): FrozenSelector(changed, frame)
        short = frame.iloc[:400]
        with self.assertRaises(ValueError): fit_selector(short, schedule(frame))
        constant = frame.copy()
        constant.loc[:, ["Open", "Close"]] = 100.
        constant["High"], constant["Low"], constant["Volume"] = 101., 99., 1000.
        with self.assertRaises(ValueError): fit_selector(constant, schedule(frame))

    def test_predict_cache_is_immutable_and_does_not_prepare_alpha_twice(self) -> None:
        frame = source_frame(); artifact = fit_selector(frame, schedule(frame)); selector = FrozenSelector(artifact, frame)
        cutoff = str(frame.Datetime.iloc[1100].date())
        with patch("core.causal_alpha.alpha_values", wraps=alpha_values) as computation:
            first = selector.predict(frame.iloc[:1101], cutoff)
            first["factors"][0]["value"] = 999.
            second = selector.predict(frame.iloc[:1101], cutoff)
            self.assertEqual(computation.call_count, 1)
            self.assertLessEqual(abs(second["factors"][0]["value"]), 1.)

    def test_all_common_branches_share_projection_and_native_request_is_unchanged(self) -> None:
        with TemporaryDirectory() as directory:
            fx, bundle, artifact = causal_fixture(Path(directory))
            bound = CausalSources(fx.spec, fx.root).bind(fx.snapshot)
            methods = MethodAdapters(fx.spec["decision"])
            self.assertEqual(methods.prepare("original_fix", fx.snapshot, {}, 0), methods.prepare("original_fix", bound, {}, 0))
            expected = decision_payload(bound, "original_common")
            for variant in ("bayesian_v1", "C2", "A_tp_pool", "B_semantic", "Fact_Anchor", "MT_BICL"):
                self.assertEqual(decision_payload(bound, variant), expected)
            self.assertNotEqual(expected["alpha_report"], fx.snapshot.document()["payload"]["alpha_report"])
            for name in ("indicator_report", "pattern_report", "trend_report", "sentiment_report", "price_prefix"):
                self.assertEqual(expected[name], fx.snapshot.document()["payload"][name])
            ids = [row["alpha_id"] for row in artifact["payload"]["selected"]]
            for slot, prepared in bundle["preparations"].items():
                if not slot.endswith("/original_fix") and prepared["request"] is not None:
                    prompt = prepared["request"]["messages"][0]["content"]
                    self.assertLess(len(prompt), 6500)
                    self.assertTrue(all(key in prompt for key in ids))
            counts = {}; result = fx.run(bundle, counts)
            self.assertEqual(counts["upstream"], 1)
            self.assertEqual(result["complete_slots"], 8)
            self.assertEqual(result["input_profile"], "causal_common_v1")
            self.assertEqual(result["native_rowwise_causal_gate"], "FAIL")
            for row in result["rows"]:
                self.assertEqual(row["input_profile"], "native_fix" if row["variant"] == "original_fix" else "causal_common_v1")
            self.assertEqual(result, verify_run(fx.root / fx.spec["namespace"], root=fx.root))

    def test_v2_spec_and_bridge_refuse_unbound_sources_or_resigned_projection(self) -> None:
        with TemporaryDirectory() as directory:
            fx, _, _ = causal_fixture(Path(directory))
            wrong = deepcopy(fx.spec); wrong["causal_sources"] = {}
            with self.assertRaises(ValueError): ExperimentSpec.create(wrong)
            source = CausalSources(fx.spec, fx.root); bound = source.bind(fx.snapshot)
            doc = bound.document(); projection = doc["payload"]["causal_alpha"]["projection"]
            projection["factors"][0]["value"] *= -1
            projection["projection_sha256"] = digest({k: v for k, v in projection.items() if k != "projection_sha256"})
            forged = SharedSnapshot.create(doc["point"], 0, doc["payload"], doc["provenance"])
            with self.assertRaises(ValueError): source.bind(forged)

    def test_cli_fit_verify_predict_bridge_are_offline_and_never_overwrite(self) -> None:
        with TemporaryDirectory() as directory:
            fx, bundle, artifact = causal_fixture(Path(directory))
            for name, value in (("schedule.json", artifact["payload"]["schedule"]), ("native.json", fx.snapshot.document()), ("decision.json", fx.spec["decision"])):
                (fx.root / name).write_bytes(json_bytes(value))
            cli = [sys.executable, "-I", "-X", "utf8", str(ROOT / "scripts/manage_causal_profile.py")]
            common = ["--prices", str(fx.root / "causal-prices.json")]
            subprocess.run([*cli, "fit", *common, "--schedule", str(fx.root / "schedule.json"), "--output", str(fx.root / "fit.json")], capture_output=True, check=True)
            self.assertEqual(json.loads((fx.root / "fit.json").read_bytes()), artifact)
            subprocess.run([*cli, "verify", *common, "--selector", str(fx.root / "fit.json")], capture_output=True, check=True)
            subprocess.run([*cli, "predict", *common, "--selector", str(fx.root / "fit.json"),
                "--cutoff", fx.point["cutoff"], "--output", str(fx.root / "prediction.json")], capture_output=True, check=True)
            self.assertEqual(json.loads((fx.root / "prediction.json").read_bytes())["version"], "causal_common_v1")
            args = [*cli, "bridge", *common, "--selector", str(fx.root / "fit.json"), "--snapshot", str(fx.root / "native.json"),
                    "--decision", str(fx.root / "decision.json"), "--output", str(fx.root / "bridge.json")]
            subprocess.run(args, capture_output=True, check=True)
            self.assertTrue(json.loads((fx.root / "bridge.json").read_bytes())["native_request_unchanged"])
            self.assertEqual(subprocess.run(args, capture_output=True).returncode, 2)


if __name__ == "__main__":
    unittest.main()
