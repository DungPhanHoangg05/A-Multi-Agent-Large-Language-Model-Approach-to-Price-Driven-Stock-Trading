# Thesis outline

## A. Research direction

**Title:** Regime-Aware Multi-Task Bayesian In-Context Learning for Multi-Agent LLM Stock Trading in the Vietnamese Stock Market.

**Language:** English throughout the thesis manuscript, including front matter, chapters, captions and figure/table labels. User communication, the writing plan, progress checklists and management guidance use Vietnamese.

**Central argument:** begin with a price-driven multi-agent system, construct historical context that is eligible at the decision time and conditioned on market state, introduce that context through Bayesian priors and MT-BICL, and evaluate its effect on forecasts and LONG/CASH actions under a shared economic contract.

The title identifies a research direction, not a demonstrated performance advantage. Explain multi-task learning separately from multi-agent orchestration. Attribute inherited components rather than presenting HMMs, Alpha101, QuantAgent or the referenced student architecture as inventions of this thesis.

### A.1. Objectives and scope

- Explain the implemented system, including price/news inputs, agent reports, historical memory, market regimes, retrieval, student/teacher resources, policy and evaluation.
- Assess the incremental contribution of historical context under shared inputs, upstream reports and trading rules, retaining unsupported cases and unfavorable results.
- Separate engineering adaptation, context/policy design and reproducible evaluation as different types of contribution.
- Focus empirical claims on the recorded daily historical studies. The realtime application is an implementation demonstration, not prospective evidence of profitability.

### A.2. Research questions

| ID | Question | Comparison and evidence | Interpretation boundary |
| --- | --- | --- | --- |
| RQ1 | How does the multi-agent system combining price, alpha and sentiment behave relative to its controls? | Component study: paired Full versus Base on 102 points; recorded numerical controls; separate nine-unit upstream and factorial panels. Report BA/MCC, both-class support, account returns and exposure using the recorded protocol. Sources: component scope/classification/accounts tables and saved panel analyses. | Full/Base changes information and prompt representation together. Panel supports differ; numerical controls do not isolate the LLM factor selector. Higher classification performance does not establish profitability. |
| RQ2 | How does regime-aware historical context and conditional evidence change outcomes under the same upstream realization? | Historical-context study: Bayesian v1, C2, A_tp_pool and B_semantic each versus Common and versus Native on paired support. Use contrasts, prior traces, coverage, recorded example age/similarity and fallback, retaining unsupported points in primary metrics. | Native/Common also changes alpha projection and instructions. Low support limits mechanism attribution. Covered-subset results are secondary; six exposed folds yield descriptive evidence, not confirmation of a regime-specific causal effect. |
| RQ3 | How do Fact Anchor, MT-BICL and the utility policy affect final actions? | Descriptive bridges Common → Fact Anchor → MT-BICL; compare paired final actions/metrics and inspect raw proposals, anchor validity, eligibility, bypasses, vetoes and utility quantiles. Sources: bridge table, prediction records and policy/context traces in the locked study. | These comparisons add combined interventions. Student, task context and utility effects cannot be isolated without unperformed matched ablations. Retain the observed 302/306 MT/anchor final-action agreements. |
| RQ4 | Which temporal, economic and operational contracts are supported by evidence, and which limitations remain? | Compare contract requirements with scoped PIT/causality audits, canonical labels/P&L checks, shared-upstream identities, prompt measurements, retry/checkpoint records and cold-replay receipts. This is a contract-to-evidence audit, not a performance contrast. | Report snapshot and tested path for each check. Outer-cutoff compliance and offline replay do not certify native row-wise causality, live execution, prospective profitability or browser acceptance. |

