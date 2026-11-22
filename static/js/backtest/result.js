import {byId,element,json,jobUrl,label} from '../analysis/common.js';
import {renderer} from './view.js';
import {restoreLocaleControls} from '../display_locale.js?v=bilingual-v1';

// Một controller dùng cho /backtest và /experiments; GET/poll không tự start/resume.
export function resultController(config,io=json,schedule=setTimeout,cancel=clearTimeout) {
  const view = renderer(config), text = config.messages;
  let runId,kind,generation=0,timer,abort,initialized=false,controlling=false;
  const endpoint = () => kind === 'legacy_backtest' ? '/api/serving/v1/legacy-backtests/'+encodeURIComponent(runId) :
    '/api/serving/v1/jobs/'+encodeURIComponent(runId)+'/evaluation';
  function stop() { ++generation; abort?.abort(); cancel(timer); }
  function parameters() {
    if (!initialized || kind === 'legacy_backtest') return '';
    const methods = [...document.querySelectorAll('input[name="bt-filter-method"]:checked')].map(node => node.value);
    if (!methods.length) throw new Error(text.select_methods);
    return new URLSearchParams({methods:methods.join(','),symbol:byId('bt-filter-symbol').value,repeat:byId('bt-filter-repeat').value,
      baseline:byId('bt-filter-baseline').value,start_date:byId('bt-filter-start').value,end_date:byId('bt-filter-end').value}).toString();
  }
  function options(id,values) {
    byId(id).replaceChildren(...values.map(([value,title]) => { const node = element('option',title); node.value = value; return node; }));
    byId(id).value = values[0]?.[0] ?? '';
  }
  function setup(data) {
    if (initialized || kind === 'legacy_backtest') return false;
    byId('bt-method-filters').replaceChildren(...data.execution_plan.map(id => {
      const node = element('label'),input = element('input'); input.type = 'checkbox'; input.name = 'bt-filter-method'; input.value = id;
      input.checked = data.request.variant_ids.includes(id); node.append(input,element('span',label(config,id))); return node;
    }));
    options('bt-filter-symbol',[['all',text.all],...data.request.symbols.map(symbol => [symbol,symbol])]);
    options('bt-filter-repeat',[['all',text.all],...Array.from({length:data.request.repeats},(_,i) => [String(i),String(i+1)])]);
    options('bt-filter-baseline',[['none',text.none],...['original_fix','original_common'].filter(id => data.execution_plan.includes(id)).map(id => [id,label(config,id)])]);
    byId('bt-filter-baseline').value = data.filters.baseline;
    for (const [id,key] of [['bt-filter-start','start_date'],['bt-filter-end','end_date']]) {
      byId(id).value = data.request[key]; byId(id).min = data.request.start_date; byId(id).max = data.request.end_date;
    }
    initialized = true;
    return restoreLocaleControls(byId('bt-result-filters'));
  }
  async function refresh() {
    stop(); const mine = generation; abort = new AbortController();
    if (!runId) return;
    try {
      if (kind === 'serving_backtest') jobUrl(runId,config.language);
      const query = parameters();
      const data = await io(endpoint()+(query ? '?'+query : ''),undefined,abort.signal);
      if (mine !== generation) return;
      if (data.run_id !== runId || data.kind !== kind) throw new Error(text.failed);
      if (setup(data)) return refresh();
      view.render(data,endpoint(),query);
      if (kind === 'serving_backtest' && ['queued','running','partial','stop_requested'].includes(data.status) && data.worker_alive)
        timer = schedule(refresh,3000);
    } catch (error) { if (mine === generation) view.error(error.message === text.select_methods ? error.message : error.status === 404 ? text.read_error : text.failed); }
  }
  async function select(id,source='serving_backtest') {
    stop(); view.clear(); runId = id; kind = source; initialized = false;
    if (!id) { byId('bt-result').hidden = true; return; }
    return refresh();
  }
  async function control(action) {
    if (controlling || byId('bt-'+action).disabled || kind !== 'serving_backtest') return;
    controlling = true; stop(); byId('bt-stop').disabled = byId('bt-resume').disabled = true;
    try { await io('/api/serving/v1/jobs/'+encodeURIComponent(runId)+'/'+action,{}); await refresh(); }
    catch { view.error(text.failed); }
    finally { controlling = false; }
  }
  function init() {
    byId('bt-result-filters').addEventListener('submit',event => { event.preventDefault(); refresh(); });
    byId('bt-result-filters').addEventListener('change',() => { stop(); view.clear(); timer = schedule(refresh,250); });
    byId('bt-refresh').addEventListener('click',refresh);
    byId('bt-stop').addEventListener('click',() => control('stop')); byId('bt-resume').addEventListener('click',() => control('resume'));
    byId('bt-chart-account').addEventListener('change',view.charts);
  }
  return {init,select,refresh,stop,control};
}
