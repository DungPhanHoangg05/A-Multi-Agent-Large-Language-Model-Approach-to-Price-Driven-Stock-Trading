import {byId,json,jobUrl} from './common.js';
import {renderer} from './view.js';

// Poll chỉ đọc; không tự resume hoặc POST lại sau lỗi mạng/UNKNOWN.
export function resultController(config,io=json,schedule=setTimeout,cancel=clearTimeout) {
  const view = renderer(config), text = config.messages;
  let generation = 0, timer, abort, controlling = false;
  const api = '/api/serving/v1/jobs/'+encodeURIComponent(config.runId);
  function clear() { cancel(timer); ++generation; abort?.abort(); }
  async function refresh() {
    clear(); const mine = generation; abort = new AbortController();
    try {
      jobUrl(config.runId,config.language);
      const data = await io(api,undefined,abort.signal);
      if (mine !== generation) return;
      if (data.run_id !== config.runId || !['analyze','compare'].includes(data.identity.request.mode)) throw new Error('Invalid job');
      view.render(data);
      if (['queued','running','partial','stop_requested'].includes(data.state) && data.worker_alive) timer = schedule(refresh,2000);
    } catch (error) { if (mine === generation) view.error(text.read_error); }
  }
  async function control(action) {
    if (controlling || byId(action+'-job').disabled) return;
    controlling = true; clear(); byId('stop-job').disabled = true; byId('resume-job').disabled = true;
    try { await io(api+'/'+action,{}); await refresh(); }
    catch { view.error(text.failed); }
    finally { controlling = false; }
  }
  function init() {
    byId('refresh-job').addEventListener('click',refresh);
    byId('stop-job').addEventListener('click',() => control('stop'));
    byId('resume-job').addEventListener('click',() => control('resume'));
    return refresh();
  }
  return {init,refresh,control,clear};
}
if (byId('analysis-config')) resultController(JSON.parse(byId('analysis-config').textContent)).init();
