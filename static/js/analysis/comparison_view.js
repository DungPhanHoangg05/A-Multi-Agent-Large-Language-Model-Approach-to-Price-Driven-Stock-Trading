import {byId,element,label,jobUrl,displayWithoutTaskCodes,FINALIZED_PROFILE} from './common.js';
import {renderReport} from './report.js';

export function isPairedResult(data,config) {
  const request=data.identity?.request, ids=request?.variant_ids;
  const live=config.source==='live';
  return request?.mode===(live ? 'compare' : 'backtest') && (request.data_source==='live')===live &&
    request.version===FINALIZED_PROFILE && request.repeats===1 &&
    request.symbols?.length===1 && request.start_date===request.end_date &&
    Array.isArray(ids) && ids.length===2 && ids[0]!==ids[1] &&
    ids.every(id=>config.registry.variants.some(method=>method.id===id&&method.group==='main'));
}

export function comparisonView(config) {
  const text=config.messages, live=config.source==='live';
  const base=live ? '/api/serving/live/v1' : '/api/serving/v1';
  let lastCards;
  const percent=value=>Number.isFinite(value) ? new Intl.NumberFormat(config.language,{maximumFractionDigits:4}).format(value)+'%' : text.na;
  function field(list,name,value) {
    list.append(element('dt',name),element('dd',value??text.na));
  }

  function comparisonCard(id,row,data) {
    const card=element('article',null,'decision-card');
    card.append(element('h3',label(config,id)));
    if (!row) { card.append(element('p',text.pending)); return card; }
    const slot=variant=>data.policy_details?.[`forecast/${row.point_id}/r0/${variant}`];
    const chosen=slot(id), effective=slot(row.executed_id);
    const metrics=element('dl');
    field(metrics,text.raw,row.raw_prediction??text.no_own_proposal);
    field(metrics,text.final,row.final_prediction);
    field(metrics,text.action,row.final_action);
    field(metrics,text.effective,label(config,row.executed_id));
    if (!live) field(metrics,text.net_return,percent(row.net_return_pct));
    card.append(metrics);
    const reason=chosen?.context?.trace?.reason ?? row.fallback_reason ?? row.bypass_reason;
    if (reason || row.executed_id!==id) {
      card.append(element('p',text['reason_'+reason] ?? text.fallback,'serving-muted'));
    }
    const trace=chosen?.context?.trace ?? {};
    const groups=chosen?.context?.aux?.branch?.projection?.summary;
    const context=element('dl');
    if (Array.isArray(trace.population_ids)) field(context,text.bicl_population,trace.population_ids.length);
    if (Array.isArray(trace.conditional?.groups?.conditional)) field(context,text.bicl_conditional,trace.conditional.groups.conditional.length);
    if (Array.isArray(trace.selected_ids)) field(context,text.bicl_examples,trace.selected_ids.length);
    if (Array.isArray(groups)) field(context,text.bicl_group,groups.length);
    if (context.children.length) card.append(element('h4',text.bicl_context),context);
    // Giữ lời giải thích của đầu ra riêng; khi bỏ qua đề xuất, dùng đúng lượt thực thi đã lưu.
    const reply=chosen?.raw_reply ? chosen : effective;
    const verified=chosen?.decision_display?.[config.language];
    const fields=[['justification',text.decision_rationale],['evidence_for',verified ? text.decision_verified_facts : text.decision_support],
      ['evidence_against',verified ? text.decision_historical_utility : text.decision_opposition]];
    let shown=false;
    for (const [key,caption] of fields) {
      const en=config.language==='en' ? reply?.display_en?.[key] : null;
      const value=verified?.[key] ?? (en || reply?.raw_reply?.[key]);
      if (typeof value!=='string' || !value.trim()) continue;
      const paragraph=element('div');
      if (config.language==='en'&&!verified&&!en) paragraph.setAttribute('lang','vi');
      renderReport(paragraph,displayWithoutTaskCodes(value));
      card.append(element('h4',caption),paragraph);
      shown=true;
    }
    if (!shown) card.append(element('p',text.reasons_unavailable,'serving-muted'));
    if (data.state==='completed') {
      const report=element('a',text.open_report,'comparison-open-report');
      report.href='/compare?'+new URLSearchParams({run_id:data.run_id,source:config.source,report:id,lang:config.language});
      report.setAttribute('aria-label',`${text.open_report} · ${label(config,id)}`);
      card.append(report);
    }
    return card;
  }

  function render(data) {
    const request=data.identity.request, ids=request.variant_ids;
    const rows=ids.map(id=>data.rows.find(row=>row.requested_id===id && row.repeat===0));
    byId('compare-meta').textContent=[request.symbols[0],request.start_date,live ? text.live_mode : text.history_mode,'1D'].join(' · ');
    if (data.live_input?.support_scope==='LIVE_CATALOG_EXPLORATORY') byId('compare-meta').textContent+=' · '+text.catalog_live;
    byId('job-state').textContent=text[data.state==='failed' ? 'job_failed' : data.state]??data.state;
    byId('job-progress').textContent=`${rows.filter(Boolean).length}/2 · ${text.attempts}: ${data.progress.api_attempts}`+
      (data.retry_at ? ' · '+text.retry_at+' '+new Date(data.retry_at*1000).toLocaleString(config.language) : '');
    const busy=['queued','running','partial','stop_requested'].includes(data.state) && data.worker_alive;
    byId('job-status-panel').setAttribute('aria-busy',String(Boolean(busy)));
    byId('stop-job').disabled=!busy||data.state==='stop_requested';
    byId('resume-job').disabled=Boolean(data.worker_alive)||['completed','unknown','stop_requested'].includes(data.state);
    byId('job-error').textContent=data.state==='unknown' ? text.unknown : data.error ?
      (data.error.code==='INVALID_MODEL_OUTPUT' ? text.invalid_model_output : text.job_failed) : '';
    const url=base+'/jobs/'+encodeURIComponent(data.run_id);
    const download=byId('compare-export'), more=byId('compare-details');
    download.href=url+'/export'; download.hidden=!live&&data.state!=='completed';
    more.href=live ? jobUrl(data.run_id,config.language,'live')+'&presentation=details' :
      '/backtest?'+new URLSearchParams({run_id:data.run_id,lang:config.language});
    more.hidden=false;
    const key=JSON.stringify([data.state,rows,data.policy_details]);
    if (key===lastCards) return;
    lastCards=key;
    byId('compare-cards').replaceChildren(...ids.map((id,index)=>comparisonCard(id,rows[index],data)));
    const summary=byId('compare-summary'), note=byId('compare-outcome-note');
    summary.replaceChildren(); summary.hidden=!rows.every(Boolean);
    note.hidden=summary.hidden;
    if (summary.hidden) return;
    const [left,right]=rows;
    summary.append(element('h2',left.final_prediction===right.final_prediction ? text.same_decision : text.different_decisions));
    if (left.executed_id===right.executed_id) summary.append(element('p',text.same_effective));
    const realized=rows.every(row=>Number.isFinite(row.net_return_pct));
    if (!live && realized) {
      const delta=new Intl.NumberFormat(config.language,{maximumFractionDigits:4,signDisplay:'exceptZero'}).format(right.net_return_pct-left.net_return_pct);
      summary.append(element('p',text.delta_return+' · '+delta+' '+text.percentage_points));
    }
    note.textContent=text.same_behavior+' '+(live ? text.live_outcome_note : realized ? text.history_outcome_note : text.no_outcome);
  }

  function error(message) {
    lastCards=undefined;
    byId('job-state').textContent=text.unavailable;
    byId('job-error').textContent=message;
    byId('job-status-panel').setAttribute('aria-busy','false');
    for (const id of ['compare-cards','compare-summary','compare-meta','job-progress']) byId(id).replaceChildren();
    for (const id of ['compare-summary','compare-outcome-note','compare-export','compare-details']) byId(id).hidden=true;
    byId('stop-job').disabled=true;
    byId('resume-job').disabled=true;
  }
  return {render,error};
}
