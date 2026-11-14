# Chapter 4. Proposed System: Regime-Aware Bayesian Context for Multi-Agent Trading

> **Draft status: structural skeleton only.** Component explanations, diagrams and algorithms have not been written.
> Each placeholder identifies missing content; a named component does not establish that its isolated effect was measured.

Writing aids: [chapter outline](../outline.md#chapter-4-proposed-system-regime-aware-bayesian-context-for-multi-agent-trading), [EX01](../evidence.md#7-ví-dụ-xuyên-suốt-có-truy-vết), [artifact catalogue](../evidence.md#6-danh-mục-hình-bảng-và-thuật-toán-có-nguồn) and [shared evidence ledger](../evidence.md#8-khung-bản-thảo-và-đối-soát-luận-điểm).

## 4.1. System overview and one-decision walkthrough

> **Not yet drafted.** Introduce the decision problem in plain English and open EX01 at its historical cutoff without revealing its later outcome. Create the overview figure separating deterministic processing, hosted inference, offline training, external policy and post-decision evaluation; introduce readable record names before implementation IDs.

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
