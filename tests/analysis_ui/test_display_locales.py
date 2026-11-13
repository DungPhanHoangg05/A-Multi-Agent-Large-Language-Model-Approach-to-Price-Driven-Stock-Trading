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


class Sender:
    def __init__(self,clock,action=None): self.clock,self.action=clock,action; self.bodies=[]
    def send(self,body):
        self.bodies.append(body); self.clock.advance()
        if isinstance(self.action,BaseException): raise self.action
        source=body['messages'][-1]['content'].split('SOURCE DATA:\n')[-1]
        value=self.action or source.replace('Giá trị','Value').replace('TĂNG','UP')
        return 200,json.dumps({'choices':[{'message':{'content':json.dumps({'text':value})}}]}).encode(),{}
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

    def test_web_get_owner_and_cross_origin_never_dispatch_translation(self) -> None:
        with patch('core.realtime_loader.get_all_symbols_realtime',return_value=[]): web=importlib.import_module('web_interface')
        with patch.dict(web.app.config,{'DISPLAY_LOCALE_SERVICE':self.service,'SERVING_API_KEY_PROVIDER':lambda:'fixture'}),patch('utils.display_locale_web.owner',return_value=('a'*64,None)):
            client=web.app.test_client()
            response=client.post('/api/display-locales',json={'texts':{'n0':'Giá trị 1'},'target':'en'},headers={'Origin':'https://untrusted.example'})
            self.assertEqual(response.status_code,400); self.assertEqual(self.senders,[])
            self.assertEqual(client.get('/api/display-locales/12345678-1234-4234-8234-123456789abc').status_code,404)
            self.assertEqual(self.senders,[])

    def test_post_translates_once_get_cache_is_readonly_and_other_owner_cannot_read(self) -> None:
        with patch('core.realtime_loader.get_all_symbols_realtime',return_value=[]): web=importlib.import_module('web_interface')
        with patch.dict(web.app.config,{'DISPLAY_LOCALE_SERVICE':self.service,'SERVING_API_KEY_PROVIDER':lambda:'fixture'}),patch('utils.display_locale_web.owner',return_value=('a'*64,None)):
            client=web.app.test_client()
            body={'texts':{'n0':'Giá trị 1.23; SHORT'},'target':'en'}
            response=client.post('/api/display-locales',json=body)
            self.assertIn(response.status_code,(200,202)); identifier=response.get_json()['id']
            for worker in self.service.tasks.values(): worker.join(10); self.assertFalse(worker.is_alive())
            count=len(self.senders[0].bodies)
            for _ in range(2):
                data=client.get('/api/display-locales/'+identifier).get_json()
                self.assertEqual(data['texts']['n0'],'Value 1.23; SHORT')
            self.assertEqual(count,len(self.senders[0].bodies))
            with patch('utils.display_locale_web.owner',return_value=('b'*64,None)):
                self.assertEqual(client.get('/api/display-locales/'+identifier).status_code,404)
