import {byId,element,json,jobUrl,blockerText} from '../analysis/common.js';

export function formController(config,io=json,navigate=url => location.assign(url)) {
  const text = config.messages;
  let defaults,grant,generation=0,abort,timer,starting=false;
  function request() {
    const ids = name => [...document.querySelectorAll(`input[name="${name}"]:checked`)].map(node => node.value);
    const models = structuredClone(defaults.models);
    for (const role of ['decision','pattern','trend']) {
      models[role].options.temperature = Number(byId('bt-'+role+'-temperature').value);
      models[role].options.max_tokens = Number(byId('bt-'+role+'-tokens').value);
    }
    return {version:'variant_serving_v1',mode:'backtest',variant_ids:ids('bt-variant'),symbols:ids('bt-symbol'),
      start_date:byId('bt-start').value,end_date:byId('bt-end').value,timeframe:'1d',language:byId('bt-language').value,
      repeats:Number(byId('bt-repeats').value),models};
  }
  async function check() {
    cancel(); const mine = generation; abort = new AbortController(); const signal = abort.signal;
    byId('bt-start-error').textContent = '';
    if (!defaults || starting) return;
    byId('bt-preflight').textContent = text.waiting;
    try {
      const spec = request();
      const data = await io('/api/serving/v1/preflight',spec,signal);
      if (mine !== generation || signal.aborted) return;
      if (data.run_enabled && data.status === 'ready') {
        grant = structuredClone(spec); byId('bt-start-job').disabled = false;
        byId('bt-preflight').textContent = `${text.ready} · ${text.points}: ${data.points.length} · ${text.slots}: ${data.planned_decision_slots} · ${text.attempts} ≤ ${data.estimated_max_api_attempts}`;
      } else byId('bt-preflight').textContent = (data.blockers ?? []).map(row => blockerText(row,text)).join(' · ');
    } catch { if (mine === generation && !signal.aborted) byId('bt-preflight').textContent = text.failed; }
  }
  function cancel() { ++generation; abort?.abort(); clearTimeout(timer); grant = undefined; byId('bt-start-job').disabled = true; }
  function invalidate() { cancel(); byId('bt-preflight').textContent = text.unchecked; if (!starting) timer = setTimeout(check,350); }
  async function start(event) {
    event?.preventDefault(); if (starting || !grant) return;
    const spec = structuredClone(grant); starting = true; cancel();
    const controls = [...document.querySelectorAll('#bt-form input, #bt-form select')]; controls.forEach(node => node.disabled = true);
    try {
      const data = await io('/api/serving/v1/jobs',spec); jobUrl(data.run_id,config.language);
      try { localStorage.setItem('qa_last_backtest',data.run_id); } catch {}
      navigate('/backtest?'+new URLSearchParams({run_id:data.run_id,lang:config.language}));
    } catch (error) { byId('bt-start-error').textContent = error.status === 409 ?
      (error.data?.blockers ?? []).map(row => blockerText(row,text)).join(' · ') || text.failed : text.start_unknown;
    } finally { starting = false; controls.forEach(node => node.disabled = false); }
  }
  async function init() {
    byId('bt-form').addEventListener('submit',start); byId('bt-form').addEventListener('input',invalidate);
    byId('bt-form').addEventListener('change',invalidate); byId('bt-check').addEventListener('click',check);
    try { const previous = localStorage.getItem('qa_last_backtest');
      if (previous) { jobUrl(previous,config.language); byId('bt-last').href = '/backtest?'+new URLSearchParams({run_id:previous,lang:config.language}); byId('bt-last').hidden = false; }
    } catch {}
    try {
      defaults = await io('/api/serving/v1/defaults');
      for (const role of ['decision','pattern','trend']) {
        const section = element('div'); section.append(element('h4',text[role+'_model']),element('p',defaults.models[role].model));
        for (const [key,suffix,min,max,step] of [['temperature','temperature',0,2,.1],['max_tokens','tokens',1,role === 'decision' ? 2048 : 1024,1]]) {
          const field = element('label',text[key],'serving-field'), input = element('input');
          Object.assign(input,{id:'bt-'+role+'-'+suffix,type:'number',min,max,step,value:defaults.models[role].options[key],required:true});
          field.append(input); section.append(field);
        }
        byId('bt-models').append(section);
      }
      await check();
    } catch { byId('bt-start-error').textContent = text.failed; }
  }
  return {init,check,start,invalidate,cancel};
}
