# Appendix C. Algorithms and Configurations

This appendix records configuration values behind Chapters 3–5. **Source**
columns refer to the frozen binding IDs in the shared evidence ledger;
they identify artifacts, not library defaults or newly executed tests.
Numerical settings are grouped by study and resource. The algorithms in
§4.9 remain the complete orchestration pseudocode; this appendix supplies
their numerical and fitting details.[^c-sources]

## C.1. Runtime and hosted requests

| Setting | Component collection | Historical-context collection | Source |
| --- | --- | --- | --- |
| Python | 3.13.5 | 3.13.5 | ED01/ED22; B04c |
| NumPy / pandas / SciPy | 2.1.2 / 2.3.3 / 1.16.1 | Same | B04c/runtime bindings |
| scikit-learn / TA-Lib / Pydantic | 1.7.2 / 0.6.8 / 2.11.7 | Same | B04c/runtime bindings |
| groq / langchain-core / langchain-groq | 0.37.1 / 1.2.17 / 1.1.2 | Same | B04c/runtime bindings |
| Vision / Decision aliases | `qwen/qwen3.8-27b` / `openai/gpt-oss-20b` | Same aliases | Request telemetry |
| Declared / observed temperature | 0 / $10^{-8}$ in SDK metadata | 0 / $10^{-8}$ in wire options | ED01/ED17/ED46; §5.3.1 |
| Maximum output tokens, vision / Decision | 1,024 / 2,048 | 960 / 960 | Collection-specific runtime/request records |
| Language / timeframe | Vietnamese / 1D | Vietnamese / 1D | Same source profiles as §5.3.1 |
| Context transport options | Not inferred from U08 | `n=1`, non-streaming, on-demand, hidden reasoning; vision effort none, Decision low; SDK retries 0 | ED46; §4.10.2 |
| Context repeats / upstream | Separate component panels | Three Decision repeats / one upstream realization per point | ED14; §5.1 |

