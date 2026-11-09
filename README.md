# A Multi-Agent Large Language Model Approach to Price-Driven Stock Trading in the Vietnamese Stock Market

Research code for a LangGraph stock-direction system for the Vietnamese market.
The original pipeline combines technical indicators, chart-pattern and trend
analysis, quantitative alpha factors, Vietnamese financial-news sentiment, and
a structured `LONG` or `SHORT` decision. Optional Bayesian priors and MT-BICL
modules provide historical context and policy controls for research comparisons.

## Economic contract

`LONG` buys at `Open(t+1)` and liquidates at `Close(t+3)`, using trading-session
positions. `SHORT` keeps cash. Both legs apply a 0.25% brokerage fee and 0.10%
slippage. Accounts start at VND 50,000,000 and compound independently;
the mean of account returns is not a portfolio return. Stock prices in thousands
of VND are converted once for accounting.

`core/backtest_engine.py:compute_round_trip_net_return` defines the net-return
oracle. Canonical target records use `net_cycle_v1`; legacy records retain their
unverified status. Risk ratios report their return frequency and convention,
with undefined values represented as `null`. Sparse cycle returns must not be
annualized as daily returns.

## Architecture

1. Indicator, Pattern, and Trend agents prepare shared upstream reports.
2. Alpha/Sentiment produces the enabled factor and dated-news reports.
3. Each comparison branch receives a deep copy of the shared upstream state.
4. Decision consumes distilled reports and optional historical context.
5. Outcomes are evaluated separately from forecast inputs and checkpointed.

The native ablations are `full`, `alpha_only`, `sentiment_only`, and `baseline`.
Bayesian modules support regime-conditioned retrieval, conditional statistics,
price-pool and semantic variants. MT-BICL adds numeric context, a student,
an anchor decision, posterior utility, and policy vetoes. Native and common
prompt profiles are distinct; disabling a prior does not establish native parity.

The CLI/web default `decision_profile` is `original_fix_serving_v1`: native
reports, caps, schema and model options, with a pre-inference character guard.
Requests of 6,500 characters or more fail instead of being silently recapped.
Oversized historical native requests are limited to frozen offline replay.
`integrated_default_v1` retains the existing research report caps; research
common prompts and prior settings remain explicit configurations.

Historical features use at most 600 candles ending at the query cutoff.
Research news excludes unavailable and undated items, and memory episodes
must exit strictly before the query date. The native alpha selector has a known
row-wise causality limitation: outer query cutoff compliance does not establish
causal preprocessing or an unbiased walk-forward study. See the preserved
revision audits before interpreting empirical claims.

## Upstream attribution

