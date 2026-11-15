# Chapter 3. Theoretical Background and Problem Formulation

> **Draft status: partial chapter.** Sections 3.1–3.5 have source-checked drafts.
> Sections 3.6–3.7 remain placeholders; the chapter has not undergone final manuscript review.

Writing aids: [chapter outline](../outline.md#chapter-3-theoretical-background-and-problem-formulation), [terminology and notation](../evidence.md#5-thuật-ngữ-tiếng-anh-ký-hiệu-và-quy-ước-diễn-đạt) and [shared evidence ledger](../evidence.md#8-khung-bản-thảo-và-đối-soát-luận-điểm).

## 3.1. Observations and time indexing

### 3.1.1. Daily observations

The historical studies represent each stock as an ordered sequence of daily
bars. For a single stock, let

$$
b_i=(d_i,O_i,H_i,L_i,C_i,V_i),\qquad i=0,\ldots,N-1,
$$

where $N$ is the number of observations in the declared analysis view and
$d_i$ is the date attached to observation $i$. The fields $O_i$, $H_i$,
$L_i$ and $C_i$ are the opening, highest, lowest and closing prices reported
for that bar. $V_i$ is its reported volume. Together these fields are called
OHLCV. Prices must retain the dataset's declared units and adjustment basis;
the field names alone do not establish either. In particular, the volume
field is distinct from a price or a net return.[^time-inputs]

An *observed session* in this thesis means one dated daily row used by the
protocol. Indices count these rows after the analysis view has been
established, with dates in strictly increasing order. They do not certify
that the vendor sequence contains every exchange session. Thus $i+1$ means
the next observation in this sequence, not the next calendar day. A weekend,
holiday, suspension or absent vendor record may separate consecutive dated
rows; the cause of a gap cannot be inferred from its length alone.

The subscripts above identify price fields: $L_i$ is a low price. The
unsubscripted $L$ introduced below instead denotes the execution horizon
in observed bars.

### 3.1.2. Decision cutoff and the exclusive window boundary

Let $t$ be the zero-based index of the last bar visible to a decision, and
let its date be $d_t$. The daily decision is modeled as occurring after this
bar has completed. Its OHLCV values may therefore be used, whereas the next
bar's open is still a future price. This is the study's information boundary,
not a claim that historical vendor data were published with verified
real-time latency.

The engine expresses the same boundary using $e=t+1$, the **exclusive** end
index of an input window. If $W$ is the chart-window length, the slice
$[e-W,e)$ contains indices $e-W,\ldots,e-1$: exactly $W$ observations,
ending at $t=e-1$. Row $e$ is excluded. Here $[a,b)$ denotes a half-open
interval of integer row positions, not a date range.[^time-engine]

The execution horizon $L$ counts the future bars starting with the entry bar.
Under the daily contract, $L=3$. The corresponding positions are:

| Event | Position in the parent sequence | Price used or information boundary |
| --- | --- | --- |
| First chart bar | $e-W=t-W+1$ | First included OHLCV observation |
| Decision bar | $e-1=t$ | Last visible completed bar |
| LONG entry | $e=t+1$ | Open of the first future observed bar |
| Intermediate bar | $e+1=t+2$ | Second future observed bar |
| LONG exit | $e+L-1=t+L$ | Close of the final horizon bar; $t+3$ when $L=3$ |

The horizon therefore comprises bars $t+1,t+2,t+3$, rather than three
calendar days added to $d_t$. The outcome record may be evaluated only once
the required future observations exist; their prices do not belong to the
forecast input. SHORT is executed as CASH in this research contract, so this
timeline does not imply a short sale. Section 3.2 will define the associated
net label, costs and LONG/CASH payoff.[^time-target]

These are positions in the **parent** analysis sequence. The engine resets
the index of an extracted chart window for local processing; local positions
$0,\ldots,W-1$ do not replace the parent cutoff or move the entry bar.

### 3.1.3. Chart windows, longer history and warm-up

A chart window and the complete history available at the cutoff serve
different purposes. The locked historical-data path gives the chart/report
pipeline the final $W=45$ bars and supplies a longer prefix of $A=600$ bars
through the Alpha history input. Both end at the same cutoff. Their row
intervals are $[e-W,e)$ and $[e-A,e)$ respectively. The 600-bar history is
not an additional block after the chart window: it contains the final
45-bar window.[^time-inputs]

Warm-up is the history needed before a query can be formed. The engine
requires $e\geq\max(W,A)$ so that both slices are available. A full horizon
also requires $e+L-1<N$. For the earliest possible single query, these
conditions imply at least $\max(W,A)+L$ rows: 603 when $W=45$, $A=600$ and
$L=3$. The final three rows in that minimum are evaluation observations,
not warm-up or forecast inputs.[^time-engine]

This minimum is a data-availability requirement. It does not show that every
indicator is numerically defined on its first row, that an estimator has
converged, or that model training used the same history length. An indicator's
own lookback/initialization, a model's training period, the query's chart
window and the future execution horizon are separate concepts. Their
component-specific rules are introduced in the later sections.

### 3.1.4. Missing and invalid records

The declared analysis view matters because removing observations can change
row positions. In the frozen historical-data path, the price-view check
requires unique increasing dates, finite positive OHLC prices and finite
nonnegative volumes with positive total volume. If OHLC ordering is invalid,
that path retains the suffix after the last such row and records the excluded
prefix. These are properties of this particular input path, not a claim that
all live or legacy loaders use identical cleaning.[^time-view]

An insufficient clean prefix or incomplete future horizon is not permission
to shorten $W$, borrow future warm-up data or use an earlier exit. The locked
historical provider rejects a query without the required history or exact
cutoff, and the canonical target contract rejects an incomplete horizon.
The engine's lower-level direction helper can return an UNKNOWN sentinel
when the target lies outside the frame; this is not a valid evaluated label
or a support-based CASH decision.[^time-inputs][^time-target][^time-engine]

The notation also provides no basis for manufacturing flat candles to fill
a gap or declaring every absent date a market holiday. Missing-data decisions
must retain their source and exclusions. Where the vendor calendar has not
been independently authenticated, the execution horizon should be described
as three subsequent observed bars. This local time boundary alone does not
establish row-wise causality of every historical feature; Section 3.7 will
address that wider validity question.

### 3.1.5. A dated example

The running example uses FPT at the recorded cutoff of **3 July 2023**. Its
shared snapshot contains 600 bars from 2 February 2021 through that date;
the final 45 bars span **27 April–3 July 2023**, inclusive. These are counts
of saved observations, not counts of all calendar dates in either interval.

The saved outcome record identifies the decision-bar index as $t=872$ in
the parent analysis sequence. Consequently $e=873$, the chart slice is
$[828,873)$, and its final included row is 872. The recorded subsequent
observations are 4, 5 and 6 July: LONG enters at the open of row 873 on
4 July and exits at the close of row 875 on 6 July. Reading these dates to
explain the schedule does not make the corresponding prices available to
the forecast. The later realized outcome is reserved for the case analysis
in Chapter 5.[^time-example]

![Decision cutoff, entry and exit, with the dated FPT example.](../assets/diagrams/F01_trade_timeline.png)

*Figure F01. Decision cutoff, entry and exit of a trading cycle. The upper
panel illustrates the 45-bar chart inside the longer history and the three
future execution bars. The lower panel uses the dates and decision index
saved for EX01; spacing is schematic and no future price or return is shown.
This is an illustration of the study contract, not a measured trading result
or an authenticated exchange calendar.* [Vector PDF](../assets/diagrams/F01_trade_timeline.pdf).

[^time-engine]: Frozen execution source: `core/backtest_engine.py`, `required_backtest_rows`, `build_walk_forward_end_indices`, `_prepare_window` and `_get_actual_direction`. Exact source bindings are recorded as TIME01 in the shared evidence ledger.
[^time-target]: Frozen target source: `utils/target_contract.py`, `target_fields`; TIME02 in the shared evidence ledger. Its horizon is an execution convention of the study.
[^time-inputs]: Frozen historical provider and serialization: `HistoricalData.prefix/state` in `core/historical_evaluation_data.py`, and `snapshot_payload` in `core/historical_signals.py`; TIME03/TIME05 in the shared evidence ledger.
[^time-view]: Frozen input validation: `price_view` in `core/historical_asset_readiness.py`; TIME04 in the shared evidence ledger.
[^time-example]: Archived EX01-S and EX01-O, joined by point and price-source identity; the shared evidence ledger records their ZIP/member hashes and the derived row-index arithmetic. No forecast or outcome has been regenerated.

## 3.2. Economic contract and prediction target

### 3.2.1. A candidate LONG cycle

For a decision at bar $t$, consider the candidate trade that buys at the next
observed open $O_{t+1}$ and closes at $C_{t+3}$. These are the entry and exit
defined in Section 3.1. Let $f=0.0025$ denote the brokerage fee and $s=0.001$
the proportional slippage on **each** leg. Buying one unit requires
$O_{t+1}(1+s)(1+f)$ of capital; selling it yields
$C_{t+3}(1-s)(1-f)$. The canonical net return is therefore

$$
r_t^{\mathrm{net}}=
\frac{C_{t+3}}{O_{t+1}}
\frac{(1-s)(1-f)}{(1+s)(1+f)}-1.
$$

This is the equation implemented by the shared economic oracle,
`compute_round_trip_net_return`; canonical historical labels use the same
oracle. The numerator includes selling costs and the denominator includes
buying costs. Subtracting a fixed 0.70 percentage points from the gross return
is only an approximation and is not the calculation used here.
Entry/exit prices must be positive and finite. The date convention and costs
are study assumptions, not a statement of current exchange settlement rules
or proof of executable fills.[^economic-oracle]

For comparison, the cost-free return is
$r_t^{\mathrm{gross}}=C_{t+3}/O_{t+1}-1$. Net break-even requires a price ratio
of $(1+s)(1+f)/[(1-s)(1-f)]$, approximately 1.00702457 under these costs.
A small positive gross move can consequently have a negative net result.

### 3.2.2. Label, proposal and execution action

The supervised target describes the candidate LONG trade, regardless of the
action eventually taken:

$$
y_t=\mathbf{1}\{r_t^{\mathrm{net}}>0\}.
$$

UP means $y_t=1$; DOWN includes every nonpositive return, **including zero**.
The canonical implementation compares the unrounded net return with zero;
a rounded displayed value must not replace that comparison. A cost-free
direction, a close-to-close return, or the LLM's stated confidence is a
different quantity.[^economic-oracle]

The raw forecast is LONG or SHORT. In this long-only research contract,
SHORT maps to the execution action CASH; it does not open a short position.
Let $a_t\in\{\mathrm{LONG},\mathrm{CASH}\}$ be the action after any external
policy. The cycle payoff fraction is

$$
r_t^{\mathrm{strategy}}=
\mathbf{1}\{a_t=\mathrm{LONG}\}\,r_t^{\mathrm{net}}.
$$

CASH keeps the simulated capital unchanged over that cycle, with no
short-sale profit or modeled interest. Correctly choosing CASH when the
candidate LONG label is DOWN can improve classification without earning a
positive cycle return. Conversely, an UP label does not mean that an account
which stayed in CASH earned that candidate return. Account aggregation over
several cycles is a separate evaluation operation.

### 3.2.3. Illustrative calculation

The following numbers are **Illustrative**: they are chosen for arithmetic,
not taken from EX01 or from an experimental performance table. Prices use
one consistent arbitrary unit and both rows use the costs above.

| Entry Open | Exit Close | Gross return | Canonical net return | Net label | LONG payoff | CASH payoff |
| --- | --- | --- | --- | --- | --- | --- |
| 100 | 100 | 0.000000% | −0.697557% | DOWN | −0.697557% | 0% |
| 100 | 103 | +3.000000% | +2.281516% | UP | +2.281516% | 0% |

For the second row, the purchase cost is $100(1.001)(1.0025)=100.35025$,
and sale proceeds are $103(0.999)(0.9975)=102.6397575$. Their ratio minus
one is approximately 0.022815164885. At exact mathematical break-even,
$C_{t+3}=O_{t+1}(1+s)(1+f)/[(1-s)(1-f)]$, the net return is zero and belongs
to DOWN; this is a symbolic boundary, not a claim that rounded floating-point
prices necessarily produce an exactly zero machine value.

These examples explain the contract. They neither regenerate frozen labels
nor resolve discrepancies in legacy evidence. Recorded bank/query price-basis
differences remain a validity limitation to disclose when interpreting the
historical studies.

[^economic-oracle]: Frozen `core/backtest_engine.py`, `compute_round_trip_net_return` and `compute_account_metrics`, and `utils/target_contract.py`, `target_fields`; bindings TIME01/TIME02 in the shared ledger. Illustrative arithmetic and scope are mapped as CL007–CL008.

## 3.3. Technical, alpha and sentiment signals

### 3.3.1. Five deterministic indicator families

Indicators transform admissible prices into descriptions of momentum or
position within a recent range. They do not supply the future net label.
Let $\operatorname{SMA}_n$ be a trailing mean, $\operatorname{EMA}_n$ an
exponential moving average with update weight $2/(n+1)$ after initialization,
and $H_t^{(n)},L_t^{(n)}$ the highest high and lowest low in the last $n$ bars.
The configured families are as follows.[^signal-formulas]

| Indicator | Definition and configured lookback |
| --- | --- |
| MACD (12,26,9) | $M_t=\operatorname{EMA}_{12}(C)_t-\operatorname{EMA}_{26}(C)_t$, signal $\operatorname{EMA}_9(M)_t$, histogram $M_t-\operatorname{EMA}_9(M)_t$. The histogram measures separation from the signal, not from zero. |
| RSI (14) | For gains $g_t=\max(C_t-C_{t-1},0)$ and losses $\ell_t=\max(C_{t-1}-C_t,0)$, Wilder-smoothed averages $G_t,D_t$ give $100G_t/(G_t+D_t)$ when the denominator is nonzero. After initialization, the smoothing weight is $1/14$. The usual range is 0–100. |
| Slow Stochastic (14,3,3) | Raw $k_t=100(C_t-L_t^{(14)})/(H_t^{(14)}-L_t^{(14)})$; slow %K is $\operatorname{SMA}_3(k)$ and %D is $\operatorname{SMA}_3(\text{slow %K})$. These are range oscillators, not MACD histograms. |
| Williams %R (14) | $-100(H_t^{(14)}-C_t)/(H_t^{(14)}-L_t^{(14)})$, in [−100,0] for a valid nonflat range. It locates the close relative to the recent high. |
| ROC (10) | $100(C_t/C_{t-10}-1)$, a percentage change over ten observed bars, distinct from the net execution return. |

Library initialization and flat-range handling are part of an actual series.
The frozen toolkit calls TA-Lib with these settings; its recorded runtime,
rather than current upstream code, determines historical values. Missing
warm-up values and calculation failures differ from a finite value of zero.

The Indicator role computes values and heuristic classifications in Python.
For example, MACD crossover rules have priority over histogram rules. The
other oscillators have their own range and direction conditions. A bullish
vote means a configured heuristic fired, not that the probability of a
profitable LONG is known. Votes derived from the same prices are not
independent observations. Chapter 4 will detail the implemented priorities
after these definitions.[^signal-runtime]

### 3.3.2. Alpha transformations and selection

An alpha factor is a numerical transformation intended to describe a
potential predictive relation; its value need not be a probability or a
return. The [Alpha101 collection](https://arxiv.org/abs/1601.00991v3) is an
inherited source of candidates. Adapting a cross-sectional operation to a
single-stock time series changes the operation; a shared formula name alone
does not establish equivalent implementations.

In the causal-common profile, value $a_u$ is normalized with its expanding
prefix mean $\mu_u$ and sample standard deviation $\sigma_u$:

$$
\widetilde a_u=\tanh\!\left((a_u-\mu_u)/\sigma_u\right).
$$

A near-constant finite prefix is handled as zero, while missingness is
retained. Training information coefficient (IC) is a Spearman correlation
between factor values and candidate-LONG net returns. Its sign determines
orientation; declared validation support selects factors and thresholds
before the selector is frozen. Orientation and ranking are fitted choices,
not evidence of future profitability. Native construction and its row-wise
causality limits remain distinct.[^signal-alpha]

### 3.3.3. Sentiment and missing information

Sentiment summarizes textual evidence separately from price-derived alpha.
A language-model backbone, sentiment classifier, score and aggregation
recipe are different objects. A bounded score is not automatically the
probability that a stock price will rise.

The frozen historical provider uses verified scores in [−1,1], a
90-calendar-day availability window and a minimum of three eligible scores.
It averages them with weights proportional to $\exp[-(\log 2)a/30]$ for age
$a$ days, a 30-day half-life. Under its conservative date-only policy, an
article is unavailable before the day following publication. Undated and
future information is excluded. Fewer than three eligible scores produces
unavailable sentiment, not an observed neutral value.[^signal-news]

EX01 has no eligible verified articles. A zero-filled display or legacy
NEUTRAL code cannot supply the missing evidence. LLM confidence categories,
IC, indicator votes and sentiment scores must all remain separate from the
numerical label probabilities introduced in Section 3.6. None is called
empirically calibrated solely because it is numerical or confidently stated.

[^signal-formulas]: Official computational references consulted 15 November 2026: TA-Lib [MACD](https://raw.githubusercontent.com/TA-Lib/ta-lib/main/src/ta_func/ta_MACD.c), [RSI](https://raw.githubusercontent.com/TA-Lib/ta-lib/main/src/ta_func/ta_RSI.c), [STOCH](https://raw.githubusercontent.com/TA-Lib/ta-lib/main/src/ta_func/ta_STOCH.c), [WILLR](https://raw.githubusercontent.com/TA-Lib/ta-lib/main/src/ta_func/ta_WILLR.c) and [ROC](https://raw.githubusercontent.com/TA-Lib/ta-lib/main/src/ta_func/ta_ROC.c). These references do not replace the frozen study runtime.
[^signal-runtime]: Frozen `utils/graph_util.py`, `Toolkit.compute_*`, and Indicator calculation/classification; CL009. Live Indicator presentation changes were accepted as logic-equivalent by the author; the historical binding remains frozen.
[^signal-alpha]: Frozen `core/causal_alpha.py`, `normalize` and `fit_selector`; CL010.
[^signal-news]: Frozen `core/historical_evaluation_data.py`, `FrozenNews.get_sentiment_at`; TIME03/CL011. EX01 unavailability has its own saved-source binding.

## 3.4. Hidden Markov models for market regimes

### 3.4.1. Latent states and observed features

A regime is an inferred description of market conditions, not an observed
profitable-trade label. Regime-switching models represent changing behavior
through a latent state; [Hamilton (2005)](https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf)
provides the economic modeling context. In an HMM, hidden state $S_u$ follows
a first-order Markov transition matrix $A$, where
$A_{ij}=P(S_u=j\mid S_{u-1}=i)$ and each row sums to one. The initial-state
distribution is $\boldsymbol\pi$. An emission density $b_j(\boldsymbol x_u)$
describes the observed feature vector conditional on state $j$.

The implemented detector uses four Gaussian states with diagonal covariance.
Its VN-Index feature vector contains log return
$\log(C_u/C_{u-1})$, the sample standard deviation of the last 20 log returns,
and $C_u/\operatorname{SMA}_n(C)_u-1$ for $n=20,50,200$. These are index-level
conditions, not each stock's return. The 200-bar moving average determines
the feature warm-up; the volatility uses sample standard deviation with
`ddof=1`.[^hmm-implementation]

### 3.4.2. Fitting, scaling and naming states

Feature scaling is fitted on the declared training features. Its means and
scales are then fixed when transforming later prefixes. HMM fitting estimates
the initial probabilities, transitions and emission parameters;
expectation–maximization is the standard iterative approach used by the
[hmmlearn implementation](https://hmmlearn.readthedocs.io/en/stable/tutorial.html).
Fitting and query-time state inference are separate operations.

Latent state numbers have no inherent BULL/BEAR meaning. The frozen detector
names the state with the largest training MA200 distance BULL and the smallest
remaining one BEAR; it distinguishes the two remaining states by volatility
as CHOPPY and CONSOLIDATION. Training convergence, occupancy and separation
checks can instead select a documented MULTI_FACTOR classifier based on
moving-average distances and training volatility thresholds. That result
must be identified as a fallback method rather than an HMM posterior. The
mapping and fallback thresholds remain part of the frozen fitted resource.

The source module permits training within 2018–2022 and registers numerical
settings, including four states and diagonal covariance. A permitted range
is not the actual fit cutoff of every saved model: the historical paths use
the resource and training dates recorded in their own manifests. For example,
EX01's numerical MT query uses a model trained through 31 December 2020.
Its BULL assignment is distinct from the signal-prior path's recorded
CONSOLIDATION assignment. Neither should be silently relabeled to make them
agree.[^hmm-implementation]

### 3.4.3. Endpoint inference and future observations

For a fixed fitted model, let
$\alpha_u(j)=P(\boldsymbol x_{1:u},S_u=j)$ be a forward quantity. Its recursion is

$$
\alpha_u(j)=b_j(\boldsymbol x_u)\sum_i\alpha_{u-1}(i)A_{ij},
\qquad
P(S_u=j\mid\boldsymbol x_{1:u})=
\frac{\alpha_u(j)}{\sum_k\alpha_u(k)}.
$$

Filtering conditions on observations through $u$. Smoothing at an earlier
index also conditions on subsequent observations in the supplied sequence.
At its final index there are no subsequent observations, so endpoint
smoothing and filtering give the same state marginal for fixed parameters.
This follows from the forward–backward construction in
[Rabiner (1989), Sections III.A–B](https://web.mit.edu/6.435/www/Rabiner89.pdf).
It does not make all earlier smoothed rows point-in-time valid.

The detector supplies only the permitted prefix to `predict_proba` and uses
the **last** posterior row, followed by the saved state-name mapping.
Thus the function may internally use forward–backward inference without
accessing observations after the query cutoff. Taking an earlier row from
a later, longer call would be a different operation. A Viterbi most-likely
state path is also different from these marginal probabilities.

Endpoint truncation is insufficient if fitting already used future data.
The implementation rejects a model trained after the query date and checks
the query history against the frozen training-prefix hash. Feature dates,
scaler, parameter fit, state interpretation and threshold calibration all
need appropriate temporal boundaries. No model is refitted or prediction
regenerated to write this explanation.[^hmm-implementation]

[^hmm-implementation]: Frozen `core/regime_detector.py`: `build_regime_features`, `fit`, `_regime_calibration`, `_fallback_regime` and `classify_regime`; CL012–CL013 and binding §8.6. EX01 resource dates/hash are recorded in the shared example, not inferred from module defaults.

## 3.5. Bayesian summaries of historical evidence

### 3.5.1. Counts and a conjugate update

A binary historical event may be modeled as $Y_i\mid\theta\sim
\operatorname{Bernoulli}(\theta)$. For $n$ conditionally independent events
with $s$ successes, the likelihood is proportional to
$\theta^s(1-\theta)^{n-s}$. Multiplying by a
$\operatorname{Beta}(a,b)$ prior gives

$$
\theta\mid Y_{1:n}\sim\operatorname{Beta}(a+s,b+n-s),\qquad
E[\theta\mid Y]=\frac{a+s}{a+b+n}.
$$

This follows by collecting powers in the Beta density. The
[Stan conjugate Bernoulli example](https://mc-stan.org/learn-stan/case-studies/mle-params.html)
illustrates this update for a uniform prior. The event and denominator must
be stated: a win rate counts profitable candidate LONG cycles, whereas a
bull-trap rate is conditional on the specified bullish reports. Those
denominators need not match.

**Illustrative:** a Beta(2,2) prior and seven successes in ten trials yield
Beta(9,5), mean $9/14\approx0.642857$, rather than the raw rate 0.7.
Using Beta quantiles gives an equal-tailed 95% interval of approximately
[0.385738,0.861421]. These are invented counts for explaining inference,
not a result for a stock or method.

### 3.5.2. Conditional evidence with a disjoint background

The implemented conditional prior first forms an eligible same-stock,
same-regime historical population $\mathcal P$ at the query cutoff. A signal
condition defines $\mathcal C\subseteq\mathcal P$; the background is
$\mathcal B=\mathcal P\setminus\mathcal C$. These sets are disjoint. For
metric $h$, write $(s_{c,h},n_{c,h})$ and $(s_{b,h},n_{b,h})$ for success and
support counts under that metric's event definition.

The plug-in background mean and prior shapes are

$$
\mu_{b,h}=\frac{s_{b,h}+1}{n_{b,h}+2},\quad
a_h=\tau\mu_{b,h},\quad b_h=\tau(1-\mu_{b,h}),
$$

where $\tau=4$ is the registered shrinkage strength. Only conditional counts
enter the subsequent likelihood:

$$
\theta_h\mid\mathcal C,\widehat\mu_{b,h}
\sim\operatorname{Beta}(a_h+s_{c,h},b_h+n_{c,h}-s_{c,h}).
$$

Thus the same conditional episode is not counted once in a whole-population
prior and again as conditional data. Background observations influence a
plug-in prior mean, not an additional likelihood term. This construction
does not integrate uncertainty in the estimated background mean.
With no background, the rule gives mean 0.5; with no conditional observations,
the implementation reports NO_CONDITIONAL_HISTORY and leaves its conditional
posterior fields unavailable rather than reporting an observed zero rate.
[^bayes-implementation]

**Illustrative:** take background support 18 with 11 successes and conditional
support 4 with 3 successes. Then $\mu_b=12/20=0.6$, $(a,b)=(2.4,1.6)$ and
the posterior is Beta(5.4,2.6), with mean 0.675. Its 95% interval is
approximately [0.339435,0.928893]. Population support is 22; it is not the
number of displayed examples. Despite having a computable posterior, this
metric fails the registered minimum conditional support of five.

### 3.5.3. Interval meaning, readiness and example counts

For positive Beta shapes, an equal-tailed interval uses quantiles at 0.025
and 0.975. The computational convention is documented by
[SciPy's Beta reference](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.beta.html).
It is a model-conditional credible interval for a historical event rate.
It is not a net-return prediction interval, a confidence statement about
an LLM explanation, or proof of calibrated query probabilities. Dependence
between cycles, changing regimes and plug-in hyperparameters limit that
interpretation further.

Readiness adds engineering evidence requirements beyond obtaining a posterior.
In the split gate, population support must be at least 20; a statistic needs
conditional support at least five and interval width at most 0.75. Example
readiness is checked separately using feature/scaler availability and
qualified selections. Gate failure triggers the documented fallback path;
it does not mean that a numerical posterior is zero or that a trade should
automatically be CASH.[^bayes-implementation]

Finally, $K_{\mathrm{ex}}\leq3$ bounds examples shown in a signal-prior prompt.
It is neither $|\mathcal P|$ nor a metric-specific denominator. Bayesian v1
reports empirical counts/rates from its eligible population; that display
must not be silently described as the conditional shrinkage construction
above. Counts, posterior estimates, displayed examples and action policy
are distinct stages.

[^bayes-implementation]: Frozen `core/prior_conditional_statistics.py`, `conditional_metric/compute_conditional_statistics`; `core/prior_quality_gate.py`, `THRESHOLDS/_readiness`; and `core/bayesian_retriever.py` for v1 counts/denominators. CL014–CL016 and source bindings are in the shared ledger. All numerical examples in this section are explicitly illustrative.

## 3.6. Multi-task context and utility

> **Not yet drafted.** Define prior tasks, matured target observations, an unlabeled query, factual buckets and teacher/student roles. Explain why sign probability differs from expected net return, introduce gain/loss magnitudes and utility differences relative to an anchor, and give a clearly labeled numerical illustration.

## 3.7. Temporal validity and evaluation principles

> **Not yet drafted.** State the price/news cutoffs, exclusion of undated news, strict historical-exit condition and reserved-ID rules. Explain purging, row-wise causality versus outer-cutoff compliance, paired upstream and repeated decisions. Define classification/account evaluation units and undefined-denominator handling; add the chronological partition diagram.
