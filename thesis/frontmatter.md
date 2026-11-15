# Front matter

> **Draft status:** the cover metadata follows the author-confirmed brief. The abstract, abbreviation list and notation have been checked against the manuscript. The author has confirmed the acknowledgement and declaration wording; the declaration remains unsigned. No institutional abstract word limit or prescribed declaration/front-matter rules have been supplied.

## Cover metadata

| Field | Text |
| --- | --- |
| National university | VIETNAM NATIONAL UNIVERSITY, HANOI |
| University | UNIVERSITY OF ENGINEERING AND TECHNOLOGY |
| Author | Phan Hoang Dung |
| Student ID | 23020346 |
| Title | Regime-Aware Multi-Task Bayesian In-Context Learning for Multi-Agent LLM Stock Trading in the Vietnamese Stock Market |
| Thesis type | BACHELOR'S GRADUATION THESIS |
| Major | Artificial Intelligence |
| Supervisor | Dr. Tran Hong Viet |
| Place and year | HA NOI - 2026 |

## Outer cover

VIETNAM NATIONAL UNIVERSITY, HANOI\
UNIVERSITY OF ENGINEERING AND TECHNOLOGY

[University logo](assets/figures/UET_logo.jpg)

PHAN HOANG DUNG

REGIME-AWARE MULTI-TASK\
BAYESIAN IN-CONTEXT LEARNING\
FOR MULTI-AGENT LLM STOCK\
TRADING IN THE VIETNAMESE\
STOCK MARKET

BACHELOR'S GRADUATION THESIS

**Major:** Artificial Intelligence

HA NOI - 2026

## Inner cover

VIETNAM NATIONAL UNIVERSITY, HANOI\
UNIVERSITY OF ENGINEERING AND TECHNOLOGY

PHAN HOANG DUNG

REGIME-AWARE MULTI-TASK\
BAYESIAN IN-CONTEXT LEARNING\
FOR MULTI-AGENT LLM STOCK\
TRADING IN THE VIETNAMESE\
STOCK MARKET

BACHELOR'S GRADUATION THESIS

**Major:** Artificial Intelligence

**Supervisor:** Dr. Tran Hong Viet

HA NOI - 2026

## Abstract

Historical context may help a trading system interpret conflicting
reports, but its value depends on temporal eligibility, coverage and the
policy that converts evidence into an action. This thesis adapts a
price-driven multi-agent pipeline for Vietnamese stocks, combining
indicator and chart reports, alpha signals and dated sentiment with
regime-aware historical context. Bayesian prior variants summarize
completed episodes, while multi-task Bayesian in-context learning
(MT-BICL) adds numerical task context and a frozen student/teacher path.
Factual anchoring and an external utility policy distinguish a model's
proposal from the final LONG/CASH action.

Two historical exploratory studies use a recorded schedule of 102 market
points across nine stocks and six exposed temporal blocks/folds, with
51 separately capitalized stock–fold accounts. Their response collections
and statistical conventions remain distinct. The historical-context study
compares eight roles over three Decision repeats conditional on one
shared upstream realization per point; its 2,448 forecast slots are not
independent market observations. The common study contract enters LONG
at the next session's open, exits at the third following session's close
and charges costs on both legs; SHORT maps to CASH.

In the component study, the combined system (Full) exceeds its control
without alpha and sentiment (Base) by 3.247 percentage points (pp) in
balanced accuracy but has a mean net account-return difference of
−0.047 pp. Bayesian v1 exceeds the common-profile baseline (Common) by
0.327 pp in mean return, whereas its difference from the native-profile
baseline (Native) is −0.045 pp. These comparisons are
descriptive, baseline-dependent and sensitive to support and dependence
assumptions. MT-BICL retains Fact Anchor's final action in 302 of 306
slots; the combined comparison does not identify an isolated student or
utility-policy benefit. All eight context research methods have negative
mean net account returns. The Native row-wise causality audit remains
FAIL, and whole-system causality is not certified; provenance, execution
and application-acceptance limitations remain unresolved. The contribution
is a traceable system integration and bounded historical assessment,
with no established prospective profitability.

## Keywords

Vietnamese stock market; multi-agent systems; large language models; regime-aware historical context; multi-task Bayesian in-context learning; LONG/CASH evaluation; point-in-time validity.

## Acknowledgements

> **Author-confirmed wording.** This draft names only the
> supervisor supplied by the author and claims no unverified contribution,
> funding, endorsement or institutional approval.

I thank my supervisor, Dr. Tran Hong Viet.

## Declaration

