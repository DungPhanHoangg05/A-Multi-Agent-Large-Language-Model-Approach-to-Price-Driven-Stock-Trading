"""Một upstream và một decision realization, hai ngôn ngữ sẵn có trước khi mở kết quả."""
import unittest


class BilingualLive(unittest.TestCase):
    def test_live_job_saves_both_languages_and_views_do_not_dispatch(self) -> None:
        from test_live_api import LiveApiTests
        from support import request,charts
        LiveApiTests.setUpClass(); case=LiveApiTests(); case.setUp()
        try:
            case.snapshots.charts=charts
            captured=case.client.post('/api/serving/live/v1/snapshot',json={'symbol':'MWG','timeframe':'1d'}).get_json()
            body=request(captured['snapshot_id'],captured['cutoff'],['C2'])
            body.update(version='variant_serving_timeframe_v1',chart_timeframe='1d')
            started=case.client.post('/api/serving/live/v1/jobs',json=body).get_json(); case.join()
            data=case.client.get('/api/serving/live/v1/jobs/'+started['run_id']).get_json()
            self.assertEqual(data['state'],'completed',data.get('error'))
            point=next(iter(data['presentations'])); reports=data['presentations'][point]
            for role in ('indicator','pattern','trend','alpha','sentiment'):
                self.assertEqual(set(reports[role]),{'vi','en'}); self.assertTrue(reports[role]['en'].strip())
            before=sum(len(sender.bodies) for sender in case.senders)
            self.assertEqual(before,3)
            for lang in ('en','vi','en'):
                response=case.client.get('/output?serving_run='+started['run_id']+'&serving_source=live&presentation=analysis&lang='+lang)
                self.assertEqual(response.status_code,200)
                raw=response.get_data(as_text=True)
                self.assertIn('id="report-view-vi"',raw); self.assertIn('id="report-view-en"',raw)
            self.assertEqual(before,sum(len(sender.bodies) for sender in case.senders))
            self.assertEqual(case.client.post('/api/display-locales',json={'target':'en','texts':{'n0':'no translation'}}).status_code,404)
        finally: case.doCleanups()
