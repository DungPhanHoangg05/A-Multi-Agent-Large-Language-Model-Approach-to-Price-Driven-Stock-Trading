        /* ── i18n: catalogue + ngôn ngữ hiện tại / catalogue + current language ── */
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

        /* ── State ──────────────────────────────────────────────────────────── */
        let jobId = null;
        let pollHandle = null;
        let testPoints = [];
        let isRunning = false;
        let startedAt = null;
        let initialCapitalVnd = 50000000;

        // Chart instances
        let pnlChart = null;
        let accChart = null;

        function initCharts() {
            if (pnlChart) return;
            const commonOptions = {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: 'index', intersect: false },
                plugins: {
                    legend: { position: 'top', labels: { usePointStyle: true, font: { size: 11 } } }
                },
                scales: {
                    x: { grid: { display: false }, title: { display: true, text: tr('bt_test') } },
                    y: { grid: { color: 'rgba(0,0,0,0.05)' } }
                }
            };

            pnlChart = new Chart(document.getElementById('pnlChart'), {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [
                        { label: tr('bt_ds_full_pnl'), borderColor: '#2563eb', backgroundColor: 'rgba(37,99,235,0.08)', data: [], tension: 0.35, fill: true, pointRadius: 4, pointHoverRadius: 6 },
                        { label: tr('bt_ds_no_pnl'), borderColor: '#16a34a', backgroundColor: 'rgba(22,163,74,0.05)', data: [], tension: 0.35, fill: true, borderDash: [5, 5], pointRadius: 4, pointHoverRadius: 6 }
                    ]
                },
                options: {
                    ...commonOptions,
                    plugins: {
                        ...commonOptions.plugins,
                        tooltip: {
                            callbacks: {
                                label: ctx => `${ctx.dataset.label}: ${formatVnd(ctx.parsed.y)}`,
                                afterLabel: ctx => {
                                    if (ctx.dataIndex === 0) return tr('bt_initial_capital');
                                    const tp = testPoints[ctx.dataIndex - 1];
                                    if (!tp) return '';
                                    const variant = ctx.datasetIndex === 0 ? 'full' : 'no_alpha';
                                    const action = displayAccountAction(tp[`executed_action_${variant}`]);
                                    const cash = tp[`cash_${variant}_vnd`];
                                    const shares = Number(tp[`shares_${variant}`]);
                                    const fee = tp[`transaction_fee_${variant}_vnd`];
                                    return [
                                        `${tr('bt_action')}: ${action}`,
                                        `${tr('bt_cash')}: ${formatVnd(cash)}`,
                                        `${tr('bt_shares')}: ${shares.toFixed(4)}`,
                                        `${tr('bt_fee')}: ${formatVnd(fee)}`
                                    ];
                                }
                            }
                        }
                    },
                    scales: {
                        x: { grid: { display: false }, title: { display: true, text: tr('bt_chart_x') } },
                        y: {
                            grid: { color: 'rgba(0,0,0,0.05)' },
                            title: { display: true, text: tr('bt_chart_y_pnl') },
                            ticks: { callback: v => formatVnd(v) }
                        }
                    }
                }
            });

            accChart = new Chart(document.getElementById('accChart'), {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [
                        { label: tr('bt_ds_full_correct'), borderColor: '#2563eb', data: [], stepped: true },
                        { label: tr('bt_ds_no_correct'), borderColor: '#16a34a', data: [], stepped: true, borderDash: [5, 5] }
                    ]
                },
                options: commonOptions
            });
            document.getElementById('chartSection').style.display = 'grid';
        }

        /* ── Polling ────────────────────────────────────────────────────────── */
        function startBacktest() {
            const symbol = document.getElementById('cfgSymbol').value.trim().toUpperCase();
            const nTests = parseInt(document.getElementById('cfgNTests').value);
            const window_ = parseInt(document.getElementById('cfgWindow').value);
            const step = parseInt(document.getElementById('cfgStep').value);

            if (!symbol) { alert(tr('bt_enter_symbol')); return; }

            setRunning(true);
            testPoints = [];
            startedAt = Date.now();
            renderTimeline([]);
            resetScores();
            setStep('step-data', 'active');
            setStep('step-full', '');
            setStep('step-no', '');
            setStep('step-save', '');
            document.getElementById('nTotal').textContent = nTests;

            fetch('/api/backtest/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ symbol, n_tests: nTests, window_size: window_, step, language: LANG })
            })
                .then(r => r.json())
                .then(data => {
                    if (data.error) { alert(data.error); setRunning(false); return; }
                    jobId = data.job_id;
                    setStatus('running', tr('bt_running', { symbol: symbol, n: nTests }));
                    pollHandle = setInterval(poll, 4000);
                })
                .catch(e => { alert(tr('err_connection_prefix') + e.message); setRunning(false); });
        }

        function stopBacktest() {
            if (!jobId) return;
            fetch('/api/backtest/stop/' + jobId, { method: 'POST' })
                .then(() => { setStatus('stopped', tr('bt_stopped')); setRunning(false); clearInterval(pollHandle); })
                .catch(() => { });
        }

        function poll() {
            if (!jobId) return;
            fetch('/api/backtest/status/' + jobId)
                .then(r => r.json())
                .then(data => {
                    const { status, step: stepName, partial, latest, test_points: tps } = data;

                    // Update step indicator
                    if (stepName === 'loading') { setStep('step-data', 'active'); }
                    if (stepName === 'full') { setStep('step-data', 'done'); setStep('step-full', 'active'); }
                    if (stepName === 'no_alpha') { setStep('step-full', 'done'); setStep('step-no', 'active'); }
                    if (stepName === 'saving') { setStep('step-no', 'done'); setStep('step-save', 'active'); }

                    if (tps && tps.length) {
                        testPoints = tps;
                        renderTimeline(tps);
                        updateCharts(tps);
                    }
                    if (partial) updateScores(partial);
                    if (latest) showLastTest(latest);

                    if (status === 'done') {
                        clearInterval(pollHandle);
                        setRunning(false);
                        setStatus('done', tr('bt_done'));
                        ['step-data', 'step-full', 'step-no', 'step-save'].forEach(s => setStep(s, 'done'));
                        if (data.summary) renderFinalSummary(data.summary, data.partial || {});
                    } else if (status === 'error') {
                        clearInterval(pollHandle);
                        setRunning(false);
                        setStatus('error', '❌ ' + (data.error || tr('err_unknown')));
                    }
                })
                .catch(() => { });
        }

        /* ── UI helpers ─────────────────────────────────────────────────────── */
        function setRunning(on) {
            isRunning = on;
            document.getElementById('btnStart').disabled = on;
            document.getElementById('btnStop').classList.toggle('hidden', !on);
            const dot = document.getElementById('statusDot');
            dot.className = 'dot ' + (on ? 'dot-run' : 'dot-idle');
        }

        function setStatus(state, text) {
            document.getElementById('statusSub').textContent = text;
            const dot = document.getElementById('statusDot');
            if (state === 'running') dot.className = 'dot dot-run';
            else if (state === 'done') dot.className = 'dot dot-done';
            else if (state === 'error' || state === 'stopped') dot.className = 'dot dot-err';
            else dot.className = 'dot dot-idle';
        }

        function setStep(id, state) {
            const el = document.getElementById(id);
            if (!el) return;
            el.className = 'step-item' + (state ? ' ' + state : '');
        }

        function resetScores() {
            ['accFull', 'accNo', 'liftVal', 'nDone'].forEach(id => document.getElementById(id).textContent = '-');
            document.getElementById('accFullSub').textContent = tr('bt_calculating');
            document.getElementById('accNoSub').textContent = tr('bt_calculating');
            document.getElementById('liftSub').textContent = tr('bt_calculating');
            document.getElementById('pnlFullText').textContent = '-';
            document.getElementById('pnlNoText').textContent = '-';
            document.getElementById('pnlFullSub').textContent = tr('bt_pnl_sub');
            document.getElementById('pnlNoSub').textContent = tr('bt_pnl_sub');
            document.getElementById('etaSub').textContent = '-';
            document.getElementById('metricsBody').innerHTML =
                '<div class="empty"><i class="fas fa-chart-bar"></i><p>' + tr('bt_waiting_data') + '</p></div>';
        }

        function updateScores(p) {
            if (Number.isFinite(Number(p.initial_capital_vnd))) {
                initialCapitalVnd = Number(p.initial_capital_vnd);
            }
            document.getElementById('accFull').textContent = p.acc_full ?? '-';
            document.getElementById('accNo').textContent = p.acc_no_alpha ?? '-';
            document.getElementById('nDone').textContent = p.n_completed ?? 0;

            const lift = p.alpha_lift ?? 0;
            const liftEl = document.getElementById('liftVal');
            liftEl.textContent = (lift >= 0 ? '+' : '') + lift + '%';
            liftEl.style.color = lift >= 0 ? '#d97706' : '#C41E3A';

            document.getElementById('liftCard').className =
                'score-card ' + (lift >= 0 ? 'score-card-lift-pos' : 'score-card-lift-neg');

            document.getElementById('accFullSub').textContent =
                tr('bt_valid_correct', { valid: p.n_valid_full ?? 0, correct: p.n_correct_full ?? 0 });
            document.getElementById('accNoSub').textContent =
                tr('bt_valid_correct', { valid: p.n_valid_no ?? 0, correct: p.n_correct_no ?? 0 });

            // P&L Update
            if (p.pnl_full !== undefined) {
                const pf = p.pnl_full;
                const el = document.getElementById('pnlFullText');
                el.textContent = (pf >= 0 ? '+' : '') + pf.toFixed(2);
                el.style.color = pf >= 0 ? 'var(--blue)' : 'var(--red)';
                document.getElementById('pnlFullSub').textContent =
                    `${formatVnd(initialCapitalVnd)} → ${formatVnd(p.equity_full_vnd)} · P&L ${signedVnd(p.pnl_full_vnd)}`;
            }
            if (p.pnl_no_alpha !== undefined) {
                const pn = p.pnl_no_alpha;
                const el = document.getElementById('pnlNoText');
                el.textContent = (pn >= 0 ? '+' : '') + pn.toFixed(2);
                el.style.color = pn >= 0 ? 'var(--green)' : 'var(--red)';
                document.getElementById('pnlNoSub').textContent =
                    `${formatVnd(initialCapitalVnd)} → ${formatVnd(p.equity_no_alpha_vnd)} · P&L ${signedVnd(p.pnl_no_alpha_vnd)}`;
            }

            const liftDesc = lift > 2 ? tr('bt_lift_strong')
                : lift > 0 ? tr('bt_lift_slight')
                    : lift === 0 ? tr('bt_lift_none')
                        : tr('bt_lift_neg');
            document.getElementById('liftSub').textContent = liftDesc;

            // ETA
            if (startedAt && p.n_completed > 0) {
                const elapsed = (Date.now() - startedAt) / 1000;
                const perTest = elapsed / p.n_completed;
                const rem = (document.getElementById('nTotal').textContent - p.n_completed) * perTest;
                document.getElementById('etaSub').textContent =
                    rem > 0 ? tr('bt_eta', { n: Math.ceil(rem / 60) }) : tr('bt_finished');
            }

            // Metrics bars
            renderMetricBars(p);
        }

        function updateCharts(points) {
            initCharts();
            if (!points || !points.length) return;

            const labels = [0, ...points.map(tp => tp.test_id)];
            const pnlF = [initialCapitalVnd, ...points.map(tp => Number(tp.equity_full_vnd) || initialCapitalVnd)];
            const pnlN = [initialCapitalVnd, ...points.map(tp => Number(tp.equity_no_alpha_vnd) || initialCapitalVnd)];

            let cumCorrectF = 0;
            let cumCorrectN = 0;
            const accF = points.map(tp => { if (tp.correct_full) cumCorrectF++; return cumCorrectF; });
            const accN = points.map(tp => { if (tp.correct_no_alpha) cumCorrectN++; return cumCorrectN; });

            pnlChart.data.labels = labels;
            pnlChart.data.datasets[0].data = pnlF;
            pnlChart.data.datasets[1].data = pnlN;
            pnlChart.update('none');

            accChart.data.labels = points.map(tp => tp.test_id);
            accChart.data.datasets[0].data = accF;
            accChart.data.datasets[1].data = accN;
            accChart.update('none');
        }

        function renderMetricBars(p) {
            const rows = [
                { label: tr('bt_acc_total'), full: p.acc_full || 0, no: p.acc_no_alpha || 0 },
            ];
            document.getElementById('metricsBody').innerHTML = rows.map(r => `
    <div class="metric-row">
      <span class="metric-label">${r.label}</span>
      <div style="flex:1;">
        <div style="display:flex;align-items:center;gap:.5rem;margin-bottom:.4rem;">
          <span style="font-size:.72rem;color:#2563eb;width:60px;">${tr('bt_ds_full_pnl')}</span>
          <div class="metric-track" style="flex:1;">
            <div class="metric-fill-full" style="width:${Math.min(100, r.full)}%;"></div>
          </div>
          <span class="metric-val" style="color:#2563eb;">${r.full}%</span>
        </div>
        <div style="display:flex;align-items:center;gap:.5rem;">
          <span style="font-size:.72rem;color:var(--green);width:60px;">${tr('bt_ds_no_pnl')}</span>
          <div class="metric-track" style="flex:1;">
            <div class="metric-fill-no" style="width:${Math.min(100, r.no)}%;"></div>
          </div>
          <span class="metric-val" style="color:var(--green);">${r.no}%</span>
        </div>
      </div>
    </div>`).join('');
        }

        function showLastTest(tp) {
            const dir = tp.actual_direction === 'UP' ? '📈' : '📉';
            const pct = signedPct(tp.actual_pct_change);
            const executionPct = signedPct(tp.execution_pct_change);
            const fullPeriod = signedPct(tp.account_return_full);
            const noPeriod = signedPct(tp.account_return_no_alpha);
            const fullActionNote = accountActionText(tp, 'full');
            const noActionNote = accountActionText(tp, 'no_alpha');
            const fullAction = displayAccountAction(tp.executed_action_full) + (fullActionNote ? `: ${fullActionNote}` : '');
            const noAction = displayAccountAction(tp.executed_action_no_alpha) + (noActionNote ? `: ${noActionNote}` : '');
            const fullSource = tp.decision_source_full === 'fallback_conservative' ? ` [${tr('bt_decision_fallback')}]` : '';
            const noSource = tp.decision_source_no_alpha === 'fallback_conservative' ? ` [${tr('bt_decision_fallback')}]` : '';
            const prog = document.getElementById('progressFill');
            const cnt = document.getElementById('progressCount');
            const nT = parseInt(document.getElementById('nTotal').textContent) || 1;
            const done = tp.test_id;
            prog.style.width = Math.min(100, done / nT * 100) + '%';
            cnt.textContent = `${done} / ${nT}`;
            document.getElementById('lastTestInfo').innerHTML =
                `<strong>${tr('bt_test')} ${done}</strong> - ${tp.window_start} → ${tp.window_end} &nbsp;|&nbsp; ` +
                `${tr('bt_actual')}: ${dir} ${pct} &nbsp;|&nbsp; ` +
                `${tr('bt_execution')}: ${formatVnd(tp.entry_price_vnd)} → ${formatVnd(tp.exit_price_vnd)} (${executionPct}) &nbsp;|&nbsp; ` +
                `${tr('bt_ds_full_pnl')}: <strong>${tp.pred_full}${fullSource}</strong> ${tp.correct_full ? '✅' : '❌'} → ${fullAction} · ${fullPeriod} · ${formatVnd(tp.equity_full_vnd)} &nbsp;|&nbsp; ` +
                `${tr('bt_ds_no_pnl')}: <strong>${tp.pred_no_alpha}${noSource}</strong> ${tp.correct_no_alpha ? '✅' : '❌'} → ${noAction} · ${noPeriod} · ${formatVnd(tp.equity_no_alpha_vnd)}`;
        }

        function signedPct(value) {
            const number = Number(value);
            const safe = Number.isFinite(number) ? number : 0;
            return (safe >= 0 ? '+' : '') + safe.toFixed(2) + '%';
        }

        function formatVnd(value) {
            const number = Number(value);
            const safe = Number.isFinite(number) ? number : 0;
            return new Intl.NumberFormat(LANG === 'vi' ? 'vi-VN' : 'en-US', {
                maximumFractionDigits: 0
            }).format(safe) + ' ₫';
        }

        function signedVnd(value) {
            const number = Number(value);
            const safe = Number.isFinite(number) ? number : 0;
            return (safe >= 0 ? '+' : '−') + formatVnd(Math.abs(safe));
        }

        function displayAccountAction(action) {
            return action === 'BUY_SELL' ? 'BUY → SELL' : (action || 'CASH');
        }

        function accountReturnCell(tp, variant) {
            const action = tp[`executed_action_${variant}`] || 'CASH';
            const actionLabel = displayAccountAction(action);
            const actionText = accountActionText(tp, variant);
            const period = Number(tp[`account_return_${variant}`]);
            const cumulative = Number(tp[`pnl_${variant}`]);
            const cash = Number(tp[`cash_${variant}_vnd`]);
            const shares = Number(tp[`shares_${variant}`]);
            const equity = Number(tp[`equity_${variant}_vnd`]);
            const fee = Number(tp[`transaction_fee_${variant}_vnd`]);
            const slippage = Number(tp[`slippage_cost_${variant}_vnd`]);
            const periodClass = period > 0 ? 'badge-up' : period < 0 ? 'badge-down' : 'badge-unk';
            const actionNote = actionText ? `<span style="font-size:.68rem;white-space:nowrap;">${actionText}</span><br>` : '';
            return `<span class="badge ${periodClass}">${actionLabel}</span><br>` +
                actionNote +
                `<span style="font-size:.68rem;white-space:nowrap;">${tr('bt_cash')}: ${formatVnd(cash)} · ${tr('bt_shares')}: ${shares.toFixed(4)}</span><br>` +
                `<span style="font-size:.68rem;white-space:nowrap;">${tr('bt_equity')}: ${formatVnd(equity)}</span><br>` +
                `<span style="font-size:.68rem;white-space:nowrap;">${tr('bt_fee')}: ${formatVnd(fee)} · ${tr('bt_slippage')}: ${formatVnd(slippage)}</span><br>` +
                `<span style="font-size:.72rem;white-space:nowrap;">${tr('bt_period')}: ${signedPct(period)}</span><br>` +
                `<span style="font-size:.72rem;color:var(--gray-4);white-space:nowrap;">${tr('bt_cumulative')}: ${signedPct(cumulative)}</span>`;
        }

        function accountActionText(tp, variant) {
            const action = tp[`executed_action_${variant}`] || 'CASH';
            const reason = tp[`execution_skip_reason_${variant}`] || '';
            const reasonKey = {
                SHORT_STAYS_CASH: 'bt_cash_short',
                INVALID_PREDICTION: 'bt_skip_invalid'
            }[reason];
            if (action === 'BUY_SELL') return tr('bt_trade_round_trip');
            return reasonKey ? tr(reasonKey) : '';
        }

        function renderTimeline(tps) {
            const tbody = document.getElementById('timelineTbody');
            document.getElementById('timelineSub').textContent =
                tps.length ? tr('bt_test_points', { n: tps.length }) : tr('bt_no_data');

            if (!tps.length) {
                tbody.innerHTML = '<tr><td colspan="11"><div class="empty"><i class="fas fa-spinner fa-spin"></i><p>'
                    + tr('bt_waiting_first') + '</p></div></td></tr>';
                return;
            }

            tbody.innerHTML = [...tps].reverse().map(tp => {
                const dirBadge = tp.actual_direction === 'UP'
                    ? `<span class="badge badge-up">📈 UP</span>`
                    : `<span class="badge badge-down">📉 DOWN</span>`;
                const pct = signedPct(tp.actual_pct_change);
                const executionPct = signedPct(tp.execution_pct_change);

                const predBadge = (pred, source) => {
                    const badge = pred === 'LONG'
                    ? `<span class="badge badge-long">LONG</span>`
                    : pred === 'SHORT'
                        ? `<span class="badge badge-short">SHORT</span>`
                        : `<span class="badge badge-unk">?</span>`;
                    return source === 'fallback_conservative'
                        ? `${badge}<br><span style="font-size:.65rem;color:#d97706;white-space:nowrap;">${tr('bt_decision_fallback')}</span>`
                        : badge;
                };

                const okBadge = ok => ok
                    ? `<span class="badge badge-ok">✅</span>`
                    : `<span class="badge badge-fail">❌</span>`;

                const alphaAdds = tp.correct_full && !tp.correct_no_alpha ? tr('bt_alpha_helps')
                    : !tp.correct_full && tp.correct_no_alpha ? tr('bt_alpha_hurts')
                        : tp.correct_full && tp.correct_no_alpha ? tr('bt_both_right')
                            : tr('bt_both_wrong');

                return `<tr>
      <td>${tp.test_id}</td>
      <td style="font-size:.75rem;">${tp.window_start}<br><span style="color:var(--gray-4);">→ ${tp.window_end}</span></td>
      <td>${dirBadge}<br><span style="font-size:.72rem;color:var(--gray-4);">${pct}</span></td>
      <td style="font-size:.75rem;white-space:nowrap;">O ${formatVnd(tp.entry_price_vnd)} → C ${formatVnd(tp.exit_price_vnd)}<br><span style="color:var(--gray-4);">${executionPct}</span></td>
      <td>${predBadge(tp.pred_full, tp.decision_source_full)}</td>
      <td>${okBadge(tp.correct_full)}</td>
      <td>${accountReturnCell(tp, 'full')}</td>
      <td>${predBadge(tp.pred_no_alpha, tp.decision_source_no_alpha)}</td>
      <td>${okBadge(tp.correct_no_alpha)}</td>
      <td>${accountReturnCell(tp, 'no_alpha')}</td>
      <td style="font-size:.8rem;">${alphaAdds}</td>
    </tr>`;
            }).join('');
        }

        function renderFinalSummary(s, p) {
            // p = partial (pnl_full, pnl_no_alpha); s = summary (win rates)
            const pnlFull = (p && p.pnl_full  !== undefined) ? p.pnl_full  : (s.pnl_full  || 0);
            const pnlNo   = (p && p.pnl_no_alpha !== undefined) ? p.pnl_no_alpha : (s.pnl_no_alpha || 0);

            // Cập nhật các card P&L / update P&L cards
            const elPF = document.getElementById('pnlFullText');
            if (elPF) {
                elPF.textContent = (pnlFull >= 0 ? '+' : '') + pnlFull.toFixed(2);
                elPF.style.color = pnlFull >= 0 ? 'var(--blue)' : 'var(--red)';
                document.getElementById('pnlFullSub').textContent =
                    `${formatVnd(s.initial_capital_vnd)} → ${formatVnd(s.equity_full_vnd)} · P&L ${signedVnd(s.pnl_full_vnd)}`;
            }
            const elPN = document.getElementById('pnlNoText');
            if (elPN) {
                elPN.textContent = (pnlNo >= 0 ? '+' : '') + pnlNo.toFixed(2);
                elPN.style.color = pnlNo >= 0 ? 'var(--green)' : 'var(--red)';
                document.getElementById('pnlNoSub').textContent =
                    `${formatVnd(s.initial_capital_vnd)} → ${formatVnd(s.equity_no_alpha_vnd)} · P&L ${signedVnd(s.pnl_no_alpha_vnd)}`;
            }

            // Cập nhật metrics bars / update metric bars
            const mb = document.getElementById('metricsBody');
            const fmt = v => (v !== null && v !== undefined && !isNaN(v)) ? v : 0;
            const mkRow = (label, full, no, unit = '%', barMax = 100) => `
    <div class="metric-row">
      <span class="metric-label">${label}</span>
      <div style="flex:1;">
        <div style="display:flex;align-items:center;gap:.5rem;margin-bottom:.4rem;">
          <span style="font-size:.72rem;color:#2563eb;width:60px;">${tr('bt_ds_full_pnl')}</span>
          <div class="metric-track" style="flex:1;">
            <div class="metric-fill-full" style="width:${Math.min(100, Math.max(0, (fmt(full)/barMax)*100))}%;"></div>
          </div>
          <span class="metric-val" style="color:#2563eb;">${(fmt(full) >= 0 ? (unit==='%'&&barMax!==100?'+':'') : '')}${fmt(full).toFixed ? fmt(full).toFixed(1) : fmt(full)}${unit}</span>
        </div>
        <div style="display:flex;align-items:center;gap:.5rem;">
          <span style="font-size:.72rem;color:var(--green);width:60px;">${tr('bt_ds_no_pnl')}</span>
          <div class="metric-track" style="flex:1;">
            <div class="metric-fill-no" style="width:${Math.min(100, Math.max(0, (fmt(no)/barMax)*100))}%;"></div>
          </div>
          <span class="metric-val" style="color:var(--green);">${(fmt(no) >= 0 ? (unit==='%'&&barMax!==100?'+':'') : '')}${fmt(no).toFixed ? fmt(no).toFixed(1) : fmt(no)}${unit}</span>
        </div>
      </div>
    </div>`;

            mb.innerHTML = [
                mkRow(tr('bt_acc_total'), fmt(s.acc_full), fmt(s.acc_no_alpha), '%', 100),
                mkRow(tr('bt_pnl_sim'), pnlFull, pnlNo, '%', Math.max(20, Math.abs(pnlFull), Math.abs(pnlNo))),
                mkRow(tr('bt_win_long'), fmt(s.long_win_full), fmt(s.long_win_no_alpha), '%', 100),
                mkRow(tr('bt_win_short'), fmt(s.short_win_full), fmt(s.short_win_no_alpha), '%', 100),
            ].join('');
        }
