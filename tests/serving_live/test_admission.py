"""Ledger API dùng chung và biên loader mới: không nhân đôi quota khi chuyển nguồn."""
import importlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from support import ROOT, Clock, prices
from core.serving_live.service import LiveService
from core.serving_live.snapshots import market_prices, market_news
from core.serving_runtime.service import Service


class AdmissionTests(unittest.TestCase):
    def test_default_live_api_shares_asof_admission_ledger_and_credential_scope(self) -> None:
        from utils import serving_live_web
        with TemporaryDirectory() as folder,patch('core.realtime_loader.get_all_symbols_realtime',return_value=[]):
            web = importlib.import_module('web_interface')
            clock = Clock()
            asof = Service(ROOT,state_root=Path(folder)/'asof',clock=clock)
            live = LiveService(ROOT,state_root=Path(folder)/'live',clock=clock)
            serving_live_web.default_service.cache_clear()
            self.addCleanup(serving_live_web.default_service.cache_clear)
            with web.app.app_context(),patch.dict(web.app.config,{'SERVING_SERVICE':asof}),patch.object(serving_live_web,'LiveService',return_value=live):
                backend = serving_live_web.default_service()
            self.assertIs(backend.quota,asof.quota)
            self.assertEqual(backend.quota.credential_scope('fixture-key'),asof.quota.credential_scope('fixture-key'))
            self.assertNotEqual(backend.store.root,asof.store.root)

    def test_market_loader_requests_daily_long_history_without_short_cache(self) -> None:
        expected = prices('MWG')
        with patch('core.realtime_loader.fetch_realtime_ohlcv',return_value=(expected,'')) as fetch:
            self.assertIs(market_prices('MWG'),expected)
        self.assertEqual(fetch.call_args.args,('MWG','1d'))
        self.assertGreaterEqual(fetch.call_args.kwargs['tail'],600)
        self.assertFalse(fetch.call_args.kwargs['use_cache'])

    def test_market_loader_failure_never_substitutes_frozen_prices(self) -> None:
        import pandas as pd
        with patch('core.realtime_loader.fetch_realtime_ohlcv',return_value=(pd.DataFrame(),'fixture')):
            with self.assertRaises(ValueError): market_prices('MWG')

    def test_live_news_maps_actual_scorer_ids_and_preserves_original_provenance(self) -> None:
        from core.historical_evaluation_data import FrozenNews
        rows = [{'date_parsed':'2026-11-09','title':'fixture'}]*3+[{'date_parsed':None},{'date_parsed':'2026-11-13'}]
        scored = [{'date_parsed':'2026-11-09','numeric_score':.2,'scorer':name}
                  for name in ('5CD-AI/Vietnamese-Sentiment-visobert','viquant-lexicon-v1','viquant-lexicon-v1')]
        with patch('data_manager.sentiment_cache._crawl_articles_full',return_value=rows),patch('data_manager.sentiment_cache._score_articles',return_value=scored) as score:
            result = market_news('MWG','2026-11-12')
        self.assertEqual(len(score.call_args.args[0]),3)
        self.assertEqual([row['scorer'] for row in result],['visobert','lexicon','lexicon'])
        self.assertEqual(result[0]['scorer_source'],'5CD-AI/Vietnamese-Sentiment-visobert')
        data,_ = FrozenNews({'MWG':result}).get_sentiment_at('MWG','2026-11-12')
        self.assertFalse(data['is_unavailable']); self.assertEqual(data['verified_article_count'],3)

    def test_live_news_unknown_scorer_is_an_error_instead_of_neutral_fallback(self) -> None:
        with patch('data_manager.sentiment_cache._crawl_articles_full',return_value=[]),patch('data_manager.sentiment_cache._score_articles',return_value=[{'scorer':'unknown-provider'}]):
            with self.assertRaises(ValueError): market_news('MWG','2026-11-12')
