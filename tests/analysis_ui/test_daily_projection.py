"""Chiếu đúng policy/nguồn ra cửa sổ Original; không giả quyết định hoặc làm mất fallback."""
from copy import deepcopy
import unittest

from fixture import fixture
from utils.realtime_analysis_view import project


class DailyProjection(unittest.TestCase):
    def data(self) -> dict:
        data = fixture()['data']
        data['identity']['request'].update(mode='analyze',data_source='live',chart_timeframe='1d')
        data['requested_ids'] = ['C2']
        data['live_input'] = {'captured_at':'2026-11-13T10:00:00+07:00'}
        return data

    def test_fallback_uses_executed_reply_final_policy_and_common_alpha(self) -> None:
        data = self.data(); original = deepcopy(data)
        point = next(iter(data['snapshots']))
        data['policy_details'][f'forecast/{point}/r0/original_common']['raw_reply']['decision'] = 'LONG'
        result = project(data,'vi')
        self.assertEqual(result['final_decision']['decision'],'SHORT')
        self.assertIn('FALLBACK_ORIGINAL',result['bicl']['reason'])
        self.assertIn('Baseline chung',result['bicl']['status'])
        self.assertIn('Alpha common synthetic',result['alpha_analysis'])
        self.assertIsNone(result['bicl']['raw'])
        self.assertEqual(original['rows'],data['rows'])
        self.assertEqual(result['sentiment_data'],{})

    def test_model_html_remains_escaped_and_trace_retains_exact_context(self) -> None:
        data = self.data(); point = next(iter(data['snapshots']))
        attack = '<img src=x onerror=alert(1)>'
        data['snapshots'][point]['payload']['indicator_report'] = attack
        data['policy_details'][f'forecast/{point}/r0/C2']['context']['trace'] = {'evidence':{'tasks':[{'exit_date':'2026-01-01'}],'current_regime':'bull'}}
        result = project(data,'en')
        self.assertNotIn('<img',result['technical_indicators'])
        self.assertEqual(result['bicl']['prior_count'],1); self.assertEqual(result['bicl']['regime'],'bull')
        self.assertIn('2026-01-01',result['bicl']['details'])

    def test_incomplete_compare_or_other_timeframes_cannot_masquerade_as_daily_result(self) -> None:
        for key,value in [('state','running'),('mode','compare'),('chart_timeframe','5m'),('repeats',2)]:
            data = self.data()
            if key=='state': data[key]=value
            else: data['identity']['request'][key]=value
            with self.assertRaises(ValueError): project(data,'vi')