> **Author-confirmed wording; unsigned.** No prescribed
> institutional declaration has been supplied. This text is not an
> institution-approved form or an assertion that the author has signed it.

I acknowledge the published methods, software and data sources on which
this thesis builds, and distinguish inherited components from the
adaptations and evaluation reported here. The historical findings are
presented with their adverse outcomes and unresolved limitations.
Unperformed experiments are identified as future work, and historical
simulations are distinguished from prospective trading evidence.

AI-assisted tools have been used to draft and edit this thesis manuscript.
Responsibility for checking the final text, references, attribution and
reported evidence rests with the author.

**Author:** Phan Hoang Dung\
**Student ID:** 23020346\
**Signature:** [To be completed by the author]\
**Date:** [To be completed by the author]

## List of abbreviations

| Abbreviation | Meaning |
| --- | --- |
| API | Application programming interface |
| BA | Balanced accuracy |
| BICL | Bayesian in-context learning |
| BRPP | Bayesian Regime Prior Prefix |
| EMA | Exponential moving average |
| EOD | End of day |
| F1 | F1 score; harmonic mean of precision and recall when defined |
| FN | False negative |
| FP | False positive |
| HAC | Heteroskedasticity and autocorrelation consistent |
| HMM | Hidden Markov model |
| HTTP | Hypertext Transfer Protocol |
| IC | Information Coefficient |
| ICL | In-context learning |
| JSON | JavaScript Object Notation |
| LLM | Large language model |
| MACD | Moving average convergence divergence |
| MAP-EM | Maximum a posteriori expectation–maximization |
| MCC | Matthews correlation coefficient |
| MDD | Maximum drawdown |
| MT-BICL | Multi-task Bayesian in-context learning |
| NA | Not available; missing or undefined as specified |
| NAV | Net asset value |
| NLL | Negative log-likelihood |
| OHLCV | Open, high, low, close and volume |
| P&L | Profit and loss |
| PFN | Prior-data fitted network |
| PIT | Point in time |
| pp | Percentage points |
| R:R | Risk/reward ratio reported in a model reply |
| ROC | Rate of change |
| RPM | Requests per minute |
| RSI | Relative Strength Index |
| SD | Standard deviation |
| SHA-256 | Secure Hash Algorithm with a 256-bit digest |
| SMA | Simple moving average |
| TN | True negative |
| TP | True positive |
| TPM | Tokens per minute |
| UI | User interface |
| VLM | Vision-language model |
| VND | Vietnamese dong |

## List of symbols

This list collects common notation used in Chapters 3–5. Local indices
and specialized symbols retain the definitions given in their sections.
In particular, a conditional-statistic index and a teacher-mixture
component index do not denote the same object merely because the same
letter is used locally.

