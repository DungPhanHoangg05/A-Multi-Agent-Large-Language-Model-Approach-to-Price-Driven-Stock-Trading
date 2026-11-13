import {byId} from './dom.js';
import {renderer} from './view.js';
import {resultController} from '../backtest/result.js';

const config = JSON.parse(byId('research-config').textContent), text = config.messages;
const render = renderer(config);
let runs = [], offset = 0, controller = null, legacyData = null;
const backtest = resultController({messages:config.backtestMessages,language:config.language,registry:config.registry});
backtest.init();

// Hủy request trước khi đổi run/filter để response cũ không ghi đè lựa chọn mới.
async function json(url, signal) {
  const response = await fetch(url, {signal});
  if (!response.ok) throw new Error(text.failed);
  return response.json();
}
function clear() {
  backtest.stop(); byId('bt-result').hidden = true;
  byId('bt-downloads').replaceChildren();
  byId('research-result').hidden = true; byId('legacy-result').hidden = true;
  byId('downloads').replaceChildren(); byId('legacy-downloads').replaceChildren();
  byId('empty').hidden = true; byId('error').textContent = ''; legacyData = null;
}
function parameters() {
  const methods = [...document.querySelectorAll('input[name="method"]:checked')].map(node => node.value);
  if (!methods.length) throw new Error(text.choose);
  return new URLSearchParams({methods: methods.join(','), baseline: byId('baseline').value,
    repeat: byId('repeat').value, symbol: byId('symbol').value, fold: byId('fold').value,
    table: byId('table').value, offset: String(offset), limit: '50'});
}
async function load() {
  controller?.abort(); controller = new AbortController();
  const signal = controller.signal;
  clear(); byId('state').textContent = text.loading;
  byId('research-result').setAttribute('aria-busy', 'true');
  const run = runs.find(r => r.id === byId('run').value && r.kind === byId('run').selectedOptions[0]?.dataset.kind);
  if (!run) {
    byId('empty').hidden = false; byId('state').textContent = text.empty;
    byId('research-result').setAttribute('aria-busy', 'false'); return;
  }
  const isResearch = run.kind === 'paper_evidence';
  const isBacktest = ['serving_backtest','legacy_backtest'].includes(run.kind);
  byId('research-filters').hidden = !isResearch; byId('legacy-filter').hidden = isResearch || isBacktest;
  try {
    if (isBacktest) {
      await backtest.select(run.id,run.kind);
      if (signal.aborted) return;
    } else if (isResearch) {
      const query = parameters();
      const data = await json(`/api/research-results/${encodeURIComponent(run.id)}?${query}`, signal);
      if (signal.aborted) return;
      render.research(data, query);
    } else {
      const data = await json(`/api/experiments/${encodeURIComponent(run.id)}`, signal);
      if (signal.aborted) return;
      legacyData = data; render.legacy(data, run.id);
    }
    byId('state').textContent = isBacktest ? config.backtestMessages[run.kind === 'serving_backtest' ? 'new_backtest' : run.kind] : text.complete;
  } catch (error) {
    if (error.name === 'AbortError' || signal.aborted) return;
    clear();
    byId('error').textContent = error.message; byId('state').textContent = text.failed;
  } finally {
    if (!signal.aborted) byId('research-result').setAttribute('aria-busy', 'false');
  }
}
function selectRuns(defaultId) {
  const kind = byId('kind').value, filtered = runs.filter(run => kind === 'all' || run.kind === kind);
  byId('run').replaceChildren(...filtered.map(run => {
      const option = new Option(`${text[run.kind] ?? config.backtestMessages?.[run.kind === 'serving_backtest' ? 'new_backtest' : run.kind]} · ${run.label}`, run.id);
    option.dataset.kind = run.kind; return option;
  }));
  if (filtered.some(r => r.id === defaultId)) byId('run').value = defaultId;
  offset = 0; load();
}
byId('filters').addEventListener('submit', event => { event.preventDefault(); offset = 0; load(); });
byId('detail-filters').addEventListener('submit', event => { event.preventDefault(); offset = 0; load(); });
byId('kind').addEventListener('change', () => selectRuns('u09_analysis_r1'));
byId('run').addEventListener('change', () => { offset = 0; load(); });
byId('prev').addEventListener('click', () => { offset = Math.max(0, offset - 50); load(); });
byId('next').addEventListener('click', () => { offset += 50; load(); });
byId('variant').addEventListener('change', () => { if (legacyData) render.legacy(legacyData, byId('run').value); });
try {
  const catalog = await json('/api/research-results/runs');
  const extra = await Promise.allSettled(['/api/serving/v1/jobs','/api/serving/v1/legacy-backtests'].map(url => json(url)));
  byId('bt-catalog-error').textContent = extra.some(result => result.status === 'rejected') ? config.backtestMessages?.failed ?? text.failed : '';
  runs = [...catalog.runs,...extra.flatMap(result => result.status === 'fulfilled' ? result.value.runs ?? [] : [])];
  const query = new URLSearchParams(location.search);
  if (['serving_backtest','legacy_backtest'].includes(query.get('kind'))) byId('kind').value = query.get('kind');
  selectRuns(query.get('run_id') ?? catalog.default);
} catch {
  clear(); byId('state').textContent = text.failed; byId('error').textContent = text.failed;
}
