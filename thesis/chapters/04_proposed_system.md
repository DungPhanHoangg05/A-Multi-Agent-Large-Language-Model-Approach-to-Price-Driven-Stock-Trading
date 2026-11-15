# Chapter 4. Proposed System: Regime-Aware Bayesian Context for Multi-Agent Trading

> **Draft status: partial chapter.** Section 4.1 has a source-checked draft and overview figure.
> The remaining placeholders identify missing content; naming a component does not establish its isolated effect.

Writing aids: [chapter outline](../outline.md#chapter-4-proposed-system-regime-aware-bayesian-context-for-multi-agent-trading), [EX01](../evidence.md#7-ví-dụ-xuyên-suốt-có-truy-vết), [artifact catalogue](../evidence.md#6-danh-mục-hình-bảng-và-thuật-toán-có-nguồn) and [shared evidence ledger](../evidence.md#8-khung-bản-thảo-và-đối-soát-luận-điểm).

## 4.1. System overview and one-decision walkthrough

### 4.1.1. What the system decides

At the end of an observed daily bar, the system summarizes admissible price
and textual information and proposes whether to enter the next candidate
LONG cycle. As defined in Chapter 3, execution is LONG or CASH, with entry
at the next observed open and exit at the third future observed close.
The explanation accompanying a proposal is useful for tracing evidence;
it is not a substitute for the subsequent economic outcome.

The proposed system adds historical context to a price-driven multi-agent
pipeline. Its purpose is to present relevant completed experience and
explicit numerical evidence when synthesizing current reports. That purpose
does not imply that every query has sufficient history or that adding
context improves profitability. The component and historical-context studies
remain separate evidence collections, as introduced in the research scope.

### 4.1.2. Computation, interpretation and external policy

Figure F03 distinguishes four kinds of work. **Offline fitting and selection**
produce versioned resources: the Common alpha selector, market-regime
models/scalers and numerical teacher/student. Their permitted fit cutoffs
are checked separately from the price cutoff of each forecast. Query-time
conditioning or retrieval uses these resources without refitting them.

**Deterministic processing** prepares price windows and chart images,
computes indicator values/votes and processes alpha/news inputs. In the
historical path, Indicator returns the computed report directly; it does not
request an additional LLM interpretation. **Hosted interpretation** is used
for Pattern and Trend and for eligible Decision requests. A role name is
therefore not a count of hosted calls.[^overview-source]

The historical execution order is Indicator, Pattern, Trend, followed by
the joint alpha/sentiment stage. F03 groups processing by type rather than
reproducing that node sequence. The resulting **shared snapshot** is a
versioned bundle of reports, visible inputs and provenance. All compared
branches receive protected copies of the same upstream realization. Common
alpha projection and historical/numerical context are subsequently resolved
for the appropriate profile; sharing the parent does not mean every branch
receives an identical final prompt.

The Decision family includes Native/Common foundations, historical-prior
variants and the Fact Anchor/MT path. Dependencies are resolved within the
same repeat. Some branches issue a new request; unsupported branches can
reuse a documented dependency. In the MT path, the numerical student is a
separate model from the hosted Decision LLM. Context and utility estimates
are numerical inputs rather than free-form claims invented by that LLM.

**External resolution** validates the reply, maps LONG/SHORT to executable
actions and, where applicable, keeps or revises an anchor under the utility
rule. Thus a raw proposal and the final action can differ. Technical failure
is recorded as failure, not silently recoded as a legitimate CASH decision.
Only after the forecast/policy record is durable does the evaluation path
join the query outcome and compute classification/account measures. No query
outcome flows back into its forecasting context.[^overview-source]

![System overview separating offline resources, numerical processing, hosted interpretation, policy and later evaluation.](../assets/diagrams/F03_system_overview.png)

*Figure F03. System overview from available inputs to evaluated actions.
This is an Illustrative architecture of the locked historical research path.
The grouped processing boxes distinguish computation types; the text gives
the actual upstream order. Same-repeat dependencies and bypasses remain
explicit, and later outcome data enter evaluation only. Colors do not imply
measured latency, isolated benefits or live acceptance.*
[Vector PDF](../assets/diagrams/F03_system_overview.pdf).

### 4.1.3. Opening the FPT example

The running case, EX01, is FPT at the **3 July 2023** cutoff, with upstream
realization 0 and Decision repeat 0. The saved price prefix ends on that date.
Its final 45 bars supply the chart/Indicator window, while a 600-bar prefix
supports the longer-history path. The case is a saved historical research
execution, not evidence that a trade was executed in July 2023.[^overview-case]

The snapshot reports MACD below its signal line while remaining positive,
and a close above SMA20. Pattern and Trend provide visual interpretations;
news is explicitly unavailable. A reader can now ask which observations
support the reports, whether matured context exists, and how a proposed
action would be resolved. The following sections answer those questions
without treating missing news as observed neutrality.

For this case, the scheduled entry and exit observations are 4 and 6 July.
Their realized prices and net result are deliberately not used to explain
what was known at the cutoff; Chapter 5 will reveal the outcome. The same
case will connect input contracts, report interpretation, context and policy,
with distinct IDs for each saved record rather than a reconstructed successful
example.

[^overview-source]: Frozen graph, unified providers/methods/contracts, alpha projection and MT policy, bound in the shared ledger §9.1 and the earlier BG/TIME source tables. The live graph/Indicator/Decision presentation changes are accepted by the author as logic-equivalent; this does not replace frozen byte identities or complete application acceptance.
[^overview-case]: EX01-S and the declared EX01 selection/source record in the shared ledger §7. CL026–CL028 map this overview, the figure and the case opening; no new inference or market data were collected.

## 4.2. Input preparation and shared state

> **Not yet drafted.** Explain price, VN-Index and news provenance, windows, temporal availability, missingness and snapshot identity. Build the component input/output contract table, keeping query outcomes outside forecast inputs and introducing serialization/provenance only where needed to understand reproducibility.

## 4.3. The base multi-agent pipeline

> **Not yet drafted.** Introduce the shared reports and the path to the base decision. For every role below, explain its purpose, admissible inputs, processing, outputs, consumer, missing-evidence/error behavior and inherited versus adapted elements.

### 4.3.1. Indicator

> **Not yet drafted.** Explain deterministic indicator calculation, priority rules, heuristic votes and missing values. Ground the explanation in the numeric input/report contract and EX01; distinguish computation from hosted inference.

### 4.3.2. Pattern

> **Not yet drafted.** Explain candlestick rendering, the visual evidence requested, report fields and consistency-check limits. Use the archived EX01 image with source identity and English annotations when produced; distinguish the chart from the model's interpretation.

### 4.3.3. Trend

> **Not yet drafted.** Explain the separate support/resistance chart, geometric construction and requested trend report. Contrast its contribution with Pattern and separate geometric checks from the semantic correctness of a forecast.

### 4.3.4. Alpha

> **Not yet drafted.** Explain candidate transformations, orientation, ranking and report selection, with formulas and verified attribution. Disclose in-sample diagnostics and native causality limits, keeping the native and causal-common paths distinct.

### 4.3.5. Sentiment

> **Not yet drafted.** Explain dated articles or frozen aggregates, scoring provenance, aggregation and coverage. Describe explicit unavailability and its relationship to Alpha; preserve EX01's missing news rather than interpreting it as observed neutral sentiment.

### 4.3.6. Decision

> **Not yet drafted.** Explain report condensation, evidence priorities, the structured response and proposal-to-action mapping. Show how a base proposal is formed without assuming one hosted call per named role; keep confidence separate from a calibrated probability.

## 4.4. Native and Common foundations

> **Not yet drafted.** Identify shared inputs and the changes to alpha projection, selector fitting and common instructions. Explain the Native/Common profile bridge and distinguish it from the Full/Base intervention in the separate component study.

## 4.5. Historical memory and market regimes

> **Not yet drafted.** Define episode fields, canonical labels, maturity filtering, reserved IDs and bank provenance. Explain HMM/scaler fitting and query-time regime assignment. Distinguish signal memory from numerical task context, retaining EX01's separate regime sources.

## 4.6. Bayesian Prior v1

> **Not yet drafted.** Explain the purpose of same-stock historical retrieval, temporal filtering, regime/signal matching, ranking and tie-breaking under the evaluated protocol. Annotate a bounded BRPP and explain unsupported-case reuse of the same-repeat Common result; use EX01's recorded examples and support without substituting displayed counts for population size.

## 4.7. Conditional and alternative priors

> **Not yet drafted.** Explain C2's disjoint conditional/background counts, shrinkage and separate readiness gates; contrast Trend/Pattern pooling and explicit-count presentation. Create the comparison table for filtering, statistics, examples, prompt content and fallback. Do not infer embedding search from the name B_semantic; preserve EX01's recorded bypasses.

## 4.8. MT-BICL and action revision

> **Not yet drafted.** Introduce the numerical context and action-revision path before its details. Separate resources trained offline, numerical inference, hosted proposals and external policy, using the source-bound EX01 records.

### 4.8.1. Fact packet and Fact Anchor

> **Not yet drafted.** Define numeric facts, assertions, Common dependency and anchor validation/failure behavior. Explain the limited scope of assertion validity and identify the anchor action before evaluating a proposed revision.

### 4.8.2. Task construction

> **Not yet drafted.** Explain factual buckets, prior tasks, target observations, query vectors, scaling and membership cutoffs. Use EX01 to distinguish task counts from observation counts and displayed signal examples; keep the query unlabeled.

### 4.8.3. Teacher and student

> **Not yet drafted.** Describe the actual locked architecture, teacher targets, training objective, sampling and checkpoint selection with verified attribution. Separate fitting from frozen inference and identify what the student predicts; do not replace the evaluated resource with a generic architecture.

### 4.8.4. Utility

> **Not yet drafted.** Explain posterior sampling of sign and gain/loss magnitude, support requirements, mean/quantiles and insufficient-evidence behavior. Separate student probability, teacher estimates, utility and realized query return; use the recorded EX01 utility values only with their source and units.

### 4.8.5. Context projection

> **Not yet drafted.** Explain complete membership summaries, representative examples, numerical estimates and bounded prompt projection. Distinguish the underlying context from the material displayed to the LLM; provide a source-bound annotated prompt excerpt when prepared.

### 4.8.6. External policy

> **Not yet drafted.** Define anchor retention, eligibility, assertion checks and the strict utility conditions for accepting a different action, including both action directions. Create the policy diagram and distinguish invalid proposals from technical failures; EX01 illustrates retention, not a veto.

### 4.8.7. Traceability

> **Not yet drafted.** Trace raw proposal, anchor, validity, eligibility, bypass, reason and final action as separate records. Identify decisions attributable to the LLM versus external policy and connect them to EX01 without revealing outcome labels as inputs.

## 4.9. Variant orchestration and complete algorithms

> **Not yet drafted.** Present the eight-role dependency table/DAG, one shared upstream realization per point and same-repeat dependency resolution. Distinguish forecast slots, bypasses and actual hosted calls. Write the three algorithms for PIT preparation, method/policy execution and paired forecasting followed by outcome/account joining.

## 4.10. Prompt limits, recovery and application

> **Not yet drafted.** Explain report distillation/capping, BRPP and complete-prompt character limits, retry/backoff, schema handling, checkpoints, resume and UNKNOWN reconciliation. Separate support fallback from technical errors, describe the realtime 1D application with versioned context, and revisit EX01 through final action before explaining when evaluation becomes possible. Application demonstration must retain its actual acceptance limits.
