"""Rào query payoff tại oracle U08 và chống state poison trên cả chín mã."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests"))
from core.unified_live.manager import canonical_outcome
from core.unified_live.release import NAMESPACES
from core.unified_execution import StageBook
from core.unified_protocol import ordered_branches, read
from core.unified_contracts import SharedSnapshot
from core.unified_preflight import ASSETS
from core.backtest_engine import compute_round_trip_net_return


class LiveLeakageTests(unittest.TestCase):
    """Chỉ dùng giá synthetic cho target, không mở payoff thật trước thu forecast."""
    def setUp(self) -> None:
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.point = {"id": "FPT-2023-01-02", "symbol": "FPT", "cutoff": "2023-01-02", "fold": "synthetic", "quality": "SYNTHETIC"}
        self.run = {"phase": "RESEARCH", "mode": "HOSTED_TEST", "repeats": 3, "points": [self.point]}

    def fill(self, count: int) -> StageBook:
        """Hoàn tất slot synthetic để kiểm barrier, không giả là forecast hosted."""
        book = StageBook(self.root / NAMESPACES["RESEARCH"], self.run)
        slots = [f"forecast/{self.point['id']}/u0/r{r}/{v}" for r in range(3) for v in ordered_branches(r)]
        for slot in slots[:count]:
            book.execute(slot, {"synthetic": True}, lambda _: {"synthetic": True})
        return book

    def test_no_run_and23_forecasts_do_not_even_read_price_file(self) -> None:
        with self.assertRaisesRegex(ValueError, "khóa"):
            canonical_outcome(self.root, self.point)
        self.fill(23)
        with self.assertRaisesRegex(ValueError, "24 forecast"):
            canonical_outcome(self.root, self.point)

    def test_after24_slots_target_uses_vnd_once_and_economic_oracle(self) -> None:
        self.fill(24)
        directory = self.root / "outputs/unified_integration/u06_assets_v2/prices"
        directory.mkdir(parents=True)
        frame = {"Datetime": ["2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05"],
            "Open": [50., 51., 52., 53.], "High": [56.]*4, "Low": [49.]*4,
            "Close": [50., 52., 53., 55.], "Volume": [1000.]*4}
        (directory / "FPT.json").write_text(json.dumps(frame), encoding="utf-8")
        record = canonical_outcome(self.root, self.point)
        target = record["target"]
        self.assertEqual(target["entry_open"], 51000.)
        self.assertEqual(target["exit_close"], 55000.)
        self.assertAlmostEqual(target["net_return"], compute_round_trip_net_return(51000., 55000.))
        self.assertEqual(record["dates"][-1], "2023-01-05")

    def test_unplanned_query_stays_locked_even_when_other_point_done(self) -> None:
        self.fill(24)
        with self.assertRaises(ValueError): canonical_outcome(self.root, {**self.point, "fold": "other"})

    def test_each_symbol_snapshot_rejects_nested_query_y_and_future_bars(self) -> None:
        manifest = read(ROOT, ASSETS + "/provider_manifest.json")
        seen = set()
        for row in manifest["points"]:
            saved = read(ROOT, row["path"])["snapshot"]
            symbol = saved["point"]["symbol"]
            if symbol in seen:
                continue
            seen.add(symbol)
            poisoned = deepcopy(saved["payload"])
            poisoned["sentiment_data"]["injected"] = {"query_y": 1}
            with self.assertRaises(ValueError): SharedSnapshot.create(saved["point"], 0, poisoned, saved["provenance"])
            poisoned = deepcopy(saved["payload"])
            poisoned["price_prefix"]["Datetime"][-1] = "2099-01-01"
            with self.assertRaises(ValueError): SharedSnapshot.create(saved["point"], 0, poisoned, saved["provenance"])
        self.assertEqual(len(seen), 9)


if __name__ == "__main__":
    unittest.main()
