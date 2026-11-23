import {byId,json,requestFor} from './common.js';
import {startLive,submitServing} from './timeframe.js';
import {resultController} from './result.js';
import {comparisonView, isPairedResult} from './comparison_view.js';
import {restoreLocaleControls} from '../display_locale.js?v=bilingual-v1';

export function comparisonForm(config,io=json,navigate=url=>location.assign(url)) {
  const text=config.messages, registry=config.registry;
  let defaults, starting=false, uncertain=false, displayLanguage=config.language;
  const main=new Set(registry.variants.filter(variant=>variant.group==='main').map(variant=>variant.id));
  const selectors=['compare-first','compare-second','compare-symbol','compare-symbol-search','compare-source','compare-date'];

  function supported() {
    return byId('compare-source').value !== 'history' || registry.domain.released_symbols.includes(byId('compare-symbol').value);
  }

  function filterSymbols() {
    const select=byId('compare-symbol');
    const query=byId('compare-symbol-search').value.trim().toUpperCase();
    for (const option of select.options) {
      option.hidden=option.value!==select.value && !option.textContent.toUpperCase().includes(query);
    }
  }

  function update() {
    const historical=byId('compare-source').value==='history';
    byId('compare-date-field').hidden=!historical;
    for (const id of selectors) byId(id).disabled=starting || (id==='compare-date' && !historical);
    byId('compare-date').required=historical;
    byId('compare-source-note').textContent=historical ? text.history_outcome_note : text.live_outcome_note;
    const available=supported();
    const support=byId('compare-support');
    support.hidden=available;
    support.textContent=available ? '' : `${text.asset_unavailable} · ${registry.domain.released_symbols.join(', ')}.`;
    byId('compare-start').disabled=starting || uncertain || !defaults || !available;
    byId('compare-form').setAttribute('aria-busy',String(starting));
  }

  async function start(event) {
    event?.preventDefault();
    if (starting || uncertain || !defaults) return;
    const ids=[byId('compare-first').value,byId('compare-second').value];
    const symbol=byId('compare-symbol').value, source=byId('compare-source').value;
    const date=byId('compare-date').value;
    const status=message=>{ byId('compare-status').textContent=message; };
    if (ids[0]===ids[1] || !ids.every(id=>main.has(id))) return status(text.distinct);
    if (!supported()) { update(); return; }
    if (source==='history' && (!/^\d{4}-\d{2}-\d{2}$/.test(date) || !registry.domain.released_date_ranges.some(
      range=>range.start_date<=date && date<=range.end_date))) return status(text.invalid_date);
    starting=true; update();
    const selection={ids,symbol,date,version:registry.default_profile,language:config.language,repeats:1,timeframe:'1d'};
    try {
      const runId=source==='history'
        ? await submitServing(config,'/api/serving/v1',requestFor({...selection,mode:'backtest'},defaults.models),io,status)
        : await startLive(config,{...selection,mode:'compare'},defaults.models,io,status);
      navigate('/compare?'+new URLSearchParams({run_id:runId,source,lang:displayLanguage}));
    } catch(error) {
      uncertain=error.message===text.start_unknown;
      status(error.message || text.failed);
    } finally { starting=false; update(); }
  }

  async function init() {
    const form=byId('compare-form');
    restoreLocaleControls(form);
    form.addEventListener('submit',start);
    byId('compare-source').addEventListener('change',update);
    byId('compare-symbol').addEventListener('change',() => { filterSymbols(); update(); });
    byId('compare-symbol-search').addEventListener('input',filterSymbols);
    document.addEventListener('click',event=>{
      const link=event.target.closest?.('.site-language a[lang]');
      if (starting && link && !event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey) {
        event.preventDefault(); displayLanguage=link.lang;
      }
    },true);
    update();
    try { defaults=await io('/api/serving/v1/defaults'); }
    catch { byId('compare-status').textContent=text.failed; }
    update();
  }
  return {init,start};
}

const startup=byId('compare-config');
if (startup) {
  const config=JSON.parse(startup.textContent);
  if (config.runId) {
    resultController(config,undefined,undefined,undefined,{
      view:comparisonView(config),accepts:data=>isPairedResult(data,config),
    }).init();
  } else comparisonForm(config).init();
}
