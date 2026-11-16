# Appendix A. Data and Temporal Contracts

This appendix specifies the compact interfaces behind §§3.1–3.2, §3.7
and §4.2. Field names and version strings retain the locked implementation's
spelling. Tables summarize contracts; they are not newly issued executable
schemas. Examples are projections of stored records unless explicitly
identified as complete. The historical study and current presentation layer
retain separate source identities.

## A.1. Identity, working state and sealed input

The historical context run is identified by `unified_experiment_v1`.
Its shared document uses `shared_snapshot_v1` or
`shared_snapshot_causal_v1`; the latter identifies an embedded Common-alpha
projection, not a certificate that Native or the whole system is causal.
A graph working state may contain operational fields that are deliberately
absent from this sealed forecast input.[^a-source]

**Table A1. Shared-document contract.** The five reports are required
nonempty strings. Optional payload fields must still pass their own
identity, availability and primitive-JSON checks.

| Object / fields | Recorded contract | Boundary |
| --- | --- | --- |
| `point.id`, `symbol`, `cutoff`, `fold`, `quality` | Exact stock/date/fold identity and declared research quality | A date alone does not identify a price source or profile |
| `realization` | Nonnegative native integer; the study uses upstream realization 0 | Decision repeat is a separate downstream index |
| `payload.stock_name`, `as_of_date`, `is_backtest`, `time_frame`, `language` | Must agree with point; historical profile is `True`, `1d`, `vi` | English thesis prose is not a claim that the historical prompt was English |
| `indicator_report`, `pattern_report`, `trend_report`, `alpha_report`, `sentiment_report` | Five nonempty report strings in the payload | Text may contain warnings; nonempty text is not verified financial truth |
| Optional `pattern_image`, `trend_image`, `alpha_factors`, `sentiment_data`, `price_prefix`, `causal_alpha` | Whitelisted fields only, with primitive finite JSON values | Additional graph fields are not automatically admitted |
| `price_prefix` | `Datetime`, `Open`, `High`, `Low`, `Close`, `Volume`; aligned lists, unique ordered dates, exact cutoff end, at most 600 rows | Provider requires 600 clean rows; the final 45 supply chart/Indicator input |
| `provenance` | Exactly `source_sha256`, `upstream_sha256`, `price_end`, `news_dates` | Hashes identify different objects; news dates and price end must pass cutoff checks |
| Sealed representation | Canonical finite JSON bytes; every branch decodes a fresh document | Editing a branch copy does not mutate another branch's parent |

The recursive forbidden-key check excludes query outcomes and prior/Decision
material, including `entry_date`, `exit_date`, `entry_open`, `exit_close`,
`net_return`, `r_net`, `label_net`, `query_y`, `target`, `evaluation`,
`decision_prompt` and `bayesian_prior_context`. This list is representative;
the frozen `FORBIDDEN` set is authoritative. Historical labels are admitted
later only through their separate, maturity-checked context interfaces.

The following **identity projection** comes from EX01's stored shared
stage. It omits reports, prices, images and provenance; it is not a complete
document that could be submitted to the snapshot constructor.

```json
{
  "version": "shared_snapshot_causal_v1",
  "point": {
    "cutoff": "2023-07-03",
    "fold": "b2023_h2",
    "id": "FPT-2023-07-03",
    "quality": "U08_HOSTED_HISTORICAL_EXPLORATORY",
    "symbol": "FPT"
  },
  "realization": 0
}
```

The sealed content digest for EX01 is
`e6c16c36dd776a804922f466af1c9742bf3ba70015d60929e4112992e269a103`.
It is distinct from the archive-member digest and the Native-parent digest.
The forecast record binds those identities separately.

## A.2. A completed historical episode

The schema `urn:kltn:historical-task-record:1` uses JSON Schema draft
2020-12, rejects additional fields and requires the eight top-level groups
below. Its recorded symbol enum is **FPT, VNM, VCB, MWG**. It is a
CORE4 signal-memory schema, not a nine-stock coverage claim. Date formats
and JSON types alone cannot enforce economic consistency or
`exit_date < query cutoff`; application validation supplies those checks.
[^a-episode]

| Field group | Required representation | Application meaning |
| --- | --- | --- |
| `episode_id`, `symbol` | Nonempty ID and admitted stock | Unique historical cycle identity |
| `as_of_date`, `entry_date`, `exit_date` | ISO dates | Decision, following observed open, third following observed close |
| `regime` | BULL, BEAR, CHOPPY or CONSOLIDATION | Stored market assignment, not the future return label |
| `agent_signals` | Required nonempty strings: `trend`, `pattern`, `alpha_consensus`, `indicator_consensus`, `sentiment` | Historical signals; aliases/normalization follow the loader, not a keyword search over prose |
| `outcome.actual_direction`, `net_return_pct` | UP/DOWN and finite numerical percentage | Candidate-LONG result under the common oracle |
| `outcome.was_bull_trap`, `result` | Native Boolean and WIN_IF_LONG/LOSS_IF_LONG | Trap convention uses historical bullish Trend/Pattern and a nonpositive net result |

