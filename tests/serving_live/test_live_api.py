"""Luồng phân tích mới nhất qua Flask/provider thật; chỉ mock mạng thị trường và HTTP Groq."""
from copy import deepcopy
from datetime import datetime
import importlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from support import ROOT, Clock, Sender, prices, news, request, runtime
from core.serving_live.snapshots import Snapshots, ZONE
from core.serving_live.service import LiveService, LiveRequest
from core.serving_runtime.service import Service
from core.serving_registry import MAIN_IDS


class LiveApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with patch('core.realtime_loader.get_all_symbols_realtime',return_value=[]):
            cls.web = importlib.import_module('web_interface')

    def setUp(self) -> None:
        self.temp = TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); self.clock = Clock(); self.senders = []; self.market_calls = []
        def market(symbol: str):
            self.market_calls.append(symbol); return prices(symbol)
        self.snapshots = Snapshots(self.root/'inputs',prices=market,news=news,now=lambda:datetime(2026,11,13,10,tzinfo=ZONE))
        def sender(key: str):
            result = Sender(self.clock); self.senders.append(result); return result
        self.service = LiveService(ROOT,state_root=self.root/'live',snapshots=self.snapshots,clock=self.clock,sender_factory=sender)
        self.asof = Service(ROOT,state_root=self.root/'asof',clock=self.clock,sender_factory=sender)
        settings = patch.dict(self.web.app.config,{'SERVING_SERVICE':self.asof,'SERVING_LIVE_SERVICE':self.service,
            'SERVING_API_KEY_PROVIDER':lambda:'fixture-live-key'})
        settings.start(); self.addCleanup(settings.stop)
        self.client = self.web.app.test_client(); self.addCleanup(self.join)

    def join(self) -> None:
        for worker in list(self.service.tasks.values()):
            worker.join(240); self.assertFalse(worker.is_alive())

    def capture(self) -> dict:
        response = self.client.post('/api/serving/live/v1/snapshot',json={'symbol':'MWG'})
        self.assertEqual(response.status_code,200,response.get_json())
        return response.get_json()

    def test_actual_each_selected_version_and_all_six_compare_use_live_prefix_not_u09(self) -> None:
        captured = self.capture(); self.assertEqual(captured['cutoff'],'2026-11-12')
        for ids,mode in [*(([identifier],'analyze') for identifier in MAIN_IDS),(list(MAIN_IDS),'compare')]:
            body = request(captured['snapshot_id'],captured['cutoff'],ids,mode=mode)
            checked = self.client.post('/api/serving/live/v1/preflight',json=body)
            self.assertTrue(checked.get_json()['run_enabled'],checked.get_json())
            response = self.client.post('/api/serving/live/v1/jobs',json=body)
            self.assertEqual(response.status_code,202,response.get_json()); self.join()
            identifier = response.get_json()['run_id']
            count = sum(len(s.bodies) for s in self.senders)
            data = self.client.get('/api/serving/live/v1/jobs/'+identifier).get_json()
            self.assertEqual(data['state'],'completed',data.get('error'))
            self.assertEqual(data['requested_ids'],ids); self.assertEqual(data['identity']['request']['mode'],mode)
            self.assertEqual(data['identity']['config']['provider_version'],'serving_live_daily_v1')
            self.assertEqual(data['outcome_points'],0)
            self.assertTrue(all(row['net_return_pct'] is None and row['as_of_date']=='2026-11-12' for row in data['rows']))
            self.assertEqual(len(data['snapshots']),1)
            snapshot = next(iter(data['snapshots'].values()))
            self.assertEqual(snapshot['payload']['price_prefix']['Datetime'][-1],'2026-11-12')
            self.assertIn('LIVE_FROZEN_SELECTION_TRANSFER',snapshot['payload']['causal_alpha']['projection']['scope'])
            self.assertTrue(all('live_input' in row['context']['trace'] for row in data['policy_details'].values()))
            if 'MT_BICL' in ids: self.assertIn('Fact_Anchor',data['execution_plan'])
            sender = self.senders[-1]
            self.assertEqual(sum('response_format' not in body for body in sender.bodies),2)
            self.assertTrue(all(len(body['messages'][0]['content']) < 6500 for body in sender.bodies if 'response_format' in body))
            self.assertNotIn('fixture-live-key',json.dumps(data))
            self.assertEqual(self.client.get('/api/serving/live/v1/jobs/'+identifier+'/export').get_json(),data)
            self.assertEqual(count,sum(len(s.bodies) for s in self.senders))
            self.assertEqual(self.web.app.test_client().get('/api/serving/live/v1/jobs/'+identifier).status_code,404)
            self.assertEqual(self.client.get('/api/serving/v1/jobs/'+identifier).status_code,404)
        self.assertEqual(self.market_calls,['MWG','VNINDEX'])

    def test_snapshot_owner_symbol_date_and_origin_are_bound_before_dispatch(self) -> None:
        captured = self.capture(); body = request(captured['snapshot_id'],captured['cutoff'],['original_fix'])
        other = self.web.app.test_client()
        self.assertEqual(other.post('/api/serving/live/v1/jobs',json=body).status_code,404)
        for name,value in [('symbols',['FPT']),('start_date','2026-11-11')]:
            changed = deepcopy(body); changed['request'][name] = value
            if name=='start_date': changed['request']['end_date'] = value
            self.assertEqual(self.client.post('/api/serving/live/v1/jobs',json=changed).status_code,409)
        self.assertEqual(self.client.post('/api/serving/live/v1/snapshot',json={'symbol':'MWG'},headers={'Origin':'https://example.com'}).status_code,400)
        self.assertEqual(self.senders,[])

    def test_live_form_default_and_result_shell_preserve_source_without_inference(self) -> None:
        from html.parser import HTMLParser
        raw = self.client.get('/demo?lang=vi').get_data(as_text=True)
        self.assertIn('<option value="latest" selected>',raw)
        self.assertIn('id="capture-live"',raw); self.assertIn('MT_BICL',raw)
        raw = self.client.get('/output?serving_run=12345678-1234-4234-8234-123456789abc&serving_source=live&lang=en').get_data(as_text=True)
        self.assertIn('"source": "live"',raw); self.assertIn('serving_source=live',raw)
        self.assertEqual(self.market_calls,[]); self.assertEqual(self.senders,[])

    def recovery(self, unknown: bool) -> None:
        """Dùng provider nhẹ cho lỗi vận hành; snapshot/resource/transport/store live vẫn thật."""
        captured = self.capture(); record = self.snapshots.read(captured['snapshot_id'])
        owner = record['owner_scope_sha256']; key = 'fixture-live-key'
        spec = LiveRequest.create(request(captured['snapshot_id'],captured['cutoff'],['original_fix','original_common'],mode='compare'))
        def provider(reservation: dict):
            body = reservation['job']['identity']['request']
            return runtime.Provider(ROOT,reservation['points'],body['models'],body['variant_ids'])
        self.service.provider = provider
        identifier = self.service.create(spec,key,owner,background=False)
        sender = Sender(self.clock,actions=[TimeoutError('fixture')] if unknown else [])
        if not unknown: sender.on_send = lambda:self.service.store.control(identifier,True)
        self.service.sender_factory = lambda _:sender
        self.service.work(identifier,key,owner,wait=False)
        before = self.service.result(identifier,owner)
        self.assertEqual(before['state'],'unknown' if unknown else 'stopped')
        sender.on_send = None
        fresh = LiveService(ROOT,state_root=self.root/'live',snapshots=self.snapshots,clock=self.clock,sender_factory=lambda _:sender)
        fresh.provider = provider
        generation = fresh.store.control(identifier)['generation']
        fresh.work(identifier,key,owner,wait=False,resume_generation=generation)
        after = fresh.result(identifier,owner)
        self.assertEqual(after['identity_sha256'],before['identity_sha256'])
        self.assertEqual(after['live_input']['snapshot_id'],captured['snapshot_id'])
        self.assertEqual(self.market_calls,['MWG','VNINDEX'])
        if unknown:
            self.assertEqual(after['state'],'unknown'); self.assertEqual(after['rows'],[])
            self.assertEqual(len(sender.bodies),1)
        else:
            self.assertEqual(after['state'],'completed'); self.assertEqual(after['rows'][0],before['rows'][0])
            self.assertEqual(len(sender.bodies),2)

    def test_fresh_live_service_resumes_same_capture_without_refetch_or_duplicate(self) -> None:
        self.recovery(False)

    def test_unknown_live_attempt_never_resends_or_becomes_cash_after_restart(self) -> None:
        self.recovery(True)
