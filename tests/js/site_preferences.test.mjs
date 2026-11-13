// Theme/locale trên DOM fixture; không thay cho nghiệm thu browser trực quan.
import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';

test('Theme áp dụng trước paint, nhớ lựa chọn và đồng bộ tab khác',() => {
  const events={},handlers={},store=new Map(),root={dataset:{},style:{},classList:{add(){}}};
  const button={textContent:'',attributes:{},setAttribute(k,v){this.attributes[k]=v;},addEventListener(k,v){handlers[k]=v;}};
  const document={documentElement:root,addEventListener:(k,v)=>events[k]=v,getElementById:id => id==='theme-toggle' ? button : {textContent:JSON.stringify({dark:'Dark mode',light:'Light mode'})}};
  const context={document,localStorage:{getItem:k=>store.get(k),setItem:(k,v)=>store.set(k,v)},matchMedia:()=>({matches:true,addEventListener(){}}),addEventListener:(k,v)=>events[k]=v};
  runInNewContext(readFileSync(new URL('../../static/js/site_preferences.js',import.meta.url),'utf8'),context);
  assert.equal(root.dataset.theme,'dark'); assert.equal(root.style.colorScheme,'dark');
  events.DOMContentLoaded(); assert.equal(button.textContent,'Light mode'); assert.equal(button.attributes['aria-pressed'],'true');
  handlers.click(); assert.equal(root.dataset.theme,'light'); assert.equal(store.get('qa_theme'),'light');
  events.storage({key:'qa_theme',newValue:'dark'}); assert.equal(root.dataset.theme,'dark');
});

globalThis.document={getElementById:()=>null};
const {localizeElements,needsTranslation}=await import('../../static/js/display_locale.js');
class Node {
  constructor(text='',dataset={}) {this.textContent=text;this.dataset=dataset;this.attrs={};this.children=[];this.classList={add(){}};}
  setAttribute(k,v){this.attrs[k]=v;} removeAttribute(k){delete this.attrs[k];}
  append(...values){this.children.push(...values);} replaceChildren(...values){this.children=values;this.textContent='';}
}
const config={language:'en',preparing:'Translating',locale_failed:'Translation unavailable',locale_unknown:'Unknown translation'};
test('Chọn EN dịch đúng report, không thay decision và không gửi lại khi đọc trạng thái',async () => {
  const status=new Node(),node=new Node('Giá trị 1.23; SHORT',{sourceLanguage:'vi'}),calls=[];
  globalThis.document={getElementById:()=>status,createElement:()=>new Node()};
  await localizeElements([node],config,async(url,body) => {
    calls.push({url,body});
    return body ? {state:'running',id:'12345678-1234-4234-8234-123456789abc'} : {state:'completed',target:'en',texts:{n0:'Value 1.23; SHORT'}};
  },async()=>{});
  assert.equal(node.textContent,'Value 1.23; SHORT'); assert.equal(node.dataset.localizedLanguage,'en');
  assert.equal(calls[0].body.target,'en'); assert.equal(calls[1].body,undefined);
  assert.equal(status.hidden,true);
});
test('Báo cáo EN sẵn có không gọi dịch; metadata VI trong report EN vẫn được xử lý',async () => {
  const node=new Node('Value 1.23',{sourceLanguage:'en'});let calls=0;
  await localizeElements([node],config,async()=>{calls++;}); assert.equal(calls,0);
  assert.equal(needsTranslation('TĂNG mạnh', 'en','en'),true);
});
test('Lỗi/key thiếu không fallback về báo cáo VI trên trang EN',async () => {
  const node=new Node('Giá trị 1.23',{sourceLanguage:'vi'}),status=new Node();
  globalThis.document={getElementById:()=>status};
  await localizeElements([node],config,async()=>{throw new Error('offline');});
  assert.equal(node.textContent,'Translation unavailable'); assert.equal(status.textContent,'Translation unavailable');
  assert.equal(status.hidden,false);
});
