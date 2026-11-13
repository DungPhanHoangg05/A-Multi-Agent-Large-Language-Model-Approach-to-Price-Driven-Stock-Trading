import {element} from './common.js';

// Giá đóng cửa của cùng prefix as-of; không tải giá mới hoặc nến tương lai.
export function chart(parent, prefix, title) {
  if (!prefix || !Array.isArray(prefix.Close) || !Array.isArray(prefix.Datetime)) return;
  const values = prefix.Close.slice(-45), dates = prefix.Datetime.slice(-45);
  if (values.length < 2 || values.length !== dates.length || values.some(v => typeof v !== 'number' || !Number.isFinite(v))) return;
  const svg = document.createElementNS('http://www.w3.org/2000/svg','svg');
  svg.setAttribute('viewBox','0 0 900 240'); svg.setAttribute('role','img');
  svg.setAttribute('aria-label',title+' · Close · 1d');
  const low = Math.min(...values), high = Math.max(...values), span = high-low || 1;
  function node(tag,attributes,text) {
    const child = document.createElementNS('http://www.w3.org/2000/svg',tag);
    for (const [key,value] of Object.entries(attributes)) child.setAttribute(key,String(value));
    if (text != null) child.textContent = String(text);
    svg.append(child); return child;
  }
  node('title',{},title+' · Close · '+dates[0]+' — '+dates.at(-1));
  node('polyline',{points:values.map((v,i) => `${65+i*800/(values.length-1)},${180-(v-low)*155/span}`).join(' '),fill:'none',stroke:'#9d1730','stroke-width':2});
  node('text',{x:5,y:28,fill:'#566274','font-size':14},high.toFixed(2));
  node('text',{x:5,y:185,fill:'#566274','font-size':14},low.toFixed(2));
  node('text',{x:65,y:225,fill:'#566274','font-size':14},dates[0]);
  node('text',{x:865,y:225,'text-anchor':'end',fill:'#566274','font-size':14},dates.at(-1));
  const figure = element('figure'); figure.append(svg,element('figcaption',title+' · Close · 1d · 10³ VND'));
  parent.append(figure);
}
