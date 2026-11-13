// DOM in-memory kiểm hành vi và an toàn text; không thay cho nghiệm thu browser.
import assert from 'node:assert/strict';
import {test,beforeEach} from 'node:test';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {requestFor,jobUrl} from '../../static/js/analysis/common.js';
import {renderer} from '../../static/js/analysis/view.js';

globalThis.document = {getElementById:() => null};
const {formController} = await import('../../static/js/analysis/form.js');
const {resultController} = await import('../../static/js/analysis/result.js');
const root = fileURLToPath(new URL('../../',import.meta.url));
const fixture = JSON.parse(execFileSync('py',['-3.13','-X','utf8','tests/analysis_ui/fixture.py'],{cwd:root,encoding:'utf8'}));
let nodes, selected, events, legacyRuns, legacyLoads;
class Element {
  constructor(tag) { this.tag = tag; this.children = []; this.attributes = {}; this.listeners = {}; this.dataset = {}; this.disabled = false; this.hidden = false; this.value = ''; }
  set id(value) { this._id = value; nodes?.set(value,this); }
  get id() { return this._id; }
  set textContent(value) { this.text = String(value); this.children = []; }
  get textContent() { return (this.text ?? '')+this.children.map(child => child.textContent ?? String(child)).join(''); }
  set innerHTML(_) { throw new Error('Không được chèn HTML từ model'); }
  append(...children) { this.children.push(...children); }
  replaceChildren(...children) { this.text = ''; this.children = children; }
  setAttribute(key,value) { this.attributes[key] = String(value); }
  addEventListener(name,callback) { this.listeners[name] = callback; }
}
const node = id => document.getElementById(id);
const ready = {run_enabled:true,status:'ready'};
const flush = () => new Promise(resolve => setImmediate(resolve));
beforeEach(() => {
  nodes = new Map(); selected = ['original_fix','bayesian_v1']; events = {}; legacyRuns = 0; legacyLoads = 0;
  globalThis.document = {
    getElementById(id) { if (!nodes.has(id)) nodes.set(id,new Element('div')); return nodes.get(id); },
    createElement:tag => new Element(tag),createElementNS:(_,tag) => new Element(tag),
    addEventListener:(name,callback) => events[name] = callback,
    querySelectorAll:selector => selector.includes(':checked') ? selected.map(value => ({value})) : [],
  };
  globalThis.localStorage = {setItem(){},getItem:() => null};
  globalThis.window = {legacyAnalysis:{run:() => legacyRuns++,load:() => legacyLoads++}};
  for (const [id,value] of Object.entries({'analysis-source':'asof','analysis-version':'original_fix','asof-symbol':'MWG',
    'asof-date':'2026-07-02','report-language':'vi','analysis-repeats':'1'})) node(id).value = value;
});

