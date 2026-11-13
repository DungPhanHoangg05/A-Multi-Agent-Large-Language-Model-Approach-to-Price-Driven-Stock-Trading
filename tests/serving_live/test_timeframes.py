"""Kiểm capture đa khung/PIT và sáu phương pháp thực thi từ lựa chọn intraday."""
from copy import deepcopy
from datetime import datetime
import importlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import pandas as pd

from support import ROOT,Clock,Sender,prices,news,charts,request
from core.serving_live.snapshots import Snapshots,ZONE
from core.serving_live.service import LiveRequest,LiveService
from core.serving_live.timeframes import TIMEFRAMES,chart_frame,extend_daily
from core.serving_registry import MAIN_IDS


class CaptureTimeframes(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.store = Snapshots(Path(self.temp.name),prices=prices,news=news,charts=charts,
            now=lambda:datetime(2026,11,13,10,tzinfo=ZONE))
        self.owner = '7'*64

    def test_all_seven_timeframes_keep_actual_chart_and_daily_target_context(self) -> None:
        for timeframe in TIMEFRAMES:
            with self.subTest(timeframe=timeframe):
                captured = self.store.capture_timeframe('MWG',timeframe,self.owner)
                record = self.store.read(captured['snapshot_id'],self.owner)
                self.assertEqual(captured['chart_timeframe'],timeframe)
                self.assertEqual(record['cutoff'],'2026-11-13')
                self.assertTrue(record['daily_provisional']); self.assertGreaterEqual(len(record['prices']['Close']),600)
                self.assertTrue(all(pd.Timestamp(value)<=pd.Timestamp('2026-11-13 10:00') for value in record['chart']['Datetime']))
                self.assertEqual(record['prices']['Datetime'][-1],'2026-11-13')

    def test_future_intraday_bars_and_missing_opening_session_raise_before_model(self) -> None:
        future = charts('MWG','5m'); future.loc[future.index[-1],'Datetime'] = pd.Timestamp('2026-11-13 10:05')
        with self.assertRaises(ValueError): chart_frame(future,datetime(2026,11,13,10,tzinfo=ZONE))
        late = charts('MWG','5m'); late = late.loc[late.Datetime > '2026-11-13 09:30']
        with self.assertRaises(ValueError): extend_daily(prices('MWG'),late,'2026-11-13')

    def test_request_binds_chart_timeframe_and_rejects_unknown_or_backtest(self) -> None:
        base = request('a'*64,'2026-11-13',['MT_BICL'])
        body = {**base,'version':'variant_serving_timeframe_v1','chart_timeframe':'5m'}
        self.assertEqual(LiveRequest.create(body).document()['chart_timeframe'],'5m')
        for value in ('1s','garbage'):
            with self.assertRaises(ValueError): LiveRequest.create({**body,'chart_timeframe':value})
        changed = deepcopy(body); changed['request']['mode'] = 'backtest'
        with self.assertRaises(ValueError): LiveRequest.create(changed)

    def test_chart_daily_currency_mismatch_is_not_silently_rescaled(self) -> None:
        def wrong_units(symbol: str, timeframe: str):
            result = charts(symbol,timeframe)
            result[['Open','High','Low','Close']] *= 1000.
            return result
        # Daily đã có phiên query để kiểm cả trường hợp không phải tổng hợp provisional.
        self.store.prices = lambda symbol:prices(symbol)
        self.store.charts = wrong_units
        self.store.now = lambda:datetime(2026,11,12,16,tzinfo=ZONE)
        def visible(symbol: str, timeframe: str):
            result = wrong_units(symbol,timeframe)
            return result.loc[result.Datetime < '2026-11-13']
        self.store.charts = visible
        with self.assertRaises(ValueError): self.store.capture_timeframe('MWG','5m',self.owner)
        forming = wrong_units('MWG','5m')
        with self.assertRaises(ValueError): extend_daily(prices('MWG'),forming,'2026-11-13')


class TimeframeProviders(unittest.TestCase):
    def test_api_capture_and_preflight_bind_owner_and_timeframe_before_dispatch(self) -> None:
        from core.serving_runtime.service import Service
        with TemporaryDirectory() as folder,patch('core.realtime_loader.get_all_symbols_realtime',return_value=[]):
            web = importlib.import_module('web_interface')
            clock = Clock(); store = Snapshots(Path(folder)/'inputs',prices=prices,news=news,charts=charts,
                now=lambda:datetime(2026,11,13,10,tzinfo=ZONE))
            backend = LiveService(ROOT,state_root=Path(folder)/'live',snapshots=store,clock=clock)
            asof = Service(ROOT,state_root=Path(folder)/'asof',clock=clock)
            with patch.dict(web.app.config,{'SERVING_SERVICE':asof,'SERVING_LIVE_SERVICE':backend,'SERVING_API_KEY_PROVIDER':lambda:'fixture'}):
                client = web.app.test_client()
                captured = client.post('/api/serving/live/v1/snapshot',json={'symbol':'MWG','timeframe':'1h'})
                self.assertEqual(captured.status_code,200)
                data = captured.get_json()
                body = request(data['snapshot_id'],data['cutoff'],['C2'])
                body.update(version='variant_serving_timeframe_v1',chart_timeframe='1h')
                self.assertTrue(client.post('/api/serving/live/v1/preflight',json=body).get_json()['run_enabled'])
                self.assertEqual(web.app.test_client().post('/api/serving/live/v1/preflight',json=body).status_code,404)
                mismatch = {**body,'chart_timeframe':'5m'}
                checked = client.post('/api/serving/live/v1/preflight',json=mismatch).get_json()
                self.assertFalse(checked['run_enabled']); self.assertEqual(backend.tasks,{})

    def test_monthly_and_hourly_roles_use_chosen_bars_and_daily_alpha_without_mutating_parent(self) -> None:
        from core.serving_live.timeframe_provider import TimeframeProvider
        provider = object.__new__(TimeframeProvider)
        provider.points = [{'symbol':'MWG','cutoff':'2026-11-12'}]
        provider.prefix = lambda _:prices('MWG')
        for timeframe in ('1h','1mo'):
            state = {'time_frame':timeframe,'kline_data':{'Close':[1.,2.]},'point_in_time_df':prices('MWG')}
            technical = provider.role_state('indicator',state)
            alpha = provider.role_state('full',state)
            self.assertEqual(technical['time_frame'],timeframe)
            self.assertEqual(alpha['time_frame'],'1d'); self.assertEqual(len(alpha['kline_data']['Close']),45)
            self.assertEqual(state['time_frame'],timeframe); self.assertEqual(state['kline_data']['Close'],[1.,2.])

    def test_each_version_daily_agents_original_layout_and_bicl_with_single_upstream_and_no_payoff(self) -> None:
        with TemporaryDirectory() as folder:
            clock = Clock(); store = Snapshots(Path(folder)/'inputs',prices=prices,news=news,charts=charts,
                now=lambda:datetime(2026,11,13,10,tzinfo=ZONE))
            owner = '7'*64; captured = store.capture_timeframe('MWG','1d',owner)
            senders = []; providers = []
            def sender(key: str):
                result = Sender(clock); senders.append(result); return result
            service = LiveService(ROOT,state_root=Path(folder)/'state',snapshots=store,clock=clock,sender_factory=sender)
            original_provider = service.provider
            def provider(reservation: dict):
                result = original_provider(reservation); providers.append(result); return result
            service.provider = provider
            with patch('core.realtime_loader.get_all_symbols_realtime',return_value=[]): web = importlib.import_module('web_interface')
            for variant in MAIN_IDS:
                with self.subTest(variant=variant):
                    body = request(captured['snapshot_id'],captured['cutoff'],[variant])
                    body.update(version='variant_serving_timeframe_v1',chart_timeframe='1d')
                    spec = LiveRequest.create(body)
                    identifier = service.create(spec,'fixture',owner,background=False)
                    from core.serving_live.progress import agent_progress
                    reservation = service.store.reservation(identifier,owner)
                    samples = []
                    service.sender_factory = lambda key: sender_with_progress(key)
                    def sender_with_progress(key):
                        result = sender(key)
                        result.on_send = lambda: samples.append(agent_progress(service.store,reservation))
                        return result
                    service.work(identifier,'fixture',owner,wait=False)
                    result = service.result(identifier,owner)
                    self.assertEqual(result['state'],'completed',result.get('error'))
                    self.assertEqual(result['requested_ids'],[variant])
                    self.assertEqual(result['identity']['request']['chart_timeframe'],'1d')
                    self.assertEqual(set(result['agent_progress'].values()),{'complete'})
                    self.assertTrue(any(sample['pattern']=='running' for sample in samples))
                    self.assertTrue(any(sample['trend']=='running' for sample in samples))
                    if next(row for row in result['rows'] if row['requested_id']==variant)['raw_prediction'] is not None:
                        self.assertTrue(any(sample['decision']=='running' for sample in samples))
                    self.assertTrue(all(row['net_return_pct'] is None for row in result['rows']))
                    self.assertEqual(result['outcome_points'],0)
                    self.assertEqual(result['realtime_chart'],store.read(captured['snapshot_id'])['chart'])
                    self.assertEqual(sum('response_format' not in body for body in senders[-1].bodies),2)
                    state = providers[-1].state('MWG','2026-11-13')
                    self.assertEqual(state['time_frame'],'1d')
                    self.assertEqual(providers[-1].role_state('full',state)['time_frame'],'1d')
                    self.assertEqual(state['kline_data'],result['realtime_chart'])
                    self.assertTrue(all(detail['context']['trace']['live_input']['chart_timeframe']=='1d' for detail in result['policy_details'].values()))
                    with patch.dict(web.app.config,{'SERVING_LIVE_SERVICE':service,'SERVING_SERVICE':service}):
                        # GET shell không thực thi model; cookie owner API được kiểm ở các suite riêng.
                        self.assertEqual(web.app.test_client().get('/output?serving_run='+identifier+'&serving_source=live').status_code,200)
                        with patch('utils.serving_web.owner',return_value=(owner,None)):
                            client = web.app.test_client()
                            count = len(senders[-1].bodies)
                            for language in ('vi','en'):
                                response = client.get('/output?serving_run='+identifier+'&serving_source=live&presentation=analysis&lang='+language)
                                self.assertEqual(response.status_code,200,response.get_data(as_text=True)[-1000:])
                                raw = response.get_data(as_text=True)
                                self.assertIn('legacy_output.css',raw); self.assertIn('daily_output.js',raw)
                                self.assertNotIn('js/analysis/result.js',raw); self.assertNotIn('/api/images/',raw)
                                self.assertEqual('bicl-panel' in raw,variant!='original_fix')
                            self.assertEqual(count,len(senders[-1].bodies))
                        self.assertEqual(web.app.test_client().get('/output?serving_run='+identifier+'&serving_source=live&presentation=analysis').status_code,404)
