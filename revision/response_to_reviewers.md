# Response to reviewer comments

Current response for the unified manuscript release dated 13 November 2026. We thank the reviewers and distinguish two historical studies: the original Full/Base corrected-chart evaluation and the separately collected U08/U09 extension on the same eligible calendar. They retain separate responses, method interfaces, statistics and provenance; neither repeats nor matching dates enlarge the independent market sample. The article preserves the author's title, metadata, eight-section framework and A-F topics while reporting negative economics, baseline-dependent effects and unfulfilled evidence requirements.

All 18 comments and 87 indexed requests are mapped below and in the synchronized matrix. `documented_with_limits` means the specified explanation/evidence is present within its stated scope; it does not mean reviewer acceptance. Other states explicitly retain missing scientific evidence, unresolved historical identities, editorial requests or rights/author-route dependencies. **Zero of eighteen comments is certified closed.** Native row-wise causal status remains FAIL and whole-system NOT_CERTIFIED.

Locations below refer only to the newly built release: main has 51 physical pages and submit 50, including the unnumbered highlights sheet. Physical page 2 is the title/abstract page, with subsequent printed numbers one lower than physical pages. PDFs have no printed line numbering; source lines, LaTeX labels and physical pages are supplied, with text bounding boxes where applicable. Author/CRediT blocks are commented in submit; funding remains rendered, so anonymity/journal-route compliance is not certified.

The [final release manifest](../docs/plan/revision_evidence/README.md#manuscript_unified_final_v1), [request crosswalk](../docs/plan/revision_evidence/README.md#manuscript_unified_final_v1), [current matrix](reviewer_matrix.csv) and [archive runbook](archive_runbook.md) identify evidence, source bytes and exact PDF versions. The pre-F05 response and 43-row matrix are preserved byte-for-byte in the F05 QA archive; all older releases remain unchanged. The current 87-row matrix supersedes their current-status claims and stale locators. No inference, scoring, bootstrap, refitting, upload or submission is performed in F05. Local handoff is complete; public rights/PID and scientific/editorial acceptance are separate.

## R1 — Baselines, class imbalance and economic interpretation

### R1.1

We replaced the 180-point legacy headline with the completed common-support historical study: 102 eligible symbol-cutoff units, 25 UP and 77 DOWN, over twelve dates and six blocks. Full and Base use identical truths and eligibility. Table 3 and companion S1 report pooled, symbol and block support; six unavailable early BHN cells remain excluded rather than becoming CASH predictions. The separately collected U08/U09 extension uses the same 102 eligible market points, one upstream realization and three Decision repeats; it is not added to the original sample size.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Purposive historical support; missing BHN cells stay excluded; no representative population claim.

Evidence: [outputs/revision/final_baselines_v1/classification.csv](../outputs/revision/final_baselines_v1/classification.csv); [outputs/revision/final_baselines_v1/per_class.csv](../outputs/revision/final_baselines_v1/per_class.csv); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/results.tex:6](../paper/content/results.tex) (`Table~\ref{tab:classification}`); [paper/content/tables/component/classification.tex:6](../paper/content/tables/component/classification.tex) (`\label{tab:classification}`); [paper/content/tables/component/accounts.tex:6](../paper/content/tables/component/accounts.tex) (`\label{tab:accounts}`).

Verified PDF locations: main physical pp. 20, 26, 27, 29, 44; main_submit physical pp. 20, 26, 27, 28, 43. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R1.2

Table 3 reports BA, MCC, accuracy, LONG rate and precision/recall for both classes. Full BA is 52.96%, MCC 0.060 and accuracy 65.69%; Base BA is 49.71%, MCC -0.005 and accuracy 60.78%. Both identify seven of 25 UP outcomes; Full has 17 false LONG forecasts versus 22 for Base. Undefined metrics are NA/null, and unweighted symbol macro summaries retain their planned and defined denominators in S1. Extension Table 5 and Table F.3 retain both Native/Common baselines, five extensions, Fact_Anchor and CASH/Always-LONG controls with class-aware metrics.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Class-aware reporting is supplied; independent predictive validation is not established.

Evidence: [outputs/revision/final_baselines_v1/classification.csv](../outputs/revision/final_baselines_v1/classification.csv); [outputs/revision/final_baselines_v1/per_class.csv](../outputs/revision/final_baselines_v1/per_class.csv); [outputs/revision/final_baselines_v1/report.md](../outputs/revision/final_baselines_v1/report.md); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/results.tex:6](../paper/content/results.tex) (`Table~\ref{tab:classification}`); [paper/content/tables/component/classification.tex:6](../paper/content/tables/component/classification.tex) (`\label{tab:classification}`); [paper/content/tables/component/accounts.tex:6](../paper/content/tables/component/accounts.tex) (`\label{tab:accounts}`).

Verified PDF locations: main physical pp. 26, 27, 29, 44; main_submit physical pp. 26, 27, 28, 43. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R1.3

Always-CASH and a majority rule fitted on purged historical training data are both included on every eligible test unit and by symbol in S1. They coincide on this test set, with 75.49% pooled accuracy, BA 50% and undefined MCC; the training rule was not fitted to the observed test majority. A correct DOWN forecast is a CASH decision and earns no short-sale return. The extension keeps CASH and cost-bearing Always-LONG cycles; Always-LONG is not continuous buy-and-hold.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Training-majority and CASH coincide on this support; DOWN predictions do not earn a short-sale return.

Evidence: [outputs/revision/final_baselines_v1/baseline_contracts.json](../outputs/revision/final_baselines_v1/baseline_contracts.json); [outputs/revision/final_baselines_v1/classification.csv](../outputs/revision/final_baselines_v1/classification.csv); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/results.tex:6](../paper/content/results.tex) (`Table~\ref{tab:classification}`); [paper/content/tables/component/classification.tex:6](../paper/content/tables/component/classification.tex) (`\label{tab:classification}`); [paper/content/tables/component/accounts.tex:6](../paper/content/tables/component/accounts.tex) (`\label{tab:accounts}`).

Verified PDF locations: main physical pp. 26, 27, 29, 44; main_submit physical pp. 26, 27, 28, 43. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R1.4

Table 4 compares the mean over 51 separately funded symbol-block accounts: Full -0.797%, Base -0.750%, CASH zero and continuous price-only hold -2.128%. Always-LONG three-bar cycles (-3.000%) are reported separately from continuous hold, which retains exposure through calendar gaps. These are account means under explicit fill/cost assumptions, not a pooled executable portfolio or total-return index. Extension Native/Common/Bayesian-v1/MT-BICL mean account returns are -0.653%/-1.025%/-0.698%/-1.253%. All eight research-role means are negative; the U09 account estimand remains separate from the original study.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Separate-account means and continuous hold are conditional on assumed fills/costs; no executable portfolio or profitability.

Evidence: [outputs/revision/final_baselines_v1/baseline_contracts.json](../outputs/revision/final_baselines_v1/baseline_contracts.json); [outputs/revision/final_baselines_v1/financial.csv](../outputs/revision/final_baselines_v1/financial.csv); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/results.tex:6](../paper/content/results.tex) (`Table~\ref{tab:classification}`); [paper/content/tables/component/classification.tex:6](../paper/content/tables/component/classification.tex) (`\label{tab:classification}`); [paper/content/tables/component/accounts.tex:6](../paper/content/tables/component/accounts.tex) (`\label{tab:accounts}`).

Verified PDF locations: main physical pp. 26, 27, 29, 44; main_submit physical pp. 26, 27, 28, 43. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R1.5

Momentum-20, train-fitted logistic-price, logistic with matched numerical market inputs, and deterministic factor vote are retained alongside the constants and LLM branches. Logistic-price BA is 55.61%, above Full. Fits and preprocessing use purged chronological training data, with validation/test kept separate. Numerical inputs do not match chart/report representations or pretrained knowledge, so these comparisons do not identify a controlled information-only effect.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** Numerical comparators do not match chart/report representations or pretrained knowledge; exact-information effect is unidentified.

Evidence: [outputs/revision/final_baselines_v1/baseline_contracts.json](../outputs/revision/final_baselines_v1/baseline_contracts.json); [outputs/revision/final_baselines_v1/report.md](../outputs/revision/final_baselines_v1/report.md).

Source anchors: [paper/content/results.tex:6](../paper/content/results.tex) (`Table~\ref{tab:classification}`); [paper/content/tables/component/classification.tex:6](../paper/content/tables/component/classification.tex) (`\label{tab:classification}`); [paper/content/tables/component/accounts.tex:6](../paper/content/tables/component/accounts.tex) (`\label{tab:accounts}`).

Verified PDF locations: main physical pp. 26, 27, 29, 44; main_submit physical pp. 26, 27, 28, 43. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R1.6

Full makes 24/102 LONG decisions and Base 29/102, while both recover the same seven UP cases. Their BA difference therefore accompanies higher DOWN recall and is compatible with a shift toward CASH. We report scheduled LONG propensity and calendar held-session fractions separately; Full-Base is not exposure matched and cannot establish why the propensity changed. The extension comparison reports LONG rates, raw/bypass counts and CORE4/OOD5 support; fallback outcomes remain in primary metrics rather than being dropped.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** LONG propensity and held sessions are reported; no exposure-matched causal explanation of the difference.

Evidence: [outputs/revision/final_baselines_v1/classification.csv](../outputs/revision/final_baselines_v1/classification.csv); [outputs/revision/final_baselines_v1/financial.csv](../outputs/revision/final_baselines_v1/financial.csv); [outputs/revision/final_repeats_v1/contrasts.csv](../docs/plan/revision_evidence/README.md#final_repeats_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/results.tex:6](../paper/content/results.tex) (`Table~\ref{tab:classification}`); [paper/content/tables/component/classification.tex:6](../paper/content/tables/component/classification.tex) (`\label{tab:classification}`); [paper/content/tables/component/accounts.tex:6](../paper/content/tables/component/accounts.tex) (`\label{tab:accounts}`).

Verified PDF locations: main physical pp. 26, 27, 29, 44; main_submit physical pp. 26, 27, 28, 43. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R1.7

The original title is retained at the author's instruction. Abstract, highlights, contributions and conclusion now limit the claims to a specified integration and historical comparison. Full loses more than Base on the main account mean, underperforms CASH economically and logistic-price on BA; favorable small panels do not override these outcomes. No causal alpha, stable predictive superiority or profitable deployment is asserted. U09 Bayesian v1 minus Common is +0.327 pp with descriptive band [0.067,0.586], but minus Native is -0.045 pp [-0.362,0.271]. Improvement relative to Common therefore does not establish superiority over Native.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Negative outcomes and baseline-dependent interpretation remain explicit; original title is retained by author instruction.

Evidence: [outputs/revision/final_baselines_v1/financial.csv](../outputs/revision/final_baselines_v1/financial.csv); [outputs/revision/final_baselines_v1/report.md](../outputs/revision/final_baselines_v1/report.md); [docs/plan/week12/manuscript_final_checks.zip](../docs/plan/week12/manuscript_final_checks.zip); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/results.tex:6](../paper/content/results.tex) (`Table~\ref{tab:classification}`); [paper/content/tables/component/classification.tex:6](../paper/content/tables/component/classification.tex) (`\label{tab:classification}`); [paper/content/tables/component/accounts.tex:6](../paper/content/tables/component/accounts.tex) (`\label{tab:accounts}`).

Verified PDF locations: main physical pp. 2, 26, 27, 29, 34, 44; main_submit physical pp. 2, 26, 27, 28, 34, 43. Current section/table context; locators do not certify acceptance or unperformed evidence.

## R2 — Historical coverage and cross-sectional dependence

### R2.1

The final study contains real archived hosted decisions at twelve selected dates across six historical blocks rather than extending the sample with synthetic predictions. Nine securities contribute 102 eligible units, with 96 units on the common-eight universe and 54 on the recent-nine universe. The calendar and all outcomes are in S4. This is sparse historical coverage, not a continuous multi-year strategy or an untouched prospective evaluation.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** Twelve selected historical dates, no untouched prospective or dense continuous multi-year LLM validation.

