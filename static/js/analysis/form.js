import {byId,json} from './common.js';
import {runTimeframe} from './timeframe.js';
import {followAnalysis,showAgentProgress} from './progress.js';

// Một form realtime 1D; Original giữ đường chạy cũ, bản nâng cấp dùng cùng overlay/kết quả.
export function formController(config, io = json, navigate = url => location.assign(url), pause) {
  const text = config.messages;
  let defaults, starting = false, legacyBusy = false, uncertain = false;
  function buttons() {
    const busy = starting || legacyBusy;
    byId('analyzeBtn').disabled = busy || uncertain || (byId('analysis-version').value !== 'original_fix' && !defaults);
    byId('analysis-version').disabled = busy;
    byId('legacy-inputs').inert = busy;
  }
  function description() {
    const id = byId('analysis-version').value;
    byId('version-description').textContent = id === 'original_fix' ? text.native_description :
      id === 'MT_BICL' ? text.mt_description : text.prior_description;
    buttons();
  }
  async function start(mode = 'analyze') {
    if (mode !== 'analyze' || starting || legacyBusy || uncertain) return;
    if (byId('analysis-version').value === 'original_fix') { window.legacyAnalysis.run(); return; }
    if (!defaults || !window.legacyAnalysis.begin(true)) return;
    starting = true; buttons(); byId('timeframe-run-status').textContent = '';
    try {
      const chosen = {...window.legacyAnalysis.selection(),timeframe:'1d',variant:byId('analysis-version').value,language:config.language,repeats:1};
      const result = await runTimeframe(config,chosen,structuredClone(defaults.models),io,
        value => byId('analysis-progress-message').textContent = value);
      const link = byId('last-serving-job'); link.href = result.url; link.hidden = false;
      try { localStorage.setItem('qa_last_serving_job',result.runId); localStorage.setItem('qa_last_serving_source','live'); } catch {}
      await followAnalysis(config,result.runId,io,data => showAgentProgress(data,config),pause);
      navigate(result.url);
    } catch (error) {
      uncertain = error.message === text.start_unknown;
      byId('timeframe-run-status').textContent = error.message || text.failed;
    } finally { starting = false; window.legacyAnalysis.end(); buttons(); }
  }
  async function init() {
    document.querySelectorAll('[data-legacy-only]').forEach(node => node.hidden = false);
    byId('legacy-inputs').hidden = false;
    window.legacyAnalysis.load();
    byId('analyzeBtn').addEventListener('click',() => start());
    byId('analysis-version').addEventListener('change',description);
    for (const [event,busy] of [['analysis-legacy-start',true],['analysis-legacy-end',false]]) {
      document.addEventListener(event,() => { legacyBusy = busy; buttons(); });
    }
    description();
    try { defaults = await io('/api/serving/v1/defaults'); }
    catch { byId('timeframe-run-status').textContent = text.failed; }
    buttons();
  }
  return {init,start};
}
if (byId('analysis-config')) formController(JSON.parse(byId('analysis-config').textContent)).init();
