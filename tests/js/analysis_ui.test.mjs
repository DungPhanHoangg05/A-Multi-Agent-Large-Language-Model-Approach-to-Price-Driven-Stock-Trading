// DOM in-memory kiểm hành vi và an toàn text; không thay cho nghiệm thu browser.
import assert from 'node:assert/strict';
import {test,beforeEach} from 'node:test';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';
import {requestFor,jobUrl} from '../../static/js/analysis/common.js';
import {renderer} from '../../static/js/analysis/view.js';
import {runTimeframe} from '../../static/js/analysis/timeframe.js';

globalThis.document = {getElementById:() => null};
const {formController} = await import('../../static/js/analysis/form.js');
const {resultController} = await import('../../static/js/analysis/result.js');
const root = fileURLToPath(new URL('../../',import.meta.url));
const fixture = JSON.parse(execFileSync('py',['-3.13','-X','utf8','tests/analysis_ui/fixture.py'],{cwd:root,encoding:'utf8'}));
let nodes, selected, events, legacyRuns, legacyLoads;
const {followAnalysis,showAgentProgress} = await import('../../static/js/analysis/progress.js');
const {renderReport,normalizeIndicator} = await import('../../static/js/analysis/report.js');
class Element {
  constructor(tag) { this.tag = tag; this.children = []; this.attributes = {}; this.listeners = {}; this.dataset = {}; this.disabled = false; this.hidden = false; this.value = ''; this.classes = new Set(); this.classList = {toggle:(key,on) => on ? this.classes.add(key) : this.classes.delete(key)}; }
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
  globalThis.window = {legacyAnalysis:{run:() => { legacyRuns++; events['analysis-legacy-start']?.(); },begin:() => { events['analysis-legacy-start']?.(); return true; },end:() => events['analysis-legacy-end']?.(),load:() => legacyLoads++,selection:() => ({symbol:'MWG',timeframe:'1d'})}};
  for (const [id,value] of Object.entries({'analysis-source':'asof','analysis-version':'original_fix','asof-symbol':'MWG',
    'asof-date':'2026-07-02','report-language':'vi','analysis-repeats':'1'})) node(id).value = value;
});
test('Profile sửa dùng snapshot raw và preflight riêng, kết quả giữ đúng route/schema', async () => {
  const calls = [], config = fixture.config;
  const selection = {symbol:'MWG',timeframe:'1d',version:'finalize_serving_v1',variant:'original_fix',language:'vi',repeats:1};
  const io = async (url,body) => {
    calls.push({url,body});
    if (url.endsWith('/snapshot')) return {symbol:'MWG',cutoff:'2026-10-01',snapshot_id:'a'.repeat(64),capture_version:'finalize_live_raw_capture_v1'};
    return url.endsWith('/preflight') ? ready : {run_id:fixture.data.run_id};
  };
  const result = await runTimeframe(config,selection,fixture.data.identity.request.models,io,() => {});
  assert.deepEqual(calls[0].body,{symbol:'MWG',profile:'finalize_serving_v1'});
  assert.equal(calls[1].body.version,'variant_serving_live_v1');
  assert.equal(calls[1].body.request.version,'finalize_serving_v1');
  assert.equal(calls[1].body.chart_timeframe,undefined);
  assert.deepEqual(calls[1].body,calls[2].body);
  assert.match(result.url,/presentation=analysis/);
});
test('Preflight chặn hosted profile sửa và giữ thông báo tiếng Anh', async () => {
  const calls=[];
  const config = {...fixture.config,language:'en'};
  const selection = {symbol:'MWG',timeframe:'1d',version:'finalize_serving_v1',variant:'C2',language:'en',repeats:1};
  const io = async (url) => {
    calls.push(url);
    return url.endsWith('/snapshot') ? {symbol:'MWG',cutoff:'2026-10-01',snapshot_id:'a'.repeat(64),capture_version:'finalize_live_raw_capture_v1'}
      : {run_enabled:false,status:'blocked',blockers:[{code:'HOSTED_RELEASE_PENDING_FIN10'}]};
  };
  await assert.rejects(runTimeframe(config,selection,fixture.data.identity.request.models,io,() => {}), /Hosted execution.*pending/);
  assert.equal(calls.length,2);
});

