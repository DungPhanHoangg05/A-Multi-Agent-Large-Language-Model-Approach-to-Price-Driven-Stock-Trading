import {element} from './common.js';

// Dựng Markdown bằng node an toàn; không diễn giải HTML hoặc URL do model cung cấp.
function inline(parent,text) {
  for (const chunk of text.split(/(\*\*[^*]+\*\*|`[^`]+`|\*[^*\n]+\*)/g)) {
    const bold = chunk.startsWith('**') && chunk.endsWith('**');
    const code = chunk.startsWith('`') && chunk.endsWith('`');
    const emphasis = !bold && chunk.startsWith('*') && chunk.endsWith('*');
    parent.append(element(bold ? 'strong' : code ? 'code' : emphasis ? 'em' : 'span',bold ? chunk.slice(2,-2) : code || emphasis ? chunk.slice(1,-1) : chunk));
  }
}

export function normalizeIndicator(text) {
  return text.replace(/^\s*===\s*(.*?)\s*===\s*$/gm,(_,name) => '### '+name.replace(/\s*—\s*CHỈ ĐỌC SỐ TRONG SECTION NÀY\s*$/u,''))
    .replace(/^\s*\[END [^\n]*SECTION[^\n]*\]\s*$/gm,'');
}

const cells = line => line.trim().replace(/^\|/,'').replace(/\|$/,'').split(/(?<!\\)\|/).map(value => value.trim().replace(/\\\|/g,'|'));
const separator = line => line.includes('|') && cells(line).every(value => /^:?-{3,}:?$/.test(value));

export function renderReport(parent,text) {
  parent.replaceChildren();
  const lines = text.replace(/\r\n/g,'\n').split('\n');
  let list, listType, code;
  for (let index=0; index<lines.length; index++) {
    const line = lines[index];
    if (line.trim().startsWith('```')) {
      list = undefined;
      if (code) code = undefined;
      else { code = element('pre'); parent.append(code); }
      continue;
    }
    if (code) { code.textContent += line+'\n'; continue; }
    if (!line.trim()) { list = undefined; continue; }
    if (line.includes('|') && index+1<lines.length && separator(lines[index+1])) {
      const table = element('table'), head = element('thead'), body = element('tbody'), row = element('tr');
      for (const cell of cells(line)) { const node = element('th'); node.setAttribute('scope','col'); inline(node,cell); row.append(node); }
      head.append(row); table.append(head,body);
      const wrap = element('div',null,'report-table'); wrap.append(table); parent.append(wrap); index++;
      while (index+1<lines.length && lines[index+1].includes('|') && lines[index+1].trim()) {
        const row = element('tr');
        for (const cell of cells(lines[++index])) { const node = element('td'); inline(node,cell); row.append(node); }
        body.append(row);
      }
      list = undefined; continue;
    }
    if (/^\s*(?:-{3,}|\*{3,}|_{3,})\s*$/.test(line)) { parent.append(element('hr')); list=undefined; continue; }
    const bullet = line.match(/^\s*([-*]|\d+\.)\s+(.+)$/);
    if (bullet) {
      const type = /\d/.test(bullet[1]) ? 'ol' : 'ul';
      if (!list || listType!==type) { list = element(type); listType=type; parent.append(list); }
      const item = element('li'); inline(item,bullet[2]); list.append(item); continue;
    }
    list = undefined;
    const heading = line.match(/^\s*(#{1,6})\s+(.+)$/), quote = line.match(/^\s*>\s?(.*)$/);
    const node = element(heading ? 'h'+Math.max(2,heading[1].length) : quote ? 'blockquote' : 'p');
    inline(node,heading ? heading[2] : quote ? quote[1] : line); parent.append(node);
  }
}
