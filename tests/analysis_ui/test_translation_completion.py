"""Tái hiện HTTP400 output cutoff thật và phục hồi ba báo cáo tiếng Anh mà không gọi lại forecast."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from uuid import uuid5,NAMESPACE_URL

from test_display_locales import Sender,Clock
from core.serving_locales import LocaleService
from core.serving_runtime.quota import Quota
from core.historical_evaluation_journal import load,save
from core.unified_contracts import digest
from core.translation_transport import translation_body
from core.groq_pacing import request_budget
from core.display_translation import ReportPlan,validate_translation


class TranslationCompletion(unittest.TestCase):
    def setUp(self) -> None:
        self.temp=TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.clock=Clock(); self.sender=Sender(self.clock)
        self.service=LocaleService(Path(self.temp.name)/'cache',Quota(Path(self.temp.name)/'quota.sqlite3',self.clock),
            sender_factory=lambda key:self.sender,clock=self.clock)
        self.fixture=json.loads((Path(__file__).parent/'completion_regression.json').read_bytes())

    def test_real_cutoff_body_gets_larger_completion_reserve_within_shared_quota(self) -> None:
        old=self.fixture['request']; batch=json.loads(old['messages'][-1]['content'])
        self.assertEqual(old['max_tokens'],2048)
        body=translation_body(batch,'en')
        self.assertEqual(body['max_tokens'],4096); self.assertLessEqual(request_budget(body),8000)
        self.assertIn('max completion tokens',self.fixture['response']['error']['failed_generation'])

    def test_exact_three_source_reports_complete_in_english_through_guarded_transport(self) -> None:
        plans={name:ReportPlan(text) for name,text in self.fixture['english_reports'].items()}
        original=self.sender.send
        def send(body):
            if body['max_tokens']<=2048:
                self.sender.bodies.append(body); self.clock.advance()
                return 400,json.dumps(self.fixture['response']).encode(),{}
            self.sender.action=lambda batch:{key:plans[key.rsplit('_',1)[0]].segments[key.rsplit('_',1)[1]].masked for key in batch}
            return original(body)
        self.sender.send=send
        value=self.service.start(self.fixture['source_reports'],'en','a'*64,'fixture',background=False)
        self.assertEqual(value['state'],'completed'); self.assertEqual(len(value['texts']),3)
        for name,text in value['texts'].items(): validate_translation(self.fixture['source_reports'][name],text,'en')
        self.assertIn('Trading implication',value['texts']['n19']); self.assertIn('Trend forecast',value['texts']['n20'])

    def test_known_output_cutoff_splits_into_checkpointed_children(self) -> None:
        original=self.sender.send
        def send(body):
            if len(json.loads(body['messages'][-1]['content']))>1:
                self.sender.bodies.append(body); self.clock.advance()
                return 400,json.dumps(self.fixture['response']).encode(),{}
            return original(body)
        self.sender.send=send
        value=self.service.start({'alpha':'Giá trị 1','pattern':'Giá trị 2'},'en','a'*64,'fixture',background=False)
        self.assertEqual(value['state'],'completed'); self.assertEqual(value['texts'],{'alpha':'Value 1','pattern':'Value 2'})
        self.assertEqual(len(self.sender.bodies),3)
        self.service.start({'alpha':'Giá trị 1','pattern':'Giá trị 2'},'en','a'*64,'fixture',background=False)
        self.assertEqual(len(self.sender.bodies),3)

    def test_other_http400_does_not_trigger_split_or_retry(self) -> None:
        def send(body):
            self.sender.bodies.append(body); self.clock.advance()
            return 400,b'{"error":{"code":"invalid_request_error","failed_generation":"different error"}}',{}
        self.sender.send=send
        value=self.service.start({'alpha':'Giá trị 1','pattern':'Giá trị 2'},'en','a'*64,'fixture',background=False)
        self.assertEqual(value['state'],'failed'); self.assertEqual(len(self.sender.bodies),1)

    def test_v2_recovery_reuses_completed_reports_and_only_translates_missing_fields(self) -> None:
        texts={'alpha':'Giá trị 1','pattern':'Giá trị 2','trend':'Giá trị 3'}
        source={'version':'display_locale_v2','texts':texts,'target':'en','owner':'a'*64,
            'credential_scope_sha256':self.service.quota.credential_scope('fixture')}
        old=str(uuid5(NAMESPACE_URL,digest(source))); path=self.service.path(old); path.mkdir()
        save(path/'source.json',source); save(path/'status.json',{'state':'failed'}); save(path/'result.json',{'alpha':'Value 1'})
        before={name:(path/name).read_bytes() for name in ('source.json','status.json','result.json')}
        value=self.service.start(texts,'en','a'*64,'fixture',background=False)
        self.assertEqual(value['state'],'completed'); self.assertEqual(value['texts'],{'alpha':'Value 1','pattern':'Value 2','trend':'Value 3'})
        self.assertFalse(any(key.startswith('alpha_') for body in self.sender.bodies for key in json.loads(body['messages'][-1]['content'])))
        self.assertEqual(before,{name:(path/name).read_bytes() for name in before})

    def test_completed_translation_can_be_read_without_key_and_other_owner_cannot_use_it(self) -> None:
        texts={'alpha':'Giá trị 1'}
        result=self.service.start(texts,'en','a'*64,'fixture',background=False)
        calls=len(self.sender.bodies)
        cached=self.service.start(texts,'en','a'*64,'',background=False)
        self.assertEqual(cached['id'],result['id']); self.assertEqual(cached['texts'],{'alpha':'Value 1'})
        self.assertEqual(len(self.sender.bodies),calls)
        with self.assertRaises(ValueError): self.service.start(texts,'en','b'*64,'',background=False)
