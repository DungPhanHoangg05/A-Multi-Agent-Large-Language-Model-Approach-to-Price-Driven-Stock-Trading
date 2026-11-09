"""Future poisoning/prefix extension trên đủ 85 alpha và holdout selector đóng băng."""
from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import numpy as np
import pandas as pd

from core.causal_alpha import FrozenSelector, alpha_values, fit_selector, features, handlers
from core.causal_alpha import frame_document
from core.causal_bridge import CausalSources
from core.unified_contracts import json_bytes
from core.unified_methods import snapshot_from_graph
from core.revision_alpha_contract import rowwise_diagnostics
from causal_profile_support import causal_fixture, prepared_bundle, schedule, source_frame


class CausalCommonLeakageTests(unittest.TestCase):
    """Không nhận local alpha PASS thành Zero-Leakage cho toàn HMM/retrieval/news/model."""
    def test_all_raw_handlers_are_prefix_invariant_before_warmup(self) -> None:
        frame = source_frame().iloc[:700]
        short, complete = features(frame.iloc[:120]), features(frame)
        for identifier, handler in handlers().items():
            with self.subTest(identifier=identifier):
                np.testing.assert_allclose(handler(short).to_numpy(), handler(complete).iloc[:120].to_numpy(),
                                           rtol=1e-11, atol=1e-12, equal_nan=True)

    def test_all_85_factors_are_prefix_invariant_at_multiple_boundaries(self) -> None:
        frame = source_frame().iloc[:1100]
        complete = alpha_values(frame)
        self.assertEqual(complete.shape[1], 85)
        for end in (380, 600, 900):
            with self.subTest(end=end):
                short = alpha_values(frame.iloc[:end])
                np.testing.assert_allclose(short.to_numpy(), complete.iloc[:end].to_numpy(), rtol=1e-11, atol=1e-12, equal_nan=True)
                self.assertGreater(int(np.isfinite(short.to_numpy()).sum()), 0)

    def test_future_ohlcv_volume_missing_poison_cannot_rewrite_past_factors(self) -> None:
        frame = source_frame().iloc[:1100]
        poisoned = frame.copy()
        poisoned.loc[600:, ["Open", "High", "Low", "Close"]] *= 100.
        poisoned.loc[600:, "Volume"] = np.nan
        before, after = alpha_values(frame), alpha_values(poisoned)
        np.testing.assert_allclose(before.iloc[:600], after.iloc[:600], rtol=1e-11, atol=1e-12, equal_nan=True)

    def test_arbitrary_test_prices_do_not_enter_fit_or_orientation(self) -> None:
        frame = source_frame(); plan = schedule(frame)
        poisoned = frame.copy()
        poisoned.loc[1001:, ["Open", "High", "Low", "Close", "Volume"]] = np.nan
        self.assertEqual(fit_selector(frame, plan), fit_selector(poisoned, plan))

    def test_validation_poison_cannot_change_train_orientation(self) -> None:
        frame = source_frame(); plan = schedule(frame)
        before = fit_selector(frame, plan)
        poisoned = frame.copy()
        poisoned.loc[751:1000, ["Open", "High", "Low", "Close"]] *= 1.2
        after = fit_selector(poisoned, plan)
        self.assertEqual(before["payload"]["candidates"], after["payload"]["candidates"])
        self.assertNotEqual(before["payload"]["fit_price_sha256"], after["payload"]["fit_price_sha256"])

    def test_prediction_refuses_future_rows_changed_train_origin_and_missing_query(self) -> None:
        frame = source_frame(); selector = FrozenSelector(fit_selector(frame, schedule(frame)), frame)
        cutoff = str(frame.Datetime.iloc[1100].date())
        for wrong in (frame.iloc[:1102], frame.iloc[1:1101], frame.iloc[:1100]):
            with self.assertRaises(ValueError): selector.predict(wrong, cutoff)
        changed = frame.iloc[:1101].copy()
        changed.loc[500, "Volume"] *= 2
        with self.assertRaises(ValueError): selector.predict(changed, cutoff)
        changed = frame.iloc[:1101].copy(); changed.loc[1100, "Volume"] = np.nan
        with self.assertRaises(ValueError): selector.predict(changed, cutoff)

    def test_native_counterexamples_still_fail_and_are_not_relabelled(self) -> None:
        result = rowwise_diagnostics()
        self.assertEqual(result["diagnostic_result"], "PASS_DETECTION")
        self.assertEqual(result["native_rowwise_causal_gate"], "FAIL")

    def test_every_branch_request_ignores_future_prices_and_full_file_hash_changes(self) -> None:
        with TemporaryDirectory() as directory:
            fx, before, _ = causal_fixture(Path(directory))
            old_shared = next(iter(before["snapshots"].values()))
            changed = fx.frame.copy()
            changed.loc[1297:, ["Open", "High", "Low", "Close"]] *= 17
            changed.loc[1299, "Close"] *= 1.2
            changed.loc[1299, "High"] = max(changed.loc[1299, "Open"], changed.loc[1299, "Close"]) + 1.
            fx.frame = changed
            path = fx.root / "causal-prices.json"; path.write_bytes(json_bytes(frame_document(changed)))
            fx.source_sha = hashlib.sha256(path.read_bytes()).hexdigest()
            fx.spec["source_hashes"]["causal-prices.json"] = fx.source_sha
            prefix = changed.loc[changed.Datetime <= pd.Timestamp(fx.point["cutoff"])].tail(600)
            fx.snapshot = snapshot_from_graph(fx.point, 0, fx.payload, prefix, fx.source_sha, [])
            bound = CausalSources(fx.spec, fx.root).bind(fx.snapshot)
            after = prepared_bundle(fx, bound)
            self.assertNotEqual(old_shared["provenance"], bound.document()["provenance"])
            self.assertNotEqual(before["outcomes"][fx.point["id"]]["target"], after["outcomes"][fx.point["id"]]["target"])
            for slot in before["preparations"]:
                with self.subTest(slot=slot):
                    self.assertEqual(before["preparations"][slot]["request"], after["preparations"][slot]["request"])


if __name__ == "__main__":
    unittest.main()
