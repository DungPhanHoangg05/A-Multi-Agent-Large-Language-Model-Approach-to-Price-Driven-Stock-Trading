"""API owner, cấu hình snapshot và hai job đồng thời, không LLM/thị trường thật."""
from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import threading
import unittest

from flask import Flask

from core.serving_contracts import ServingRequest
from core.serving_runtime.service import Service
from utils.serving_web import serving
from support import ROOT, Clock, Provider, Sender, FixtureResources, spec


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.clock = Clock()
        self.senders, self.keys = [], []
        def sender_factory(key):
            sender = Sender(self.clock)
            self.senders.append(sender); self.keys.append(key)
            return sender
        self.service = Service(ROOT,state_root=Path(self.temp.name),clock=self.clock,provider_factory=Provider,
            resources_factory=FixtureResources,sender_factory=sender_factory)
        self.key = 'fixture-secret-A'
        app = Flask(__name__)
        app.config['SERVING_SERVICE'] = self.service
        app.config['SERVING_API_KEY_PROVIDER'] = lambda:self.key
        app.register_blueprint(serving)
        self.app, self.client = app, app.test_client()
        self.addCleanup(self.join_workers)
    def join_workers(self):
        for worker in list(self.service.tasks.values()):
            worker.join(15)
            self.assertFalse(worker.is_alive())
    def start(self, client=None, request=None):
        response = (client or self.client).post('/api/serving/v1/jobs',json=(request or spec()).document())
        self.assertEqual(response.status_code,202,response.get_data(as_text=True))
        return response.get_json()['run_id']

    def test_preflight_ready_and_endpoint_starts_real_runner_with_owner_cookie(self):
        response = self.client.post('/api/serving/v1/preflight',json=spec().document())
        self.assertTrue(response.get_json()['run_enabled'])
        self.assertIn('HttpOnly',response.headers['Set-Cookie'])
        identifier = self.start()
        self.join_workers()
        data = self.client.get('/api/serving/v1/jobs/'+identifier).get_json()
        self.assertEqual(data['state'],'completed')
        self.assertNotIn(self.key,json.dumps(data))
        self.assertEqual(self.app.test_client().get('/api/serving/v1/jobs/'+identifier).status_code,404)
        self.assertIn(self.client.get('/api/serving/v1/jobs/..%2Fother').status_code,(404,405))

    def test_missing_key_unsupported_domain_and_cross_origin_never_start(self):
        self.key = ''
        response = self.client.post('/api/serving/v1/jobs',json=spec().document())
        self.assertEqual(response.status_code,409)
        self.assertFalse(response.get_json()['run_enabled'])
        self.assertEqual(self.senders,[])
        self.key = 'fixture-secret-A'
        value = spec().document(); value['language'] = 'en'
        self.assertFalse(self.client.post('/api/serving/v1/preflight',json=value).get_json()['run_enabled'])
        response = self.client.post('/api/serving/v1/jobs',json=spec().document(),headers={'Origin':'https://untrusted.example'})
        self.assertEqual(response.status_code,400)
        self.assertEqual(self.senders,[])

    def test_two_owners_jobs_snapshot_key_and_model_without_global_graph_mutation(self):
        one = spec().document()
        two = deepcopy(one)
        two['symbols'] = ['VNM']
        two['models']['decision']['options']['temperature'] = .6
        first = self.start(request=ServingRequest.create(one))
        self.key = 'fixture-secret-B'
        second_client = self.app.test_client()
        second = self.start(client=second_client,request=ServingRequest.create(two))
        self.join_workers()
        first_data = self.client.get('/api/serving/v1/jobs/'+first).get_json()
        second_data = second_client.get('/api/serving/v1/jobs/'+second).get_json()
        self.assertEqual(first_data['state'],'completed')
        self.assertEqual(second_data['state'],'completed')
        self.assertNotEqual(first_data['cache_sha256'],second_data['cache_sha256'])
        self.assertEqual(first_data['identity']['request'],one)
        self.assertEqual(second_data['identity']['request'],two)
        self.assertEqual(set(self.keys),{'fixture-secret-A','fixture-secret-B'})
        self.assertEqual(self.client.get('/api/serving/v1/jobs/'+second).status_code,404)
        self.assertEqual(second_client.post('/api/serving/v1/jobs/'+first+'/stop',json={}).status_code,404)
        self.assertEqual(self.client.post('/api/serving/v1/jobs/'+first+'/resume',json={}).status_code,409)

    def test_resume_completed_is_idempotent_and_control_body_cannot_change_config(self):
        identifier = self.start()
        self.join_workers()
        before = sum(len(sender.bodies) for sender in self.senders)
        response = self.client.post('/api/serving/v1/jobs/'+identifier+'/resume',json={})
        self.assertEqual(response.status_code,202)
        self.assertEqual(sum(len(sender.bodies) for sender in self.senders),before)
        response = self.client.post('/api/serving/v1/jobs/'+identifier+'/resume',json={'models':{}})
        self.assertEqual(response.status_code,409)


if __name__ == '__main__':
    unittest.main()
