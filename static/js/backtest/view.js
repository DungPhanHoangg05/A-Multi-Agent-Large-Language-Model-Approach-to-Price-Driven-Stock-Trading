import {byId,element,label} from '../analysis/common.js';
import {chart} from './charts.js';

export const number = (value,multiplier=1) => typeof value === 'number' && Number.isFinite(value) ? (value*multiplier).toFixed(3) : 'NA';
export function renderer(config) {
  const text = config.messages;
  let last;
  const name = id => text[id] ?? label(config,id);
  function table(id,headers,rows) {
    const tr = element('tr'); tr.append(...headers.map(value => element('th',value))); byId(id+'-head').replaceChildren(tr);
    byId(id+'-rows').replaceChildren(...rows.map(values => {
      const row = element('tr');
      for (const value of values) { const missing = value == null || value === 'NA'; const cell = element('td',missing ? 'NA' : value,missing ? 'na' : '');
        if (missing) cell.title = text.na+' · ZERO_DENOMINATOR / MISSING_OUTCOME / LEGACY_UNRECORDED'; row.append(cell); }
      return row;
    }));
  }
  function charts() {
    if (!last) return;
    const [symbol,repeat] = byId('bt-chart-account').value.split('/');
    const select = row => row.symbol === symbol && String(row.repeat) === repeat;
    chart('bt-nav-chart',last.daily_nav.filter(select),'date','nav_vnd',config);
    chart('bt-cycle-chart',last.cycles.filter(select).map(row => ({...row,return_pct:row.strategy_return*100})),'date','return_pct',config);
  }
  function render(data, endpoint, query='') {
    last = data; const legacy = data.kind === 'legacy_backtest';
    byId('bt-result').hidden = false;
    byId('bt-run-meta').textContent = `${data.run_id} · ${text[legacy ? 'legacy_backtest' : 'new_backtest']}`;
    byId('bt-state').textContent = text[data.status === 'failed' ? 'job_failed' : data.status] ?? data.status;
    byId('bt-result-error').textContent = data.status === 'unknown' ? text.unknown : data.error ? data.error.code+' · '+text.failed : '';
    byId('bt-progress').textContent = data.progress ? `${text.points}: ${data.progress.points_complete}/${data.progress.points_total} · ${text.slots}: ${data.progress.decision_slots_complete}/${data.progress.decision_slots_total} · ${text.attempts}: ${data.progress.api_attempts}`+
      (data.retry_at ? ` · ${text.retry_at}: ${new Date(data.retry_at*1000).toLocaleString(config.language)}` : '') : text.legacy_scope;
    byId('bt-incomplete').hidden = legacy || data.evaluation_status === 'COMPLETE';
    byId('bt-incomplete').textContent = data.evaluation_status === 'EMPTY_SUPPORT' ? text.empty_support : text.no_metrics;
    byId('bt-stop').disabled = legacy || !['queued','running','partial'].includes(data.status);
    byId('bt-resume').disabled = legacy || data.worker_alive || ['completed','unknown','stop_requested'].includes(data.status);
    byId('bt-result-filters').hidden = legacy;
    byId('bt-coverage').textContent = data.coverage ? `${text.coverage}: ${data.coverage.filtered_complete_slots}/${data.coverage.filtered_planned_slots} · ${data.coverage.filtered_points} ${text.points}` : text.legacy_scope;
    if (legacy) table('bt-summary',[text.method,text.accuracy,text.returns,text.cycle_mdd],data.summary.map(r => [name(r.method),number(r.accuracy_pct),number(r.return_pct),number(r.cycle_end_mdd_pct)]));
    else table('bt-summary',[text.method,text.coverage,text.returns,text.accuracy,text.balanced_accuracy,text.mcc,text.f1,text.long_rate,text.daily_mdd,text.cycle_mdd,text.fee,text.slippage,text.turnover,text.fallback],
      data.summary.map(r => [name(r.method),r.n_forecasts,number(r.mean_account_return_pct),number(r.accuracy,100),number(r.balanced_accuracy,100),number(r.mcc),number(r.macro_f1),number(r.long_rate,100),number(r.mean_daily_mdd_pct),number(r.mean_cycle_end_mdd_pct),number(r.mean_fee_vnd),number(r.mean_slippage_vnd),number(r.mean_turnover_vnd),`${r.fallback_forecasts}/${r.bypass_forecasts}`]));
    byId('bt-contrasts-section').hidden = legacy || data.evaluation_status !== 'COMPLETE';
    table('bt-contrasts',[text.method,text.baseline,text.delta_return,text.delta_ba],data.contrasts.map(r => [name(r.method),name(r.baseline),number(r.return_difference_pp),number(r.balanced_accuracy_difference_pp)]));
    table('bt-predictions',[text.date,text.symbol,text.repeat,text.method,text.raw,text.final,text.action,text.effective,text.outcome,text.cycle_return,text.reason],
      data.predictions.map(r => [r.date,r.symbol,r.repeat == null ? null : r.repeat+1,name(r.method),r.raw_prediction,r.final_prediction,r.final_action,r.executed_id ? name(r.executed_id) : null,r.label_net,number(r.net_return_pct),r.fallback_reason ?? r.bypass_reason ?? r.reason ?? r.error]));
    const previous = byId('bt-chart-account').value;
    const keys = [...new Set(data.accounts.map(r => `${r.symbol}/${r.repeat}`))];
    byId('bt-chart-account').replaceChildren(...keys.map(key => { const option = element('option',key); option.value = key; return option; }));
    byId('bt-chart-account').value = keys.includes(previous) ? previous : keys[0] ?? '';
    byId('bt-charts-section').hidden = !keys.length; charts();
    byId('bt-downloads').replaceChildren();
    for (const [title,format,tableName] of [[text.json,'json','predictions'],[text.csv_summary,'csv','summary'],[text.csv_predictions,'csv','predictions'],[text.csv_accounts,'csv','accounts'],[text.csv_daily,'csv','daily_nav'],[text.csv_cycles,'csv','cycles'],[text.csv_contrasts,'csv','contrasts']]) {
      if (legacy && !['summary','predictions'].includes(tableName)) continue;
      const url = new URL(endpoint.replace(/\/evaluation$/,'')+'/export',location.origin);
      url.search = query; url.searchParams.set('format',format); url.searchParams.set('table',tableName);
      const link = element('a',title); link.href = url.href; byId('bt-downloads').append(link);
    }
    byId('bt-provenance').textContent = JSON.stringify({provenance:data.provenance,filters:data.filters,metric_scope:data.metric_scope,units:data.units,limitations:data.limitations,coverage:data.coverage,request:data.request},null,2);
    if (!legacy) { const link = byId('bt-experiments-link'); link.href = '/experiments?'+new URLSearchParams({kind:'serving_backtest',run_id:data.run_id,lang:config.language}); link.hidden = false; }
    else byId('bt-experiments-link').hidden = true;
  }
  function clear() {
    last = null;
    for (const id of ['bt-summary-rows','bt-predictions-rows','bt-contrasts-rows','bt-nav-chart','bt-cycle-chart','bt-downloads','bt-provenance']) byId(id).replaceChildren();
  }
  function error(message) { clear(); byId('bt-result').hidden = false; byId('bt-result-error').textContent = message;
    byId('bt-state').textContent = text.unavailable; byId('bt-stop').disabled = byId('bt-resume').disabled = true; }
  return {render,charts,clear,error};
}