The two studies use separate response collections and statistical conventions. The historical-context design has 102 market points, 51 stock–fold accounts, three Decision repeats and eight forecast roles. Its 2,448 slots are conditional on one shared upstream realization per point. They are not 2,448 independent market observations. [The evidence ledger](evidence.md#2-phạm-vi-nghiên-cứu-và-ranh-giới-luận-điểm) records the source roles and unresolved evidence boundaries for this scope review.

### A.3. Evidence rules

1. An implemented method does not imply a completed experiment. Every result needs a cohort, protocol, artifact source and applicable acceptance scope.
2. Previously exposed historical folds are exploratory; renaming them does not create an untouched holdout.
3. Keep the component study and the historical-context study separate: responses, supports and statistical conventions differ.
4. Outer-cutoff isolation does not establish row-wise causality. At the planning baseline, native row-wise causality is `FAIL` and whole-system causality is `NOT_CERTIFIED`.
5. Retain fallback and negative outcomes in primary results. Covered-subset analyses are explicitly secondary.

### A.4. Contributions and attribution

| Contribution type | Thesis-specific work to explain and assess | Inherited foundation | Evidence and claim limit |
| --- | --- | --- | --- |
| System adaptation | Integrate price/chart reports, alpha and dated sentiment into a Vietnamese-stock LONG/CASH research pipeline with shared inputs and explicit execution accounting. | QuantAgent-style role specialization, established indicators and adapted Alpha101 formulas. | Explain the actual graph and component contracts; use the component study for observed behavior. Do not claim invention of multi-agent trading or validated execution in the market. |
| Historical-context and policy design | Connect matured episodes and market-state conditioning to bounded Bayesian summaries; implement alternative priors, factual anchoring and MT context with utility-gated action revision. | HMMs, Beta–Bernoulli inference, in-context learning and the referenced student–teacher methodology. | Explain implementation choices and dependencies, then evaluate paired contrasts and policy traces. System integration is distinct from theoretical novelty; primary-publication attribution still requires source verification. |
| Evaluation and reproducibility | Preserve a common economic oracle, immutable paired upstream, distinct proposal/action/outcome records, support/fallback accounting and source/runtime-bound replay. | Standard chronological evaluation, resampling and reproducibility principles. | Use scoped receipts and archived records; keep native causal failures and incomplete data provenance visible. Engineering checks do not prove whole-system validity. |
| Empirical findings | Report the two historical studies, including baseline-dependent differences, sparse context activation, anchor retention and negative mean returns. | Recorded observations and the protocols under which they were collected. | Treat these as bounded descriptive findings. The title does not promise an improvement, and aggregate MT results do not establish a student-specific benefit. |

### A.5. Six-chapter scope and exclusions

| Chapter | Responsibility in the argument | Main RQ connection | Boundary |
| --- | --- | --- | --- |
| 1. Introduction | Define the decision problem, motivation, questions, contribution types and study boundaries. | Introduces RQ1–RQ4. | No assumed performance advantage or completed unobserved experiment. |
| 2. Related Work | Attribute technical analysis, multi-agent finance, regimes, Bayesian/MT context and evaluation methods; establish a source-supported gap. | Positions all four questions. | Existing bibliography entries remain candidates until primary sources are read and checked. |
| 3. Theoretical Background and Problem Formulation | Define time indexing, economic labels, signals, HMM/Bayesian/MT concepts, utility and evaluation principles. | Supplies concepts for RQ1–RQ4, especially RQ4. | A study assumption is not a current exchange rule; probability, confidence and utility remain distinct. |
| 4. Proposed System | Explain the entire implemented path, Native/Common, priors, MT/anchor/policy, orchestration and operational recovery. | Methods for RQ1–RQ3; mechanisms for RQ4. | Explain a method's existence separately from whether its isolated effect was measured. |
| 5. Experiments and Discussion | Separate component and historical-context results, paired contrasts, support, policy traces, robustness and contract evidence. | Answers RQ1–RQ4 within recorded support. | No pooled response study, new model calls, refits or missing ablations introduced to fill writing gaps. |
| 6. Conclusions and Future Work | Answer each RQ, distinguish contribution types and state limitations and needed research. | Consolidates RQ1–RQ4. | No new results; prospective confirmation, native-causality repair, isolated MT ablations and application acceptance remain separate work. |

The empirical scope is daily historical evaluation on the recorded purposive Vietnamese-equity sample. It excludes high-frequency trading, actual short selling, a validated capital-constrained multi-stock portfolio and prospective deployment claims. The realtime 1D application illustrates implementation; it does not extend the financial evidence. The shared study contract remains LONG at `Open(t+1)` to `Close(t+3)`, SHORT mapped to CASH, and fees/slippage on both legs. Primary outcomes retain unsupported/fallback cases and negative results.

## B. Structure adapted from the template

| Part | Thesis content |
| --- | --- |
| Front matter | Outer/inner covers, abstract, acknowledgements, declaration, contents, lists of figures/tables, abbreviations and notation. |
| Chapter 1 | Introduction. |
| Chapter 2 | Related Work. |
| Chapter 3 | Theoretical Background and Problem Formulation. |
| Chapter 4 | Proposed System: Regime-Aware Bayesian Context for Multi-Agent Trading. |
| Chapter 5 | Experiments and Discussion. |
| Chapter 6 | Conclusions and Future Work. |
| Back matter | References only; no appendices in the submission. |

The author has selected the sample's first two pages as the cover presentation, retaining the institution, logo placement, major and place/year while replacing the author, title and supervisor. Confirmed metadata and unresolved requirements are recorded in [the evidence ledger](evidence.md#1-thông-tin-tác-giả-và-yêu-cầu-trình-bày), with English cover text in [front matter](frontmatter.md). The student ID is recorded there; the sample does not print it on either cover.

The sample uses A4, 12-point text, one-and-a-half line spacing, Roman front-matter pagination and Arabic main-text pagination. Outside the selected cover presentation, these remain template observations rather than verified institutional requirements. No official citation/layout policy or submission deadline has been supplied. Any mandatory forms must be confirmed independently. Do not import subject-specific macros, the sample bibliography or its personal metadata.

The working budget is **66 physical PDF pages**, within **60–70 including covers, front matter and references**: front matter 10; Chapters 1–6 respectively 3/5/7/20/15/3; references 3. Retain 12 pt, 1.5 spacing and existing margins. The submission has no appendices and no rotated pages. Evidence archives support traceability without replacing essential method explanations.

The edited draft after T73 has **60 pages**: front matter 10; Chapters 1–6
3/4/6/19/13/2; references 3. The budgets guide emphasis rather than requiring
padding. The scope below can be merged into fewer final subsections; the
LaTeX table of contents gives the current structure. T74–T80 are complete
as an internal review; external review and P10 packaging remain pending.

## C. Detailed chapter outline

### Front matter

- **Outer and inner covers:** institution, title, author, student ID, program, supervisor, place and year. Leave unknown metadata visibly unresolved during drafting.
- **Abstract:** problem, approach, evaluation design, principal findings, limitations and contribution; write after the results are stable.
- **Acknowledgements and declaration:** original text based on actual contributions and required wording.
- **Contents, figure list and table list:** generated from the final source.
- **Abbreviations and notation:** LLM, VLM, ICL, BICL, MT-BICL, HMM, PIT, OHLCV, BRPP, BA, MCC and NAV; distinguish probability, confidence, utility, return and support.

Use the [controlled terminology and notation](evidence.md#5-thuật-ngữ-tiếng-anh-ký-hiệu-và-quy-ước-diễn-đạt) throughout drafting. Resolve Native/Common/Base and overloaded artifact names by study/profile; distinguish displayed-example counts from prior-task counts and percent from percentage points.

### Chapter 1. Introduction

**Purpose:** motivate a precise problem and define the claims to be evaluated. **Budget:** 3–4 pages.

#### 1.1. Context and motivation

- Explain the different information supplied by price histories, technical indicators, chart patterns and financial news.
- Introduce LLM/VLM interpretation and the need to control temporal availability, consistency and operational cost.
- Motivate historical examples and regime conditioning when reports disagree or historical support is sparse.
- Introduce the long-only simulation, execution delay and two-sided costs as study assumptions rather than universal market rules.

#### 1.2. Problem statement

- At decision date `t`, identify admissible prices, regime information, dated sentiment and matured historical episodes.
- Distinguish the LONG/SHORT forecast, the LONG/CASH execution action and the accompanying explanation.
- Separate predicting the candidate-LONG net label from earning a positive account return.

#### 1.3. Objectives and research questions

- Present RQ1–RQ4 and their comparator families.
- State testable questions without assuming that regime conditioning or multi-task inference must help.

#### 1.4. Challenges and boundaries

- Nonstationarity, small dependent samples, missing news and incomplete bank coverage.
- Query-time leakage, noncausal historical rows, bank/query provenance and Native/Common differences.
- LLM variability, prompt/API limits, fallback and external policy decisions.
- Daily sampled historical evaluation, distinct from high-frequency trading or a deployed portfolio.

#### 1.5. Contributions and thesis organization

- Separate inherited components, system-specific extensions and evaluation infrastructure.
- Describe empirical contributions at the strength supported by the results, including negative findings.
- Explain how the remaining chapters build the argument.

**Planned material:** problem input/output illustration; question–method–evidence table.

### Chapter 2. Related Work

**Purpose:** establish the intellectual context and identify what is inherited, adapted and evaluated. **Budget:** 4–5 pages.

#### 2.1. Technical analysis and quantitative stock prediction

- Price/volume indicators, alpha factors and statistical or machine-learning controls.
- Alpha101 and the limitations of translating cross-sectional formulas into single-asset time-series operations.
- In-sample selection diagnostics versus out-of-sample investment performance.

#### 2.2. LLMs, VLMs and multi-agent financial systems

- Role specialization, shared state, report synthesis and visual inputs.
- QuantAgent inheritance and the implementation changes made for this system.
- Limits of chart grounding, fluent explanations and hosted-model reproducibility.

#### 2.3. Market regime detection

- Hidden Markov models and trend/volatility alternatives.
- Training cutoffs, frozen fits and inference using only the available prefix.
- Regimes as retrieval conditions, not guaranteed profitable trading signals.

#### 2.4. In-context learning and Bayesian historical context

- Few-shot prompting and example retrieval versus updating LLM weights.
- Priors, posteriors and finite historical evidence.
- Separate interventions for examples, summary statistics and task-based context.

#### 2.5. Multi-task Bayesian ICL and student–teacher methods

- Prior tasks, target observations and query inference across tasks.
- Teacher targets, student training and frozen inference resources.
- Identify the source method and actual implementation differences; multiple examples alone do not establish MT-BICL.

#### 2.6. Evaluation of trading systems using LLMs

- Walk-forward evaluation, purging overlapping labels, transaction costs and paired comparisons.
- Ablations, numerical controls, dependent-data inference and reproducibility.
- Exploratory historical analyses versus prospective confirmation.

#### 2.7. Research gap and position of the thesis

- Comparison matrix: inputs, architecture, historical context, regimes, PIT protections, execution contract and controls.
- Explain the problem directly addressed and the questions that remain open.

**Source requirement:** read and verify primary publications before filling the comparison matrix. The existing bibliography is a discovery aid, not proof that a source supports a new claim.

### Chapter 3. Theoretical Background and Problem Formulation

**Purpose:** supply the concepts and notation needed to understand the method without repository knowledge. **Budget:** 6–7 pages.

#### 3.1. Observations and time indexing

- Define OHLCV, an observed trading session, decision cutoff `t`, chart windows and factor history.
- Map to engine indices: window `[e-W,e)`, decision `t=e-1`, entry `e`, exit `e-1+L`, with `L=3` in the study.
- Distinguish observed sessions from calendar arithmetic, missing records and warm-up periods.

#### 3.2. Economic contract and prediction target

- LONG buys at `Open(t+1)` and exits at `Close(t+3)`; SHORT maps to CASH rather than a short sale.
- Preserve the formula implemented by `compute_round_trip_net_return`, with fee `f=0.0025` and slippage `s=0.001` on each leg:

$$
r^{net}_t=\frac{C_{t+3}}{O_{t+1}}
\frac{(1-s)(1-f)}{(1+s)(1+f)}-1.
$$

- UP means `r_net > 0`; DOWN means `r_net <= 0`, including zero.
- Explain why candidate-LONG labels and realized LONG/CASH account returns differ.
- The approximate 0.70% round-trip cost does not replace the multiplicative formula. Apply the same economic oracle to new historical labels; disclose discrepancies in frozen legacy evidence without rewriting it.

#### 3.3. Technical, alpha and sentiment signals

- Introduce MACD, RSI, Stochastic, Williams %R and ROC before their report rules.
- Explain alpha factors, normalization, IC orientation and selection; distinguish native and causal-common constructions.
- Treat sentiment as a separate dated contextual input with explicit missingness.
- Heuristic votes and reported confidence are not automatically calibrated probabilities.

#### 3.4. Hidden Markov models for market regimes

- States, emissions, transition matrix, fitting and endpoint inference.
- Current VN-Index features: log return, 20-session volatility and distances from MA20/50/200.
- State interpretation, fit quality, fallback and time-appropriate model/scaler freezing.

#### 3.5. Bayesian summaries of historical evidence

- Beta–Bernoulli counts, posterior mean and credible intervals.
- Conditional evidence and shrinkage from a disjoint background without counting an episode twice.
- Statistical population size versus the number `K` of displayed examples.
- Plug-in historical intervals versus calibrated query probabilities or return forecasts.

#### 3.6. Multi-task context and utility

- Prior tasks, matured target-task observations and the unlabeled query.
- Teacher, numerical student, feature/scaler definitions and factual buckets.
- Why `P(y=1)` is different from expected net return; include gain/loss magnitudes.
- The anchor action, a proposed revision and uncertainty in its utility difference.

#### 3.7. Temporal validity and evaluation principles

- Prices dated at or before `t`; news with valid availability timestamps; exclude undated news and explain protocol-specific conservative availability.
- Historical observations with `exit_date < t`; reserved evaluation IDs excluded from context.
- Purged chronological partitions; outer cutoff versus row-wise causality.
- Shared upstream paired comparisons; Decision repeats do not increase independent market sample size.
- Classification, account, exposure and drawdown measures, with explicit undefined-denominator rules.

**Planned material:** decision/entry/exit timeline; chronological partition diagram; notation table; a clearly labeled illustrative posterior calculation.

### Chapter 4. Proposed System: Regime-Aware Bayesian Context for Multi-Agent Trading

**Purpose:** let a lecturer reconstruct how the complete system works from the chapter alone. **Budget:** 19–21 pages.

**Explanatory pattern for every component:** motivation → plain-English intuition → inputs available at the cutoff → processing → outputs → downstream consumer → failure/fallback → implementation/source evidence. Introduce each symbol before its equation and each acronym before its repeated use. File inventories belong in the companion evidence record, not in place of an explanation.

#### 4.1. System overview and one-decision walkthrough

- Introduce the system in plain English before presenting detailed equations or variant IDs.
- Trace one stock/date through admissible data, shared reports, optional context, a proposed decision, policy resolution and later evaluation.
- Distinguish deterministic computation, hosted inference, offline training and post-decision evaluation in the architecture figure.
- Reuse this example throughout the chapter. Archived evidence must carry source IDs; synthetic numbers must be explicitly illustrative and never presented as measured results.

#### 4.2. Input preparation and shared state

- Explain OHLCV/VN-Index/news sources, chart and factor windows, time boundaries, missing values and snapshot identity.
- Describe the data supplied to each component in an input/output contract table.
- Keep forecast inputs separate from query outcomes; explain serialization and provenance only to the extent needed for reproducibility.

#### 4.3. The base multi-agent pipeline

- **4.3.1. Indicator:** deterministic indicator computation, priority rules, votes and missing-value behavior.
- **4.3.2. Pattern:** candlestick image construction, requested visual evidence, report fields and limits of consistency checks.
- **4.3.3. Trend:** support/resistance construction, separate chart input, report fields and geometric versus semantic correctness.
- **4.3.4. Alpha:** candidate transformations, orientation/ranking and selected report; disclose in-sample diagnostics and native causality limitations.
- **4.3.5. Sentiment:** dated articles or frozen aggregates, scoring provenance, aggregation, coverage and missingness; explain its relationship to Alpha.
- **4.3.6. Decision:** condensed reports, intended evidence priorities, structured LONG/SHORT output and LONG/CASH mapping. Role names do not imply one hosted call per role.

#### 4.4. Native and Common foundations

- Explain what remains shared and what changes in the causal-common alpha projection and common prompt.
- Identify inherited versus adapted behavior and frozen selector fitting.
- Explain why Native/Common is a bridge between profiles, while Full/Base is a different intervention in a separate study.

#### 4.5. Historical memory and market regimes

- Episode fields, decision/entry/exit dates, agent signals, regimes, outcomes and provenance.
- Label construction, maturity filtering, reserved evaluation IDs and bank versioning.
- HMM/scaler fitting and regime assignment at the query cutoff.
- Distinguish the Bayesian signal bank from MT-BICL numerical task context rather than assuming a single interchangeable memory.

#### 4.6. Bayesian Prior v1

- Explain the motivation for retrieving comparable matured same-stock episodes.
- Specify PIT filtering before outcome-based statistics, regime/signal matching, distance, ranking, tie-breaking and up to `K=3` examples using the evaluated protocol.
- Show an annotated BRPP and how it joins the condensed reports.
- Explain exact reuse of Common for unsupported cases, including the recorded reason and repeat identity.

#### 4.7. Conditional and alternative priors

- **C2:** conditional/background populations, Beta shrinkage and separate readiness for statistics and examples.
- **A_tp_pool:** Trend/Pattern matching and the support/specificity tradeoff.
- **B_semantic:** explicit counts, intervals and example identities. Its name alone does not imply embedding-based search.
- Compare filtering, summaries, examples, prompt content and fallback in one table.

#### 4.8. MT-BICL and action revision

- **4.8.1. Fact packet and Fact Anchor:** factual assertions, the Common dependency and invalid-anchor behavior.
- **4.8.2. Task construction:** factual bucket, prior tasks, target observations, query vector and membership cutoffs.
- **4.8.3. Teacher and student:** actual architecture, training targets, loss and checkpoint selection from the locked implementation; separate training from inference.
- **4.8.4. Utility:** posterior sampling, gain/loss support, mean/quantiles and insufficient-evidence conditions.
- **4.8.5. Context projection:** summaries over complete membership, representative examples, numeric estimates and prompt limits.
- **4.8.6. External policy:** retain the anchor when ineligible or factually invalid; accept a different action only when `Q10(ΔU)>0`. CASH→LONG uses `Q10(U)`; LONG→CASH uses `-Q90(U)`.
- **4.8.7. Traceability:** distinguish raw proposal, anchor, bypass, veto reason and final action. Explain which changes come from the LLM and which are imposed by policy.

#### 4.9. Variant orchestration and complete algorithms

| Research role | Implementation ID | Main dependency/resource |
| --- | --- | --- |
| Native | `original_fix` | Native alpha projection and prompt. |
| Common | `original_common` | Causal-common alpha and shared instruction family. |
| Bayesian prior | `bayesian_v1` | Common; signal bank and regime. |
| Conditional prior | `C2` | Common; conditional statistics/readiness. |
| Trend–pattern prior | `A_tp_pool` | Common; relaxed Trend/Pattern pooling. |
| Explicit-count prior | `B_semantic` | Common; explicit evidence presentation. |
| Fact anchor | `Fact_Anchor` | Common; facts and assertion validation. |
| MT-BICL | `MT_BICL` | Common and Fact Anchor; task context, student and utility. |

- Run upstream once per point/realization and deep-copy the shared parent to all branches.
- Resolve dependencies once per repeat; distinguish eight research roles, UI choices, forecast slots and actual calls.
- Use one combined algorithm for PIT preparation, same-repeat method/policy execution, durable forecasting and later label/account evaluation.

#### 4.10. Prompt limits, recovery and application

- Explain distillation/capping, BRPP at most 600 characters for `K=3`, and Decision prompts strictly below 6,500 characters. Characters are not tokens.
- Describe the audited retry wrapper, backoff/retry-after, schema repair, checkpoint persistence, resume and UNKNOWN reconciliation.
- Distinguish valid support-based fallback from a technical error; an error must not silently become a valid CASH forecast.
- Explain the Flask realtime 1D workflow, model selection, agent progress, BICL report, final decision, stored comparisons and exports.
- Keep bilingual presentation separate from canonical actions. Screenshots need version/source context; browser acceptance remains pending at the planning baseline.
- Finish by revisiting the initial example from inputs to final action, then explain when its outcome becomes available for evaluation.

**Retained material:** overview architecture, compact component contract, one running example, observed-session timeline, MT training/inference diagram, action-policy diagram and variant comparison. Retrieval/regime/dependency logic is explained in formulas and prose instead of repeating diagrams. One combined algorithm replaces the three earlier blocks. The original Pattern/Trend image pair has readable external annotations; UI acceptance remains pending and no screenshot substitutes for scientific evidence.

### Chapter 5. Experiments and Discussion

**Purpose:** answer RQ1–RQ4 using identifiable evidence. **Budget:** 14–16 pages.

#### 5.1. Studies and evidence scope

- Separate the base-system component study from the unified historical-context study.
- State freeze/protocol boundaries, historical exposure and the distinction between completed evidence and proposed analyses.

#### 5.2. Data and evaluation support

- Nine stocks: FPT, CMG, VCB, MBB, MWG, VNM, BHN, HVN and VJC; price, VN-Index and sentiment provenance.
- Six temporal blocks, twelve selected dates, 102 eligible points and 51 stock–fold accounts; document exclusions and warm-up.
- A prior bank of 852 examples covering FPT/MWG/VCB/VNM, with explicit policy for other stocks.
- Missing sentiment at 79/102 historical-context points; missing is not an observed neutral sentiment value.
- Training/validation/test partitions, 45-bar chart windows and longer alpha prefixes. Twelve selected dates do not constitute a continuous daily multi-year backtest.

#### 5.3. Configuration and paired protocol

- Use the recorded study runtime, model aliases/options, fingerprints and source/data/model pins; do not substitute current live settings.
- One upstream per point, three Decision repeats and eight roles yield `102 × 3 × 8 = 2,448` historical-context forecast slots.
- Separate market observations, slots, active responses, fallback, HTTP attempts and retired records.

#### 5.4. Comparators and interventions

- Component study: Full/Base, recorded numerical controls and their actual supports.
- Historical-context study: five extensions versus Native and versus Common, plus bridge contrasts and economic controls.
- Base omits alpha/sentiment; Common retains them under a different profile. Always-LONG cycles differ from continuous hold.
- Component factorial/placebo/upstream panels do not constitute completed MT-BICL ablations.

#### 5.5. Metrics and statistical analysis

- BA, MCC, accuracy, class precision/recall, confusion and LONG rate; preserve undefined values and denominators.
- Account returns, costs, turnover, exposure, NAV and drawdown; separate account averages from a pooled portfolio.
- Preserve each study's averaging order, Sharpe/Sortino definitions and frequency conventions; do not annualize irregular schedules inappropriately.
- Paired block/fold bootstrap, contrast families, simultaneous descriptive bands and sensitivity analyses.
- The six exposed folds support descriptive/sensitivity interpretation, not confirmed statistical significance, power or calibrated coverage.

#### 5.6. Component-study results

- Main comparisons, numerical controls, stock/block patterns and accuracy–return differences.
- Completed alpha/sentiment/placebo panels and upstream variation with their own supports.
- Prompt format/length confounding and native row-wise causality; answer RQ1 within the evidence available.

#### 5.7. Historical-context results

- All eight roles and two economic controls: return/BA, support, raw calls, fallback and repeat dispersion.
- Contrast families versus Native and Common; secondary fold, stock and bank-covered analyses.
- Existing reference values: mean account return is approximately −0.653% for Native, −1.025% for Common, −0.698% for Bayesian v1 and −1.253% for MT-BICL. All eight research roles have negative mean returns.
- Bayesian v1 improves on Common within the recorded descriptive band but does not establish superiority over Native. Import exact values from artifacts when drafting the final tables.

#### 5.8. Mechanisms, case studies and robustness

- Support/readiness, example age/similarity, regimes and fallback by method.
- Common → Fact Anchor → MT-BICL, with raw proposals versus policy outcomes. Existing evidence records identical MT/anchor final actions in 302/306 slots.
- C2 and B_semantic each have three new raw Decision responses; A_tp_pool has 24. Interpret aggregate outcomes with this fallback coverage visible.
- Select cases by a declared rule: context used, insufficient support, conflicting reports, policy veto and an incorrect decision. Avoid selecting only profitable cases.
- Recorded costs/usage/latency, execution sensitivities and missing fields; do not conflate UI demonstrations with financial validation.

#### 5.9. Unperformed ablations and threats to validity

- Mark retrieval-only, statistics-only, no-prior, no-target, no-utility and student/policy separation as unperformed where no unified-study results exist.
- Discuss native causality, input authentication, bank/query provenance, narrow bank coverage, correlated small samples, historical exposure and possible model-training contamination.
- Disclose purposive stock selection, unresolved market membership, corporate actions and execution assumptions.
- Preserve the audit finding of numerical bank/query return differences in 828/852 records; this is not a count of changed labels.
- End with an RQ–observation–supported conclusion–remaining evidence table.

**Required material:** data/split tables, configuration/support table, separate result panels, contrast bands, bridge/policy analysis, coverage/fallback, traceable cases and costs/audit summary. Do not construct a continuous equity curve by splicing independent accounts.

### Chapter 6. Conclusions and Future Work

**Purpose:** conclude at the strength supported by the work. **Budget:** 2–3 pages.

#### 6.1. Summary of the approach

- Reconnect multi-agent reports, regime/Bayesian context, MT-BICL, policy and the shared evaluator.
- Distinguish inherited methods from system-specific work.

#### 6.2. Answers and contributions

- Answer RQ1–RQ4 with references to results and audits.
- Separate reproducible engineering outcomes from limited empirical findings.
- Avoid a blanket improvement claim when conclusions depend on baseline, support and policy.

#### 6.3. Limitations

- Summarize the limitations that materially restrict conclusions.
- Retain unresolved causality and application-acceptance qualifications if they still apply at manuscript freeze.

#### 6.4. Future work

- Repair and test native row-wise causality; reconcile source/label provenance in a separately versioned study.
- Expand authenticated historical coverage and financial-news/chart-grounding validation.
- Conduct registered ablations separating retrieval, statistics, task context, student and utility.
- Design a prospective study with appropriate precision/power and independently regenerated upstream realizations.
- Improve venue-specific execution and portfolio capital modeling; complete application acceptance.

### References

- Build a thesis-specific bibliography from primary research and official methodological/data documentation.
- Verify author/year/DOI/URL and the claim supported by each citation.
- Attribute inherited methods, adapted code and figures accurately. Internal receipts establish provenance, not the scholarly origin of a method.
- Verify any market-rule claim against a source applicable to the study period; a backtest assumption does not establish current law.

### Submission boundary and archived evidence

No appendices are included in the submission or build package. Transfer essential temporal contracts to Chapter 3; schemas, prompts, configurations and recovery logic to Chapter 4; results, uncertainty, audit findings and reproducibility limits to Chapter 5. Full prompts, extended result matrices, commands and hashes remain traceable in the external evidence repository and Git history. The editing map is maintained in the shared evidence ledger, Section 15.

## D. Implementation and evidence map

This is a writing aid, not the final scholarly bibliography. Current paths identify components; experimental claims must refer to the corresponding frozen source/runtime.

| Topic | Sources | Check when drafting |
| --- | --- | --- |
| Template | [LaTeX main](../Latex/main.tex), [preamble](../Latex/preamble.tex), [sample PDF](../23020332_Tran_Xuan_Bao.pdf) | Structure/presentation only; replace metadata and subject content. |
| Scope | [project plan](../docs/plan/plan.md), [integration record](../docs/plan/week12/README.md) | Current state versus historical receipts and pending work. |
| Agents | [graph](../utils/graph_setup.py), [state](../agents/agent_state.py), [Indicator](../agents/indicator_agent.py), [Pattern](../agents/pattern_agent.py), [Trend](../agents/trend_agent.py), [Alpha](../agents/alpha_agent.py), [Sentiment](../agents/sentiment_agent.py), [Decision](../agents/decision_agent.py) | Actual profile, deterministic/LLM boundary and prompt. |
| Economics | [engine](../core/backtest_engine.py), [target contract](../utils/target_contract.py), [MT accounting](../core/mt_bicl_accounting.py) | Oracle, indices, costs, ledger and frequency. |
| Regime and memory | [regime detector](../core/regime_detector.py), [memory](../core/bayesian_memory.py), [retriever](../core/bayesian_retriever.py), [historical outcomes](../core/historical_outcomes.py) | Fit/query/episode cutoffs and provenance. |
| Conditional priors | [statistics](../core/prior_conditional_statistics.py), [selection](../core/prior_example_selection.py), [readiness](../core/prior_quality_gate.py), [A/B prior](../core/improvement_prior.py) | Disjoint populations, support and fallback. |
| MT-BICL | [tasks](../core/mt_bicl_tasks.py), [teacher](../core/mt_bicl_teacher.py), [student](../core/mt_bicl_student.py), [replica student](../core/mt_bicl_replica_student.py), [context](../core/mt_bicl_context.py), [utility](../core/mt_bicl_utility.py), [policy](../core/mt_bicl_policy.py) | Evaluated architecture/checkpoint, context and action conditions. |
| Paired execution | [registry](../core/variant_registry.py), [bridge](../core/causal_bridge.py), [adapters](../core/unified_methods.py), [protocol](../core/unified_protocol.py) | Native/Common, immutable parent and per-repeat dependencies. |
| Component study | [setup](../paper/content/experimental_setup.tex), [tables](../paper/content/tables/component/), [results](../paper/content/results.tex) | Separate main/upstream/factorial supports and conventions. |
| Historical-context study | [tables](../paper/content/tables/historical_context/), [acceptance](../docs/plan/week12/unified_analysis_acceptance.json), [results archive](../docs/plan/week12/unified_analysis_results.zip), [analysis](../core/unified_analysis/analysis.py) | Observation/account/repeat units, contrasts and descriptive bands. |
| Evidence restoration | [evidence map](../docs/plan/week12/final_evidence_map.md), [table sources](../core/manuscript_u09/sources.py), [recorded limitations](../paper/content/limitations.tex) | Trace each value; do not substitute live source for frozen source. |
| Application | [entrypoint](../web_interface.py), [serving contract](../docs/plan/week12/variant_serving_contract.md), [live service](../core/serving_live/service.py), [viewer](../utils/research_view.py) | Realtime 1D, recorded results and actual acceptance status. |
| Contract checks | [paired](../tests/test_paired_protocol.py), [retrieval leakage](../tests/test_bayesian_retriever_leakage.py), [regime leakage](../tests/test_regime_leakage.py), [prompt budget](../tests/test_backtest_token_budget.py), [MT tasks leakage](../tests/test_mt_bicl_tasks_leakage.py) | Test existence is not a test execution on a particular snapshot. |

## E. Writing and review

Use the [figure, table and algorithm catalogue](evidence.md#6-danh-mục-hình-bảng-và-thuật-toán-có-nguồn) to track each item's message, chapter, responsible writing task, source type and provenance. Working titles and proposed output paths do not establish that an artifact has been produced or visually verified; final numbering is generated in LaTeX.

Use [EX01 and its selection/source record](evidence.md#7-ví-dụ-xuyên-suốt-có-truy-vết) for the running example: FPT at the 3 July 2023 cutoff, upstream realization 0 and Decision repeat 0. Introduce the available inputs and historical context before revealing the subsequent outcome at the end of Chapter 4; Chapter 5 assesses the complete cohort. Preserve the separate v1 and MT regime sources, bypasses and unchanged anchor action; this case contains no veto. Its negative net outcome is part of the example, not an estimate of comparative performance.

Follow the [writing plan](plan.md) and maintain task status in the [project checklist](plan.md#21-một-nguồn-trạng-thái-công-việc). Draft the contracts and methods and keep the reduced LaTeX manuscript as the single submission source. Preserve RQ1–RQ4, adverse results and validity limits while removing repetition. Review the rendered document before handover. The plan and checklist remain in Vietnamese for project management.

Keep task IDs, weekly progress and incident history out of the thesis body. They remain planning/provenance aids only.