test('Request dùng đúng IDs, model/options snapshot; compare từ chối một bản', () => {
  const values = {mode:'compare',ids:['C2','MT_BICL'],symbol:'MWG',date:'2026-07-02',language:'vi',repeats:2};
  const models = structuredClone(fixture.data.identity.request.models);
  const request = requestFor(values,models); models.decision.options.temperature = .9;
  assert.deepEqual(request.variant_ids,['C2','MT_BICL']); assert.equal(request.models.decision.options.temperature,0);
  assert.equal(request.mode,'compare'); assert.equal(request.repeats,2);
  assert.throws(() => requestFor({...values,ids:['original_fix']},models),/COMPARE_SELECTION/);
  assert.throws(() => jobUrl('../../outside','vi'));
});
test('Sáu bản chính và hai dependency, raw/final/CASH riêng; null không thành P&L 0', () => {
  const view = renderer(fixture.config); view.render(fixture.data);
  assert.equal(node('decision-cards').children.length,6);
  assert.equal(node('control-cards').children.length,2);
  assert.match(node('shared-reports').textContent,/profile gốc \(native\)/);
  assert.match(node('shared-reports').textContent,/Alpha common synthetic/);
  assert.match(node('shared-reports').textContent,/10³ VND/);
  assert.match(node('decision-cards').children[1].textContent,/FALLBACK_ORIGINAL/);
  assert.match(node('decision-cards').textContent,/CASH/); assert.match(node('decision-cards').textContent,/NOT_EVALUATED/);
  assert.doesNotMatch(node('decision-cards').textContent,/0\.0000%/);
  assert.match(node('job-progress').textContent,/8\/8/); assert.equal(node('resume-job').disabled,true);
  const first = node('decision-cards').children[0], reports = node('shared-reports').children[0];
  const detail = first.children.find(child => child.tag === 'details'); detail.open = true;
  view.render({...fixture.data,worker_alive:true});
  assert.equal(node('decision-cards').children[0],first); assert.equal(node('shared-reports').children[0],reports);
  const changed = structuredClone(fixture.data); changed.rows[0].raw_prediction = 'LONG'; view.render(changed);
  assert.equal(node('decision-cards').children[0].children.find(child => child.tag === 'details').open,true);
});
test('Report/model context không thành HTML; chart lấy đúng prefix, không gọi giá realtime', () => {
  const data = structuredClone(fixture.data), point = Object.keys(data.snapshots)[0];
  const attack = '<img src=x onerror=attack()>';
  data.snapshots[point].payload.pattern_report = attack;
  data.snapshots[point].payload.pattern_image = 'javascript:attack()';
  Object.values(data.policy_details)[0].context.aux = {value:attack};
  renderer(fixture.config).render(data);
  assert.match(node('shared-reports').textContent,/<img src=x onerror=attack\(\)>/);
  const group = node('shared-reports').children[0], figure = group.children.find(child => child.tag === 'figure');
  const svg = figure.children[0]; assert.match(svg.attributes['aria-label'],/MWG-2026-07-02/);
  assert.equal(svg.children.find(child => child.tag === 'polyline').attributes.points,'65,180 865,25');
  assert.equal(group.children.find(child => child.tag === 'details' && child.textContent.includes(attack)).children.length,2);
});
test('Partial không tạo CASH cho slot thiếu; UNKNOWN khóa resume và giữ row đã xong', () => {
  const data = structuredClone(fixture.data); data.state = 'unknown'; data.rows = data.rows.slice(0,1);
  data.progress.decision_slots_complete = 1; data.progress.points_complete = 0;
  renderer(fixture.config).render(data);
  assert.match(node('job-error').textContent,/UUID/); assert.equal(node('resume-job').disabled,true);
  assert.equal(node('partial-note').hidden,false);
  assert.match(node('decision-cards').textContent,/Chưa hoàn tất/);
  const pending = node('decision-cards').children.filter(child => child.textContent.includes('Chưa hoàn tất'));
  assert.ok(pending.length); assert.ok(pending.every(child => !child.textContent.includes('CASH')));
});
test('UI tiếng Anh giữ nguyên báo cáo VI và không diễn giải confidence thành xác suất', () => {
  const config = structuredClone(fixture.config); config.language = 'en';
  const en = JSON.parse(execFileSync('py',['-3.13','-X','utf8','-c',"from utils.analysis_ui import messages; import json; print(json.dumps(messages('en')))"],{cwd:root,encoding:'utf8'}));
  config.messages = en; renderer(config).render(fixture.data);
  assert.match(node('decision-cards').textContent,/Original/); assert.match(node('decision-cards').textContent,/No outcome yet/);
  assert.match(node('shared-reports').textContent,/Báo cáo synthetic/); assert.doesNotMatch(node('decision-cards').textContent,/100%/);
});
test('Preflight ready chạy đúng request sáu bản, giữ model đã check và chỉ tạo một job', async () => {
  const calls = [], routes = [];
  const io = async (url,body) => { calls.push({url,body}); return url.endsWith('/defaults') ? {models:fixture.data.identity.request.models} :
    url.endsWith('/jobs') ? {run_id:fixture.data.run_id} : ready; };
  const form = formController(fixture.config,io,url => routes.push(url)); await form.init();
  selected = [...fixture.data.requested_ids]; form.invalidate(); await form.check();
  node('decision-temperature').value = .7;
  await Promise.all([form.start('compare'),form.start('compare')]);
  const jobs = calls.filter(row => row.url.endsWith('/jobs'));
  assert.equal(jobs.length,1); assert.deepEqual(jobs[0].body.variant_ids,fixture.data.requested_ids);
  assert.equal(jobs[0].body.models.decision.options.temperature,0); assert.equal(jobs[0].body.mode,'compare');
  assert.match(routes[0],/serving_run=12345678/); assert.equal(legacyRuns,0);
});
test('Đổi form hủy grant, response preflight cũ không bật lại nút; thiếu resource giữ disabled', async () => {
  const pending = [];
  const io = async (url,body,signal) => url.endsWith('/defaults') ? {models:fixture.data.identity.request.models} :
    new Promise(resolve => pending.push({resolve,signal,body}));
  const form = formController(fixture.config,io); const initial = form.init(); await flush();
  assert.equal(pending.length,2); node('analysis-version').value = 'MT_BICL'; form.invalidate();
  const current = form.check(); assert.ok(pending[0].signal.aborted);
  pending[2].resolve({run_enabled:false,status:'blocked',blockers:[{code:'RESOURCES_NOT_READY'}]});
  pending[3].resolve({run_enabled:false,status:'blocked',blockers:[{code:'RESOURCES_NOT_READY'}]}); await current;
  pending[0].resolve(ready); pending[1].resolve(ready); await initial;
  assert.equal(node('analyzeBtn').disabled,true); assert.equal(node('compareBtn').disabled,true);
  assert.match(node('preflight-status').textContent,/Resource/);
});
test('Compare thiếu lựa chọn bị khóa riêng; latest chỉ gọi native legacy, không gửi variants giả', async () => {
  selected = ['MT_BICL']; const calls = [];
  const form = formController(fixture.config,async(url,body) => { calls.push({url,body}); return url.endsWith('/defaults') ? {models:fixture.data.identity.request.models} : ready; });
  await form.init(); assert.equal(node('compareBtn').disabled,true); assert.equal(node('analyzeBtn').disabled,false);
  node('analysis-source').value = 'latest'; form.source();
  await form.start('analyze'); await form.start('compare');
  assert.equal(legacyRuns,1); assert.equal(legacyLoads,1); assert.equal(node('asof-inputs').hidden,true);
  assert.equal(calls.filter(row => row.url.endsWith('/jobs')).length,0);
  events['analysis-legacy-start'](); assert.equal(node('analysis-source').disabled,true);
  events['analysis-legacy-end'](); assert.equal(node('analysis-source').disabled,false);
});
test('Lỗi POST start mơ hồ không retry; nút chạy giữ khóa tới check/input mới', async () => {
  let jobs = 0;
  const form = formController(fixture.config,async url => {
    if (url.endsWith('/defaults')) return {models:fixture.data.identity.request.models};
    if (url.endsWith('/jobs')) { jobs++; throw new Error('offline'); } return ready;
  });
  await form.init(); await form.start('analyze'); await form.start('analyze');
  assert.equal(jobs,1); assert.equal(node('analyzeBtn').disabled,true); assert.match(node('serving-form-error').textContent,/Không tự gửi lại/);
});
test('Poll/reload chỉ GET; stop/resume body rỗng và UNKNOWN không tự retry', async () => {
  const calls = [], scheduled = [];
  const data = structuredClone(fixture.data); data.state = 'running'; data.worker_alive = true;
  const controller = resultController(fixture.config,async (url,body) => { calls.push({url,body}); return body ? {} : data; },fn => { scheduled.push(fn); return scheduled.length; },() => {});
  await controller.init(); assert.equal(calls.length,1); assert.equal(calls[0].body,undefined); assert.equal(scheduled.length,1);
  await controller.control('stop'); assert.deepEqual(calls[1].body,{}); assert.match(calls[1].url,/\/stop$/);
  data.state = 'unknown'; data.worker_alive = false; await controller.refresh(); await controller.control('resume');
  assert.equal(calls.filter(call => call.url.endsWith('/resume')).length,0);
  controller.clear();
});
test('Response poll cũ không ghi đè; sai owner/lỗi đọc xóa card và ảnh cũ', async () => {
  const pending = [];
  const controller = resultController(fixture.config,() => new Promise(resolve => pending.push(resolve)),() => 1,() => {});
  const old = controller.refresh(), current = controller.refresh();
  pending[1](fixture.data); await current; assert.equal(node('decision-cards').children.length,6);
  pending[0]({...fixture.data,state:'running'}); await old; assert.equal(node('job-state').textContent,fixture.config.messages.completed);
  const failed = resultController(fixture.config,async () => { throw new Error('404'); }); await failed.refresh();
  assert.equal(node('decision-cards').children.length,0); assert.equal(node('shared-reports').children.length,0);
  assert.equal(node('stop-job').disabled,true); assert.equal(node('resume-job').disabled,true); assert.match(node('job-error').textContent,/owner/);
});
test('ID trên URL không hợp lệ bị từ chối trước API, reload không tin sessionStorage legacy', async () => {
  let calls = 0;
  const controller = resultController({...fixture.config,runId:'../other'},async () => { calls++; return fixture.data; });
  await controller.init(); assert.equal(calls,0); assert.equal(node('resume-job').disabled,true);
});
