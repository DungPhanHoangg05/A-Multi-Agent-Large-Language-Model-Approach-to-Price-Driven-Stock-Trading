"""Job isolation, PIT/barrier, recovery/UNKNOWN và quota trên đường serving mới."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import threading
import unittest
from unittest.mock import patch

from core.groq_pacing import reset_seconds
from core.historical_evaluation_journal import load, save
from core.serving_runtime.service import Service
from core.serving_runtime.transport import Calls, retry_until
from core.serving_runtime.quota import Quota, Waiting, Unknown, Failed
from core.serving_runtime.resources import Resources, START, END, default_models
from core.serving_contracts import ServingRequest
from core.unified_contracts import digest
from support import ROOT, Clock, Provider, Sender, FixtureResources, spec, original


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.clock = Clock()
        self.sender = Sender(self.clock)
        Provider.instances.clear()
        self.service = Service(ROOT,state_root=Path(self.temp.name),clock=self.clock,provider_factory=Provider,
            sender_factory=lambda _:self.sender,resources_factory=FixtureResources)
        self.owner = '7'*64
    def create(self, request=None):
        return self.service.create(request or spec(),'fixture-private-key',self.owner,background=False)
    def work(self, identifier):
        self.service.work(identifier,'fixture-private-key',self.owner,wait=False)
        return self.service.result(identifier,self.owner)

    def test_native_common_repeats_share_one_upstream_and_resume_no_new_http(self):
        identifier = self.create(spec(['original_fix','original_common'],'compare',repeats=3))
        data = self.work(identifier)
        self.assertEqual(data['state'],'completed')
        self.assertEqual(data['progress']['decision_slots_complete'],6)
        self.assertEqual(Provider.instances[0].shared_count,1)
        self.assertEqual(len(set(Provider.instances[0].payload_hashes)),1)
        self.assertEqual(len(self.sender.bodies),6)
        self.assertTrue(all(r['net_return_pct'] is None for r in data['rows']))
        self.assertEqual(Provider.instances[0].outcome_count,0)
        again = self.work(identifier)
        self.assertEqual(again['identity_sha256'],data['identity_sha256'])
        self.assertEqual(len(self.sender.bodies),6)
        self.assertEqual(Provider.instances[-1].shared_count,0)

    def test_unknown_timeout_is_not_cash_or_blind_retry(self):
        self.sender.actions = [TimeoutError('fixture-private-key')]
        identifier = self.create()
        data = self.work(identifier)
        self.assertEqual(data['state'],'unknown')
        self.assertEqual(data['rows'],[])
        self.assertEqual(data['error']['code'],'UNKNOWN_ATTEMPT')
        self.assertFalse(data['error']['retryable'])
        self.work(identifier)
        self.assertEqual(len(self.sender.bodies),1)
        self.assertNotIn('fixture-private-key',json.dumps(data))

    def test_rate_limit_wait_resumes_same_slot_without_repeating_upstream(self):
        self.sender.actions = [(429,b'{"error":"Please try again in 90 seconds"}',{})]
        identifier = self.create()
        data = self.work(identifier)
        self.assertEqual(data['state'],'partial')
        self.assertGreaterEqual(data['retry_at'],self.clock()+90)
        self.assertEqual(data['rows'],[])
        self.clock.advance(100)
        data = self.work(identifier)
        self.assertEqual(data['state'],'completed')
        self.assertEqual(len(self.sender.bodies),2)
        self.assertEqual(Provider.instances[-1].shared_count,0)

    def test_stopped_job_keeps_complete_slots_and_resumes_without_duplicates(self):
        identifier = self.create(spec(['original_fix','original_common'],'compare'))
        self.sender.on_send = lambda:self.service.store.control(identifier,True)
        data = self.work(identifier)
        self.assertEqual(data['state'],'stopped')
        self.assertEqual(len(data['rows']),1)
        self.sender.on_send = None
        self.service.store.control(identifier,False)
        data = self.work(identifier)
        self.assertEqual(data['state'],'completed')
        self.assertEqual(len(self.sender.bodies),2)
        self.assertEqual(len(data['rows']),2)

    def test_invalid_output_repair_and_lifetime_cap_never_fabricate_result(self):
        malformed = (200,b'{"choices":[{"message":{"content":"{bad"}}],"usage":{"total_tokens":20}}',{})
        self.sender.actions = [malformed]*3
        identifier = self.create()
        data = self.work(identifier)
        self.assertEqual(data['state'],'failed')
        self.assertEqual(data['rows'],[])
        self.assertEqual(len(self.sender.bodies),3)
        self.assertGreater(len(self.sender.bodies[1]['messages'][0]['content']),len(self.sender.bodies[0]['messages'][0]['content']))
        self.work(identifier)
        self.assertEqual(len(self.sender.bodies),3)

    def test_crash_after_raw_replays_response_without_new_dispatch(self):
        identifier = self.create()
        reservation = self.service.store.reservation(identifier,self.owner)
        from core.serving_runtime.runner import Runner
        provider = Provider(ROOT,reservation['points'],spec().document()['models'],['original_fix'])
        def crash(stage):
            if stage == 'raw':
                raise KeyboardInterrupt('synthetic crash')
        calls = Calls(self.service.store.path(identifier),identifier,self.service.quota,self.sender,lambda:None,clock=self.clock,hook=crash)
        with self.assertRaises(KeyboardInterrupt):
            Runner(self.service.store,reservation,calls,provider).tick()
        self.assertEqual(len(self.sender.bodies),1)
        data = self.work(identifier)
        self.assertEqual(data['state'],'completed')
        self.assertEqual(len(self.sender.bodies),1)

    def test_backtest_uses_oracle_after_all_forecasts_and_cash_stays_zero(self):
        self.sender.actions = [original('SHORT'),original('LONG')]
        identifier = self.create(spec(['original_fix','original_common'],'backtest'))
        data = self.work(identifier)
        self.assertEqual(data['state'],'completed')
        self.assertEqual(data['outcome_points'],1)
        self.assertEqual(data['rows'][0]['net_return_pct'],0.)
        from core.backtest_engine import compute_round_trip_net_return
        self.assertAlmostEqual(data['rows'][1]['net_return_pct'],float(compute_round_trip_net_return(100.,110.))*100)
        self.assertEqual(Provider.instances[0].outcome_count,1)

    def test_failure_before_all_forecasts_does_not_open_outcome(self):
        self.sender.actions = [original(),TimeoutError()]
        identifier = self.create(spec(['original_fix','original_common'],'backtest'))
        data = self.work(identifier)
        self.assertEqual(data['state'],'unknown')
        self.assertEqual(len(data['rows']),1)
        self.assertIsNone(data['rows'][0]['net_return_pct'])
        self.assertEqual(Provider.instances[0].outcome_count,0)

    def test_source_tamper_and_wrong_credentials_do_not_dispatch_or_change_identity(self):
        identifier = self.create()
        with patch('core.unified_experiment.source_identity',return_value={'changed':'1'*64}):
            data = self.work(identifier)
        self.assertEqual(data['error']['code'],'INTEGRITY_FAILURE')
        self.assertEqual(len(self.sender.bodies),0)
        with self.assertRaises(ValueError): self.service.start(identifier,'other-key',self.owner)
        with self.assertRaises(PermissionError): self.service.result(identifier,'8'*64)

    def test_queued_get_is_read_only_and_does_not_load_provider_or_secret(self):
        identifier = self.create()
        folder = self.service.store.path(identifier)
        before = {str(p):p.read_bytes() for p in folder.rglob('*') if p.is_file()}
        data = self.service.result(identifier,self.owner)
        self.assertEqual(data['state'],'queued')
        self.assertEqual(Provider.instances,[])
        self.assertEqual(before,{str(p):p.read_bytes() for p in folder.rglob('*') if p.is_file()})
        self.assertNotIn('fixture-private-key',json.dumps(data))

    def test_completed_response_tamper_is_rejected_by_read_only_status(self):
        identifier = self.create()
        self.work(identifier)
        path = next((self.service.store.path(identifier)/'http').glob('*.json'))
        wire = load(path); wire['rows'][0]['response'] = '{}'; save(path,wire)
        with self.assertRaises(ValueError): self.service.result(identifier,self.owner)

    def test_body_drift_cannot_be_swallowed_by_legacy_agent_as_text_fallback(self):
        identifier = self.create()
        self.work(identifier)
        path = next((self.service.store.path(identifier)/'http').glob('*.json'))
        wire = load(path); row = wire['rows'][0]
        calls = Calls(self.service.store.path(identifier),identifier,self.service.quota,self.sender,lambda:None,clock=self.clock)
        body = deepcopy(row['body']); body['messages'][0]['content'] += ' drift'
        with self.assertRaises(Failed): calls.call(row['slot'],body,row['attempt'])
        self.assertEqual(len(self.sender.bodies),1)

    def test_direct_worker_entry_also_enforces_credential_identity(self):
        identifier = self.create()
        self.service.work(identifier,'wrong-key',self.owner,wait=False)
        self.assertEqual(self.service.result(identifier,self.owner)['state'],'failed')
        self.assertEqual(len(self.sender.bodies),0)

    def test_stop_generation_prevents_resume_from_erasing_new_stop(self):
        identifier = self.create()
        generation = self.service.store.control(identifier)['generation']
        self.service.store.control(identifier,True)
        self.service.work(identifier,'fixture-private-key',self.owner,wait=False,resume_generation=generation)
        self.assertEqual(self.service.result(identifier,self.owner)['state'],'stopped')
        self.assertEqual(len(self.sender.bodies),0)


class QuotaTests(unittest.TestCase):
    def test_provider_reset_supports_milliseconds_and_compound_durations(self):
        self.assertAlmostEqual(reset_seconds("12ms"), .012)
        self.assertAlmostEqual(reset_seconds("1m2s34ms"), 62.034)
        self.assertEqual(reset_seconds("24h"), 86400.)
        self.assertIsNone(reset_seconds("unparseable"))
        row = {"status": 200, "completed_at": 100., "response": "{}", "headers": {
            "x-ratelimit-remaining-requests": "0", "x-ratelimit-reset-requests": "12ms"}}
        self.assertAlmostEqual(retry_until(row, 0), 100.112)

    def test_repairs_only_legacy_deadline_supported_by_latest_raw(self):
        """Hết mốc ms đã ghi thì cho tiếp tục, giữ nguyên lượt và quota thật."""
        with TemporaryDirectory() as folder:
            clock = Clock()
            ledger = Quota(Path(folder) / "luna.sqlite3", clock, limits=None)
            ledger.reserve("last", "followup", 1000)
            observed_at = clock()
            headers = {"x-ratelimit-remaining-requests": "4999", "x-ratelimit-reset-requests": "12ms",
                       "x-ratelimit-remaining-tokens": "1", "x-ratelimit-reset-tokens": "30s"}
            with patch("core.groq_pacing.reset_seconds", side_effect=lambda v: None if v.endswith("ms") else 30.):
                ledger.observe("last", headers, observed_at)
            ledger.finish("last", "200", 150)
            with ledger.connect() as db:
                db.execute("UPDATE headroom SET remaining=0 WHERE kind='requests'")
            clock.advance(1)
            row = {"id": "last", "status": 200, "completed_at": observed_at, "headers": headers}
            with self.assertRaises(Waiting) as blocked:
                ledger.reserve("next", "followup", 1000)
            self.assertAlmostEqual(blocked.exception.until, observed_at + 86400.1)
            self.assertEqual(ledger.repair_millisecond_deadline("other", row), [])
            self.assertEqual(ledger.repair_millisecond_deadline("followup", row), ["requests"])
            self.assertEqual(ledger.attempts("followup"), 1)
            with self.assertRaises(Waiting) as token_wait:
                ledger.reserve("next", "followup", 1000)
            self.assertAlmostEqual(token_wait.exception.until, observed_at + 30.1)
            clock.advance(31)
            ledger.reserve("next", "followup", 1000)
            self.assertEqual(ledger.attempts("followup"), 2)

    def test_provider_remaining_headers_lower_admission_and_replay_never_restores_quota(self):
        with TemporaryDirectory() as folder:
            clock = Clock(); quota = Quota(Path(folder)/'quota.sqlite3',clock)
            quota.reserve('one','job',1000)
            headers = {'x-ratelimit-remaining-tokens':'1200','x-ratelimit-reset-tokens':'60s'}
            quota.observe('one',headers,clock())
            with self.assertRaises(Waiting): quota.reserve('two','other',2000)
            quota.reserve('two','other',1000)
            quota.observe('one',headers,clock())
            with self.assertRaises(Waiting): quota.reserve('three','other',1000)
    def test_global_pool_across_instances_models_and_keys_and_unknown_reserve(self):
        with TemporaryDirectory() as folder:
            clock = Clock()
            path = Path(folder)/'quota.sqlite3'
            first, second = Quota(path,clock),Quota(path,clock)
            self.assertEqual(first.credential_scope('key-A'),second.credential_scope('key-A'))
            self.assertNotEqual(first.credential_scope('key-A'),second.credential_scope('key-B'))
            first.reserve('a','job-A',5000)
            with self.assertRaises(Waiting): second.reserve('b','job-B',5000)
            first.finish('a','200',0)
            with self.assertRaises(Waiting): second.reserve('b','job-B',5000)
            clock.advance()
            second.reserve('b','job-B',5000)
            self.assertEqual(first.attempts('job-B'),1)

    def test_retry_headers_and_message_wait_are_not_capped_at_sixty_seconds(self):
        row = {'status':429,'completed_at':100.,'response':'Please try again in 120 seconds', 'headers':{'retry-after':'180'}}
        self.assertEqual(retry_until(row,0),280.)
        row['headers'] = {'retry-after':'Thu, 01 Jan 1970 00:10:00 GMT'}
        self.assertEqual(retry_until(row,0),600.)
        row.update(status=200,response='{"justification":"try again in 999999 seconds"}',headers={})
        self.assertEqual(retry_until(row,0),0.)


if __name__ == '__main__':
    unittest.main()
