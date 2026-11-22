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

    def test_model_html_remains_escaped_and_historical_example_hides_episode_id(self) -> None:
        data = self.data(); point = next(iter(data['snapshots']))
        attack = '<img src=x onerror=alert(1)>'
        data['snapshots'][point]['payload']['indicator_report'] = attack
        data['policy_details'][f'forecast/{point}/r0/C2']['context']['trace'] = {
            'evidence':{'tasks':[{'episode_id':'MWG:2025-12-28','exit_date':'2026-01-01'}],'current_regime':'bull'}}
        result = project(data,'en')
        self.assertNotIn('<img',result['technical_indicators'])
        self.assertEqual(result['bicl']['regime'],'bull')
        self.assertEqual(result['bicl']['examples'],[
            {'symbol':'MWG','date':'2025-12-28','exit_date':'2026-01-01','net_return':None}])
        self.assertNotIn('MWG:2025-12-28',str(result['bicl']))

    def test_research_prior_reads_saved_conditional_statistics_even_without_examples(self) -> None:
        from core.finalize_serving_profile import VERSION

        data = self.data()
        data['identity']['request'].update(version=VERSION, variant_ids=['A_tp_pool'])
        data['requested_ids'] = ['A_tp_pool']
        next(row for row in data['rows'] if row['requested_id'] == 'A_tp_pool').update(
            executed_id='A_tp_pool', raw_prediction='SHORT')
        point = next(iter(data['snapshots']))
        detail = data['policy_details'][f'forecast/{point}/r0/A_tp_pool']
        prefix = 'Win=4/12→0.36[0.15,0.60]; k=0'
        trace = {'request':{'prefix':prefix},'population_ids':list(range(62)),
                 'selected_ids':[],'counts':{'win_rate_long':{'numerator':25,'denominator':62,'rate':25/62},
                    'bull_trap_rate':{'numerator':9,'denominator':19,'rate':9/19}},
                 'conditional':{'groups':{'conditional':list(range(12)),'background':list(range(12,62))},
                    'metrics':{
                        'win_rate_long':{'raw_counts':{'conditional':{'success_count':4,'support_count':12},
                            'background':{'success_count':21,'support_count':50}},'posterior_mean':.3557692,
                            'credible_interval':{'lower':.1490,'upper':.5966}},
                        'bull_trap_rate':{'raw_counts':{'conditional':{'success_count':0,'support_count':0},
                            'background':{'success_count':9,'support_count':19}},'posterior_mean':None,
                            'credible_interval':None}}},
                 'gate':{'ready_metric_ids':['win_rate_long'],'examples_reason_codes':['NO_QUALIFIED_EXAMPLES']}}
        detail['context'] = {'trace':trace,'aux':{}}
        original = deepcopy(data)
        result = project(data,'vi')
        stats = result['bicl']['statistics']
        self.assertEqual([stats[f'{key}_count'] for key in ('population','conditional','background')],[62,12,50])
        self.assertEqual(result['bicl']['examples'],[])
        self.assertEqual([row['in_prompt'] for row in stats['rows']],[True,False])
        self.assertEqual([row['conditional'] for row in stats['rows']],['4/12','0/0'])
        for language, heading, no_examples in (
                ('vi','Prior và thống kê đã truy xuất','Không có ví dụ riêng đạt điều kiện chọn.'),
                ('en','Retrieved priors and statistics','No individual examples met the selection criteria.')):
            with self.subTest(language=language), self.web.app.test_request_context('/output?lang='+language):
                html = self.web.render_localized('output.html',results=result).get_data(as_text=True)
                for expected in (heading,no_examples,'>25/62<','>4/12<','>21/50<','>35.6%<','>14.9%–59.7%<','>0/0<'):
                    self.assertIn(expected,html)
                self.assertNotIn('class="bicl-context">{}</pre>',html)
        self.assertEqual(data,original)

    def test_research_bayesian_v1_shows_dates_and_returns_instead_of_episode_ids(self) -> None:
        data = self.data()
        data['requested_ids'] = ['bayesian_v1']
        next(row for row in data['rows'] if row['requested_id'] == 'bayesian_v1').update(
            executed_id='bayesian_v1',raw_prediction='SHORT')
        point = next(iter(data['snapshots']))
        detail = data['policy_details'][f'forecast/{point}/r0/bayesian_v1']
        episode = 'MWG:2025-01-06'
        detail['context'] = {'trace':{'population_ids':[episode],'conditional':None,
            'counts':{'win_rate_long':{'numerator':0,'denominator':1,'rate':0.}},
            'selected_ids':[episode],'request':{'prefix':f'Win=0/1(0.0%)\n{episode} T/P/A/I=-0++ L -1.25%'}},'aux':{}}
        result = project(data,'en')
        stats = result['bicl']['statistics']
        self.assertFalse(stats['conditional'])
        self.assertEqual(stats['rows'],[{'id':'win_rate_long','population':'0/1','rate':0.,'in_prompt':True}])
        self.assertEqual(result['bicl']['examples'],[
            {'symbol':'MWG','date':'2025-01-06','exit_date':None,'net_return':'-1.25%'}])
        for lang in ('vi','en'):
            with self.web.app.test_request_context('/output?lang='+lang):
                html = self.web.render_localized('output.html',results=result).get_data(as_text=True)
            for value in ('<td>MWG</td>','<td>2025-01-06</td>','<td>-1.25%</td>'):
                self.assertIn(value,html)
            for hidden in (episode,'population_ids','selected_ids','FIN05','T/P/A/I'):
                self.assertNotIn(hidden,html)

    def test_multitask_context_shows_saved_facts_and_group_summary_without_codes(self) -> None:
        data = self.data()
        data['requested_ids'] = ['MT_BICL']
        point = next(iter(data['snapshots']))
        data['policy_details'][f'forecast/{point}/r0/MT_BICL']['context']['aux'] = {
            'packet':{'point_id':point,'numeric':{'close':50.,'sma20':48.,'macd':-.2,'signal':-.3}},
            'branch':{'projection':{
                'summary':[{'task':'P1','n':4,'wins':3,'losses':1,'mean_r_net_fraction':.02}],
                'exemplars':[{'episode_id':'MWG-2025-01-06','task':'P1','r_net_fraction':.045}],
                'prefix':'MWG:block0021 P1'}}}
        result = project(data,'vi')
        with self.web.app.test_request_context('/output?lang=vi'):
            html = self.web.render_localized('output.html',results=result).get_data(as_text=True)
        for visible in ('Nhóm lịch sử 1','3/4','50.0000','+4.50%', '2025-01-06'):
            self.assertIn(visible,html)
        for hidden in ('MWG:block0021','MWG-2025-01-06','"task"'):
            self.assertNotIn(hidden,html)

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

    def test_saved_research_result_opens_full_report_with_stored_components(self) -> None:
        from html.parser import HTMLParser
        from types import SimpleNamespace
        from unittest.mock import Mock
        from core.finalize_serving_profile import VERSION

        class Report(HTMLParser):
            """Lấy ID báo cáo đang hiển thị, bỏ qua hai template song ngữ."""
            def __init__(self) -> None:
                super().__init__()
                self.ids = []
                self.in_template = False
                self.factors = 0

            def handle_starttag(self, tag: str, attrs: list) -> None:
                if tag == 'template':
                    self.in_template = True
                if not self.in_template:
                    node = dict(attrs)
                    self.ids.append(node.get('id'))
                    self.factors += 'alpha-card' in node.get('class', '').split()

            def handle_endtag(self, tag: str) -> None:
                if tag == 'template':
                    self.in_template = False

        data = self.data()
        spec = data['identity']['request']
        spec.pop('chart_timeframe')
        spec.update(version=VERSION, snapshot_id='b'*64)
        data['scientific_status'] = 'EXPLORATORY_NOT_CERTIFIED'
        point = next(iter(data['snapshots']))
        payload = data['snapshots'][point]['payload']
        payload['price_prefix']['Datetime'] = ['2026-07-02'] * 600
        for role in ('pattern','trend'):
            payload[f'{role}_image'] = 'iVBORw0KGgo='
        payload['causal_alpha']['projection']['factors'] = [
            {'alpha_id':name,'signal':'GIẢM','value':-.25,'orientation':-1}
            for name in ('CURRENT_1_FDM','CURRENT_2_SFA','WQ03_OpenVolCorr','WQ42_VwapCloseRatio','WQ45_DelayCloseCorr')]
        payload['sentiment_data'] = {'main_sentiment':{'avg_score':None},'missing_reason':'NO_ELIGIBLE_NEWS',
                                     'verified_article_count':0,'is_unavailable':True}
        backend = SimpleNamespace(result=Mock(return_value=data),snapshots=SimpleNamespace(read=Mock(return_value={'news':[]})))
        for variant in ('C2','original_fix'):
            data['requested_ids'] = [variant]
            with patch.dict(self.web.app.config,{'SERVING_LIVE_SERVICE':backend}),patch('utils.serving_web.owner',return_value=('a'*64,None)):
                path = '/output?serving_run='+data['run_id']+'&serving_source=live&lang=vi'
                client = self.web.app.test_client()
                response = client.get(path)
                self.assertEqual(response.status_code,200)
                raw = response.get_data(as_text=True)
                report = Report(); report.feed(raw)
                self.assertTrue({'indicatorContent','researchAlphaFactors','patternContent','patternChart',
                                 'trendContent','trendChart'} <= set(report.ids))
                self.assertEqual(report.factors,5)
                self.assertIn('Phân bổ bài báo - 0 bài',raw)
                self.assertIn('SENT_ZSCORE',raw); self.assertIn('REL_SENTIMENT',raw)
                self.assertIn('Công ty liên quan',raw)
                self.assertIn('Công thức đầy đủ',raw); self.assertIn('Các bước tính toán',raw)
                self.assertIn('Kết quả cuối cùng',raw)
                self.assertIn('decision-short',raw); self.assertIn('>45</div>',raw)
                self.assertIn('Không có bài đủ điều kiện',raw)
                self.assertIn('0.005 × C',raw)
                self.assertIn('BICL đã được áp dụng' if variant == 'C2' else 'Bản nghiên cứu',raw)
                self.assertIn('/api/serving/live/v1/jobs/'+data['run_id']+'/export',raw)
                self.assertNotIn('/api/images/',raw)
                self.assertIn('id="job-status-panel"',client.get(path+'&presentation=details').get_data(as_text=True))
        backend.snapshots.read.assert_called_with('b'*64,'a'*64)

    def test_research_alpha_renders_actual_fixed_window_implementation_in_both_languages(self) -> None:
        from utils.realtime_analysis_view import research_factor_metadata

        vi = research_factor_metadata('WQ52_TsMinRetVol','vi')
        en = research_factor_metadata('WQ52_TsMinRetVol','en')
        self.assertEqual(vi['implementation'],en['implementation'])
        self.assertIn('n240 = 240',vi['implementation'])
        self.assertIn('return _safe_series(p1 * r1 * r2)',vi['implementation'])
        self.assertEqual(research_factor_metadata('unknown-factor','vi')['implementation'],'')

    def test_research_sentiment_renders_bars_from_stored_article_probabilities(self) -> None:
        from core.finalize_serving_profile import VERSION

        data = self.data()
        request = data['identity']['request']
        request.pop('chart_timeframe')
        request['version'] = VERSION
        payload = next(iter(data['snapshots'].values()))['payload']
        payload['sentiment_data'] = {'main_sentiment':{'avg_score':.3,'article_count':3}, 'verified_article_count':3,
                                     'scored_articles':[{'published_at':'2026-07-01','numeric_score':row[1]-row[0],
                                                         'probabilities':row,'source_url_or_archive_id':'archive-fixture'}
                                                        for row in ([.1,.8,.1],[.2,.7,.1],[.8,.1,.1])]}
        result = project(data,'vi')
        self.assertTrue(result['sentiment_data']['distribution_available'])
        self.assertEqual([result['sentiment_data']['main_sentiment'][label] for label in ('positive','neutral_count','negative')],[2,0,1])
        with self.web.app.test_request_context('/output?lang=vi'):
            raw = self.web.render_localized('output.html',results=result).get_data(as_text=True)
        self.assertIn('aria-label="Tích cực 66.7%"',raw)
        self.assertIn('aria-label="Tiêu cực 33.3%"',raw)
        self.assertIn('archive-fixture',raw)

    def test_research_live_sentiment_shows_the_same_saved_article_in_both_languages(self) -> None:
        from core.finalize_serving_profile import VERSION

        data = self.data()
        request = data['identity']['request']
        request.pop('chart_timeframe')
        request['version'] = VERSION
        payload = next(iter(data['snapshots'].values()))['payload']
        url = 'https://cafef.vn/fpt-123456.chn'
        peer_url = 'https://cafef.vn/cmg-234567.chn'
        payload['sentiment_data'] = {
            'main_sentiment': {'avg_score': .4, 'article_count': 3}, 'verified_article_count': 3,
            'scorer_version': 'viquant-lexicon-v1', 'fallback_article_count': 1,
            'live_news': {'version': 'cafef_live_sentiment_v2', 'as_of_at': '2026-07-02T10:00:00.123456+07:00',
                          'status': 'AVAILABLE'},
            'scored_articles': [{'label': 'positive', 'numeric_score': .4, 'title': 'FPT công bố kết quả kinh doanh',
                                 'published_at': '2026-07-02T09:15:00+07:00', 'source_url_or_archive_id': url}],
            'sentiment_norm': {'z_score': .0234, 'rel_sentiment': .1301, 'is_reliable': False, 'relative_peer_count': 1},
            'related_sentiment': {'CMG': {'name': 'CMC', 'avg_score': .2699, 'article_count': 3, 'industry_code': '9530',
                                          'scored_articles': [{'title': 'CMC ký hợp đồng', 'numeric_score': .15,
                                                               'published_at': '2026-07-02T09:30:00+07:00',
                                                               'source_url_or_archive_id': peer_url}]}},
            'related_norm': {'CMG': {'z_score': -.012, 'is_reliable': False}},
            'relative_available': True}
        for lang, heading, fallback, industry, sample in (
                ('vi', 'Dữ liệu Sentiment (CafeF live)', 'Số bài chấm bằng từ điển dự phòng', 'Cùng nhóm ngành ICB', 'Mẫu nhỏ'),
                ('en', 'Sentiment data (CafeF live)', 'Articles scored with the fallback lexicon', 'Same ICB industry group', 'Small sample')):
            with self.subTest(lang=lang), self.web.app.test_request_context('/output?lang='+lang):
                raw = self.web.render_localized('output.html', results=project(data, lang)).get_data(as_text=True)
                for text in (heading, fallback, industry, sample, f'href="{url}"', f'href="{peer_url}"',
                             'FPT công bố kết quả kinh doanh', '2026-07-02 09:15:00+07:00', '+0.4000',
                             '+0.0234', '+0.1301', '− avg_' if lang == 'en' else 'avg_nhóm_đối_chiếu', 'CMG'):
                    self.assertIn(text, raw)
                self.assertNotIn('FIN05', raw)
                self.assertNotIn('No eligible articles', raw)
