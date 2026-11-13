"""Kiểm form/result qua Flask thật và job fixture, không gọi thị trường hoặc hosted LLM."""
from copy import deepcopy
from html.parser import HTMLParser
import importlib
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT),str(ROOT/'tests/serving_runtime')]
from support import Clock, Provider, FixtureResources, Sender, spec
from core.serving_runtime.service import Service
from core.serving_registry import MAIN_IDS
from core.serving_contracts import ServingRequest
from utils.analysis_ui import messages


class Page(HTMLParser):
    """Đọc JSON bootstrap và thuộc tính để kiểm escaping/asset mà không cần browser."""
    def __init__(self, raw: str) -> None:
        super().__init__(); self.nodes = []; self.config = ''; self.active = False; self.feed(raw)
    def handle_starttag(self, tag: str, attrs: list) -> None:
        row = dict(attrs); self.nodes.append((tag,row))
        if tag == 'script' and row.get('id') == 'analysis-config': self.active = True
    def handle_data(self, data: str) -> None:
        if self.active: self.config += data
    def handle_endtag(self, tag: str) -> None:
        if tag == 'script': self.active = False


class AnalysisPages(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with patch('core.realtime_loader.get_all_symbols_realtime',return_value=[]):
            cls.web = importlib.import_module('web_interface')
    def setUp(self) -> None:
        self.temp = TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.clock = Clock(); self.senders = []
        def sender(key: str) -> Sender:
            client = Sender(self.clock); self.senders.append(client); return client
        self.service = Service(ROOT,state_root=Path(self.temp.name),clock=self.clock,
            resources_factory=FixtureResources,provider_factory=Provider,sender_factory=sender)
        self.settings = patch.dict(self.web.app.config,{'SERVING_SERVICE':self.service,'SERVING_API_KEY_PROVIDER':lambda:'fixture-private-key'})
        self.settings.start(); self.addCleanup(self.settings.stop)
        self.client = self.web.app.test_client(); self.addCleanup(self.join)
    def join(self) -> None:
        for worker in list(self.service.tasks.values()):
            worker.join(180); self.assertFalse(worker.is_alive())

    def test_home_bilingual_six_choices_defaults_and_local_assets(self) -> None:
        for lang in ('vi','en'):
            response = self.client.get('/demo?lang='+lang)
            self.assertEqual(response.status_code,200)
            page = Page(response.get_data(as_text=True)); config = json.loads(page.config)
            self.assertEqual(config['language'],lang)
            self.assertEqual(config['messages'],messages(lang))
            self.assertNotIn('name="compare-method"',response.get_data(as_text=True))
            self.assertNotIn('id="compareBtn"',response.get_data(as_text=True))
            raw = response.get_data(as_text=True)
            self.assertIn('<option value="legacy" selected>',raw)
            self.assertNotIn('<option value="latest"',raw); self.assertNotIn('<option value="asof"',raw)
            self.assertNotIn('id="asof-inputs"',raw)
            self.assertEqual([a['data-tf'] for tag,a in page.nodes if 'data-tf' in a],['1d'])
            self.assertEqual(len([a for tag,a in page.nodes if a.get('id') == 'step-bicl']),1)
            self.assertLess(raw.index('id="step-bicl"'),raw.index('id="step6"'))
            self.assertEqual(raw.count('<option value='),7)
            self.assertIn('disabled',next(a for tag,a in page.nodes if a.get('id') == 'analyzeBtn'))
            self.assertNotIn('onclick',next(a for tag,a in page.nodes if a.get('id') == 'analyzeBtn'))
            for tag,attrs in page.nodes:
                url = attrs.get('src',attrs.get('href',''))
                if url.startswith('/static/'):
                    self.assertEqual(self.client.get(url).status_code,200,url)
    def test_result_shell_get_does_not_infer_and_never_loads_legacy_images(self) -> None:
        raw = self.client.get('/output?serving_run=12345678-1234-4234-8234-123456789abc&lang=en').get_data(as_text=True)
        self.assertIn('js/analysis/result.js',raw)
        self.assertNotIn('legacy_output.js',raw); self.assertNotIn('/api/images/',raw)
        self.assertEqual(json.loads(Page(raw).config)['messages']['metric'],'No outcome yet · NOT_EVALUATED')
        self.assertEqual(self.senders,[])
    def test_untrusted_query_is_json_escaped_and_empty_id_stays_in_serving_shell(self) -> None:
        attack = '</script><img src=x onerror=attack()>'
        response = self.client.get('/output',query_string={'serving_run':attack})
        raw = response.get_data(as_text=True)
        self.assertNotIn(attack,raw)
        self.assertEqual(json.loads(Page(raw).config)['runId'],attack)
        self.assertIn('js/analysis/result.js',self.client.get('/output?serving_run=').get_data(as_text=True))
    def test_legacy_result_and_job_routes_remain_available(self) -> None:
        for lang in ('vi','en'):
            raw = self.client.get('/output?lang='+lang).get_data(as_text=True)
            self.assertIn('legacy_output.js',raw); self.assertIn('legacy_output.css',raw)
            self.assertNotIn('id="analysis-config"',raw)
        identifier = 'fixture-legacy'
        self.web._jobs[identifier] = {'status':'done','step':6,'result':{'success':True},'ts':0}
        try:
            self.assertEqual(self.client.get('/api/analyze/status/'+identifier).get_json()['status'],'done')
        finally: self.web._jobs.pop(identifier,None)
    def test_owned_api_start_reload_context_and_read_only_result(self) -> None:
        request = spec(['original_fix','original_common'],'compare').document()
        self.assertTrue(self.client.post('/api/serving/v1/preflight',json=request).get_json()['run_enabled'])
        created = self.client.post('/api/serving/v1/jobs',json=request)
        self.assertEqual(created.status_code,202); identifier = created.get_json()['run_id']; self.join()
        count = sum(len(s.bodies) for s in self.senders)
        for _ in range(2):
            self.assertEqual(self.client.get('/output?serving_run='+identifier).status_code,200)
            data = self.client.get('/api/serving/v1/jobs/'+identifier).get_json()
            self.assertEqual(data['state'],'completed')
            self.assertTrue(all(row['net_return_pct'] is None for row in data['rows']))
            self.assertEqual(len(data['snapshots']),1)
            for value in data['policy_details'].values():
                self.assertIn('trace',value['context']); self.assertIn('aux',value['context'])
            self.assertNotIn('fixture-private-key',json.dumps(data))
        self.assertEqual(count,sum(len(s.bodies) for s in self.senders))
        self.assertEqual(self.web.app.test_client().get('/api/serving/v1/jobs/'+identifier).status_code,404)
    def test_all_six_through_web_api_actual_resources_and_fixture_http(self) -> None:
        from core.serving_runtime.providers import AsOfProvider
        from core.serving_runtime.resources import Resources
        self.service.resources_factory = Resources; self.service.provider_factory = AsOfProvider
        request = spec(list(MAIN_IDS),'compare',symbol='MWG').document()
        created = self.client.post('/api/serving/v1/jobs',json=request)
        self.assertEqual(created.status_code,202,created.get_data(as_text=True))
        self.join(); identifier = created.get_json()['run_id']
        data = self.client.get('/api/serving/v1/jobs/'+identifier).get_json()
        self.assertEqual(data['state'],'completed',data.get('error'))
        self.assertEqual(data['requested_ids'],list(MAIN_IDS)); self.assertEqual(len(data['rows']),8)
        self.assertEqual(len(data['snapshots']),1)
        self.assertIsNotNone(next(r for r in data['rows'] if r['requested_id']=='MT_BICL')['raw_prediction'])
        for value in data['policy_details'].values(): self.assertIsInstance(value['context']['aux'],dict)
    def test_english_reports_and_missing_resources_are_blocked_before_start(self) -> None:
        request = spec().document(); request['language'] = 'en'
        self.assertEqual(self.client.post('/api/serving/v1/jobs',json=request).status_code,409)
        with patch.object(self.service.resources_factory,'verify',side_effect=ValueError('fixture')):
            request['language'] = 'vi'
            self.assertFalse(self.client.post('/api/serving/v1/preflight',json=request).get_json()['run_enabled'])
        self.assertEqual(self.senders,[])


if __name__ == '__main__': unittest.main()
