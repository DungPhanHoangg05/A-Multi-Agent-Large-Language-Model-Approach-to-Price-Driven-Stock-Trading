import {byId, element, label, json, jobUrl, requestFor, blockerText} from './common.js';

// Mỗi lần sửa form hủy grant cũ; chỉ response đúng generation mới được bật nút chạy.
export function formController(config, io = json, navigate = url => location.assign(url)) {
  const text = config.messages;
  let defaults, generation = 0, abort, timer, starting = false, legacyLoaded = false, legacyBusy = false;
  let snapshot, captureAbort, captureGeneration = 0, capturing = false;
  const grants = new Map();
  const latest = () => byId('analysis-source').value === 'latest';
  const legacy = () => byId('analysis-source').value === 'legacy';
  const api = () => latest() ? '/api/serving/live/v1' : '/api/serving/v1';
  function buttons() {
    byId('analyzeBtn').disabled = starting || capturing || legacyBusy || (!legacy() && !grants.has('analyze'));
    byId('compareBtn').disabled = starting || capturing || legacy() || !grants.has('compare');
    byId('compareBtn').hidden = legacy();
    byId('capture-live').disabled = starting || capturing;
  }
  function values(mode) {
    return {mode, ids:mode === 'analyze' ? [byId('analysis-version').value] :
      [...document.querySelectorAll('input[name="compare-method"]:checked')].map(node => node.value),
      symbol:byId('asof-symbol').value, date:latest() ? snapshot?.cutoff : byId('asof-date').value,
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
    if (legacy() || !defaults || starting || capturing) return;
    if (latest() && (!snapshot || snapshot.symbol !== byId('asof-symbol').value)) {
      byId('preflight-status').textContent = text.live_unloaded; return;
    }
    byId('preflight-status').textContent = text.waiting;
    const results = await Promise.all(['analyze','compare'].map(async mode => {
      try {
        const base = requestFor(values(mode),models());
        const request = latest() ? {version:'variant_serving_live_v1',snapshot_id:snapshot.snapshot_id,request:base} : base;
        const data = await io(api()+'/preflight',request,signal);
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
    ++captureGeneration; captureAbort?.abort(); capturing = false;
    if (snapshot?.symbol !== byId('asof-symbol').value) {
      snapshot = undefined; byId('live-input-status').textContent = text.live_unloaded;
    }
    buttons();
    byId('preflight-status').textContent = text.unchecked;
    clearTimeout(timer);
    if (!legacy() && !starting && (!latest() || snapshot)) timer = setTimeout(check,350);
  }
  function source() {
    document.querySelectorAll('[data-legacy-only]').forEach(node => node.hidden = !legacy());
    byId('asof-inputs').hidden = legacy(); byId('legacy-inputs').hidden = !legacy();
    byId('legacy-note').hidden = !legacy();
    for (const id of ['live-note','live-input-status','capture-live']) byId(id).hidden = !latest();
    byId('asof-date-field').hidden = latest(); byId('asof-date').disabled = latest();
    if (legacy() && !legacyLoaded) { window.legacyAnalysis.load(); legacyLoaded = true; }
    invalidate();
  }
  async function capture() {
    if (!latest() || starting || capturing) return;
    ++generation; abort?.abort(); clearTimeout(timer); grants.clear(); snapshot = undefined;
    const mine = ++captureGeneration, symbol = byId('asof-symbol').value;
    captureAbort?.abort(); captureAbort = new AbortController();
    capturing = true; buttons(); byId('live-input-status').textContent = text.live_loading;
    byId('serving-form-error').textContent = '';
    try {
      const data = await io('/api/serving/live/v1/snapshot',{symbol},captureAbort.signal);
      if (mine !== captureGeneration || !latest() || symbol !== byId('asof-symbol').value) return;
      if (data.symbol !== symbol || !/^[0-9a-f]{64}$/.test(data.snapshot_id) || !/^\d{4}-\d{2}-\d{2}$/.test(data.cutoff)) throw new Error('Invalid capture');
      snapshot = structuredClone(data);
      byId('live-input-status').textContent = `${text.live_captured}: ${data.symbol} · ${data.cutoff} · ${data.price_rows} · ${data.captured_at}`;
      capturing = false; await check();
    } catch (error) {
      if (mine === captureGeneration) {
        byId('live-input-status').textContent = text.live_failed;
        byId('serving-form-error').textContent = text.live_failed;
      }
    } finally { if (mine === captureGeneration) { capturing = false; buttons(); } }
  }
  async function start(mode) {
    if (starting) return;
    if (legacy()) { if (mode === 'analyze') window.legacyAnalysis.run(); return; }
    const request = grants.get(mode);
    if (!request) return;
    starting = true; ++generation; abort?.abort(); clearTimeout(timer); grants.clear(); buttons();
    const controls = [...document.querySelectorAll('#asof-inputs input, #asof-inputs select, #analysis-source')];
    controls.forEach(node => node.disabled = true);
    try {
      const sourceName = latest() ? 'live' : 'asof';
      const data = await io(api()+'/jobs',structuredClone(request));
      const url = jobUrl(data.run_id,config.language,sourceName);
      try { localStorage.setItem('qa_last_serving_job',data.run_id); localStorage.setItem('qa_last_serving_source',sourceName); } catch {}
      navigate(url);
    } catch (error) {
      byId('serving-form-error').textContent = error.status === 409 ?
        (error.data?.blockers ?? []).map(b => blockerText(b,text)).join(' · ') || text.failed : text.start_unknown;
    } finally {
      starting = false; controls.forEach(node => node.disabled = false); byId('asof-date').disabled = latest(); buttons();
    }
  }
  async function init() {
    source(); buttons(); description();
    byId('capture-live').addEventListener('click',capture);
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
      if (previous) { byId('last-serving-job').href = jobUrl(previous,config.language,localStorage.getItem('qa_last_serving_source')); byId('last-serving-job').hidden = false; }
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
  return {init,check,start,invalidate,source,capture};
}
if (byId('analysis-config')) formController(JSON.parse(byId('analysis-config').textContent)).init();
