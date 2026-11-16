# Appendix F. Reproduction and Application

This appendix supplies resource identities, working directories and
source-checked command examples. Commands are instructions for a later
operator; they are **not newly executed experiments or acceptance results**
in this thesis-writing task. Reading saved artifacts, recomputing an
offline analysis, numerical model inference and hosted live analysis are
different operations. [Appendix E](E_verification.md#e1-evidence-matrix-and-status-meanings)
states the scope of the historical receipts.

## F.1. Inputs, source and model identities

| Role | Repository-relative path | Bytes | Outer SHA-256 |
| --- | --- | --- | --- |
| U09 saved results | `docs/plan/week12/unified_analysis_results.zip` | 1383945 | `e168d1d59218804d1f587fcb342d02c4e7bafbb963162eddae706039a00769a9` |
| U08 hosted collection | `docs/plan/week12/unified_live_research.zip` | 78438700 | `5936bc971bebf1b139a34b93f154ad8e54d0a0e37fdaa6ac4673295f8b60a11c` |
| Frozen source/model snapshot | `docs/plan/week12/final_evidence_snapshot.zip` | 93154448 | `80fed8c9a1c265098a394bfc40f13d7f0266c1e05abdb142fba01d873cb8b8b5` |
| U09 acceptance | `docs/plan/week12/unified_analysis_acceptance.json` | 5064 | `6b435c21c89000775be1f1e1d043b6b3429a0729f37efc16f4bd03be92355456` |

The U09 ZIP contains `outputs/unified_integration/u09_analysis_r1/`:
results/receipt JSON, summary/contrast/bridge/per-repeat CSVs, prediction
and group-classification CSVs, accounts/cycles/daily-NAV CSVs, prior traces
and saved report/plot outputs. Its fifteen reproducible artifacts are
bound by the receipt; archive manifests and receipt files are not counted
as new independent analysis observations.

U08 retains shared/render/graph, prepare, raw/forecast/policy and outcome
stages with request/dependency identities. The source/model snapshot has
its own manifest and historical source commit
`384725a66fec074700963fac67c358b28b842092`. U08's acceptance source commit
`69935d71b469d0a34ef8959ca598e1cee791f7ac` identifies a different scope.
Neither commit is a promise that the current live files are byte-identical.

Additional resources are:

| Resource | Path / identity | Purpose and prerequisite |
| --- | --- | --- |
| Frozen comparison assets | `docs/plan/week12/unified_comparison_assets_v2.zip`, SHA-256 `d5c4f1bc31c1a95d9e685a9cc13d1f86ce2d3cc0105b9023561fd5f567e2d8c4` | 286 checked price/provider/selector assets; not hosted predictions |
| Protocol / asset manifest | `unified_comparison_protocol_v2.json` / `unified_comparison_manifest_v2.json` under `docs/plan/week12/` | Study schedule, profile/domain/source bindings and explicit validity limitations |
| Runtime | `docs/plan/week12/unified_analysis_runtime.json`, `unified_live_runtime.json`, `requirements-unified.lock.txt` | Keep the appropriate recorded analysis, hosted and platform environments distinct |
| Revision archive index | `docs/plan/revision_evidence/index.json`, SHA-256 `cc4400dadc585b6b0dd5dd3a012f1f510a994347b9395cdbbcc721cc9f2b9599` | Maps original release paths to verified ZIP chunks; a path need not be unpacked on disk |
| Baseline export | `outputs/revision/final_baselines_v1/manifest.json`, SHA-256 `0a20fbe49049dd61fae2eb8bf3289f65039395e6bcac6745b851a5a00d804226` | Eleven pinned output files, including the component classification/financial tables |
| Student export | Snapshot `outputs/bayesian_benchmark/mt_bicl/replicas/full_r1/model/candidate.pt`, SHA-256 `a6f0d294b6f731bfc630fe58631b921ec2f0877338745a84e9459ec6a248e702` | Selected seed 42 / step 3,000; exported model differs from resumable optimizer checkpoint |
| Teacher | Same snapshot namespace `model/teacher.json`, SHA-256 `c0a39f327bacd8636fd7edff2f19b30799581bd144ac28176a7cd97fe9dbc335` | Frozen numerical count model; no hosted teacher call |
| Numerical regime timeline | Same snapshot namespace `inputs/regime_models.json`, SHA-256 `5df0307a70b3df177a43faba8be04a72c00dabcb422c0b1c66a4b76cd84e724d` | Separate from the end-2022 signal-query HMM resource |

A file hash proves stored identity, not source authenticity or permission
to replace missing data with a new vendor download. Missing local-only
chunks, model assets or historical inputs are explicit prerequisites;
they must not be silently regenerated from current prices. The final
self-contained thesis source/release package is a later deliverable.
[^f-resources]

## F.2. Read-only inspection and scoped archive restoration

The following examples use **PowerShell from the repository root**, where
`scripts/`, `docs/` and `outputs/` are siblings. Python 3.13.5 is the
recorded interpreter; a `py -3.13` launcher must resolve to that patch
version for a strict replay. A standard-library-only archive read has
fewer dependencies than the full historical environment.

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath docs/plan/week12/unified_analysis_results.zip
py -3.13 -X utf8 scripts/revision_evidence.py verify alpha_contract_v1
```

The first command reports the outer hash for comparison with F.1. The
second checks one named archived release through its index/chunks without
running the alpha audit. Its CLI uses a positional release name, not a
`--prefix` option. It can fail if a required chunk is missing or modified.

To inspect the saved ten-method U09 summary without model dependencies,
credentials or extraction, use this separate standard-library command:

```powershell
@'
from pathlib import Path
import csv, hashlib, io, json, zipfile
path = Path("docs/plan/week12/unified_analysis_results.zip")
assert hashlib.sha256(path.read_bytes()).hexdigest() == "e168d1d59218804d1f587fcb342d02c4e7bafbb963162eddae706039a00769a9"
name = "outputs/unified_integration/u09_analysis_r1/summary.csv"
with zipfile.ZipFile(path) as archive:
    manifest = json.loads(archive.read("manifest.json"))["members"]
    raw = archive.read(name)
    assert hashlib.sha256(raw).hexdigest() == manifest[name]["sha256"]
rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))
assert len(rows) == 10
for row in rows:
    print(row["method"], row["n_points"], row["mean_account_return_pct"])
