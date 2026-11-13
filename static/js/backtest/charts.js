import {byId,element,label} from '../analysis/common.js';
const colors = ['#9d1730','#126378','#7551a8','#8b5d13','#17603b','#bd4c18','#3b4fa1','#62505f'];

// Mỗi plot chỉ một symbol/repeat; tuyệt đối không cộng NAV của các account.
export function chart(id, rows, xKey, yKey, config) {
  const target = byId(id); target.replaceChildren();
  const usable = rows.filter(r => typeof r[yKey] === 'number' && Number.isFinite(r[yKey]));
  if (!usable.length) { target.append(element('p',config.messages.unavailable)); return; }
  const dates = [...new Set(usable.map(r => r[xKey]))].sort(), values = usable.map(r => r[yKey]);
  const low = Math.min(...values), high = Math.max(...values), span = high-low || 1;
  const svg = document.createElementNS('http://www.w3.org/2000/svg','svg'); svg.setAttribute('viewBox','0 0 900 250'); svg.setAttribute('role','img');
  svg.setAttribute('aria-label',id === 'bt-nav-chart' ? config.messages.daily_nav : config.messages.cycle_returns);
  const add = (tag,attrs,text) => { const node = document.createElementNS('http://www.w3.org/2000/svg',tag);
    for (const [k,v] of Object.entries(attrs)) node.setAttribute(k,String(v));
    if (text != null) node.textContent = String(text); svg.append(node); return node; };
  const legend = element('div',null,'bt-legend');
  [...new Set(usable.map(r => r.method))].forEach((method,index) => {
    const selected = usable.filter(r => r.method === method).sort((a,b) => a[xKey].localeCompare(b[xKey]));
    const color = colors[index%colors.length];
    const points = selected.map(r => `${110+dates.indexOf(r[xKey])*750/Math.max(1,dates.length-1)},${195-(r[yKey]-low)*165/span}`);
    add('polyline',{points:points.join(' '),fill:'none',stroke:color,'stroke-width':2,'data-method':method});
    if (points.length === 1) { const [cx,cy] = points[0].split(','); add('circle',{cx,cy,r:4,fill:color}); }
    const item = element('span',label(config,method)); item.style.borderColor = color; legend.append(item);
  });
  add('text',{x:4,y:30,'font-size':14},high.toFixed(2)); add('text',{x:4,y:200,'font-size':14},low.toFixed(2));
  add('text',{x:110,y:235,'font-size':14},dates[0]); add('text',{x:860,y:235,'font-size':14,'text-anchor':'end'},dates.at(-1));
  target.append(svg,legend);
}
