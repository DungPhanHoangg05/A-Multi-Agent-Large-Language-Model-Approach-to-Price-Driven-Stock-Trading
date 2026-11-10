"""Chống query-y/future leakage và kiểm namespace của assets U06 trên nguồn thật."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from core.unified_protocol import read, MANIFEST
from core.unified_preflight_assets import ASSETS, frames

ROOT = Path(__file__).resolve().parents[1]


class PreflightLeakageTests(unittest.TestCase):
    """Chỉ fit/forward local; không tạo client hoặc mở outcome cohort."""
    def test_poison_all_test_prices_leaves_real_selector_fit_unchanged(self) -> None:
        from core.causal_alpha import fit_selector
        alpha = read(ROOT, ASSETS + "/frozen_alpha_manifest.json")
        path = alpha["causal_sources"]["FPT/b2023_h2"]["selector"]
        artifact = read(ROOT, path)
        frame = frames(ROOT)["FPT"]
        poisoned = frame.copy()
        poisoned.loc[poisoned.Datetime >= artifact["payload"]["schedule"]["test_start"], ["Open", "High", "Low", "Close", "Volume"]] = np.nan
        self.assertEqual(fit_selector(poisoned, artifact["payload"]["schedule"]), artifact)

    def test_every_frozen_context_excludes_all_102_query_ids_before_labels(self) -> None:
        planned = {p["runner_point_id"] for p in read(ROOT, MANIFEST, True)["points"]}
        providers = read(ROOT, ASSETS + "/provider_manifest.json")
        for row in providers["points"]:
            episode = read(ROOT, row["path"])["context"]
            observations = [r for t in episode["prior"] for r in t["observations"]] + episode["target"]
            self.assertTrue(all(r["episode_id"] not in planned and r["exit_date"] < row["frozen_before"] for r in observations))
            self.assertNotIn("y", episode["query"])
            self.assertNotIn("outcome", episode["query"])

    def test_nine_symbol_schema_is_isolated_from_native_contract(self) -> None:
        from core.unified_asset_providers import StudyScope
        from core.mt_bicl_contracts import wire_schema, validate_fact_packet
        original = deepcopy(wire_schema())
        scope = StudyScope(ROOT)
        providers = read(ROOT, ASSETS + "/provider_manifest.json")
        row = next(r for r in providers["points"] if r["point_id"].startswith("BHN-"))
        packet = read(ROOT, row["path"])["context"]["advisor"]["query_facts"]
        scope.module("mt_bicl_contracts").validate_fact_packet(packet)
        with self.assertRaises(ValueError):
            validate_fact_packet(packet)
        self.assertEqual(wire_schema(), original)

    def test_real_frozen_context_never_fits_hmm_or_updates_after_first_query(self) -> None:
        from core.unified_asset_providers import study_data, FrozenStudyContext
        from core.regime_detector import MarketRegimeDetector
        data = study_data(ROOT)
        ids = {r["id"] for r in read(ROOT, MANIFEST, True)["points"]}
        data.by_day = {k: r for k, r in data.by_day.items() if r["id"] in ids}
        with patch.object(MarketRegimeDetector, "fit", side_effect=AssertionError("Không được fit HMM")):
            context = FrozenStudyContext(data, "2023-07-03")
            first = context.build("FPT", "2023-07-03")
            frozen_ids = [r["episode_id"] for r in context.view._records]
            context.build("FPT", "2023-09-22")
            self.assertEqual([r["episode_id"] for r in context.view._records], frozen_ids)
            self.assertFalse(set(frozen_ids).intersection(r["runner_point_id"] for r in read(ROOT, MANIFEST, True)["points"]))
            self.assertNotIn("y", first["query"])

    def test_schema_and_execution_compatibility_preserve_original_frozen_bytes(self) -> None:
        import hashlib
        import json
        audit = read(ROOT, "docs/plan/week2/memory_bank_audit.json")
        schema = ROOT / "docs/plan/week1/historical_task_record.schema.json"
        legacy = ROOT / ASSETS / "compatibility/docs/plan/week1/historical_task_record.schema.json"
        self.assertEqual(hashlib.sha256(legacy.read_bytes()).hexdigest(), audit["schema_sha256"])
        self.assertEqual(json.loads(schema.read_bytes()), json.loads(legacy.read_bytes()))
        self.assertNotEqual(schema.read_bytes(), legacy.read_bytes())
        manifest = read(ROOT, ASSETS + "/compatibility/execution_prices/manifest.json")
        for files in manifest["files"].values():
            for kind in ("csv", "events", "evidence"):
                path = ROOT / ASSETS / "compatibility/execution_prices" / files[kind]["file"]
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), files[kind]["sha256"])

    def test_legacy_h03_runtime_verifier_still_refuses_the_new_serving_tree(self) -> None:
        from core.historical_evaluation_data import HistoricalData
        with self.assertRaisesRegex(ValueError, "Nguồn khác H03"):
            HistoricalData(ROOT)

    def test_future_prices_and_events_cannot_change_real_scoped_features_or_facts(self) -> None:
        from core.unified_asset_providers import study_data
        data = study_data(ROOT)
        for symbol, cutoff in (("FPT", "2023-07-03"), ("BHN", "2025-10-01")):
            frame = data.frames[symbol]
            events = data.events[symbol]
            extractor = data.scope.features
            facts = data.scope.module("mt_bicl_features").make_fact_packet
            before_x = extractor(frame, events, data.calendar, cutoff, source=data.scope.source)
            before_facts = facts(frame, symbol, cutoff)
            poisoned = frame.copy()
            poisoned.loc[poisoned.Datetime > cutoff, ["Open", "High", "Low", "Close"]] *= 7.
            poisoned.loc[poisoned.Datetime > cutoff, "Volume"] = 0.
            late_events = [*events, {"exrightDate": "2026-09-30"}]
            self.assertEqual(extractor(poisoned, late_events, data.calendar, cutoff, source=data.scope.source), before_x)
            self.assertEqual(facts(poisoned, symbol, cutoff), before_facts)

    def test_reservation_blocks_oracle_before_computation_with_positive_control(self) -> None:
        from types import SimpleNamespace
        from core.unified_asset_providers import study_data
        from core.historical_evaluation_context import ContextBank
        data = study_data(ROOT)
        for i, symbol in enumerate(data.scope.symbols):
            frame = data._frames[symbol].copy()
            opens = 100000. * (i + 1) + np.arange(len(frame), dtype=float)
            frame.loc[:, ["Open", "High", "Low", "Close"]] = np.column_stack((opens, opens + 2, opens - 1, opens + .5))
            frame.loc[:, "Volume"] = 1e6
            data._frames[symbol] = frame
            data._events[symbol] = []
        index = 1220
        cutoff = str(data.calendar[index].date())
        exit_date = str(data.calendar[index + 3].date())
        data.by_day = {("FPT", cutoff): {"id": "SYNTHETIC_RESERVED_QUERY", "exit_date": exit_date}}
        frame = data._frames["FPT"]
        pos = frame.Datetime.tolist().index(pd.Timestamp(cutoff))
        forbidden = (float(frame.Open.iloc[pos + 1]), float(frame.Close.iloc[pos + 3]))
        module = data.scope.module("mt_bicl_stream")
        original = module.compute_round_trip_net_return
        calls = []
        def observed(entry: float, exit_close: float, **kwargs: object) -> float:
            calls.append((float(entry), float(exit_close)))
            return original(entry, exit_close, **kwargs)
        with patch.object(module, "compute_round_trip_net_return", side_effect=observed):
            context = ContextBank(data, lambda _: False, student=SimpleNamespace())
            context.stream.advance("2024-07-01")
            self.assertTrue(calls)
            self.assertNotIn(forbidden, calls)
            calls.clear()
            data.by_day = {}
            context.stream.advance("2024-07-01")
            self.assertIn(forbidden, calls)


if __name__ == "__main__":
    unittest.main()