This complete stored bank record is the first selected signal example in
EX01. Its exit precedes 3 July 2023. Reproducing its stored value does not
resolve the bank/query price-provenance discrepancy discussed in §5.9.2.

```json
{
  "episode_id": "FPT:2022-04-07",
  "symbol": "FPT",
  "as_of_date": "2022-04-07",
  "entry_date": "2022-04-08",
  "exit_date": "2022-04-13",
  "regime": "CONSOLIDATION",
  "agent_signals": {
    "trend": "BULLISH",
    "pattern": "BULLISH",
    "indicator_consensus": "BEARISH",
    "alpha_consensus": "BULLISH",
    "sentiment": "NEUTRAL"
  },
  "outcome": {
    "actual_direction": "UP",
    "net_return_pct": 0.8800636494421088,
    "was_bull_trap": false,
    "result": "WIN_IF_LONG"
  }
}
```

Numerical MT context has a different representation: prior datasets,
target observations, feature/scaler identities and an unlabeled query.
The schema and validators in `mt_bicl.schema.json` and
`core/mt_bicl_contracts.py` govern that path. Its task count is not a
count of the signal records above, and its historical label pool is
additionally frozen before the first query of the fold (§4.8.2).

## A.3. Time mapping and economic labels

| Boundary | Required relation / mapping | EX01 or scope |
| --- | --- | --- |
| Query price cutoff | Included bar dates ≤ cutoff; exact cutoff observation required | 3 July 2023 |
| Half-open engine window | End index $e=t+1$; input $[e-W,e)$ excludes entry | Chart window $W=45$; longer prefix 600 |
| News | Recorded publication **and protocol-defined availability** ≤ cutoff; undated news excluded | An empty eligible set is unavailable news |
| Historical outcome maturity | Exit strictly before cutoff; equality is excluded | Further universe/reserved-ID/fold-freeze rules also apply |
| Candidate entry / exit | Open at $t+1$; Close at $e+L-1=t+3$, $L=3$ observed sessions | Entry 4 July, middle session 5 July, exit 6 July 2023 |
| Forecast barrier | Required forecasts/policy outputs durably complete before query outcome is joined | Context protocol requires 24 slots per point |
| Future evaluation | Actual entry/exit prices and query label remain in the separate outcome stage | Scheduled/outcome dates are not fields in the sealed report payload |

With per-leg brokerage $f=0.0025$ and slippage $s=0.001$, the common oracle is

$$
r_t^{\mathrm{net}}=\frac{C_{t+3}}{O_{t+1}}
\frac{(1-s)(1-f)}{(1+s)(1+f)}-1,
\qquad y_t=\mathbf1\{r_t^{\mathrm{net}}>0\}.
$$

This is a study convention, not current venue regulation. UP requires
strictly positive unrounded return; DOWN includes zero. Raw SHORT maps to
the final action CASH and earns zero under the reference contract, not a
short-sale payoff. `net_return_pct` is a percentage, while outcome `r_net`
is a fraction. Account compounding and repeat/account aggregation are
separate from this one-cycle label.

## A.4. Missingness, failure and serialization

| Stored state | Correct interpretation | Incorrect substitution |
| --- | --- | --- |
| `sentiment_data.is_unavailable=True` | No admitted observation under the news contract | An observed neutral score |
| Missing/unknown publication date | Excluded from eligible news | A publication at the query cutoff |
| Nonfinite indicator or warm-up gap | Missing/error under its calculation contract | A genuine zero indicator |
| Conditional view not ready | Follow the declared same-repeat dependency; record fallback | A fresh prior-informed reply |
| MT query/utility unsupported | Retain resolved anchor with bypass reason | A rejected raw response that was never requested |
| Missing required response, corrupt hash or malformed schema | Technical failure/incomplete stage | A completed valid CASH decision |
| `NA` / JSON `null` metric | Preserve missing/undefined reason and denominator | A numerical zero or an omitted adverse row |
| Zero net return | DOWN label and zero candidate payoff | A missing value or UP |
| NumPy scalar, NaN or infinity in a return document | Convert intentionally at the producer or reject; sealed JSON admits native finite values only | Silent acceptance by the snapshot serializer |

The outer cutoff and these checks establish local contract properties.
They do not overturn Native row-wise causal **FAIL**, authenticate the
original bank/news production process or certify whole-system causality.
Appendix E records those audit scopes explicitly.

[^a-source]: Frozen `core/unified_contracts.py`, input providers and EX01 shared/prepare/forecast stages; ledger BG16–BG18, SYS44–SYS47, §9.2 and §13.4. The exact shared-stage identity and member hashes are checked against U08, not reconstructed by running agents.
[^a-episode]: Frozen `docs/plan/week1/historical_task_record.schema.json`, `data_manager/regime_memory_store.json`, canonical economic oracle and MT schema/contracts; ledger §3, §7, §9.8–§9.12 and §13.4. Schema checks, economic verification and historical availability are separate forms of evidence.
