# Chapter 5. Experiments and Discussion

> **Draft status: partial chapter.** Sections 5.1–5.2 define the source-checked study scope and data support; subsequent sections remain to be drafted.
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

### 5.2.1. Vendor data, admissible views and exclusions

The reconstructed price-quality record identifies vnstock/VCI daily series
requested for 1 January 2020–30 September 2026. Each of the nine raw stock
files has 1,681 observed rows, from 2 January 2020 to 30 September 2026.
Retrieval was recorded on 1 November 2026. The record explicitly labels
these as a **new retrieval, not an authenticated historical-run snapshot**.
Observed vendor sessions are not an independently certified exchange
calendar; a complete action/dividend adjustment ledger is unavailable.
Consistent units allow the stated return calculation but do not resolve
these provenance limitations.[^data-provenance]

BHN's 13 September 2022 row has Open 43.55 below Low 43.96. The analysis
view retains the raw file but discards the prefix through that contradiction:
673 rows are excluded and the valid suffix starts on 14 September 2022.
It does not synthesize a corrected candle. BHN consequently contributes
only the last three evaluation blocks; its six absent earlier stock/date
cells are structural input exclusions, not losses or model failures.
The nine-stock/twelve-date rectangular frame would contain 108 market
cells, but actual eligible support is 102. In the component nine-strategy
grid this is 972 potential cells versus 918 admitted predictions; the 54
absent strategy cells are not additional missing market points.

Each admitted test decision requires 600 historical bars for alpha
preparation, a 45-bar chart/indicator window and three later observed
sessions for the economic label. Longer warm-up requirements of individual
indicators/resources are respected within their own history. Invalid or
unavailable required history is not filled with future data. A retrospective
loader's ability to read future outcome prices is separate from what the
forecast snapshot is allowed to contain.

### 5.2.2. Main schedule and chronological partitions

**Table B04a. Actual market schedule, shared by the two main studies.**
Each admitted stock/fold has two evaluated endpoints. These are selected
decision dates, not every daily decision in the intervening interval.

| Block/fold | First decision | Second decision | Stocks | Points | Stock/fold accounts per method/repeat |
| --- | --- | --- | ---: | ---: | ---: |
| b2023_h2 | 2023-07-03 | 2023-09-22 | 8 | 16 | 8 |
| b2024_h2 | 2024-07-01 | 2024-09-20 | 8 | 16 | 8 |
| b2025_h1 | 2025-01-02 | 2025-03-31 | 8 | 16 | 8 |
| f2025_q4 | 2025-10-01 | 2025-12-19 | 9 | 18 | 9 |
| f2026_q2 | 2026-04-01 | 2026-06-24 | 9 | 18 | 9 |
| f2026_q3 | 2026-07-01 | 2026-09-23 | 9 | 18 | 9 |
| Total | 12 distinct dates | — | 9 distinct stocks | 102 | 51 |

The component numerical-control schedule is chronological and purged.
For example, CMG in b2023_h2 has 70 training cycles and 19 validation
cycles: its last training label is dated 31 March 2023, first validation
decision 5 April, last validation label 28 June and first test decision
3 July. It has two test endpoints and 89 final-refit cycles. Across the
51 component scopes, recorded train counts range from 32 to 318 and
validation counts from 18 to 21; the source audit reports all 51 purge
checks passing. These are the component controls' recorded schedules,
not the final Common-alpha split in the second study.[^data-partitions]

The historical-context study retains all 102 donor endpoints but freezes
one Common-alpha selector per stock **before that stock's earliest test**.
The final eight non-BHN selectors use training decisions from 14 April
2021 to 30 September 2022 and validation decisions from 6 October 2022
to 27 June 2023. Each has 123 admitted train cycles; common validation
support varies from 54 to 60. BHN instead uses 20 December 2023–26 December
2024 for training and 2 January–25 September 2025 for validation, with
85 train and 56 common validation cycles. Labels must mature before the
next partition; these date ranges are decision bounds, not permission to
fit on labels before their exits.

