import {renderReport,normalizeIndicator} from './analysis/report.js';

const active=new WeakSet();
const vietnamese=/[ăâđêôơưĂÂĐÊÔƠƯ\u1ea0-\u1ef9]/u;
const delay=ms => new Promise(resolve => setTimeout(resolve,ms));

export function needsTranslation(text,target,source) {
  return target==='en' ? source==='vi' || vietnamese.test(text) : source==='en';
}

async function request(url,body) {
  const response=await fetch(url,{method:body ? 'POST' : 'GET',headers:body ? {'Content-Type':'application/json'} : {},body:body ? JSON.stringify(body) : undefined});
  const data=await response.json(); if (!response.ok) throw new Error('LOCALIZATION_FAILED'); return data;
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
      const id='n'+pending.length; texts[id]=raw; pending.push({id,node});
      node.setAttribute('data-locale-pending','');
    } else finish(node,raw,config.language);
  }
  if (!pending.length) return;
  const status=document.getElementById('display-locale-status');
  if (status) { status.hidden=false; status.textContent=config.preparing; }
  try {
    let result=await io('/api/display-locales',{target:config.language,texts});
    while (['queued','running'].includes(result.state)) {
      if (!/^[0-9a-f-]{36}$/.test(result.id)) throw new Error('Invalid translation ID');
      await pause(1500); result=await io('/api/display-locales/'+encodeURIComponent(result.id));
    }
    if (result.state!=='completed' || result.target!==config.language || Object.keys(result.texts ?? {}).length!==pending.length) throw new Error(result.state==='unknown' ? 'UNKNOWN' : 'LOCALIZATION_FAILED');
    for (const {id,node} of pending) {
      if (typeof result.texts[id]!=='string') throw new Error('Incomplete translation');
      finish(node,result.texts[id],config.language);
    }
    if (status) status.hidden=true;
  } catch (error) {
    if (status) { status.hidden=false; status.textContent=error.message==='UNKNOWN' ? config.locale_unknown : config.locale_failed; }
    // Không fallback sang tiếng Việt trên trang EN khi API/key không khả dụng.
    for (const {node} of pending) { node.textContent=config.locale_failed; node.removeAttribute('data-locale-pending'); }
  }
}

function finish(node,text,language) {
  if (node.dataset.markdown==='true') { node.classList.add('auto-beautify'); renderReport(node,text); }
  else node.textContent=text;
  node.dataset.localizedLanguage=language; node.removeAttribute('data-locale-pending');
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
