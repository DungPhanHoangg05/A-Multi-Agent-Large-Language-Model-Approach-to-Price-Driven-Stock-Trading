"""Hồi quy fit/load prefix sau2022, parity recipe và tiếp tục không ghi đè model cũ."""

from contextlib import redirect_stdout
import hashlib
import io
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits

from core.historical_evaluation_audit import prepare_regimes
from core.historical_evaluation_scope import AlgorithmScope
from core.historical_evaluation_runner import Regimes
from core.regime_detector import MarketRegimeDetector, TRAIN_END, training_data_hash
from test_regime_features import make_history

ROOT = Path(__file__).resolve().parents[1]


class HistoricalRegimePrefixTests(unittest.TestCase):
    """Chỉ fit fixture synthetic trong thư mục tạm; không chạy492 model production."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.scope = AlgorithmScope(ROOT)
        cls.extended = cls.scope.module("regime_detector").MarketRegimeDetector
        cls.archive = make_history(700, "2021-01-04")
        cls.legacy_prefix = cls.archive.iloc[:500].copy()
        cls.new_prefix = cls.archive.iloc[:650].copy()
        with threadpool_limits(limits=1):
            cls.legacy = MarketRegimeDetector().fit(cls.legacy_prefix)
            cls.extended_legacy = cls.extended().fit(cls.legacy_prefix)
            cls.new = cls.extended().fit(cls.new_prefix)

    def test_legacy_recipe_and_artifact_bytes_are_identical(self) -> None:
        self.assertEqual(TRAIN_END, pd.Timestamp("2022-12-31"))
        self.assertEqual(self.legacy.metadata, self.extended_legacy.metadata)
        with tempfile.TemporaryDirectory() as folder:
            old, adapted = Path(folder) / "old.json", Path(folder) / "adapted.json"
            self.legacy.save(old)
            self.extended_legacy.save(adapted)
            self.assertEqual(old.read_bytes(), adapted.read_bytes())
            self.assertEqual(self.extended.load(old).metadata, self.legacy.metadata)

    def test_post2022_roundtrip_keeps_original_guard_and_prefix_identity(self) -> None:
        cutoff = str(self.new_prefix.Datetime.iloc[-1].date())
        self.assertGreater(cutoff, "2022-12-31")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "new.json"
            self.new.save(path)
            loaded = self.extended.load(path, expected_training_hash=training_data_hash(self.new_prefix))
            self.assertEqual(loaded.metadata, self.new.metadata)
            with threadpool_limits(limits=1):
                self.assertEqual(loaded.classify_regime(self.new_prefix, cutoff), self.new.classify_regime(self.new_prefix, cutoff))
            with self.assertRaises(ValueError):
                MarketRegimeDetector().fit(self.new_prefix)
            with self.assertRaises(ValueError):
                MarketRegimeDetector.load(path)
            with self.assertRaises(ValueError):
                self.extended.load(path, expected_training_hash="0" * 64)
            with self.assertRaises(ValueError):
                loaded.fit(self.new_prefix)

    def test_future_data_and_model_after_cutoff_are_rejected(self) -> None:
        cutoff = str(self.new_prefix.Datetime.iloc[-1].date())
        poisoned = self.archive.copy()
        poisoned.loc[poisoned.Datetime > cutoff, "Close"] = np.inf
        with threadpool_limits(limits=1):
            self.assertEqual(self.new.get_market_regime(cutoff, poisoned), self.new.classify_regime(self.new_prefix, cutoff))
        with self.assertRaises(ValueError):
            self.new.classify_regime(poisoned, cutoff)
        with self.assertRaises(ValueError):
            self.new.get_market_regime(str(self.legacy_prefix.Datetime.iloc[-1].date()), self.archive)
        with self.assertRaises(ValueError):
            self.extended().fit(make_history(500, "2026-01-01"))

    def test_prefix_in_final_historical_year_is_supported(self) -> None:
        """Không chỉ qua2023: numerical fit/validation phải chấp nhận prefix trong2026."""
        prefix = make_history(650, "2024-01-02")
        with threadpool_limits(limits=1):
            detector = self.extended().fit(prefix)
        self.assertEqual(detector.metadata["train_end_date"], str(prefix.Datetime.iloc[-1].date()))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "2026.json"
            detector.save(path)
            self.assertEqual(self.extended.load(path).metadata, detector.metadata)

    def test_prepare_resume_reuses_legacy_and_never_fits_future_rows(self) -> None:
        old_day = str(self.legacy_prefix.Datetime.iloc[-1].date())
        new_day = str(self.new_prefix.Datetime.iloc[-1].date())
        poisoned = self.archive.copy()
        poisoned.loc[poisoned.Datetime > new_day, "Close"] = np.nan
        data = SimpleNamespace(scope=self.scope, history=poisoned,
                               inputs={"history": [{"date": old_day}, {"date": new_day}]})
        fits = []
        original_fit = self.extended.fit

        def counted_fit(detector: object, prefix: pd.DataFrame) -> object:
            """Ghi prefix thực tới numerical fit, không thay thuật toán HMM."""
            fits.append(str(prefix.Datetime.iloc[-1].date()))
            return original_fit(detector, prefix)

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            directory = root / "outputs/historical_reevaluation/h04_assets/legacy_regimes"
            old = directory / (old_day + ".json")
            self.legacy.save(old)
            old_sha = hashlib.sha256(old.read_bytes()).hexdigest()
            with patch("core.historical_evaluation_data.HistoricalData", return_value=data), \
                    patch.object(self.extended, "fit", new=counted_fit), redirect_stdout(io.StringIO()):
                self.assertEqual(prepare_regimes(root)["count"], 2)
                self.assertEqual(fits, [new_day])
                snapshots = {p.name: p.read_bytes() for p in directory.glob("*.json")}
                self.assertEqual(prepare_regimes(root)["count"], 2)
                self.assertEqual(fits, [new_day])
                self.assertEqual(snapshots, {p.name: p.read_bytes() for p in directory.glob("*.json")})
                data.history = data.history.copy()
                data.history.loc[0, "Close"] += 1
                with self.assertRaises(ValueError):
                    prepare_regimes(root)
            self.assertEqual(hashlib.sha256(old.read_bytes()).hexdigest(), old_sha)

    def test_runner_get_and_preflight_load_post2022_without_refitting(self) -> None:
        cutoff = str(self.new_prefix.Datetime.iloc[-1].date())
        data = SimpleNamespace(history=self.archive, inputs={"history": [{"date": cutoff}]})
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder)
            self.new.save(directory / (cutoff + ".json"))
            regimes = Regimes.__new__(Regimes)
            regimes.data, regimes.directory, regimes.fixture = data, directory, False
            regimes.historical_detector = self.extended
            with patch.object(self.extended, "fit", side_effect=AssertionError("Không refit khi nạp")), \
                    patch.object(MarketRegimeDetector, "load", side_effect=AssertionError("Sai loader historical")), \
                    threadpool_limits(limits=1):
                regimes.preflight()
                self.assertEqual(regimes.get(cutoff, historical=True), self.new.classify_regime(self.new_prefix, cutoff)["regime_name"])


if __name__ == "__main__":
    unittest.main()
