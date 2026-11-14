import {renderReport,normalizeIndicator} from './analysis/report.js';

// Chỉ dựng dữ liệu đã có trong HTML; tuyệt đối không fetch/POST hoặc khởi động dịch.
export function renderStoredReports(root=document) {
  const nodes=[...(root.matches?.('[data-localize]') ? [root]:[]),...root.querySelectorAll('[data-localize]')];
  for (const node of nodes) {
    const raw=node.id==='indicatorContent' ? normalizeIndicator(node.textContent) : node.textContent;
    if (node.dataset.markdown==='true') { node.classList.add('auto-beautify'); renderReport(node,raw); }
    node.removeAttribute('data-locale-pending'); node.setAttribute('aria-busy','false');
  }
}

export function switchStoredLanguage(language,doc=document,historyApi=history,locationApi=location) {
  const template=doc.getElementById('report-view-'+language),view=doc.getElementById('localized-report-view');
  if (!template || !view) return false;
  view.replaceChildren(template.content.cloneNode(true));
  doc.documentElement.lang=language; doc.title=template.dataset.title;
  doc.cookie='qa_lang='+language+'; Max-Age=31536000; Path=/; SameSite=Lax';
  const url=new URL(locationApi.href); url.searchParams.set('lang',language); historyApi.replaceState(null,'',url);
  for (const link of doc.querySelectorAll('.site-language a[lang]')) {
    if (link.lang===language) link.setAttribute('aria-current','true'); else link.removeAttribute('aria-current');
    const target=new URL(link.href,locationApi.href); target.searchParams.set('lang',link.lang); link.href=target;
  }
  const button=doc.getElementById('theme-toggle');
  if (button) {
    const dark=doc.documentElement.dataset.theme==='dark';
    button.textContent=language==='en' ? dark ? 'Light mode' : 'Dark mode' : dark ? 'Chế độ sáng' : 'Chế độ tối';
    button.setAttribute('aria-label',language==='en' ? 'Dark mode' : 'Chế độ tối');
  }
  doc.querySelector?.('.site-preferences')?.setAttribute('aria-label',language==='en'?'Navigation':'Điều hướng');
  const raw=doc.getElementById('site-preferences-config');
  if (raw) { const config=JSON.parse(raw.textContent); config.language=language; config.dark=language==='en'?'Dark mode':'Chế độ tối'; config.light=language==='en'?'Light mode':'Chế độ sáng'; raw.textContent=JSON.stringify(config); }
  renderStoredReports(view); return true;
}

if (typeof document!=='undefined') {
  renderStoredReports();
  for (const link of document.querySelectorAll('.site-language a[lang]')) link.addEventListener('click',event=>{
    if (!event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey && switchStoredLanguage(link.lang)) event.preventDefault();
  });
  if (typeof MutationObserver!=='undefined') new MutationObserver(records=>{
    for (const record of records) for (const node of record.addedNodes) if (node.nodeType===1 && (node.matches?.('[data-locale-pending]') || node.querySelector('[data-locale-pending]'))) renderStoredReports(node);
  }).observe(document.body,{childList:true,subtree:true});
}
