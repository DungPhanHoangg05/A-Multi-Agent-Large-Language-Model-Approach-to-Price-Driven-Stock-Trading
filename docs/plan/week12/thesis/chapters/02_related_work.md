# Chapter 2. Related Work

> **Draft status: complete chapter draft.** The literature synthesis and comparison matrix use scoped, version-checked primary sources. Cross-chapter review and final typesetting remain pending.
> Only sources admitted to the thesis bibliography support citations here. Unread discovery candidates remain separate in the reading register.

Writing aids: [chapter outline](../outline.md#chapter-2-related-work), [reading register](../evidence.md#4-danh-sách-đọc-nguồn-gốc-và-quy-ước-khóa-trích-dẫn) and [shared evidence ledger](../evidence.md#8-khung-bản-thảo-và-đối-soát-luận-điểm).

## 2.1. Technical analysis and quantitative stock prediction

Technical analysis turns price and volume histories into hypotheses about
future behavior. For a computational study, the useful distinction is
between an observable feature, a decision rule built from that feature and
evidence that the rule remains useful outside its development sample.
Lo, Mamaysky and Wang formalize chart-pattern recognition and compare
conditional with unconditional return distributions. Their work provides
an empirical way to study patterns that might otherwise be identified
subjectively. It does not establish that every familiar indicator, visual
interpretation or market adaptation is profitable. [@lo2000technical]

The present system uses indicators and rendered charts as complementary
representations of an admissible price prefix. Indicator rules, chart
interpretation and the final action are separate stages. An RSI category
or MACD relationship is therefore an input to analysis, rather than the
future label itself. Chapter 3 defines the implemented indicators;
Chapter 4 explains how their reports are produced and shortened before
the Decision request. This distinction matters because an interpretation
can change through the reporting interface even when the underlying
price feature has not changed.[^technical-implementation]

Formulaic alphas offer another way to construct features systematically.
Kakushadze publishes a library of explicit expressions and defines its
operators. In particular, cross-sectional `rank` and group neutralization
operate across securities, whereas temporal operators operate over a
security's history. A single-security implementation cannot silently
replace the former with the latter and still claim mathematical identity.
The source also distinguishes volume-weighted price inputs from ordinary
OHLC values. [@kakushadze2016formulaic]

This thesis accordingly treats its adapted formula library and five
system-specific factors as an implementation family with its own
definitions. A typical-price proxy is not authenticated intraday VWAP,
and a temporal-rank adaptation is not the original cross-sectional rank.
The native and Common alpha paths additionally differ in normalization,
orientation, selection and report projection. The source attribution
belongs to the formula library, while the consequences of those choices
must be evaluated using the actual implementation. Merely adding more
candidate formulas does not establish new independent information or a
causal improvement in trading.[^technical-implementation]

Quantitative controls help locate where the agent system adds behavior.
A constant action reveals class imbalance and cash exposure; a momentum
rule supplies a simple directional heuristic; logistic controls test
whether an ordinary supervised classifier can use price or matched market
features. Scikit-learn supplies a common software environment for such
models, but its general library description does not determine the
fitting recipe or hyperparameters of this study. Those are specified
from the locked artifacts in Chapter 5. [@pedregosa2011sklearn]

Feature selection also belongs inside the evaluated procedure. Varma and
Simon show how optimizing a classifier on a cross-validation score and
then reporting that same score can bias error estimation; their
experiments concern classification rather than financial time-series
purging. The relevant lesson here is to distinguish a selection diagnostic
from an independent performance assessment. The numerical factor-control
panel likewise evaluates its own fixed, train-ranked and random rules;
it is not an isolated experiment on an LLM selector. [@varma2006bias]

Finally, an indicator or classifier predicts the thesis's specified net
candidate-LONG label, while the executed action selects LONG or CASH.
The entry/exit schedule, two-way costs and account aggregation determine
the economic outcome. A classification improvement can therefore coexist
with a lower mean return. Related work motivates feature and control
choices; the separate component results in Section 5.6 determine what
was actually observed under this contract.

[^technical-implementation]: Thesis implementation evidence CL009–CL010 and CL043–CL047; frozen source cards SYS03/SYS10/SYS11/BG03, with the alpha registry and native/Common differences in Sections 3.3 and 4.3.4. These internal bindings establish the implemented adaptations, not the original paper's trading performance.

## 2.2. LLMs, VLMs and multi-agent financial systems

Financial agent systems can assign different inputs and responsibilities
to separate model calls, then combine their reports through shared state
or dialogue. This architecture makes intermediate decisions inspectable,
but the number of roles alone says little about predictive value. The
important comparisons concern which information each role receives, how
reports are combined and which actions and costs the evaluator records.

QuantAgent is the direct architectural predecessor of this system.
Xiong et al.'s version 3 uses price-derived inputs with Indicator, Pattern,
Trend and Risk roles; its method section separately describes the final
DecisionAgent. Numerical indicators, candlestick interpretation and
trendline views contribute complementary reports. The paper evaluates
one-hour and four-hour bar benchmarks and predicts short-horizon
direction. Its RiskAgent introduces stop-loss/take-profit boundaries,
whereas its DecisionAgent produces the directional recommendation.
Those responsibilities should be attributed according to the source
rather than inferred from the names used in this repository.
[@xiong2025quantagent]

The implementation inheritance is also concrete: state/agent contracts,
chart tools, parts of the LangGraph orchestration and web interface are
adapted from the upstream source. The comparison snapshot is commit
`92519f806286192345e940e7ab77496462d662b7`; the originally adopted commit
was not recorded. This distinction is retained in the repository's
[third-party notices](../../../../../THIRD_PARTY_NOTICES.md). The current upstream
name QuantHarness does not change the versioned QuantAgent paper used
for methodological attribution. [@yresearch2026quantagentcode]

Relative to that foundation, this thesis adds Vietnamese-market data and
sentiment handling, an alpha representation/selection path, distinct
Native/Common profiles, historical-context methods, numerical MT context
and an anchor-relative policy. It evaluates daily LONG/CASH outcomes with
a fixed three-session net economic oracle. A predicted risk–reward ratio
or price level in an explanation does not replace that evaluator with
live stop-loss/take-profit orders. The inherited visual specialists and
multi-agent structure are therefore part of the starting point; the
integration and source-bound comparisons define the work evaluated here.
Neither the upstream title nor its reported results establish high-frequency
execution performance for this daily study.[^agent-inheritance]

TradingAgents explores a different organization inspired by a trading
firm. Fundamental, sentiment, news and technical analysis feed research
debate, trading and risk-management teams, with structured communication
alongside natural-language interactions. Its stated simulation uses
historical US technology stocks and buy/sell/hold recommendations. This
provides a useful comparison for role specialization and communication,
but does not supply the same input profiles, temporal protections or
LONG/CASH economic contract as the present experiments. Its own reported
performance is not a head-to-head benchmark result for this thesis.
[@tradingagents2024]

FinVision combines news summaries and visual technical analysis with
textual and visual reflection before producing a trading recommendation.
Its reflection module makes past signals and outcomes an explicit source
of feedback. This is related to the use of history, but a reflection
report does not by itself specify a Bayesian generative model, a posterior
update or a numerical multi-task learner. These mechanisms should be
compared at the level of the information retained and the decision rule
applied. [@fatemi2024finvision]

Two additional distinctions concern the input modalities. ChartLlama
studies chart instruction data and tasks such as question answering,
description and extraction; it illustrates that chart understanding has
its own evaluation problem. Such capability evidence does not establish
correct candlestick reasoning or profitable actions in a different model.
This system does not use ChartLlama's weights. [@han2023chartllama]
For Vietnamese sentiment, ViSoBERT supplies a social-media language-model
backbone, while the pinned 5CD resource supplies the downstream
three-label classifier. Their source domains and resources are distinct;
neither their reported task scores nor fluent agent explanations validate
the study's news availability, financial sentiment accuracy or probability
calibration. Missing news therefore remains visible in the method and
results. [@nguyen2023visobert] [@hf5cdsentiment]

[^agent-inheritance]: Internal attribution and implemented differences: THIRD_PARTY_NOTICES, CL025–CL028, CL039–CL050 and Chapters 4–5. The comparison pin is evidence of the source comparison, not a recovered adoption date or an immutable hosted-model version. Native row-wise causality and application acceptance retain the limitations reported in Section 5.9.

## 2.3. Market regime detection

A regime model represents changes in the data-generating process through
state-dependent behavior. Hamilton describes economic regime-switching
models in which a latent state changes according to transition
probabilities. This provides a way to model persistent changes without
equating a manually drawn trend category with an observed economic truth.
The selected source here is the dated 2005 author manuscript.
[@hamilton2005regimes]

Rabiner's HMM tutorial separates the transition model, observation
likelihoods and the problems of evaluation, state inference and parameter
estimation. Its forward and backward constructions also clarify why the
information set matters: a historical state's inference can incorporate
later observations when smoothing over a complete sequence. Fitting a
model and inferring a state are different operations. In a trading study,
both the model/scaler fitting period and the observations supplied at
inference must therefore be identified. [@rabiner1989hmm]

The implementation uses frozen resources and a VN-Index feature prefix
for numerical regime inference. Other descriptive categories in the
study use price/SMA thresholds or train-relative volatility/liquidity
proxies. These are alternative definitions with different purposes and
should not be treated as interchangeable labels. The signal-bank regime
and numerical MT regime likewise retain separate source identities and
can disagree for the same query.[^regime-related-implementation]

A regime can condition a historical candidate set or affect task ranking
without directly determining an action. Whether this conditioning improves
prediction is a separate empirical question requiring matched alternatives.
For example, changing the bank, similarity representation and support gate
at the same time would not isolate a regime effect. The HMM literature
motivates a representation of nonstationarity; it does not establish that
the named regimes are stable, that a fitted state is a tradable signal or
that the system has overcome its documented native causality limitation.

[^regime-related-implementation]: CL012–CL013/CL061–CL063 and Section 4.5.4 bind numerical HMM/scaler resources and endpoint inference; CL165/CL177 distinguish signal-bank regimes and descriptive component strata. No HMM or scaler is refitted in the writing process.

## 2.4. In-context learning and Bayesian historical context

In-context learning conditions a fixed predictor on a context at inference,
whereas training changes the predictor's parameters. A new prompt can
alter a hosted LLM's response without performing a weight update. This
operational distinction does not specify which learning or inference
algorithm, if any, the model has implemented internally.

Xie et al. analyze an implicit Bayesian explanation under a pretraining
distribution built from a mixture of HMMs. A shared latent concept supplies
the connection between examples, and the theoretical result depends on
explicit assumptions about that distribution and distinguishability.
Their synthetic GINC experiments help study the phenomenon in a controlled
setting. This is an explanation with a specified model, rather than a
certificate that any financial prompt performs Bayesian inference. The
HMM in this account concerns document generation and is distinct from a
VN-Index regime detector. [@xie2022implicitbayes]

Retrieval addresses which examples enter the context. Rubin, Herzig and
Berant train a dense prompt retriever using supervision derived from a
language model's conditional output probabilities, evaluated on semantic
parsing. This shows that example choice can be an explicit learned
component. It does not make every similarity heuristic a learned dense
retriever, nor does selecting similar examples establish a Bayesian
posterior. The implementation named B_semantic in this thesis has its
own documented selector and rendering contract; its name does not imply
Rubin et al.'s architecture. [@rubin2022retrieve]

Historical context in the present system takes several forms. Bayesian
v1 presents selected signal episodes and population-level empirical rates;
the name does not turn those rates into Beta-posterior means. C2 introduces
specified count-based Beta summaries and readiness checks, while A_tp_pool
and B_semantic change the evidence construction or representation. These
counts, rendered examples and numerical task datasets have different
denominators and roles. Their admissibility additionally requires matured
historical outcomes and explicit missing-support behavior.
[^historical-context-implementation]

Accordingly, a favorable context/no-context result would still require
care in interpretation. It could reflect additional information, a
different representation, prompt length or which queries reached the
active branch. Separating examples, statistics, regime conditions and
fallbacks makes such questions testable. Chapter 5 reports the actual
coverage and marks the matched interventions that remain unperformed;
the Bayesian interpretation is not used as a substitute for those tests.

[^historical-context-implementation]: CL064–CL075 and Sections 4.6–4.7 specify v1 empirical populations, C2 plug-in Beta summaries, A/B selection/rendering and same-repeat Common fallback. CL163–CL165 bind observed readiness and descriptor availability. These are implementation statements, separate from claims about the cited ICL theories.

## 2.5. Multi-task Bayesian ICL and student–teacher methods

Prior-Data Fitted Networks make a Bayesian objective explicit at training
time. Müller et al. repeatedly sample supervised datasets from a specified
prior and train a predictor with a prior-data negative log-likelihood.
The resulting network approximates a posterior predictive mapping from
context to query distributions in a forward pass. The ability to sample
the training prior is central to that construction. This is a trained
numerical inference method, and its guarantees or approximation behavior
do not automatically transfer to an arbitrary pretrained language model.
[@muller2022transformers]

Zhu, Oermann and Cho extend the context to multiple datasets that inform
a shared prior, followed by observations from a target task and an
unlabeled target query. Their hierarchical construction retains task
boundaries, allowing prior datasets to change the predictive distribution
without pooling all labels into one task. The paper trains a transformer
on target-task predictive likelihoods and studies synthetic regression
families as well as a temperature-prediction application. Its results
motivate task-structured prior adaptation; they are not stock-trading
evidence. [@zhu2026multitask]

The thesis adopts this task distinction in a different numerical and
economic setting. Earlier same-stock blocks supply prior tasks; mature
observations from the current block supply target context. Bucket
filtering, regime-prioritized ranking and frozen resource constraints
determine the context actually admitted. A small numerical student and
a probabilistic teacher operate before a hosted Decision LLM sees a text
projection. Multi-task refers to these datasets; multi-agent refers to
the separate reporting and decision roles.[^mt-related-implementation]

The differences from the source paper are substantive. The registered
teacher here is a fitted mixture of sixteen Beta components with
task-specific Bernoulli rates. Its predictive calculation uses visible
label counts under that model, not a feature-conditional regression
likelihood. Synthetic distillation trains the student on teacher soft
probabilities at the query; sampled feature vectors are independent of
the synthetic latent rates and labels. This differs from treating the
source paper's generative regression tasks and target-observation
likelihood objective as the exact implementation used here. The local
student also has two attention blocks and four heads, whereas the source
paper's synthetic setup specifies eight layers and eight heads. Resource
names containing “replica” therefore identify local artifacts, not proof
of an exact replication.[^mt-related-implementation]

At market inference the numerical parameters are frozen, while the visible
context can change. A separate magnitude model and utility gate determine
whether a hosted proposal may replace Fact Anchor. An approximate
teacher probability, the hosted LLM's verbal confidence and the final
LONG/CASH action are distinct outputs. Synthetic teacher agreement is
evidence about that approximation task; it does not establish calibrated
market probabilities or the causal value of the student, target context
or utility policy separately. Those contributions require the matched
interventions identified in Section 5.9, beyond the combined bridge that
was actually observed.

[^mt-related-implementation]: Sections 4.8.2–4.8.6 and CL078–CL101 bind task membership, the sixteen-component teacher, synthetic sampling, paired numerical packing, two-block/four-head student, selected weights, text projection and external policy. Source-paper comparison uses R16 §4/§5.1/Appendix C; local recipe and outcomes remain independently source-bound.

## 2.6. Evaluation of trading systems using LLMs

Evaluation must separate information available at the decision cutoff,
choices made during development and economic outcomes produced by a
specified execution contract. Arnott, Harvey and Markowitz discuss a
financial research protocol that addresses data limitations, selection,
implementation shortfall and changing market behavior. This motivates
reporting costs and implementation assumptions alongside prediction
metrics, rather than treating a favorable historical score as deployment
evidence. [@arnott2019backtesting]

Chronological ordering is necessary for the recorded decision problem,
but ordering row timestamps alone is insufficient. A training example's
label may require prices after its decision date; the relevant boundary
is when its outcome has matured. The thesis therefore states entry and
exit dates, purges inadmissible holding intervals and binds model/scaler
fitting periods separately from query prefixes. News requires its own
availability evidence. These are explicit implementation contracts, and
the unresolved native row-wise and news-provenance limits remain visible
rather than being inferred away from a chronological split.
[^evaluation-implementation]

Selection and repeated inspection create another problem. White's Reality
Check addresses predictive comparison after specification search and
explains how repeated data use can produce apparently attractive results.
Varma and Simon's classification study similarly shows the danger of
using an optimized validation score as its own independent error estimate.
Together these motivate separating fitting, selection and assessment,
while retaining the assumptions of each source. The thesis does not claim
to have run White's procedure or to have established the time-series
validity of nested random cross-validation. [@white2000reality]
[@varma2006bias]

For an LLM system, the comparison unit also includes stochastic model
responses and their upstream inputs. A paired comparison can preserve
one recorded upstream realization for all methods at a point, instead
of asking each branch to obtain a different chart interpretation.
Repeating the final Decision call then probes conditional response
variation, not a new market history. Matched ablations should preserve
the comparison support and other inputs when isolating an intervention.
A comparison that jointly changes projection, instructions and information
cannot identify their separate effects merely because its final actions
were paired.[^evaluation-implementation]

Dependence-aware uncertainty methods retain assumptions of their own.
Politis and Romano develop a stationary bootstrap with random-length
blocks for weakly dependent stationary observations. The fixed-length
circular blocks and whole-fold resampling recorded in this thesis are
different constructions. The reference motivates preserving dependence;
it does not certify the chosen block lengths or nominal coverage with
six exposed folds. [@politis1994stationary] Newey and West's covariance
estimation work likewise addresses heteroskedasticity and autocorrelation
under regularity conditions; a stored panel-HAC diagnostic is not a
finite-sample guarantee for this dataset. [@newey1987hac]

Multiplicity must be considered with the validity of the underlying
comparisons. Holm's sequential procedure controls family-wise error when
the individual tests meet their validity requirements. Applying its
adjustment does not repair an unverified block-sign symmetry assumption
or turn post-inference analysis into prospective confirmation. The
component numerical diagnostics and the context study's joint descriptive
bands therefore retain their separate constructions, full contrast
families and undefined-value rules. [@holm1979multiple]

Finally, reproducibility has several levels. Versioned sources, inputs,
prompts, responses and checkpoints can make a stored analysis traceable;
offline reproduction can check the published artifacts. A new hosted call
may still differ because the served model or service behavior changes.
Prospective confirmation additionally requires evidence collected under
a fixed, previously unexposed protocol. The historical receipts and
descriptive sensitivities in Chapter 5 establish only their stated scope.
Neither a fluent explanation, a successful replay nor a source hash by
itself establishes input authenticity, live fills or profitable deployment.

[^evaluation-implementation]: Sections 3.7, 4.9–4.10 and 5.1–5.5 bind event-time maturity, outcome barriers, shared upstream, pairing, prompt/retry/checkpoint handling and each estimator; CL021–CL024/CL126–CL144/CL182–CL186. These internal contracts and historical audit limits are distinguished from the methodological results of the cited publications.

## 2.7. Research gap and position of the thesis

The selected literature establishes specialist financial agents, visual
analysis and reflection as existing ideas, while the Bayesian-ICL
literature provides explicit models for learning from datasets in context.
The question addressed here is how these ingredients behave when combined
under a particular historical information boundary, action contract and
paired evaluation. It is an integration and measurement problem with
unresolved empirical components, rather than a claim to have invented
multi-agent trading, chart reasoning or multi-task Bayesian inference.

**Table B08a. Selected financial-agent systems and the thesis.** Each
publication row summarizes the inspected method/evaluation sections,
identified by its versioned citation. A reported availability rule is an
author-stated protocol, not an independent PIT or venue audit conducted
for this review. Different assets, schedules and economic contracts
prevent ranking the systems by their separately reported returns.

| System / source | Inputs and visual representation | Reasoning / historical context | Reported evaluation and economic scope |
| --- | --- | --- | --- |
| QuantAgent v3 [@xiong2025quantagent] | Price-derived indicators, candlestick and trendline views | Indicator/Pattern/Trend/Risk with a final DecisionAgent | One-hour/four-hour segments with future bars withheld; LONG/SHORT forecasts and risk bounds; not the thesis daily LONG/CASH oracle |
| TradingAgents v7 [@tradingagents2024] | Fundamental, news, sentiment and technical inputs | Analyst, researcher/debate, trader and risk teams; structured communication | Historical US technology-stock simulation; authors state day-available inputs; buy/sell/hold under their own backtest |
| FinVision v1 [@fatemi2024finvision] | News, candlestick and technical-indicator images | News summary, technical analysis, textual/visual reflection and final recommendation | Dated historical news/charts/signals in the method; BUY/SELL/HOLD and position size; own simulation rather than the thesis fixed net-cycle label |
| This thesis (Chapters 4–5) | Price, adapted alpha, Vietnamese sentiment and two chart views | Inherited report chain, signal priors, numerical prior/target tasks, Fact Anchor and utility policy | Daily LONG/CASH, Open(t+1)→Close(t+3), two-way costs and separate accounts; checked prefixes/bindings retain Native causal FAIL and whole-system NOT_CERTIFIED |

**Table B08b. Historical context and Bayesian inference are different
methodological objects.** Validation domain identifies what the cited
work studied, without extending its conclusions to Vietnamese stock
trading. The thesis row describes the implemented path and its recorded
limits; it does not claim the source theories' guarantees.

| Method / source | Context or prior representation | Learned / inferred object | Validation domain and relevance |
| --- | --- | --- | --- |
| Implicit-Bayes ICL [@xie2022implicitbayes] | Examples share a latent concept in a specified pretraining model | Concept inference analyzed under mixture-of-HMMs assumptions | Theory and synthetic GINC; conceptual explanation, not proof for the hosted trading LLM |
| Learned prompt retrieval [@rubin2022retrieve] | Selected input–output examples | Dense retriever trained from LM-based supervision | Semantic parsing; example selection mechanism, not a financial posterior or the implementation named B_semantic |
| PFN [@muller2022transformers] | A context dataset drawn from a specified training prior | Amortized posterior-predictive approximation via prior-data NLL | Prior-defined supervised inference tasks; neither generic LLM prompting nor the thesis checkpoint |
| Multi-task Bayesian ICL [@zhu2026multitask] | Marked prior datasets, target observations and an unlabeled query | Hierarchical predictive adaptation across priors with task boundaries | Synthetic regression families and ERA5 temperature prediction; intellectual source for task-structured context |
| This thesis numerical/hosted path | Mature same-stock prior/target tasks selected with buckets/regimes; later text projection | Fitted count-based teacher, distilled frozen student, hosted proposal and external utility policy | Recorded Vietnamese-equity study; altered model/objective/architecture, mostly anchor-retaining final actions and missing isolated ablations |

These comparisons identify three concrete requirements for the thesis.
First, historical evidence needs an explicit unit: a selected signal
episode, a population statistic and a task dataset must remain
distinguishable. Second, the proposal must remain separate from the
executed action: a numerical posterior summary, a fact-checked LLM reply
and an anchor-relative utility decision are not equivalent outputs.
Third, a comparison needs common market support and a fixed economic
oracle, with unsupported cases and adverse outcomes retained. The cited
publications motivate these distinctions but do not supply a matched
benchmark for this repository's frozen queries.[^research-position]

The implemented contribution is consequently a source-bound synthesis:
an adapted multi-agent reporting path, matured historical-context
construction with explicit fallback, a numerical task/teacher/student
path, external action resolution and paired research accounting. Chapters
4–5 explain those mechanisms and measure the combinations that were
actually run. This position credits the inherited architecture and
inference ideas while making the added interfaces, constraints and audit
evidence assessable.

Its empirical scope remains limited. The context results depend on the
chosen baseline and readiness; MT final actions mostly retain Fact
Anchor; all eight research roles have negative mean returns. Native
row-wise causality remains FAIL and whole-system causality remains
NOT_CERTIFIED. Missing matched retrieval, prior and MT ablations prevent
isolated mechanism claims. Thus the open research gap is whether the
proposed conditioning and revision mechanisms add reliable value under
repaired temporal provenance and independent evaluation. This thesis
provides an implementation and a bounded historical assessment of that
question, while the stronger claim remains future work.

[^research-position]: B08 publication cells map to R04/R06/R07 and R13–R16 in ledger §11.1/§11.6. Implementation cells map to Chapters 4–5, CL025–CL028/CL064–CL101/CL145–CL187 and the source cards cited there. The selected comparison is not an exhaustive literature search or a claim of global priority, superiority, independently certified PIT or profitable execution.
