"""Kiểm amendment xác nhận nguồn không giả chứng cứ độc lập hoặc gỡ rào quyền."""
from copy import deepcopy
from pathlib import Path
import unittest
from unittest.mock import patch

from core.finalize_price_acceptance import PROFILE, accepted_prices, require_accepted_prices
from core.finalize_price_audit import require_price_gate

ROOT = Path(__file__).resolve().parents[1]


class PriceAcceptanceTests(unittest.TestCase):
    """Phân biệt acceptance của tác giả, PIT độc lập và eligibility nhãn."""

    @classmethod
    def setUpClass(cls) -> None:
        """Chạy audit một lần cho corpus đã pin, không truy cập mạng."""
        cls.record = accepted_prices(ROOT)

    def test_real_corpus_keeps_102_forecasts_and_five_rights_unavailable(self) -> None:
        record = self.record
        self.assertTrue(record["FIN04_complete"])
        self.assertEqual((record["planned_forecasts"], record["economic_eligible_points"],
                          record["economic_unavailable_points"]), (102, 97, 5))
        self.assertFalse(record["independent_price_pit_certified"])
        self.assertFalse(record["query_outcomes_computed"])
        self.assertFalse(record["resources_rebuilt"])
        self.assertTrue(all(p["forecast_planned"] and not p["admitted"] for p in record["points"]))
        self.assertEqual(len(record["query_sources"]), 9)

    def test_acceptance_is_explicit_and_rejects_resigned_changes(self) -> None:
        with self.assertRaises(ValueError):
            require_accepted_prices(ROOT, profile="independent_pit")
        for key, value in (("independent_price_pit_certified", True), ("economic_unavailable_points", 0),
                           ("owner_confirmation", {}), ("profile", "unversioned")):
            poisoned = deepcopy(self.record)
            poisoned[key] = value
            with patch("core.finalize_price_acceptance.read", return_value=poisoned), \
                 patch("core.finalize_price_acceptance.accepted_prices", return_value=self.record):
                with self.assertRaises(ValueError):
                    require_accepted_prices(ROOT, profile=PROFILE)

    def test_owner_acceptance_does_not_unlock_old_independent_gate(self) -> None:
        with patch("core.finalize_price_audit.audit_prices", return_value=self.record):
            with self.assertRaises((ValueError, KeyError)):
                require_price_gate(ROOT, self.record)

    def test_source_drift_stops_acceptance(self) -> None:
        with patch("core.finalize_price_acceptance.audit_prices", return_value={}):
            with self.assertRaises(ValueError):
                accepted_prices(ROOT)


if __name__ == "__main__":
    unittest.main()
