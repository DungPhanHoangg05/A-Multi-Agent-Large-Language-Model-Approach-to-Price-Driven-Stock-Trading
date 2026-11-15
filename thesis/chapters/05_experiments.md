# Chapter 5. Experiments and Discussion

> **Draft status: partial chapter.** Section 5.1 defines the source-checked study scope; subsequent sections remain to be drafted.
> Result placeholders do not establish comparative performance. This chapter reports locked historical evidence, not newly collected experiments.

Writing aids: [chapter outline](../outline.md#chapter-5-experiments-and-discussion), [locked study inventory](../evidence.md#3-kiểm-kê-nguồn-hiện-tại-và-hai-nghiên-cứu-đã-khóa), [EX01](../evidence.md#7-ví-dụ-xuyên-suốt-có-truy-vết) and [shared evidence ledger](../evidence.md#8-khung-bản-thảo-và-đối-soát-luận-điểm).

## 5.1. Studies and evidence scope

### 5.1.1. Two response collections and two questions

The **component study** examines the price-driven pipeline with and without
alpha/sentiment report components, together with numerical controls and
small upstream/factorial panels. The **historical-context study** compares
Native, Common and historical-context extensions on one accepted shared
upstream realization per market point. It also records Fact Anchor as a
dependency role. These studies address related questions but have separate
response collections, protocol histories and statistical summaries.
Full/Base in the component study must not be relabeled MT/Common, and
Native responses in the second study are not copies of Full responses
from the first.[^study-scope]

| Scope item | Component study | Historical-context study |
| --- | --- | --- |
| Main market support | 102 stock/date points; nine stocks, 12 dates, six blocks, 51 stock/block accounts | The same 102-point market schedule; nine stocks, 12 dates, six folds, 51 stock/fold accounts per repeat |
| Main response comparison | Full (`AS`) versus Base (`B`): 204 Decision outputs, one per branch/point | Eight roles × three Decision repeats: 2,448 forecast slots, including Fact Anchor |
| Wider response support | 375 distinct Decision executions across main and the two small panels, with documented reuse | 1,290 raw Decision responses and 1,158 no-request bypass slots in the main role grid |
| Supplementary evidence | Upstream panel: nine units × three executions × two branches; factorial/placebo: nine units × three executions × five branches; numerical controls and execution scenarios | Two baseline contrast families, Common–Native / Anchor–Common / MT–Anchor bridges, registered numerical economic controls and recorded sensitivities |
| Principal collections | `revision_minimal_final_v1`, `final_repeats_v1`, `final_temporal_v1`, numerical/execution/contract artifacts | U08 hosted collection and U09 analysis artifacts, with separate receipts/source identities |
| Interpretation | Historical exploratory comparisons, post-inference analysis and prompt-family limitations | Historical exposed-cohort comparisons conditional on shared upstream; descriptive sensitivity analysis |

The 375 component executions are not obtained by adding all nominal panel
counts as if independent. Main has 204 outputs; the upstream panel has
54 branch/execution cells but reuses 18 main outputs; the factorial panel
has 135 outputs. Thus $204+54+135-18=375$. The completion record retains
193 reused outputs and 182 newly successful Decision calls, with 194 new
HTTP attempts and 12 errors. “New” is relative to that component release;
it does not count all earlier donor/vision work. Reusing a response avoids
inventing another execution, but does not turn the panel into a new sample
of market conditions.[^component-lineage]

In the context study, a forecast slot is a planned point/role/repeat output.
A bypass has a valid inherited action and provenance but no new Decision
response. Retries, format repair and retired request generations belong
to HTTP accounting, not additional market points. Numerical controls have
no hosted response. Sections 5.3–5.4 specify these units and comparisons
before the result sections report effects.

### 5.1.2. What was frozen, and what acceptance establishes

The component release is identified by run signature
`904b838a466290d9c8aa73245a6285e813b4f7c90d280355d3b2847ed9933fab`.
Its archived exposure audit places the final queue freeze at
**3 November 2026, 14:44:29.033800 UTC**, between the first recorded request
on 2 November and the last on 4 November. No decision or label date in that
audit is after the final queue freeze. The analysis is explicitly
post-inference and the immutable served-weight revision is null.
This is a versioned historical release, not a claim of preregistration or
a prospectively untouched holdout.

The context collection has its own protocol/runtime, source and journal
identities. U08's research receipt was sealed on **12 November 2026,
03:10:18.266468 UTC**; its acceptance audit was recorded at
03:17:37.298613 UTC. U09 binds that exact package and its own analysis
receipt/artifacts. These timestamps identify collection/acceptance history,
not the dates when financial information became available. Earlier donor
exposure, quota amendments and user-authorized replacements remain in the
ledger. The frozen-source snapshot and archive/member hashes identify
which implementation and records support this thesis; they do not freeze
an external hosted model into a reproducible immutable weight revision.
[^study-freezes]

Recorded PASS receipts support integrity, coverage and the checks within
their declared scopes. They do not negate the **Native row-wise causal
FAIL** or the **whole-system NOT_CERTIFIED** limitation. Nor do they certify
the historical availability of all news, exclude model memorization,
establish survivorship-free sampling or demonstrate realizable live fills.
Application browser acceptance is a separate pending gate, as Section
4.10 explains. No experiment, model call, fit or acceptance replay is
performed to write these sections.

The available component factorial/placebo evidence must not fill gaps in
the context study. A matched retrieval-only/statistics-only/no-target/
no-utility/student-versus-policy decomposition is absent from the unified
response collection. Builder support in code is not a measured ablation.
Sections 5.6–5.9 will distinguish observed effects, mechanisms and remaining
evidence needs; the design specified here does not anticipate a favorable
result or claim that adding historical context makes trading profitable.

[^study-scope]: ED01–ED03 component manifest/summary/completion; ED06–ED09 U09/U08 result/receipts and acceptance; ledger §10.1–§10.2, CL117. The shared market schedule does not make the response collections identical.
[^component-lineage]: ED03 completion and component records/panel support in ED02; CL118. The 18 reused upstream cells reconcile nominal panel counts with 375 unique executions; this is accounting, not a new performance estimate.
[^study-freezes]: ED04 contamination audit, ED05 repeat protocol, ED06–ED09 context receipts/acceptance; CL119–CL120. Ledger §3 retains source/package pins and the distinction between receipt scope and scientific validity.

## 5.2. Data and evaluation support

> **Not yet drafted.** Describe the recorded stocks, selected dates, folds, exclusions, accounts, window/warm-up requirements, bank coverage and sentiment missingness using source-bound counts. Explain training/validation/evaluation partitions and data provenance; a sampled schedule is not a continuous daily backtest.

## 5.3. Configuration and paired protocol

> **Not yet drafted.** Report each study's frozen runtime, hosted-model options and source/data/model identities. Explain shared upstream, Decision repeats and role counts; distinguish market points, accounts, slots, new responses, fallback, HTTP attempts and retired records without treating repeats as independent market samples.

## 5.4. Comparators and interventions

> **Not yet drafted.** Specify the actual Full/Base and numerical controls in the component study, then the Native/Common comparison families, bridges and economic controls in the historical-context study. State support for each panel and distinguish cyclic Always-LONG from continuous holding; do not count component panels as unified MT ablations.

## 5.5. Metrics and statistical analysis

> **Not yet drafted.** Define classification metrics, account returns, exposure, turnover, NAV and drawdown with units and denominators. Preserve study-specific aggregation, frequency and undefined-value rules. Describe the recorded paired bootstrap, contrast families, descriptive bands and sensitivities without promising confirmatory significance or calibrated coverage.

## 5.6. Component-study results

> **Not yet drafted.** Import exact values from locked component artifacts and map every result cell to its source. Present main, numerical, upstream and factorial/placebo panels with their own supports; retain classification–return differences, prompt confounding and native causality limits when answering the first research question.

## 5.7. Historical-context results

> **Not yet drafted.** Import exact values for all research roles and economic controls, showing support, response/bypass counts and repeat dispersion. Present the Native and Common contrast families separately and label secondary subset analyses. Retain negative outcomes and baseline-dependent conclusions; no figures or summary estimates have been inserted here.

## 5.8. Mechanisms, case studies and robustness

> **Not yet drafted.** Analyze recorded support/readiness, age/similarity, fallback and Common–Anchor–MT bridges, separating raw proposals from policy actions. Apply the declared case-selection rules, reveal EX01's later outcome here, and include unsupported or incorrect cases. Report only recorded robustness/resource fields; mark absent costs, usage, latency or ablations as unavailable.

## 5.9. Unperformed ablations and threats to validity

> **Not yet drafted.** Identify missing matched ablations and limits involving native causality, input authentication, bank/query provenance, coverage, dependence, historical exposure, model contamination, sampling and execution assumptions. Distinguish numerical return discrepancies from label changes. Conclude with the research-question/observation/supported-answer/remaining-evidence table; do not fill it before reviewing the actual results.
