        // ── i18n: catalogue + ngôn ngữ hiện tại / catalogue + current language ─────
        const T = JSON.parse(document.getElementById("legacy-config").textContent).messages;
        const LANG = JSON.parse(document.getElementById("legacy-config").textContent).language;

        /** Lấy chuỗi đã dịch, hỗ trợ {placeholder}. / Translate with {placeholder}. */
        function tr(key, vars) {
            let s = T[key] != null ? T[key] : key;
            if (vars) {
                for (const k in vars) s = s.split('{' + k + '}').join(vars[k]);
            }
            return s;
        }

        let maDaChon = '';
        let KHUNG_THOI_GIAN = '1d';   // updated when user picks a timeframe
        let danhSachMa = [];
        let keyDaLuu = false;

        // ── Timeframe selector ─────────────────────────────────────────────────────
        const TF_META = {
            "5m": { label: "5m - " + tr('tf_5m'), desc: tr('tf_recent_candles', { n: 78 }), icon: "fas fa-stopwatch" },
            "15m": { label: "15m - " + tr('tf_15m'), desc: tr('tf_recent_candles', { n: 60 }), icon: "fas fa-clock" },
            "30m": { label: "30m - " + tr('tf_30m'), desc: tr('tf_recent_candles', { n: 50 }), icon: "fas fa-clock" },
            "1h": { label: "1h - " + tr('tf_1h'), desc: tr('tf_recent_candles', { n: 45 }), icon: "fas fa-clock" },
            "1d": { label: "1D - " + tr('tf_1d'), desc: tr('tf_recent_candles', { n: 45 }), icon: "fas fa-calendar-day" },
            "1w": { label: "1W - " + tr('tf_1w'), desc: tr('tf_recent_candles', { n: 52 }), icon: "fas fa-calendar-week" },
            "1mo": { label: "1M - " + tr('tf_1mo'), desc: tr('tf_recent_candles', { n: 36 }), icon: "fas fa-calendar-alt" },
        };

        function initTimeframeSelector() {
            document.querySelectorAll('.tf-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    document.querySelectorAll('.tf-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    KHUNG_THOI_GIAN = btn.dataset.tf;
                    const meta = TF_META[KHUNG_THOI_GIAN] || {};
                    document.getElementById('tfLabel').textContent = meta.label || KHUNG_THOI_GIAN;
                    document.getElementById('tfDesc').textContent = meta.desc || '';
                });
            });
        }

        // ── Step tracking (7 steps) ────────────────────────────────────────────────
        const STEP_IDS = ['step1', 'step2', 'step3', 'step4', 'step5', 'step6'];
        let _currentStep = 0;

        function setLoadingStep(step) {
            _currentStep = step;
            STEP_IDS.forEach((id, idx) => {
                const stepNum = idx + 1;
                const el = document.getElementById(id);
                if (!el) return;
                el.classList.remove('active', 'done');
                if (step >= 7) {
                    el.classList.add('done');
                } else if (stepNum < step) {
                    el.classList.add('done');
                } else if (stepNum === step) {
                    el.classList.add('active');
                }
            });
        }

        function resetLoadingSteps() {
            _currentStep = 0;
            STEP_IDS.forEach(id => {
                const el = document.getElementById(id);
                if (el) el.classList.remove('active', 'done');
            });
        }

        // ── API Key ────────────────────────────────────────────────────────────────
        function toggleKeyVisibility() {
            const inp = document.getElementById('groqApiKeyInput');
            const icon = document.getElementById('toggleKeyIcon');
            if (inp.type === 'password') { inp.type = 'text'; icon.className = 'fas fa-eye-slash'; }
            else { inp.type = 'password'; icon.className = 'fas fa-eye'; }
        }

        function luuApiKey() {
            const apiKey = document.getElementById('groqApiKeyInput').value.trim();
            const statusEl = document.getElementById('apiKeyStatus');
            if (!apiKey) { statusEl.innerHTML = '<div class="key-status-err"><i class="fas fa-times-circle"></i> ' + tr('key_enter_prompt') + '</div>'; return; }
            if (!apiKey.startsWith('gsk_')) { statusEl.innerHTML = '<div class="key-status-err"><i class="fas fa-times-circle"></i> ' + tr('key_bad_format') + '</div>'; return; }
            statusEl.innerHTML = '<div style="color:var(--gray-500);font-size:0.82rem;"><i class="fas fa-spinner fa-spin"></i> ' + tr('key_connecting') + '</div>';
            fetch('/api/update-api-key', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ api_key: apiKey }) })
                .then(r => r.json()).then(data => {
                    if (data.success) {
                        statusEl.innerHTML = '<div class="key-status-ok"><i class="fas fa-check-circle"></i> ' + tr('key_ok') + '</div>';
                        keyDaLuu = true;
                        document.dispatchEvent(new Event('analysis-key-changed'));
                        document.getElementById('apiNotice').classList.add('hidden');
                        localStorage.setItem('groq_key_set', '1');
                        kiemTraGroq();
                    } else {
                        statusEl.innerHTML = '<div class="key-status-err"><i class="fas fa-times-circle"></i> ' + (data.error || tr('key_invalid')) + '</div>';
                    }
                }).catch(e => { statusEl.innerHTML = '<div class="key-status-err"><i class="fas fa-times-circle"></i> ' + tr('err_connection_prefix') + e.message + '</div>'; });
        }

        function kiemTraGroq() {
            const dot = document.getElementById('groqStatusDot'), text = document.getElementById('groqStatusText');
            dot.className = 'status-dot loading'; text.textContent = tr('st_checking_groq');
            fetch('/api/groq-status').then(r => r.json()).then(data => {
                if (data.valid) {
                    dot.className = 'status-dot ok'; text.textContent = tr('st_groq_ready');
                    document.getElementById('groqBadge').style.display = 'inline-flex';
                    document.getElementById('agentModelTag').style.display = 'inline-block';
                    document.getElementById('graphModelTag').style.display = 'inline-block';
                    document.getElementById('agentModelTag').textContent = (data.agent_model || '').split('/').pop().substring(0, 20);
                    document.getElementById('graphModelTag').textContent = (data.graph_model || '').split('/').pop().substring(0, 20);
                    document.getElementById('apiNotice').classList.add('hidden');
                    keyDaLuu = true;
                } else {
                    dot.className = 'status-dot warn'; text.textContent = tr('st_groq_unconfigured');
                    document.getElementById('groqBadge').style.display = 'none';
                }
            }).catch(() => { dot.className = 'status-dot err'; text.textContent = tr('st_groq_check_failed'); });
        }

        function kiemTraTrangThaiRT() {
            const dot = document.getElementById('rtStatusDot'), text = document.getElementById('rtStatusText');
            dot.className = 'status-dot loading'; text.textContent = tr('st_checking_vnstock');
            fetch('/api/realtime-status').then(r => r.json()).then(data => {
                const rows = [];
                rows.push('<div class="rt-status-row"><span class="rt-status-icon ' + (data.available ? 'rt-pip-ok' : 'rt-pip-err') + '">' + (data.available ? '✅' : '❌') + '</span><div><div class="rt-status-label">' + tr('vnstock_library') + '</div><div class="rt-status-value">' + (data.available ? tr('vnstock_installed') : (data.install_cmd || 'pip install vnstock')) + '</div></div></div>');
                if (data.available) {
                    const via = data.connected_via ? ' (' + data.connected_via + ')' : '';
                    rows.push('<div class="rt-status-row"><span class="rt-status-icon ' + (data.connected ? 'rt-pip-ok' : 'rt-pip-err') + '">' + (data.connected ? '🌐' : '🔌') + '</span><div><div class="rt-status-label">' + tr('data_connection') + via + '</div><div class="rt-status-value">' + (data.connected ? 'OK - ' + data.test_symbol + ': ' + data.test_rows + ' ' + tr('candles') : (data.error || tr('st_connect_failed'))) + '</div></div></div>');
                    rows.push('<div class="rt-status-row"><span class="rt-status-icon">📡</span><div><div class="rt-status-label">' + tr('data_sources') + '</div><div class="rt-status-value">' + (data.sources || ['VCI', 'MSN']).join(' → ') + '</div></div></div>');
                    rows.push('<div class="rt-status-row"><span class="rt-status-icon">🗄️</span><div><div class="rt-status-label">' + tr('cache') + '</div><div class="rt-status-value">' + tr('cache_items', { n: (data.cached_items || 0), ttl: (data.cache_ttl || 300) }) + '</div></div></div>');
                }
                document.getElementById('rtDetailRows').innerHTML = rows.join('');
                if (!data.available) { dot.className = 'status-dot warn'; text.textContent = tr('st_vnstock_missing'); }
                else if (data.connected) {
                    dot.className = 'status-dot ok'; text.textContent = tr('st_rt_ready');
                    document.getElementById('rtBadge').style.display = 'inline-block';
                    const lb = document.getElementById('lastUpdateBadge');
                    lb.style.display = 'flex'; lb.className = 'last-update live';
                    document.getElementById('lastUpdateTime').textContent = new Date().toLocaleTimeString(tr('locale_tag'));
                } else { dot.className = 'status-dot err'; text.textContent = tr('st_connect_failed'); }
            }).catch(() => { dot.className = 'status-dot err'; text.textContent = tr('st_status_check_failed'); });
        }

        function xoaCache() {
            fetch('/api/realtime-cache/clear', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' })
                .then(r => r.json()).then(() => { hienThongBao(tr('cache_cleared'), 'ok'); kiemTraTrangThaiRT(); })
                .catch(e => hienThongBao(tr('err_clear_cache') + e.message, 'error'));
        }

        function taiDanhSachMa() {
            const container = document.getElementById('stockListContainer');
            container.innerHTML = '<div style="padding:2rem;text-align:center;color:var(--gray-400);"><i class="fas fa-spinner fa-spin"></i> ' + tr('loading_from_vnstock') + '</div>';
            fetch('/api/assets').then(r => r.json()).then(data => {
                danhSachMa = data.assets || [];
                const soLuong = danhSachMa.length;
                document.getElementById('stockCountBadge').textContent = soLuong;
                document.getElementById('symbolCountLabel').textContent = tr('st_symbol_count', { n: soLuong.toLocaleString(tr('locale_tag')) });
                hienThiDanhSachMa(danhSachMa);
                const daChu = localStorage.getItem('vn_selected_asset');
                if (daChu && danhSachMa.find(s => s.code === daChu)) chonMa(daChu);
            }).catch(() => { container.innerHTML = '<div style="padding:1.5rem;text-align:center;color:#ef4444;"><i class="fas fa-exclamation-triangle"></i> ' + tr('err_load_symbol_list') + '</div>'; });
        }

        function hienThiDanhSachMa(dsMa) {
            const container = document.getElementById('stockListContainer');
            if (!dsMa.length) { container.innerHTML = '<div style="padding:1.5rem;text-align:center;color:var(--gray-400);">' + tr('no_symbol_found') + '</div>'; return; }
            container.innerHTML = dsMa.map(s => {
                const tenCty = s.name && s.name !== s.code ? s.name : '';
                const san = s.exchange || '';
                const sanB = san ? '<span class="stock-exchange">' + san + '</span>' : '';
                const tenDong = tenCty ? '<div class="stock-company" title="' + tenCty + '">' + tenCty + '</div>' : '';
                return '<div class="stock-item ' + (s.code === maDaChon ? 'active' : '') + '" data-code="' + s.code + '" onclick="chonMa(\'' + s.code + '\')"><div class="stock-dot"></div><div style="flex:1;min-width:0;"><div style="display:flex;align-items:center;gap:0.4rem;"><span class="stock-code">' + s.code + '</span>' + sanB + '</div>' + tenDong + '</div></div>';
            }).join('');
        }

        function locMa(tuKhoa) {
            const q = tuKhoa.trim().toUpperCase();
            if (!q) { hienThiDanhSachMa(danhSachMa); return; }
            hienThiDanhSachMa(danhSachMa.filter(s => s.code.includes(q) || (s.name && s.name.toUpperCase().includes(q))));
        }

        function chonMa(ma) {
            maDaChon = ma;
            localStorage.setItem('vn_selected_asset', ma);
            document.querySelectorAll('.stock-item').forEach(el => el.classList.toggle('active', el.dataset.code === ma));
            const co = danhSachMa.find(s => s.code === ma) || {};
            const tenCty = co.name && co.name !== ma ? co.name : '';
            const display = document.getElementById('selectedStockDisplay');
            display.classList.add('visible');
            document.getElementById('selectedStockCode').textContent = ma;
            const tenEl = document.getElementById('selectedStockName');
            if (tenEl) tenEl.textContent = tenCty ? '- ' + tenCty : '';
            taiThongTinMa(ma);
        }

        function taiThongTinMa(ma) {
            const card = document.getElementById('stockInfoCard');
            card.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + tr('loading');
            fetch('/api/stock-info/' + ma).then(r => r.json()).then(info => {
                if (!info.exists) { card.innerHTML = '<div style="display:flex;align-items:center;gap:0.6rem;flex-wrap:wrap;"><strong style="color:var(--vn-red);font-size:1.05rem;">' + ma + '</strong><span class="live-tag"><i class="fas fa-bolt"></i> ' + tr('realtime') + '</span></div><div style="color:var(--gray-500);font-size:0.78rem;margin-top:0.4rem;">' + tr('fetch_on_run_hint') + '</div>'; return; }
                const tenVN = info.organ_name || info.name || '';
                const tenEN = info.en_organ_name || info.en_name || '';
                // Ở chế độ tiếng Anh ưu tiên tên tiếng Anh / prefer the English name in EN mode
                const tenChinh = LANG === 'en' ? (tenEN || tenVN) : tenVN;
                const tenPhu = LANG === 'en' ? (tenEN ? tenVN : '') : tenEN;
                const san = info.exchange || '';
                const nganh = info.industry || '';
                const dongTen = tenChinh ? '<div style="grid-column:1/-1;margin-bottom:0.35rem;"><span style="color:var(--gray-500);font-size:0.78rem;">' + tr('company') + '</span><br><strong style="color:var(--gray-800);font-size:0.88rem;line-height:1.4;">' + tenChinh + '</strong>' + (tenPhu ? '<div style="color:var(--gray-500);font-size:0.76rem;">' + tenPhu + '</div>' : '') + '</div>' : '';
                const sanB = san ? '<span style="display:inline-block;background:var(--vn-red);color:#fff;border-radius:5px;padding:0.1rem 0.45rem;font-size:0.7rem;font-weight:700;margin-left:0.3rem;">' + san + '</span>' : '';
                card.innerHTML = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.35rem 0.6rem;">' + dongTen + '<div><span style="color:var(--gray-500);font-size:0.78rem;">' + tr('symbol') + '</span><br><strong style="color:var(--vn-red);font-size:1.05rem;">' + info.code + '</strong>' + sanB + '<span class="live-tag" style="margin-left:0.3rem;"><i class="fas fa-bolt"></i> ' + tr('live') + '</span></div>' + (nganh ? '<div><span style="color:var(--gray-500);font-size:0.78rem;">' + tr('industry') + '</span><br><strong style="font-size:0.85rem;">' + nganh + '</strong></div>' : '') + '</div>';
            }).catch(() => { card.innerHTML = '<span style="color:var(--gray-500);">' + tr('err_load_stock_info') + '</span>'; });
        }

        function capNhatModel() {
            const agentModel = document.getElementById('agentModelInput').value.trim();
            const graphModel = document.getElementById('graphModelInput').value.trim();
            const successEl = document.getElementById('settingsSuccess'), errorEl = document.getElementById('settingsError');
            successEl.style.display = errorEl.style.display = 'none';
            if (!agentModel || !graphModel) { errorEl.textContent = tr('err_models_both'); errorEl.style.display = 'block'; return; }
            fetch('/api/update-models', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ agent_model: agentModel, graph_model: graphModel, language: LANG }) })
                .then(r => r.json()).then(data => {
                    if (data.success) { successEl.innerHTML = '<i class="fas fa-check-circle"></i> ' + tr('models_saved', { text: data.agent_model, vision: data.graph_model }); successEl.style.display = 'block'; setTimeout(() => successEl.style.display = 'none', 4000); }
                    else { errorEl.textContent = data.error || tr('err_update_failed'); errorEl.style.display = 'block'; }
                }).catch(e => { errorEl.textContent = tr('err_connection_prefix') + e.message; errorEl.style.display = 'block'; });
        }

        function resetBtn() {
            document.dispatchEvent(new Event('analysis-legacy-end'));
            const btn = document.getElementById('analyzeBtn');
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-play"></i> ' + tr('run_analysis') + ' <i class="fas fa-arrow-right"></i>';
            document.getElementById('loadingOverlay').classList.remove('active');
            resetLoadingSteps();
        }

        function chayPhanTich() {
            if (!maDaChon) { hienThongBao(tr('warn_select_stock'), 'warn'); return; }
            if (!keyDaLuu) { hienThongBao(tr('warn_save_key'), 'warn'); document.getElementById('groqApiKeyInput').focus(); return; }
            document.dispatchEvent(new Event('analysis-legacy-start'));
            const btn = document.getElementById('analyzeBtn');
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + tr('analyzing');
            document.getElementById('loadingOverlay').classList.add('active');
            resetLoadingSteps();
            setLoadingStep(1);

            // Update step1 label with selected timeframe
            const tfMeta = TF_META[KHUNG_THOI_GIAN] || {};
            const step1El = document.getElementById('step1Text');
            if (step1El) step1El.textContent = tr('load_step1_tf', { tf: tfMeta.label || KHUNG_THOI_GIAN });

            // Gửi kèm ngôn ngữ để các tác tử trả lời đúng ngôn ngữ / send language so agents reply in it
            fetch('/api/analyze', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ asset: maDaChon, timeframe: KHUNG_THOI_GIAN, language: LANG }) })
                .then(r => r.json()).then(data => {
                    if (data.error) { resetBtn(); hienThongBao(data.error, 'error'); return; }
                    if (!data.job_id) { resetBtn(); hienThongBao(tr('err_no_job_id'), 'error'); return; }
                    pollJob(data.job_id, 0);
                }).catch(err => { resetBtn(); hienThongBao(tr('err_no_flask') + ' (' + err.message + ')', 'error'); });
        }

        function pollJob(jobId, attempt) {
            if (attempt >= 150) { resetBtn(); hienThongBao(tr('err_timeout'), 'error'); return; }
            setTimeout(() => {
                fetch('/api/analyze/status/' + jobId).then(r => r.json()).then(data => {
                    if (typeof data.step === 'number' && data.step > _currentStep) setLoadingStep(data.step);
                    if (data.status === 'running') { pollJob(jobId, attempt + 1); return; }
                    setLoadingStep(7);
                    setTimeout(() => {
                        resetBtn();
                        const result = data.result || {};
                        if (data.status === 'error' || result.error) { hienThongBao(result.error || tr('err_unknown'), 'error'); return; }
                        if (result.redirect) {
                            sessionStorage.setItem('analysisResults', JSON.stringify(result));
                            window.location.href = result.redirect;
                        }
                    }, 600);
                }).catch(err => { resetBtn(); hienThongBao(tr('err_poll') + err.message, 'error'); });
            }, 2000);
        }

        function lamMoiTatCa() { kiemTraGroq(); kiemTraTrangThaiRT(); }

        function hienThongBao(noi_dung, loai) {
            const cu = document.getElementById('toastMsg'); if (cu) cu.remove();
            const cls = loai === 'error' ? 'alert-danger' : loai === 'warn' ? 'alert-warning' : 'alert-success';
            const el = document.createElement('div');
            el.id = 'toastMsg'; el.className = 'alert ' + cls;
            el.style.cssText = 'position:fixed;bottom:1.5rem;right:1.5rem;z-index:99999;min-width:280px;max-width:420px;box-shadow:0 8px 24px rgba(0,0,0,0.15);';
            el.innerHTML = noi_dung; document.body.appendChild(el);
            setTimeout(() => el.remove(), 6000);
        }

        document.addEventListener('DOMContentLoaded', () => {
            initTimeframeSelector();
            kiemTraGroq();
            if (localStorage.getItem('groq_key_set') === '1') keyDaLuu = true;

        });

// Chỉ tải danh sách realtime khi chọn nguồn legacy; giữ nhịp kiểm trạng thái năm phút.
window.legacyAnalysis = {run: chayPhanTich, load: () => {
    kiemTraTrangThaiRT(); taiDanhSachMa();
    setInterval(() => { if (document.getElementById('analysis-source').value === 'legacy') kiemTraTrangThaiRT(); }, 5 * 60 * 1000);
}};
