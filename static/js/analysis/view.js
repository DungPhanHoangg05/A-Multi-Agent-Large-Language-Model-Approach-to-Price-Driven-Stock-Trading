import {byId, element, label} from './common.js';
import {chart} from './chart.js';

// Mỗi card chỉ trình bày một slot durable, không tính lại quyết định hoặc policy.
export function renderer(config) {
  const text = config.messages;
  const detailNodes = new Map();
  let cardsKey, reportsKey;
  function field(list, name, value) { list.append(element('dt',name),element('dd',value ?? text.na)); }
  function card(data, id, repeat, row) {
    const node = element('article',null,'decision-card');
    node.append(element('h3',label(config,id)+' · '+text.repeat+' '+(repeat+1)));
    if (!row) { node.append(element('p',text.pending)); return node; }
    const list = element('dl');
    field(list,text.raw,row.raw_prediction); field(list,text.final,row.final_prediction);
    field(list,text.action,row.final_action); field(list,text.effective,label(config,row.executed_id));
    field(list,'P&L',row.net_return_pct == null ? text.metric : row.net_return_pct.toFixed(4)+'%');
    node.append(list);
    const detail = data.policy_details?.[`forecast/${row.point_id}/r${repeat}/${id}`];
    node.append(element('p',text.reason+': '+[row.fallback_reason,row.bypass_reason,detail?.policy?.reason].filter(Boolean).filter((v,i,a) => a.indexOf(v) === i).join(' · ')));
    if (detail) {
      const details = element('details'); details.append(element('summary',text.details),element('pre',JSON.stringify(detail,null,2)));
      const key = `${data.run_id}/${row.point_id}/${repeat}/${id}`;
      details.open = detailNodes.get(key)?.open ?? false;
      detailNodes.set(key,details);
      node.append(details);
    }
    return node;
  }
  function image(parent, raw, title) {
    if (typeof raw !== 'string' || !raw.startsWith('iVBORw0KGgo') || !/^[A-Za-z0-9+/=\r\n]+$/.test(raw)) return;
    const node = element('img'); node.src = 'data:image/png;base64,'+raw; node.alt = title; node.loading = 'lazy'; parent.append(node);
  }
  function shared(data) {
    const key = JSON.stringify([data.run_id,Object.entries(data.snapshots ?? {}).map(([point,snapshot]) => [point,snapshot.sha256])]);
    if (key === reportsKey) return;
    reportsKey = key;
    const container = byId('shared-reports'); container.replaceChildren();
    for (const [point,snapshot] of Object.entries(data.snapshots ?? {})) {
      const group = element('section'); group.append(element('h3',point));
      const payload = snapshot.payload;
      chart(group,data.realtime_chart ?? payload.price_prefix,point,data.live_input?.chart_timeframe ?? '1d');
      for (const role of ['indicator','pattern','trend','alpha','sentiment']) {
        const report = element('details',null,'serving-report');
        report.append(element('summary',role === 'alpha' ? text.native_alpha : text[role+'_report']),element('pre',payload[role+'_report'] ?? text.unavailable));
        if (role === 'pattern' || role === 'trend') image(report,payload[role+'_image'],text[role+'_report']);
        group.append(report);
      }
      if (payload.causal_alpha?.projection) {
        const common = element('details',null,'serving-report');
        common.append(element('summary',text.common_alpha),element('pre',payload.causal_alpha.projection.report ?? text.unavailable));
        group.append(common);
      }
      container.append(group);
    }
  }
  function render(data) {
    const request = data.identity.request, progress = data.progress;
    byId('job-state').textContent = text[data.state === 'failed' ? 'job_failed' : data.state] ?? data.state;
    const source = request.chart_timeframe ? text.timeframe_source : request.data_source === 'live' ? text.live_source : text.asof_source;
    byId('job-meta').textContent = `${source} · ${request.symbols.join(', ')} · ${request.start_date} · ${request.chart_timeframe ?? request.timeframe} · ${request.language.toUpperCase()} · ${data.run_id}`;
    if (data.live_input) byId('job-meta').textContent += ` · ${text.live_captured}: ${data.live_input.captured_at}`;
    byId('job-progress').textContent = `${text.points}: ${progress.points_complete}/${progress.points_total} · ${text.slots}: ${progress.decision_slots_complete}/${progress.decision_slots_total} · ${text.attempts}: ${progress.api_attempts}`;
    byId('partial-note').hidden = data.state === 'completed';
    byId('retry-at').textContent = data.retry_at ? text.retry_at+': '+new Date(data.retry_at*1000).toLocaleString(config.language) : '';
    byId('job-error').textContent = data.state === 'unknown' ? text.unknown : data.error ? data.error.code+' · '+data.error.message : '';
    byId('stop-job').disabled = !['queued','running','partial'].includes(data.state);
    byId('resume-job').disabled = ['completed','unknown','stop_requested'].includes(data.state) || data.worker_alive === true;
    byId('job-status-panel').setAttribute('aria-busy',String(['queued','running','partial'].includes(data.state)));
    byId('no-decisions').hidden = data.rows.length > 0;
    // Heartbeat không dựng lại reports/card đang đọc; slot mới giữ trạng thái mở chi tiết.
    const key = JSON.stringify([data.run_id,request,data.execution_plan,data.rows,data.policy_details]);
    if (key !== cardsKey) {
      cardsKey = key;
      const main = byId('decision-cards'), controls = byId('control-cards'); main.replaceChildren(); controls.replaceChildren();
      for (let repeat = 0; repeat < request.repeats; repeat++) {
        for (const id of data.execution_plan) {
          const row = data.rows.find(row => row.requested_id === id && row.repeat === repeat);
          (data.requested_ids.includes(id) ? main : controls).append(card(data,id,repeat,row));
        }
      }
    }
    byId('control-details').hidden = data.execution_plan.every(id => data.requested_ids.includes(id));
    shared(data);
    byId('job-provenance').textContent = JSON.stringify({run_id:data.run_id, identity:data.identity,
      identity_sha256:data.identity_sha256,input_snapshot_scope:data.input_snapshot_scope,
      shared:Object.fromEntries(Object.entries(data.snapshots ?? {}).map(([point,snapshot]) => [point,{sha256:snapshot.sha256,provenance:snapshot.provenance}]))},null,2);
  }
  function error(message) {
    cardsKey = reportsKey = undefined; detailNodes.clear();
    for (const id of ['job-meta','job-progress','retry-at','decision-cards','control-cards','shared-reports','job-provenance']) byId(id).replaceChildren();
    byId('no-decisions').hidden = false; byId('control-details').hidden = true;
    byId('partial-note').hidden = true;
    byId('job-error').textContent = message;
    byId('job-state').textContent = text.unavailable;
    byId('job-status-panel').setAttribute('aria-busy','false');
    byId('stop-job').disabled = true; byId('resume-job').disabled = true;
  }
  return {render,error};
}