This repository adapts [QuantAgent, now maintained as QuantHarness](https://github.com/Y-Research-SBU/QuantHarness),
by Y-Research @SBU. Its indicator, pattern, trend and decision agents,
chart-analysis tools, LangGraph structure and parts of the web interface form
the upstream foundation. Vietnamese-market data and sentiment, alpha
integration, execution accounting and the paired research workflow extend it.

See [Third-party notices](THIRD_PARTY_NOTICES.md) and the preserved
[MIT license and copyright notice](LICENSES/QuantAgent-MIT.txt). The source
comparison is pinned to `92519f806286192345e940e7ab77496462d662b7`; the exact
upstream commit originally adopted was not recorded. These notices do not
assign a blanket license to project additions, datasets or model weights.

## Installation

Python **3.13.5** is pinned in `.python-version`. Windows examples:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The runtime uses TA-Lib, PyTorch, Transformers, LangGraph, LangChain, HMMlearn,
and scikit-learn. `vnstock==4.0.9` and `vnai==2.6.2` use the declared vendor
index; see [market-data setup](docs/vnstock_upgrade.md). The integration lock
is `requirements-unified.lock.txt`; use it with `-r` for the recorded Windows
package versions. Unix deployment needs its own platform lock. Historical revision environments retain
their own source and dependency pins in `revision/` and evidence manifests.

Supply `GROQ_API_KEY` through the web interface or process environment.
Sentiment supports `VISOBERT_BACKEND`, `VISOBERT_DEVICE`, optional `HF_TOKEN`,
and `HF_INFERENCE_ENDPOINT_URL`. A `.env` file must be explicitly loaded by
the chosen launcher; importing an agent does not load credentials. Never
commit `.env` or keys. The local ViSoBERT model can require an initial download.

## Running and validation

```powershell
py -3.13 web_interface.py
```

Open `http://127.0.0.1:5000`; `PORT` overrides the port. Live analysis and
walk-forward backtesting use provider data and hosted models. Research
entrypoints under `scripts/` require their own protocol, input, runtime and
release checks. Preserve checkpoint identities when resuming a run.

Select checks for changed contracts and their callers, for example:

```powershell
py -3.13 -X utf8 -m unittest discover -s tests -p "test_account_risk.py" -v
py -3.13 -X utf8 -m unittest discover -s tests -p "test_target_contract.py" -v
py -3.13 -X utf8 -m unittest discover -s tests -p "test_paired_protocol.py" -v
```

The complete offline regression commands are available for an explicit
system-wide acceptance run:

```powershell
py -3.13 -m compileall agents core data_manager scripts tests utils
py -3.13 -X utf8 -m unittest discover -s tests -v
py -3.13 scripts/run_end_to_end_test.py
py -3.13 -X utf8 -m unittest discover -s tests -p "test_*leakage.py" -v
```

Decision research prompts must remain below 6,500 characters and the K=3
prior prefix at most 600 characters. Retry and checkpoint wrappers track
attempts; an unresolved attempt must not be silently reissued or scored as cash.

## Unified experiments

The shared experiment registry and offline result viewer are available at
`/experiments`. It defaults to `original_fix` and identifies six research
methods plus the Fact_Anchor dependency. The existing native backtest remains
available at `/backtest`; research selections do not grant hosted inference.

```powershell
py -3.13 -I -X utf8 scripts/run_unified_experiment.py registry
py -3.13 -I -X utf8 scripts/run_unified_experiment.py validate path/to/spec.json
py -3.13 -I -X utf8 scripts/run_unified_experiment.py replay path/to/bundle.json --sha256 <full-bundle-sha256>
py -3.13 -I -X utf8 scripts/run_unified_experiment.py verify outputs/unified_integration/<run-id>
py -3.13 -I -X utf8 scripts/run_unified_experiment.py export outputs/unified_integration/<run-id> --format csv --output table.csv
```

`ExperimentSpec` locks variants, dependencies, cohort order, repeats,
realizations, serving options, source/resource hashes, runtime, calendar,
costs and missing-support policy. `SharedSnapshot` seals raw reports, images,
factors and PIT provenance; each branch receives a copy. `UnifiedRunner` uses
the existing RunBook and accounting engine, opens outcomes after all required
forecasts are durable, and retains raw proposals separately from final policy.
Accounts reset by symbol/fold/realization/repeat. Undefined metrics remain null.

For an existing verified asset provider, `MethodAdapters` accepts lazy bank,
regime, facts and context factories. It delegates to the existing request and
MT policy primitives. Pass `runner.forecasts_done` to the gated ContextBank;
native/common OFF paths do not initialize these resources. Resource paths and
hashes belong in `resource_sources` and `source_hashes` in the spec. The
`snapshot_from_graph` adapter validates a 600-bar prefix before sealing it.

The CLI replay bundle contains `spec`, `snapshots`, `preparations`, `responses`
and separate `outcomes`. Replay reconstructs prompts, schemas, policy and
accounting from the locked assets. It is conditional on the recorded retrieval
and numeric preparations; it does not rerun retrieval, load student weights,
or regenerate hosted responses. A new release must separately validate the
asset providers, cohort, quota and transport. Existing historical runners and
archives retain their original identities and are not relabelled as new runs.

## Causal alpha profile

`causal_common_v1` provides a separate alpha profile with the same 85 formula
handlers and explicit causal operator changes. It removes backward filling,
full-series normalization, global volume proxy selection and six window sizes
that depend on the input length. Warm-up and missing-volume observations are
masked. Normalization uses expanding prefixes; it keeps a fixed history origin
instead of resetting to a rolling 600-bar origin.

The selector learns orientation on train only, selects five IDs and a threshold
on purged validation support, and freezes them before the test window. Labels
call the canonical round-trip oracle; selection scores use LONG/CASH cycles.
Artifacts pin source, runtime, schedule, prices, costs and the full validation
search. Loading replays the train/validation fit; prediction rejects changed
training prices, future rows, a shifted origin or unavailable selected factors.

```powershell
py -3.13 -I -X utf8 scripts/manage_causal_profile.py fit --prices prices.json --schedule schedule.json --output outputs/unified_integration/<new-run>/selector.json
py -3.13 -I -X utf8 scripts/manage_causal_profile.py verify --prices prices.json --selector outputs/unified_integration/<new-run>/selector.json
py -3.13 -I -X utf8 scripts/manage_causal_profile.py predict --prices prices.json --selector outputs/unified_integration/<new-run>/selector.json --cutoff YYYY-MM-DD --output outputs/unified_integration/<new-run>/prediction.json
```

The input is explicit daily OHLCV in CSV or JSON column lists. Schedule fields
are `train_start`, `train_end`, `validation_start`, `validation_end`, `test_start`
and `test_end`; create a fresh output directory first. The `bridge` command also
accepts `--snapshot`, `--decision` and `--output` to compare native and causal
common requests without model calls.

An experiment uses `unified_experiment_v2`, `input_profile: causal_common_v1`
and a `causal_sources` map from `symbol/fold` to `prices` and `selector` paths,
both bound in `source_hashes`. The raw upstream still shares its last 600 bars.
The runner verifies and seals the causal alpha projection from the anchored
history once per point, uses it for every common method, and preserves the
native request on the same raw parent. V1 specs retain their original profile;
they cannot silently receive a causal snapshot. New record/profile versions
identify the bridge in JSON and CSV.

V2 anchor source cards hash the rendered request and reply content. Full-file
provenance hashes remain in the snapshot and dependency ledger; they are not
fed back into the prompt through a source-card token. This keeps prepared
requests invariant when only post-cutoff prices or audit metadata change.

This is an alpha-only causal contract. It does not certify news availability,
universe, HMM/scaler or retrieval/student provenance, execution quality, or
whole-system zero leakage. Those providers and the comparison protocol still
need their own release checks. Native row-wise causality remains FAIL, and
neither profile grants hosted collection or a claim of statistical superiority.

## Repository and evidence

- `agents/`, `utils/`: agents, graph assembly, prompts, charting and contracts.
- `core/`, `data_manager/`: accounting, PIT inputs, priors, MT-BICL and research adapters.
- `scripts/`, `tests/`: entrypoints, offline audits and regression checks.
- `paper/`, `revision/`: manuscript sources, generation tools and research policies.
- `outputs/revision/`: frozen evidence, including historical source snapshots.
- `docs/plan/`: protocols, checklists, acceptance records and evidence indexes.
- `templates/`, `web_interface.py`: Flask interface.

Frozen evidence and historical source files are read-only research inputs,
not additional live engines. Some model/data assets remain local and are not
recoverable from a source checkout alone. Replay needs the original hashes,
runtime, inputs and archive resolver. A historical receipt certifies its own
snapshot, not later source changes. Hosted responses are not guaranteed to
reproduce across serving epochs, and exposed historical data do not establish
prospective superiority.

This research simulator does not certify exchange fills, vendor price quality,
taxes, liquidity, or complete production execution behavior.
