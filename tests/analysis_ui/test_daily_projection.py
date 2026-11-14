"""Chiếu đúng policy/nguồn ra cửa sổ Original; không giả quyết định hoặc làm mất fallback."""
from copy import deepcopy
import unittest
import importlib
from unittest.mock import patch

from fixture import fixture
from utils.realtime_analysis_view import project


class DailyProjection(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with patch('core.realtime_loader.get_all_symbols_realtime',return_value=[]):
            cls.web=importlib.import_module('web_interface')
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
        self.assertIn('Báo cáo synthetic',result['alpha_analysis'])
        self.assertIn('Alpha common synthetic',result['common_alpha_analysis'])
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

    def test_complete_original_reference_report_keeps_formulas_components_and_expert_text(self) -> None:
        import json
        from pathlib import Path
        reference = json.loads((Path(__file__).parent/'report_reference.json').read_bytes())
        data = self.data(); point=next(iter(data['snapshots']))
        data['snapshots'][point]['payload']['alpha_report']=reference['alpha']
        result=project(data,'vi')
        from html import unescape
        self.assertEqual(unescape(result['alpha_analysis']),reference['alpha'])
        for text in ('composite_score','Công thức đầy đủ','Các bước tính toán','Alpha 5:','Chuyên gia định lượng','TỔNG HỢP'):
            self.assertIn(text,result['alpha_analysis'])
        self.assertIn('Alpha common synthetic',result['common_alpha_analysis'])

    def test_result_html_uses_full_alpha_and_separate_common_without_global_image_or_html_execution(self) -> None:
        data=self.data(); point=next(iter(data['snapshots']))
        data['snapshots'][point]['payload']['alpha_report']='## Full Alpha\n**Formula**: `<script>bad()</script>`'
        with self.web.app.test_request_context('/output?lang=en'):
            raw=self.web.render_localized('output.html',results=project(data,'en')).get_data(as_text=True)
        self.assertIn('Full Alpha',raw); self.assertIn('causal_common_v1',raw)
        self.assertIn('commonAlphaContent',raw); self.assertNotIn('<script>bad()</script>',raw)
        self.assertNotIn('/api/images/',raw)

    def test_owned_result_route_reads_dated_news_from_same_snapshot_without_inference(self) -> None:
        from types import SimpleNamespace
        from unittest.mock import Mock
        from core.historical_evaluation_data import FrozenNews
        data=self.data(); data['identity']['request']['snapshot_id']='b'*64
        point=next(iter(data['snapshots']))
        articles=[{'date_parsed':'2026-06-30','numeric_score':score,'label':label,'scorer':'lexicon','title':'Tin đã khóa'}
            for score,label in ((.8,'positive'),(.6,'positive'),(-.2,'negative'))]
        source,_=FrozenNews({'MWG':articles}).get_sentiment_at('MWG','2026-07-02')
        data['snapshots'][point]['payload']['sentiment_data']=source
        read=Mock(return_value={'news':articles}); result=Mock(return_value=data)
        backend=SimpleNamespace(result=result,snapshots=SimpleNamespace(read=read))
        with patch.dict(self.web.app.config,{'SERVING_LIVE_SERVICE':backend}),patch('utils.serving_web.owner',return_value=('a'*64,None)):
            response=self.web.app.test_client().get('/output?serving_run='+data['run_id']+'&serving_source=live&presentation=analysis&lang=en')
            self.assertEqual(response.status_code,200)
            raw=response.get_data(as_text=True)
            self.assertIn('Tin đã khóa',raw); self.assertIn('lexicon',raw)
            self.assertNotIn('REL_SENTIMENT',raw)
        read.assert_called_once_with('b'*64,'a'*64); result.assert_called_once_with(data['run_id'],'a'*64)
