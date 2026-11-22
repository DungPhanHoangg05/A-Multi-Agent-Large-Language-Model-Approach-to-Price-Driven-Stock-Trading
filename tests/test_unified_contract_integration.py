"""Kiểm nối economics/schema giữa engine fix và callers Prior/MT, không mạng."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import os
import unittest

import pandas as pd

from core.backtest_engine import PRIOR_BRANCH_MODES, compute_round_trip_net_return
from core.mt_bicl_accounting import account, evaluate_cycle
from core.prior_backtest import LEGACY_SCHEMA_VERSION, ResearchSchema, evaluate_point, summarize_points
from utils import static_util
from utils.target_contract import target_record_fields


def frame() -> pd.DataFrame:
    """Lịch qua weekend, có gap giữa decision Close và entry Open."""
    return pd.DataFrame({'Datetime': pd.bdate_range('2024-01-05', periods=8),
        'Open': [100., 90., 94., 95., 105., 103., 100., 99.],
        'High': [120.] * 8, 'Low': [80.] * 8, 'Close': [100., 92., 94., 95., 104., 102., 100., 99.],
        'Reference': [100., 100., 92., 94., 95., 104., 102., 100.], 'Volume': [1000.] * 8})


def branches(action: str = 'LONG') -> dict:
    """Năm action đã durable trước khi tạo evaluation."""
    return {name: {'status': 'complete', 'decision': {'action': action, 'confidence': 'Cao',
            'risk_reward_ratio': '1.5', 'latency_seconds': 0.}} for name in PRIOR_BRANCH_MODES}


def prior_point(evaluation: dict, action: str = 'LONG') -> dict:
    """Record đủ dữ kiện evaluator; không giả lập report hay gọi agent."""
    return {'status': 'complete', 'context': {'as_of_date': '2024-01-05'},
            'source_proof': {'prices': {'snapshot_start_date': '2024-01-05'}},
            'branches': branches(action), 'evaluation': evaluation}


class UnifiedContractTests(unittest.TestCase):
    """Oracle giá/phiên thật, canonical tamper, null risk và legacy compatibility."""

    def test_prior_and_mt_agree_on_gap_and_three_trading_sessions(self) -> None:
        data = frame()
        prior = evaluate_point(data, [], '2024-01-05', branches())
        mt = evaluate_cycle(data, [], '2024-01-05')
        for key, value in mt.items():
            self.assertEqual(prior[key], value)
        self.assertEqual((prior['decision_close'], prior['entry_open'], prior['exit_close']), (100., 90., 95.))
        self.assertEqual((prior['entry_date'], prior['exit_date']), ('2024-01-08', '2024-01-10'))
        self.assertEqual(prior['net_return'], compute_round_trip_net_return(90., 95.))
        self.assertEqual((prior['decision_bar_index'], prior['entry_bar_index'], prior['exit_bar_index']), (0, 1, 3))
        self.assertEqual(prior['label_contract_version'], 'net_cycle_v1')
        self.assertEqual(target_record_fields(prior)['target_horizon_bars'], 3)

    def test_cash_null_risk_validates_v2_without_relabeling_legacy(self) -> None:
        evaluation = evaluate_point(frame(), [], '2024-01-05', branches('SHORT'))
        point = prior_point(evaluation, 'SHORT')
        summary = summarize_points([point])
        ResearchSchema().validate(summary, 'summary')
        metrics = summary['original']['account_metrics']
        self.assertEqual(metrics['final_equity_vnd'], 50_000_000.)
        self.assertIsNone(metrics['sharpe_ratio'])
        self.assertIsNone(metrics['sortino_ratio'])
        self.assertEqual(metrics['risk_metrics']['frequency_status'], 'insufficient_schedule')
        json.dumps(summary, allow_nan=False)
        old = deepcopy(summary)
        for row in old.values():
            row['account_metrics'].pop('risk_metrics')
            row['account_metrics'].update(sharpe_ratio=0., sortino_ratio=0.)
        ResearchSchema(LEGACY_SCHEMA_VERSION).validate(old, 'summary')
        with self.assertRaises(ValueError):
            ResearchSchema().validate(old, 'summary')
        self.assertEqual(target_record_fields({'entry_open': 90., 'exit_close': 95.}), {})

    def test_prior_frequency_uses_session_indices_and_legacy_stays_unknown(self) -> None:
        data = frame()
        points = [prior_point(evaluate_point(data, [], data.Datetime.iloc[i].strftime('%Y-%m-%d'), branches()))
                  for i in (0, 3)]
        metrics = summarize_points(points)['original']['account_metrics']
        self.assertEqual(metrics['risk_metrics']['periods_per_year'], 84.)
        for point in points:
            point['evaluation'] = {k: v for k, v in point['evaluation'].items() if k in (
                'entry_open', 'exit_close', 'entry_date', 'exit_date', 'actual_direction', 'net_return_long', 'branches')}
        legacy = summarize_points(points)['original']['account_metrics']
        self.assertIsNone(legacy['sharpe_ratio'])
        self.assertEqual(legacy['risk_metrics']['frequency_status'], 'missing_bar_indices')

    def test_canonical_tamper_is_rejected_by_both_account_callers(self) -> None:
        original = evaluate_point(frame(), [], '2024-01-05', branches())
        for field, value in (('net_return', .99), ('entry_bar_index', 2), ('label_net', 'DOWN')):
            bad = {**original, field: value}
            with self.subTest(field=field), self.assertRaises(ValueError):
                summarize_points([prior_point(bad)])
            point = {'point_id': 'FPT-2024-01-05', 'symbol': 'FPT', 'repeat_index': 0,
                     'as_of_date': '2024-01-05', 'evaluation': bad, 'branches': {'original': {'action': 'LONG'}}}
            with self.subTest(mt_field=field), self.assertRaises(ValueError):
                account([point], 'original')

    def test_renderer_no_artifacts_keeps_fix_image_bytes(self) -> None:
        from scripts.audit_chart_convention import fixture_frame
        data = fixture_frame().to_dict('list')
        previous = Path.cwd()
        with TemporaryDirectory() as directory:
            try:
                os.chdir(directory)
                for render in (static_util.generate_kline_image, static_util.generate_trend_image):
                    quiet = render(data, write_artifacts=False)
                    self.assertFalse(list(Path(directory).iterdir()))
                    emitted = render(data, write_artifacts=True)
                    self.assertEqual(quiet, emitted)
                    for path in Path(directory).iterdir():
                        path.unlink()
            finally:
                os.chdir(previous)


if __name__ == '__main__':
    unittest.main()
