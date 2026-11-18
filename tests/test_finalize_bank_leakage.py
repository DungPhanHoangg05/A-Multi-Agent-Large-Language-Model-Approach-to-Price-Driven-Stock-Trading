"""Kiểm reservation và selector giá thô trước ranh giới train/validation/query."""
from pathlib import Path
import unittest
from unittest.mock import patch

import numpy as np

from causal_profile_support import schedule, source_frame
from core.causal_alpha import fit_selector
from core.finalize_bank_resources import ASSETS, RECIPE, mature_cycles
from core.finalize_raw_selector import cycle_masks, fit_raw_selector
from core.unified_protocol import binding, read

ROOT = Path(__file__).resolve().parents[1]


class FinalizeBankLeakageTests(unittest.TestCase):
    """Kiểm tập fit và rào truy xuất mà không gọi model hoặc tính outcome query."""

    def test_reserved_duplicate_or_immature_cycles_fail_closed(self) -> None:
        row = {"symbol": "FPT", "as_of_date": "2022-12-26", "exit_date": "2022-12-29"}
        mature_cycles([row], set(), "2022-12-30")
        for rows, reserved, cutoff in (([row], {"FPT-2022-12-26"}, "2022-12-30"),
                                      ([row, row], set(), "2022-12-30"), ([row], set(), "2022-12-29")):
            with self.assertRaises(ValueError):
                mature_cycles(rows, reserved, cutoff)

    def test_rights_no_volume_and_reserved_removed_before_oracle(self) -> None:
        frame = source_frame()
        frame["Volume"] = frame.Volume.round()
        frame["Reference"] = frame.Close.shift().fillna(frame.Close.iloc[0])
        fit = schedule(frame)
        past = frame.loc[frame.Datetime < fit["test_start"]].copy()
        masks, _ = cycle_masks(past, [], fit, frozenset())
        rights, halted, reserved = np.flatnonzero(masks["train"])[:3]
        dates = frame.Datetime.dt.strftime("%Y-%m-%d")
        events = [{"exrightDate": dates.iloc[rights + 2]}]
        frame.loc[halted + 1, "Volume"] = 0
        past.loc[halted + 1, "Volume"] = 0
        reserved_dates = frozenset({dates.iloc[reserved]})
        masks, excluded = cycle_masks(past, events, fit, reserved_dates)
        originals = np.flatnonzero(masks["train"] | masks["validation"])
        expected = list(zip(frame.Open.iloc[originals + 1], frame.Close.iloc[originals + 3]))
        from core.backtest_engine import compute_round_trip_net_return
        with patch("core.finalize_raw_selector.compute_round_trip_net_return", wraps=compute_round_trip_net_return) as oracle:
            fit_raw_selector(frame, events, fit, reserved_dates)
        self.assertEqual([call.args for call in oracle.call_args_list], expected)
        self.assertEqual(excluded["train"]["rights"], [dates.iloc[rights]])
        self.assertEqual(excluded["train"]["no_volume"], [dates.iloc[halted]])
        self.assertEqual(excluded["train"]["reserved"], [dates.iloc[reserved]])

    def test_clean_selector_keeps_old_recipe_and_future_poison_cannot_move_fit(self) -> None:
        frame = source_frame()
        frame["Volume"] = frame.Volume.round()
        frame["Reference"] = frame.Close.shift().fillna(frame.Close.iloc[0])
        fit = schedule(frame)
        legacy = fit_selector(frame, fit)["payload"]
        raw = fit_raw_selector(frame, [], fit, frozenset())
        for field in ("selected", "threshold", "train_dates", "validation_dates", "fit_price_sha256", "candidates"):
            self.assertEqual(raw["payload"][field], legacy[field], field)
        frame.loc[frame.Datetime >= fit["test_start"], ["Open", "High", "Low", "Close", "Volume", "Reference"]] = np.nan
        self.assertEqual(raw, fit_raw_selector(frame, [{"exrightDate": fit["test_end"]}], fit, frozenset()))

    def test_frozen_manifests_keep_ood_separate_from_missing_signal_and_no_query_outcomes(self) -> None:
        manifest = read(ROOT, ASSETS + "manifest.json", True)
        self.assertEqual(binding(ROOT, RECIPE), manifest["recipe"])
        for pin in manifest["asset_bindings"]:
            self.assertEqual(pin, binding(ROOT, pin["path"]))
        self.assertEqual((manifest["bank_numeric_records"], manifest["signal_ready"], manifest["query_input_count"]), (852, 0, 102))
        self.assertFalse(manifest["FIN06_complete"])
        self.assertFalse(manifest["query_outcomes_computed"])
        query = read(ROOT, ASSETS + "query_inputs.json")
        reserved = set(read(ROOT, RECIPE, True)["reserved_ids"])
        self.assertEqual({row["id"] for row in query}, reserved)
        for row in query:
            self.assertTrue({"r_net", "y", "outcome", "entry_open", "exit_close"}.isdisjoint(row))
            self.assertLessEqual(row["regime"]["feature_end_date"], row["cutoff"])
            self.assertEqual(row["fallback_variant"], "original_common" if row["symbol"] in {"BHN", "CMG", "HVN", "MBB", "VJC"} else None)


if __name__ == "__main__":
    unittest.main()
