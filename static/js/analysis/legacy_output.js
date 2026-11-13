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

        document.addEventListener('DOMContentLoaded', () => {

            // Khôi phục ảnh base64 từ sessionStorage
            const raw = sessionStorage.getItem('analysisResults');
            if (raw) {
                try {
                    const data = JSON.parse(raw);
                    if (data.pattern_chart) {
                        const img = document.getElementById('patternChart');
                        if (img) img.src = `data:image/png;base64,${data.pattern_chart}`;
                    }
                    if (data.trend_chart) {
                        const img = document.getElementById('trendChart');
                        if (img) img.src = `data:image/png;base64,${data.trend_chart}`;
                    }
                    sessionStorage.removeItem('analysisResults');
                } catch (e) { console.warn('sessionStorage parse error:', e); }
            }

            // Render Markdown
            ['indicatorContent', 'patternContent', 'trendContent', 'sentimentContent'].forEach(id => {
                const el = document.getElementById(id);
                if (!el) return;
                const rawHtml = el.innerHTML;
                try {
                    const decoded = rawHtml
                        .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&')
                        .replace(/&quot;/g, '"').replace(/&#39;/g, "'");
                    const toRender = (id === 'trendContent' && !decoded.includes('**'))
                        ? normalizeTrendPlainText(decoded)
                        : decoded;
                    el.innerHTML = marked.parse(toRender);
                } catch (e) { console.warn('marked error [' + id + ']:', e); }
                el.classList.add('auto-beautify');
            });

            renderPanelAlpha();
        });

        function normalizeTrendPlainText(text) {
            // Nhận cả nhãn tiếng Việt và tiếng Anh: báo cáo cũ có thể ở ngôn ngữ khác.
            // Match VI and EN labels - a stored report may be in the other language.
            const LABEL_KEYS = ['trend_lbl_direction', 'trend_lbl_support', 'trend_lbl_resistance',
                'trend_lbl_slope', 'trend_lbl_price_vs_sup', 'trend_lbl_detail',
                'trend_lbl_forecast', 'trend_lbl_confidence'];
            const VI_FALLBACK = ['Hướng xu hướng', 'Mức hỗ trợ', 'Mức kháng cự', 'Độ dốc đường xu hướng', 'Giá so với hỗ trợ', 'Phân tích chi tiết', 'Dự đoán', 'Độ tin cậy'];
            const EN_FALLBACK = ['Trend direction', 'Support level', 'Resistance level', 'Trendline slope', 'Price vs support', 'Detailed analysis', 'Forecast', 'Confidence'];
            const LABELS = [...new Set(
                LABEL_KEYS.map(k => T[k]).filter(Boolean)
                    .concat(VI_FALLBACK, EN_FALLBACK)
            )];
            const escapedLabels = LABELS.map(l => l.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
            const labelPattern = new RegExp('\\*{0,2}(' + escapedLabels.join('|') + ')\\*{0,2}\\s*:', 'gi');
            const matches = [...text.matchAll(labelPattern)];
            if (matches.length < 2) return text.split(/\s{2,}/).filter(Boolean).map(s => s.trim()).join('\n\n');
            const segments = [];
            matches.forEach((match, i) => {
                const label = match[1];
                const start = match.index + match[0].length;
                const end = i + 1 < matches.length ? matches[i + 1].index : text.length;
                const value = text.slice(start, end).trim().replace(labelPattern, '').trim();
                if (value) segments.push(`**${label}:** ${value}`);
            });
            return segments.join('\n\n');
        }

        function renderPanelAlpha() {
            const container = document.getElementById('alphaContent');
            if (!container) return;

            // ── Decode HTML entities ───────────────────────────────────────
            const rawHtml = container.innerHTML;
            let decoded;
            try {
                decoded = rawHtml
                    .replace(/&lt;/g, '<').replace(/&gt;/g, '>')
                    .replace(/&amp;/g, '&').replace(/&quot;/g, '"')
                    .replace(/&#39;/g, "'");
            } catch (e) {
                decoded = container.innerText || container.textContent || '';
            }

            if (!decoded.trim()) return;

            // ── Extract CONSENSUS line for the badge ──────────────────────
            // Chấp nhận cả "TỔNG HỢP" và "SUMMARY" / accept both VI and EN headings.
            const summaryWords = [...new Set([T.alpha_summary, 'TỔNG HỢP', 'SUMMARY'].filter(Boolean))]
                .map(w => w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
            const summaryRe = new RegExp('^(?:' + summaryWords.join('|') + ')\\s*:\\s*(.+)$', 'im');
            const consensusMatch = decoded.match(summaryRe);
            const consensusLine = consensusMatch ? consensusMatch[1].trim() : null;
            const textForRender = decoded.replace(
                new RegExp('^(?:' + summaryWords.join('|') + ')\\s*:.*$', 'im'), '').trim();

            // ── Render as markdown (same as indicator agent) ───────────────
            let rendered = '';
            try {
                rendered = marked.parse(textForRender);
            } catch (e) {
                console.warn('marked error in alphaContent:', e);
                rendered = `<div style="white-space:pre-wrap;">${textForRender}</div>`;
            }

            // ── Build consensus bar from parsed CONSENSUS line ─────────────
            let consensusHtml = '';
            if (consensusLine) {
                const upper = consensusLine.toUpperCase();
                let cssClass = 'mixed';
                let pct = 50;
                if (/\bLONG\b/.test(upper) && !/\bSHORT\b/.test(upper)) { cssClass = 'majority-long'; }
                else if (/\bSHORT\b/.test(upper) && !/\bLONG\b/.test(upper)) { cssClass = 'majority-short'; }
                const fracMatch = consensusLine.match(/(\d+)\s*\/\s*(\d+)/);
                if (fracMatch) pct = Math.round((parseInt(fracMatch[1]) / parseInt(fracMatch[2])) * 100);
                const color = cssClass === 'majority-long' ? '#16a34a' : cssClass === 'majority-short' ? '#dc2626' : '#6b7280';
                const label = cssClass === 'majority-long' ? tr('consensus_buy') : cssClass === 'majority-short' ? tr('consensus_sell') : tr('consensus_mixed');
                consensusHtml = `
                    <div class="alpha-consensus-section" style="margin-top:1.5rem;">
                        <span class="consensus-label"><i class="fas fa-calculator"></i> ${tr('alpha_consensus')}</span>
                        <div class="consensus-bar-wrap">
                            <div class="consensus-bar-track">
                                <div class="consensus-bar-fill ${cssClass}" style="width:${pct}%;"></div>
                            </div>
                        </div>
                        <span class="consensus-text" style="color:${color};font-weight:700;">${label} - ${consensusLine}</span>
                    </div>`;
            }

            // ── Write final output ─────────────────────────────────────────
            container.innerHTML = `<div class="auto-beautify alpha-sequential-report">${rendered}</div>${consensusHtml}`;
        }