| Symbol | Meaning | Unit and scope |
| --- | --- | --- |
| $t$, $e=t+1$, $L$ | Decision-bar index, exclusive window end/entry index and holding horizon. | Observed sessions; $L=3$, entry at $e$, exit at $e+L-1=t+3$. |
| $W$, $[e-W,e)$ | Chart-window length and half-open input window. | Observed bars; distinct from longer feature-computation history. |
| $O_{t+1}$, $C_{t+3}$ | Entry Open and exit Close of the candidate LONG. | Prices on the declared basis; excluded from query-time inference. |
| $f$, $s$ | Brokerage fee and slippage on each leg. | Fractions: $f=0.0025$, $s=0.001$ under the study contract. |
| $r_t^{\mathrm{net}}$ | Candidate-LONG net round-trip return. | Fraction after entry and exit costs; §3.2. |
| $y_t$ | Positive net label, $\mathbf{1}[r_t^{\mathrm{net}}>0]$. | Binary: UP is 1; DOWN is 0, including zero return. |
| $\hat d_{t,v,j}$, $a_{t,v,j}$, $a_0$ | Raw direction, final action and resolved anchor for method $v$/repeat $j$. | Direction LONG/SHORT; actions LONG/CASH; SHORT maps to CASH. |
| $r_{t,v,j}^{\mathrm{strategy}}$ | Cycle payoff under the final action. | Net-return fraction; candidate-LONG payoff for LONG, zero for CASH. |
| $N_{\mathrm{point}}$, $N_{\mathrm{account}}$, $n_{\mathrm{rep}}$ | Market points, separately capitalized accounts and Decision repeats. | Counts; context study 102, 51 and 3, respectively. |
| $K_{\mathrm{ex}}$ | Selected/displayed signal-bank examples. | Records; different from population support or the requested upper limit. |
| $K_{\mathrm{task}}$, $m$ | Prior-task count and target-task observation count. | Task datasets and labeled observations, respectively; not LLM calls. |
| $n_k$, $\mathcal D_k$, $\mathcal C_q$, $\boldsymbol x_q$ | Prior-task size, prior dataset, target observations and unlabeled query features. | Historical memberships/features; the query has no visible label. |
| $\boldsymbol x_i$, $\boldsymbol z_i$ | Raw and standardized numerical feature vectors. | Feature-specific units before scaling; dimensionless after scaling. |
| $S_t$ | Market-regime assignment at cutoff $t$. | Categorical model output; not an action or an outcome label. |
| $n_{c,h}$, $s_{c,h}$, $n_{b,h}$, $s_{b,h}$ | Conditional/background support and success counts for metric $h$. | Counts in disjoint metric-specific subsets; not displayed-example counts. |
| $\tau$, $a_h$, $b_h$ | Shrinkage strength and Beta shapes for a conditional statistic. | Model parameters; teacher component parameters are defined locally in §4.8.3. |
| $p_{S,q}$, $p_{T,q}$ | Student positive-label estimate and teacher predictive mean. | Fractions in [0,1]; neither is the LLM confidence field. |
| $\theta_q$, $\boldsymbol\pi$ | Target-task Bernoulli parameter and frozen teacher mixture weights. | Model probabilities/weights; distinct from hosted-model weights. |
| $g_q$, $\ell_q$ | Positive-return and nonpositive-return loss magnitudes for utility. | Nonnegative net-return fractions; zero belongs to the nonpositive group. |
| $U_q$, $\Delta U_q$ | LONG-versus-CASH utility and utility change from the anchor. | Net-return fractions; $U_q=\theta_q g_q-(1-\theta_q)\ell_q$ for posterior draws. |
| $Q_\eta(U_q)$ | Quantile at level $\eta$ of model-based posterior utility draws. | Net-return fraction; the policy uses the 0.1 and 0.9 quantiles. |
| $R_{a,j}$, $\bar R_v$ | Account return and method mean after repeat averaging. | Fractions in equations; percent-valued output fields are already multiplied by 100. |
| $V_{a,d}$, MDD | Account NAV at date $d$ and maximum drawdown. | VND for NAV; percent loss magnitude for MDD, with the NAV path specified. |
| BA, MCC, IC | Balanced accuracy, Matthews correlation and factor Information Coefficient. | BA is a fraction or percent as labeled; MCC and rank IC are dimensionless. |
| $\Delta_R^{\mathrm{pp}}$, $\Delta_{\mathrm{BA}}^{\mathrm{pp}}$ | Named method-minus-comparator return and BA differences. | Percentage points; a difference of fractions is multiplied by 100 once. |
| $\operatorname{age}_i$, $d_i$, $\operatorname{sim}_i$ | Historical-item age, numerical distance and retrieval similarity. | Age in recorded calendar days; distance/similarity use their declared score scales. |

## Reading conventions

**Study and method names.** Full and Base refer to the component study.
Native and Common refer to distinct profiles in the historical-context
study. These are not interchangeable response collections. MT-BICL
concerns numerical task context and action revision; multi-agent describes
the division of analysis roles. The [controlled terminology](evidence.md#5-thuật-ngữ-tiếng-anh-ký-hiệu-và-quy-ước-diễn-đạt)
records method aliases and overloaded implementation names.

**Actions and targets.** LONG/SHORT is the raw proposal vocabulary;
LONG/CASH is the final action vocabulary. SHORT maps to CASH rather than
an equity short sale. UP/DOWN labels describe whether the candidate LONG
has strictly positive net return; DOWN includes zero. A CASH action does
not earn the candidate LONG return. The timing and costs are study
assumptions, not a statement of current exchange rules.

**Evidence and units.** Displayed signal examples, prior-task datasets,
target observations, market points, forecast slots, new replies, HTTP
attempts and stock–fold accounts have different denominators. An average
of separately capitalized accounts is not a validated shared-capital
portfolio. Percent and percentage points remain distinct.

**Probability, confidence and utility.** Numerical student/teacher
probabilities are model outputs, not automatically calibrated forecasts.
A model's confidence field is a separate report. Posterior utility is a
model-based net-return quantity used by the external action policy, not
a measured guarantee of profit.

**Missingness and validity.** NA/null retains a recorded missingness or
undefined-value reason; it is not a genuine numerical zero. Unavailable
news is not observed neutral sentiment. A documented fallback or bypass
differs from a technical failure. Point-in-time input eligibility does
not by itself establish row-wise causality, and a source hash or offline
replay does not certify authentic historical availability, live execution
or application acceptance.
