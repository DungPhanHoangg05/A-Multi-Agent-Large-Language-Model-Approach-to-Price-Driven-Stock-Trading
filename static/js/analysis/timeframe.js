import {jobUrl,requestFor,blockerText,captureErrorMessage,FINALIZED_PROFILE} from './common.js';

// Một click phân tích: khóa selection, capture nến, preflight rồi tạo đúng phiên bản đã chọn.
export async function runTimeframe(config, selection, models, io, status) {
  const text = config.messages;
  if (!selection.symbol) throw new Error(text.timeframe_choose_symbol);
  if (selection.timeframe !== '1d') throw new Error(text.daily_note);
  const finalized = selection.version === FINALIZED_PROFILE;
  if (finalized && !config.registry.domain.released_symbols.includes(selection.symbol)) throw new Error(text.blocked_support);
  status(text.live_loading,'live_loading');
  let snapshot;
  const capture = finalized ? {symbol:selection.symbol,profile:FINALIZED_PROFILE}
    : {symbol:selection.symbol,timeframe:selection.timeframe};
  try { snapshot = await io('/api/serving/live/v1/snapshot',capture); }
  catch (error) { throw new Error(captureErrorMessage(error,config)); }
  const captureMatches = finalized ? snapshot.capture_version === 'finalize_live_raw_capture_v1'
    : snapshot.chart_timeframe === selection.timeframe;
  if (snapshot.symbol !== selection.symbol || !captureMatches || !/^[0-9a-f]{64}$/.test(snapshot.snapshot_id)) throw new Error(text.live_failed);
  const body = {version:finalized ? 'variant_serving_live_v1' : 'variant_serving_timeframe_v1',
    snapshot_id:snapshot.snapshot_id,...(finalized ? {} : {chart_timeframe:selection.timeframe}),
    request:requestFor({version:selection.version,mode:'analyze',ids:[selection.variant],symbol:selection.symbol,date:snapshot.cutoff,
      language:selection.language,repeats:selection.repeats},models)};
  status(text.waiting,'waiting');
  const checked = await io('/api/serving/live/v1/preflight',body);
  if (!checked.run_enabled || checked.status !== 'ready') throw new Error((checked.blockers ?? []).map(b => blockerText(b,text,config.language)).join(' · ') || text.failed);
  status(text.running,'running');
  let data;
  try { data = await io('/api/serving/live/v1/jobs',structuredClone(body)); }
  catch { throw new Error(text.start_unknown); }
  const url = jobUrl(data.run_id,config.language,'live');
  return {runId:data.run_id,url:url+'&presentation=analysis'};
}