'@ | py -3.13 -X utf8 -
```

If unpacked audit files are needed, the following optional command
**writes a separate destination**. It preserves archived bytes and refuses
to overwrite conflicting files; it does not execute the restored audit.

```powershell
py -3.13 -X utf8 scripts/revision_evidence.py restore alpha_contract_v1 --destination tmp/thesis-offline-review
```

The restored path is
`tmp/thesis-offline-review/outputs/revision/alpha_contract_v1/`, because
the destination is a root for the original relative paths, not a flat
output folder. Further release names can be inspected with
`scripts/revision_evidence.py list`; the entire archive need not be restored.

## F.3. Historical offline replay requires the matching checkout

Strict replay requires the recorded code, input bytes and numerical
environment. A Git checkout alone does not provide ignored/local-only
resources. Use an isolated historical checkout, hydrate the pinned source
and data/model assets from the declared packages and follow the recorded
restore bindings. The live Indicator/Decision/graph presentation changes
must not be relabeled as identical historical raw source. Source-check
failure should identify a mismatch, not trigger weakening an expected hash.

**In that isolated historical repository root**, the U06 asset commands are:

```powershell
py -3.13 -I -X utf8 scripts/prepare_unified_comparison_v2.py restore
py -3.13 -I -X utf8 scripts/prepare_unified_comparison_v2.py verify
```

`restore` hydrates declared asset paths from the pinned package; `verify`
checks the prepared source/runtime/resource contract. These are not
`replay-numeric`, fresh asset fitting, a hosted collection or a new
training run. Full numerical replay is a separate CPU operation with its
own additional model/selector prerequisites.

The statistical cold-replay entrypoint is:

```powershell
py -3.13 -I -X utf8 scripts/unified_analysis/run.py verify
```

This `verify` command is more than reading hashes: it regenerates the
analysis artifacts in a temporary directory from fixed saved predictions,
including their registered statistical calculations/resampling, and
compares all fifteen output bindings with the receipt. It blocks network,
key access, live model/client and provider constructors; it does not
request new responses or train models. It requires the frozen source
bindings and recorded analysis environment and can therefore fail in an
edited live checkout. The previously recorded outcome was byte-identical
with zero new API calls; no new replay result is claimed here.

Avoid using `freeze`, `analyze`, a new namespace or changed bootstrap
settings to manufacture agreement with an old receipt. A new experimental
protocol belongs to a separately versioned study and cannot overwrite the
historical artifacts on which this thesis relies.[^f-commands]

## F.4. Resource levels and practical limits

| Operation | Required resources | What it establishes |
| --- | --- | --- |
| Read saved CSV/JSON or check hashes | Python standard library / shell, pinned ZIP/index/chunks | Identity and recorded values; no inference |
| Cold statistical analysis | Historical source/runtime, fixed predictions/outcomes and plotting/numerical dependencies | Artifact reproducibility under those inputs; not a fresh market sample |
| Numerical asset inference/replay | Frozen teacher/student/HMM/scalers/selectors, appropriate PyTorch/TA-Lib/HMM/numerical dependencies and CPU memory | Recorded numerical path; distinct from reading stored outputs and from hosted LLM calls |
| Offline application fixture | Current repository, serving-integration fixtures and application dependencies | Mock HTTP/application behavior; no market or hosted-model evidence |
| Live analysis | Admitted stock/index/news capture, model assets, provider access and credentials, compatible runtime | New provider/inference job; not a reproduction of historical financial outcomes |

The standard historical environment is Windows Python 3.13.5; the full
analysis/asset lock records 107 packages. Dependency installation or an
uncached sentiment model can require downloads before an offline run.
OS-specific compiled packages, fonts and rendering tools also matter to
byte-identical artifacts. A Linux deployment needs its own platform
environment rather than claiming the Windows lock is portable unchanged.
No minimum GPU, wall-time or monetary bill is inferred from unavailable
matched measurements. The selected numerical student is served on CPU;
this does not imply that training or every optional backend is cost-free.

## F.5. Offline preview versus current live workflow

For an explicitly mocked preview, this documented entrypoint binds only
loopback and writes a separate temporary fixture-job namespace:

```powershell
py -3.13 -X utf8 scripts/serve_serving_review.py --port 5051 --duration 300 --seed
```

It uses HTTP fixtures, a distinct owner cookie and a seeded MWG/six-version
backtest fixture. It does not call real market/Groq providers. The seeded
review pages are a fixture harness, not proof that the current Realtime
form exposes a six-version backtest or that browser acceptance is complete.
The script prints its local URL and stops at the requested duration or
Ctrl+C. This command has not been run as part of writing the appendix.

The **actual application** has the separate entrypoint, from repository root:

```powershell
py -3.13 web_interface.py
```

Its documented local URL is `http://127.0.0.1:5000` unless the configured
port differs. This path may access live data and hosted models when
analysis is requested; it is not the offline fixture or cold-replay CLI.
Credentials are supplied through the application's supported interface or
process environment, never copied into thesis examples or result artifacts.

