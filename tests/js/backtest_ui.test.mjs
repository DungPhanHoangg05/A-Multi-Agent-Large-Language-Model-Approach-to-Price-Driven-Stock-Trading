// DOM cục bộ kiểm dynamic IDs/filter/export/recovery; không chứng nhận browser responsive.
import assert from 'node:assert/strict';
import {test,beforeEach} from 'node:test';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {renderer,number} from '../../static/js/backtest/view.js';
import {formController} from '../../static/js/backtest/form.js';
import {resultController} from '../../static/js/backtest/result.js';

const root = fileURLToPath(new URL('../../',import.meta.url));
const fixture = JSON.parse(execFileSync('py',['-3.13','-X','utf8','tests/backtest_ui/fixture.py'],{cwd:root,encoding:'utf8',maxBuffer:2**22}));
let nodes,methods,symbols,filterMethods;
class Element {
  constructor(tag) { this.tag=tag; this.children=[]; this.dataset={}; this.attributes={}; this.listeners={}; this.style={}; this.value=''; this.hidden=false; this.disabled=false; }
  set id(value) { this._id=value; nodes?.set(value,this); }
  get id() { return this._id; }
  set textContent(value) { this.text=String(value); this.children=[]; }
  get textContent() { return (this.text ?? '')+this.children.map(child => child.textContent ?? String(child)).join(''); }
  set innerHTML(_) { throw new Error('Không cho phép HTML từ model hoặc file legacy'); }
  append(...children) { this.children.push(...children); }
  replaceChildren(...children) { this.text=''; this.children=children; }
  addEventListener(name,callback) { this.listeners[name]=callback; }
  setAttribute(name,value) { this.attributes[name]=String(value); }
  get selectedOptions() { return this.children.filter(child => child.value === this.value); }
}
const node = id => document.getElementById(id);
const clone = () => structuredClone(fixture.data);
const flush = () => new Promise(resolve => setImmediate(resolve));
const ready = {status:'ready',run_enabled:true,points:[{},{}],planned_decision_slots:12,estimated_max_api_attempts:48};
beforeEach(() => {
  nodes=new Map(); methods=['original_fix','bayesian_v1']; symbols=['FPT']; filterMethods=null;
  globalThis.document={getElementById(id) { if (!nodes.has(id)) nodes.set(id,new Element('div')); return nodes.get(id); },
    createElement:tag => new Element(tag),createElementNS:(_,tag) => new Element(tag),
    querySelectorAll(selector) {
      if (selector.includes('name="bt-variant"')) return methods.map(value => ({value}));
      if (selector.includes('name="bt-symbol"')) return symbols.map(value => ({value}));
      if (selector.includes('name="bt-filter-method"')) return filterMethods ? filterMethods.map(value => ({value})) :
        node('bt-method-filters').children.flatMap(label => label.children.filter(child => child.tag === 'input' && child.checked));
      return [];
    }};
  globalThis.location={origin:'http://localhost',search:''};
  globalThis.localStorage={getItem:() => null,setItem(){}};
  globalThis.Option=class extends Element { constructor(text,value) { super('option'); this.textContent=text; this.value=value; }};
  for (const [id,value] of Object.entries({'bt-start':'2026-07-02','bt-end':'2026-07-07','bt-language':'vi','bt-repeats':'2','kind':'all'})) node(id).value=value;
});
test('Preflight và start giữ hồ sơ chạy của backtest sửa', async () => {
  const calls = [];
  node('bt-profile').value = 'finalize_serving_v1';
  const io = async (url,body) => {
    calls.push({url,body});
    if (url.endsWith('/defaults')) return {models:fixture.data.request.models};
    if (url.endsWith('/jobs')) return {run_id:fixture.data.run_id};
    return ready;
  };
  const form = formController(fixture.config,io,() => {});
  await form.init();
  await form.start();
  assert.equal(calls[1].body.version,'finalize_serving_v1');
  assert.deepEqual(calls[1].body,calls[2].body);
  const result = clone(); result.request.version = 'finalize_serving_v1';
  renderer(fixture.config).render(result,'/api/serving/v1/jobs/'+result.run_id+'/evaluation');
  assert.match(node('bt-run-meta').textContent,/finalize_serving_v1/);
});
test('Metric 0/âm giữ nguyên; NA không bị biến thành zero',() => {
  assert.equal(number(0),'0.000'); assert.equal(number(-.5,100),'-50.000');
  for (const value of [null,undefined,NaN]) assert.equal(number(value),'NA');
  renderer(fixture.config).render(fixture.data,'/api/serving/v1/jobs/'+fixture.data.run_id+'/evaluation');
  assert.equal(node('bt-summary-rows').children.length,2);
  assert.match(node('bt-summary-rows').children[1].textContent,/0\.000/);
  assert.match(node('bt-summary-rows').textContent,/NA/);
  assert.equal(node('bt-downloads').children.length,7);
});
test('Số hàng sinh theo IDs; thêm phương pháp không tạo một cặp Full/Base hard-code',() => {
  const data=clone(); data.summary.push({...data.summary[0],method:'MT_BICL'});
  renderer(fixture.config).render(data,'/api/serving/v1/jobs/'+data.run_id+'/evaluation');
  assert.equal(node('bt-summary-rows').children.length,3); assert.match(node('bt-summary-rows').textContent,/MT-BICL/);
  assert.equal(node('bt-predictions-rows').children.length,8);
});
test('Daily NAV và cycle returns vẽ riêng cho một account, không cộng mã/repeat',() => {
  const data=clone(); data.daily_nav.push({...data.daily_nav[0],symbol:'VNM',nav_vnd:9e10});
  const view=renderer(fixture.config); view.render(data,'/api/serving/v1/jobs/'+data.run_id+'/evaluation');
  const svg=node('bt-nav-chart').children[0];
  assert.equal(svg.children.filter(child => child.tag === 'polyline').length,2);
  assert.doesNotMatch(node('bt-nav-chart').textContent,/90000000000/);
  assert.match(node('bt-cycle-chart').children[0].attributes['aria-label'],/chu kỳ/);
  assert.ok(node('bt-chart-account').children.some(child => child.value === 'FPT/1'));
});
test('Partial/UNKNOWN không có summary/NAV giả, giữ prediction đã xong và khóa resume',() => {
  const data=clone(); Object.assign(data,{status:'unknown',evaluation_status:'INCOMPLETE_JOB',summary:[],daily_nav:[],cycles:[],accounts:[],contrasts:[]});
  data.predictions=data.predictions.slice(0,1); data.predictions[0].net_return_pct=null;
  renderer(fixture.config).render(data,'/api/serving/v1/jobs/'+data.run_id+'/evaluation');
  assert.equal(node('bt-summary-rows').children.length,0); assert.equal(node('bt-charts-section').hidden,true);
  assert.equal(node('bt-incomplete').hidden,false); assert.equal(node('bt-resume').disabled,true);
  assert.match(node('bt-result-error').textContent,/UUID/); assert.match(node('bt-predictions-rows').textContent,/NA/);
});
test('Legacy Full/No-Alpha giữ nhãn riêng, lỗi thiếu không thành CASH, không ghép contrast',() => {
  const data={run_id:'backtest_FPT_20261113_0910',kind:'legacy_backtest',status:'legacy_saved',evaluation_status:'LEGACY_DECLARED_NOT_RECERTIFIED',
    summary:[{method:'legacy_full',return_pct:0,accuracy_pct:50,cycle_end_mdd_pct:null},{method:'legacy_no_alpha',return_pct:-1,accuracy_pct:null,cycle_end_mdd_pct:null}],
    predictions:[{method:'legacy_full',date:'2026-07-02',raw_prediction:'SHORT',final_action:null,net_return_pct:null,error:'timeout'}],
    accounts:[],daily_nav:[],cycles:[],contrasts:[],units:{},provenance:{},limitations:[]};
  renderer(fixture.config).render(data,'/api/serving/v1/legacy-backtests/'+data.run_id);
  assert.match(node('bt-summary-rows').textContent,/No-Alpha/); assert.doesNotMatch(node('bt-summary-rows').textContent,/original_common/);
  assert.equal(node('bt-contrasts-section').hidden,true); assert.equal(node('bt-result-filters').hidden,true);
  assert.doesNotMatch(node('bt-predictions-rows').textContent,/CASH/); assert.equal(node('bt-downloads').children.length,3);
});
test('Nội dung không tin cậy đi qua text DOM; export giữ filter và đúng endpoint owner',() => {
  const data=clone(); data.predictions[0].fallback_reason='<img src=x onerror=attack()>';
  const query='methods=original_fix&baseline=original_common&repeat=0';
  renderer(fixture.config).render(data,'/api/serving/v1/jobs/'+data.run_id+'/evaluation',query);
  assert.match(node('bt-predictions-rows').textContent,/<img src=x onerror=attack\(\)>/);
  const link=new URL(node('bt-downloads').children[3].href);
  assert.match(link.pathname,/\/export$/); assert.equal(link.searchParams.get('repeat'),'0');
  assert.equal(link.searchParams.get('baseline'),'original_common');
});
test('Preflight và start gửi cùng symbols/window/repeats/variants/options; double click chỉ tạo một job',async () => {
  const calls=[],routes=[];
  const io=async(url,body) => { calls.push({url,body}); return url.endsWith('/defaults') ? {models:fixture.data.request.models} :
    url.endsWith('/jobs') ? {run_id:fixture.data.run_id} : ready; };
  const form=formController(fixture.config,io,url => routes.push(url)); await form.init();
  methods=fixture.config.registry.variants.filter(v => v.group === 'main').map(v => v.id); symbols=['FPT','VNM'];
  form.invalidate(); await form.check(); node('bt-decision-temperature').value=.7;
  await Promise.all([form.start(),form.start()]);
  const jobs=calls.filter(call => call.url.endsWith('/jobs')); assert.equal(jobs.length,1);
  assert.equal(jobs[0].body.mode,'backtest'); assert.deepEqual(jobs[0].body.symbols,['FPT','VNM']);
  assert.equal(jobs[0].body.variant_ids.length,6); assert.equal(jobs[0].body.repeats,2);
  assert.equal(jobs[0].body.models.decision.options.temperature,0); assert.match(routes[0],/\/backtest\?run_id=/);
});
test('Đổi filter form hủy preflight cũ; thiếu resource/language không bật nút chạy',async () => {
  const pending=[];
  const form=formController(fixture.config,async(url,body,signal) => url.endsWith('/defaults') ? {models:fixture.data.request.models} :
    new Promise(resolve => pending.push({resolve,signal})));
  const old=form.init(); await flush(); form.invalidate(); const current=form.check();
  assert.ok(pending[0].signal.aborted); pending[1].resolve({run_enabled:false,status:'blocked',blockers:[{code:'SUPPORT_MISMATCH'}]}); await current;
  pending[0].resolve(ready); await old; assert.equal(node('bt-start-job').disabled,true);
  assert.match(node('bt-preflight').textContent,/ngoài miền/);
});
test('POST mất phản hồi không retry tự động hoặc bỏ UUID cũ để gửi lại',async () => {
  let attempts=0;
  const form=formController(fixture.config,async url => {
    if (url.endsWith('/defaults')) return {models:fixture.data.request.models};
    if (url.endsWith('/jobs')) { attempts++; throw new Error('timeout'); } return ready;
  });
  await form.init(); await form.start(); await form.start(); assert.equal(attempts,1);
  assert.match(node('bt-start-error').textContent,/Không tự gửi lại/);
});
test('Filter kết quả dùng cùng run/cohort; response run cũ bị bỏ và lỗi xóa export/card',async () => {
  const pending=[]; const controller=resultController(fixture.config,(url,body,signal) => new Promise(resolve => pending.push({url,resolve,signal})),() => 1,() => {}); controller.init();
  const first=controller.select(fixture.data.run_id); const second=controller.refresh();
  pending[1].resolve(fixture.data); await second; assert.ok(pending[0].signal.aborted);
  pending[0].resolve({...fixture.data,status:'running'}); await first;
  assert.equal(node('bt-state').textContent,fixture.config.messages.completed);
  filterMethods=['original_fix']; node('bt-filter-repeat').value='0'; const selected=controller.refresh();
  assert.match(pending[2].url,/repeat=0/); assert.match(pending[2].url,/methods=original_fix/);
  pending[2].resolve({...fixture.data,run_id:'different'}); await selected;
  assert.equal(node('bt-downloads').children.length,0); assert.equal(node('bt-summary-rows').children.length,0);
});
test('Poll chỉ GET; stop/resume body rỗng; UNKNOWN không cho resume',async () => {
  const calls=[],scheduled=[]; const data=clone(); Object.assign(data,{status:'running',worker_alive:true,evaluation_status:'INCOMPLETE_JOB'});
  const controller=resultController(fixture.config,async(url,body) => { calls.push({url,body}); return body ? {} : data; },fn => { scheduled.push(fn); return 1; },() => {}); controller.init();
  await controller.select(data.run_id); assert.equal(calls[0].body,undefined); assert.equal(scheduled.length,1);
  await controller.control('stop'); assert.deepEqual(calls[1].body,{}); assert.match(calls[1].url,/\/stop$/);
  data.status='unknown'; data.worker_alive=false; await controller.refresh(); await controller.control('resume');
  assert.equal(calls.filter(call => call.url.endsWith('/resume')).length,0); controller.stop();
});
test('ID lỗi bị chặn trước GET evaluation',async () => {
  let calls=0; const controller=resultController(fixture.config,async() => { calls++; return fixture.data; });
  await controller.select('../outside'); assert.equal(calls,0); assert.equal(node('bt-resume').disabled,true);
});
test('Trang experiments chọn Backtest mới từ catalog owner và không gọi endpoint U09 của run khác',async () => {
  node('research-config').textContent=JSON.stringify({messages:fixture.config.researchMessages,backtestMessages:fixture.config.messages,
    registry:fixture.config.registry,variants:fixture.config.registry.variants,language:'vi'});
  location.search='?kind=serving_backtest&run_id='+fixture.data.run_id;
  const calls=[]; const response=data => ({ok:true,json:async() => data});
  globalThis.fetch=async(url) => { calls.push(url);
    if (url === '/api/research-results/runs') return response({default:'u09_analysis_r1',runs:[{id:'u09_analysis_r1',kind:'paper_evidence',label:'U09'}]});
    if (url === '/api/serving/v1/jobs') return response({runs:[{id:fixture.data.run_id,kind:'serving_backtest',label:'Fixture'}]});
    if (url === '/api/serving/v1/legacy-backtests') return response({runs:[]});
    if (url.includes('/evaluation')) return response(fixture.data); throw new Error('Unexpected read '+url);
  };
  await import('../../static/js/experiments/main.js?new-backtest'); await flush();
  assert.equal(node('bt-result').hidden,false); assert.equal(node('research-result').hidden,true);
  assert.equal(node('bt-summary-rows').children.length,2);
  assert.equal(node('state').textContent,fixture.config.messages.new_backtest);
  assert.equal(calls.filter(url => url.includes('u09_analysis_r1?')).length,0);
});
