"""Resource PIT/provider thật, request mới ngoài U09, HTTP fixture và không refit weights."""
from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import pandas as pd

from core.serving_contracts import ServingRequest
from core.serving_registry import MAIN_IDS
from core.serving_runtime.resources import Resources, START, END, MANIFEST_SHA256, default_models
from core.serving_runtime.providers import AsOfProvider
from core.serving_runtime.runner import Runner
from core.serving_runtime.service import Service
from core.serving_runtime.transport import Calls
from core.unified_contracts import SharedSnapshot
from support import ROOT, Clock, Sender, spec


class ResourceTests(unittest.TestCase):
    def test_stop_between_real_vision_nodes_resumes_without_calling_pattern_twice(self):
        clock = Clock(); sender = Sender(clock)
        with TemporaryDirectory() as folder:
            service = Service(ROOT,state_root=Path(folder),clock=clock,sender_factory=lambda _:sender)
            identifier = service.create(spec(),'fixture-private-key','7'*64,background=False)
            sender.on_send = lambda:service.store.control(identifier,True)
            service.work(identifier,'fixture-private-key','7'*64,wait=False)
            data = service.result(identifier,'7'*64)
            self.assertEqual(data['state'],'stopped')
            self.assertEqual(len(sender.bodies),1)
            self.assertEqual(data['rows'],[])
            sender.on_send = None
            service.store.control(identifier,False)
            service.work(identifier,'fixture-private-key','7'*64,wait=False)
            data = service.result(identifier,'7'*64)
            self.assertEqual(data['state'],'completed')
            self.assertEqual(len(sender.bodies),3)
            self.assertEqual(data['progress']['points_complete'],1)

    def test_manifest_actual_bindings_and_support_calendar_are_pinned(self):
        resources = Resources(ROOT)
        resources.verify()
        self.assertEqual(len(resources.document()['bindings']),188)
        self.assertEqual(len(resources.document()['support']['symbols']),9)
        self.assertEqual(len(resources.document()['support']['calendar']),58)
        self.assertFalse(resources.document()['support']['live_latest_supported'])
        for field, value in (('start_date','2026-11-13'),('symbols',['AAA']),('language','fr')):
            request = spec().document(); request[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError): resources.points(request)
        request = spec().document(); request.update(mode='backtest',start_date=START,end_date=END)
        points = resources.points(request)
        self.assertLessEqual(len(points),30)
        calendar = resources.document()['support']['calendar']
        self.assertEqual([p['cutoff'] for p in points],calendar[::3])

    def test_modified_resource_is_rejected_without_refit_or_hash_update(self):
        from core.serving_runtime.resources import decode_manifest
        with self.assertRaises(ValueError): decode_manifest(b'{"version":"forged"}')
        resources = Resources(ROOT)
        with patch('core.serving_runtime.resources.binding',return_value={'bytes':0,'sha256':'0'*64}):
            with self.assertRaises(ValueError): resources.verify()

    def test_ood_bank_fallback_is_declared_and_fact_anchor_accepts_nine_symbol_scope(self):
        request = spec(list(MAIN_IDS),'compare',symbol='BHN')
        point = Resources(ROOT).points(request.document())[0]
        provider = AsOfProvider(ROOT,[point],request.document()['models'],list(MAIN_IDS))
        provider.validate_point(point)
        payload = {'stock_name':'BHN','as_of_date':point['cutoff'],'time_frame':'1d','language':'vi','is_backtest':True,
                   **{name+'_report':'Báo cáo synthetic.' for name in ('indicator','pattern','trend','alpha','sentiment')}}
        payload.update(trend_report='**Hướng xu hướng:** Tăng',pattern_report='**Thiên lệch dự báo:** Tăng',
                       indicator_report='**Đồng thuận chủ đạo:** Tăng',alpha_factors=[{'signal':'TĂNG'}],
                       sentiment_data={'main_sentiment':{'avg_score':None}})
        snapshot = SharedSnapshot.create(point,0,payload,{'source_sha256':'1'*64,'upstream_sha256':'2'*64,
                                                       'price_end':point['cutoff'],'news_dates':[]})
        for variant in ('bayesian_v1','C2','A_tp_pool','B_semantic'):
            prepared = provider.prepare(variant,snapshot,{},0)
            provider.validate(variant,snapshot,prepared,0)
            self.assertIsNone(prepared['request'])
            self.assertEqual(prepared['trace']['reason'],'NO_SAME_SYMBOL_FROZEN_BANK_OOD')
        anchored = provider.prepare('Fact_Anchor',snapshot,{},0)
        provider.validate('Fact_Anchor',snapshot,anchored,0)
        self.assertEqual(anchored['aux']['packet']['point_id'],point['id'])
        self.assertIsNotNone(anchored['request'])

    def test_all_six_actual_adapters_new_query_one_shared_snapshot_and_no_query_payoff(self):
        clock = Clock()
        sender = Sender(clock)
        with TemporaryDirectory() as folder:
            request = spec(list(MAIN_IDS),'compare',symbol='MWG')
            service = Service(ROOT,state_root=Path(folder),clock=clock)
            identifier = service.create(request,'fixture-private-key','7'*64,background=False)
            reservation = service.store.reservation(identifier,'7'*64)
            provider = AsOfProvider(ROOT,reservation['points'],request.document()['models'],list(MAIN_IDS))
            point = reservation['points'][0]
            with self.assertRaises(ValueError): provider.outcome(point)
            # Thay tương lai trong RAM không đổi prefix query, source trên đĩa vẫn khóa.
            prefix = provider.prefix(point)
            mask = provider.prices[point['symbol']].Datetime > pd.Timestamp(point['cutoff'])
            provider.prices[point['symbol']].loc[mask,['Open','High','Low','Close']] *= 1000
            pd.testing.assert_frame_equal(prefix,provider.prefix(point))
            provider.validate_point(point)
            resources = Resources(ROOT)
            calls = Calls(service.store.path(identifier),identifier,service.quota,sender,lambda:service._guard(reservation,resources),clock=clock)
            runner = Runner(service.store,reservation,calls,provider)
            with patch.object(provider,'outcome',side_effect=AssertionError('Không đọc payoff trong compare')):
                runner.tick()
            service.store.status(identifier,'completed')
            data = service.result(identifier,'7'*64)
            self.assertEqual(data['state'],'completed')
            self.assertEqual(len(data['rows']),8)
            self.assertEqual({r['requested_id'] for r in data['rows']},set(data['execution_plan']))
            self.assertTrue(all(r['net_return_pct'] is None for r in data['rows']))
            self.assertIsNotNone(next(r for r in data['rows'] if r['requested_id']=='MT_BICL')['raw_prediction'])
            self.assertEqual(len(data['snapshots']),1)
            self.assertTrue(all(len(body['messages'][0]['content']) < 6500 for body in sender.bodies if 'response_format' in body))
            self.assertTrue((service.store.path(identifier)/'journal/images'/point['id']/'pattern.png').is_file())
            before = len(sender.bodies)
            runner.tick()
            self.assertEqual(len(sender.bodies),before)
            with self.assertRaises(ValueError): provider.outcome(point)


if __name__ == '__main__':
    unittest.main()