test('Kết quả profile sửa hiển thị phạm vi PIT và xuất đúng namespace owner', () => {
  const data = structuredClone(fixture.data);
  data.identity.request = {...data.identity.request,version:'finalize_serving_v1',mode:'analyze'};
  data.scientific_status = 'EXPLORATORY_NOT_CERTIFIED';
  const view = renderer({...fixture.config,language:'en',source:'live'});
  view.render(data);
  assert.match(node('job-profile').textContent,/PIT unverified independently .*finalize_serving_v1/);
  assert.match(node('job-provenance').textContent,/EXPLORATORY_NOT_CERTIFIED/);
  assert.equal(node('export-job').href,`/api/serving/live/v1/jobs/${data.run_id}/export`);
  assert.equal(node('export-job').hidden,false);
  data.identity.request.repeats = 1;
  view.render(data);
  assert.match(node('full-report').href,/presentation=analysis/);
  assert.equal(node('full-report').hidden,false);
  view.error('Không đọc được job');
  assert.equal(node('job-profile').textContent,'');
  assert.equal(node('export-job').hidden,true);
  assert.equal(node('full-report').hidden,true);
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
test('UI tiếng Anh dùng báo cáo EN đã lưu và không diễn giải confidence thành xác suất', () => {
  const config = structuredClone(fixture.config); config.language = 'en';
  const en = JSON.parse(execFileSync('py',['-3.13','-X','utf8','-c',"from utils.analysis_ui import messages; import json; print(json.dumps(messages('en')))"],{cwd:root,encoding:'utf8'}));
  const data=structuredClone(fixture.data);
  data.presentations=Object.fromEntries(Object.keys(data.snapshots).map(point=>[point,Object.fromEntries(['indicator','pattern','trend','alpha','sentiment'].map(role=>[role,{vi:'Báo cáo synthetic',en:'Stored English report'}]))]));
  config.messages = en; renderer(config).render(data);
  assert.match(node('decision-cards').textContent,/Original/); assert.match(node('decision-cards').textContent,/No outcome yet/);
  assert.match(node('shared-reports').textContent,/Stored English report/);
  assert.doesNotMatch(node('shared-reports').textContent,/Báo cáo synthetic/); assert.doesNotMatch(node('decision-cards').textContent,/100%/);
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

test('Reload kết quả live chỉ đọc đúng namespace, giữ nguồn và thời điểm capture', async () => {
  const calls = [], data = structuredClone(fixture.data);
  data.identity.request.data_source = 'live';
  data.live_input = {captured_at:'2026-11-13T10:00:00+07:00'};
  const controller = resultController({...fixture.config,source:'live'},async (url,body) => { calls.push({url,body}); return data; });
  await controller.init();
  assert.equal(calls[0].url,'/api/serving/live/v1/jobs/'+fixture.data.run_id);
  assert.equal(calls[0].body,undefined); assert.match(node('job-meta').textContent,/Realtime/);
  assert.match(node('job-meta').textContent,/2026-11-13T10:00:00/);
});

test('Poll trạng thái intraday chỉ chạy khi đang chọn nguồn legacy, không làm mới snapshot live', () => {
  const registry = new Map(), calls = []; let heartbeat;
  const mockDocument = {addEventListener(){},querySelectorAll:() => [],getElementById(id) {
    if (!registry.has(id)) registry.set(id,{style:{},textContent:'',value:'',innerHTML:''});
    return registry.get(id);
  }};
  mockDocument.getElementById('legacy-config').textContent = JSON.stringify({messages:{},language:'vi'});
  const context = {document:mockDocument,window:{},fetch:url => { calls.push(url); return new Promise(() => {}); },
    setInterval:callback => heartbeat = callback,localStorage:{getItem:() => null}};
  runInNewContext(readFileSync(root+'/static/js/analysis/legacy_form.js','utf8'),context);
  context.window.legacyAnalysis.load(); calls.length = 0;
  heartbeat(); assert.deepEqual(calls,['/api/realtime-status']);
});

test('Chart kết quả intraday giữ đúng timestamp và nhãn 5m, không đổi thành đường daily', () => {
  const data = structuredClone(fixture.data);
  data.identity.request.chart_timeframe = '5m'; data.identity.request.data_source = 'live';
  data.live_input = {chart_timeframe:'5m',captured_at:'2026-11-13T10:00:00+07:00'};
  data.realtime_chart = {Datetime:['2026-11-13 09:00:00','2026-11-13 09:05:00'],Close:[1,2]};
  renderer(fixture.config).render(data);
  assert.match(node('shared-reports').textContent,/5m/); assert.match(node('shared-reports').textContent,/09:05:00/);
  assert.match(node('job-meta').textContent,/5m/);
});

test('Capture lỗi trả đúng VNINDEX/giai đoạn trong UI, không che thành lỗi chung hoặc gọi model', async () => {
  node('analysis-source').value = 'legacy'; node('analysis-version').value = 'C2';
  const calls = [];
  const io = async url => {
    calls.push(url);
    if (url.endsWith('/defaults')) return {models:fixture.data.identity.request.models};
    throw Object.assign(new Error('Request failed'),{status:409,data:{capture_error:{code:'CAPTURE_INDEX_DAILY',stage:'index.daily',
      message:{vi:'Không lấy được Close VNINDEX.',en:'Could not load VNINDEX Close.'}}}});
  };
  const form = formController(fixture.config,io); await form.init(); await form.start('analyze');
  assert.match(node('timeframe-run-status').textContent,/VNINDEX.*CAPTURE_INDEX_DAILY.*index.daily/);
  assert.equal(calls.filter(url => url.endsWith('/jobs')).length,0); assert.equal(legacyRuns,0);
});

test('Hệ gốc chờ cấu hình chạy của máy chủ và khóa nút nếu không tải được', async () => {
  const calls = [];
  const form = formController(fixture.config,async url => { calls.push(url); throw new Error('offline'); });
  await form.init();
  assert.equal(legacyLoads,1);
  assert.equal(node('legacy-inputs').hidden,false); assert.equal(node('analyzeBtn').disabled,true);
  await form.start(); assert.equal(legacyRuns,0);
  assert.deepEqual(calls,['/api/serving/v1/defaults']);
});

test('Sáu phương pháp dùng profile nghiên cứu mặc định; nhấn hai lần chỉ tạo một job', async () => {
  for (const variant of ['original_fix','bayesian_v1','C2','A_tp_pool','B_semantic','MT_BICL']) {
    node('analysis-version').value = variant;
    const calls = [],routes = []; let polls = 0;
    const io = async (url,body) => {
      calls.push({url,body});
      if (url.endsWith('/defaults')) return {models:fixture.data.identity.request.models};
      if (url.endsWith('/snapshot')) {
        assert.equal(node('step-bicl').hidden,variant === 'original_fix');
        assert.ok(node('step1').classes.has('active'));
        return {symbol:'MWG',cutoff:'2026-11-13',capture_version:'finalize_live_raw_capture_v1',snapshot_id:'c'.repeat(64)};
      }
      if (url.endsWith('/preflight')) return ready;
      if (url.endsWith('/jobs')) return {run_id:fixture.data.run_id};
      assert.equal(routes.length,0);
      const result = structuredClone(fixture.data); Object.assign(result.identity.request,{mode:'analyze',variant_ids:[variant]});
      result.state = ++polls === 1 ? 'running' : 'completed'; result.worker_alive = polls === 1;
      result.agent_progress = {loading:'complete',indicator:'complete',pattern:'complete',trend:'complete',alpha:'complete',context:'complete',decision:polls===1 ? 'running' : 'complete'};
      return result;
    };
    const form = formController(fixture.config,io,url => routes.push(url),async () => {});
    await form.init(); await Promise.all([form.start(),form.start()]);
    const jobs = calls.filter(call => call.url.endsWith('/jobs'));
    assert.equal(jobs.length,1); assert.deepEqual(jobs[0].body.request.variant_ids,[variant]);
    assert.equal(jobs[0].body.request.timeframe,'1d'); assert.equal(jobs[0].body.request.repeats,1);
    assert.equal(jobs[0].body.request.version,'finalize_serving_v1');
    assert.deepEqual(calls.find(call => call.url.endsWith('/preflight')).body,jobs[0].body);
    assert.equal(polls,2); assert.match(routes[0],/presentation=analysis/);
    assert.equal(node('step-bicl').hidden,variant === 'original_fix');
    assert.equal(node('step-bicl').classes.has('done'),variant !== 'original_fix');
    assert.ok(node('step6').classes.has('done')); assert.equal(node('analysis-version').disabled,false);
  }
  assert.equal(legacyRuns,0);
});

test('Tiến trình phản ánh checkpoint và quota; UNKNOWN không redirect hoặc gửi lại', async () => {
  const data = structuredClone(fixture.data); data.identity.request.mode = 'analyze';
  data.state = 'unknown'; data.agent_progress = {indicator:'complete',pattern:'running',trend:'pending'};
  data.retry_at = 1000000;
  showAgentProgress(data,fixture.config);
  assert.ok(node('step2').classes.has('done')); assert.ok(node('step3').classes.has('active'));
  assert.ok(!node('step4').classes.has('done')); assert.match(node('analysis-progress-message').textContent,/Chờ đến/);
  const calls = [];
  await assert.rejects(followAnalysis(fixture.config,data.run_id,async (url,body) => { calls.push({url,body}); return data; },() => {}),/UUID/);
  assert.equal(calls.length,1); assert.equal(calls[0].body,undefined);
});

test('POST tạo job mơ hồ khóa gửi lại; capture/preflight không rơi sang Original', async () => {
  node('analysis-version').value = 'C2'; let jobs = 0;
  const form = formController(fixture.config,async url => {
    if (url.endsWith('/defaults')) return {models:fixture.data.identity.request.models};
    if (url.endsWith('/snapshot')) return {symbol:'MWG',cutoff:'2026-11-13',capture_version:'finalize_live_raw_capture_v1',snapshot_id:'c'.repeat(64)};
    if (url.endsWith('/preflight')) return ready;
    jobs++; throw new Error('offline');
  });
  await form.init(); await form.start(); await form.start();
  assert.equal(jobs,1); assert.equal(legacyRuns,0); assert.equal(node('analyzeBtn').disabled,true);
  assert.match(node('timeframe-run-status').textContent,/Không tự gửi lại/);
});

test('Báo cáo ở bố cục Original giữ bold/bảng nhưng không thực thi HTML/link model', () => {
  const target = new Element('div');
  renderReport(target,'## Báo cáo\n**LONG** và `<script>`\n| Tên | Giá |\n|---|---|\n| FPT | 100 |\n<img src=x onerror=attack()>\n- [link](javascript:attack())');
  assert.match(target.textContent,/LONG/); assert.match(target.textContent,/<img src=x/);
  assert.match(target.textContent,/javascript:attack/);
  assert.ok(target.children.some(child => child.tag==='h2'));
  assert.ok(target.children.some(child => child.children.some(node => node.tag==='table')));
  const tags = parent => [parent.tag,...parent.children.flatMap(child => tags(child))];
  assert.ok(!tags(target).includes('img')); assert.ok(!tags(target).includes('script')); assert.ok(!tags(target).includes('a'));
});

test('Preflight blocked giữ lỗi resource, không gọi model hoặc chuyển về Original', async () => {
  node('analysis-version').value = 'MT_BICL'; const calls = [];
  const form = formController(fixture.config,async url => {
    calls.push(url);
    if (url.endsWith('/defaults')) return {models:fixture.data.identity.request.models};
    if (url.endsWith('/snapshot')) return {symbol:'MWG',cutoff:'2026-11-13',capture_version:'finalize_live_raw_capture_v1',snapshot_id:'c'.repeat(64)};
    return {run_enabled:false,status:'blocked',blockers:[{code:'RESOURCES_NOT_READY'}]};
  });
  await form.init(); await form.start();
  assert.match(node('timeframe-run-status').textContent,/Resource/);
  assert.equal(calls.filter(url => url.endsWith('/jobs')).length,0); assert.equal(legacyRuns,0);
});

test('Đổi VI/EN trước lần poll đầu không thêm BICL vào hệ gốc', async () => {
  const baseQuery = document.querySelectorAll;
  const en = new Element('button'); en.lang = 'en';
  document.querySelectorAll = selector => selector === '[data-progress-language]' ? [en] : baseQuery(selector);
  for (const id of ['step1','step2','step3','step4','step5','step-bicl','step6']) {
    const span = new Element('span');
    node(id).querySelector = () => span;
  }
  const config = {...fixture.config,progressLocales:{
    vi:{title:'Đang phân tích',messages:fixture.config.messages,steps:['Dữ liệu','Chỉ báo','Mô hình','Xu hướng','Alpha','Quyết định']},
    en:{title:'Analysis',messages:{bicl_step:'BICL context'},steps:['Data','Indicator','Pattern','Trend','Alpha','Decision']}}};
  const form = formController(config,async url => {
    if (url.endsWith('/defaults')) return {models:fixture.data.identity.request.models};
    en.listeners.click();
    throw new Error('fixture capture');
  });
  await form.init();
  await form.start();
  assert.equal(node('step-bicl').hidden,true);
  assert.equal(node('step3').querySelector().textContent,'Pattern');
  assert.equal(node('step5').querySelector().textContent,'Alpha');
  assert.equal(node('analysis-progress-title').textContent,'Analysis');
  assert.equal(node('loadingOverlay').lang,'en');
});

test('HTML Original tham chiếu giữ đủ 5 alpha, công thức, thành phần, chuyên gia và table header thật', () => {
  const reference=JSON.parse(readFileSync(root+'/tests/analysis_ui/report_reference.json','utf8'));
  const target=new Element('div'); renderReport(target,reference.alpha);
  const find=(parent,tag) => [parent,...parent.children.flatMap(child => find(child,tag))].filter(child => child.tag===tag);
  assert.equal(find(target,'thead')[0].children[0].children.length,6);
  assert.equal(find(target,'tbody')[0].children.length,5);
  assert.ok(find(target,'th').every(node => node.attributes.scope==='col'));
  assert.match(target.textContent,/Công thức đầy đủ/); assert.match(target.textContent,/composite_score/);
  assert.match(target.textContent,/Chuyên gia định lượng/); assert.match(target.textContent,/TỔNG HỢP/);
  assert.ok(find(target,'em').length>=5); assert.ok(find(target,'hr').length>=5);
  const indicator=new Element('div'); renderReport(indicator,normalizeIndicator(reference.indicator));
  assert.match(indicator.textContent,/39\.4957/); assert.ok(find(indicator,'hr').length>=4);
});

test('Indicator số được chuẩn hóa header/bảng mà không đổi số hoặc rò guard prompt', () => {
  const raw='=== MACD (12,26,9) — CHỈ ĐỌC SỐ TRONG SECTION NÀY ===\n| Chỉ số | Giá trị mới nhất | Chuỗi 5 nến gần nhất |\n|---|---|---|\n| MACD Line | **-2.8411** | [-3.009, -2.9592] |\n[END MACD SECTION — giá trị Histogram=0.1286 KHÔNG áp dụng cho chỉ báo khác]\n---\n=== RSI (14) — CHỈ ĐỌC SỐ TRONG SECTION NÀY ===\n- RSI: **30.4664**';
  const target=new Element('div'); renderReport(target,normalizeIndicator(raw));
  const tags = parent => [parent.tag,...parent.children.flatMap(child => tags(child))];
  assert.equal(tags(target).filter(tag => tag==='th').length,3); assert.equal(tags(target).filter(tag => tag==='td').length,3);
  assert.match(target.textContent,/-2\.8411/); assert.match(target.textContent,/30\.4664/);
  assert.doesNotMatch(target.textContent,/CHỈ ĐỌC|END MACD|===/);
  assert.equal(tags(target).filter(tag => tag==='h3').length,2);
});

test('Indicator VI/EN bỏ cảnh báo nội bộ và icon, giữ giá trị, dấu âm và nhận định sau quy tắc', () => {
  const saved = JSON.parse(readFileSync(root+'/tests/analysis_ui/locale_regression.json','utf8'));
  const forbidden = /ĐÃ XÁC ĐỊNH BỞI HỆ THỐNG|ĐÃ ĐẾM BỞI HỆ THỐNG|Quy tắc bắt buộc|CHỈ ĐỌC SỐ|KHÔNG dùng|KHÔNG có Histogram|Mandatory rules|BY THE SYSTEM|DO NOT use|NO Histogram|ranh giới cứng|cross-reference|\p{Extended_Pictographic}|[←→]|[^\S\n]*[−–—]/iu;
  for (const [raw, title, afterwards] of [
    [saved.source,'## PHÂN LOẠI TÍN HIỆU','### Nhận xét\n- ⚡ MACD−Signal = −0.1974 ‒ rủi ro tăng–giảm.'],
    [saved.expected_translation,'## INDICATOR CLASSIFICATION','### Outlook\n- ✔️ MACD−Signal = −0.1974 ‒ upside–downside risk.'],
  ]) {
    const text = normalizeIndicator(raw+'\n\n'+afterwards);
    assert.ok(text.includes(title));
    for (const value of ['Histogram=0.1286','MACD Line=-2.8411','-4.9336%','%K=10.5486, %D=12.3251',
      '3/5','2/5','0/5','MACD-Signal = -0.1974 -']) assert.ok(text.includes(value), value);
    assert.doesNotMatch(text,forbidden);
    assert.equal(normalizeIndicator(text),text);
  }
});

test('Màn hình chi tiết lọc Indicator giống báo cáo và giữ nguyên nội dung đã lưu', () => {
  const data = structuredClone(fixture.data);
  const {source,expected_translation} = JSON.parse(readFileSync(root+'/tests/analysis_ui/locale_regression.json','utf8'));
  const point = Object.keys(data.snapshots)[0];
  data.presentations = {[point]:{indicator:{vi:source,en:expected_translation}}};
  for (const language of ['vi','en']) {
    renderer({...fixture.config,language}).render(data);
    const sections = node('shared-reports').children[0].children;
    const indicator = sections.find(section => section.tag === 'details' &&
      section.children[0].textContent === fixture.config.messages.indicator_report);
    const report = indicator.children.find(child => child.tag === 'pre').textContent;
    assert.match(report,/Histogram=0\.1286/);
    assert.doesNotMatch(report,/Quy tắc bắt buộc|Mandatory rules|⚠️|—/u);
  }
  assert.equal(data.presentations[point].indicator.vi,source);
  assert.equal(data.presentations[point].indicator.en,expected_translation);
});

test('Màn hình chi tiết hiển thị giải thích quyết định và bỏ mã task trong trace', () => {
  const data = structuredClone(fixture.data);
  const point = Object.keys(data.snapshots)[0];
  const detail = data.policy_details[`forecast/${point}/r0/original_fix`];
  detail.context.trace = {episode_id:'MWG:2025-01-06', task_id:'MWG:block0021', population_ids:['MWG:2025-01-07']};
  detail.raw_reply.justification = 'FIN05 · MWG@2025-01-06 suy yếu.';
  const before = structuredClone(detail);
  renderer(fixture.config).render(data);
  const text = node('decision-cards').children[0].textContent;
  assert.match(text,/MWG · 2025-01-06 suy yếu/);
  assert.doesNotMatch(text,/FIN05|MWG[@:]2025|block0021|episode_id|task_id|population_ids/u);
  assert.deepEqual(detail,before);
});
