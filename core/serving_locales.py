"""Bản dịch trình bày có cache/checkpoint riêng; tuyệt đối không sửa forecast hoặc artifact nguồn."""
from __future__ import annotations

from pathlib import Path
import re
import threading
import time
from uuid import NAMESPACE_URL,uuid5
from typing import Any,Callable

from core.historical_evaluation_journal import load,save
from core.serving_runtime.transport import Calls,GroqHTTP
from core.serving_runtime.quota import Unknown,Failed
from core.unified_execution import StageBook
from core.unified_contracts import digest

from core.display_translation import ReportPlan,TranslationError,validate_translation,batch_segments
from core.translation_transport import translate_batch

VERSION='display_locale_v3'


def chunks(text: str) -> list[str]:
    """Giữ ranh giới khoảng trắng để nối lại Markdown; prompt nhỏ hơn guard chung của transport."""
    parts=[]
    while len(text)>1700:
        cut=max(text.rfind('\n',0,1700),text.rfind(' ',0,1700))
        cut=cut+1 if cut>800 else 1700
        parts.append(text[:cut]); text=text[cut:]
    if text: parts.append(text)
    return parts


class LocaleService:
    """Quota dùng chung serving; UUID bản dịch độc lập, chỉ một worker/owner/source/locale."""
    def __init__(self, directory: Path, quota: Any, *, sender_factory: Callable=GroqHTTP, clock: Callable=time.time) -> None:
        self.root=directory.resolve(); self.root.mkdir(parents=True,exist_ok=True)
        (self.root/'.gitignore').write_text('*\n',encoding='utf-8')
        self.quota,self.sender_factory,self.clock=quota,sender_factory,clock
        self.lock=threading.RLock(); self.tasks={}

    def path(self, identifier: str) -> Path:
        """ID do server tạo, không nhận đường dẫn từ browser."""
        from uuid import UUID
        if str(UUID(identifier))!=identifier: raise ValueError('ID bản dịch không hợp lệ')
        path=self.root/identifier
        if path.is_symlink() or not path.resolve().is_relative_to(self.root): raise ValueError('Đường bản dịch không hợp lệ')
        return path

    def start(self, texts: dict, target: str, owner: str, key: str, *, background: bool=True) -> dict:
        """Cache theo owner/credential; request chỉ chứa văn bản, key không ghi vào body/journal."""
        if target not in ('vi','en') or type(texts) is not dict or not 1<=len(texts)<=200:
            raise ValueError('Ngôn ngữ hoặc số trường bản dịch không hợp lệ')
        if any(not re.fullmatch(r'[a-zA-Z0-9_-]{1,80}',name) or type(value) is not str or len(value)>30000 for name,value in texts.items()) or sum(map(len,texts.values()))>60000:
            raise ValueError('Văn bản dịch vượt miền hiển thị')
        if not key:
            # Đọc bản dịch hoàn tất chỉ cần owner; không bắt nhập key lại để xem kết quả cũ.
            for candidate in self.root.iterdir():
                if not candidate.is_dir() or not (candidate/'source.json').exists(): continue
                saved=load(candidate/'source.json')
                if saved.get('owner')==owner and saved.get('target')==target and saved.get('texts')==texts:
                    cached=self.result(candidate.name,owner)
                    if cached['state']=='completed': return cached
            raise ValueError('Cần API key để chuẩn bị ngôn ngữ')
        base={'texts':texts,'target':target,'owner':owner,'credential_scope_sha256':self.quota.credential_scope(key)}
        with self.lock:
            seeded={}
            for version in ('display_locale_v1','display_locale_v2'):
                previous=str(uuid5(NAMESPACE_URL,digest({'version':version,**base})))
                if self.path(previous).exists():
                    prior=self.result(previous,owner)
                    if prior['state'] in ('unknown','queued','running'): return prior
                    seeded.update(prior.get('texts',{}))
            # Seed bất biến thuộc identity, không đổi cách nhóm batch khi resume.
            source={'version':VERSION,**base,'seeded_texts':seeded}
            identifier=str(uuid5(NAMESPACE_URL,digest(source))); path=self.path(identifier)
            if path.exists():
                result=self.result(identifier,owner)
                if result['state'] in ('queued','running') and not (identifier in self.tasks and self.tasks[identifier].is_alive()) and key:
                    worker=threading.Thread(target=self.work,args=(identifier,str(key),owner),daemon=True)
                    self.tasks[identifier]=worker; worker.start()
                return result
            path.mkdir()
            save(path/'source.json',source); save(path/'status.json',{'state':'queued'}); save(path/'result.json',seeded)
            if background:
                worker=threading.Thread(target=self.work,args=(identifier,str(key),owner),daemon=True)
                self.tasks[identifier]=worker; worker.start()
        if not background: self.work(identifier,key,owner)
        return self.result(identifier,owner)

    def result(self, identifier: str, owner: str) -> dict:
        """GET chỉ đọc cache/owner, không mở client hoặc tự replay UNKNOWN."""
        path=self.path(identifier); source=load(path/'source.json')
        if source['owner']!=owner: raise PermissionError('Bản dịch không thuộc owner')
        status=load(path/'status.json')
        result={'id':identifier,'state':status['state'],'target':source['target'],'source_sha256':digest(source['texts'])}
        result['errors']=status.get('errors',{})
        result['error_code']=status.get('error_code')
        result['retry_at']=status.get('retry_at')
        if (path/'result.json').exists():
            result['texts']=load(path/'result.json')
            if not set(result['texts'])<=set(source['texts']) or status['state']=='completed' and set(result['texts'])!=set(source['texts']): raise ValueError('Bản dịch khác inventory nguồn')
            for name,text in result['texts'].items():
                if source['texts'][name].strip(): validate_translation(source['texts'][name],text,source['target'])
        return result

    def work(self, identifier: str, key: str, owner: str) -> None:
        """Mỗi chunk qua Calls/_invoke_with_retry, checkpoint trước/sau; lỗi không thay bằng bản VI."""
        path=self.path(identifier); source=load(path/'source.json'); sender=None
        try:
            if source['owner']!=owner: raise PermissionError('Sai owner bản dịch')
            if self.quota.credential_scope(key)!=source['credential_scope_sha256']: raise ValueError('Credential bản dịch đã đổi')
            book=StageBook(path/'journal',source)
            sender=self.sender_factory(key)
            def guard() -> None:
                if load(path/'source.json')!=source: raise ValueError('Nguồn bản dịch đã đổi')
            calls=Calls(path,identifier,self.quota,sender,guard,clock=self.clock)
            save(path/'status.json',{'state':'running'})
            output=load(path/'result.json'); errors={}; plans={}; segments={}; refs={}; translated={}
            for name,text in source['texts'].items():
                if name in source.get('seeded_texts',{}): continue
                try:
                    plans[name]=ReportPlan(text); translated[name]={}
                    for key,segment in plans[name].segments.items():
                        segment_id=name+'_'+key; segments[segment_id]=segment; refs[segment_id]=(name,key)
                except TranslationError:
                    errors[name]='INVALID_TRANSLATION'
            def publish() -> None:
                for name,plan in plans.items():
                    if name in output or name in errors or set(translated[name])!=set(plan.segments): continue
                    try:
                        value=plan.render(translated[name],source['target'])
                        if source['texts'][name].strip(): validate_translation(source['texts'][name],value,source['target'])
                        output[name]=value; save(path/'result.json',output)
                    except TranslationError: errors[name]='INVALID_TRANSLATION'
            publish()
            def waiting(until: float | None) -> None:
                save(path/'status.json',{'state':'running','retry_at':until})
            for index,batch in enumerate(batch_segments(segments)):
                slot='segments/'+str(index)
                reply,limited=translate_batch(book,calls,slot,batch,source['target'],self.clock,waiting)
                for segment_id in limited: errors[refs[segment_id][0]]='OUTPUT_LIMIT'
                for segment_id,value in reply.items():
                    name,key=refs[segment_id]
                    try:
                        segments[segment_id].restore(value,source['target']); translated[name][key]=value
                    except TranslationError: errors[name]='INVALID_TRANSLATION'
                publish()
            save(path/'status.json',{'state':'partial' if errors else 'completed','errors':errors})
        except Unknown:
            save(path/'status.json',{'state':'unknown','error_code':'UNKNOWN_ATTEMPT'})
        except Failed:
            save(path/'status.json',{'state':'failed','error_code':'PROVIDER_FAILURE'})
        except Exception:
            save(path/'status.json',{'state':'failed','error_code':'LOCALIZATION_FAILED'})
        finally:
            if sender is not None: sender.close()
