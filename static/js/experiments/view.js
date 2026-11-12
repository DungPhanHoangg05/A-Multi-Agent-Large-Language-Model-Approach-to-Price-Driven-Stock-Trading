import {byId, element, number, table, download} from './dom.js';
import {renderChart} from './chart.js';

// Các bảng chỉ format giá trị artifact; mọi nội dung động được ghi bằng textContent.
export function renderer(config) {
  const text = config.messages;
  const names = Object.fromEntries(config.variants.map(v => [v.id, v.label[config.language]]));
  const label = id => names[id] ?? id;
  function options(id, values) {
    const select = byId(id), previous = select.value;
    select.replaceChildren(new Option(text.all, 'all'), ...values.map(v => new Option(v, v)));
    select.value = values.includes(previous) ? previous : 'all';
  }
  function research(data, query) {
    byId('research-result').hidden = false;
    const support = data.support;
    byId('stats').replaceChildren();
    for (const [caption, value] of [[text.points, support.points], [text.accounts, support.accounts],
      [text.repeats, 3], [text.missing_news, `${support.sentiment_missing}/${support.points}`]]) {
      const card = element('div', null, 'stat');
      card.append(element('strong', value), element('span', caption));
      byId('stats').append(card);
    }
    table('summary-rows', data.summary.map(r => [label(r.method), number(r.mean_account_return_pct), number(r.balanced_accuracy_pct),
      number(r.accuracy, 2, 100), number(r.mcc), number(r.f1_positive), number(r.f1_negative), number(r.long_rate, 2, 100),
      number(r.mean_daily_mdd_pct), number(r.mean_fee_vnd, 0), number(r.mean_slippage_vnd, 0), number(r.mean_turnover_vnd, 0),
      `${r.bypass_forecasts}/${r.n_forecasts}`]), text.na);
    [...byId('summary-rows').children].forEach((row, index) => {
      row.children[row.children.length - 1].title = JSON.stringify(data.summary[index].policy_reasons);
    });
    table('contrast-rows', data.contrasts.map(r => [label(r.method), label(r.baseline), r.endpoint,
      number(r.effect_pp), r.band95_low_pp == null || r.band95_high_pp == null ? 'NA' : `[${number(r.band95_low_pp)}; ${number(r.band95_high_pp)}]`]), text.na);
    renderChart(byId('contrast-chart'), data.contrasts, label, text);
    table('bridge-rows', data.bridge.map(r => [label(r.method), label(r.baseline), number(r.return_difference_pp), number(r.BA_difference_pp), r.same_action_forecasts]), text.na);
    table('repeat-rows', data.per_repeat.map(r => {
      const classification = data.classification_by_repeat.find(c => c.method === r.method && c.repeat === r.repeat);
      return [label(r.method), r.repeat, number(r.mean_account_return_pct), number(r.balanced_accuracy_pct),
        number(classification?.accuracy, 2, 100), number(classification?.mcc), number(classification?.f1_positive),
        number(classification?.f1_negative), number(r.cycle_sharpe), number(r.cycle_sortino_lpm2)];
    }), text.na);
    const columns = {
      predictions: ['date', 'symbol', 'fold', 'method', 'repeat', 'raw_proposal', 'final_action', 'reason', 'r_net'],
      accounts: ['symbol', 'fold', 'method', 'repeat', 'return_pct', 'daily_mdd_pct', 'fee_vnd', 'slippage_vnd', 'turnover_vnd'],
      cycles: ['date', 'symbol', 'fold', 'method', 'repeat', 'action', 'strategy_return', 'fee_vnd', 'slippage_vnd'],
      daily_nav: ['date', 'symbol', 'fold', 'method', 'repeat', 'nav_vnd'],
    }[data.details.table];
    const headings = element('tr');
    columns.forEach(key => headings.append(element('th', ({method: text.method, date: text.date, symbol: text.symbol,
      fold: text.fold, repeat: text.repeat, strategy_return: 'strategy_return (fraction)', r_net: 'label r_net (fraction)',
      nav_vnd: 'NAV (VND)', return_pct: text.return})[key] ?? key)));
    byId('detail-head').replaceChildren(headings);
    table('detail-rows', data.details.rows.map(row => columns.map(key => key === 'method' ? label(row[key])
      : typeof row[key] === 'number' ? number(row[key], key === 'repeat' ? 0 : 5) : row[key])), text.na);
    const detail = data.details, end = Math.min(detail.offset + detail.rows.length, detail.total);
    byId('page-info').textContent = detail.total ? `${detail.offset + 1}–${end} / ${detail.total} ${text.rows}` : text.no_rows;
    byId('prev').disabled = detail.offset === 0;
    byId('next').disabled = end >= detail.total;
    options('symbol', data.options.symbols); options('fold', data.options.folds);
    byId('provenance').textContent = JSON.stringify({provenance: data.provenance, coverage: data.coverage,
      support: data.support, telemetry: data.telemetry, definitions: data.definitions, units: data.units,
      filters: data.filters, metric_scope: data.metric_scope, limitations: data.limitations}, null, 2);
    byId('downloads').replaceChildren();
    const exportUrl = new URL(`/api/research-results/${data.run_id}/export`, location.origin);
    exportUrl.search = query.toString();
    for (const [caption, format, name] of [[text.json, 'json', 'summary'], [text.csv_summary, 'csv', 'summary'], [text.csv_details, 'csv', 'details']]) {
      exportUrl.searchParams.set('format', format); exportUrl.searchParams.set('export_table', name);
      download('downloads', caption, exportUrl.href);
    }
    download('downloads', text.original_plot, `/api/research-results/${data.run_id}/artifacts/return_contrasts.png`);
  }
  function legacy(data, id) {
    byId('legacy-result').hidden = false;
    const variant = byId('variant').value;
    table('legacy-rows', data.rows.filter(r => r.variant === variant).map(r => [r.point_id, r.raw_proposal,
      r.final_action, number(r.strategy_return, 4, 100), r.reason, r.quality]), text.na);
    byId('legacy-support').textContent = `${data.complete_slots}/${data.planned_slots} slots · ${data.points} points · ${data.mode}`;
    byId('legacy-accounts').textContent = Object.entries(data.accounts).filter(([key]) => key.split('/')[0] === variant)
      .map(([key, a]) => `${key}: ${number(a.total_return_pct, 4)}%`).join(' · ');
    byId('legacy-downloads').replaceChildren();
    for (const format of ['json', 'csv']) download('legacy-downloads', format.toUpperCase(), `/api/experiments/${encodeURIComponent(id)}/export?format=${format}`);
  }
  return {research, legacy};
}
