"""EN là locale hiển thị của job; snapshot/prompt nghiên cứu VI và số lần inference không bị thay."""
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from support import ROOT,prices,news,charts,request
from core.serving_live.snapshots import Snapshots,ZONE
from core.serving_live.service import LiveService,LiveRequest


class LocaleContract(unittest.TestCase):
    def test_en_preflight_and_identity_use_selected_locale_without_loading_or_calling_models(self) -> None:
        with TemporaryDirectory() as folder:
            snapshots=Snapshots(Path(folder)/'inputs',prices=prices,news=news,charts=charts,
                now=lambda:datetime(2026,11,13,16,tzinfo=ZONE))
            owner='a'*64; captured=snapshots.capture_timeframe('MWG','1d',owner)
            backend=LiveService(ROOT,state_root=Path(folder)/'state',snapshots=snapshots)
            body=request(captured['snapshot_id'],captured['cutoff'],['C2'])
            body.update(version='variant_serving_timeframe_v1',chart_timeframe='1d'); body['request']['language']='en'
            spec=LiveRequest.create(body)
            checked=backend.preflight(spec,'fixture')
            self.assertTrue(checked['run_enabled']); self.assertIn('en',checked['support']['languages'])
            identifier=backend.create(spec,'fixture',owner,background=False)
            result=backend.result(identifier,owner)
            self.assertEqual(result['identity']['request']['language'],'en')
            self.assertEqual(result['generation_language'],'vi'); self.assertEqual(result['display_language'],'en')
            self.assertEqual(result['progress']['api_attempts'],0); self.assertEqual(backend.tasks,{})
            self.assertEqual(result['rows'],[])
