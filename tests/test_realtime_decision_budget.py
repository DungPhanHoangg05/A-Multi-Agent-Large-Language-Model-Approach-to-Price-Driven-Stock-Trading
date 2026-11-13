"""UI realtime không bị trần benchmark, vẫn trả quyết định model thật và giữ guard backtest."""
import json
from types import SimpleNamespace
from unittest.mock import patch
import unittest

from agents.decision_agent import create_final_trade_decider
from core.decision_profiles import NATIVE_PROFILE


class Client:
    """Ghi đúng prompt/response schema; không gọi mạng và không dùng fallback action."""
    def __init__(self) -> None:
        self.prompts = []
    def invoke(self,prompt: str):
        self.prompts.append(prompt)
        return SimpleNamespace(content=json.dumps({'decision':'SHORT','forecast_horizon':'T+2.5',
            'confidence':'Low','risk_reward_ratio':1.,'evidence_for':'fixture','evidence_against':'fixture',
            'justification':'Actual fixture reply, no synthetic LONG/CASH.'}))


class RealtimeDecisionBudgetTests(unittest.TestCase):
    def state(self, language: str = 'en') -> dict:
        return {'stock_name':'FPT','time_frame':'1 Ngày','language':language,
            **{name+'_report':'R'*length for name,length in [('trend',441),('pattern',319),('indicator',414),('alpha',133),('sentiment',600)]}}

    def test_exact_7730_character_ui_incident_returns_real_binary_decision(self) -> None:
        client = Client()
        with patch('builtins.print'):
            result = create_final_trade_decider(client,decision_profile=NATIVE_PROFILE)(self.state())
        self.assertEqual(len(result['decision_prompt']),7730)
        self.assertEqual(client.prompts,[result['decision_prompt']])
        self.assertEqual(json.loads(result['final_trade_decision'])['decision'],'SHORT')
        self.assertNotIn('fallback',json.loads(result['final_trade_decision']).get('decision_source',''))

    def test_live_vi_en_long_reports_across_all_timeframes_do_not_invoke_budget_guard(self) -> None:
        for language in ('vi','en'):
            for timeframe in ('5m','15m','30m','1h','1d','1w','1mo'):
                state = self.state(language); state['time_frame'] = timeframe
                state.update({name+'_report':'R'*10000 for name in ('trend','pattern','indicator','alpha','sentiment')})
                client = Client()
                with patch('agents.decision_agent._guard_backtest_prompt',side_effect=AssertionError('Không phải backtest')),patch('builtins.print'):
                    result = create_final_trade_decider(client,decision_profile=NATIVE_PROFILE)(state)
                self.assertEqual(len(client.prompts),1)
                self.assertEqual(json.loads(result['final_trade_decision'])['decision'],'SHORT')

    def test_backtest_still_rejects_6500_before_any_model_call(self) -> None:
        state = {**self.state(),'is_backtest':True}; client = Client()
        with patch('agents.decision_agent._build_compact_prompt_en',return_value='R'*6500),patch('builtins.print'):
            with self.assertRaises(ValueError): create_final_trade_decider(client,decision_profile=NATIVE_PROFILE)(state)
        self.assertEqual(client.prompts,[])

    def test_structured_reply_for_7730_prompt_reaches_web_result_without_changing_decision(self) -> None:
        import importlib
        from scripts.verify_original_fix_parity import client_class
        client = client_class()(model='openai/gpt-oss-20b',temperature=0.,max_tokens=2048,max_retries=3)
        client.replies = [json.dumps({'decision':'SHORT','forecast_horizon':'T+2.5','confidence':'Low',
            'risk_reward_ratio':1.5,'evidence_for':'fixture','evidence_against':'fixture','justification':'fixture'})]
        with patch('builtins.print'):
            final_state = create_final_trade_decider(client,decision_profile=NATIVE_PROFILE)(self.state())
        self.assertEqual(len(client.requests),1)
        self.assertEqual(len(client.requests[0]['wire']['messages'][0]['content']),7730)
        self.assertEqual(json.loads(final_state['final_trade_decision'])['decision_source'],'llm_structured')
        with patch('core.realtime_loader.get_all_symbols_realtime',return_value=[]):
            web = importlib.import_module('web_interface')
        analyzer = object.__new__(web.WebTradingAnalyzer)
        result = analyzer.extract_analysis_results({'success':True,'asset_name':'FPT','timeframe':'1 day',
            'data_length':45,'final_state':final_state},'en')
        self.assertTrue(result['success']); self.assertEqual(result['final_decision']['decision'],'SHORT')
