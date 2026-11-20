// Các phần dùng chung không ghi HTML từ response hoặc model.
export const byId = id => document.getElementById(id);
export const CURRENT_PROFILE = 'variant_serving_v1';
export const FINALIZED_PROFILE = 'finalize_serving_v1';
export function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text != null) node.textContent = String(text);
  if (className) node.className = className;
  return node;
}
export function label(config, id) {
  return config.registry.variants.find(v => v.id === id)?.label[config.language] ?? id;
}
export function jobUrl(id, language, source = 'asof') {
  if (!/^[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}$/.test(id)) throw new Error('Invalid job ID');
  return '/output?' + new URLSearchParams({serving_run: id, lang: language, ...(source === 'live' ? {serving_source:'live'} : {})});
}
export async function json(url, body, signal) {
  const response = await fetch(url, {signal, credentials:'same-origin', cache:'no-store',
    ...(body === undefined ? {} : {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})});
  const data = await response.json();
  if (!response.ok) throw Object.assign(new Error('Request failed'), {data, status:response.status});
  return data;
}
export function requestFor(values, models) {
  if (values.mode === 'compare' && values.ids.length < 2) throw new Error('COMPARE_SELECTION');
  return {version:values.version || CURRENT_PROFILE,mode:values.mode,variant_ids:[...values.ids],symbols:[values.symbol],
    start_date:values.date,end_date:values.date,timeframe:'1d',language:values.language,repeats:values.repeats,
    models:structuredClone(models)};
}
export function blockerText(blocker, text, language = 'vi') {
  if (blocker.code === 'HOSTED_RELEASE_PENDING_FIN10') return language === 'en'
    ? 'Hosted execution for the repaired profile is pending release.'
    : 'Bản sửa đang chờ phát hành chạy API.';
  const key = {CREDENTIAL_MISSING:'blocked_credential',SUPPORT_MISMATCH:'blocked_support',RESOURCES_NOT_READY:'blocked_resource',
    MODEL_NOT_RELEASED:'blocked_model',TOKENIZER_NOT_READY:'blocked_tokenizer'}[blocker.code];
  return key ? text[key] : blocker.code;
}

export function profileText(version, language) {
  if (!version) return '';
  if (version !== FINALIZED_PROFILE) return version;
  const label = language === 'en' ? 'Repaired profile · exploratory · PIT unverified independently'
    : 'Bản sửa · nghiên cứu thăm dò · PIT nguồn chưa xác minh độc lập';
  return `${label} (${version})`;
}

export function captureErrorMessage(error, config) {
  const detail = error?.data?.capture_error;
  const message = detail?.message?.[config.language];
  if (typeof message !== 'string' || !/^[A-Z_]{3,80}$/.test(detail?.code ?? '') || !/^[a-z.]{3,48}$/.test(detail?.stage ?? '')) return config.messages.live_failed;
  return `${message} [${detail.code} · ${detail.stage}]`;
}
