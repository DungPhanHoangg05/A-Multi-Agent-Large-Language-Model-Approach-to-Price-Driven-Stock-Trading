"""Oracle kinh tế/daily NAV, common support và chống leakage trên GET evaluator mới."""
from copy import deepcopy
import csv
import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from fixtures import ROOT, Clock, Provider, Sender, Resources, spec, original, prices
from core.backtest_engine import compute_round_trip_net_return
from core.historical_evaluation_journal import save
from core.serving_runtime.service import PREVIOUS_EVALUATION_CALLER_SHA256, Service
from core.serving_runtime.runner import Runner, slot_id
from core.serving_runtime.evaluation import evaluate
from core.unified_contracts import digest
from utils.backtest_export import export_bytes


class EvaluationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.clock = Clock(); self.sender = Sender(self.clock,[original('LONG'),original('SHORT')]*4)
        self.service = Service(ROOT,state_root=Path(self.temp.name),clock=self.clock,sender_factory=lambda _:self.sender,
            provider_factory=Provider,resources_factory=Resources)
        self.owner = '7'*64; self.key = 'fixture-key'
        self.loader = patch('core.serving_runtime.evaluation.prices',side_effect=prices).start()
        self.addCleanup(patch.stopall)
    def start(self,run: bool = True) -> str:
        identifier = self.service.create(spec(),self.key,self.owner,background=False)
        if run: self.service.work(identifier,self.key,self.owner,wait=False)
        return identifier
    def test_shared_evaluator_account_cash_costs_daily_nav_and_repeat_mean(self) -> None:
        identifier = self.start(); data = self.service.evaluation(identifier,self.owner,{})
        self.assertEqual(data['evaluation_status'],'COMPLETE')
        self.assertEqual(len(data['predictions']),8); self.assertEqual(len(data['accounts']),4)
        self.assertEqual(len(data['daily_nav']),28)
        net = compute_round_trip_net_return(100000.,110000.)
        native = next(r for r in data['summary'] if r['method']=='original_fix')
        common = next(r for r in data['summary'] if r['method']=='original_common')
        self.assertAlmostEqual(native['mean_account_return_pct'],((1+net)**2-1)*100,places=10)
        self.assertEqual(common['mean_account_return_pct'],0.)
        self.assertEqual(common['mean_fee_vnd'],0.); self.assertEqual(common['mean_slippage_vnd'],0.)
        self.assertGreater(native['mean_fee_vnd'],0.); self.assertGreater(native['mean_turnover_vnd'],0.)
        self.assertIsNone(native['balanced_accuracy']); self.assertIsNone(common['mcc'])
        self.assertEqual(len(data['per_repeat']),4)
        self.assertTrue(all(r['net_return_pct']==0 for r in data['predictions'] if r['final_action']=='CASH'))
        json.dumps(data,allow_nan=False)
    def test_filter_recomputes_account_on_same_subset_and_baseline_is_paired(self) -> None:
        identifier = self.start()
        data = self.service.evaluation(identifier,self.owner,{'start_date':'2026-07-07','end_date':'2026-07-07','repeat':'0',
            'methods':'original_fix','baseline':'original_common'})
        self.assertEqual(len(data['predictions']),1); self.assertEqual(len(data['accounts']),1)
        self.assertAlmostEqual(data['summary'][0]['mean_account_return_pct'],compute_round_trip_net_return(100000,110000)*100)
        self.assertEqual(len(data['daily_nav']),4); self.assertEqual(data['coverage']['filtered_planned_slots'],1)
        self.assertEqual(data['contrasts'][0]['baseline'],'original_common')
        self.assertEqual(data['contrasts'][0]['return_difference_pp'],data['summary'][0]['mean_account_return_pct'])
        self.assertNotIn('ci95',data['contrasts'][0]); self.assertNotIn('p_value',data['contrasts'][0])
    def test_partial_stop_keeps_completed_rows_but_no_summary_nav_or_outcomes(self) -> None:
        identifier = self.start(False)
        self.sender.on_send = lambda:self.service.store.control(identifier,True)
        self.service.work(identifier,self.key,self.owner,wait=False)
        data = self.service.evaluation(identifier,self.owner,{})
        self.assertEqual(data['status'],'stopped'); self.assertEqual(data['evaluation_status'],'INCOMPLETE_JOB')
        self.assertEqual(len(data['predictions']),1); self.assertIsNone(data['predictions'][0]['label_net'])
        self.assertEqual(data['summary'],[]); self.assertEqual(data['daily_nav'],[]); self.assertEqual(data['contrasts'],[])
        self.loader.assert_not_called()
        self.sender.on_send = None; self.service.store.control(identifier,False)
        self.service.work(identifier,self.key,self.owner,wait=False)
        resumed = self.service.evaluation(identifier,self.owner,{})
        self.assertEqual(resumed['run_id'],identifier); self.assertEqual(resumed['evaluation_status'],'COMPLETE')
        self.assertEqual(len(self.sender.bodies),8)
    def test_unknown_never_becomes_cash_or_retried_by_evaluation(self) -> None:
        self.sender.actions = [TimeoutError('fixture')]
        identifier = self.start()
        for _ in range(2):
            data = self.service.evaluation(identifier,self.owner,{})
            self.assertEqual(data['status'],'unknown'); self.assertEqual(data['predictions'],[])
            self.assertEqual(data['summary'],[])
        self.assertEqual(len(self.sender.bodies),1); self.loader.assert_not_called()
    def test_outcome_before_forecast_barrier_is_rejected_on_read(self) -> None:
        identifier = self.start(False); reservation = self.service.store.reservation(identifier,self.owner)
        runner = Runner(self.service.store,reservation,None,None,read_only=True)
        point = reservation['points'][0]
        required = [slot_id(point,r,v) for r in range(2) for v in runner.plan]
        from core.unified_execution import StageBook
        book = StageBook(runner.directory/'journal',runner.doc)
        provider = Provider(ROOT,[],spec().document()['models'],[])
        book.execute('outcome/'+point['id'],{'slots':required},lambda _:provider.outcome(point))
        with self.assertRaises(ValueError): self.service.evaluation(identifier,self.owner,{})
        self.loader.assert_not_called(); self.assertEqual(self.sender.bodies,[])
    def test_invalid_or_cross_run_filters_and_evaluator_source_drift_rejected(self) -> None:
        identifier = self.start()
        for query in ({'methods':'original_fix,original_fix'},{'methods':'no_alpha'},{'symbol':'MWG'},{'repeat':'2'},
                      {'baseline':'MT_BICL'},{'start_date':'2026-01-01'},{'run_id':'other'}):
            with self.subTest(query=query),self.assertRaises(ValueError): self.service.evaluation(identifier,self.owner,query)
        sources = self.service.sources(); sources['files']['core/backtest_engine.py'] = '0'*64
        with patch.object(self.service,'sources',return_value=sources),self.assertRaises(ValueError):
            self.service.evaluation(identifier,self.owner,{})
        sources = self.service.sources(); sources['runtime']['python'] = '0.0.0'
        with patch.object(self.service,'sources',return_value=sources),self.assertRaises(ValueError):
            self.service.evaluation(identifier,self.owner,{})
    def test_completed_backtest_from_previous_caller_remains_readable(self) -> None:
        sources = self.service.sources()
        sources['files']['core/serving_runtime/service.py'] = PREVIOUS_EVALUATION_CALLER_SHA256
        with patch.object(self.service, 'sources', return_value=sources):
            identifier = self.start()
        result = self.service.evaluation(identifier, self.owner, {})
        self.assertEqual(result['evaluation_status'], 'COMPLETE')
        self.assertEqual(len(result['predictions']), 8)
    def test_raw_tampering_is_not_silently_accepted_as_success(self) -> None:
        identifier = self.start(); reservation = self.service.store.reservation(identifier,self.owner)
        point = reservation['points'][0]; slot = slot_id(point,0,'original_fix')
        from core.historical_evaluation_journal import load
        path = self.service.store.path(identifier)/'http'/(digest(slot)+'.json')
        raw = load(path); raw['rows'][0]['response'] = '{}'; save(path,raw)
        with self.assertRaises(ValueError): self.service.evaluation(identifier,self.owner,{})
    def test_json_csv_same_projection_na_zero_and_formula_escaping(self) -> None:
        data = self.service.evaluation(self.start(),self.owner,{'methods':'original_common'})
        data['predictions'][0]['fallback_reason'] = ' =1+1'
        encoded,_ = export_bytes(data,'json','predictions')
        csv_raw,_ = export_bytes(data,'csv','predictions')
        rows = list(csv.DictReader(io.StringIO(csv_raw.decode('utf-8-sig'))))
        self.assertEqual(len(rows),len(json.loads(encoded)['predictions']))
        self.assertEqual(float(rows[0]['net_return_pct']),0.)
        self.assertTrue(rows[0]['fallback_reason'].startswith("'"))
        self.assertIn('identity_sha256',rows[0]['provenance_json'])
        summary_raw,_ = export_bytes(data,'csv','summary')
        summary = next(csv.DictReader(io.StringIO(summary_raw.decode('utf-8-sig'))))
        self.assertEqual(summary['mcc'],''); self.assertEqual(float(summary['mean_account_return_pct']),0.)

    def test_duplicate_response_uuid_across_slots_is_rejected_even_with_updated_envelopes(self) -> None:
        identifier = self.start(); reservation = self.service.store.reservation(identifier,self.owner)
        runner = Runner(self.service.store,reservation,None,None,read_only=True); point = reservation['points'][0]
        from core.historical_evaluation_journal import load
        from core.prior_stage_journal import decode_output, encode_output
        first = decode_output(load(runner.book.path(slot_id(point,0,'original_fix')))['attempts'][0]['output'])
        second = slot_id(point,0,'original_common'); stage = load(runner.book.path(second))
        record = decode_output(stage['attempts'][0]['output']); raw = record['forecast']['raw']
        path = runner.directory/'http'/(digest(second)+'.json'); wire = load(path)
        wire['rows'][0]['id'] = first['forecast']['raw']['source_request_id']
        raw.update(source_request_id=wire['rows'][0]['id'],source_sha256=digest(wire['rows'][0])); save(path,wire)
        stage['attempts'][0].update(output=encode_output(record),output_sha256=digest(encode_output(record)))
        save(runner.book.path(second),stage)
        with self.assertRaisesRegex(ValueError,'Response nguồn'): self.service.evaluation(identifier,self.owner,{})
