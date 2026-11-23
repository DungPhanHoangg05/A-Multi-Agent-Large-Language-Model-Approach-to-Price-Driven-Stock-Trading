import {byId,json} from './common.js';
import {runTimeframe} from './timeframe.js';
import {followAnalysis,showAgentProgress,showAgentSteps} from './progress.js';
import {restoreLocaleControls} from '../display_locale.js?v=bilingual-v1';

// Chọn phương pháp phân tích; phiên bản chạy do cấu hình máy chủ xác định.
export function formController(config, io = json, navigate = url => location.assign(url), pause) {
  const text = config.messages;
  let defaults, starting = false, uncertain = false;
  let displayLanguage = config.language, phase, progress;
  const progressConfig = {...config};
  function chooseDisplayLanguage(language) {
    const locale = config.progressLocales?.[language];
    if (!locale) return;
    displayLanguage = language;
    progressConfig.language = language; progressConfig.messages = locale.messages;
    byId('loadingOverlay').lang = language;
    byId('analysis-progress-title').textContent = locale.title;
    locale.steps.forEach((label,index) => {
      const node = byId('step'+(index+1)).querySelector?.('span');
      if (node) node.textContent = label.replaceAll('&amp;','&');
    });
    const bicl = byId('step-bicl').querySelector?.('span');
    if (bicl) bicl.textContent = locale.messages.bicl_step;
    for (const button of document.querySelectorAll('[data-progress-language]'))
      button.setAttribute('aria-pressed',String(button.lang === language));
    if (progress) showAgentProgress(progress,progressConfig);
    else byId('analysis-progress-message').textContent = locale.messages[phase] ?? locale.intro;
  }
  function buttons() {
    byId('analyzeBtn').disabled = starting || uncertain || !defaults;
    byId('analysis-version').disabled = starting;
    byId('legacy-inputs').inert = starting;
  }
  function description() {
    const id = byId('analysis-version').value;
    const summary = id === 'original_fix' ? text.native_description :
      id === 'MT_BICL' ? text.mt_description : text.prior_description;
    byId('version-description').textContent = `${summary} ${text.live_full_catalog}`;
    buttons();
  }
  async function start(mode = 'analyze') {
    if (mode !== 'analyze' || starting || uncertain || !defaults || !window.legacyAnalysis.begin()) return;
    const variant = byId('analysis-version').value;
    const selection = window.legacyAnalysis.selection();
    const status = byId('timeframe-run-status');
    starting = true; buttons(); status.textContent = '';
    phase = undefined; progress = undefined;
    showAgentSteps([variant],{loading:'running'},progressConfig);
    chooseDisplayLanguage(config.language);
    try {
      const chosen = {...selection,timeframe:'1d',version:config.registry.default_profile,variant,language:config.language,repeats:1};
      const result = await runTimeframe(config,chosen,structuredClone(defaults.models),io,
        (value,key) => { phase = key; byId('analysis-progress-message').textContent = progressConfig.messages[key] ?? value; });
      const link = byId('last-serving-job'); link.href = result.url; link.hidden = false;
      try { localStorage.setItem('qa_last_serving_job',result.runId); localStorage.setItem('qa_last_serving_source','live'); } catch {}
      await followAnalysis(progressConfig,result.runId,io,data => { progress = data; showAgentProgress(data,progressConfig); },pause);
      const route = new URL(result.url,'http://localhost'); route.searchParams.set('lang',displayLanguage);
      navigate(route.pathname+route.search);
    } catch (error) {
      uncertain = error.message === text.start_unknown;
      status.textContent = error.message || text.failed;
    } finally { starting = false; window.legacyAnalysis.end(); buttons(); }
  }
  async function init() {
    restoreLocaleControls(byId('analysis-language-fields'));
    for (const button of document.querySelectorAll('[data-progress-language]'))
      button.addEventListener('click',() => chooseDisplayLanguage(button.lang));
    document.querySelectorAll('[data-legacy-only]').forEach(node => node.hidden = false);
    byId('legacy-inputs').hidden = false;
    window.legacyAnalysis.load();
    byId('analyzeBtn').addEventListener('click',() => start());
    byId('analysis-version').addEventListener('change',description);
    description();
    try { defaults = await io('/api/serving/v1/defaults'); }
    catch { byId('timeframe-run-status').textContent = text.failed; }
    buttons();
  }
  return {init,start};
}
if (byId('analysis-config')) formController(JSON.parse(byId('analysis-config').textContent)).init();
