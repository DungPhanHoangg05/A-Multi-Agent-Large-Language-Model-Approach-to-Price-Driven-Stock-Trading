"""Rào chắn preview fixture không được đụng key/owner thật hoặc gọi API legacy."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from fixtures import ROOT
from review_app import make_app


class PreviewBoundaryTests(unittest.TestCase):
    def test_preview_uses_fixture_key_separate_cookie_and_blocks_legacy_mutations(self) -> None:
        from utils import serving_web
        with TemporaryDirectory() as folder,patch.dict('os.environ',{'GROQ_API_KEY':'fixture-must-not-use-existing-key'}),patch.object(serving_web,'COOKIE','qa_serving_review_owner'):
            app,service,_ = make_app(Path(folder)); client = app.test_client()
            self.assertEqual(app.config['SERVING_API_KEY_PROVIDER'](),'fixture-review-key')
            page = client.get('/demo'); raw = page.get_data(as_text=True)
            self.assertIn('HTTP FIXTURE',raw); self.assertNotIn('fixture-must-not-use-existing-key',raw)
            cookies = page.headers.getlist('Set-Cookie')
            self.assertTrue(any(value.startswith('qa_serving_review_owner=') for value in cookies))
            self.assertFalse(any(value.startswith('qa_serving_owner=') for value in cookies))
            for path in ('/api/analyze','/api/backtest/start','/api/update-api-key','/api/update-models'):
                self.assertEqual(client.post(path,json={}).status_code,409)
            self.assertEqual(client.get('/api/assets?refresh=1').get_json()['assets'],[])
            self.assertTrue(client.get('/api/groq-status').get_json()['fixture'])
            live = client.post('/api/serving/live/v1/snapshot',json={'symbol':'MWG'})
            self.assertEqual(live.status_code,200)
            self.assertEqual(live.get_json()['cutoff'],'2026-11-12')
            intraday = client.post('/api/serving/live/v1/snapshot',json={'symbol':'MWG','timeframe':'5m'})
            self.assertEqual(intraday.status_code,200)
            self.assertEqual(intraday.get_json()['chart_timeframe'],'5m')
            self.assertEqual(service.tasks,{})
