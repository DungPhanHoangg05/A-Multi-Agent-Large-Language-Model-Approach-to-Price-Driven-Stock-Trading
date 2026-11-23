import {byId,jobUrl} from './common.js';

// Chỉ đọc checkpoint của job; không đoán tiến trình bằng thời gian hoặc POST lại job.
export async function followAnalysis(config,runId,io,update,pause = ms => new Promise(resolve => setTimeout(resolve,ms))) {
  jobUrl(runId,config.language,'live');
  while (true) {
    let data;
    try { data = await io('/api/serving/live/v1/jobs/'+encodeURIComponent(runId)); }
    catch { throw new Error(config.messages.read_error); }
    if (data.run_id !== runId || data.identity?.request?.mode !== 'analyze') throw new Error(config.messages.read_error);
    update(data);
    if (data.state === 'completed') return data;
    if (data.state === 'unknown') throw new Error(config.messages.unknown);
    if (!['queued','running','partial'].includes(data.state) || !data.worker_alive) {
      const message = data.error?.code === 'INVALID_MODEL_OUTPUT' ? config.messages.invalid_model_output : config.messages.job_failed;
      throw new Error(data.error ? `${data.error.code} · ${message}` : message);
    }
    await pause(2000);
  }
}

export function showAgentSteps(variants,progress,config) {
  const hasContext = config.registry.variants.some(variant => variants.includes(variant.id) && variant.dependencies.length > 0);
  const keys = {loading:'step1',indicator:'step2',pattern:'step3',trend:'step4',alpha:'step5',context:'step-bicl',decision:'step6'};
  for (const [role,id] of Object.entries(keys)) {
    const node = byId(id);
    node.hidden = role === 'context' && !hasContext;
    const state = node.hidden ? 'pending' : progress?.[role] ?? 'pending';
    node.classList.toggle('active',state === 'running');
    node.classList.toggle('done',state === 'complete');
    node.setAttribute('data-state',state);
  }
}

export function showAgentProgress(data,config) {
  showAgentSteps(data.identity.request.variant_ids,data.agent_progress,config);
  byId('analysis-progress-message').textContent = data.retry_at ?
    config.messages.retry_at+': '+new Date(data.retry_at*1000).toLocaleString(config.language) :
    config.messages[data.state] ?? data.state;
}
