"""Nghiệm thu đường HTTP thật/worker restart và support release, chỉ mock HTTP Groq."""
from collections import Counter
from copy import deepcopy
import csv
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import threading
import unittest
from unittest.mock import patch

from flask import Flask
from werkzeug.serving import make_server, WSGIRequestHandler

from fixtures import ROOT, Clock, Sender, Provider, FixtureResources, spec, original, Client, TracedProvider
from core.serving_contracts import ServingRequest
from core.serving_registry import MAIN_IDS
from core.serving_runtime.service import Service
from core.serving_runtime.runner import Runner
from core.serving_runtime.transport import Calls
from core.serving_runtime.resources import Resources
from core.unified_contracts import digest
from core.historical_evaluation_journal import load
from utils.serving_web import serving


class QuietHandler(WSGIRequestHandler):
    """Không ghi request/cookie/body vào console nghiệm thu."""
    def log(self, *args: object, **kwargs: object) -> None:
        pass


class RealHttpAcceptance(unittest.TestCase):
    def test_two_concurrent_real_providers_keep_keys_options_snapshots_and_pairing(self) -> None:
        with TemporaryDirectory() as folder:
            clock = Clock(); key = ['fixture-owner-A']; instances = []; senders = {}; release = threading.Event()
            ready = {'MWG':threading.Event(),'FPT':threading.Event()}
            def provider_factory(*args: object) -> TracedProvider:
                provider = TracedProvider(*args); instances.append(provider)
                ready[provider.points[0]['symbol']].set()
                if not release.wait(180): raise AssertionError('Không nhả được barrier test')
                return provider
            def sender_factory(secret: str) -> Sender:
                sender = Sender(clock); senders[secret] = sender; return sender
            service = Service(ROOT,state_root=Path(folder),clock=clock,provider_factory=provider_factory,sender_factory=sender_factory)
            app = Flask(__name__); app.config.update(SERVING_SERVICE=service,SERVING_API_KEY_PROVIDER=lambda:key[0]); app.register_blueprint(serving)
            server = make_server('127.0.0.1',0,app,threaded=True,request_handler=QuietHandler)
            thread = threading.Thread(target=server.serve_forever,daemon=True); thread.start()
            try:
                base = f'http://127.0.0.1:{server.server_port}'; a,b = Client(base),Client(base)
                first = spec(list(MAIN_IDS),'backtest',symbol='MWG',repeats=2).document()
                status,data,_,_ = a.call('/api/serving/v1/jobs',first,origin=base)
                self.assertEqual(status,202); aid = data['run_id']
                second = spec(['original_fix'],'analyze',symbol='FPT').document()
                second['models']['decision']['options'].update(temperature=.6,max_tokens=512)
                key[0] = 'fixture-owner-B'
                status,data,_,_ = b.call('/api/serving/v1/jobs',second,origin=base)
                self.assertEqual(status,202); bid = data['run_id']
                self.assertTrue(ready['MWG'].wait(180)); self.assertTrue(ready['FPT'].wait(180))
                # Sửa object phía caller sau POST không đổi job/config/provider đã sở hữu riêng.
                first['models']['decision']['options']['temperature'] = 1.9
                key[0] = 'fixture-config-changed-after-start'; release.set()
                for worker in service.tasks.values(): worker.join(240); self.assertFalse(worker.is_alive())
                adata = a.call('/api/serving/v1/jobs/'+aid)[1]; bdata = b.call('/api/serving/v1/jobs/'+bid)[1]
                self.assertEqual(adata['state'],'completed',adata['error']); self.assertEqual(bdata['state'],'completed',bdata['error'])
                self.assertEqual(len(adata['rows']),16); self.assertEqual(len(bdata['rows']),1)
                self.assertNotEqual(adata['cache_sha256'],bdata['cache_sha256'])
                self.assertEqual(adata['identity']['request']['models']['decision']['options']['temperature'],0)
                self.assertEqual(bdata['identity']['request']['models']['decision']['options']['temperature'],.6)
                self.assertEqual(set(senders),{'fixture-owner-A','fixture-owner-B'})
                for secret,temperature,maximum in [('fixture-owner-A',0,960),('fixture-owner-B',.6,512)]:
                    decision = [body for body in senders[secret].bodies if 'response_format' in body]
                    self.assertTrue(decision)
                    self.assertTrue(all(abs(body['temperature']-temperature)<1e-7 and body['max_tokens']==maximum for body in decision))
                mwg = next(p for p in instances if p.points[0]['symbol']=='MWG')
                fpt = next(p for p in instances if p.points[0]['symbol']=='FPT')
                self.assertEqual(mwg.shared_count,1); self.assertEqual(fpt.shared_count,1)
                self.assertEqual(len(mwg.parents),1); self.assertEqual(len(mwg.prepares),16)
                self.assertTrue(all(count==1 for count in mwg.prepares.values()))
                self.assertEqual(mwg.outcomes_count,1); self.assertEqual(fpt.outcomes_count,0)
                self.assertTrue(mwg.prefix_lengths); self.assertLessEqual(max(mwg.prefix_lengths),600)
                self.assertLess(max(mwg.prompt_lengths),6500)
                from core.causal_bridge import decision_payload
                from core.unified_contracts import SharedSnapshot
                book = Runner(service.store,service.store.reservation(aid,adata['owner_scope_sha256']),None,None,read_only=True)
                point = book.reservation['points'][0]
                snapshot = book.book.execute('shared/'+point['id'],{'point':point},None)
                shared = SharedSnapshot.create(snapshot['point'],0,snapshot['payload'],snapshot['provenance'])
                native,common = decision_payload(shared,'original_fix'),decision_payload(shared,'original_common')
                self.assertNotEqual(native['alpha_report'],common['alpha_report'])
                self.assertTrue(all(native[role]==common[role] for role in ('indicator_report','pattern_report','trend_report','sentiment_report')))
                wire = [load(path) for path in (service.store.path(aid)/'http').glob('*.json')]
                self.assertEqual(sum(row['slot'].endswith('/pattern') for row in wire),1)
                self.assertEqual(sum(row['slot'].endswith('/trend') for row in wire),1)
                self.assertEqual(b.call('/api/serving/v1/jobs/'+aid)[0],404)
                self.assertEqual(a.call('/api/serving/v1/jobs/'+bid+'/export')[0],404)
                self.assertEqual(a.call('/api/serving/v1/jobs/'+aid+'/resume',{})[0],409)
                self.assertEqual(a.call('/api/serving/v1/jobs/'+aid+'/evaluation?run_id='+bid)[0],400)
                before = sum(len(sender.bodies) for sender in senders.values())
                report = a.call('/api/serving/v1/jobs/'+aid+'/evaluation')[1]
                exported = a.call('/api/serving/v1/jobs/'+aid+'/export?format=json')[1]
                self.assertEqual(report,exported); self.assertEqual(report['evaluation_status'],'COMPLETE')
                self.assertEqual(len(report['summary']),6); self.assertEqual(len(report['accounts']),12)
                csv_raw = a.call('/api/serving/v1/jobs/'+aid+'/export?format=csv&table=predictions')[2]
                self.assertEqual(len(list(csv.DictReader(io.StringIO(csv_raw.decode('utf-8-sig'))))),12)
                self.assertEqual(sum(len(sender.bodies) for sender in senders.values()),before)
                self.assertTrue(all('fixture-owner-' not in json.dumps(data) for data in (adata,bdata,report)))
            finally:
                release.set()
                for worker in service.tasks.values(): worker.join(240)
                server.shutdown(); server.server_close(); thread.join(10)


