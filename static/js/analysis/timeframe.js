import {jobUrl,requestFor,blockerText,captureErrorMessage,FINALIZED_PROFILE} from './common.js';

// Capture một lần để hai phương pháp dùng chung đúng bộ dữ liệu.
export async function startLive(config, selection, models, io, status) {
  const text = config.messages;
  if (!selection.symbol) throw new Error(text.timeframe_choose_symbol);
  if (selection.timeframe !== '1d') throw new Error(text.daily_note);
  const finalized = selection.version === FINALIZED_PROFILE;
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
    request:requestFor({version:selection.version,mode:selection.mode,ids:selection.ids,symbol:selection.symbol,date:snapshot.cutoff,
      language:selection.language,repeats:selection.repeats},models)};
  return submitServing(config,'/api/serving/live/v1',body,io,status);
}

export async function submitServing(config,base,body,io,status) {
  const text = config.messages;
  status(text.waiting,'waiting');
  const checked = await io(base+'/preflight',body);
  if (!checked.run_enabled || checked.status !== 'ready') throw new Error((checked.blockers ?? []).map(b => blockerText(b,text,config.language)).join(' · ') || text.failed);
  status(text.running,'running');
  try {
    const data = await io(base+'/jobs',structuredClone(body));
    jobUrl(data.run_id,config.language);
    return data.run_id;
  }
  catch { throw new Error(text.start_unknown); }
}

export async function runTimeframe(config,selection,models,io,status) {
  const runId = await startLive(config,{...selection,mode:'analyze',ids:[selection.variant]},models,io,status);
  const url = jobUrl(runId,config.language,'live');
  return {runId,url:url+'&presentation=analysis'};
}
