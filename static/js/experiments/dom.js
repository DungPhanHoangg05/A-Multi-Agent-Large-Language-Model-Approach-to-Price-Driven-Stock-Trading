// Hàm DOM chung chỉ ghi text; không đưa model hoặc artifact text vào HTML.
export const byId = id => document.getElementById(id);
export function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text != null) node.textContent = String(text);
  if (className) node.className = className;
  return node;
}
export function number(value, digits = 3, multiplier = 1) {
  return value == null || typeof value !== 'number' || !Number.isFinite(value)
    ? 'NA' : (value * multiplier).toFixed(digits);
}
export function table(id, rows, naReason) {
  const body = byId(id);
  body.replaceChildren();
  for (const values of rows) {
    const tr = element('tr');
    for (const value of values) {
      const missing = value == null || value === 'NA';
      const td = element('td', missing ? 'NA' : value, missing ? 'na' : '');
      if (missing) td.title = naReason;
      tr.append(td);
    }
    body.append(tr);
  }
}
export function download(container, text, href) {
  const link = element('a', text);
  link.href = href;
  byId(container).append(link);
}
