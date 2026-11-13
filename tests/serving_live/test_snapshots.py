"""Rào PIT của dữ liệu mới nhất: không future, không tin undated, không tự tạo payoff."""
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import pandas as pd

from support import prices, news, request
from core.serving_live.service import LiveRequest
from core.serving_live.snapshots import Snapshots, ZONE


class SnapshotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.calls = []
        def fetch(symbol: str) -> pd.DataFrame:
            self.calls.append(symbol); return prices(symbol)
        self.source = Snapshots(Path(self.temp.name),prices=fetch,news=news,
            now=lambda:datetime(2026,11,13,10,tzinfo=ZONE))
        self.owner = '7'*64

    def test_capture_owner_hash_undated_news_and_reload_without_refetch(self) -> None:
        summary = self.source.capture('MWG',self.owner)
        self.assertEqual(summary['cutoff'],'2026-11-12'); self.assertEqual(summary['news_articles'],3)
        record = self.source.read(summary['snapshot_id'],self.owner)
        self.assertEqual(record['prices']['Datetime'][-1],'2026-11-12')
        with self.assertRaises(PermissionError): self.source.read(summary['snapshot_id'],'8'*64)
        self.assertEqual(self.calls,['MWG','VNINDEX'])
        self.source.read(summary['snapshot_id'],self.owner)
        self.assertEqual(self.calls,['MWG','VNINDEX'])
        path = self.source.path(summary['snapshot_id']); raw = path.read_bytes()
        path.write_bytes(raw.replace(b'2026-11-12',b'2026-11-11'))
        with self.assertRaises(ValueError): self.source.read(summary['snapshot_id'],self.owner)

    def test_incomplete_current_session_is_excluded_before_close(self) -> None:
        self.source.now = lambda:datetime(2026,11,12,14,tzinfo=ZONE)
        self.assertEqual(self.source.capture('MWG',self.owner)['cutoff'],'2026-11-11')
        self.source.now = lambda:datetime(2026,11,12,16,tzinfo=ZONE)
        self.assertEqual(self.source.capture('MWG',self.owner)['cutoff'],'2026-11-12')

    def test_future_prices_news_and_stale_or_short_sources_raise(self) -> None:
        self.source.now = lambda:datetime(2026,11,11,16,tzinfo=ZONE)
        with self.assertRaises(ValueError): self.source.capture('MWG',self.owner)
        self.source.now = lambda:datetime(2026,11,13,16,tzinfo=ZONE)
        self.source.news = lambda *_:[{'date_parsed':'2026-11-13','numeric_score':.1,'scorer':'lexicon'}]
        with self.assertRaises(ValueError): self.source.capture('MWG',self.owner)
        self.source.news = news
        self.source.prices = lambda symbol:prices(symbol).tail(100)
        with self.assertRaises(ValueError): self.source.capture('MWG',self.owner)
        self.source.prices = prices; self.source.now = lambda:datetime(2026,12,1,16,tzinfo=ZONE)
        with self.assertRaises(ValueError): self.source.capture('MWG',self.owner)

    def test_contract_refuses_backtest_en_intraday_and_path_ids(self) -> None:
        base = request('a'*64,'2026-11-12',['MT_BICL'])
        self.assertEqual(LiveRequest.create(base).document()['data_source'],'live')
        for field,value in [('mode','backtest'),('language','fr'),('timeframe','15m')]:
            changed = deepcopy(base); changed['request'][field] = value
            with self.assertRaises(ValueError): LiveRequest.create(changed)
        with self.assertRaises(ValueError): self.source.path('../outside')
        with self.assertRaises(ValueError): self.source.capture('AAA',self.owner)
