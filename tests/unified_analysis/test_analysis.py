"""Oracle độc lập cho estimand, circular folds, joint band, support và đơn vị kinh tế."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from core.unified_analysis.statistics import (METHODS, VARIANTS, CONTRASTS, bands, effects, estimates, indices, plain)
from core.unified_analysis.inputs import check_files, decoded, validate_grid, frames, accept
from core.unified_analysis.analysis import classified
from core.unified_analysis.runtime import artifact_bindings
from core.unified_contracts import digest, json_bytes
from core.backtest_engine import compute_round_trip_net_return


class StatisticsTests(unittest.TestCase):
    """So vectorized estimators với hạch toán scalar trên vài draw có duplicate fold."""
    def setUp(self) -> None:
        self.rng = np.random.default_rng(92)
        self.a = self.rng.integers(0, 2, (6, 9, 2, 3, 10)).astype(bool)
        self.r = self.rng.uniform(-.06, .07, (6, 9, 2))
        self.mask = np.ones((6, 9, 2), bool); self.mask[:3, 0] = False

    def test_registered_rng_wrap_and_lengths(self) -> None:
        np.testing.assert_array_equal(indices()[:2], [[4, 5, 3, 4, 4, 5], [0, 1, 1, 2, 3, 4]])
        for length in (1, 2, 3):
            idx = indices(length); self.assertEqual(idx.shape, (10000, 6))
            blocks = idx.reshape(10000, 6//length, length)
            np.testing.assert_array_equal((blocks[..., 1:]-blocks[..., :-1]) % 6, np.ones_like(blocks[..., 1:]))
        with self.assertRaises(ValueError): indices(4)

    def test_vectorized_estimates_match_scalar_duplicate_account_oracle(self) -> None:
        draws = np.array([[0, 0, 0, 0, 0, 0], [5, 0, 1, 2, 3, 4], [4, 5, 3, 4, 4, 5]])
        returned, ba = estimates(self.a, self.r, self.mask, draws)
        for d, selected in enumerate(draws):
            for method in range(10):
                accounts, class_by_repeat = [], []
                for repeat in range(3):
                    truth, prediction = [], []
                    for fold in selected:
                        for symbol in range(9):
                            if not self.mask[fold, symbol, 0]: continue
                            capital = 1.
                            for cycle in range(2):
                                action = self.a[fold, symbol, cycle, repeat, method]
                                capital *= 1. + (self.r[fold, symbol, cycle] if action else 0.)
                                truth.append(self.r[fold, symbol, cycle] > 0); prediction.append(action)
                            accounts.append(capital-1.)
                    tp = sum(p and y for p, y in zip(prediction, truth)); tn = sum(not p and not y for p, y in zip(prediction, truth))
                    class_by_repeat.append(.5*(tp/sum(truth)+tn/(len(truth)-sum(truth)))*100.)
                self.assertAlmostEqual(returned[d, method], np.mean(accounts)*100., places=12)
                self.assertAlmostEqual(ba[d, method], np.mean(class_by_repeat), places=12)

    def test_missing_bhn_is_not_ninth_cash_account(self) -> None:
        self.a[:] = True; self.r[:] = .10
        ret, _ = estimates(self.a, self.r, self.mask, np.array([[0]*6]))
        self.assertAlmostEqual(ret[0, 0], 21.)

    def test_repeat_average_is_not_vote_or_cross_repeat_compound(self) -> None:
        self.a[:] = False; self.a[:, :, :, 0] = True; self.r[:] = .1
        ret, _ = estimates(self.a, self.r, self.mask)
        self.assertAlmostEqual(ret[0, 0], 7.)

    def test_account_folds_are_not_stitched(self) -> None:
        self.a[:] = True; self.r[:] = .1
        ret, _ = estimates(self.a, self.r, self.mask)
        self.assertAlmostEqual(ret[0, 0], 21.)
        self.assertNotAlmostEqual(ret[0, 0], (1.1**12-1)*100.)

    def test_zero_sd_invalidates_whole_twenty_column_family(self) -> None:
        d = self.rng.normal(size=(10000, 20)); d[:, 4] = 0.
        result = bands(np.zeros(20), d)
        self.assertIsNone(result["ci95"]); self.assertEqual(result["zero_sd_columns"], [4])
        self.assertIn("ZERO_SD_IN_JOINT_FAMILY", result["reasons"])

    def test_lost_draws_are_not_redrawn_and_minimum_is_exact(self) -> None:
        d = self.rng.normal(size=(10000, 20)); d[:501, 17] = np.nan
        result = bands(np.zeros(20), d)
        self.assertEqual(result["joint_finite_draws"], 9499); self.assertIsNone(result["ci95"])
        d[500, 17] = .2
        self.assertEqual(bands(np.zeros(20), d)["joint_finite_draws"], 9500)
        self.assertIsNotNone(bands(np.zeros(20), d)["ci95"])

    def test_higher_quantile_centered_at_registered_estimate_and_joint_sd(self) -> None:
        d = self.rng.normal(size=(10000, 20)); p = np.arange(20)*.1
        d[:100, 8] = np.nan
        result = bands(p, d); finite = d[100:]
        sd = np.array([float(np.std(finite[:, c], ddof=1)) for c in range(20)])
        maximum = [max(abs(row[c]-p[c])/sd[c] for c in range(20)) for row in finite]
        critical = sorted(maximum)[math.ceil(.95*(len(maximum)-1))]
        self.assertAlmostEqual(result["critical_value"], critical, places=12)
        np.testing.assert_allclose(result["ci95"], np.column_stack((p-critical*sd, p+critical*sd)), rtol=1e-14)

    def test_one_class_point_and_draws_keep_null(self) -> None:
        self.r[:] = -.02
        ret, ba = estimates(self.a, self.r, self.mask)
        self.assertTrue(np.isfinite(ret).all()); self.assertTrue(np.isnan(ba).all())
        result = bands(np.full(20, np.nan), self.rng.normal(size=(10000, 20)))
        self.assertIn("UNDEFINED_POINT_ESTIMATE", result["reasons"])
        self.assertEqual(result["point"], [None]*20)

    def test_twenty_effect_columns_keep_both_baselines_and_endpoints(self) -> None:
        returned = np.arange(10)[None, :].astype(float); ba = returned*2
        result = effects(returned, ba)
        self.assertEqual(result.shape, (1, 20))
        for column, (_, method, baseline) in enumerate(CONTRASTS):
            self.assertEqual(result[0, column], METHODS.index(method)-METHODS.index(baseline))
            self.assertEqual(result[0, 10+column], 2*result[0, column])

    def test_missing_half_account_nan_bad_shape_or_indices_raise(self) -> None:
        self.mask[0, 1, 0] = False
        with self.assertRaises(ValueError): estimates(self.a, self.r, self.mask)
        self.mask[0, 1, 0] = True; self.r[0, 1, 0] = np.nan
        with self.assertRaises(ValueError): estimates(self.a, self.r, self.mask)
        self.r[0, 1, 0] = .1
        with self.assertRaises(ValueError): estimates(self.a[..., :9], self.r, self.mask)
        with self.assertRaises(ValueError): estimates(self.a, self.r, self.mask, np.array([[6]]))

    def test_plain_has_no_numpy_or_nonfinite_json_leaks(self) -> None:
        result = plain({"count": np.int64(2), "flag": np.bool_(True), "values": np.array([1., np.nan])})
        self.assertEqual(result, {"count": 2, "flag": True, "values": [1., None]})
        json_bytes(result)


class ConsumerTests(unittest.TestCase):
    """Không nới support, checksum, đơn vị tiền hoặc rào snapshot để có summary."""
    def test_envelope_payload_tamper_rejected(self) -> None:
        value = {"a": 1}; raw = json_bytes({"payload": value, "sha256": digest(value)})
        self.assertEqual(decoded(raw), value)
        with self.assertRaises(ValueError): decoded(json_bytes({"payload": {"a": 2}, "sha256": digest(value)}))

    def test_binding_tamper_and_path_escape_rejected(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary); (root/'a').write_bytes(b"A")
            binding = {"a": {"bytes": 1, "sha256": hashlib.sha256(b"A").hexdigest()}}
            check_files(root, binding); (root/'a').write_bytes(b"B")
            with self.assertRaises(ValueError): check_files(root, binding)
            with self.assertRaises(ValueError): check_files(root, {"../outside": binding['a']})

    def test_bad_archive_rejected_before_any_provider(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary); path = root/'docs/plan/week12/unified_live_research.zip'
            path.parent.mkdir(parents=True); path.write_bytes(b"wrong")
            with patch('dotenv.dotenv_values', side_effect=AssertionError("Cấm key")), self.assertRaises(ValueError): accept(root)

    def grid(self) -> tuple:
        points = [{"id": f"p{i}"} for i in range(102)]
        records = [{"forecast": {"point_id": p["id"], "repeat": r, "variant": v, "realization": 0, "raw": None},
            "policy": {"final_action": "CASH"}} for p in points for r in range(3) for v in VARIANTS]
        return points, records, {p["id"]: {} for p in points}

    def test_grid_rejects_missing_duplicate_repeat_or_outcome(self) -> None:
        points, records, outcomes = self.grid(); validate_grid(points, records, outcomes)
        with self.assertRaises(ValueError): validate_grid(points, records[:-1], outcomes)
        with self.assertRaises(ValueError): validate_grid(points, records[:-1]+[records[0]], outcomes)
        with self.assertRaises(ValueError): validate_grid(points, records, {})

    def test_grid_rejects_reused_raw_and_invalid_action(self) -> None:
        points, records, outcomes = self.grid()
        records[0]['forecast']['raw'] = records[1]['forecast']['raw'] = {'source_request_id': 'same'}
        with self.assertRaises(ValueError): validate_grid(points, records, outcomes)
        records[1]['forecast']['raw'] = None; records[0]['policy']['final_action'] = 'SHORT'
        with self.assertRaises(ValueError): validate_grid(points, records, outcomes)

    def test_vnd_conversion_exactly_once_and_target_cannot_change(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary); path = root/'outputs/unified_integration/u06_assets_v2/prices/X.json'
            path.parent.mkdir(parents=True)
            dates = ['2026-01-05','2026-01-06','2026-01-07','2026-01-08']
            path.write_bytes(json_bytes({'Datetime': dates, 'Open': [50.]*4, 'Close': [50.,50.,51.,55.]}))
            bundle = {'points': [{'id': 'p','symbol': 'X','cutoff':dates[0]}], 'outcomes': {'p': {'dates': dates,
                'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                'target':{'entry_open':50000.,'exit_close':55000.,'net_return':float(compute_round_trip_net_return(50000.,55000.))}}}}
            self.assertEqual(float(frames(root,bundle)['X']['Open'].iloc[1]),50.)
            bundle['outcomes']['p']['target']['entry_open'] = 50.
            with self.assertRaises(ValueError): frames(root,bundle)

    def test_classification_keeps_missing_class_and_undefined_f1(self) -> None:
        result = classified([{'final_action':'CASH','label_net':'DOWN'}]*2)
        self.assertIsNone(result['balanced_accuracy']); self.assertIsNone(result['f1_positive'])
        self.assertIn('balanced_accuracy',result['undefined_reasons'])
        self.assertEqual(result['support_down'],2)

    def test_artifact_inventory_excludes_only_operational_receipt_and_locks(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ('a.csv','results.json','report.md','receipt.json','run.owner.json','run.lock'):(root/name).write_bytes(b'x')
            self.assertEqual(set(artifact_bindings(root)),{'a.csv','results.json','report.md'})


if __name__ == '__main__': unittest.main()