The current Realtime 1D flow is:

1. Select a stock and one of Original, v1, C2, A, B or MT-BICL. Original
   delegates to the legacy route; enhanced versions use a captured job.
2. Capture the versioned 1D stock/index snapshot with source, units,
   timestamp and provisional flags. The current timeframe path may
   include a forming daily observation (`daily_provisional`); it differs
   from the older latest-completed-session backend's local-time cutoff.
3. Validate cutoff/calendar/freshness, sufficient 600-observation context,
   eligible dated news and resource identity. Missing verified sentiment
   remains unavailable. Newer market data require a new capture/job.
4. Preflight the selected version and create one analysis job/repeat.
   MT schedules Common→Fact Anchor→MT, not all eight research roles over
   three repeats. The request, dependencies and fallback action remain
   separately observable.
5. Poll/read the same job, including raw proposal, final LONG/CASH action,
   policy reason, support and source identity. Reload/resume retains the
   original capture; uncertain creates/sends are not blindly duplicated.
6. Switch stored Vietnamese/English presentation views without requesting
   a translation or changing canonical policy fields. Treat provisional
   data, report statements and missing evidence with their stated limits.

The application receipt remains OFFLINE_PASS_BROWSER_PENDING with
`f11_complete=false`, desktop/mobile NOT_RUN. Equivalent research behavior
accepted by the author for the three named modules does not complete that
browser check, certify live fills or establish prospective profitability.
[^f-application]

[^f-resources]: Ledger §3.2–§3.4, RG01/RG02/TR01–TR08 and U08/U09/F01 resource bindings; §13.9 maps these paths and pins. Original archive/member identity remains separate from a working-directory path after restoration.
[^f-commands]: Source-inspected parsers and implementations in `scripts/revision_evidence.py`, `core/revision_evidence_archive.py`, `scripts/prepare_unified_comparison_v2.py`, `scripts/unified_analysis/run.py` and `core/unified_analysis/runtime.py`. Commands are syntax/path checked, not executed as replay or new acceptance during writing.
[^f-application]: Current `web_interface.py` and source-bound AP01–AP17 workflow/receipt, `scripts/serve_serving_review.py` fixture harness and §4.10.4. Current Realtime 1D controls, backend capabilities and fixture-review pages are explicitly different scopes.
