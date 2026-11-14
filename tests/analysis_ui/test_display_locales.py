"""Cache/owner/quota/UNKNOWN bản dịch, giữ số và công thức; không gọi hosted LLM."""
from pathlib import Path
from tempfile import TemporaryDirectory
import importlib
import json
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tests/serving_runtime'))
from support import Clock
from core.serving_runtime.quota import Quota
from core.serving_locales import LocaleService,validate_translation,chunks
from core.historical_evaluation_journal import load,save
from core.unified_contracts import digest
from uuid import uuid5,NAMESPACE_URL
from core.display_translation import ReportPlan


class Sender:
    def __init__(self,clock,action=None): self.clock,self.action=clock,action; self.bodies=[]
    def send(self,body):
        self.bodies.append(body); self.clock.advance()
        if isinstance(self.action,BaseException): raise self.action
        source=json.loads(body['messages'][-1]['content'])
        value=self.action(source) if callable(self.action) else self.action or {key:text.replace('Giá trị','Value').replace('TĂNG','UP') for key,text in source.items()}
        return 200,json.dumps({'choices':[{'message':{'content':json.dumps(value)}}]}).encode(),{}
    def close(self): pass


class DisplayLocales(unittest.TestCase):
    def setUp(self) -> None:
        self.temp=TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.clock=Clock(); self.senders=[]
        self.quota=Quota(Path(self.temp.name)/'quota.sqlite3',self.clock)
        def factory(key):
            sender=Sender(self.clock); self.senders.append(sender); return sender
        self.service=LocaleService(Path(self.temp.name)/'locales',self.quota,sender_factory=factory,clock=self.clock)

    def test_cache_preserves_numeric_trade_codes_and_original_input_without_repeat_calls(self) -> None:
        source={'report':'Giá trị **-2.8411**; TĂNG; LONG; `rank(C,5)`'}
        result=self.service.start(source,'en','a'*64,'fixture',background=False)
        self.assertEqual(result['state'],'completed'); self.assertIn('Value',result['texts']['report'])
        self.assertIn('-2.8411',result['texts']['report']); self.assertIn('Giá trị',source['report'])
        self.service.start(source,'en','a'*64,'fixture',background=False)
        self.assertEqual(len(self.senders),1)
        with self.assertRaises(PermissionError): self.service.result(result['id'],'b'*64)
        self.assertNotIn('fixture',(self.service.path(result['id'])/'source.json').read_text(encoding='utf-8'))

    def test_changed_numbers_codes_formula_or_language_fail_instead_of_fake_translation(self) -> None:
        for source,value in [('Value 1','Value 2'),('SHORT','LONG'),('`rank(C,5)`','`rank(C,6)`'),('Giá trị 1','Giá trị 1'),('WQ57_VwapArgmax FPT SMA20','WQ58_VwapArgmax FPT SMA20')]:
            with self.assertRaises(ValueError): validate_translation(source,value,'en')
        text='word '*2000
        self.assertEqual(''.join(chunks(text)),text); self.assertTrue(all(len(part)<=1700 for part in chunks(text)))

    def test_unknown_attempt_never_resends_and_key_changes_create_separate_locale_identity(self) -> None:
        self.service.sender_factory=lambda key:Sender(self.clock,TimeoutError('fixture timeout'))
        result=self.service.start({'report':'Giá trị 1'},'en','a'*64,'fixture',background=False)
        self.assertEqual(result['state'],'unknown')
        self.assertEqual(self.service.start({'report':'Giá trị 1'},'en','a'*64,'fixture')['id'],result['id'])
        self.service.sender_factory=lambda key:Sender(self.clock)
        another=self.service.start({'report':'Giá trị 1'},'en','a'*64,'another-key',background=False)
        self.assertNotEqual(result['id'],another['id']); self.assertEqual(another['state'],'completed')

    def test_retired_translation_routes_never_dispatch(self) -> None:
        with patch('core.realtime_loader.get_all_symbols_realtime',return_value=[]): web=importlib.import_module('web_interface')
        client=web.app.test_client()
        self.assertEqual(client.post('/api/display-locales',json={'texts':{'n0':'report'},'target':'en'}).status_code,404)
        self.assertEqual(client.get('/api/display-locales/12345678-1234-4234-8234-123456789abc').status_code,404)
        self.assertEqual(self.senders,[])

    def test_one_invalid_report_does_not_hide_other_translations(self) -> None:
        def translate(batch):
            return {key:'Value' if key.startswith('bad_') else text.replace('Giá trị','Value') for key,text in batch.items()}
        self.service.sender_factory=lambda key:Sender(self.clock,translate)
        value=self.service.start({'bad':'Giá trị 1','good':'Giá trị 2'},'en','a'*64,'fixture',background=False)
        self.assertEqual(value['state'],'partial'); self.assertEqual(value['texts'],{'good':'Value 2'})
        self.assertEqual(value['errors'],{'bad':'INVALID_TRANSLATION'})

    def test_transport_failed_baseexception_becomes_terminal_status_without_raw_error(self) -> None:
        sender=Sender(self.clock)
        sender.send=lambda body:(401,b'{"error":{"message":"fixture-secret"}}',{})
        self.service.sender_factory=lambda key:sender
        value=self.service.start({'report':'Giá trị 1'},'en','a'*64,'fixture',background=False)
        self.assertEqual(value['state'],'failed'); self.assertEqual(value['error_code'],'PROVIDER_FAILURE')
        self.assertNotIn('fixture-secret',json.dumps(value))

    def test_protocol_upgrade_replaces_failed_cache_without_deleting_it_or_replaying_unknown(self) -> None:
        owner='a'*64; key='fixture'; texts={'report':'Giá trị 1'}
        source={'version':'display_locale_v1','texts':texts,'target':'en','owner':owner,
            'credential_scope_sha256':self.quota.credential_scope(key)}
        old=str(uuid5(NAMESPACE_URL,digest(source))); path=self.service.path(old); path.mkdir()
        save(path/'source.json',source); save(path/'status.json',{'state':'unknown'})
        result=self.service.start(texts,'en',owner,key,background=False)
        self.assertEqual(result['id'],old); self.assertEqual(result['state'],'unknown'); self.assertEqual(self.senders,[])
        save(path/'status.json',{'state':'failed'})
        result=self.service.start(texts,'en',owner,key,background=False)
        self.assertNotEqual(result['id'],old); self.assertEqual(result['state'],'completed')
        self.assertEqual(load(path/'status.json'),{'state':'failed'})

    def test_real_indicator_payload_translates_through_http_schema_and_keeps_all_four_rules(self) -> None:
        fixture=json.loads((Path(__file__).parent/'locale_regression.json').read_bytes())
        source=ReportPlan(fixture['source']); expected=ReportPlan(fixture['expected_translation'])
        self.assertEqual(set(source.segments),set(expected.segments))
        def translate(batch):
            return {key:expected.segments[key.rsplit('_',1)[1]].masked for key in batch}
        self.service.sender_factory=lambda key:Sender(self.clock,translate)
        value=self.service.start({'report':fixture['source']},'en','a'*64,'fixture',background=False)
        self.assertEqual(value['state'],'completed')
        for number in range(1,5): self.assertIn('\n'+str(number)+'. ',value['texts']['report'])
        self.assertIn('Use EXACTLY',value['texts']['report']); self.assertIn('do not cross-reference',value['texts']['report'])
        validate_translation(fixture['source'],value['texts']['report'],'en')

    def test_resume_after_first_report_published_replays_completed_http_without_resending(self) -> None:
        texts={'short':'Giá trị 1','long':'Giá trị 2\n'*40}
        def crash(path,value):
            save(path,value)
            if path.name=='result.json' and 'short' in value: raise KeyboardInterrupt('fixture crash after publish')
        with patch('core.serving_locales.save',side_effect=crash),self.assertRaises(KeyboardInterrupt):
            self.service.start(texts,'en','a'*64,'fixture',background=False)
        self.assertEqual(len(self.senders[0].bodies),1)
        value=self.service.start(texts,'en','a'*64,'fixture')
        for worker in self.service.tasks.values(): worker.join(10); self.assertFalse(worker.is_alive())
        value=self.service.result(value['id'],'a'*64)
        self.assertEqual(value['state'],'completed'); self.assertEqual(value['texts']['long'],'Value 2\n'*40)
        self.assertEqual(len(self.senders[1].bodies),2)
