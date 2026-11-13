import {byId, element, label, json, jobUrl, requestFor, blockerText} from './common.js';

// Mỗi lần sửa form hủy grant cũ; chỉ response đúng generation mới được bật nút chạy.
export function formController(config, io = json, navigate = url => location.assign(url)) {
  const text = config.messages;
  let defaults, generation = 0, abort, timer, starting = false, legacyLoaded = false, legacyBusy = false;
  const grants = new Map();
  const latest = () => byId('analysis-source').value === 'latest';
  function buttons() {
    byId('analyzeBtn').disabled = starting || legacyBusy || (!latest() && !grants.has('analyze'));
    byId('compareBtn').disabled = starting || latest() || !grants.has('compare');
    byId('compareBtn').hidden = latest();
  }
  function values(mode) {
    return {mode, ids:mode === 'analyze' ? [byId('analysis-version').value] :
      [...document.querySelectorAll('input[name="compare-method"]:checked')].map(node => node.value),
      symbol:byId('asof-symbol').value, date:byId('asof-date').value,
      language:byId('report-language').value, repeats:Number(byId('analysis-repeats').value)};
  }
  function models() {
    const result = structuredClone(defaults.models);
    for (const role of ['decision','pattern','trend']) {
      result[role].options.temperature = Number(byId(role+'-temperature').value);
      result[role].options.max_tokens = Number(byId(role+'-tokens').value);
    }
    return result;
  }
  function description() {
    const id = byId('analysis-version').value;
    byId('version-description').textContent = id === 'original_fix' ? text.native_description :
      id === 'MT_BICL' ? text.mt_description : text.prior_description;
  }
  async function check() {
    clearTimeout(timer);
    abort?.abort(); abort = new AbortController();
    const mine = ++generation, signal = abort.signal;
    grants.clear(); buttons(); byId('serving-form-error').textContent = '';
    if (latest() || !defaults || starting) return;
    byId('preflight-status').textContent = text.waiting;
    const results = await Promise.all(['analyze','compare'].map(async mode => {
      try {
        const request = requestFor(values(mode),models());
        const data = await io('/api/serving/v1/preflight',request,signal);
        if (mine !== generation || signal.aborted) return null;
        if (data.run_enabled && data.status === 'ready') grants.set(mode,structuredClone(request));
        return (mode === 'analyze' ? text.analyze : text.compare)+': '+(data.run_enabled ? text.ready :
          (data.blockers ?? []).map(b => blockerText(b,text)).join(' · '));
      } catch (error) {
        if (mine !== generation || signal.aborted) return null;
        return (mode === 'analyze' ? text.analyze : text.compare)+': '+
          (error.message === 'COMPARE_SELECTION' ? text.choose : text.failed);
      }
    }));
    if (mine === generation && !signal.aborted) {
      byId('preflight-status').replaceChildren(...results.filter(Boolean).map(value => element('p',value)));
      buttons();
    }
  }
  function invalidate() {
    ++generation; abort?.abort(); grants.clear(); buttons(); description();
    byId('preflight-status').textContent = text.unchecked;
    clearTimeout(timer);
    if (!latest() && !starting) timer = setTimeout(check,350);
  }
  function source() {
    document.querySelectorAll('[data-legacy-only]').forEach(node => node.hidden = !latest());
    byId('asof-inputs').hidden = latest(); byId('legacy-inputs').hidden = !latest();
    byId('legacy-note').hidden = !latest();
    if (latest() && !legacyLoaded) { window.legacyAnalysis.load(); legacyLoaded = true; }
    invalidate();
  }
  async function start(mode) {
    if (starting) return;
    if (latest()) { if (mode === 'analyze') window.legacyAnalysis.run(); return; }
    const request = grants.get(mode);
    if (!request) return;
    starting = true; ++generation; abort?.abort(); clearTimeout(timer); grants.clear(); buttons();
    const controls = [...document.querySelectorAll('#asof-inputs input, #asof-inputs select, #analysis-source')];
    controls.forEach(node => node.disabled = true);
    try {
      const data = await io('/api/serving/v1/jobs',structuredClone(request));
      const url = jobUrl(data.run_id,config.language);
      try { localStorage.setItem('qa_last_serving_job',data.run_id); } catch {}
      navigate(url);
    } catch (error) {
      byId('serving-form-error').textContent = error.status === 409 ?
        (error.data?.blockers ?? []).map(b => blockerText(b,text)).join(' · ') || text.failed : text.start_unknown;
    } finally {
      starting = false; controls.forEach(node => node.disabled = false); buttons();
    }
  }
  async function init() {
    buttons(); description();
    byId('preflightBtn').addEventListener('click',check);
    byId('analyzeBtn').addEventListener('click',() => start('analyze'));
    byId('compareBtn').addEventListener('click',() => start('compare'));
    byId('analysis-source').addEventListener('change',source);
    byId('asof-inputs').addEventListener('input',invalidate);
    byId('asof-inputs').addEventListener('change',invalidate);
    document.addEventListener('analysis-key-changed',invalidate);
    for (const [event,busy] of [['analysis-legacy-start',true],['analysis-legacy-end',false]]) {
      document.addEventListener(event,() => { legacyBusy = busy; byId('analysis-source').disabled = busy; buttons(); });
    }
    try {
      const previous = localStorage.getItem('qa_last_serving_job');
      if (previous) { byId('last-serving-job').href = jobUrl(previous,config.language); byId('last-serving-job').hidden = false; }
    } catch {}
    try {
      defaults = await io('/api/serving/v1/defaults');
      const container = byId('serving-models');
      for (const role of ['decision','pattern','trend']) {
        const group = element('div');
        group.append(element('h4',text[role+'_model']),element('p',defaults.models[role].model,'serving-muted'));
        for (const [option,suffix,max,step] of [['temperature','temperature',2,.1],['max_tokens','tokens',role === 'decision' ? 2048 : 1024,1]]) {
          const field = element('label',text[option],'serving-field'), input = element('input');
          Object.assign(input,{id:role+'-'+suffix,type:'number',min:option === 'temperature' ? 0 : 1,max,step,
            value:defaults.models[role].options[option],required:true});
          field.append(input); group.append(field);
        }
        container.append(group);
      }
      await check();
    } catch { byId('serving-form-error').textContent = text.failed; }
  }
  return {init,check,start,invalidate,source};
}
if (byId('analysis-config')) formController(JSON.parse(byId('analysis-config').textContent)).init();
