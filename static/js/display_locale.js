import {renderReport,normalizeIndicator} from './analysis/report.js';
import {displayWithoutTaskCodes} from './analysis/common.js';

// Chỉ dựng dữ liệu đã có trong HTML; tuyệt đối không fetch/POST hoặc khởi động dịch.
export function renderStoredReports(root=document) {
  const nodes=[...(root.matches?.('[data-localize]') ? [root]:[]),...root.querySelectorAll('[data-localize]')];
  for (const node of nodes) {
    const raw = displayWithoutTaskCodes(node.textContent);
    if (node.dataset.markdown==='true') { node.classList.add('auto-beautify'); renderReport(node,node.id==='indicatorContent' ? normalizeIndicator(raw) : raw); }
    else if (raw !== node.textContent) node.textContent = raw;
    node.removeAttribute('data-locale-pending'); node.setAttribute('aria-busy','false');
  }
}

export function switchStoredLanguage(language,doc=document,historyApi=history,locationApi=location) {
  const template=doc.getElementById('report-view-'+language),view=doc.getElementById('localized-report-view');
  if (!template || !view) return false;
  const open = [...(view.querySelectorAll?.('details') ?? [])].map(node => node.open);
  view.replaceChildren(template.content.cloneNode(true));
  view.querySelectorAll?.('details').forEach((node,index) => { node.open = open[index] ?? false; });
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

function localeControls(root) {
  return [...root.querySelectorAll('select[id], input[id][type="date"], input[id][type="number"], input[type="checkbox"][name]')];
}

function localeControlKey(node) {
  return node.type === 'checkbox' ? node.name+':'+node.value : node.id;
}

function localeStorageKey(root, url) {
  const page = new URL(url); page.searchParams.delete('lang'); page.searchParams.sort();
  return 'qa_locale_controls:'+page.pathname+page.search+':'+root.id;
}

export function restoreLocaleControls(root) {
  if (!root?.matches?.('[data-preserve-locale]')) return false;
  try {
    const key = localeStorageKey(root, location.href);
    const stored = sessionStorage.getItem(key);
    if (!stored) return false;
    const saved = JSON.parse(stored);
    for (const node of localeControls(root)) {
      const value = saved[localeControlKey(node)];
      if (node.type === 'checkbox' && typeof value === 'boolean') node.checked = value;
      else if (typeof value === 'string' && (node.tagName !== 'SELECT' || [...node.options].some(option => option.value === value))) node.value = value;
    }
    sessionStorage.removeItem(key);
    return true;
  } catch { return false; }
}

if (typeof document!=='undefined' && document.documentElement) {
  renderStoredReports();
  for (const link of document.querySelectorAll('.site-language a[lang]')) link.addEventListener('click',event=>{
    if (event.defaultPrevented || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    if (switchStoredLanguage(link.lang)) { event.preventDefault(); return; }
    try {
      for (const root of document.querySelectorAll('[data-preserve-locale]')) {
        const data = Object.fromEntries(localeControls(root).map(node => [localeControlKey(node), node.type === 'checkbox' ? node.checked : node.value]));
        sessionStorage.setItem(localeStorageKey(root, link.href), JSON.stringify(data));
      }
    } catch { /* Liên kết ngôn ngữ tiếp tục hoạt động nếu storage bị chặn. */ }
  });
  if (typeof MutationObserver!=='undefined') new MutationObserver(records=>{
    for (const record of records) for (const node of record.addedNodes) if (node.nodeType===1 && (node.matches?.('[data-locale-pending]') || node.querySelector('[data-locale-pending]'))) renderStoredReports(node);
  }).observe(document.body,{childList:true,subtree:true});
}
