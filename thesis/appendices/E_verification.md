# Appendix E. Verification and Audits

This appendix separates contract checks, stored audit outcomes and
unfinished acceptance. A PASS result must be read with its tested source,
runtime, data and interpretation. **No runtime suite, counterexample,
economic replay, model inference or cold analysis replay is run to write
this appendix.** Reading and checking a receipt is not rerunning its test.

## E.1. Evidence matrix and status meanings

| Requirement / path | Recorded evidence and scope | Supported interpretation / remaining limit |
| --- | --- | --- |
| Candidate-LONG target and costs | Component `final_contracts_v1/targets.json`: 102 units / 918 classification prediction rows; canonical labels and frozen two-way costs | Different prediction rows are not new hosted calls; account execution certification is separate |
| Target alignment | Same audit: 65 entry Opens differ from the decision Close; seven gross/net labels disagree | Close-to-close or gross direction cannot replace the net execution target |
| Indicator/report contract | `final_contracts_v1/indicators.json`: 102 recorded unit replays, 375 saved Decision requests, zero model calls in that audit | Descriptive frozen-sample checks, not a new inference collection or independent chart truth |
| Outer query cutoff | Native alpha-contract synthetic poison-after-cutoff check PASS; two recorded native backtest fixtures, 85 candidates each | This checks the supplied end cutoff, not causal construction of every earlier row |
| Native row-wise causality | `alpha_contract_v1/leakage.json`: diagnostic PASS_DETECTION, causal gate FAIL | Detecting the failure successfully is not passing causality |
| Shared upstream / dependencies | Frozen shared/forecast contracts, U08 identities and EX01 24-slot timestamps/dependency hashes | Branches reuse one parent and same-repeat dependencies; the barrier does not undo prior historical exposure |
| Prior maturity / resource boundaries | Historical-memory/MT validators and scoped PIT fixtures; reserved IDs and fold-frozen label pool | Necessary local admissibility checks, not authentication of original raw signals or news |
| Prompt / retry / checkpoint | Frozen source and U08 acceptance: maximum 4,750 Decision characters including repair and three HTTP attempts per execution | Historical U08 scope; neither character count nor slot attempts certify every component override |
| U08 integrity / completion | PASS_U08_ACCEPTANCE; 718 source pins; 102 points, 2,448 slots; no new inference in acceptance | Coverage/integrity receipt, not whole-system causal or financial acceptance |
| U09 cold replay | PASS_U09_COLD_REPLAY; 15 byte-identical artifacts; zero new API calls; training false | Historical offline reproducibility under its runtime/inputs, not deterministic future hosted replies |
| Application acceptance | OFFLINE_PASS_BROWSER_PENDING; F11 false; desktop/mobile NOT_RUN | Fixture/source checks do not complete browser or live execution acceptance |

The component contract report explicitly records `code_changed=false`,
`new_llm_api_jobs=0` and `new_predictions=0`. Its target, indicator and
risk scopes remain distinct. The manifest's queue signature identifies
the source collection; it does not create an untouched holdout.
[^e-contracts]

## E.2. Retained Native row-wise counterexamples

The following vectors are **stored synthetic audit outputs**, rounded to
six decimals. The left vector is the earlier prefix; the right shows
values for those same earlier rows after the prefix is extended. No
audit is regenerated here. All three normalizers change old values.

| Normalizer | Earlier-prefix historical values | Same rows after prefix extension | Changed |
| --- | --- | --- | --- |
| zscore_tanh | [-0.821656, -0.369029, 0.369029, 0.821656] | [-0.447409, -0.428885, -0.409993, -0.390743] | True |
| minmax | [-1.000000, -0.333333, 0.333333, 1.000000] | [-1.000000, -0.979798, -0.959596, -0.939394] | True |
| rank | [-0.500000, 0.000000, 0.500000, 1.000000] | [-0.600000, -0.200000, 0.200000, 0.600000] | True |

For example, the fourth zscore-tanh value changes from 0.821656 to
−0.390743 even though it refers to the same historical position. The
record additionally reports `delay_bfill_changes_past=True` and
`global_volume_branch_changes_past=True`. These are construction
counterexamples, not evidence that the outer query necessarily read
beyond its final cutoff. The outer poison test retains its own PASS.

The saved summary result is `PASS_CONTRACT_AUDIT`, while
`native_rowwise_causal_gate=FAIL`. Its manifest reports 2,331 frozen-source
hash checks before/after, `network_or_inference=false` and
`runtime_modified=false`. These statements identify the old audit's scope;
they do not say the appendix reruns those checks or that unchanged bytes
make the algorithm causal. Correcting the implementation requires a
separately versioned study rather than relabeling this failure.
[^e-native]

## E.3. Provenance and unfavorable records retained