Evidence: [outputs/revision/final_temporal_v1/calendar_panel.csv](../docs/plan/revision_evidence/README.md#final_temporal_v1); [outputs/revision/final_temporal_v1/report.md](../docs/plan/revision_evidence/README.md#final_temporal_v1).

Source anchors: [paper/content/experimental_setup.tex:11](../paper/content/experimental_setup.tex) (`Six blocks cover`); [paper/content/tables/component/temporal.tex:6](../paper/content/tables/component/temporal.tex) (`\label{tab:temporal}`).

Verified PDF locations: main physical pp. 20, 21, 31, 47, 48; main_submit physical pp. 20, 21, 31, 46, 47. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R2.2

We report all observed bull/bear/sideways, volatility and turnover-proxy strata with class support, defined counts, scores and exposure. Trend is each security's Close/SMA60 context; other thresholds use purged training medians. These post-inference descriptions are not validated index regimes, an ex ante regime-aware policy or evidence of robust performance across market conditions. An all-DOWN block has undefined within-block BA. The extension uses frozen VN-Index filtering and matured historical regime context; the original per-security descriptive strata are not relabelled as that regime model.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** Original security-level strata are post-inference descriptions; extension regime context is not validated cross-regime performance.

Evidence: [outputs/revision/final_temporal_v1/report.md](../docs/plan/revision_evidence/README.md#final_temporal_v1); [outputs/revision/final_temporal_v1/stratified_metrics.json](../docs/plan/revision_evidence/README.md#final_temporal_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/experimental_setup.tex:11](../paper/content/experimental_setup.tex) (`Six blocks cover`); [paper/content/tables/component/temporal.tex:6](../paper/content/tables/component/temporal.tex) (`\label{tab:temporal}`).

Verified PDF locations: main physical pp. 21, 31, 47, 48; main_submit physical pp. 21, 31, 46, 47. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R2.3

Whole-block resampling retains dates, the complete eligible cross-section, variants and paired outcomes together. The two fixed-universe cohorts also have six calendar-aligned Bartlett HAC accuracy rows at lags 0/1/2; these are accuracy differences, not BA estimates. Twelve or six selected dates and irregular gaps do not support calibrated significance, coverage or an independence claim. U09 uses a distinct joint paired circular-fold bootstrap: 10,000 draws, PCG64 seed 20261110, primary L2, simultaneous max-standardized bands across twenty endpoint/contrasts. Its L1/L3, CORE4 and leave-one-out views are descriptive on six exposed folds.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Joint resampling retains dependence; six exposed folds do not justify calibrated significance, coverage or power.

Evidence: [outputs/revision/final_temporal_v1/panel_hac.csv](../docs/plan/revision_evidence/README.md#final_temporal_v1); [outputs/revision/final_temporal_v1/report.md](../docs/plan/revision_evidence/README.md#final_temporal_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/experimental_setup.tex:11](../paper/content/experimental_setup.tex) (`Six blocks cover`); [paper/content/tables/component/temporal.tex:6](../paper/content/tables/component/temporal.tex) (`\label{tab:temporal}`).

Verified PDF locations: main physical pp. 21, 31, 47, 48; main_submit physical pp. 21, 31, 46, 47. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R2.4

The effective number of independent market replications is not 102, nor the count after multiplying by classifiers, repeats or bootstrap draws. The primary support has twelve dates/six blocks; overlapping cohorts and correlated securities share outcomes. Purposive/surviving-universe selection, unverified listing/suspension membership and possible training contamination remain explicit limitations.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Correlated securities/repeats/overlapping cohorts are not independent market replications.

Evidence: [outputs/revision/final_temporal_v1/calendar_panel.csv](../docs/plan/revision_evidence/README.md#final_temporal_v1); [outputs/revision/final_temporal_v1/folds.csv](../docs/plan/revision_evidence/README.md#final_temporal_v1); [outputs/revision/final_temporal_v1/report.md](../docs/plan/revision_evidence/README.md#final_temporal_v1).

Source anchors: [paper/content/experimental_setup.tex:11](../paper/content/experimental_setup.tex) (`Six blocks cover`); [paper/content/tables/component/temporal.tex:6](../paper/content/tables/component/temporal.tex) (`\label{tab:temporal}`).

Verified PDF locations: main physical pp. 20, 21, 22, 31, 47, 48; main_submit physical pp. 20, 21, 22, 31, 46, 47. Current section/table context; locators do not certify acceptance or unperformed evidence.

## R3 — Repeated executions and variability

### R3.1

The legacy default labels and matching prediction sequences cannot authenticate equal actual prompts, served weights, executed code or independent runs. We retain those artifacts for lineage audit and no longer interpret their table-to-table differences as treatment effects or stable defaults. The final response uses the completed corrected-chart release, not the superseded 474/270-job grids or earlier 18-unit repeat panel. The completed U08/U09 collection is another study with its own source/request identities and ledger; it does not authenticate legacy branch execution.

**Disposition:** `unresolved_historical_identity`; comment closure not certified. **Remaining:** Legacy default labels do not authenticate original requests, code or served weights; their differences are not treatment effects.

Evidence: [outputs/revision/final_repeats_v1/disagreement.csv](../docs/plan/revision_evidence/README.md#final_repeats_v1); [outputs/revision/final_repeats_v1/report.md](../docs/plan/revision_evidence/README.md#final_repeats_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/results.tex:45](../paper/content/results.tex) (`Table~\ref{tab:repeats}`); [paper/content/tables/component/variability.tex:6](../paper/content/tables/component/variability.tex) (`\label{tab:repeats}`).

Verified PDF locations: main physical pp. 21, 30, 45; main_submit physical pp. 21, 30, 44. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R3.2

We report two separate nine-unit panels, each with two UP/seven DOWN and three real executions. One regenerates upstream inputs for B/AS; the other fixes upstream reports and repeats Decision over B/A/S/AS/P. They have different dates/symbols and prompt representations. We did not repeat every main-grid configuration or cross upstream and Decision in a full factorial variance design; that part of the request remains unfulfilled. U09 now supplies three Decision repeats on all 102 extension points while keeping one upstream realization fixed. This fills the extension Decision-repeat coverage gap but not a crossed upstream-by-Decision study.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** U09 adds three full-support Decision repeats but only one upstream realization; no crossed upstream-by-Decision variance study.

Evidence: [outputs/revision/final_repeats_v1/pairing.csv](../docs/plan/revision_evidence/README.md#final_repeats_v1); [outputs/revision/final_repeats_v1/repeat_summary.csv](../docs/plan/revision_evidence/README.md#final_repeats_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/results.tex:45](../paper/content/results.tex) (`Table~\ref{tab:repeats}`); [paper/content/tables/component/variability.tex:6](../paper/content/tables/component/variability.tex) (`\label{tab:repeats}`).

Verified PDF locations: main physical pp. 21, 30, 45; main_submit physical pp. 21, 30, 44. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R3.3

Table 6 and S2 retain all 21 variant-execution metric rows, all 48 contrast-metric rows, sample SD (ddof=1), median/range and 63 cutoff-level disagreement rows. Aggregate score equality is not equated with identical predictions. Return summaries use nine upstream or eight factorial accounts per variant/execution, not the main 51-account support; favourable executions are not selected. Table F.5 and the extension companions retain every repeat on 51 accounts; repeating hosted decisions does not add independent dates.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** All recorded executions/disagreements are retained; small-panel variation is not transferred to the main market support.

Evidence: [outputs/revision/final_repeats_v1/contrasts.csv](../docs/plan/revision_evidence/README.md#final_repeats_v1); [outputs/revision/final_repeats_v1/disagreement.csv](../docs/plan/revision_evidence/README.md#final_repeats_v1); [outputs/revision/final_repeats_v1/repeat_summary.csv](../docs/plan/revision_evidence/README.md#final_repeats_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/results.tex:45](../paper/content/results.tex) (`Table~\ref{tab:repeats}`); [paper/content/tables/component/variability.tex:6](../paper/content/tables/component/variability.tex) (`\label{tab:repeats}`).

Verified PDF locations: main physical pp. 21, 30, 45; main_submit physical pp. 21, 30, 44. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R3.4

Repeated-panel contrasts use joint block/paired-execution resampling, with undefined draws retained in the denominator report. Only 6,986/10,000 BA draws are defined; 3,014 lack class support. Three executions do not certify stable variance or calibrated inference. Across the complete pairing audit, 40/147 groups differ from listed successful-call order and nine cross epochs; quota/routing/resume did not implement complete counterbalancing, and immutable served weights remain unknown. U09 keeps retry/reset/retired lineage and dependency order. Its three repeats remain conditional on one upstream realization rather than an independent market replication.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** Order/epoch confounding, three executions and unknown hosted weight revisions prevent a calibrated stability claim.

Evidence: [outputs/revision/final_repeats_v1/contrasts.csv](../docs/plan/revision_evidence/README.md#final_repeats_v1); [outputs/revision/final_repeats_v1/report.md](../docs/plan/revision_evidence/README.md#final_repeats_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/results.tex:45](../paper/content/results.tex) (`Table~\ref{tab:repeats}`); [paper/content/tables/component/variability.tex:6](../paper/content/tables/component/variability.tex) (`\label{tab:repeats}`).

Verified PDF locations: main physical pp. 21, 30, 45; main_submit physical pp. 21, 30, 44. Current section/table context; locators do not certify acceptance or unperformed evidence.

## R4 — Bundle ablation, factorial contrasts and placebo

### R4.1

We agree that Base removes both alpha and sentiment, not alpha alone. The manuscript now defines Full as AS and Base as B and describes Full-Base as a bundle difference including report/prompt content and possible CASH propensity. The general instructions can still mention concepts whose sections have been removed; the actual prompts, not branch names alone, define delivered content. Extension Common retains alpha and sentiment under a causal-alpha/common-instruction profile. It is not the original Base or a pure alpha-off intervention.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Original Base removes alpha and sentiment; extension Common is a different alpha/prompt baseline.

Evidence: [outputs/revision/final_baselines_v1/baseline_contracts.json](../outputs/revision/final_baselines_v1/baseline_contracts.json); [outputs/revision/fusion_prompt_audit_v1/audit.json](../docs/plan/revision_evidence/README.md#fusion_prompt_audit_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/experimental_setup.tex:43](../paper/content/experimental_setup.tex) (`P retains`); [paper/content/tables/component/scope.tex:6](../paper/content/tables/component/scope.tex) (`\label{tab:scope}`); [paper/content/tables/component/variability.tex:6](../paper/content/tables/component/variability.tex) (`\label{tab:repeats}`).

Verified PDF locations: main physical pp. 18, 21, 30, 46, 47; main_submit physical pp. 18, 20, 30, 45, 46. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R4.2

The explicit factorial panel includes B, A, S, AS and P on the same nine units and three paired Decision executions. Frozen reports, five numeric factor rows, signals, skills and parent identities are checked against actual requests. This representation differs from compact main/upstream prompts, so the factorial is not pooled into the 102-unit main comparison or treated as its identical mechanism. U09 deep-copies one shared I/P/T parent, binds native/common projections and resolves dependencies within each repeat. These are distinct interfaces and responses from the original factorial panel.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Original factorial and main prompts differ in representation/support; U09 is another response collection.

Evidence: [outputs/revision/final_repeats_v1/contrasts.csv](../docs/plan/revision_evidence/README.md#final_repeats_v1); [outputs/revision/final_repeats_v1/pairing.csv](../docs/plan/revision_evidence/README.md#final_repeats_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/experimental_setup.tex:43](../paper/content/experimental_setup.tex) (`P retains`); [paper/content/tables/component/scope.tex:6](../paper/content/tables/component/scope.tex) (`\label{tab:scope}`); [paper/content/tables/component/variability.tex:6](../paper/content/tables/component/variability.tex) (`\label{tab:repeats}`).

Verified PDF locations: main physical pp. 18, 21, 30, 46, 47; main_submit physical pp. 18, 20, 30, 45, 46. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R4.3

P preserves current names, headings, schema/missingness and sentiment while replacing scalar/signal/skill fields with one predetermined earlier train-only rank-vector donor; donor label exits precede validation/test. This supplies a reproducible structured replacement control, but not name-matched covariance, exposure matching or a distribution of placebo interventions. We report that limitation rather than describing it as a perfect information-only placebo.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** Rank-vector replacement is not name-matched covariance, exposure matching or a distribution of placebo interventions.

Evidence: [outputs/revision/final_repeats_v1/donors.csv](../docs/plan/revision_evidence/README.md#final_repeats_v1); [outputs/revision/final_repeats_v1/report.md](../docs/plan/revision_evidence/README.md#final_repeats_v1).

Source anchors: [paper/content/experimental_setup.tex:43](../paper/content/experimental_setup.tex) (`P retains`); [paper/content/tables/component/scope.tex:6](../paper/content/tables/component/scope.tex) (`\label{tab:scope}`); [paper/content/tables/component/variability.tex:6](../paper/content/tables/component/variability.tex) (`\label{tab:repeats}`).

Verified PDF locations: main physical pp. 18, 21, 30, 46, 47; main_submit physical pp. 18, 20, 30, 45, 46. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R4.4

Actual-content integrity establishes delivery, not that the LLM used a factor semantically or that sentiment/alpha caused the decision. In the factorial panel mean AS-B BA is -9.52 pp and AS-P -11.90 pp; all seven descriptive BA family envelopes include zero, and all factorial account means are negative. We withdrew independent-alpha, sentiment-information and semantic-reasoning benefit claims. C2 and B_semantic each have only 3 raw Decisions and 303 bypasses per 306 slots. MT agrees with Fact_Anchor on 302/306 final actions. These outcomes cannot identify pure retriever/student value without support and policy.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** Content delivery and near-equal fallback actions do not establish semantic information use or component causality.

Evidence: [outputs/revision/final_repeats_v1/contrasts.csv](../docs/plan/revision_evidence/README.md#final_repeats_v1); [outputs/revision/fusion_prompt_audit_v1/audit.json](../docs/plan/revision_evidence/README.md#fusion_prompt_audit_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/experimental_setup.tex:43](../paper/content/experimental_setup.tex) (`P retains`); [paper/content/tables/component/scope.tex:6](../paper/content/tables/component/scope.tex) (`\label{tab:scope}`); [paper/content/tables/component/variability.tex:6](../paper/content/tables/component/variability.tex) (`\label{tab:repeats}`).

Verified PDF locations: main physical pp. 18, 21, 30, 46, 47; main_submit physical pp. 18, 20, 30, 45, 46. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R4.5

We distinguish interaction AS-A-S+B (mean +14.29 pp) from the post-hoc gap between AS mean BA and the observed best single component (zero here). A positive interaction in this small dependent panel is not validated synergy; every family envelope spans zero. The upstream AS-B mean of +4.76 pp on different support is retained separately and cannot replace the negative factorial or bounded main result. The native-to-common, common-to-anchor and anchor-to-MT bridges are descriptive dependency steps. U09 did not execute retrieval-only, statistics-only, no-prior, no-target or no-utility ablations.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Interaction and post-hoc best-single gap are distinct; descriptive family envelopes do not establish synergy.

Evidence: [outputs/revision/final_repeats_v1/contrasts.csv](../docs/plan/revision_evidence/README.md#final_repeats_v1); [outputs/revision/final_repeats_v1/report.md](../docs/plan/revision_evidence/README.md#final_repeats_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/experimental_setup.tex:43](../paper/content/experimental_setup.tex) (`P retains`); [paper/content/tables/component/scope.tex:6](../paper/content/tables/component/scope.tex) (`\label{tab:scope}`); [paper/content/tables/component/variability.tex:6](../paper/content/tables/component/variability.tex) (`\label{tab:repeats}`).

Verified PDF locations: main physical pp. 18, 21, 30, 46, 47; main_submit physical pp. 18, 20, 30, 45, 46. Current section/table context; locators do not certify acceptance or unperformed evidence.

## R5 — Uncertainty, HAC and risk conventions

### R5.1

Primary main BA inference is a descriptive 10,000-draw paired whole-block interval: Full-Base +3.25 pp, interval [-1.18,8.13] pp. Exact discordance is a separate accuracy diagnostic (9 Full-only versus 4 Base-only correct; nominal p=0.266846), whose independence assumption is not certified. Neither procedure is presented as proof of significance or a zero effect; block/null diagnostics show that nominal coverage is not calibrated. U09 uses its separately frozen simultaneous return/BA contrast family; no seed, band or original-study inference is recomputed for this manuscript release.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Bootstrap and accuracy discordance answer different questions; neither certifies independent observations or a significant/no effect.

Evidence: [outputs/revision/final_temporal_v1/panel_hac.csv](../docs/plan/revision_evidence/README.md#final_temporal_v1); [outputs/revision/final_temporal_v1/report.md](../docs/plan/revision_evidence/README.md#final_temporal_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/experimental_setup.tex:49](../paper/content/experimental_setup.tex) (`BA averages`); [paper/content/tables/component/temporal.tex:6](../paper/content/tables/component/temporal.tex) (`\label{tab:temporal}`).

Verified PDF locations: main physical pp. 31, 44, 46; main_submit physical pp. 31, 43, 45. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R5.2

S4 includes all six actual HAC rows. Common-eight mean accuracy difference is +3.125 pp, with lag-0/1/2 SEs 0.026042/0.023146/0.020172 and p=0.255346/0.204107/0.149610. Recent-nine is +9.259 pp, SEs 0.040713/0.047112/0.045710 and p=0.072051/0.106554/0.098654. Lags count selected dates, not consecutive sessions; Bartlett estimates with a t(dates-1) reference remain small-sample sensitivity diagnostics.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** HAC uses selected dates and accuracy effects; small-cluster inference remains sensitivity only.

Evidence: [outputs/revision/final_temporal_v1/panel_hac.csv](../docs/plan/revision_evidence/README.md#final_temporal_v1); [outputs/revision/final_temporal_v1/report.md](../docs/plan/revision_evidence/README.md#final_temporal_v1).

Source anchors: [paper/content/results.tex:61](../paper/content/results.tex) (`Calendar-aligned HAC accuracy effects`).

Verified PDF locations: main physical pp. 31, 44, 46; main_submit physical pp. 31, 43, 45. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R5.3

We separate pooled confusion-cell metrics from unweighted means over symbols and from 51-account economic means. Every export retains planned/defined counts and class support; undefined BA/MCC/risk ratios remain NA/null. BHN has six eligible units rather than twelve, and overlapping 102/96/54 cohorts are not added. A table Mean is never represented as an extra pooled independent observation. U09 averages three repeats within account and then 51 accounts equally; BA is the mean of per-repeat pooled BA, not pooled independent outcomes over 306 market points. Missing classes and risk denominators retain null/NA reasons.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Pooled classification, symbol macro and equal mean account returns remain separate estimands with explicit null reasons.

Evidence: [outputs/revision/final_baselines_v1/report.md](../outputs/revision/final_baselines_v1/report.md); [outputs/revision/final_temporal_v1/calendar_panel.csv](../docs/plan/revision_evidence/README.md#final_temporal_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/experimental_setup.tex:49](../paper/content/experimental_setup.tex) (`BA averages`); [paper/content/tables/component/temporal.tex:6](../paper/content/tables/component/temporal.tex) (`\label{tab:temporal}`).

Verified PDF locations: main physical pp. 31, 44, 46; main_submit physical pp. 31, 43, 45. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R5.4

We removed annualized cycle Sharpe/Sortino claims for irregular, gapped schedules. Where daily-ledger ratios are supplied, Sharpe uses population daily SD, a 252-session convention and zero risk-free rate; retained Sortino uses SD of negative daily observations rather than downside RMS. Daily-close drawdown includes an initial-capital anchor. These explicit conventions do not make sparse risk estimates reliable investment-quality evidence. U09 cycle Sharpe uses sample SD (ddof=1), and cycle Sortino uses RMS negative-part returns over all cycles with MAR zero. These differ from original daily conventions; annualized U09 ratios remain NA.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Original daily and U09 cycle risk conventions differ; annualized ratios remain NA for the irregular schedule.

Evidence: [outputs/revision/final_contracts_v1/report.md](../docs/plan/revision_evidence/README.md#final_contracts_v1); [outputs/revision/final_contracts_v1/risk_cycles.csv](../docs/plan/revision_evidence/README.md#final_contracts_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/experimental_setup.tex:61](../paper/content/experimental_setup.tex) (`Annualised cycle ratios are NA`).

Verified PDF locations: main physical pp. 31, 44, 46; main_submit physical pp. 31, 43, 45. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R5.5

We disclose few trades, long CASH gaps and separate account funding. Main cutoffs within blocks are 57 observed sessions apart, so comparable pending-cash/advance results are weak evidence about rapid capital reuse. Negative account means and poorly identified risk ratios cannot demonstrate deployable profitability; raw account/ledger rows and twelve sensitivities remain available privately.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Few trades and CASH gaps preclude reliable investment-quality risk estimates or rapid capital-reuse validation.

Evidence: [outputs/revision/final_baselines_v1/financial.csv](../outputs/revision/final_baselines_v1/financial.csv); [outputs/revision/final_contracts_v1/risk_cycles.csv](../docs/plan/revision_evidence/README.md#final_contracts_v1).

Source anchors: [paper/content/experimental_setup.tex:49](../paper/content/experimental_setup.tex) (`BA averages`); [paper/content/tables/component/temporal.tex:6](../paper/content/tables/component/temporal.tex) (`\label{tab:temporal}`).

Verified PDF locations: main physical pp. 31, 44, 46; main_submit physical pp. 31, 43, 45. Current section/table context; locators do not certify acceptance or unperformed evidence.

## R6 — Legacy lineage and duplicated results

### R6.1

The legacy audit compares 47 artifacts, 66 streams and 573 pairs; twenty pairs have complete duplicated sequences, including eight execution-unverified cases and twelve intended-shared-control cases with unverified parents. Byte/prediction matching and early Git matches are traceability evidence only. No authenticated original request set establishes the executed root cause, which remains unknown.

**Disposition:** `unresolved_historical_identity`; comment closure not certified. **Remaining:** The executed root cause of duplicated legacy streams is unverified; no authenticated original request set.

Evidence: [outputs/revision/legacy_lineage_v1/comparisons.json](../docs/plan/revision_evidence/README.md#legacy_lineage_v1); [outputs/revision/legacy_lineage_v1/report.json](../docs/plan/revision_evidence/README.md#legacy_lineage_v1).

Source anchors: [paper/content/limitations.tex:6](../paper/content/limitations.tex) (`Byte-level duplication`).

Verified PDF locations: main physical pp. 32; main_submit physical pp. 32. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R6.2

We cannot retrospectively certify the old Full/No-Alpha/ablation branch labels or independent execution. We have not relabelled, edited or regenerated old outcomes to match a narrative. Those legacy tables no longer support causal component attribution or robustness claims. Final comparisons instead have distinct stored request/response identities and checked parents, while retaining their own order/epoch limitations. The extension raw/prepared/policy/outcome records preserve their own UUIDs, hashes, bypass sources and reset history. That traceability does not resolve the old duplication root cause.

**Disposition:** `unresolved_historical_identity`; comment closure not certified. **Remaining:** Old branch names and independent execution cannot be certified retrospectively.

Evidence: [outputs/revision/legacy_lineage_v1/comparisons.json](../docs/plan/revision_evidence/README.md#legacy_lineage_v1); [outputs/revision/legacy_lineage_v1/report.json](../docs/plan/revision_evidence/README.md#legacy_lineage_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/limitations.tex:6](../paper/content/limitations.tex) (`Byte-level duplication`).

Verified PDF locations: main physical pp. 32; main_submit physical pp. 32. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R6.3

Repeated legacy return values such as -7.85/-7.38 are not treated as proof of matched controls, independent repeats or a specific caching bug. The audit records exact duplicated streams without inferring an unobserved execution. New paired/factorial results use their own frozen support and requests; neither their completion nor unit tests authenticate the historical duplicates.

**Disposition:** `unresolved_historical_identity`; comment closure not certified. **Remaining:** Duplicate returns do not identify a caching bug; new results cannot authenticate the old duplication.

Evidence: [outputs/revision/final_repeats_v1/pairing.csv](../docs/plan/revision_evidence/README.md#final_repeats_v1); [outputs/revision/legacy_lineage_v1/comparisons.json](../docs/plan/revision_evidence/README.md#legacy_lineage_v1).

Source anchors: [paper/content/limitations.tex:6](../paper/content/limitations.tex) (`Byte-level duplication`).

Verified PDF locations: main physical pp. 32; main_submit physical pp. 32. Current section/table context; locators do not certify acceptance or unperformed evidence.

## R7 — Sentiment counts, provenance and domain validation

### R7.1

We withdraw the claim of 8,180 authenticated news articles. The retained legacy files contain 180 article records but 177 unique identities, with three excess duplicate identities; these are article records, not 180 independent prediction cutoffs or validated sentiment labels. All 180 historical scorer identities are unknown. The separate 102-unit evaluation and 154 rescored excerpts have distinct provenance scopes.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Legacy records and identities are counted separately; no claim of 8,180 authenticated articles.

Evidence: [outputs/revision/sentiment_inventory_v1/inventory.json](../docs/plan/revision_evidence/README.md#sentiment_inventory_v1); [outputs/revision/sentiment_inventory_v1/summary.json](../docs/plan/revision_evidence/README.md#sentiment_inventory_v1).

Source anchors: [paper/content/problem_formulation.tex:308](../paper/content/problem_formulation.tex) (`Legacy inventory`).

Verified PDF locations: main physical pp. 21, 47; main_submit physical pp. 21, 46. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R7.2

The inventory provides article identities/counts by symbol; the cutoff coverage export separately records eligible, missing and available-neutral states and unique article memberships. Under corrected strict scorer-provenance/availability rules none of the 180 legacy cutoffs has an accepted three-article set. This is a rule/provenance outcome, not evidence that no historical news existed; main frozen-report delivery is audited separately. U09 reports unavailable sentiment at 79/102 points. Availability counts are separate from the number of legacy articles or rescored excerpts.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** Cutoff/source coverage is available, but financial-domain truth and publication authentication remain missing.

Evidence: [outputs/revision/sentiment_coverage_v1/coverage.json](../docs/plan/revision_evidence/README.md#sentiment_coverage_v1); [outputs/revision/sentiment_inventory_v1/inventory.json](../docs/plan/revision_evidence/README.md#sentiment_inventory_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/problem_formulation.tex:308](../paper/content/problem_formulation.tex) (`Legacy inventory`).

Verified PDF locations: main physical pp. 21, 47; main_submit physical pp. 21, 46. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R7.3

We separate raw records, unique identities, dated records, accepted provenance and cutoff memberships instead of reusing one percentage for incompatible denominators. Of 180 legacy date records, 155 agree with the frozen date audit and 25 do not; date parsing alone does not verify original publication. Unknown legacy scorer provenance is not reclassified as ViSoBERT or lexicon output. Repaired scoring does not overwrite the historical cache.

**Disposition:** `unresolved_historical_identity`; comment closure not certified. **Remaining:** Legacy scorer provenance and conflicting date records remain unknown; new rescores do not repair the historical cache.

Evidence: [outputs/revision/sentiment_coverage_v1/summary.json](../docs/plan/revision_evidence/README.md#sentiment_coverage_v1); [outputs/revision/sentiment_inventory_v1/summary.json](../docs/plan/revision_evidence/README.md#sentiment_inventory_v1).

Source anchors: [paper/content/problem_formulation.tex:308](../paper/content/problem_formulation.tex) (`Legacy inventory`).

Verified PDF locations: main physical pp. 21, 47; main_submit physical pp. 21, 46. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R7.4

Availability requires at least three distinct accepted-provenance finite-score articles in a 90-day window; missing is not an observed neutral value. The frozen weighted score has a 30-day half-life. The normalizer receives empty article-detail/peer lists on this path, so its z-score/relative fields are zero; its >=8 reliability flag differs from >=3 report availability. We do not equate a false reliability flag with an unavailable weighted report. The extension keeps 79/102 unavailable points explicit and carries the shared sentiment report through common projection without treating missing input as neutral evidence.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Availability, reliability and unavailable sentiment are distinct; 79/102 missing extension points are not neutral observations.

Evidence: [outputs/revision/sentiment_coverage_v1/coverage.json](../docs/plan/revision_evidence/README.md#sentiment_coverage_v1); [outputs/revision/sentiment_coverage_v1/summary.json](../docs/plan/revision_evidence/README.md#sentiment_coverage_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/problem_formulation.tex:308](../paper/content/problem_formulation.tex) (`Legacy inventory`).

Verified PDF locations: main physical pp. 21, 47; main_submit physical pp. 21, 46. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R7.5

The legacy FPT Sentiment-only result cannot authenticate a sentiment-information benefit: counts are sparse, strict provenance/availability is unresolved and branch execution is unverified. It is removed as evidence of component value. The actual S/AS factorial report presence and outcomes are described separately; delivering a sentiment section does not establish that its content is correct or causal.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** The legacy FPT sentiment-only result cannot support component value; the newer factorial is a different experiment.

Evidence: [outputs/revision/legacy_lineage_v1/report.json](../docs/plan/revision_evidence/README.md#legacy_lineage_v1); [outputs/revision/sentiment_coverage_v1/coverage.json](../docs/plan/revision_evidence/README.md#sentiment_coverage_v1).

Source anchors: [paper/content/problem_formulation.tex:308](../paper/content/problem_formulation.tex) (`Legacy inventory`).

Verified PDF locations: main physical pp. 21, 47; main_submit physical pp. 21, 46. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R7.6

The text cites the ViSoBERT backbone and separately identifies 5CD-AI/Vietnamese-Sentiment-visobert at revision d7738b85200272f10ba8b048d80236c8c582b581. It reports NEG/POS/NEU, P(POS)-P(NEG), a 256-token limit and the saved scoring recipe. The XLM-R-derived social-media backbone is not conflated with the downstream classifier or a model trained/validated on Vietnamese financial news.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Backbone and downstream classifier are identified separately; neither establishes financial-news accuracy.

Evidence: [outputs/revision/reference_audit_v1/reference_audit.json](../docs/plan/revision_evidence/README.md#reference_audit_v1); [outputs/revision/sentiment_contract_v1/scorer_tokenizer.json](../docs/plan/revision_evidence/README.md#sentiment_contract_v1).

Source anchors: [paper/content/problem_formulation.tex:308](../paper/content/problem_formulation.tex) (`Legacy inventory`).

Verified PDF locations: main physical pp. 21, 47; main_submit physical pp. 21, 46. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R7.7

No independently labelled financial-news set, agreement/adjudication study or domain test performance is available. We therefore withdraw financial-domain accuracy/reliability claims and explicitly disclose social-media domain mismatch. Offline probability/tokenizer checks on 154 saved rescores are implementation checks, not domain validation. This requested validation remains unfulfilled; it has not been replaced by labels invented by an LLM.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** No independent financial-news labels, adjudication/agreement or domain validation study.

Evidence: [outputs/revision/sentiment_contract_v1/scorer_tokenizer.json](../docs/plan/revision_evidence/README.md#sentiment_contract_v1); [outputs/revision/sentiment_contract_v1/summary.json](../docs/plan/revision_evidence/README.md#sentiment_contract_v1).

Source anchors: [paper/content/problem_formulation.tex:308](../paper/content/problem_formulation.tex) (`Legacy inventory`).

Verified PDF locations: main physical pp. 21, 47; main_submit physical pp. 21, 46. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R7.8

Date-only content is made available the following day by an explicit conservative rule, but neither that rule nor URL/content hashes authenticate original content or publication availability. The corpus is not claimed to be PIT certified. Independent news provenance/domain validation remains missing, so sentiment delivery, coverage and Full-Base differences cannot certify historical information effects.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** Date-only rules and content hashes do not authenticate original news availability or content.

Evidence: [outputs/revision/sentiment_coverage_v1/summary.json](../docs/plan/revision_evidence/README.md#sentiment_coverage_v1); [outputs/revision/sentiment_inventory_v1/summary.json](../docs/plan/revision_evidence/README.md#sentiment_inventory_v1).

Source anchors: [paper/content/problem_formulation.tex:308](../paper/content/problem_formulation.tex) (`Legacy inventory`).

Verified PDF locations: main physical pp. 21, 47; main_submit physical pp. 21, 46. Current section/table context; locators do not certify acceptance or unperformed evidence.

## R8 — Attribution and the meaning of aggregation

### R8.1

The architecture and related work now attribute Indicator, Pattern, Trend and Decision roles, shared state, chart tools and trendline procedures to reused/modified QuantAgent components. The repository attribution inventory distinguishes reuse, modifications and additions. The figure follows implemented roles; it does not add a learned fusion module to make a novelty claim.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Reused QuantAgent roles/tools are attributed; engineering integration is not proof of architectural novelty.

Evidence: [outputs/revision/quantagent_attribution_v1/attribution.json](../docs/plan/revision_evidence/README.md#quantagent_attribution_v1); [outputs/revision/quantagent_attribution_v1/provenance.json](../docs/plan/revision_evidence/README.md#quantagent_attribution_v1).

Source anchors: [paper/content/related_work.tex:5](../paper/content/related_work.tex) (`QuantAgent`); [paper/content/system_architecture.tex:4](../paper/content/system_architecture.tex) (`QuantAgent`).

Verified PDF locations: main physical pp. 14, 18; main_submit physical pp. 14, 18. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R8.2

We restrict contributions to daily Vietnamese-equity adaptation, the implemented factor/sentiment path, protocol and auditable historical comparisons. Neither an added component nor a registered factor catalogue by itself establishes scientific novelty, improved reasoning or profitable trading. Native causal defects, domain uncertainty and negative/bounded comparisons qualify the contribution explicitly. Five regime/prior/task-conditioned extensions, dependency controls and the full negative U09 comparison are now explained in the existing article; registration is not evidence of isolated causal value.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** Integration and comparative evaluation are documented; novel reasoning, causal component benefit and profitability are not established.

Evidence: [outputs/revision/fusion_prompt_audit_v1/audit.json](../docs/plan/revision_evidence/README.md#fusion_prompt_audit_v1); [outputs/revision/quantagent_attribution_v1/attribution.json](../docs/plan/revision_evidence/README.md#quantagent_attribution_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/related_work.tex:5](../paper/content/related_work.tex) (`QuantAgent`); [paper/content/system_architecture.tex:4](../paper/content/system_architecture.tex) (`QuantAgent`).

Verified PDF locations: main physical pp. 14, 18; main_submit physical pp. 14, 18. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R8.3

The repository includes LICENSES/QuantAgent-MIT.txt and THIRD_PARTY_NOTICES.md with upstream attribution and the scoped MIT notice. This does not license all author additions, data, news, models or hosted outputs for public redistribution. The archive rights register keeps those permissions pending rather than applying the upstream MIT licence to the whole package.

**Disposition:** `pending_rights_or_author_route`; comment closure not certified. **Remaining:** Upstream MIT notice does not grant rights to all author additions, data, model assets or hosted outputs.

Evidence: [LICENSES/QuantAgent-MIT.txt](../LICENSES/QuantAgent-MIT.txt); [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md); [outputs/revision/quantagent_attribution_v1/attribution.json](../docs/plan/revision_evidence/README.md#quantagent_attribution_v1).

Source anchors: [paper/content/availability.tex:2](../paper/content/availability.tex) (`Distribution remains subject to source terms`).

Verified PDF locations: main physical pp. 14, 18; main_submit physical pp. 14, 18. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R8.4

We acknowledge inherited high-frequency/K-line wording in actual frozen prompts despite using daily bars. The manuscript states this mismatch and retains exact original prompts in the private evidence package rather than silently editing them and attributing the old predictions to a new prompt. Application frequency is not represented as identical to the upstream HFT setting.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Inherited HFT/K-line wording in archived daily-bar prompts is disclosed and not retrospectively rewritten.

Evidence: [outputs/revision/fusion_prompt_audit_v1/audit.json](../docs/plan/revision_evidence/README.md#fusion_prompt_audit_v1); [outputs/revision/quantagent_attribution_v1/prompt_inventory.json](../docs/plan/revision_evidence/README.md#quantagent_attribution_v1).

Source anchors: [paper/content/related_work.tex:5](../paper/content/related_work.tex) (`QuantAgent`); [paper/content/system_architecture.tex:4](../paper/content/system_architecture.tex) (`QuantAgent`).

Verified PDF locations: main physical pp. 14, 18; main_submit physical pp. 14, 18. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R8.5

We replaced the stronger knowledge-fusion framing with prompt-level report aggregation. Distilled/capped reports and heuristic precedence instructions prefer price/chart evidence, allow factors to challenge it and give sentiment lower priority. There is no separately validated explicit knowledge representation, learned/calibrated evidence weighting or guaranteed conflict-resolution algorithm. The observed Decision prompt maximum is 4,187 characters under the 6,500 guard. The 4,187-character maximum applies to the original study only. Extension prompts keep the <6,500-character total guard and <=600-character prior/context prefix. Fact assertions and teacher-utility Q10 revision veto are external policies; raw proposals and final actions are saved separately.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Prompt precedence, model confidence and external utility policy are not calibrated learned fusion or guaranteed conflict resolution.

Evidence: [outputs/revision/fusion_prompt_audit_v1/audit.json](../docs/plan/revision_evidence/README.md#fusion_prompt_audit_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/related_work.tex:5](../paper/content/related_work.tex) (`QuantAgent`); [paper/content/system_architecture.tex:4](../paper/content/system_architecture.tex) (`QuantAgent`).

Verified PDF locations: main physical pp. 14, 18; main_submit physical pp. 14, 18. Current section/table context; locators do not certify acceptance or unperformed evidence.

## R9 — Reproducibility, model provenance and public archive

### R9.1

A byte-indexed private package retains reconstructed OHLCV/news inputs, saved sentiment artifacts and model/tokenizer metadata; the T34 package adds final analyses, source snapshots and S1-S4. These are reconstructed research inputs, not an authenticated submission-time snapshot. Publication/content provenance remains bounded, and missing rights prevent claiming that the exact private package is publicly available. F01 preserves a source snapshot and historical restoration path; U08/U09 packages keep their own pins. The F05 manuscript release binds both studies and packages separate scientific companions without merging response samples.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** Research inputs are reconstructed; exact submission-time provenance and redistribution permissions are not authenticated.

Evidence: [outputs/revision/reproducibility_v1/manifest.json](../docs/plan/revision_evidence/README.md#reproducibility_v1); [outputs/revision/sentiment_inventory_v1/summary.json](../docs/plan/revision_evidence/README.md#sentiment_inventory_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/availability.tex:2](../paper/content/availability.tex) (`OHLCV/news snapshots are reconstructed`).

Verified PDF locations: main physical pp. 40; main_submit physical pp. 40. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R9.2

Pinned runtime/dependency manifests replace latest-based reproducibility claims. The T23 replay used Python 3.13.5 and NumPy 2.1.2 from a hashed runtime image in a fresh isolated venv without pip/network/user-site access. Installed interpreter/stdlib are shared, and the Windows pins/runtime clone are not original wheels or a portability proof for other OS/CUDA environments. U08/U09 lock Python 3.13.5, 107 package versions and frozen selector/HMM/scaler/teacher/student resources. Historical replay uses the declared source checkout and exact-byte overlays rather than changed serving code.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Pinned environments/replay evidence apply to their named releases, not arbitrary current serving code or all platforms.

Evidence: [outputs/revision/final_regression_v1/report.json](../docs/plan/revision_evidence/README.md#final_regression_v1); [outputs/revision/reproducibility_v1/manifest.json](../docs/plan/revision_evidence/README.md#reproducibility_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/appendices.tex:95](../paper/content/appendices.tex) (`The research runtime is Python 3.13.5`).

Verified PDF locations: main physical pp. 40; main_submit physical pp. 40. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R9.3

The private evidence preserves prompts/images, upstream reports, requests, responses/errors, parse/checkpoints and call identities. Final closure accounting has 649 attempts, 615 successes, 34 errors, 1,063,328 observed prompt tokens and 340,736 completion tokens. The 120 original Pattern calls are replayed shared dependencies, not 120 new calls; successful latency sums are not wall-clock time, and error usage/latency and monetary billing remain unknown. U08 separately retains 1,702 HTTP attempts including 15 retired records and 1,290 active raw Decision responses. Its 2,448 forecast slots are not successful calls or full-system runs and are not added to the original 649-attempt ledger.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Original and U08 attempt/token ledgers stay separate; unrecorded billing/error usage is not fabricated.

Evidence: [outputs/revision/final_cost_integrity_v1/report.json](../docs/plan/revision_evidence/README.md#final_cost_integrity_v1); [outputs/revision/reproducibility_v1/manifest.json](../docs/plan/revision_evidence/README.md#reproducibility_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/experimental_setup.tex:71](../paper/content/experimental_setup.tex) (`Archived SDK aliases`); [paper/content/availability.tex:1](../paper/content/availability.tex) (`\section`).

Verified PDF locations: main physical pp. 40; main_submit physical pp. 40. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R9.4

We state exactly the archived SDK aliases openai/gpt-oss-20b (text) and qwen/qwen3.8-27b (vision), not an independently attested catalogue entry or immutable served revision. Forty response fingerprints and near-zero SDK temperature do not certify fixed weights; no hosted seed is recorded. Ninety-one original Pattern requests lack epoch/org fields. Historical provider-catalogue/weight attestation is unavailable; no new provider probe was run to fill it.

**Disposition:** `unresolved_historical_identity`; comment closure not certified. **Remaining:** SDK aliases/fingerprints are not immutable hosted-weight or historical catalogue attestations.

Evidence: [outputs/revision/final_cost_integrity_v1/report.json](../docs/plan/revision_evidence/README.md#final_cost_integrity_v1); [outputs/revision/fusion_prompt_audit_v1/audit.json](../docs/plan/revision_evidence/README.md#fusion_prompt_audit_v1).

Source anchors: [paper/content/experimental_setup.tex:71](../paper/content/experimental_setup.tex) (`Archived SDK aliases`); [paper/content/availability.tex:1](../paper/content/availability.tex) (`\section`).

Verified PDF locations: main physical pp. 40; main_submit physical pp. 40. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R9.5

The final archive remains a local private draft: PID is null and public release is not authorized. Author-addition licensing, OHLCV redistribution, CafeF excerpts, model assets and hosted-output sharing terms require decisions; the QuantAgent notice alone is insufficient. We prepared offline verification/assembly instructions and an itemized rights register. We cannot provide a genuine DOI until the author has permission and publishes a suitable version; this request remains incomplete. The F05 final local manuscript handoff has public_release_authorized=false and pid=null. Completing U10 means an evidence-aligned local package, not journal acceptance or permission to redistribute data.

**Disposition:** `pending_rights_or_author_route`; comment closure not certified. **Remaining:** PID is null and public release remains unauthorized; no repository commit or local ZIP substitutes for publication rights.

Evidence: [outputs/revision/reproducibility_v1/manifest.json](../docs/plan/revision_evidence/README.md#reproducibility_v1); [outputs/revision/reproducibility_v1/rights.json](../docs/plan/revision_evidence/README.md#reproducibility_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/availability.tex:2](../paper/content/availability.tex) (`Public distribution rights`).

Verified PDF locations: main physical pp. 40; main_submit physical pp. 40. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R9.6

The existing no-network package-only replay reproduced 375 saved predictions, 684 T04 accounts and 37 tensors from the archived inputs, with zero unexpected external reads/network/process attempts in its isolation report. T34 verifies bytes and round-trip archive contents; it does not rerun that replay, inference, scoring or model fitting. The archive distinguishes original base evidence, the NumPy runtime image and the final response/source overlay so versions are not silently substituted. F01 previously restored 286 ignored assets and cold-replayed all fifteen U09 analysis artifacts byte-identically; F02 previously cold-replayed twenty-six presentation artifacts. F05 verifies those bindings and builds/renders the PDFs; it does not claim those scientific replays were rerun.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Existing cold replays reproduce saved outputs only; F05 checks hashes/builds PDFs and does not rerun inference, fitting or scientific analyses.

Evidence: [outputs/revision/clean_replay_v1/metrics_qa.json](../docs/plan/revision_evidence/README.md#clean_replay_v1); [outputs/revision/reproducibility_v1/manifest.json](../docs/plan/revision_evidence/README.md#reproducibility_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/experimental_setup.tex:71](../paper/content/experimental_setup.tex) (`Archived SDK aliases`); [paper/content/availability.tex:1](../paper/content/availability.tex) (`\section`).

Verified PDF locations: main physical pp. 40; main_submit physical pp. 40. Current section/table context; locators do not certify acceptance or unperformed evidence.

## R10 — Selection diagnostics and auxiliary numeric controls

### R10.1

Native frequency diagnostics cover all 85 candidates at all 102 cutoffs: 8,670 opportunities and 510 selected slots. WQ42 appears at 52/102 cutoffs (52/510 slots). Full per-factor eligible/opportunity denominators and zero selections remain in the registry diagnostics. These dependent in-sample counts are not out-of-sample discoveries or evidence that selecting five eliminated multiplicity.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Complete dependent in-sample selection counts do not establish out-of-sample factor stability.

Evidence: [outputs/revision/alpha_selection_v1/aggregate.json](../docs/plan/revision_evidence/README.md#alpha_selection_v1).

Source anchors: [paper/content/results.tex:69](../paper/content/results.tex) (`Native diagnostics separately account`).

Verified PDF locations: main physical pp. 16, 32, 46; main_submit physical pp. 15, 32, 45. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R10.2

We report 1,282 adjacent nonzero-IC sign flips over 7,894 eligible transition pairs, alongside per-factor sign/support and basket turnover. Native orientation/ranking is fitted on the trailing diagnostic sample. Row-wise causal probes fail for delay-bfill, whole-Series normalization and the full-frame volume branch; an outer-cutoff fixture passing does not cure that failure or make sign stability causal. Common uses a separate frozen causal-alpha projection with 51 selector bindings. Native-to-common also changes instructions, so its U09 bridge is not a pure correction/treatment effect.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** Native row-wise causal FAIL remains; the separate frozen common selector does not repair native history.

Evidence: [outputs/revision/alpha_selection_v1/aggregate.json](../docs/plan/revision_evidence/README.md#alpha_selection_v1); [outputs/revision/alpha_selection_v1/transitions.json](../docs/plan/revision_evidence/README.md#alpha_selection_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/problem_formulation.tex:260](../paper/content/problem_formulation.tex) (`The native row-wise causal gate fails.`); [paper/content/tables/component/numeric_controls.tex:6](../paper/content/tables/component/numeric_controls.tex) (`\label{tab:numeric}`).

Verified PDF locations: main physical pp. 16, 32, 46; main_submit physical pp. 15, 32, 45. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R10.3

We provide a separate train-fitted numeric fixed-custom-five control, with eligibility, imputation, scaling and orientation fitted only on purged training data. Dynamic-minus-fixed BA is +15.84 pp, nominal six-block sign-flip p=0.0625. This is not the requested fixed-factor hosted-LLM experiment and does not retrospectively repair native LLM inputs; that stronger experiment remains unperformed and the corresponding claims are withdrawn.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** Numeric fixed-factor control is available; the requested fixed-factor hosted-LLM intervention was not executed.

Evidence: [outputs/revision/numeric_controls_v1/summary.json](../docs/plan/revision_evidence/README.md#numeric_controls_v1); [revision/numeric_controls_protocol.json](../revision/numeric_controls_protocol.json).

Source anchors: [paper/content/results.tex:65](../paper/content/results.tex) (`Table~\ref{tab:numeric} is a separate numeric study`).

Verified PDF locations: main physical pp. 16, 32, 46; main_submit physical pp. 15, 32, 45. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R10.4

All twenty predeclared random eligible-five trials are retained, giving 23 numeric strategies and 2,346 predictions on 102 units. Dynamic-minus-random-family and dynamic-minus-no-flip BA differences are +7.33/+6.44 pp with exact six-block p=0.125/0.53125. Holm over all 23 declared hypotheses gives adjusted p=1 throughout. No seed is chosen by test outcome, and these controls do not constitute a completed Reality Check, Deflated Sharpe analysis or fixed/random LLM test.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** All random numeric trials/Holm family are retained; no random-factor hosted LLM, White Reality Check or Deflated Sharpe study.

Evidence: [outputs/revision/numeric_controls_v1/inference.json](../docs/plan/revision_evidence/README.md#numeric_controls_v1); [outputs/revision/numeric_controls_v1/summary.json](../docs/plan/revision_evidence/README.md#numeric_controls_v1).

Source anchors: [paper/content/results.tex:65](../paper/content/results.tex) (`all twenty random eligible-five trials`).

Verified PDF locations: main physical pp. 16, 32, 46; main_submit physical pp. 15, 32, 45. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R10.5

The complete registry lists all 101 source WorldQuant expressions, 80 retained adaptations, five custom handlers and 21 omissions. Seventeen omissions involve industry neutralization, one market capitalization and three price/volume omissions lack an authenticated selection rationale. We retain those unknown reasons rather than presenting all omissions as necessary or mathematically justified.

**Disposition:** `unresolved_historical_identity`; comment closure not certified. **Remaining:** Three price/volume omissions lack an authenticated selection rationale; the other exclusions are documented.

Evidence: [outputs/revision/alpha_registry_v1/registry.json](../docs/plan/revision_evidence/README.md#alpha_registry_v1); [outputs/revision/alpha_registry_v1/summary.json](../docs/plan/revision_evidence/README.md#alpha_registry_v1).

Source anchors: [paper/content/problem_formulation.tex:121](../paper/content/problem_formulation.tex) (`three price/volume omissions lack`).

Verified PDF locations: main physical pp. 16, 32, 46; main_submit physical pp. 15, 32, 45. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R10.6

Each retained expression is linked to the actual handler, operator calls, windows, tie/fill conventions and divergences, with separate fixtures and causal probes. The implemented time-series/proxy adaptations are not claimed equivalent to every source cross-sectional expression. Native leakage/normalization defects and custom registry-versus-prototype differences remain explicit; causal numeric adapters are a separate path, not a retroactive certificate for frozen native inputs. Native/common projections retain the shared I/P/T, chart and sentiment parent. Different operator profiles and frozen fits remain explicit in the four updated diagrams and method text.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** Operator divergences/probes are documented; source-expression equivalence and repaired native causal construction are not certified.

Evidence: [outputs/revision/alpha_contract_v1/leakage.json](../docs/plan/revision_evidence/README.md#alpha_contract_v1); [outputs/revision/alpha_contract_v1/summary.json](../docs/plan/revision_evidence/README.md#alpha_contract_v1); [outputs/revision/alpha_registry_v1/registry.json](../docs/plan/revision_evidence/README.md#alpha_registry_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/problem_formulation.tex:260](../paper/content/problem_formulation.tex) (`The native row-wise causal gate fails.`); [paper/content/tables/component/numeric_controls.tex:6](../paper/content/tables/component/numeric_controls.tex) (`\label{tab:numeric}`).

Verified PDF locations: main physical pp. 16, 32, 46; main_submit physical pp. 15, 32, 45. Current section/table context; locators do not certify acceptance or unperformed evidence.

## R11 — Target definition and the legacy price alias

### R11.1

The text and exported contract now use the net Open[d+1]-to-Close[d+3] candidate-LONG target with fee 0.0025 and slippage 0.001 on each leg, UP iff net return >0. The old close-to-close state-schema description is not used as the truth definition. Seven gross/net label disagreements are disclosed; saved net-elicited decisions and labels are not altered to fit the correction. The extension retains the same economic oracle. The 828/852 raw-bank/query audit count denotes numerical net-return differences above 1e-8, not 828 binary label flips; the maximum absolute discrepancy is about 0.042988489 pp.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Canonical net target and schema are documented; old raw records and saved net-elicited predictions remain unchanged.

Evidence: [outputs/revision/final_contracts_v1/targets.json](../docs/plan/revision_evidence/README.md#final_contracts_v1); [revision/target_schema.json](../revision/target_schema.json); [outputs/revision/author_preserved_v1/formula_comparison.json](../docs/plan/revision_evidence/README.md#author_preserved_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/problem_formulation.tex:99](../paper/content/problem_formulation.tex) (`actual\_prev\_close`).

Verified PDF locations: main physical pp. 7, 22; main_submit physical pp. 6, 22. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R11.2

Canonical exports distinguish decision Close, entry Open and exit Close. The legacy actual_prev_close field has unresolved semantics and is not authenticated as decision Close because it matches entry Open. The two prices differ at 65/102 final units. We document the alias and preserve raw legacy records instead of silently renaming a historical number or recomputing its labels.

**Disposition:** `unresolved_historical_identity`; comment closure not certified. **Remaining:** The legacy actual_prev_close meaning is unresolved; price equality is not provenance evidence.

Evidence: [outputs/revision/final_contracts_v1/report.md](../docs/plan/revision_evidence/README.md#final_contracts_v1); [outputs/revision/final_contracts_v1/targets.json](../docs/plan/revision_evidence/README.md#final_contracts_v1).

Source anchors: [paper/content/problem_formulation.tex:99](../paper/content/problem_formulation.tex) (`actual\_prev\_close`).

Verified PDF locations: main physical pp. 7; main_submit physical pp. 6. Current section/table context; locators do not certify acceptance or unperformed evidence.

## R12 — Indicator identities and priority rules

### R12.1

Table D.1 gives ordered RSI rules: RSI>=70 is bearish first; RSI<=30 bullish; 55<=RSI<70 bullish; 30<RSI<=45 bearish. The interior 45<RSI<55 uses change against the third retained sample rather than being automatically neutral. Order and boundaries prevent RSI>=70 satisfying both directions. We describe the implemented rule rather than claiming RSI independently predicts profitable returns.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Ordered implemented RSI boundaries are explicit; deterministic rules are not calibrated financial predictors.

Evidence: [outputs/revision/final_contracts_v1/indicators.json](../docs/plan/revision_evidence/README.md#final_contracts_v1); [outputs/revision/final_contracts_v1/report.md](../docs/plan/revision_evidence/README.md#final_contracts_v1).

Source anchors: [paper/content/tables/component/indicator_rules.tex:6](../paper/content/tables/component/indicator_rules.tex) (`\label{tab:indicator_rules}`).

Verified PDF locations: main physical pp. 39; main_submit physical pp. 39. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R12.2

The five actual Indicator votes are MACD, RSI, Stochastic, Williams %R and ROC, described as momentum/trend indicators rather than five volatility oscillators. Their exact ordered thresholds and missing/error convention are in Table D.1 and the frozen indicator contract. The backtest node is deterministic, not an extra Indicator LLM call.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Five momentum/trend votes and the deterministic backtest path are documented; no extra observed Indicator LLM call.

Evidence: [outputs/revision/final_contracts_v1/indicators.json](../docs/plan/revision_evidence/README.md#final_contracts_v1); [outputs/revision/final_contracts_v1/report.md](../docs/plan/revision_evidence/README.md#final_contracts_v1).

Source anchors: [paper/content/tables/component/indicator_rules.tex:6](../paper/content/tables/component/indicator_rules.tex) (`\label{tab:indicator_rules}`).

Verified PDF locations: main physical pp. 39; main_submit physical pp. 39. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R12.3

We distinguish declared BB/ADX state slots from numeric arrays/reports actually delivered by the Indicator node. Their presence in an old schema does not imply two additional Indicator votes or an observed volatility signal. Bollinger-derived values on the alpha path are a separate computation; missing numeric state is not invented to match a table.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Declared BB/ADX slots are not delivered Indicator arrays or two additional votes.

Evidence: [outputs/revision/final_contracts_v1/indicators.json](../docs/plan/revision_evidence/README.md#final_contracts_v1); [outputs/revision/final_contracts_v1/report.md](../docs/plan/revision_evidence/README.md#final_contracts_v1).

Source anchors: [paper/content/tables/component/indicator_rules.tex:6](../paper/content/tables/component/indicator_rules.tex) (`\label{tab:indicator_rules}`).

Verified PDF locations: main physical pp. 39; main_submit physical pp. 39. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R12.4

The architecture, shared methods and Table D.1 now use one five-vote contract with the same priority boundaries. Missing/error votes remain in the denominator of five rather than renormalizing only available indicators. Consensus/report text is not represented as a full numeric state-array payload, and the old contradictory indicator table is replaced.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Five-vote rules and denominator are consistent; the reviewer historical Table 1 number is not the current table number.

Evidence: [outputs/revision/final_contracts_v1/indicators.json](../docs/plan/revision_evidence/README.md#final_contracts_v1); [outputs/revision/final_contracts_v1/report.md](../docs/plan/revision_evidence/README.md#final_contracts_v1).

Source anchors: [paper/content/tables/component/indicator_rules.tex:6](../paper/content/tables/component/indicator_rules.tex) (`\label{tab:indicator_rules}`).

Verified PDF locations: main physical pp. 39; main_submit physical pp. 39. Current section/table context; locators do not certify acceptance or unperformed evidence.

## R13 — Signed-volume custom factor descriptions

### R13.1

We now describe native BFE/SignedVolZAlpha4 as tanh(1.5*(%B-0.5)*VolZ5). Negative VolZ5 reverses sign and zero cancels the signal, so it cannot be described as merely confirming volume expansion. The frozen handler/output is not edited to make the previous prose correct.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Signed volume z-score reverses/cancels the native signal; no expansion-only or squeeze gate is inferred.

Evidence: [outputs/revision/alpha_contract_v1/summary.json](../docs/plan/revision_evidence/README.md#alpha_contract_v1); [outputs/revision/final_contracts_v1/report.md](../docs/plan/revision_evidence/README.md#final_contracts_v1).

Source anchors: [paper/content/tables/component/custom_factors.tex:6](../paper/content/tables/component/custom_factors.tex) (`\label{tab:custom_definitions}`).

Verified PDF locations: main physical pp. 16, 38; main_submit physical pp. 15, 38. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R13.2

We withdrew unsupported volume-expansion and squeeze gating descriptions and disclose signed multiplication, proxy inputs and registry/prototype preprocessing differences. The custom appendix separates handler IDs from display rank: selected slot four is not necessarily BFE. Six selected metadata slots disagree with handler descriptions; their actual prompts omit the literal wrong formula, but a semantic effect is not ruled out.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Registry/prototype and metadata mismatches remain disclosed; semantic effects cannot be ruled out.

Evidence: [outputs/revision/alpha_registry_v1/registry.json](../docs/plan/revision_evidence/README.md#alpha_registry_v1); [outputs/revision/final_contracts_v1/report.md](../docs/plan/revision_evidence/README.md#final_contracts_v1).

Source anchors: [paper/content/tables/component/custom_factors.tex:6](../paper/content/tables/component/custom_factors.tex) (`\label{tab:custom_definitions}`).

Verified PDF locations: main physical pp. 38; main_submit physical pp. 38. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R13.3

The scientific text now calls the five formulas custom, not proprietary, and distinguishes source adaptations from new-to-this-comparison implementation choices. No order-flow measurement, protected formula, mathematical source equivalence or investment alpha is inferred from the custom labels. Full definitions remain in Table C.1 and the registry.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Custom means an implementation role, not proprietary ownership, measured order flow or profitable investment alpha.

Evidence: [outputs/revision/alpha_registry_v1/registry.json](../docs/plan/revision_evidence/README.md#alpha_registry_v1); [outputs/revision/final_contracts_v1/report.md](../docs/plan/revision_evidence/README.md#final_contracts_v1).

Source anchors: [paper/content/tables/component/custom_factors.tex:6](../paper/content/tables/component/custom_factors.tex) (`\label{tab:custom_definitions}`).

Verified PDF locations: main physical pp. 38; main_submit physical pp. 38. Current section/table context; locators do not certify acceptance or unperformed evidence.

## R14 — Chart conventions, corrected inputs and visual limits

### R14.1

We withdrew the green-bearish/red-bullish claim. Actual candle bodies are green when Close>Open and red otherwise, including doji; the price-board reference-price convention is a different comparison. Corrected Trend maps support to blue and resistance to red. The manuscript now states actual render rules rather than invoking an inaccurate national convention.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Body colour and exchange-board reference-price rules are distinct; renderer correctness is not model understanding.

Evidence: [outputs/revision/final_cost_integrity_v1/chart_replay.json](../docs/plan/revision_evidence/README.md#final_cost_integrity_v1); [outputs/revision/final_cost_integrity_v1/report.md](../docs/plan/revision_evidence/README.md#final_cost_integrity_v1).

Source anchors: [paper/content/system_architecture.tex:45](../paper/content/system_architecture.tex) (`Candle bodies are green`).

Verified PDF locations: main physical pp. 17; main_submit physical pp. 17. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R14.2

The final integrity audit rerendered 204 PNGs for 102 frozen windows byte/pixel exactly and checked 240 actual vision requests against cached images/templates. Geometry, body colour, support/resistance handles and legend agree. Figure 3 (source label fig:charts) uses exact PNG bytes for the earliest eligible unit (CMG, 3 July 2023), selected chronologically rather than by outcome; its caption and inputs have been checked in both rendered PDFs. Legacy wrong-legend images remain historical evidence and are not overwritten. U08/U09 separately bind actual shared images/reports; the original 204-image/240-request audit is not silently reassigned to the extension. F04 keeps the original CMG PNGs and source U09 contrast image unchanged.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Original chart audit and CMG input provenance are preserved; those counts do not silently describe U08 requests.

Evidence: [outputs/revision/final_cost_integrity_v1/actual_images.csv](../docs/plan/revision_evidence/README.md#final_cost_integrity_v1); [outputs/revision/final_cost_integrity_v1/chart_replay.json](../docs/plan/revision_evidence/README.md#final_cost_integrity_v1); [outputs/revision/final_cost_integrity_v1/report.json](../docs/plan/revision_evidence/README.md#final_cost_integrity_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/system_architecture.tex:60](../paper/content/system_architecture.tex) (`The renderer audit matched 204 images`).

Verified PDF locations: main physical pp. 17; main_submit physical pp. 17. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R14.3

The final whitelist has real corrected-Trend and Decision calls with original Pattern raw-response replay; only its 375 complete jobs enter final results, not incomplete superseded grids. This is not a randomized old/new-image-only effect experiment. Pixel/template agreement does not validate visual comprehension, and Vietnamese xanh remains ambiguous. Counterfactual charts or human local-evidence annotations were not performed; stronger semantic claims are withdrawn. One upstream realization in U09 and three Decision repeats do not add an old/new-chart counterfactual or validate semantic grounding.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** No randomized old/new-image-only, human local-evidence or counterfactual visual-comprehension experiment.

Evidence: [outputs/revision/final_cost_integrity_v1/report.json](../docs/plan/revision_evidence/README.md#final_cost_integrity_v1); [outputs/revision/final_cost_integrity_v1/report.md](../docs/plan/revision_evidence/README.md#final_cost_integrity_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/system_architecture.tex:45](../paper/content/system_architecture.tex) (`Candle bodies are green`).

Verified PDF locations: main physical pp. 17; main_submit physical pp. 17. Current section/table context; locators do not certify acceptance or unperformed evidence.

## R15 — Execution, settlement and horizon assumptions

### R15.1

The reference ledger assumes shares become sellable in the afternoon of T+2 conditional on allocation/fill, and sale proceeds remain pending until the specified settlement phase. We distinguish marked wealth, liquidated cash, pending receivables and advances/fees. The historical settlement source is cited, but an assumed phase convention is not proof that an actual opening/closing order would fill.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** Settlement/advance phases and broker/fill assumptions are not authenticated executable trades.

Evidence: [outputs/revision/execution_evidence_v1/sources.json](../docs/plan/revision_evidence/README.md#execution_evidence_v1); [outputs/revision/execution_final_v1/report.md](../docs/plan/revision_evidence/README.md#execution_final_v1).

Source anchors: [paper/content/experimental_setup.tex:63](../paper/content/experimental_setup.tex) (`Shares are assumed`); [paper/content/tables/component/execution_sensitivity.tex:6](../paper/content/tables/component/execution_sensitivity.tex) (`\label{tab:execution}`).

Verified PDF locations: main physical pp. 43; main_submit physical pp. 42. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R15.2

The paper reports all twelve cost, pending-cash, advance, tax/charge, no-fill/delay and lot/capacity scenarios on unchanged predictions. Daily OHLC/vendor-volume proxies do not authenticate opening auction queues, price-limit availability, partial fills or units. Ten HVN venue/calendar unit flags remain flagged; they are not silently excluded or converted to certified trades. The all-missed zero result is not a mathematical worst-return bound. All twelve execution sensitivities remain results of the original study only. U09 reports its own daily/cycle ledgers, cost/exposure and coverage; no unexecuted stress scenarios are attributed to the extensions.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** Twelve original sensitivities use OHLCV proxies; no certified queues, partial fills, venue units, capacity or corporate actions; not rerun for U09.

Evidence: [outputs/revision/execution_evidence_v1/report.md](../docs/plan/revision_evidence/README.md#execution_evidence_v1); [outputs/revision/execution_evidence_v1/sample_audit.json](../docs/plan/revision_evidence/README.md#execution_evidence_v1); [outputs/revision/execution_final_v1/report.md](../docs/plan/revision_evidence/README.md#execution_final_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/experimental_setup.tex:63](../paper/content/experimental_setup.tex) (`Shares are assumed`); [paper/content/tables/component/execution_sensitivity.tex:6](../paper/content/tables/component/execution_sensitivity.tex) (`\label{tab:execution}`).

Verified PDF locations: main physical pp. 43; main_submit physical pp. 42. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R15.3

L=3 is a fixed observed-bar protocol choice: buy on d+1 and exit on d+3, two observed sessions after entry, with three bars including entry. We do not infer horizon optimality from settlement or claim it dominates alternatives. Costs and executable-price assumptions are stated separately from the classification target and its unchanged saved decisions. The same Open(t+1)-to-Close(t+3), two-leg-cost contract governs extension labels/accounts. No new L5/L10 or optimized horizon experiment is implied.

**Disposition:** `partial_missing_scientific_evidence`; comment closure not certified. **Remaining:** L=3 is fixed by protocol; no L5/L10 study or horizon-optimality claim.

Evidence: [outputs/revision/execution_final_v1/report.md](../docs/plan/revision_evidence/README.md#execution_final_v1); [outputs/revision/final_contracts_v1/targets.json](../docs/plan/revision_evidence/README.md#final_contracts_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/experimental_setup.tex:63](../paper/content/experimental_setup.tex) (`Shares are assumed`); [paper/content/tables/component/execution_sensitivity.tex:6](../paper/content/tables/component/execution_sensitivity.tex) (`\label{tab:execution}`).

Verified PDF locations: main physical pp. 43; main_submit physical pp. 42. Current section/table context; locators do not certify acceptance or unperformed evidence.

## R16 — Bibliographic corrections and unresolved historical numbering

### R16.1

We added an explicit Kakushadze 101 Formulaic Alphas citation at the catalogue/adaptation description. Metadata follows the audited primary publication/version; the registry documents deviations instead of implying all 101 expressions are implemented exactly. The source citation is not evidence of profitable alphas in this study. Three additional primary sources for Bayesian ICL, prompt retrieval and regime filtering were inspected in F03; their assumptions do not establish a correct financial posterior or a profitability guarantee.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Formulaic Alphas source is cited; adapted operators are not claimed mathematically equivalent.

Evidence: [outputs/revision/reference_audit_v1/changes.csv](../docs/plan/revision_evidence/README.md#reference_audit_v1); [outputs/revision/reference_audit_v1/reference_audit.json](../docs/plan/revision_evidence/README.md#reference_audit_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json); [docs/plan/week12/manuscript_content_checks.zip](../docs/plan/week12/manuscript_content_checks.zip).

Source anchors: [paper/references.bib:130](../paper/references.bib) (`kakushadze2016formulaic`); [paper/content/related_work.tex:1](../paper/content/related_work.tex) (`\section{Related works}`).

Verified PDF locations: main physical pp. 4, 32, 50; main_submit physical pp. 4, 32, 49. Current bibliography context only; historical [14]/[21]/[22]/[23] identities remain unresolved. Deng is uncited.

### R16.2

We added the audited ViSoBERT paper citation and retained a separate model-card reference for the 5CD-AI classifier. The text distinguishes backbone architecture/pretraining domain from downstream labels and the unvalidated financial-news use. The classifier version/revision is not assigned retrospectively to legacy records with unknown scorer identity.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** ViSoBERT paper and separate classifier card are cited without financial-domain or unknown-legacy-scorer attribution.

Evidence: [outputs/revision/reference_audit_v1/reference_audit.json](../docs/plan/revision_evidence/README.md#reference_audit_v1); [outputs/revision/sentiment_contract_v1/scorer_tokenizer.json](../docs/plan/revision_evidence/README.md#sentiment_contract_v1); [docs/plan/week12/manuscript_content_checks.zip](../docs/plan/week12/manuscript_content_checks.zip).

Source anchors: [paper/references.bib:178](../paper/references.bib) (`nguyen2023visobert`); [paper/content/related_work.tex:1](../paper/content/related_work.tex) (`\section{Related works}`).

Verified PDF locations: main physical pp. 4, 32, 50; main_submit physical pp. 4, 32, 49. Current bibliography context only; historical [14]/[21]/[22]/[23] identities remain unresolved. Deng is uncited.

### R16.3

White (2000) is cited for data-snooping methodology, alongside a clearly prospective discussion of additional selection-aware evidence. We do not claim a completed White Reality Check or Deflated Sharpe analysis: the completed numeric family uses the explicitly described block/sign-flip/Holm diagnostics.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** White is cited for methodology/future work; no completed Reality Check is claimed.

Evidence: [outputs/revision/reference_audit_v1/changes.csv](../docs/plan/revision_evidence/README.md#reference_audit_v1); [outputs/revision/reference_audit_v1/reference_audit.json](../docs/plan/revision_evidence/README.md#reference_audit_v1); [docs/plan/week12/manuscript_content_checks.zip](../docs/plan/week12/manuscript_content_checks.zip).

Source anchors: [paper/references.bib:326](../paper/references.bib) (`white2000reality`); [paper/content/related_work.tex:1](../paper/content/related_work.tex) (`\section{Related works}`).

Verified PDF locations: main physical pp. 4, 32, 50; main_submit physical pp. 4, 32, 49. Current bibliography context only; historical [14]/[21]/[22]/[23] identities remain unresolved. Deng is uncited.

### R16.4

TradingAgents is attributed to the four audited authors Xiao, Sun, Luo and Wang, with the reviewed arXiv version/year distinguished from first posting. The organizational placeholder is removed. The related-work claim is limited to that system rather than establishing novelty for multi-agent trading architectures.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Current TradingAgents authors/version are audited; this does not authenticate the historical reviewed numbering.

Evidence: [outputs/revision/reference_audit_v1/changes.csv](../docs/plan/revision_evidence/README.md#reference_audit_v1); [outputs/revision/reference_audit_v1/reference_audit.json](../docs/plan/revision_evidence/README.md#reference_audit_v1); [docs/plan/week12/manuscript_content_checks.zip](../docs/plan/week12/manuscript_content_checks.zip).

Source anchors: [paper/references.bib:260](../paper/references.bib) (`tradingagents2024`); [paper/content/related_work.tex:1](../paper/content/related_work.tex) (`\section{Related works}`).

Verified PDF locations: main physical pp. 4, 32, 50; main_submit physical pp. 4, 32, 49. Current bibliography context only; historical [14]/[21]/[22]/[23] identities remain unresolved. Deng is uncited.

### R16.5

The Tsantekidis citation is described as limit-order-book forecasting rather than candlestick image recognition. The paragraph no longer treats that task as a chart-image benchmark or evidence that our Pattern Agent improves candlestick understanding.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** LOB forecasting citation no longer serves as candlestick-recognition validation.

Evidence: [outputs/revision/reference_audit_v1/changes.csv](../docs/plan/revision_evidence/README.md#reference_audit_v1); [outputs/revision/reference_audit_v1/reference_audit.json](../docs/plan/revision_evidence/README.md#reference_audit_v1); [docs/plan/week12/manuscript_content_checks.zip](../docs/plan/week12/manuscript_content_checks.zip).

Source anchors: [paper/references.bib:269](../paper/references.bib) (`tsantekidis2017lob`); [paper/content/related_work.tex:1](../paper/content/related_work.tex) (`\section{Related works}`).

Verified PDF locations: main physical pp. 4, 32, 50; main_submit physical pp. 4, 32, 49. Current bibliography context only; historical [14]/[21]/[22]/[23] identities remain unresolved. Deng is uncited.

### R16.6

Deng metadata distinguishes the 2017 issue from 2016 online-first timing in the retained source entry. That entry remains uncited and therefore has no rendered reference number. The current bibliography contains 43 entries and 21 rendered cited keys, including three primary sources added in F03 for regime context, Bayesian ICL and prompt retrieval. Current numbering is read from both newly built PDFs; it does not authenticate historical reviewer reference identities.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Deng metadata distinguishes issue/online-first dates; it is retained uncited and has no rendered number.

Evidence: [outputs/revision/reference_audit_v1/changes.csv](../docs/plan/revision_evidence/README.md#reference_audit_v1); [outputs/revision/reference_audit_v1/reference_audit.json](../docs/plan/revision_evidence/README.md#reference_audit_v1); [docs/plan/week12/manuscript_content_checks.zip](../docs/plan/week12/manuscript_content_checks.zip).

Source anchors: [paper/references.bib:38](../paper/references.bib) (`deng2017deep`); [paper/content/related_work.tex:1](../paper/content/related_work.tex) (`\section{Related works}`).

Verified PDF locations: main physical pp. 4, 32; main_submit physical pp. 4, 32. Current bibliography context only; historical [14]/[21]/[22]/[23] identities remain unresolved. Deng is uncited.

### R16.7

For reviewer reference [14], its identity in the reviewed PDF has not been authenticated from the available version records. We audited all 41 original entries, removed three wrong-identity DOI entries and replaced an unverified herding entry with a separately identified source. We cannot assert which revised key equals historical [14] or invent its DOI; reviewed-version mapping remains unresolved, and current numbering is verified separately and does not authenticate the historical reference identity.

**Disposition:** `unresolved_historical_identity`; comment closure not certified. **Remaining:** Historical reviewed reference [14] cannot be identified from current BibTeX numbering.

Evidence: [outputs/revision/reference_audit_v1/changes.csv](../docs/plan/revision_evidence/README.md#reference_audit_v1); [outputs/revision/reference_audit_v1/inventory.json](../docs/plan/revision_evidence/README.md#reference_audit_v1); [outputs/revision/reference_audit_v1/reference_audit.json](../docs/plan/revision_evidence/README.md#reference_audit_v1); [docs/plan/week12/manuscript_content_checks.zip](../docs/plan/week12/manuscript_content_checks.zip).

Source anchors: [paper/content/related_work.tex:6](../paper/content/related_work.tex) (`Tsantekidis`); [paper/references.bib:1](../paper/references.bib) (`@`).

Verified PDF locations: main physical pp. 4, 32; main_submit physical pp. 4, 32. Current bibliography context only; historical [14]/[21]/[22]/[23] identities remain unresolved. Deng is uncited.

### R16.8

The historical identity of reviewer reference [21] likewise remains unresolved; current BibTeX order is not evidence of the reviewer's numbering. The complete entry-by-entry audit and applied replacement/removal actions are supplied. No unverified DOI is retained as authenticated, but we cannot claim that a specific revised entry answers historical [21] without the correct reviewed reference list.

**Disposition:** `unresolved_historical_identity`; comment closure not certified. **Remaining:** Historical reviewed reference [21] cannot be identified from current BibTeX numbering.

Evidence: [outputs/revision/reference_audit_v1/changes.csv](../docs/plan/revision_evidence/README.md#reference_audit_v1); [outputs/revision/reference_audit_v1/inventory.json](../docs/plan/revision_evidence/README.md#reference_audit_v1); [outputs/revision/reference_audit_v1/reference_audit.json](../docs/plan/revision_evidence/README.md#reference_audit_v1); [docs/plan/week12/manuscript_content_checks.zip](../docs/plan/week12/manuscript_content_checks.zip).

Source anchors: [paper/content/related_work.tex:6](../paper/content/related_work.tex) (`Tsantekidis`); [paper/references.bib:1](../paper/references.bib) (`@`).

Verified PDF locations: main physical pp. 4, 32; main_submit physical pp. 4, 32. Current bibliography context only; historical [14]/[21]/[22]/[23] identities remain unresolved. Deng is uncited.

### R16.9

The same limitation applies separately to reviewer reference [22]. We provide the audited titles, version-specific metadata and applied bibliography actions, rather than mapping [22] by current key position. The identity/DOI requested for that historical number has not been independently established and remains an explicit shortfall.

**Disposition:** `unresolved_historical_identity`; comment closure not certified. **Remaining:** Historical reviewed reference [22] cannot be identified from current BibTeX numbering.

Evidence: [outputs/revision/reference_audit_v1/changes.csv](../docs/plan/revision_evidence/README.md#reference_audit_v1); [outputs/revision/reference_audit_v1/inventory.json](../docs/plan/revision_evidence/README.md#reference_audit_v1); [outputs/revision/reference_audit_v1/reference_audit.json](../docs/plan/revision_evidence/README.md#reference_audit_v1); [docs/plan/week12/manuscript_content_checks.zip](../docs/plan/week12/manuscript_content_checks.zip).

Source anchors: [paper/content/related_work.tex:6](../paper/content/related_work.tex) (`Tsantekidis`); [paper/references.bib:1](../paper/references.bib) (`@`).

Verified PDF locations: main physical pp. 4, 32; main_submit physical pp. 4, 32. Current bibliography context only; historical [14]/[21]/[22]/[23] identities remain unresolved. Deng is uncited.

### R16.10

For reviewer reference [23], historical numbering/title identity is also unverified. All current citations have defined keys in source QA, but the separately verified current rendered numbering does not authenticate the reviewer's historical [23]. We retain this unresolved version-mapping requirement for final reference/PDF checks instead of declaring the whole comment closed.

**Disposition:** `unresolved_historical_identity`; comment closure not certified. **Remaining:** Historical reviewed reference [23] cannot be identified from current BibTeX numbering.

Evidence: [outputs/revision/reference_audit_v1/changes.csv](../docs/plan/revision_evidence/README.md#reference_audit_v1); [outputs/revision/reference_audit_v1/inventory.json](../docs/plan/revision_evidence/README.md#reference_audit_v1); [outputs/revision/reference_audit_v1/reference_audit.json](../docs/plan/revision_evidence/README.md#reference_audit_v1); [docs/plan/week12/manuscript_content_checks.zip](../docs/plan/week12/manuscript_content_checks.zip).

Source anchors: [paper/content/related_work.tex:6](../paper/content/related_work.tex) (`Tsantekidis`); [paper/references.bib:1](../paper/references.bib) (`@`).

Verified PDF locations: main physical pp. 4, 32; main_submit physical pp. 4, 32. Current bibliography context only; historical [14]/[21]/[22]/[23] identities remain unresolved. Deng is uncited.

## R17 — Presentation and scope

### R17.1

The appendix retains the original scientific topics: role-specific prompt contracts, shared-state semantics, custom formulas, indicator rules and reproducibility scope. Exact full prompts, complete code/schema listings and Flask/tokenizer/endpoint/API operations remain in repository notes/runbooks and the rights-qualified private package. These concise explanations distinguish optional live paths from the calls actually evaluated; S1-S4 retain complete scientific row sets. The extension methodology and main comparison appear in the body; prompt/schema/teacher/utility/support/sensitivity details fit within the preserved A-F topics. This does not assert that every requested brevity preference is fulfilled.

**Disposition:** `partial_editorial_request`; comment closure not certified. **Remaining:** Operational listings stay in the repository; author-required A-F topics and scientific details remain, so a blanket appendix reduction is not claimed.

Evidence: [outputs/revision/final_regression_v1/report.json](../docs/plan/revision_evidence/README.md#final_regression_v1); [outputs/revision/reproducibility_v1/manifest.json](../docs/plan/revision_evidence/README.md#reproducibility_v1); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/content/appendices.tex:2](../paper/content/appendices.tex) (`\appendix`); [paper/main.tex:63](../paper/main.tex) (`\title{`); [revision/implementation_notes.md:1](../revision/implementation_notes.md) (`#`).

Verified PDF locations: main physical pp. 14, 18, 22, 29, 35, 37, 40; main_submit physical pp. 14, 18, 22, 28, 35, 36, 40. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R17.2

The article retains the author-required title, eight main sections, original subsection topics and six appendices A-F. The current build has seven figures, eight main tables and thirteen appendix tables, plus the ruled line-numbered Algorithm 1. Its 27 equation/align environments are unchanged from F04; the 24 pre-extension formulation blocks retain their F03-preserved content, with the extension/metric additions distinguished. Main has 51 physical pages and submit 50, including highlights. We preserve scientific detail rather than asserting that the requested appendix reduction or every brevity preference is satisfied. No journal page-limit or anonymity compliance is certified.

**Disposition:** `partial_editorial_request`; comment closure not certified. **Remaining:** Current 51/50-page article retains eight sections/A-F and full evidence; requested brevity/page-limit adequacy remains for editor assessment.

Evidence: [outputs/revision/final_baselines_v1/report.md](../outputs/revision/final_baselines_v1/report.md); [docs/plan/week12/manuscript_final_checks.zip](../docs/plan/week12/manuscript_final_checks.zip); [outputs/revision/author_preserved_v1/formula_comparison.json](../docs/plan/revision_evidence/README.md#author_preserved_v1).

Source anchors: [paper/content/appendices.tex:2](../paper/content/appendices.tex) (`\appendix`); [paper/main.tex:63](../paper/main.tex) (`\title{`); [revision/implementation_notes.md:1](../revision/implementation_notes.md) (`#`).

Verified PDF locations: main physical pp. 6, 14, 16, 18, 22, 29, 35; main_submit physical pp. 6, 14, 15, 18, 22, 28, 35. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R17.3

The rewritten paragraph headings are checked for the double-period pattern, and the old heading is not retained as current prose. The current typeset headings and captions have also been checked in both final PDFs; this does not authenticate the exact historical sentence that the reviewer read.

**Disposition:** `documented_with_limits`; comment closure not certified. **Remaining:** Current paragraph punctuation is checked; exact historical rendered defect is not authenticated.

Evidence: [outputs/revision/reference_audit_v1/inventory.json](../docs/plan/revision_evidence/README.md#reference_audit_v1).

Source anchors: [paper/content/appendices.tex:2](../paper/content/appendices.tex) (`\appendix`); [paper/main.tex:63](../paper/main.tex) (`\title{`); [revision/implementation_notes.md:1](../revision/implementation_notes.md) (`#`).

Verified PDF locations: main physical pp. 14, 18, 22, 29, 35; main_submit physical pp. 14, 18, 22, 28, 35. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R17.4

The quoted sub-tasks-market wording was already absent from the recovered sources and is not attributed to a new isolated fix. The replacement prose avoids that construction and uses explicit LaTeX dash conventions where needed. We do not claim to have located/repaired the exact historical rendered sentence without the reviewed version.

**Disposition:** `unresolved_historical_identity`; comment closure not certified. **Remaining:** Quoted historical sentence is absent from recovered source; current dash conventions do not prove an isolated historical correction.

Evidence: [outputs/revision/reference_audit_v1/inventory.json](../docs/plan/revision_evidence/README.md#reference_audit_v1).

Source anchors: [paper/content/appendices.tex:2](../paper/content/appendices.tex) (`\appendix`); [paper/main.tex:63](../paper/main.tex) (`\title{`); [revision/implementation_notes.md:1](../revision/implementation_notes.md) (`#`).

Verified PDF locations: main physical pp. 14, 18, 22, 29, 35; main_submit physical pp. 14, 18, 22, 28, 35. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R17.5

The original individual-agent subsection structure is retained. Current chart-agent prose uses standard LaTeX quotation pairs, checked visually in both PDFs. The exact historical Section 4.3 quotation defect is not authenticated as a current occurrence; no reviewer-acceptance conclusion follows.

**Disposition:** `unresolved_historical_identity`; comment closure not certified. **Remaining:** Current quotation pairs are checked; the exact historical Section 4.3 defect is unverified.

Evidence: [outputs/revision/reference_audit_v1/inventory.json](../docs/plan/revision_evidence/README.md#reference_audit_v1).

Source anchors: [paper/content/appendices.tex:2](../paper/content/appendices.tex) (`\appendix`); [paper/main.tex:63](../paper/main.tex) (`\title{`); [revision/implementation_notes.md:1](../revision/implementation_notes.md) (`#`).

Verified PDF locations: main physical pp. 13, 14, 18, 22, 29, 35; main_submit physical pp. 13, 14, 18, 22, 28, 35. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R17.6

At the author's instruction, the manuscript retains the original title, Enhancing Multi-Agent Large Language Models for Stock Trading through Quantitative Alpha Integration. The extension is the integration of quantitative alpha and Vietnamese sentiment into the reused chart-agent framework. The abstract, five academic highlights, contributions and conclusion describe that method and the observed class-aware/economic results; they do not claim a novel learned fusion model, causal alpha, stable superiority or profitable deployment. The narrower retitling proposed in an earlier revision is not adopted in this version, and this presentation request is not declared closed.

**Disposition:** `partial_editorial_request`; comment closure not certified. **Remaining:** Author retains the original title; a narrower decision-support retitling was not adopted and this request is not certified closed.

Evidence: [outputs/revision/final_baselines_v1/financial.csv](../outputs/revision/final_baselines_v1/financial.csv); [outputs/revision/final_baselines_v1/report.md](../outputs/revision/final_baselines_v1/report.md); [outputs/revision/fusion_prompt_audit_v1/audit.json](../docs/plan/revision_evidence/README.md#fusion_prompt_audit_v1); [outputs/revision/author_preserved_v1/formula_comparison.json](../docs/plan/revision_evidence/README.md#author_preserved_v1).

Source anchors: [paper/main.tex:63](../paper/main.tex) (`\title{`).

Verified PDF locations: main physical pp. 14, 18, 22, 29, 34, 35; main_submit physical pp. 14, 18, 22, 28, 34, 35. Current section/table context; locators do not certify acceptance or unperformed evidence.

## R18 — Author metadata

### R18.1

The author confirmed the displayed order and instructed that the remaining metadata be kept. We retain Thanh-Tam Do Thi consistently in the main author line, the commented submit line and CRediT, with the current affiliation mapping. We do not invent a given/family split for a submission portal; that separate field is not supplied.

**Disposition:** `pending_rights_or_author_route`; comment closure not certified. **Remaining:** Displayed name/order is author-confirmed; submission-portal given/family fields and any required individual approvals remain unavailable.

Evidence: [outputs/revision/author_metadata_v1/manifest.json](../docs/plan/revision_evidence/README.md#author_metadata_v1); [revision/author_metadata.md](../revision/author_metadata.md); [docs/plan/week12/manuscript_final_checks.zip](../docs/plan/week12/manuscript_final_checks.zip).

Source anchors: [paper/main.tex:69](../paper/main.tex) (`Thanh-Tam Do Thi`).

Verified PDF locations: main physical pp. 1, 2, 34; main_submit: author block not rendered. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R18.2

Under the same confirmation, Van-Tang Nguyen is retained consistently in the author line, commented submit line and CRediT, with the existing corresponding-author marker. We do not change it to the historical Tang-Van variant or infer a new identity. The corresponding email has not been supplied.

**Disposition:** `pending_rights_or_author_route`; comment closure not certified. **Remaining:** Displayed name/order and corresponding marker are retained; corresponding email and editorial route are unavailable.

Evidence: [outputs/revision/author_metadata_v1/manifest.json](../docs/plan/revision_evidence/README.md#author_metadata_v1); [revision/author_metadata.md](../revision/author_metadata.md); [docs/plan/week12/manuscript_final_checks.zip](../docs/plan/week12/manuscript_final_checks.zip).

Source anchors: [paper/main.tex:71](../paper/main.tex) (`Van-Tang Nguyen`).

Verified PDF locations: main physical pp. 1, 2, 34; main_submit: author block not rendered. Current section/table context; locators do not certify acceptance or unperformed evidence.

### R18.3

The author explicitly confirmed Phuong-Thai Nguyen's ORCID as 0009-0006-2033-7788; its earlier single commented-submit correction and the separate metadata snapshot are preserved. F03-F05 retain names/order, affiliations, CRediT, funding and declarations. Manuscript ID, editor letter, submission route, independent ORCID ownership and any required individual signed approvals are not supplied; no submission permission is asserted. F05 preserves the F04 author/CRediT/funding blocks byte-for-byte. The submit source continues to comment author/CRediT blocks while funding is rendered; this is not a certificate of full anonymity or a verified journal route.

**Disposition:** `pending_rights_or_author_route`; comment closure not certified. **Remaining:** Confirmed ORCID and metadata are preserved; manuscript ID, letter, route and independent ownership/consent evidence are not supplied.

Evidence: [outputs/revision/author_metadata_v1/manifest.json](../docs/plan/revision_evidence/README.md#author_metadata_v1); [revision/author_metadata.md](../revision/author_metadata.md); [docs/plan/week12/manuscript_final_checks.zip](../docs/plan/week12/manuscript_final_checks.zip); [docs/plan/week12/unified_analysis_results.zip](../docs/plan/week12/unified_analysis_results.zip); [docs/plan/week12/unified_live_research.zip](../docs/plan/week12/unified_live_research.zip); [outputs/revision/u09_manuscript_assets_v1/manifest.json](../outputs/revision/u09_manuscript_assets_v1/manifest.json).

Source anchors: [paper/main.tex:70](../paper/main.tex) (`0009-0006-2033-7788`).

Verified PDF locations: main physical pp. 1, 2, 34; main_submit: author block not rendered. Current section/table context; locators do not certify acceptance or unperformed evidence.

## Remaining scientific, rights and editorial requirements

The missing prospective/cohort, controlled repeat/ablation, native causal, financial-news provenance/domain, counterfactual visual and executable-market evidence are not created by completing the manuscript. Historical reviewed references [14]/[21]/[22]/[23] remain unidentified. Public PID/redistribution rights, corresponding email, editor letter and submission route remain unavailable. The author-required original title and substantial A-F detail remain, so brevity/title preferences are not claimed fully satisfied. U10 completion denotes this evidence-aligned local manuscript handoff, not acceptance, permission to submit, or public publication. No upload, external contact, submission or deployment has occurred.
