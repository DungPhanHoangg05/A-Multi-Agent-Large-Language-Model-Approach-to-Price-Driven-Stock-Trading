import {renderReport,normalizeIndicator} from './analysis/report.js';

const active=new WeakSet();
const vietnamese=/[ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯư\u1ea0-\u1ef9]/u;
const delay=ms => new Promise(resolve => setTimeout(resolve,ms));

export function needsTranslation(text,target,source) {
  return target==='en' ? source==='vi' || vietnamese.test(text) : source==='en';
}

async function request(url,body) {
  const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),15000);
  try {
    const response=await fetch(url,{method:body ? 'POST' : 'GET',signal:controller.signal,headers:body ? {'Content-Type':'application/json'} : {},body:body ? JSON.stringify(body) : undefined});
    const data=await response.json(); if (!response.ok) throw new Error('LOCALIZATION_FAILED'); return data;
  } finally { clearTimeout(timer); }
}

// Nội dung luôn đọc được khi chờ quota, lỗi mạng hoặc backend cũ; không giấu cả report bằng CSS.
function showSource(node,raw,message,config) {
  const notice=document.createElement('p'); notice.textContent=message; notice.setAttribute('role','status');
  const details=document.createElement('details'),summary=document.createElement('summary'),source=document.createElement(node.dataset.markdown==='true' ? 'div' : 'pre');
  summary.textContent=config.source_report+' · '+(node.dataset.sourceLanguage ?? 'vi').toUpperCase();
  details.open=true;
  if (node.dataset.markdown==='true') { source.classList.add('auto-beautify'); renderReport(source,raw); }
  else source.textContent=raw;
  details.append(summary,source); node.replaceChildren(notice,details); node.removeAttribute('data-locale-pending');
}

// Chỉ tạo bản hiển thị; số/mã được server đối soát, không ghi lại response hoặc artifact phân tích.
export async function localizeElements(nodes,config,io=request,pause=delay) {
  const selected=nodes.filter(node => !active.has(node) && node.dataset.localizedLanguage!==config.language);
  if (!selected.length) return;
  const texts={},pending=[];
  for (const node of selected) {
    active.add(node);
    const raw=node.id==='indicatorContent' ? normalizeIndicator(node.textContent) : node.textContent;
    if (raw.trim() && needsTranslation(raw,config.language,node.dataset.sourceLanguage ?? 'vi')) {
      const id='n'+pending.length; texts[id]=raw; pending.push({id,node,raw});
      showSource(node,raw,config.preparing,config); node.setAttribute('aria-busy','true');
    } else finish(node,raw,config.language);
  }
  if (!pending.length) return;
  const status=document.getElementById('display-locale-status');
  if (status) { status.hidden=false; status.textContent=config.preparing; }
  try {
    let result=await io('/api/display-locales',{target:config.language,texts});
    const apply=() => {
      if (result.target!==config.language) throw new Error('LOCALIZATION_FAILED');
      for (const {id,node} of pending) {
        if (node.dataset.localizedLanguage!==config.language && typeof result.texts?.[id]==='string') finish(node,result.texts[id],config.language);
      }
      if (status) {
        const count=pending.filter(({node})=>node.dataset.localizedLanguage===config.language).length;
        status.textContent=config.preparing+` (${count}/${pending.length})`+(result.retry_at ? ' · '+config.quota_wait+': '+new Date(result.retry_at*1000).toLocaleTimeString(config.language) : '');
      }
    };
    apply();
    while (['queued','running'].includes(result.state)) {
      if (!/^[0-9a-f-]{36}$/.test(result.id)) throw new Error('Invalid translation ID');
      await pause(1500); result=await io('/api/display-locales/'+encodeURIComponent(result.id));
      apply();
    }
    if (result.state!=='completed' || pending.some(({node}) => node.dataset.localizedLanguage!==config.language)) throw new Error(result.state==='unknown' ? 'UNKNOWN' : 'LOCALIZATION_FAILED');
    if (status) status.hidden=true;
  } catch (error) {
    if (status) { status.hidden=false; status.textContent=error.message==='UNKNOWN' ? config.locale_unknown : config.locale_failed; }
    // Giữ phần đã dịch và bản gốc trong mục thu gọn; không xóa báo cáo chỉ vì một phần lỗi.
    for (const {node,raw} of pending) {
      if (node.dataset.localizedLanguage===config.language) continue;
      showSource(node,raw,error.message==='UNKNOWN' ? config.locale_unknown : config.locale_failed,config);
      node.setAttribute('aria-busy','false');
    }
  }
}

function finish(node,text,language) {
  if (node.dataset.markdown==='true') { node.classList.add('auto-beautify'); renderReport(node,text); }
  else node.textContent=text;
  node.dataset.localizedLanguage=language; node.removeAttribute('data-locale-pending');
  node.setAttribute('aria-busy','false');
}

const raw=typeof document!=='undefined' ? document.getElementById('site-preferences-config') : null;
if (raw?.textContent?.trim().startsWith('{')) {
  const config=JSON.parse(raw.textContent);
  const scan=() => localizeElements([...document.querySelectorAll('[data-localize]')],config);
  scan();
  if (typeof MutationObserver!=='undefined') {
    let scheduled;
    new MutationObserver(() => { clearTimeout(scheduled); scheduled=setTimeout(scan,100); }).observe(document.body,{childList:true,subtree:true});
  }
}
