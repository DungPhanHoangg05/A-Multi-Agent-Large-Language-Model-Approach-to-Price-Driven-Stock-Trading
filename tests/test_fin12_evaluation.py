"""Hồi quy mẫu số và oracle sổ tài khoản FIN12."""
from __future__ import annotations

from copy import deepcopy
import unittest

import pandas as pd

from core.backtest_engine import compute_round_trip_net_return
from core.free_pilot_statistics import account
from core.unified_analysis.statistics import FOLDS, METHODS
from scripts.fin12_evaluation import UNAVAILABLE, account_tables, complete_grid
from scripts.fin12_evaluation_oracle import check_account


class Fin12EvaluationTests(unittest.TestCase):
    def test_mask_discards_both_cycles_of_incomplete_account(self) -> None:
        points, rows = [], []
        for index, fold in enumerate(FOLDS):
            for symbol in range(1 if index < 3 else 0, 9):
                for cycle in range(2):
                    identifier = f"{fold}/{symbol}/{cycle}"
                    points.append({"id": identifier, "fold": fold, "symbol": str(symbol),
                                   "cutoff": f"2026-01-0{cycle+1}"})
                    rows.extend({"point_id": identifier, "repeat": repeat, "method": method, "final_action": "LONG",
                                 "r_net": None if (index, symbol, cycle) == (0, 1, 0) else -.007}
                                for repeat in range(3) for method in METHODS)
        _, _, support, _ = complete_grid(rows, points)
        self.assertEqual(int(support.sum()), 100)
        self.assertEqual(support[0, 1].tolist(), [False, False])
        self.assertEqual(support[0, 2].tolist(), [True, True])
        with self.assertRaises(ValueError):
            complete_grid(rows[:-1], points)

    def test_account_na_preserves_reason_and_has_no_synthetic_nav(self) -> None:
        rows = [{"method": "original_fix", "symbol": "FPT", "fold": FOLDS[0], "repeat": 0,
                 "point_id": point, "r_net": net, "outcome_unavailable_reason": reason, "final_action": "CASH"}
                for point, net, reason in (("valid", -.02, None), ("unavailable", None, "CORPORATE_ACTION_DURING_HOLDING"))]
        accounts, cycles, nav = account_tables(rows, {})
        self.assertEqual(accounts[0]["status"], UNAVAILABLE)
        self.assertIsNone(accounts[0]["return_pct"])
        self.assertEqual(accounts[0]["missing_points"], {"unavailable": "CORPORATE_ACTION_DURING_HOLDING"})
        self.assertEqual((cycles, nav), ([], []))

    def test_oracle_rejects_tampered_mark_to_market(self) -> None:
        frame = pd.DataFrame({"Datetime": pd.date_range("2026-01-01", periods=8),
                              "Open": [10.]*8, "Close": [10., 11., 8., 9., 9., 9., 9., 9.]})
        rows = [{"date": date, "entry_date": entry, "exit_date": exit_, "action": action,
                 "r_net": compute_round_trip_net_return(10., 9.)}
                for date, entry, exit_, action in (("2026-01-01", "2026-01-02", "2026-01-04", "LONG"),
                                                   ("2026-01-05", "2026-01-06", "2026-01-08", "CASH"))]
        ledger = account(rows, frame)
        self.assertLess(ledger["return_pct"], 0.)
        check_account(rows, frame, ledger)
        modified = deepcopy(ledger)
        modified["daily_nav_vnd"][2] += 2
        with self.assertRaises(ValueError):
            check_account(rows, frame, modified)
