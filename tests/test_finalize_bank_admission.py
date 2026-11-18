"""Kiểm độ phủ bank và handoff batch sau khi chốt chính sách tín hiệu thiếu."""
from pathlib import Path
import unittest

from core.finalize_bank_admission import classify_signals, collection_plan
from core.unified_protocol import read

ROOT = Path(__file__).resolve().parents[1]


class BankAdmissionTests(unittest.TestCase):
    """Giữ mẫu số regime và không gán NA thành tín hiệu đã quan sát."""

    def test_missing_alpha_affects_examples_only(self) -> None:
        row = {"pattern": "BULLISH", "trend": "NEUTRAL", "indicator_consensus": "BULLISH",
               "alpha_consensus": None, "sentiment": None}
        self.assertEqual(classify_signals(row), (True, False))
        self.assertEqual(classify_signals(row | {"alpha_consensus": "NEUTRAL"}), (True, True))
        self.assertEqual(classify_signals(row | {"trend": None}), (False, False))
        with self.assertRaises(ValueError):
            classify_signals(row | {"sentiment": "NOT_AVAILABLE"})

    def test_frozen_queue_has_two_unique_label_blind_slots_for_every_episode(self) -> None:
        plan = collection_plan(ROOT)
        expected = read(ROOT, "docs/plan/week12/finalize_bank_collection_plan_v1.json", True)
        self.assertEqual(plan, expected)
        self.assertEqual(plan["planned_episodes"], 852)
        self.assertEqual(plan["alpha_available"], 733)
        self.assertEqual(plan["vision_slots_planned"], 1704)
        self.assertEqual(len({slot["id"] for slot in plan["slots"]}), 1704)
        self.assertEqual(plan["statistics_ready"], 0)
        self.assertEqual(plan["examples_ready"], 0)
        self.assertFalse(plan["bank_release"])
        self.assertTrue(all({"y", "r_net", "outcome", "exit_close"}.isdisjoint(slot) for slot in plan["slots"]))


if __name__ == "__main__":
    unittest.main()
