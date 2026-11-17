"""Kiểm biên warm-up, missing và selector đóng băng cho Alpha finalize."""
from __future__ import annotations

from copy import deepcopy
import unittest
from unittest.mock import patch

import numpy as np
from core.causal_alpha import CONFIG, FrozenSelector, alpha_values, features, fit_selector, handlers
from causal_profile_support import schedule, source_frame


class FinalizeAlphaLeakageTests(unittest.TestCase):
    """Phản ví dụ tổng hợp không dùng market outcome hoặc huấn luyện model mới."""

    def test_all_85_raw_handlers_preserve_short_prefixes_across_fixed_window_boundaries(self) -> None:
        frame = source_frame().iloc[:700]
        complete = features(frame)
        expected = {key: handler(complete) for key, handler in handlers().items()}
        self.assertEqual(len(expected), 85)
        for end in (1, 2, 19, 199, 200, 229, 230, 239, 240, 249, 250, 300):
            prefix = features(frame.iloc[:end])
            for key, handler in handlers().items():
                with self.subTest(end=end, alpha_id=key):
                    np.testing.assert_allclose(handler(prefix), expected[key].iloc[:end],
                                               rtol=1e-11, atol=1e-12, equal_nan=True)

    def test_warmup_and_missing_volume_have_exact_unavailable_masks_without_proxy(self) -> None:
        frame = source_frame().iloc[:1050]
        before = alpha_values(frame)
        self.assertTrue(before.iloc[:CONFIG["warmup"] + CONFIG["normalizer_min_periods"] - 2].isna().all().all())
        self.assertTrue(before.iloc[400:500].notna().any().all())
        changed = frame.copy()
        changed.loc[500, "Volume"] = np.nan
        after = alpha_values(changed)
        np.testing.assert_allclose(before.iloc[:500], after.iloc[:500], equal_nan=True)
        self.assertTrue(after.iloc[500:800].isna().all().all())
        self.assertTrue(after.iloc[900:].notna().any().all())
        absent = frame.copy()
        absent["Volume"] = np.nan
        self.assertTrue(alpha_values(absent).isna().all().all())

    def test_future_missing_or_zero_volume_cannot_switch_historical_volume_mode(self) -> None:
        frame = source_frame().iloc[:700]
        frame.loc[:34, "Volume"] = np.nan
        frame.loc[35:49, "Volume"] = 0.
        frame.loc[80:89, ["Open", "High", "Low", "Close"]] = 100.
        expected = alpha_values(frame.iloc[:420])
        for volume in (np.nan, 0., 1e12):
            changed = frame.copy()
            changed.loc[420:, "Volume"] = volume
            changed.loc[420:, ["Open", "High", "Low", "Close"]] *= 1000.
            with self.subTest(future_volume=volume):
                np.testing.assert_allclose(expected, alpha_values(changed).iloc[:420],
                                           rtol=1e-11, atol=1e-12, equal_nan=True)

    def test_prediction_never_refits_or_changes_selected_ids_orientation_and_threshold(self) -> None:
        frame = source_frame()
        artifact = fit_selector(frame, schedule(frame))
        saved = deepcopy(artifact)
        selector = FrozenSelector(artifact, frame)
        artifact["payload"]["selected"][0]["orientation"] *= -1
        with patch("core.causal_alpha.fit_selector", side_effect=AssertionError("Predict không được fit lại")):
            for end in (1050, 1200):
                prefix = frame.iloc[:end].copy()
                prefix.loc[1001:, ["Open", "High", "Low", "Close"]] *= 10.
                prediction = selector.predict(prefix, str(prefix.Datetime.iloc[-1].date()))
                self.assertEqual(prediction["selector_sha256"], saved["sha256"])
                self.assertEqual([(row["alpha_id"], row["orientation"]) for row in prediction["factors"]],
                                 [(row["alpha_id"], row["orientation"]) for row in saved["payload"]["selected"]])
                threshold = saved["payload"]["threshold"]
                for row in prediction["factors"]:
                    expected = "TĂNG" if row["value"] > threshold else "GIẢM" if row["value"] < -threshold else "TRUNG TÍNH"
                    self.assertEqual(row["signal"], expected)


if __name__ == "__main__":
    unittest.main()
