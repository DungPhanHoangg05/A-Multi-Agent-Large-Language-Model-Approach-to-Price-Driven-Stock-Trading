# Chapter 2. Related Work

> **Draft status: sources checked; prose in progress.** The scoped bibliography and reading register are established; unfinished sections remain explicitly marked.
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
[third-party notices](../../THIRD_PARTY_NOTICES.md). The current upstream
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

> **Not yet drafted.** Review HMMs and relevant trend/volatility alternatives with verified citations. Explain frozen fitting and prefix-only inference; distinguish a regime used for retrieval from a demonstrated profitable signal.

## 2.4. In-context learning and Bayesian historical context

> **Not yet drafted.** Explain example retrieval and few-shot prompting separately from weight updates. Review priors, posteriors and finite historical evidence, distinguishing interventions on examples, statistics and task context.

## 2.5. Multi-task Bayesian ICL and student–teacher methods

> **Not yet drafted.** Identify and verify the source methodology for prior tasks, target observations, teacher targets, student training and frozen query inference. State the actual implementation differences; multiple examples alone are insufficient to establish multi-task Bayesian inference.

## 2.6. Evaluation of trading systems using LLMs

> **Not yet drafted.** Review chronological evaluation, purging, transaction costs, paired comparisons, numerical controls, ablations and inference for dependent observations. Explain the difference between exploratory historical analysis and prospective confirmation, supported by primary methodological sources.

## 2.7. Research gap and position of the thesis

> **Not yet drafted.** Build the comparison matrix from publications actually read and checked, covering inputs, architecture, context, regimes, temporal protections, economics and controls. Derive a bounded research gap from that matrix and the implemented system; do not fill unsupported cells or assume novelty from a method name.
