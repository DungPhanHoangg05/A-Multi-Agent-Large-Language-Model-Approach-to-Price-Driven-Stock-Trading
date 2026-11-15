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

> **Not yet drafted.** Compare role specialization, shared state, report synthesis and visual inputs. Attribute QuantAgent and other relevant systems, identify adaptations made here, and discuss chart grounding, explanations and hosted-model reproducibility without treating fluent output as validated evidence.

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