There are 51 selector bindings but only **nine unique fitted selectors**;
later folds reuse each stock's frozen selector. The amended design discloses
an unused expanding-split prototype that computed earlier-fold query
labels, and a support amendment replacing an empty-target global context
freeze with pre-query fold freezes. Final assets exclude all 102 reserved
query IDs before historical label construction. These amendments constrain
the final path but do not erase prior exposure or convert this into a fresh
test. F02 in Chapter 3 illustrates the temporal rules; the table above
provides the actual sampled dates.

### 5.2.3. Coverage, historical resources and missing sentiment

**Table B04b. Main market support and resource coverage.** UP/DOWN are
canonical net-return labels. Missing sentiment is counted once per point
from the context study's saved shared snapshot, before expanding repeats.
The bank column describes stored signal episodes, not eligible episodes
for every query or numerical MT observations.

| Stock | Main points | Net UP / DOWN | Context sentiment unavailable | Stored signal-bank episodes |
| --- | ---: | ---: | ---: | ---: |
| BHN | 6 | 1 / 5 | 5 | 0 |
| CMG | 12 | 3 / 9 | 12 | 0 |
| FPT | 12 | 2 / 10 | 11 | 211 |
| HVN | 12 | 2 / 10 | 8 | 0 |
| MBB | 12 | 5 / 7 | 8 | 0 |
| MWG | 12 | 4 / 8 | 11 | 213 |
| VCB | 12 | 4 / 8 | 9 | 215 |
| VJC | 12 | 4 / 8 | 8 | 0 |
| VNM | 12 | 0 / 12 | 7 | 213 |
| Total | 102 | 25 / 77 | 79 | 852 |

The signal bank covers CORE4 (FPT/MWG/VCB/VNM), whose main support is
48 points; the other five stocks contribute 54. No same-stock bank means
the declared Common fallback, not cross-stock synthetic episodes. The
bank's latest exit is 30 December 2022. Its prices and the query vendor
series have different provenance: the saved audit records 828 of 852
return values differing by more than $10^{-8}$ percentage points, with maximum absolute
difference 0.04298848884252138 percentage points. That is a **return-value
comparison**, not a count of changed binary labels. Original records are
retained rather than relabeled to hide the transfer.

Numerical MT context can cover all nine stocks and is a different resource.
It uses mature cycles frozen before each fold's first query, with all
evaluation IDs withheld, and retains prior/target/query task boundaries.
The HMM, four-feature scaler and teacher/student cutoffs in Section 4.8
must not be substituted with the 2022 signal-bank cutoff. Query-local
support can still fail even where historical data exist.

Context sentiment is unavailable at 79/102 points (approximately 77.45%);
its 23 available points do not establish independent financial sentiment
validation. Component lineage also records fewer than three verified
articles at 79 of its 102 main units. The two counts have different source
fields: article-count metadata versus the shared `is_unavailable` flag.
Neither justifies treating missing text as a neutral score or excluding
those points from the primary comparison. Date metadata and conservative
next-day admission of date-only news enforce the local contract, while
content authenticity and historical availability remain limitations.
[^data-coverage]

The 96-point common-eight and 54-point recent-nine component cohorts are
overlapping sensitivity subsets of the 102, not new independent cohorts.
Likewise, CORE4 is a declared secondary context subset. Main results retain
unsupported/fallback points and their planned denominators; eligibility
must not be chosen after observing returns to create a better-looking
comparison.

[^data-provenance]: ED10 price-quality record, ED11 main predictions and ED13 fold audit; CL121. The raw nine files and BHN valid suffix have distinct identities; vendor data are not certified venue fills.
[^data-partitions]: ED13 component `folds.csv`, ED14 final U06 protocol and ED15 asset manifest `alpha_support.scopes`; CL122–CL123. Earlier component control training and the amended fixed-per-symbol Common selector have different schedules.
[^data-coverage]: ED11/ED12 main labels/lineage, ED15 bank audit/provider support and U08 shared-point metadata checked by the read-only U09 consumer; ED16 prediction grid; CL124–CL125. B04 panels use saved fields and direct counts, not a new signal, label or model evaluation.

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
