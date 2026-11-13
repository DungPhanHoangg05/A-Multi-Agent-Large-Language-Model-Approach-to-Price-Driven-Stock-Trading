import {element} from './common.js';

// Markdown báo cáo chỉ cần tiêu đề, bảng, danh sách và nhấn mạnh; HTML/link model luôn là văn bản.
function inline(parent,text) {
  for (const chunk of text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g)) {
    const bold = chunk.startsWith('**') && chunk.endsWith('**');
    const code = chunk.startsWith('`') && chunk.endsWith('`');
    parent.append(element(bold ? 'strong' : code ? 'code' : 'span',bold ? chunk.slice(2,-2) : code ? chunk.slice(1,-1) : chunk));
  }
}

export function renderReport(parent,text) {
  parent.replaceChildren();
  const lines = text.replace(/\r\n/g,'\n').split('\n');
  let table, list, code;
  for (const line of lines) {
    if (line.trim().startsWith('```')) {
      table = list = undefined;
      if (code) code = undefined;
      else { code = element('pre'); parent.append(code); }
      continue;
    }
    if (code) { code.textContent += line+'\n'; continue; }
    if (!line.trim()) { table = list = undefined; continue; }
    if (/^\s*\|.*\|\s*$/.test(line)) {
      if (/^\s*\|[\s:|\-]+\|\s*$/.test(line)) continue;
      if (!table) { table = element('table'); const wrap = element('div',null,'report-table'); wrap.append(table); parent.append(wrap); }
      const row = element('tr');
      for (const cell of line.trim().slice(1,-1).split('|')) { const node = element('td'); inline(node,cell.trim()); row.append(node); }
      table.append(row); list = undefined; continue;
    }
    table = undefined;
    const bullet = line.match(/^\s*(?:[-*]|\d+\.)\s+(.+)$/);
    if (bullet) {
      if (!list) { list = element('ul'); parent.append(list); }
      const item = element('li'); inline(item,bullet[1]); list.append(item); continue;
    }
    list = undefined;
    const heading = line.match(/^\s*#{1,6}\s+(.+)$/);
    const node = element(heading ? 'h4' : 'p'); inline(node,heading ? heading[1] : line); parent.append(node);
  }
}
