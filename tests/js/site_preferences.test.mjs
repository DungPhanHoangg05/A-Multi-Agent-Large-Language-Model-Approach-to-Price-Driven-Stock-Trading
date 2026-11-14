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

globalThis.document={querySelectorAll:()=>[]};
const {renderStoredReports,switchStoredLanguage}=await import('../../static/js/display_locale.js');

class Node {
  constructor(text='',dataset={}) {this.textContent=text;this.dataset=dataset;this.attrs={};this.children=[];this.classList={add(){}};}
  setAttribute(k,v){this.attrs[k]=v;} removeAttribute(k){delete this.attrs[k];}
  append(...values){this.children.push(...values);} replaceChildren(...values){this.children=values;this.textContent='';}
  querySelectorAll(){return [];}
}

test('Stored reports render synchronously without any translation request',()=>{
  let network=0; globalThis.fetch=()=>{network++;throw new Error('No network allowed');};
  const node=new Node('Already stored English report',{markdown:'false'});
  renderStoredReports({querySelectorAll:()=>[node]});
  assert.equal(node.textContent,'Already stored English report'); assert.equal(network,0);
  assert.equal(node.attrs['aria-busy'],'false');
});

test('Language switch uses embedded templates immediately and preserves job identity',()=>{
  let network=0; globalThis.fetch=()=>{network++;throw new Error('No network allowed');};
  const view=new Node(),links=[{lang:'vi',href:'http://localhost/output?job=42&lang=vi',setAttribute(){},removeAttribute(){}},{lang:'en',href:'http://localhost/output?job=42&lang=en',setAttribute(){},removeAttribute(){}}];
  const templates={vi:{dataset:{title:'Vietnamese'},content:{cloneNode:()=>new Node('VI report')}},en:{dataset:{title:'English'},content:{cloneNode:()=>new Node('EN report')}}};
  const doc={documentElement:{dataset:{theme:'dark'}},querySelectorAll:()=>links,getElementById:id=>id==='localized-report-view'?view:id.startsWith('report-view-')?templates[id.slice(12)]:null};
  let updated;
  assert.equal(switchStoredLanguage('en',doc,{replaceState:(a,b,url)=>updated=url},{href:'http://localhost/output?job=42&lang=vi'}),true);
  assert.equal(view.children[0].textContent,'EN report'); assert.equal(doc.documentElement.lang,'en');
  assert.equal(updated.searchParams.get('job'),'42'); assert.equal(updated.searchParams.get('lang'),'en');
  assert.equal(switchStoredLanguage('vi',doc,{replaceState(){}},{href:'http://localhost/output?job=42&lang=en'}),true);
  assert.equal(view.children[0].textContent,'VI report'); assert.equal(network,0);
});
