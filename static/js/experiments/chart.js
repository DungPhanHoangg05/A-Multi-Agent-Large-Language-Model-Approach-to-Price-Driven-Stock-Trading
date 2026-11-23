// Chỉ đặt điểm và band đã khóa lên trục; không bootstrap hoặc tạo contrast mới.
export function renderChart(container, contrasts, label, text) {
  container.replaceChildren();
  const rows = contrasts.filter(row => row.endpoint === 'account_return_percentage_points');
  if (!rows.length) { container.textContent = text.no_contrast; return; }
  const make = (tag, attrs = {}, content) => {
    const node = document.createElementNS('http://www.w3.org/2000/svg', tag);
    for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
    if (content != null) node.textContent = content;
    return node;
  };
  const points = [0, ...rows.flatMap(row => [row.effect_pp, row.band95_low_pp, row.band95_high_pp].filter(v => v != null))];
  const min = Math.min(...points), max = Math.max(...points), padding = (max - min || 1) * .13;
  const low = min - padding, high = max + padding, x = value => 260 + (value - low) / (high - low) * 640;
  const height = 80 + rows.length * 44;
  const svg = make('svg', {viewBox: `0 0 960 ${height}`, 'aria-hidden': 'true'});
  for (let i = 0; i <= 5; i++) {
    const value = low + (high - low) * i / 5;
    svg.append(make('line', {x1: x(value), x2: x(value), y1: 22, y2: height - 48, stroke: '#e1e8ef'}));
    svg.append(make('text', {x: x(value), y: height - 27, 'text-anchor': 'middle'}, value.toFixed(2)));
  }
  svg.append(make('line', {x1: x(0), x2: x(0), y1: 22, y2: height - 48, stroke: '#71849a', 'stroke-dasharray': '4 4'}));
  rows.forEach((row, index) => {
    const y = 35 + index * 44;
    svg.append(make('text', {x: 245, y: y + 5, 'text-anchor': 'end'}, label(row.method)));
    if (row.band95_low_pp != null && row.band95_high_pp != null) {
      svg.append(make('line', {x1: x(row.band95_low_pp), x2: x(row.band95_high_pp), y1: y, y2: y, stroke: '#326c96', 'stroke-width': 3}));
      for (const value of [row.band95_low_pp, row.band95_high_pp]) svg.append(make('line', {x1: x(value), x2: x(value), y1: y - 6, y2: y + 6, stroke: '#326c96'}));
    }
    const dot = make('circle', {cx: x(row.effect_pp), cy: y, r: 5, fill: '#326c96', 'data-effect': row.effect_pp});
    dot.append(make('title', {}, `${label(row.method)} − ${label(row.baseline)}: ${row.effect_pp} pp`));
    svg.append(dot);
  });
  svg.append(make('text', {x: 580, y: height - 4, 'text-anchor': 'middle'}, `${text.effect} · return · ${label(rows[0].baseline)}`));
  container.append(svg);
}