class RestartAcceptance(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.clock = Clock(); self.sender = Sender(self.clock); self.owner = '7'*64; self.key = 'fixture-restart'
        self.service = self.fresh()
    def fresh(self) -> Service:
        return Service(ROOT,state_root=Path(self.temp.name),clock=self.clock,sender_factory=lambda _:self.sender,
                       provider_factory=Provider,resources_factory=FixtureResources)
    def test_fresh_service_resumes_stopped_slots_with_same_uuid_config_and_raw(self) -> None:
        identifier = self.service.create(spec(['original_fix','original_common'],'compare',repeats=2),self.key,self.owner,background=False)
        self.sender.on_send = lambda:self.service.store.control(identifier,True)
        self.service.work(identifier,self.key,self.owner,wait=False)
        before = self.service.result(identifier,self.owner); self.assertEqual(before['state'],'stopped')
        self.sender.on_send = None; restarted = self.fresh()
        generation = restarted.store.control(identifier)['generation']
        restarted.work(identifier,self.key,self.owner,wait=False,resume_generation=generation)
        after = restarted.result(identifier,self.owner)
        self.assertEqual(after['state'],'completed'); self.assertEqual(after['run_id'],identifier)
        self.assertEqual(after['identity_sha256'],before['identity_sha256'])
        self.assertEqual(after['rows'][0],before['rows'][0]); self.assertEqual(len(self.sender.bodies),4)
    def test_fresh_service_retains_unknown_and_never_resends_or_imputes_cash(self) -> None:
        identifier = self.service.create(spec(),self.key,self.owner,background=False)
        self.sender.actions = [TimeoutError('fixture')]
        self.service.work(identifier,self.key,self.owner,wait=False)
        restarted = self.fresh(); restarted.work(identifier,self.key,self.owner,wait=False)
        after = restarted.result(identifier,self.owner)
        self.assertEqual(after['state'],'unknown'); self.assertEqual(after['rows'],[]); self.assertEqual(len(self.sender.bodies),1)
        self.assertFalse(after['error']['retryable'])
    def test_fresh_service_replays_durable_raw_after_crash_without_new_dispatch(self) -> None:
        identifier = self.service.create(spec(),self.key,self.owner,background=False)
        reservation = self.service.store.reservation(identifier,self.owner)
        def crash(stage: str) -> None:
            if stage=='raw': raise KeyboardInterrupt('fixture')
        calls = Calls(self.service.store.path(identifier),identifier,self.service.quota,self.sender,lambda:None,clock=self.clock,hook=crash)
        with self.assertRaises(KeyboardInterrupt): Runner(self.service.store,reservation,calls,Provider(ROOT,[],spec().document()['models'],[])).tick()
        restarted = self.fresh(); restarted.work(identifier,self.key,self.owner,wait=False)
        self.assertEqual(restarted.result(identifier,self.owner)['state'],'completed'); self.assertEqual(len(self.sender.bodies),1)
    def test_fresh_service_retains_429_deadline_and_attempt_ledger(self) -> None:
        identifier = self.service.create(spec(),self.key,self.owner,background=False)
        self.sender.actions = [(429,b'{"error":"try again in 90 seconds"}',{})]
        self.service.work(identifier,self.key,self.owner,wait=False)
        before = self.service.result(identifier,self.owner); self.assertEqual(before['state'],'partial')
        restarted = self.fresh(); restarted.work(identifier,self.key,self.owner,wait=False)
        self.assertEqual(len(self.sender.bodies),1)
        self.assertEqual(restarted.result(identifier,self.owner)['retry_at'],before['retry_at'])
        self.clock.advance(100); restarted.work(identifier,self.key,self.owner,wait=False)
        self.assertEqual(restarted.result(identifier,self.owner)['state'],'completed'); self.assertEqual(len(self.sender.bodies),2)
    def test_new_owner_missing_credentials_resources_and_unsupported_models_never_dispatch(self) -> None:
        app = Flask(__name__); app.config.update(SERVING_SERVICE=self.service,SERVING_API_KEY_PROVIDER=lambda:'')
        app.register_blueprint(serving); client = app.test_client()
        self.assertEqual(client.post('/api/serving/v1/jobs',json=spec().document()).status_code,409)
        app.config['SERVING_API_KEY_PROVIDER'] = lambda:self.key
        for field,value in [('language','en'),('symbols',['AAA'])]:
            data = spec().document(); data[field] = value
            self.assertEqual(client.post('/api/serving/v1/jobs',json=data).status_code,409)
        data = spec().document(); data['models']['decision']['model'] = 'unsupported-model'
        self.assertEqual(client.post('/api/serving/v1/jobs',json=data).status_code,409)
        with patch.object(FixtureResources,'verify',side_effect=ValueError('fixture')):
            self.assertEqual(client.post('/api/serving/v1/jobs',json=spec().document()).status_code,409)
        self.assertEqual(self.sender.bodies,[])


class PublishedSupportAcceptance(unittest.TestCase):
    def test_all_522_published_windows_have_600_pit_bars_and_matching_t1_t3_calendar(self) -> None:
        import pandas as pd
        from core.unified_experiment import outcome_from_frame, validate_outcome
        resources = Resources(ROOT); resources.verify(); support = resources.document()['support']
        protocol = json.loads((ROOT/'docs/plan/week11/historical_evaluation_protocol.json').read_bytes())['payload']
        calendar = pd.read_csv(ROOT/protocol['effective_mt_bicl']['calendar']['source'],parse_dates=['Datetime']).Datetime.dt.strftime('%Y-%m-%d').tolist()
        alpha = json.loads((ROOT/'outputs/unified_integration/u06_assets_v2/frozen_alpha_manifest.json').read_bytes())
        count = 0
        for symbol in support['symbols']:
            source = alpha['causal_sources'][symbol+'/f2026_q3']['prices']
            frame = pd.DataFrame(json.loads((ROOT/source).read_bytes())); dates = frame.Datetime.tolist(); frame['Datetime'] = pd.to_datetime(frame.Datetime)
            frame[['Open','High','Low','Close']] *= 1000.
            for cutoff in support['calendar']:
                index = dates.index(cutoff); master = calendar.index(cutoff)
                self.assertGreaterEqual(index+1,600)
                self.assertEqual(dates[index:index+4],calendar[master:master+4]); self.assertEqual(len(dates[index:index+4]),4)
                point = {'id':symbol+'-'+cutoff,'symbol':symbol,'cutoff':cutoff}
                # Audit resource/oracle riêng, không đưa payoff này vào job hoặc model input.
                outcome = outcome_from_frame(point,frame,'1'*64); validate_outcome(point,outcome); count += 1
        self.assertEqual(count,522)
