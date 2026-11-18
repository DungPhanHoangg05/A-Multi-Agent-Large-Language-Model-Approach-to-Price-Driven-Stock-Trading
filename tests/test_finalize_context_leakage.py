"""Rào causal ở provider thật FIN07, dùng fixture phản hồi tách khỏi forecast thị trường."""
from copy import copy, deepcopy
from pathlib import Path
import unittest

import pandas as pd
import torch

from core.causal_bridge import decision_payload
from core.finalize_context import FinalizedProviders
from core.finalize_ohlcv_keys import key_at, PATTERN, TREND
from core.finalize_prior import VARIANTS, statistics
from core.unified_contracts import SharedSnapshot
from scripts.check_finalize_context import raw_counts, verify_prior

ROOT = Path(__file__).resolve().parents[1]


class FinalizedContextLeakageTests(unittest.TestCase):
    """Kiểm những regression riêng của profile FIN07 trên nguồn giá thật đã khóa."""
    @classmethod
    def setUpClass(cls) -> None:
        torch.set_num_threads(1)
        cls.provider = FinalizedProviders(ROOT)
        cls.point = cls.provider.points["FPT-2023-07-03"]

    def test_vision_changes_prompt_without_changing_retrieval(self) -> None:
        p, point = self.provider, self.point
        bullish = decision_payload(p.control_snapshot(point, vision="BULLISH"), "bayesian_v1")
        bearish = decision_payload(p.control_snapshot(point, vision="BEARISH"), "bayesian_v1")
        for name in VARIANTS:
            with self.subTest(name=name):
                first, proof = p.prior.request(name, bullish, point["regime"])
                second, other = p.prior.request(name, bearish, point["regime"])
                self.assertEqual(proof, other)
                self.assertNotEqual(first["messages"], second["messages"])

    def test_future_price_poison_leaves_context_student_and_request_identical(self) -> None:
        p, point = self.provider, self.point
        symbol, cutoff, fold = (point[k] for k in ("symbol", "cutoff", "fold"))
        baseline_snapshot = p.control_snapshot(point)
        baseline_episode = p.context.build(symbol, cutoff)
        baseline_branch = p.context.variants(baseline_episode)["branches"]["MT_BICL"]
        adapter, _ = p.adapters(point["id"])
        baseline_request = adapter.prepare("original_common", baseline_snapshot, {}, 0)
        previous_frame = p.frames[symbol]
        previous_fold = p.context._ready.pop(fold)
        changed = previous_frame.copy(deep=True)
        changed.loc[changed.Datetime > pd.Timestamp(cutoff), ["Open", "High", "Low", "Close", "Volume", "Reference"]] = float("inf")
        p.frames[symbol] = changed
        try:
            poisoned_snapshot = p.control_snapshot(point)
            self.assertEqual(poisoned_snapshot.sha256, baseline_snapshot.sha256)
            poisoned_episode = p.context.build(symbol, cutoff)
            self.assertEqual(poisoned_episode, baseline_episode)
            self.assertEqual(p.context.variants(poisoned_episode)["branches"]["MT_BICL"], baseline_branch)
            self.assertEqual(adapter.prepare("original_common", poisoned_snapshot, {}, 0), baseline_request)
            doc = poisoned_snapshot.document()
            doc["payload"]["sentiment_data"]["unexpected"] = {"outcome": {"y": 1}}
            with self.assertRaises(ValueError):
                SharedSnapshot.create(doc["point"], doc["realization"], doc["payload"], doc["provenance"])
        finally:
            p.frames[symbol] = previous_frame
            p.context._ready[fold] = previous_fold

    def test_exit_equal_cutoff_never_touches_history_label(self) -> None:
        class Unreadable(dict):
            def __getitem__(self, key: str):
                if key in ("y", "r_net"):
                    raise AssertionError("Đã đọc nhãn cycle chưa mature")
                return super().__getitem__(key)

        p, point = self.provider, self.point
        prior = copy(p.prior)
        shared = decision_payload(p.control_snapshot(point), "bayesian_v1")
        fixture = Unreadable(deepcopy(next(r for r in p.rows if r["symbol"] == "FPT")))
        fixture.update(episode_id="FPT:TEST_RESERVED", exit_date=point["cutoff"], regime=point["regime"])
        for variant in VARIANTS:
            prior.rows = p.rows
            first = prior.request(variant, shared, point["regime"])
            prior.rows = p.rows + [fixture]
            self.assertEqual(first, prior.request(variant, shared, point["regime"]))

    def test_rejects_previous_repeat_and_tampered_cold_preparation(self) -> None:
        p, point = self.provider, self.point
        snapshot = p.control_snapshot(point)
        adapter, _ = p.adapters(point["id"])
        common = {"forecast": {"variant": "original_common", "point_id": point["id"], "repeat": 0,
                               "realization": 0, "shared_sha256": snapshot.sha256}}
        deps = {"original_common": common}
        with self.assertRaisesRegex(ValueError, "repeat"):
            adapter.prepare("Fact_Anchor", snapshot, deps, 1)
        common["forecast"]["repeat"] = 1
        prepared = adapter.prepare("bayesian_v1", snapshot, deps, 1)
        adapter.validate("bayesian_v1", snapshot, deps, 1, prepared)
        prepared["trace"]["counts"]["win_rate_long"]["denominator"] = -1
        with self.assertRaisesRegex(ValueError, "khác nguồn"):
            adapter.validate("bayesian_v1", snapshot, deps, 1, prepared)

    def test_c2_a_b_examples_are_visible_when_price_and_signal_support_qualify(self) -> None:
        p = self.provider
        point = self.point
        symbol, cutoff = point["symbol"], point["cutoff"]
        regime = "BULL"
        prior = copy(p.prior)
        features = {r["episode_id"]: r["features"] for r in prior.selector.index.payload["records"]}
        candidate = next(r for r in p.rows if r["symbol"] == symbol and r["regime"] == regime and r["exit_date"] < cutoff
                         and r["example_ready"] and features[r["episode_id"]]["status"] == "AVAILABLE"
                         and (pd.Timestamp(cutoff) - pd.Timestamp(r["as_of_date"])).days <= 730)
        shared = decision_payload(p.control_snapshot(point), "C2")
        _, observed = p.prior.request("C2", shared, point["regime"])
        self.assertIn("LOW_POPULATION_SUPPORT", observed["gate"]["examples_reason_codes"])
        # Fixture thay regime và vector bằng một ca đủ support. Cohort/khóa OHLCV đã phát hành giữ nguyên.
        directions = {"BULLISH": "TĂNG", "BEARISH": "GIẢM", "NEUTRAL": "TRUNG TÍNH"}
        for factor in shared["alpha_factors"]:
            factor["signal"] = directions[candidate["alpha_consensus"]]
        shared["indicator_report"] = "Dominant consensus: " + candidate["indicator_consensus"]
        scripted_feature = {**point["feature"], "vector": features[candidate["episode_id"]]["vector"]}
        controlled = {**point, "feature": scripted_feature, "regime": regime}
        prior.points = {point["id"]: controlled}
        for name in ("C2", "A_tp_pool", "B_semantic"):
            with self.subTest(name=name):
                _, proof = prior.request(name, shared, regime)
                self.assertTrue(proof["gate"]["examples_ready"])
                self.assertFalse(proof["fallback"])
                self.assertTrue(verify_prior(p, controlled, proof)["examples_selected"])
                self.assertTrue(all(key in proof["request"]["prefix"] for key in proof["selected_ids"]))

    def test_ohlcv_unavailable_bypasses_without_neutral_fill(self) -> None:
        p, point = self.provider, self.point
        prior = copy(p.prior)
        shared = decision_payload(p.control_snapshot(point), "bayesian_v1")
        shared["price_prefix"] = {k: vs[-44:] for k, vs in shared["price_prefix"].items()}
        frame = pd.DataFrame(shared["price_prefix"])
        frame.Datetime = pd.to_datetime(frame.Datetime)
        key = key_at(frame, p.calendar, point["cutoff"])
        prior.points = {point["id"]: {**point, "retrieval_key": key}}
        for variant in VARIANTS:
            _, proof = prior.request(variant, shared, point["regime"])
            self.assertEqual(proof["reason"], "QUERY_OHLCV_KEY_UNAVAILABLE")
            self.assertIsNone(proof["query_signals"][PATTERN])
            self.assertIsNone(proof["query_signals"][TREND])
            self.assertEqual(proof["request"]["prefix"], "")

    def test_zero_return_counts_as_loss_and_union_deduplicates(self) -> None:
        fixture = {}
        for i, (trend, pattern, net) in enumerate((("BULLISH", "BULLISH", 0.), ("NEUTRAL", "BULLISH", .1),
                                                    ("BULLISH", "NEUTRAL", -.1), ("BEARISH", "NEUTRAL", -.1))):
            fixture[str(i)] = {"retrieval_key": {TREND: trend, PATTERN: pattern}, "r_net": net, "y": int(net > 0)}
        counts = [(r["numerator"], r["denominator"]) for r in statistics(list(fixture.values())).values()]
        self.assertEqual(counts, [(1, 4), (2, 3), (2, 2), (1, 2)])
        self.assertEqual(counts, raw_counts(fixture, set(fixture)))


if __name__ == "__main__":
    unittest.main()
