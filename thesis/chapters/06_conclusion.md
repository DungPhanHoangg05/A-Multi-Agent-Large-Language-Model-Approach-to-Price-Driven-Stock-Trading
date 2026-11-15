# Chapter 6. Conclusions and Future Work

> **Draft status: partial chapter.** Sections 6.1–6.2 synthesize the approach and answers; limitations and future-work priorities remain in progress.
> Conclusions retain the recorded support, adverse outcomes and unresolved causal and execution limits.

Writing aids: [chapter outline](../outline.md#chapter-6-conclusions-and-future-work) and [shared evidence ledger](../evidence.md#8-khung-bản-thảo-và-đối-soát-luận-điểm).

## 6.1. Summary of the approach

This thesis connects a daily price-driven multi-agent analysis pipeline
with regime-aware historical context and numerical multi-task inference
for Vietnamese-stock LONG/CASH decisions. Price/volume features, chart
reports, adapted alpha signals and dated sentiment provide the current
evidence. Historical branches add earlier completed episodes, with
strict outcome-maturity requirements, market-state conditioning and
explicit readiness rules. The intended information boundary excludes
the current query's future outcome from forecasting.

The implementation provides several ways to introduce that history:
bounded Bayesian count summaries, conditional or alternative priors,
and numerical historical tasks for MT-BICL. The MT path combines a
factual anchor, a numerical student/teacher resource, a hosted proposal
and a utility-based revision policy. Its final action can retain the
anchor even when a new proposal is present. Historical multi-task
datasets and specialized analysis agents therefore have distinct roles;
neither term is a substitute for the other.

The common economic contract enters LONG at the next session's open,
exits at the third following session's close and charges brokerage and
slippage on both legs. SHORT maps to CASH. Forecasts, policy actions and
future outcomes remain separate records, and paired context branches
reuse the same upstream realization. These choices make the recorded
comparisons inspectable; they do not resolve every inherited causal or
data-provenance limitation.

The contribution lies in the adaptation, context/policy integration and
evaluation described in Chapters 3–5. Chapter 2 attributes the inherited
multi-agent architecture, indicators, HMM/Bayesian foundations and
student–teacher methodology. The two historical studies evaluate this
particular implementation under different response collections and
statistical conventions. The answers below retain that separation and
summarize the already reported results, rather than adding experiments
or treating implementation as evidence of effectiveness.[^conclusion-evidence]

## 6.2. Answers and contributions

The four answers follow the questions introduced in §1.3 and the
observation–answer–remaining-evidence map in Table B09 (§5.9.3). Percentage
point differences below retain the estimators and support specified in
Chapter 5; they are not returns on a validated multi-stock portfolio.

### 6.2.1. RQ1: combined information and controls

**How does the multi-agent system combining price, alpha and sentiment behave relative to its controls?**

The recorded component system shows a classification gain over Base
without a corresponding financial gain. On 102 paired points, Full has
BA of 52.961% versus 49.714%, a +3.247 pp difference; the saved six-block
descriptive interval is [−1.176, 8.125] pp. Both identify only 7 of the
25 UP outcomes. Full's mean net account return is −0.797% versus
−0.750%, giving a −0.047 pp difference. The price-logistic control has
higher BA than Full, and CASH remains at zero return (§5.6.1).

The separate numerical and nine-unit factorial panels answer narrower
questions on their own support (§§5.6.3–5.6.4). They do not establish
an isolated benefit from the language model's factor selector or from
adding alpha and sentiment. Full/Base changes prompt representation
along with information. The supported answer is thus an observed,
representation-dependent classification difference with adverse
financial outcomes, not a general advantage of the combined system.

### 6.2.2. RQ2: historical context and conditional evidence

**How does regime-aware historical context and conditional evidence change outcomes under the same upstream realization?**

The outcome depends on the baseline and on whether contextual evidence
is actually available. Bayesian v1 exceeds Common by +0.327 pp in mean
account return, with saved joint descriptive band [0.067, 0.586] pp.
Against Native its difference is −0.045 pp, with band [−0.362, 0.271] pp
(§5.7.4). These belong to the complete twenty-cell contrast family, not
two independently chosen tests. The shorter-block L1 band for v1 minus
Common crosses zero (§5.8.4). The six exposed folds and dependence
assumptions prevent a confirmatory superiority interpretation.

Conditional branches are sparsely exercised: C2 and B_semantic each
produce only three new Decision replies, while their remaining slots
retain designated fallback (§5.7.2). Primary comparisons include those
slots; covered subsets do not replace them. All eight context research
methods have negative mean net account returns (§5.7.1). The results
therefore support baseline- and readiness-dependent descriptive changes,
without isolating a regime effect or demonstrating profitability.

### 6.2.3. RQ3: factual anchoring, MT inference and utility

**How do Fact Anchor, MT-BICL and the utility policy affect final actions?**

The combined MT path mostly retains the factual anchor. MT-BICL and
Fact Anchor agree on 302 of 306 final-action slots. The recorded
decomposition is 108 bypasses, 189 raw proposals equal to the anchor,
five rejected changes and four accepted changes (§5.8.2). Accepted
changes cover only three unique market points. This explains why a
new hosted reply and a different final action are different events.

The MT-minus-anchor bridge has +0.033 pp mean account-return difference
and +0.433 pp BA difference (§5.7.5), while MT's mean return remains
negative. The bridge changes combined mechanisms and supplies no
isolated student, target-context or utility-policy effect. Missing
Plain_revision, No_target, No_utility and student–teacher interventions
remain missing (§5.9.1). The supported contribution is a traceable
anchor-relative revision path with very limited final-action changes,
not a measured benefit attributable to the student alone.

### 6.2.4. RQ4: temporal, economic and operational evidence

**Which temporal, economic and operational contracts are supported by evidence, and which limitations remain?**

The frozen records support specific engineering contracts: canonical
candidate-LONG labels and cost accounting, shared upstream inputs,
forecast/outcome separation, measured prompt bounds, retry/checkpoint
handling and source-bound offline replay. Each conclusion applies to
the tested historical path and receipt scope (§§5.1, 5.3 and 5.8–5.9).
Reading a saved reply or reproducing an artifact introduces no new
hosted inference and cannot verify future served-model behavior.

The Native row-wise causality gate remains **FAIL** and the whole-system
status remains **NOT_CERTIFIED_HISTORICAL_EXPLORATORY**. Bank/query/news
provenance, independent execution evidence and UI/F11 acceptance remain
unresolved; UI/F11 is **PENDING**. These limits prevent an assertion of
whole-system causal validity, live execution readiness or prospective
profitability. The answer to RQ4 is consequently a scoped inventory of
supported contracts and remaining failures, not overall certification.

Together, the answers distinguish four contributions. System adaptation
is supported by the implemented graph and component records;
historical-context/policy design by the specified mechanisms and traces;
evaluation/reproducibility by the paired accounting and scoped receipts;
and empirical findings by the two bounded historical studies. The
contribution types introduced in §1.5 survive with these limits. None
requires turning a negative result into a trading advantage.

[^conclusion-evidence]: This chapter synthesizes Chapter 5, especially B05a–b, B06a–e, the policy decomposition in §5.8.2 and B09. Evidence ledger §12.3/CL221–CL226 maps the answers to CL145–CL187 and the unchanged archived sources. No fitting, new model calls, resampling or execution replay is introduced.

## 6.3. Limitations

> **Not yet drafted.** Summarize the limitations that materially restrict the final conclusions, cross-checking the shared ledger and discussion. Retain unresolved causality, provenance and application-acceptance qualifications unless later evidence actually resolves them.

## 6.4. Future work

> **Not yet drafted.** Prioritize separately versioned causality/provenance repair, authenticated coverage, chart/news validation, registered matched ablations, prospective evaluation, execution/portfolio modeling and application acceptance. Explain what evidence each step would add; do not describe planned work as completed.
