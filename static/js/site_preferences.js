// Khởi tạo trước khi paint, dùng cùng lựa chọn trên mọi trang và tab.
(() => {
  let saved;
  try { saved=localStorage.getItem('qa_theme'); } catch {}
  const media=typeof matchMedia==='function' ? matchMedia('(prefers-color-scheme: dark)') : {matches:false};
  const root=document.documentElement;
  root.classList.add('has-js');
  function apply(theme) {
    root.dataset.theme=theme; root.style.colorScheme=theme;
    const button=document.getElementById('theme-toggle'), raw=document.getElementById('site-preferences-config');
    if (!button || !raw) return;
    const labels=JSON.parse(raw.textContent);
    button.textContent=theme==='dark' ? labels.light : labels.dark;
    button.setAttribute('aria-pressed',String(theme==='dark'));
    button.setAttribute('aria-label',labels.dark);
  }
  apply(saved==='dark' || saved==='light' ? saved : media.matches ? 'dark' : 'light');
  document.addEventListener('DOMContentLoaded',() => {
    apply(root.dataset.theme);
    document.getElementById('theme-toggle')?.addEventListener('click',() => {
      saved=root.dataset.theme==='dark' ? 'light' : 'dark'; apply(saved);
      try { localStorage.setItem('qa_theme',saved); } catch {}
    });
  });
  globalThis.addEventListener?.('storage',event => {
    if (event.key==='qa_theme') { saved=event.newValue; apply(saved==='dark' ? 'dark' : 'light'); }
  });
  media.addEventListener?.('change',event => { if (!saved) apply(event.matches ? 'dark' : 'light'); });
})();
