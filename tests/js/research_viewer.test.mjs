// Kiểm logic DOM bằng mô hình in-memory; không mở hoặc tự động hóa trình duyệt.
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {test, beforeEach} from 'node:test';
import {number} from '../../static/js/experiments/dom.js';
import {renderer} from '../../static/js/experiments/view.js';

const root = fileURLToPath(new URL('../../', import.meta.url));
const fixture = JSON.parse(execFileSync('py', ['-3.13', '-X', 'utf8', '-c',
  'import json; from pathlib import Path; from core.research_results import ResearchResults; from utils.research_view import view; from utils.research_i18n import messages; from core.serving_registry import registry_document; print(json.dumps({"data":view(ResearchResults(Path.cwd()),{}),"config":{"messages":messages("vi"),"language":"vi","variants":registry_document()["variants"]}}))'],
  {cwd: root, encoding: 'utf8', maxBuffer: 2**22}));

class Element {
  constructor(tag) { this.tag = tag; this.children = []; this.attributes = {}; this.value = 'all'; this.hidden = true; this.dataset = {}; this.listeners = {}; }
  set textContent(value) { this.text = String(value); this.children = []; }
  get textContent() { return (this.text ?? '') + this.children.map(child => child.textContent ?? String(child)).join(''); }
  set innerHTML(_) { throw new Error('Không được ghi HTML từ artifact'); }
  append(...children) { this.children.push(...children); }
  replaceChildren(...children) { this.text = ''; this.children = children; }
  setAttribute(key, value) { this.attributes[key] = String(value); }
  addEventListener(name, callback) { this.listeners[name] = callback; }
  get selectedOptions() { return this.children.filter(child => child.value === this.value); }
}
let nodes;
beforeEach(() => {
  nodes = new Map();
  globalThis.document = {getElementById(id) { if (!nodes.has(id)) nodes.set(id, new Element('div')); return nodes.get(id); },
    createElement: tag => new Element(tag), createElementNS: (_, tag) => new Element(tag)};
  globalThis.Option = class extends Element { constructor(text, value) { super('option'); this.textContent = text; this.value = value; } };
  globalThis.location = {origin: 'http://localhost'};
});

test('Giữ null thành NA, số 0 và số âm giữ đúng nghĩa', () => {
  assert.equal(number(null), 'NA'); assert.equal(number(undefined), 'NA'); assert.equal(number(NaN), 'NA');
  assert.equal(number(0), '0.000'); assert.equal(number(-.7), '-0.700'); assert.equal(number(.5, 2, 100), '50.00');
});
test('Summary, missingness, contrast plot và export lấy đúng dữ liệu khóa', () => {
  renderer(fixture.config).research(fixture.data, new URLSearchParams());
  const rows = nodes.get('summary-rows').children;
  assert.equal(rows.length, 8);
  assert.equal(rows[0].children[1].textContent, fixture.data.summary[0].mean_account_return_pct.toFixed(3));
  assert.match(nodes.get('stats').textContent, /79\/102/);
  const svg = nodes.get('contrast-chart').children[0];
  const points = svg.children.filter(node => node.tag === 'circle');
  assert.deepEqual(points.map(node => +node.attributes['data-effect']), fixture.data.contrasts.filter(row => row.endpoint === 'account_return_percentage_points').map(row => row.effect_pp));
  assert.equal(nodes.get('downloads').children.length, 4);
  assert.match(nodes.get('downloads').children[2].href, /export_table=details/);
});
test('NA có lý do, nội dung artifact không được thực thi thành HTML', () => {
  const data = structuredClone(fixture.data);
  data.summary[0].mcc = null; data.summary[0].method = '<img src=x onerror=attack()>';
  renderer(fixture.config).research(data, new URLSearchParams());
  const row = nodes.get('summary-rows').children[0];
  assert.equal(row.children[0].textContent, '<img src=x onerror=attack()>');
  assert.equal(row.children[4].textContent, 'NA'); assert.ok(row.children[4].title.length);
});
test('Chi tiết rỗng không tạo CASH, contrast rỗng không vẽ band mới', () => {
  const data = structuredClone(fixture.data);
  data.details.rows = []; data.details.total = 0; data.contrasts = [];
  renderer(fixture.config).research(data, new URLSearchParams());
  assert.equal(nodes.get('detail-rows').children.length, 0);
  assert.equal(nodes.get('contrast-chart').textContent, fixture.config.messages.no_contrast);
  assert.equal(nodes.get('page-info').textContent, fixture.config.messages.no_rows);
  assert.ok(nodes.get('next').disabled); assert.ok(nodes.get('prev').disabled);
});
test('Legacy giữ CASH return 0 và null của metric chưa xác định', () => {
  document.getElementById('variant').value = 'original_fix';
  renderer(fixture.config).legacy({rows: [{variant: 'original_fix', point_id: 'FPT', raw_proposal: null,
    final_action: 'CASH', strategy_return: 0, reason: 'FALLBACK', quality: 'fixture'}], accounts: {'original_fix/FPT': {total_return_pct: null}},
    complete_slots: 1, planned_slots: 1, points: 1, mode: 'fixture'}, 'legacy');
  assert.equal(nodes.get('legacy-rows').children[0].children[3].textContent, '0.0000');
  assert.match(nodes.get('legacy-accounts').textContent, /NA/);
});
test('Đổi filter nhanh bỏ response cũ; lỗi/empty xóa dữ liệu và link export cũ', async () => {
  document.getElementById('research-config').textContent = JSON.stringify(fixture.config);
  document.getElementById('baseline').value = 'original_fix';
  document.getElementById('table').value = 'predictions';
  let selected = fixture.data.filters.methods;
  document.querySelectorAll = () => selected.map(value => ({value}));
  const pending = [];
  const response = data => ({ok: true, json: async () => data});
  globalThis.fetch = async (url, options) => {
    if (url.startsWith('/api/serving/v1/')) return response({runs:[]});
    if (url.endsWith('/runs')) return response({default: 'u09_analysis_r1', runs: [{id: 'u09_analysis_r1', kind: 'paper_evidence', label: 'U09'}]});
    return new Promise(resolve => pending.push({resolve, signal: options.signal}));
  };
  const flush = () => new Promise(resolve => setImmediate(resolve));
  await import('../../static/js/experiments/main.js?race-test');
  assert.equal(pending.length, 1);
  selected = ['bayesian_v1'];
  nodes.get('filters').listeners.submit({preventDefault() {}});
  assert.equal(pending.length, 2); assert.ok(pending[0].signal.aborted);
  const latest = structuredClone(fixture.data);
  latest.summary = latest.summary.filter(row => row.method === 'bayesian_v1');
  pending[1].resolve(response(latest)); await flush();
  assert.equal(nodes.get('summary-rows').children.length, 1);
  pending[0].resolve(response(fixture.data)); await flush();
  assert.equal(nodes.get('summary-rows').children.length, 1);
  nodes.get('filters').listeners.submit({preventDefault() {}});
  pending[2].resolve({ok: false}); await flush();
  assert.ok(nodes.get('research-result').hidden);
  assert.ok(nodes.get('error').textContent.length);
  assert.equal(nodes.get('downloads').children.length, 0);
  nodes.get('kind').value = 'legacy_offline'; nodes.get('kind').listeners.change(); await flush();
  assert.equal(nodes.get('empty').hidden, false);
  assert.ok(nodes.get('research-result').hidden);
});
