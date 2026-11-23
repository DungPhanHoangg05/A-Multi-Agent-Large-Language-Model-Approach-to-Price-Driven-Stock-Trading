import {element} from './common.js';

const INDICATOR_HEADING = /^(?:\s*===\s*(.*?)\s*===\s*|\s*(#{1,6})[ \t]+(.+))$/u;
const INDICATOR_TITLE_GUARD = /(?:chỉ đọc số trong section này|only read (?:the )?(?:numbers|values) in this section|(?:đã )?(?:xác định|đếm|tính) bởi hệ thống|(?:determined|confirmed|counted|calculated) by the system|không (?:thay đổi|tự đếm lại)|do not (?:change|recount|recalculate))/iu;
const INDICATOR_RULE_HEADING = /^(?:#{1,6}\s+)?\*{0,2}(?:quy tắc bắt buộc|quy tắc quan trọng nhất|mandatory rules|most important rules|system instructions)(?:[\s:*]|$)/iu;
const INDICATOR_INTERNAL_NOTE = new RegExp([
  String.raw`(?:^\s*(?:(?:[-*]|\d+[.)])\s+)?|(?<=[.!?])[ \t]+)(?:(?:lưu ý|note):[ \t]*)?(?:`,
  String.raw`không (?:dùng (?:số liệu|số này|giá trị)|áp dụng cho chỉ báo khác|tự đếm lại)|chỉ số này không liên quan đến|`,
  String.raw`đây là chỉ báo momentum, không phải|stochastic không có histogram|thang đo(?=\s|:)|sử dụng đúng tín hiệu từng chỉ báo|mỗi section \[end|`,
  String.raw`do not (?:use|recount|change the summary)|this (?:index|indicator) is not related to|this is a momentum indicator, not|`,
  String.raw`stochastic has no histogram|scale(?=[ \t]*(?::|[−-]?\d))|use exactly the (?:per-indicator|indicator) signals|each \[end).*$`,
].join(''),'iu');

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
  // Chỉ lọc bản hiển thị. Dòng kết quả có thể đứng sau các chỉ dẫn trong báo cáo cũ.
  const lines = [];
  let inRules = false;
  for (const raw of text.split(/\r?\n/u)) {
    let line = raw.replace(/\p{Dash}/gu,'-')
      .replace(/[ \t]*[←→↔⇐⇒⇔➜➔][ \t]*/gu,' - ')
      .replace(/^([ \t]*)[•◦▪▫●○][ \t]*/u,'$1- ')
      .replace(/[\p{Extended_Pictographic}\p{Emoji_Presentation}\u200d\ufe0e\ufe0f\u20e3✓✔✗✘]/gu,'');
    if (INDICATOR_RULE_HEADING.test(line.trim())) { inRules = true; continue; }
    if (inRules && (!line.trim() || /^\s*(?:\d+[.)]|[-*])\s+\S/u.test(line))) continue;
    inRules = false;
    const section = line.match(INDICATOR_HEADING);
    const boldTitle = line.match(/^\s*\*\*([^*]+)\*\*\s*$/u)?.[1];
    const name = section?.[1] ?? section?.[3] ?? boldTitle;
    if (name) {
      const parts = name.split(/[ \t]+-[ \t]+/u);
      const guard = parts.findIndex(part => INDICATOR_TITLE_GUARD.test(part));
      const title = (guard < 0 ? parts : parts.slice(0,guard)).join(' - ').trim();
      if (!title) continue;
      if (section || guard >= 0) line = (section?.[2] ?? '###')+' '+title;
    }
    line = line.replace(INDICATOR_INTERNAL_NOTE,'').replace(/\[END\b[^\n\]]*\bSECTION\b[^\n\]]*\]/giu,'');
    if (line.trim() || !raw.trim()) lines.push(line.trimEnd());
  }
  return lines.join('\n').trim();
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