The unified manifest retains
`whole_system_causal_gate=NOT_CERTIFIED_HISTORICAL_EXPLORATORY` and
Native FAIL. The bank/query audit reports numerical return differences
above its threshold in **828 of 852** records, with maximum absolute
difference **0.04298848884252138 pp**. This is not a count of 828 changed
labels and does not authorize retroactive relabeling. Original raw signal
journals are unavailable. Price/news hashes identify what was stored;
they do not independently prove contemporaneous availability or vendor
adjustment correctness.

EX01 retains contradictory signal-prior/MT regimes, missing sentiment,
conditional-prior bypasses and the MT `KEEP_PROPOSED_SAME` path. Its LONG
has positive gross return but negative net return after costs (§4.10.5).
An invalid-assertion reply illustrated in §4.8.1 resolves through the
documented Common dependency; it is a contract example, not an additional
successful historical forecast. A missing/transport-failed reply must not
be silently promoted to a valid CASH or fallback action. These distinctions
preserve the difference between counterexamples, valid bypasses and
technical failures.[^e-provenance]

## E.4. Receipt-bound checks and what was not rerun

U08's acceptance source commit is
`69935d71b469d0a34ef8959ca598e1cee791f7ac`. Its stored acceptance timestamp
is `2026-11-12T03:17:37.298613+00:00`; the collection seal is
`2026-11-12T03:10:18.266468Z`. These UTC timestamps describe historical
receipt events, not financial-data availability dates.

**Table E2. Test groups explicitly reused in U08 acceptance.** Counts
are taken from `prior_checks`; they are not disjoint totals or a new
whole-unit-suite count. Every row has `rerun=false` in that receipt.

| Prior check group | Tests previously passed | Python files previously compiled | Rerun in acceptance |
| --- | --- | --- | --- |
| live | 69 | 11 | False |
| model_quota | 61 | 5 | False |
| provider_quota | 41 | 5 | False |
| point_restart | 44 | 6 | False |
| slot_restart | 40 | 4 | False |

U08 acceptance separately records blocked constructors/network and zero
new inference. U09's cold-verification record binds runtime digest
`cf743125ee3b7da792b6d37b4d5ac95c753fce334e914ef9e0c51e4081a89b2a`,
the U08 archive digest and fifteen byte-identical artifacts. Its full
source snapshot is historically restored at commit
`384725a66fec074700963fac67c358b28b842092`. These are different identities
from the live application and current thesis-writing commit.

The repository's reference gates cover compilation, unit tests,
deterministic end-to-end behavior and leakage checks. Their names do not
justify asserting that all four ran at every document revision. A release
or changed runtime needs the applicable source-bound evidence; this
writing task checks documents and source identities only. Native FAIL
and whole-system NOT_CERTIFIED remain visible alongside successful local
PIT, economics, paired and recovery checks.[^e-receipts]

## E.5. Application and missing experimental acceptance

The separately pinned application receipt is
`serving_integration_acceptance_v10`, base commit `6ad73e7a`, with
135 Python checks, 24 DOM checks, 23 compiled Python files and two
JavaScript syntax checks recorded. Its history/source-reuse rules mean
these counts must not be presented as reruns after every edit.
`f11_complete=false` and desktop/mobile browser acceptance is NOT_RUN.
The author's statement of equivalent research behavior for the three
identified live modules is retained, while raw presentation-source and
wire identities remain separate.

Matched retrieval-only, statistics/examples/no-regime, plain revision,
no-target, no-utility and isolated student/teacher interventions are not
completed by these engineering checks. Likewise, scenarios based on
daily bars provide no execution-certified fills, and browser acceptance
would not itself prove profitable prospective trading. [Appendix F](F_reproduction.md#f2-read-only-inspection-and-scoped-archive-restoration) states
the offline reproduction and application paths without turning them into
new acceptance claims.

[^e-contracts]: Archived `final_contracts_v1/report.json`, `targets.json` and `indicators.json`; frozen shared/provider/oracle contracts and EX01 stage records. Ledger §§9.2/9.19–9.21/10.13/13.8 identifies scopes and source-byte checks.
[^e-native]: Archived `alpha_contract_v1/{manifest,summary,cases,leakage}.json`, bound by the revision index; frozen SYS11/SYS12. Ledger §13.8 lists these exact file hashes. PASS_DETECTION and FAIL describe different propositions.
[^e-provenance]: ED15 unified manifest `provider_support.bank_audit`, `quality_limits` and causal fields; original EX01 and negative-case records in §§4.8/4.10/5.8–5.9. No bank labels or raw explanations are repaired during writing.
[^e-receipts]: ED08/ED09 U08 acceptance/receipt, frozen `evidence/u09_cold_verify.json` and `evidence/f01_restore_smoke.json`; AP16/AP17 separate application receipt/QA archive. The pinned records are inspected; their historical tests/replays are not rerun here.
