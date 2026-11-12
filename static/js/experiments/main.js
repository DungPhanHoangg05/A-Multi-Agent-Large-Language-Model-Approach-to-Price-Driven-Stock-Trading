import {byId} from './dom.js';
import {renderer} from './view.js';

const config = JSON.parse(byId('research-config').textContent), text = config.messages;
const render = renderer(config);
let runs = [], offset = 0, controller = null, legacyData = null;

// Hủy request trước khi đổi run/filter để response cũ không ghi đè lựa chọn mới.
async function json(url, signal) {
  const response = await fetch(url, {signal});
  if (!response.ok) throw new Error(text.failed);
  return response.json();
}
function clear() {
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
  byId('research-filters').hidden = !isResearch; byId('legacy-filter').hidden = isResearch;
  try {
    if (isResearch) {
      const query = parameters();
      const data = await json(`/api/research-results/${encodeURIComponent(run.id)}?${query}`, signal);
      if (signal.aborted) return;
      render.research(data, query);
    } else {
      const data = await json(`/api/experiments/${encodeURIComponent(run.id)}`, signal);
      if (signal.aborted) return;
      legacyData = data; render.legacy(data, run.id);
    }
    byId('state').textContent = text.complete;
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
    const option = new Option(`${text[run.kind]} · ${run.label}`, run.id);
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
  runs = catalog.runs; selectRuns(catalog.default);
} catch {
  clear(); byId('state').textContent = text.failed; byId('error').textContent = text.failed;
}
