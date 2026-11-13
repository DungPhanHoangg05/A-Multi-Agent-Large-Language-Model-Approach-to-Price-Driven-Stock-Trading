import {jobUrl,requestFor,blockerText} from './common.js';

// Một click phân tích: khóa selection, capture nến, preflight rồi tạo đúng phiên bản đã chọn.
export async function runTimeframe(config, selection, models, io, status) {
  const text = config.messages;
  if (!selection.symbol) throw new Error(text.timeframe_choose_symbol);
  status(text.live_loading);
  let snapshot;
  try { snapshot = await io('/api/serving/live/v1/snapshot',{symbol:selection.symbol,timeframe:selection.timeframe}); }
  catch { throw new Error(text.live_failed); }
  if (snapshot.symbol !== selection.symbol || snapshot.chart_timeframe !== selection.timeframe || !/^[0-9a-f]{64}$/.test(snapshot.snapshot_id)) throw new Error(text.live_failed);
  const body = {version:'variant_serving_timeframe_v1',snapshot_id:snapshot.snapshot_id,chart_timeframe:selection.timeframe,
    request:requestFor({mode:'analyze',ids:[selection.variant],symbol:selection.symbol,date:snapshot.cutoff,
      language:selection.language,repeats:selection.repeats},models)};
  status(text.waiting);
  const checked = await io('/api/serving/live/v1/preflight',body);
  if (!checked.run_enabled || checked.status !== 'ready') throw new Error((checked.blockers ?? []).map(b => blockerText(b,text)).join(' · ') || text.failed);
  status(text.running);
  let data;
  try { data = await io('/api/serving/live/v1/jobs',structuredClone(body)); }
  catch { throw new Error(text.start_unknown); }
  return {runId:data.run_id,url:jobUrl(data.run_id,config.language,'live')};
}