Aliases do not identify immutable external served weights. A declared
zero temperature is not proof of deterministic hosted generation. The
table describes archived options, not current provider specifications.
Prompt caps and per-request measurements are in [Appendix B.5](B_prompts.md#b5-budgets-repair-and-interpretation).

## C.2. Indicators and alpha transformations

| Stage | Locked setting / interpretation | Source |
| --- | --- | --- |
| Analysis windows | Final 45 bars for charts/Indicator; 600-bar research input for longer history | BG16–BG18; §4.2 |
| MACD | EMA 12 minus EMA 26; EMA 9 signal | BG02/SYS09; §3.3.1 |
| RSI | Wilder-smoothed 14-session gain/loss calculation | Same |
| Slow Stochastic | Raw 14-session range, three-session slow %K and three-session %D | Same |
| Williams %R / ROC | 14-session range / 10-session percentage change | Same |
| Native alpha candidates | 85 total: five custom plus 80 single-stock Alpha101 adaptations; top five reported | SYS03; §4.3.4 |
| Native normalization | `zscore_tanh`, sample dispersion over the full supplied selection window; maximum 600 bars | SYS03 |
| Native score weights | 0.40 normalized absolute IC + 0.35 normalized diagnostic accuracy + 0.25 normalized diagnostic Sharpe | SYS03 |
| Native direction | Strict values above +0.10 bullish / below −0.10 bearish; boundaries neutral; output rounded to four decimals after direction | SYS03 |
| Common normalization | Expanding-prefix, minimum 20 observations; observed-volume mask 300 bars, no lag backfill, six fixed window expressions | BG03/SYS05; §4.3.4 |
| Common selection | At least 60 valid train pairs; validation ≥30 common rows and ≥5 LONGs per admitted candidate; choose five factors and threshold from 0.05/0.10/0.20 | BG03; §4.3.4 |
| Separate numerical factor panel | 23 rules: fixed five, dynamic top five, no-flip, 20 random eligible five-factor sets; strict ±0.1 votes, positive mean LONG, ties CASH | ED23–ED25; §5.4.2 |

The five fixed numerical factors are CURRENT_1_FDM, CURRENT_2_SFA,
CURRENT_3_LVR, CURRENT_4_BFE and CURRENT_5_OFE. Ineligible fixed slots
abstain rather than receiving replacement factors. These numerical
controls are not hosted selector ablations.

For example, the adapted WQ18 handler is

$$
x_{18,i}=-R_{20}^{\mathrm{ts}}\left[
\operatorname{Std}_5(|C-O|)+(C-O)+\operatorname{Corr}_{10}(C,O)
\right]_i.
$$

The trailing rank is a time-series operation with the implementation's
partial-window/strict-comparison rules, not the original cross-sectional
rank. The VWAP input elsewhere is the typical-price proxy $(H+L+C)/3$.
Display templates containing ellipses are not complete executable
formulas. The bound handlers and initialization rules are authoritative;
the thesis does not claim a faithful reproduction of all 101 original
alphas. Full-window normalization and other Native operations retain the
row-wise causal failure described in §5.9.2.

## C.3. HMMs and distinct frozen regime resources

| Primitive setting | Recorded value / rule | Source |
| --- | --- | --- |
| Features | Log return; 20-session sample return volatility; relative MA20/MA50/MA200 distances | BG04/RG01/RG02; §3.4/§4.5.4 |
| Fit requirements | Longest MA 200; at least 300 feature rows; train-only StandardScaler | BG04 |
| Model | Four-state diagonal Gaussian HMM, seed 42 | BG04 |
| EM / numerics | At most 500 iterations; tolerance 0.001; minimum covariance 0.001 | BG04 |
| Quality conditions | Convergence, each posterior occupancy ≥5%, valid trend-state separation and CHOPPY volatility ≥1.1 × the other neutral state | BG04 |
| Naming | Highest train MA200 distance BULL; lowest remaining BEAR; higher-volatility remaining state CHOPPY; last CONSOLIDATION | BG04 |
| Failed fit quality | Recorded MULTI_FACTOR method with train-derived trend/volatility thresholds; no query refit | BG04 |

| Evaluated use | Actual frozen cutoff and support | Source |
| --- | --- | --- |
| Signal-prior query regime | 2 January 2018–30 December 2022; 1,251 price rows, 1,052 feature rows; HMM | RG01 metadata |
| MT queries after 2020 | Final 31 December 2020 resource; 752 price rows, 553 feature rows; HMM | RG02 final timeline entry |
| Early numerical timeline | Fewer than 499 price rows yields UNKNOWN rather than a newly fitted substitute | SYS23/RG02 |
| Bank episode regimes | Their own historical episode-prefix artifacts; stored assignments retained | SYS19/§4.5.4 |

Generic class fit bounds do not replace these artifact dates. HMM scalers
are also distinct from the four-feature numerical scaler and the C2
stock/fold example scaler. EX01's signal regime is CONSOLIDATION while
its numerical MT regime is BULL; the labels are not edited to agree.

## C.4. Retrieval, conditional rates and readiness

| Family / parameter | Recorded value / rule | Source |
| --- | --- | --- |
| v1 population | Same stock, mature exits and matching signal-prior regime | BG07/SYS19 |
| v1 score | Mean agreement of Trend/Pattern/Alpha/Indicator; sentiment not scored | BG07 |
| v1 ordering / K | Descending score, later exit, ascending ID; at most three examples | BG07 |
| C2 statistics / A statistics | Exact T/P/A/I conditional subset / exact T/P subset; background is disjoint within same population | BG05/SYS25; §4.7 |
| Conditional prior | Background mean $(s_b+1)/(n_b+2)$, strength 4; empty background Beta(2,2) | BG05 |
| Interval | Equal-tailed 2.5%/97.5% Beta quantiles; no displayed posterior with zero conditional support | BG05 |
| Example similarity | Four-signal agreement and four-feature proximity weighted 0.5/0.5 | SYS26–SYS27; §4.7.1 |
| Recency / eligibility | Half-life 365 calendar days, age ≤730 days, base similarity ≥0.625 | Same |
| Diversity / maximum | At least five VN-Index sessions between selected decision dates; at most three records; no random backfill | Same |
| Statistics ready | Population ≥20; metric conditional support ≥5; interval width ≤0.75; any passing metric suffices | BG06 |
| Examples ready | Population ≥20, query features/scaler available and nonempty selected list | BG06 |
| B_semantic | Same base evidence/selector/readiness as C2; changed count/interval presentation, no embedding retriever | SYS26–SYS28; §4.7.3 |

Writing $d(e,q)=\sqrt{\frac14\sum_j(z_{e,j}-z_{q,j})^2}$, the C2
example score uses

$$
B(e,q)=0.5S(e,q)+\frac{0.5}{1+d(e,q)},\qquad
\operatorname{score}(e,q)=B(e,q)2^{-\operatorname{age}/365}.
$$

The conditional posterior is

$$
\theta_h\mid\mathcal C\sim\operatorname{Beta}
\left(4\mu_{b,h}+s_{c,h},\,4(1-\mu_{b,h})+n_{c,h}-s_{c,h}\right).
$$

Background counts affect the plug-in prior; only conditional counts enter
the likelihood. Selection restrictions do not remove cycles from the
historical-rate population. `full_prior` projects whichever block is
ready; no visible block inherits the same-repeat Common result. These
rates/intervals are not calibrated query probabilities.

## C.5. Numerical context, teacher and student

| Context construction | Locked value / rule | Source |
| --- | --- | --- |
| Features | Five- and twenty-session returns, twenty-session population log-return volatility, Close/SMA20−1 | BG10; §4.8.2 |
| Scaling | Frozen train mean/population variance; zero-variance scale one; clip standardized features to [−4,4] | TR01 preprocessing/BG10 |
| Scaler fit | 731 observations; cutoff 31 December 2020; latest admitted exit 29 December 2020 | TR01 preprocessing |
| Task identity | Same stock / 63-session VN-Index blocks anchored 2 January 2018; three-session cycle grid | BG08–BG09 |
| Facts bucket | Strict signs of MACD−Signal and Close−SMA20 on the own 45-bar prefix; zero/missing yields UNKNOWN | SYS33/BG09 |
| Prior eligibility / selection | Earlier blocks with ≥2 available observations; regime match priority, centroid distance, later exit and task-ID tie-break | BG09 |
| Context size | At most three priors, at most eight observations per prior; latest at most eight target observations | BG09/TR02 |
| Additional temporal restrictions | Strict mature exits, disjoint observations/holding intervals, reserved IDs excluded and labeled pool frozen before fold's first query | BG09/BG17 |

| Teacher | Locked setting | Source |
| --- | --- | --- |
| Families | 16 Beta components: means {0.2,0.4,0.6,0.8} × concentrations {2,8,32,128} | TR02/TR03/BG11 |
| Fitted quantity | Mixture weights only, symmetric Dirichlet(2,…,2) MAP-EM prior | Same |
| Data / convergence | 48 training tasks / 731 cycles; maximum 1,000 iterations, weight-change tolerance $10^{-10}$; saved convergence 237 iterations | TR03 |
| Inference | Separate prior-task and target count likelihoods; target query label excluded | BG11 |

For $L_h(s,f)=B(a_h+s,b_h+f)/B(a_h,b_h)$,

$$
w_h\propto\pi_h\left[\prod_jL_h(s_j,f_j)\right]L_h(s_T,f_T),
\qquad q=\sum_hw_h\frac{a_h+s_T}{a_h+b_h+s_T+f_T}.
$$

The teacher uses label counts, not numerical feature values, in this
likelihood. Whole feature vectors in synthetic training are resampled
independently of the synthetic family/rate/labels; observed market query
outcomes are not synthetic training targets.

| Student / optimization | Recorded production setting | Source |
| --- | --- | --- |
| Packing | PAIRED_37; six numeric coordinates, three roles, four task slots, 37 positions maximum | TR02 model/BG12 |
| Architecture | Two pre-normalized causal attention blocks; hidden 128, four heads, FF 256, GELU, dropout 0; final LayerNorm and linear scalar head | Same |
| Parameter count / precision | 271,873; FP32; AMP/TF32 disabled | TR02 |
| Label masking | Prior/target markers $(0,0,0,0,-1,1)$; Q has query-label coordinate 0 and missing-label flag 1 | BG12 |
| Model seeds / steps | 17, 42, 73; fresh weights; 5,000 optimizer steps each | TR02/TR01 |
| Batch / episodes | Effective and recorded physical batch 128; 640,000 synthetic episodes per seed | TR02/TR06 |
| Optimizer | AdamW, betas (0.9,0.999), epsilon $10^{-8}$, weight decay 0.01; norm clip 1.0 | TR02 |
| Learning rate | 250-step linear warm-up to $3\times10^{-4}$, cosine decay to $3\times10^{-5}$ at step 5,000 | TR02 |
| Loss | Query-only BCE against detached teacher predictive $q$; no market-query BCE term | TR02/BG12 |
| Fixed validation / test corpora | 5,000 episodes each, including 500-case stress portion; prior order permuted | TR02 |
| Checkpoints | Every 250 steps: 20 per seed, 60 assessed; no metric early stopping | TR01/TR02 |
| Selection gates | Mean KL ≤0.02 nats; p95 absolute error ≤0.10; ≥200 eligible swap pairs and sign agreement ≥0.90; constant-control/technical gates | TR02/TR05 |
| Ranking | Eligible checkpoints: 2021 market macro log loss, macro Brier, earlier step, registered seed order; scores rounded to 12 decimals | TR02/TR05 |
| Evaluated choice | Seed 42, step 3,000; inference CPU, eval/no gradients; not a three-seed ensemble | TR01/TR05 |

The selected tensor digest is
`c60ae9695dde6f308ff30b0f4de7e40539ea5e8353cc7b1e0acb3d57a11f471c`.
Export bytes, resumable optimizer checkpoint and tensor fingerprint are
different identities (TR04/TR07/TR01). The 69-token diagnostic packing
and discarded pilot/preflight weights are not evaluated ensemble members.
Synthetic-only optimization does not mean selection was label-free:
the registered 2021 market labels influence checkpoint ranking.

## C.6. Utility and final action policy

| Quantity / condition | Locked rule | Source |
| --- | --- | --- |
| Support | AVAILABLE context, complete 45-bar facts, known bucket, ≥2 prior tasks and ≥5 positive plus ≥5 nonpositive returns | BG13/SYS33 |
| Draws | 4,096; teacher family/sign posterior and independent Exp(1) magnitude weights | BG13 |
| Utility | $U=\theta g-(1-\theta)\ell$ in net-return fractions; no second cost subtraction | BG13 |
| Quantiles | Linear empirical Q10/Q90; deterministic common component streams, not branch/repeat-specific resampling | BG13 |
| CASH→LONG | Strict $Q_{0.1}(U)>0$ plus validity/eligibility | BG14 |
| LONG→CASH | Strict $-Q_{0.9}(U)>0$ plus validity/eligibility | BG14 |
| Same proposal / unsupported | Retain anchor; record same-action or explicit bypass reason | BG14/SYS42 |

Student probability is recorded alongside utility; the utility draws use
the teacher sign posterior, not substitution of that student number.
The mean's sign alone cannot authorize a revision. None of these model
quantiles certifies economic coverage or future profit, and describing
the sampler here does not regenerate its saved draws.

[^c-sources]: Numeric table rows map to ledger BG/SYS/RG/TR/ED bindings and their detailed locators in §§9.3–9.20 and 10.4–10.6; §13.6 records this appendix's checks. TR02 is read by its TR01.protocol byte pin, not assumed from a current default. C1 reuses the two-collection B04c runtime records; source IDs are resolved by their exact paths in the ledger.
