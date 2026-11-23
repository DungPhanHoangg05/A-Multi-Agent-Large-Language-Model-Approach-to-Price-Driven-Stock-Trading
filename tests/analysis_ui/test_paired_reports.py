"""Kết quả có sẵn VI/EN, canonical riêng và chuyển ngôn ngữ không cần inference."""
from copy import deepcopy
from pathlib import Path
import json
import unittest
from unittest.mock import Mock,patch
from langchain_core.messages import AIMessage,HumanMessage

from core.ui_presentation.capture import capture,ReportClient,DecisionClient
from core.ui_presentation.wire import decision_body,decision_reply,report_reply
from agents.decision_agent import TradeDecisionOutput
from utils.paired_reports import result_views


class PairedReports(unittest.TestCase):
    def test_original_graph_stream_captures_pairs_with_one_invocation_per_node(self) -> None:
        from importlib import import_module
        from types import SimpleNamespace
        from agents.alpha_agent import _alpha1_fdm,_build_alpha_report
        from core.ui_presentation.capture import CURRENT
        from scripts.verify_original_fix_parity import market_frame
        from utils.graph_setup import SetGraph
        from utils.graph_util import TechnicalTools
        with patch('core.realtime_loader.get_all_symbols_realtime',return_value=[]):
            web=import_module('web_interface')
        calls=[]
        class Client:
            """Chỉ thế model; LangGraph, Indicator và Decision vẫn là mã thật."""
            model_name='fixture'
            def invoke(self,messages):
                calls.append('report')
                paired='LIVE UI OUTPUT OVERRIDE' in str(messages)
                return AIMessage(content=json.dumps({'vi':'Giá 50.1','en':'Price 50.1'}) if paired else 'Giá 50.1')
            def with_structured_output(self,schema,**options):
                def invoke(prompt):
                    calls.append('decision')
                    value={'decision':'SHORT','forecast_horizon':'T+2.5','confidence':'Cao','risk_reward_ratio':1.,
                        'evidence_for':'Giảm','evidence_against':'Tăng','justification':'Giá 50.1',
                        'display_en':{'evidence_for':'Bearish','evidence_against':'Bullish','justification':'Price 50.1'}}
                    return {'parsed':value,'raw':AIMessage(content=json.dumps(value)),'parsing_error':None}
                return SimpleNamespace(invoke=invoke)
        def report_factory(role):
            def factory(client,*args):
                def node(state):
                    vi=client.invoke([HumanMessage(content=role)]).content
                    if role!='alpha': return {role+'_report':vi}
                    factor=_alpha1_fdm({},'vi')
                    data={'alpha_results':[factor],'tech_vars':{},'sentiment_norm':{}}
                    return {'alpha_report':_build_alpha_report([factor],{},{},'FPT','vi')+'\n'+vi,'sentiment_data':data}
                return node
            return factory
        client=Client()
        with patch('utils.graph_setup.create_alpha_agent',side_effect=report_factory('alpha')), \
             patch('utils.graph_setup.create_pattern_agent',side_effect=report_factory('pattern')), \
             patch('utils.graph_setup.create_trend_agent',side_effect=report_factory('trend')),patch('builtins.print'):
            graph=SetGraph(client,client,TechnicalTools()).set_graph()
            analyzer=object.__new__(web.WebTradingAnalyzer); analyzer.trading_graph=SimpleNamespace(graph=graph)
            with patch('web_interface.static_util.generate_kline_image',return_value={'pattern_image':'fixture'}), \
                 patch('web_interface.static_util.generate_trend_image',return_value={'trend_image':'fixture'}):
                result=analyzer.run_analysis(market_frame().iloc[:600],'FPT','1d',step_callback=lambda step:None,lang='en')
        self.assertTrue(result['success'],result.get('error'))
        self.assertEqual(calls,['report','report','report','report','decision'])
        self.assertEqual(result['ui_report_pairs']['decision']['en']['justification'],'Price 50.1')
        self.assertIn('MACD',result['ui_report_pairs']['indicator']['en'])
        self.assertIn('Calculation',result['ui_report_pairs']['alpha']['en'])
        self.assertIsNone(CURRENT.get())

    def test_dynamic_factor_id_is_not_inferred_from_rank(self) -> None:
        from core.ui_presentation.reports import alpha_english
        factor={'id':1,'name':'Tên cũ','type':'Loại','formula':'Adapted CURRENT_4',
            'horizon':'T+2.5','value':-.37,'signal':'GIẢM','components':{'ic':-.12},'interpretation':'Mô tả'}
        source={'alpha_results':[factor],'tech_vars':{},'sentiment_norm':{}}; original=deepcopy(source)
        report=alpha_english(source,'FPT','1d')
        self.assertIn('CURRENT_4',report); self.assertIn('-0.37',report); self.assertIn('-0.12',report)
        self.assertNotIn('Flow-Driven Momentum',report); self.assertEqual(source,original)

    def test_report_proxy_calls_once_and_does_not_change_non_ui_invocation(self) -> None:
        base=Mock(); base.invoke.return_value=AIMessage(content=json.dumps({'vi':'Giá 50.1; LONG','en':'Price 50.1; LONG'}))
        proxy=ReportClient(base,'pattern'); messages=[HumanMessage(content='chart')]
        with capture() as reports:
            response=proxy.invoke(messages)
        self.assertEqual(base.invoke.call_count,1); self.assertEqual(response.content,'Giá 50.1; LONG')
        self.assertEqual(reports['pattern']['en'],'Price 50.1; LONG'); self.assertEqual(len(messages),1)
        base.invoke.reset_mock(); proxy.invoke(messages)
        base.invoke.assert_called_once_with(messages)

    def test_decision_wire_preserves_canonical_schema_and_splits_ui_fields(self) -> None:
        schema=TradeDecisionOutput.model_json_schema(); original=deepcopy(schema)
        body=decision_body({'messages':[{'role':'user','content':'canonical prompt'}],
            'response_format':{'json_schema':{'schema':schema}}})
        self.assertEqual(schema,original); self.assertIn('display_en',body['response_format']['json_schema']['schema']['properties'])
        reply={'decision':'SHORT','forecast_horizon':'T+2.5','confidence':'Cao','risk_reward_ratio':1.,
            'evidence_for':'Giảm','evidence_against':'Tăng','justification':'Giá 50.1',
            'display_en':{'evidence_for':'Bearish','evidence_against':'Bullish','justification':'Price 50.1'}}
        canonical,en=decision_reply(reply); TradeDecisionOutput.model_validate(canonical,strict=True)
        self.assertNotIn('display_en',canonical); self.assertEqual(en['justification'],'Price 50.1')
        self.assertIn('display_en',reply)

    def test_live_translations_accept_localized_dates_and_cash_without_changing_raw_text(self) -> None:
        import json

        vi = 'Nến đỏ ngày 20/11 phá hỗ trợ 18.75.'
        en = 'The red candle on Nov 20 broke support at 18.75.'
        self.assertEqual(report_reply(json.dumps({'vi':vi,'en':en})), {'vi':vi,'en':en})
        for incorrect in ('The red candle on Nov 21 broke support at 18.75.',
                          'The red candle on Nov 20 broke support at 18.50.'):
            self.assertEqual(report_reply(json.dumps({'vi':vi,'en':incorrect})), {'vi':vi,'en':None})
        source = {'justification':'Chọn SHORT để giữ CASH; LONG thiếu xác nhận.',
                  'evidence_for':'MACD 18.75', 'evidence_against':'RSI 39', 'decision':'SHORT'}
        english = {'justification':'Choose SHORT to hold cash; LONG is unconfirmed.',
                   'evidence_for':'MACD 18.50', 'evidence_against':'RSI 39'}
        canonical, shown = decision_reply({**source, 'display_en':english})
        self.assertEqual(canonical, source)
        self.assertEqual(shown, {**english,'evidence_for':None})
        from core.serving_runtime.quota import Failed
        for invalid in ('```', '[]', '{"vi":" "}', '{"en":"English only"}'):
            with self.assertRaisesRegex(Failed, 'INVALID_MODEL_OUTPUT'):
                report_reply(invalid)

    def test_invalid_english_display_uses_original_text_with_language_marker(self) -> None:
        from utils.paired_reports import result_views
        views = result_views({'report_language':'vi','pattern_analysis':'Nến đỏ ngày 20/11',
                              'final_decision':{'decision':'SHORT','justification':'Giữ CASH'},
                              'ui_report_pairs':{'pattern':{'vi':'Nến đỏ ngày 20/11','en':None},
                                                 'decision':{'en':{'justification':None}}}}, {})
        self.assertEqual(views['en']['pattern_analysis'], views['vi']['pattern_analysis'])
        self.assertEqual(views['en']['final_decision']['justification'], 'Giữ CASH')
        self.assertEqual(views['en']['report_source_languages'], {'pattern_analysis':'vi','justification':'vi'})

    def test_view_uses_stored_pairs_and_keeps_numeric_decision_unchanged(self) -> None:
        source={'report_language':'vi','asset_name':'FPT','alpha_analysis':'Alpha gốc',
            'final_decision':{'decision':'SHORT','risk_reward_ratio':1.,'confidence':'Cao','justification':'Lý do'},
            'ui_report_pairs':{'alpha':{'vi':'Alpha gốc','en':'Full English Alpha'},
                'decision':{'vi':{'justification':'Lý do'},'en':{'justification':'Reason'}}}}
        original=deepcopy(source); views=result_views(source,{})
        self.assertEqual(views['en']['alpha_analysis'],'Full English Alpha')
        self.assertEqual(views['vi']['alpha_analysis'],'Alpha gốc')
        self.assertEqual(views['en']['final_decision']['justification'],'Reason')
        self.assertEqual(views['en']['final_decision']['decision'],'SHORT'); self.assertEqual(source,original)

    def test_current_prepared_cache_reports_do_not_require_language_api(self) -> None:
        fixture=json.loads((Path(__file__).parent/'completion_regression.json').read_bytes())
        result={'report_language':'vi','alpha_analysis':fixture['source_reports']['n18'].rstrip(),
            'pattern_analysis':fixture['source_reports']['n19'].rstrip(),'trend_analysis':fixture['source_reports']['n20'].rstrip()}
        cache={value.rstrip():fixture['english_reports'][name] for name,value in fixture['source_reports'].items()}
        views=result_views(result,cache)
        self.assertIn('Trend forecast',views['en']['trend_analysis']); self.assertIn('Trading implication',views['en']['pattern_analysis'])
        self.assertIn('composite_score',views['en']['alpha_analysis'])

    def test_completed_cache_ignores_only_trailing_template_whitespace(self) -> None:
        from tempfile import TemporaryDirectory
        from core.historical_evaluation_journal import save
        from utils.paired_reports import cached_pairs
        with TemporaryDirectory() as folder:
            root=Path(folder); cache=root/'outputs/display_locales/v1/fixture'; cache.mkdir(parents=True)
            save(cache/'source.json',{'owner':'fixture','target':'en','texts':{'n0':'Giá 50.1\n                            '}})
            save(cache/'status.json',{'state':'completed'}); save(cache/'result.json',{'n0':'Price 50.1\n'})
            self.assertEqual(cached_pairs(root,'fixture'),{'Giá 50.1':'Price 50.1'})
            self.assertEqual(cached_pairs(root,'other'),{})
