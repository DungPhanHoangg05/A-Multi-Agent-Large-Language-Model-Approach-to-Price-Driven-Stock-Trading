"""Flask backtest/form/catalog/export và adapter legacy, không API thị trường/LLM thật."""
import csv
import importlib
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from fixtures import ROOT, Clock, Provider, Sender, Resources, spec, original, prices, legacy
from core.serving_contracts import ServingRequest
from core.serving_registry import MAIN_IDS
from core.serving_runtime.service import Service


class BacktestApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with patch('core.realtime_loader.get_all_symbols_realtime',return_value=[]):
            cls.web = importlib.import_module('web_interface')
    def setUp(self) -> None:
        self.temp = TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); self.clock = Clock(); self.senders = []
        def sender(key: str) -> Sender:
            client = Sender(self.clock,[original('LONG'),original('SHORT')]*4); self.senders.append(client); return client
        self.service = Service(ROOT,state_root=self.root,clock=self.clock,sender_factory=sender,provider_factory=Provider,resources_factory=Resources)
        self.settings = patch.dict(self.web.app.config,{'SERVING_SERVICE':self.service,
            'SERVING_API_KEY_PROVIDER':lambda:'fixture-key','SERVING_LEGACY_ROOT':self.root})
        self.settings.start(); self.addCleanup(self.settings.stop)
        self.loader = patch('core.serving_runtime.evaluation.prices',side_effect=prices)
        self.loader.start(); self.addCleanup(self.loader.stop)
        self.client = self.web.app.test_client(); self.addCleanup(self.join)
    def join(self) -> None:
        for worker in list(self.service.tasks.values()): worker.join(180); self.assertFalse(worker.is_alive())
    def start(self,client: object = None,request: dict | None = None) -> str:
        response = (client or self.client).post('/api/serving/v1/jobs',json=request or spec().document())
        self.assertEqual(response.status_code,202,response.get_data(as_text=True)); self.join()
        return response.get_json()['run_id']
    def saved(self) -> str:
        identifier = 'backtest_FPT_20261113_0910'; folder = self.root/'backtest_result'; folder.mkdir(exist_ok=True)
        (folder/(identifier+'.json')).write_text(json.dumps(legacy()),encoding='utf-8'); return identifier
    def test_bilingual_backtest_pages_split_assets_and_legacy_dispatch(self) -> None:
        for language in ('vi','en'):
            response = self.client.get('/backtest?lang='+language); raw = response.get_data(as_text=True)
            self.assertEqual(response.status_code,200)
            self.assertIn('js/backtest/main.js',raw); self.assertIn('name="bt-variant"',raw)
            self.assertIn('name="bt-symbol"',raw); self.assertIn('id="bt-start-job" type="submit" disabled',raw)
            self.assertNotIn('onclick="startBacktest()"',raw); self.assertNotIn('legacy.js',raw)
            raw = self.client.get('/backtest?source=legacy&lang='+language).get_data(as_text=True)
            self.assertIn('legacy.js',raw); self.assertIn('source=legacy&amp;lang=',raw)
            self.assertIn('onclick="startBacktest()"',raw)
        self.assertEqual(self.senders,[])
    def test_owned_catalog_isolation_and_new_runs_listed_without_inference(self) -> None:
        self.assertEqual(self.client.get('/api/serving/v1/jobs').get_json()['runs'],[])
        first = self.start(); other = self.web.app.test_client(); second = self.start(other)
        before = sum(len(s.bodies) for s in self.senders)
        rows = self.client.get('/api/serving/v1/jobs').get_json()['runs']
        self.assertEqual([r['id'] for r in rows],[first])
        self.assertEqual([r['id'] for r in other.get('/api/serving/v1/jobs').get_json()['runs']],[second])
        self.assertEqual(other.get('/api/serving/v1/jobs/'+first+'/evaluation').status_code,404)
        self.assertEqual(other.get('/api/serving/v1/jobs/'+first+'/export').status_code,404)
        self.assertEqual(sum(len(s.bodies) for s in self.senders),before)
    def test_filter_json_csv_export_share_same_values_and_preserve_na(self) -> None:
        identifier = self.start(); base = '/api/serving/v1/jobs/'+identifier
        query = {'methods':'original_common','repeat':'0','start_date':'2026-07-07','end_date':'2026-07-07','baseline':'original_fix'}
        response = self.client.get(base+'/evaluation',query_string=query)
        self.assertEqual(response.status_code,200); data = response.get_json()
        exported = self.client.get(base+'/export',query_string={**query,'format':'json'})
        self.assertEqual(exported.get_json(),data)
        csv_response = self.client.get(base+'/export',query_string={**query,'format':'csv','table':'summary'})
        rows = list(csv.DictReader(io.StringIO(csv_response.data.decode('utf-8-sig'))))
        self.assertEqual(rows[0]['mcc'],''); self.assertEqual(float(rows[0]['mean_account_return_pct']),0.)
        self.assertEqual(csv_response.headers['X-Content-Type-Options'],'nosniff')
        self.assertIn('attachment',csv_response.headers['Content-Disposition'])
        self.assertNotIn('fixture-key',exported.get_data(as_text=True))
    def test_duplicate_filters_cross_run_baseline_and_unknown_export_are_rejected(self) -> None:
        identifier = self.start(); base = '/api/serving/v1/jobs/'+identifier
        for url in (base+'/evaluation?repeat=0&repeat=1',base+'/evaluation?baseline=MT_BICL',
                    base+'/export?format=pickle',base+'/export?table=private',base+'/evaluation?owner=forged'):
            self.assertEqual(self.client.get(url).status_code,400,url)
    def test_full_no_alpha_legacy_is_separate_null_zero_and_error_not_cash(self) -> None:
        identifier = self.saved(); rows = self.client.get('/api/serving/v1/legacy-backtests').get_json()['runs']
        self.assertEqual(rows[0]['id'],identifier)
        data = self.client.get('/api/serving/v1/legacy-backtests/'+identifier).get_json()
        self.assertEqual([r['method'] for r in data['summary']],['legacy_full','legacy_no_alpha'])
        self.assertNotIn('original_common',json.dumps(data['summary']))
        self.assertEqual(data['summary'][0]['return_pct'],0.); self.assertIsNone(data['summary'][1]['accuracy_pct'])
        self.assertIsNone(data['predictions'][1]['final_action']); self.assertIsNone(data['predictions'][1]['net_return_pct'])
        self.assertNotIn('fixture-do-not-export',json.dumps(data))
        response = self.client.get('/api/serving/v1/legacy-backtests/'+identifier+'/export?format=csv&table=predictions')
        cells = list(csv.DictReader(io.StringIO(response.data.decode('utf-8-sig'))))
        self.assertTrue(cells[1]['error'].startswith("'")); self.assertEqual(cells[0]['net_return_pct'],'0.0')
    def test_legacy_path_invalid_json_and_symlink_rejected(self) -> None:
        identifier = self.saved(); target = self.root/'backtest_result'/(identifier+'.json')
        target.write_text('{"test_points":[],"pnl_full":NaN}',encoding='utf-8')
        self.assertEqual(self.client.get('/api/serving/v1/legacy-backtests/'+identifier).status_code,400)
        self.assertIn(self.client.get('/api/serving/v1/legacy-backtests/..%2Fother').status_code,(400,404))
        from utils.legacy_backtest import path
        with patch('pathlib.Path.is_symlink',return_value=True),self.assertRaises(ValueError): path(self.root,identifier)
    def test_experiments_keeps_u09_default_and_adds_new_and_legacy_kinds(self) -> None:
        page = self.client.get('/experiments?lang=en')
        self.assertEqual(page.status_code,200)
        raw = page.get_data(as_text=True)
        for kind in ('paper_evidence','serving_backtest','legacy_backtest','legacy_offline'):
            self.assertIn('value="'+kind+'"',raw)
        self.assertIn('id="bt-result"',raw)
        catalog = self.client.get('/api/research-results/runs').get_json()
        self.assertEqual(catalog['default'],'u09_analysis_r1')
        self.assertEqual(self.senders,[])
    def test_new_run_id_bootstrap_is_escaped_and_no_start_from_get(self) -> None:
        attack = '</script><img src=x onerror=attack()>'
        raw = self.client.get('/backtest',query_string={'run_id':attack}).get_data(as_text=True)
        self.assertNotIn(attack,raw); self.assertIn('\\u003c/script',raw); self.assertEqual(self.senders,[])
    def test_actual_all_six_one_point_backtest_uses_bound_prices_and_existing_economics(self) -> None:
        # Không patch loader trong ca này: dùng resource thật và HTTP fixture duy nhất.
        self.loader.stop()
        from core.serving_runtime.providers import AsOfProvider
        from core.serving_runtime.resources import Resources as ActualResources
        self.service.provider_factory = AsOfProvider; self.service.resources_factory = ActualResources
        value = spec(list(MAIN_IDS),1).document(); value.update(symbols=['MWG'],end_date='2026-07-02')
        identifier = self.start(request=value)
        data = self.client.get('/api/serving/v1/jobs/'+identifier+'/evaluation')
        self.assertEqual(data.status_code,200,data.get_data(as_text=True))
        result = data.get_json()
        self.assertEqual(result['evaluation_status'],'COMPLETE'); self.assertEqual(len(result['summary']),6)
        self.assertEqual(len(result['accounts']),6); self.assertEqual(len(result['daily_nav']),24)
        self.assertEqual(len(result['predictions']),6)
        self.assertTrue(all(r['label_net'] in ('UP','DOWN') for r in result['predictions']))
        self.assertIsNotNone(next(r for r in result['predictions'] if r['method']=='MT_BICL')['raw_prediction'])
        self.assertEqual(result['coverage']['planned_points'],1)
