# Detailed thesis writing plan

## 1. Objective and completion boundary

Produce an original, complete **English-language graduation thesis** explaining and evaluating the current system under the [six-chapter outline](outline.md). A lecturer unfamiliar with the repository should understand the entire proposed system, reproduce the logic of one decision and distinguish supported findings from assumptions and open questions.

The deliverable includes the manuscript, front matter, references, Appendices A–F, traceable figures/tables, a self-contained LaTeX project, a visually reviewed PDF and a reproducible handover package. Preparing this plan does not complete any drafting task below.

There are **84 small tasks**, grouped into ten phases. Dependencies express content readiness rather than calendar dates. No submission deadline has been supplied. Start with T02, T03, T05 and T08; collect T01 metadata in parallel without blocking independent writing.

All new thesis prose, planning text, headings, captions, diagram labels and explanatory notes are English. The user's language requirement supersedes the repository's general Vietnamese explanation convention for these thesis artifacts. Preserve original program identifiers, bibliographic titles and quoted source evidence accurately; explain any non-English excerpt in English.

## 2. Management and file conventions

### 2.1. One task-status source

The [writing checklist](../docs/plan/week12/README.md#thesis-writing-checklist) is the single source for progress. This document holds task specifications, dependencies and acceptance conditions. Do not maintain a second changing checklist here or create a receipt for every task.

Use `TODO`, `IN_PROGRESS`, `REVIEW`, `DONE` or `BLOCKED` in the checklist as necessary. A checked item means `DONE`: its output exists and its acceptance condition was checked. For an active/blocked item, add one short note identifying the current file or missing input. Record completion as `task ID; artifact/section; verification; remaining limitation`, grouping related tasks in one weekly note. An external review is only complete when actual feedback has been received and addressed.

Each task is intended to fit one focused work session. Split a task into lettered subtasks if the material exceeds that scope, preserving the parent ID and its acceptance condition. **S** means a small bounded edit/check; **M** means a section or a linked visual/evidence unit. These are sizing guides, not promised hours or dates.

### 2.2. Proposed artifact layout

Only `README.md`, `outline.md` and this plan are required at planning time. Create the following outputs when their tasks begin; paths in this block are planned, not claims that files already exist.

```text
thesis/
  README.md
  outline.md
  plan.md
  evidence.md                  # shared source/claim, literature and asset registers
  frontmatter.md               # editable front-matter prose and metadata
  chapters/
    01_introduction.md
    02_related_work.md
    03_background.md
    04_proposed_system.md
    05_experiments.md
    06_conclusion.md
  appendices/
    A_contracts.md
    B_prompts.md
    C_configuration.md
    D_results.md
    E_verification.md
    F_reproduction.md
  references.bib
  assets/
    diagrams/                  # editable diagram sources and exported figures
    tables/                    # derived tables with identifiable source records
    figures/                   # plots and traceable application images
  latex/
    main.tex
    preamble.tex
    frontmatter/
    chapters/
    appendices/
  release/
    thesis.pdf
    thesis-source.zip
    manifest.json
```

During drafting, Markdown is the authoritative prose source. At T72, record the transfer point and make LaTeX the authoritative submission text; retain Markdown as the reviewed drafting snapshot. Do not silently maintain divergent active copies. `references.bib` and assets remain shared sources. The packaged LaTeX build must resolve those resources within the package, without depending on the original sample or absolute local paths.

The evidence register should contain: source/version/hash and role; claim or table-cell mapping; literature reading/citation notes; figure/table inventory; open metadata and unresolved evidence issues. Reference existing frozen artifacts rather than copying large archives into the thesis. Keep checklists and completion history in `docs/plan/`.

### 2.3. Change and verification policy

- Start a `docs/<technical-topic>` branch from updated `develop`; commit and merge after the applicable checks pass. Commit subjects describe content, without weekly/day progress codes.
- Markdown/prose edits: check links, equations, terminology, source values and diff. No compileall, unit, E2E or leakage rerun is required solely for writing.
- LaTeX edits: compile the affected document, resolve citations/references, inspect layout and render the final PDF. Read and apply the PDF skill when PDF work actually begins.
- A changed table/plot generator requires appropriate scoped checks against frozen expected values. Compile only changed Python files if applicable; do not turn writing into an unsolicited runtime refactor.
- Preserve frozen data, journals, models, receipts and negative evidence. New calculations use a separate derived output with stated provenance; they never overwrite historical evidence.
- Do not launch hosted inference, market collection, model retraining or deferred ablations to fill a writing gap. Identify the missing evidence, narrow the claim or propose a separate research task.

## 3. Reader-comprehension contract for the proposed method

Assume general undergraduate knowledge of machine learning, but no knowledge of this repository, its abbreviations or trading conventions. The chapter must explain the **complete system**, not just the new prior prefix or a list of Python modules.

### 3.1. Required teaching sequence

1. Describe the practical decision in one paragraph: what is observed, what is chosen and when an outcome becomes known.
2. Show a high-level data-flow diagram with distinct training, inference, policy and evaluation boundaries.
3. Walk through a single stock/date example using simple named records before equations or implementation IDs.
4. Introduce the base agents and the information each contributes, including numerical components that do not call an LLM.
5. Explain why Native/Common differ and why historical context is added.
6. Build from a matured episode to regime-aware retrieval, then conditional statistics and alternative priors.
7. Introduce facts, prior/target tasks, teacher/student inference and utility step by step before the full MT-BICL policy.
8. Explain orchestration, valid fallback, technical failure and recovery, then present complete pseudocode.
9. Revisit the same example and identify the raw proposal, final action and later economic outcome.

### 3.2. Required component explanation

For every substantive component, answer: **Why is it needed? What enters it? What is known at that time? What calculation or inference occurs? What leaves it? Who consumes that output? What happens when evidence is missing or a request fails? What is inherited or changed?**

Provide a compact contract table with input fields/types, availability condition, output fields and consumer. Pair formulas with prose and a short example. Keep full schemas, long prompts and implementation listings in appendices, but retain enough definitions and policy rules in the main chapter for a self-contained explanation.

### 3.3. Comprehension acceptance questions

A reader of Chapters 3–4 should be able to answer all of the following without opening the code:

- Why does SHORT mean CASH in this study, and when are LONG entry and exit prices observed?
- Which data can each agent see at the cutoff, and which components are deterministic, learned offline or hosted at inference time?
- How do Pattern and Trend differ despite both consuming charts?
- How do alpha factors differ from sentiment and from the LLM's confidence statement?
- What changes between Native and Common, and why is Base a separate comparator?
- When does an episode become eligible, and how are regime, similarity, sample support and `K` different?
- What are prior tasks, target observations and the query in MT-BICL?
- What do the teacher and student learn or estimate, and what remains frozen during evaluation?
- Why does a high probability of a positive label not necessarily imply positive utility?
- What does Fact Anchor contribute, and when may policy reject a different LLM proposal?
- Why can eight forecast roles produce fewer than eight new Decision calls for a repeat?
- How does a final action become an account return without sending the query outcome back into context?
- Which protections are verified, and why do they not imply whole-system causal certification?

The internal review at T74 uses this checklist. An internal self-check may be recorded as such; do not report an independent lecturer review unless it actually occurred.

## 4. Phase and milestone map

| Phase | Tasks | Main output | Exit condition |
| --- | --- | --- | --- |
| P1. Preparation | T01–T08 | Requirements, source/evidence register, notation and draft structure | Working scope and accessible evidence are clear; unresolved external requirements are explicitly recorded. |
| P2. Foundations | T09–T15 | Chapter 3 | All concepts and contracts needed by the method are defined consistently. |
| P3. Proposed system | T16–T35 | Chapter 4, explanatory figures and algorithms | End-to-end walkthrough and component explanations cover the complete system. |
| P4. Experiments | T36–T47 | Chapter 5 and result assets | Each reported value and interpretation has a source and correct study scope. |
| P5. Related work | T48–T53 | Chapter 2 and bibliography | Primary-source coverage, attribution and gap statement are checked. |
| P6. Thesis argument | T54–T58 | Chapters 1 and 6 | Questions, contributions, findings and limitations agree. |
| P7. Supporting material | T59–T66 | Front matter and Appendices A–F | Supporting content is complete and referenced from the main text. |
| P8. Typesetting | T67–T72 | Complete self-contained LaTeX project | The full document builds with all text, references and assets. |
| P9. Review | T73–T80 | Reviewed submission candidate | Scientific, English-language, visual and applicable feedback checks pass. |
| P10. Handover | T81–T84 | Final PDF, source package and closure record | Artifacts are reproducible, identified and delivered; external submission status is explicit. |

**Working order:** P1 essentials → P2 → P3 → P4 → P6 → P7 → P8 → P9 → P10. P5 source reading can begin as soon as T04 exists and should inform P2/P3; finalize the gap statement after the actual method is understood. Institutional metadata in T01 only blocks the dependent front-matter/layout decisions, not technical drafting.

## 5. Task specifications

Task IDs below are stable management identifiers and must not appear in the thesis body. Dependencies refer to prerequisite task outputs, not to another person's permission. Each row states the work, output location and a concrete acceptance condition.

### P1. Preparation and source control

| ID / size | Depends on | Work and deliverable | Acceptance condition |
| --- | --- | --- | --- |
| T01 / S | — | Record institution, author/student ID, program, supervisor, required forms, citation/layout rules and actual deadline in the metadata section of `evidence.md`. Separate confirmed requirements from template suggestions. | Each field has a source or is explicitly unresolved; no invented identity, date or approval. Missing external information blocks only its dependent finalization. |
| T02 / S | — | Refine the working title, RQ1–RQ4, contributions and six-chapter scope using the outline and current system. | Each RQ has an intended comparison/evidence type; inherited work and empirical claims are separated. |
| T03 / M | T02 | Inventory current source and frozen component/context studies in `evidence.md`: versions, paths, checksums, support and limitations. | Every planned quantitative result has a reachable artifact or a recorded gap; historical source/runtime pins are distinguished from live code. |
| T04 / M | T02 | Create a primary-source reading list and citation-key scheme; inventory the existing bibliography as a candidate list. | Sources are grouped by topic and marked unread/read/verified; no citation is treated as verified merely because it exists in `paper/`. |
| T05 / S | T02 | Define English terminology, symbols, naming aliases and a concise style sheet in `evidence.md`. | Native/Common/Base, episode/task/query, probability/confidence/utility and percent/percentage-point units are unambiguous. |
| T06 / S | T03, T05 | Create the figure/table/algorithm register from Section 6, including intended message and source. | Each asset has an owner task, chapter destination and provenance category: measured, derived or illustrative. |
| T07 / M | T03, T05 | Select a traceable running example and case-selection rule. If no suitable archived case exists, define a clearly labeled illustrative example. | Cutoff, admissible inputs, source IDs and limits are recorded; illustrative values cannot be mistaken for results. |
| T08 / S | T02 | Create the six chapter drafts with headings from the outline and a shared evidence register. | Planned sections have stable headings; placeholders identify missing content rather than pretending that prose or results exist. |

### P2. Theoretical background and problem formulation

| ID / size | Depends on | Work and deliverable | Acceptance condition |
| --- | --- | --- | --- |
| T09 / M | T05, T08 | Draft §3.1: OHLCV, trading sessions, cutoff, windows, warm-up and engine index mapping; create the timing figure. | A reader can locate the last visible bar, entry and exit without confusing calendar days with observed sessions. |
| T10 / M | T03, T09 | Draft §3.2 with the exact economic formula, zero-return label convention and a simple LONG/CASH calculation. | Formula and example agree with the oracle, including both cost legs; CASH is never described as a short-sale profit. |
| T11 / M | T04, T05, T09 | Draft §3.3 introducing five indicators, alpha transformations/selection and separate sentiment information. | Definitions precede implementation-specific rules; ranking diagnostics and confidence are not described as calibrated forecasts. |
| T12 / M | T04, T05 | Draft §3.4 explaining HMM states/emissions/transitions, VN-Index features and endpoint inference. | Training, scaling, state interpretation and cutoff assumptions are explicit; smoothing with future observations is not implied. |
| T13 / M | T04, T05 | Draft §3.5: Beta–Bernoulli updates, conditional/background counts, shrinkage and a labeled illustrative posterior example. | All symbols and denominators are defined; population support is distinct from displayed `K`; interval interpretation is appropriately limited. |
| T14 / M | T04, T05, T13 | Draft §3.6: tasks, target observations, query, teacher/student roles and probability versus return utility. | Multi-task is distinguished from multi-agent; numerical examples show why label probability and expected gain differ. |
| T15 / M | T03, T09, T10 | Draft §3.7: PIT rules, maturity, purging, paired comparison, dependence and evaluation units. | Price/news/episode inequalities are consistent; query labels are excluded; outer cutoff and row causality are distinguished. |

### P3. Proposed system, explained from first principles

| ID / size | Depends on | Work and deliverable | Acceptance condition |
| --- | --- | --- | --- |
| T16 / M | T06, T07, T09, T10 | Draft §4.1 in plain English; create the overview architecture and begin the running example. | Diagram separates offline fitting, inference, policy and evaluation; every major component has a purpose before technical details appear. |
| T17 / M | T03, T15, T16 | Draft §4.2: sources, windows, snapshots, missingness and the component input/output contract table. | Each input has a time boundary and consumer; query outcomes cannot enter the forecast path. |
| T18 / M | T11, T17 | Draft Indicator and base Decision explanations in §4.3, including votes, distillation, structured output and action mapping. | Distinguish deterministic Indicator behavior from hosted Decision inference; describe missing/error cases without equating confidence with probability. |
| T19 / M | T11, T17 | Draft Pattern/Trend subsections and an annotated pair of chart inputs with report examples. | A novice can distinguish chart construction, VLM interpretation and numerical consistency checks; actual images retain provenance. |
| T20 / M | T03, T11, T17 | Draft Alpha processing: candidate construction, normalization, IC orientation, ranking and selected report. | Native historical noncausality and in-sample selection are visible; adapted formulas are not claimed equivalent to their originals. |
| T21 / M | T03, T11, T17 | Draft sentiment input/aggregation, provenance, dated availability, missingness and integration into the report path. | Explain live versus frozen-study inputs and aggregation thresholds from the actual profile; missing data is not invented neutral evidence. |
| T22 / M | T18, T20, T21 | Draft §4.4 and the Native/Common/Base distinction table, tracing unchanged upstream versus changed alpha/prompt fields. | Reader can identify the intervention and understand why its contrast cannot isolate a single causal factor. |
| T23 / M | T10, T15, T17 | Draft historical episode/bank construction in §4.5 with a worked record and maturity timeline. | Every field, label source and eligibility check is explained; signal bank and numerical task context remain distinct. |
| T24 / M | T12, T17, T23 | Draft regime fitting/inference integration in §4.5 and its training-versus-query diagram. | State assignment, metadata, fit-quality fallback and frozen scaler/model identity match the evaluated route. |
| T25 / M | T22, T23, T24 | Draft §4.6: eligible pool, retrieval score/tie-break, selected examples and annotated Bayesian v1 prefix. | The running example follows filtering before outcome summaries; `K<=3`, fallback and source IDs are explicit. |
| T26 / M | T13, T22, T23 | Draft C2 in §4.7: disjoint populations, shrinkage, intervals and separate statistics/example readiness. | Counts can be reconstructed from the explanation; a reader understands when statistics and examples are each unavailable. |
| T27 / M | T25, T26 | Draft A_tp_pool and B_semantic; complete the four-prior comparison table. | Differences in matching, representation, support and fallback are stated precisely; no unimplemented embedding retrieval is inferred from a name. |
| T28 / M | T14, T15, T23 | Draft MT task/context construction in §4.8, using a diagram of prior tasks, target observations and query. | Bucket membership, feature vectors, scaling and maturity conditions are defined; query outcomes never become context observations. |
| T29 / M | T03, T14, T28 | Draft teacher/student training and inference, including actual architecture, objective, recipe, selection and frozen checkpoint. | Every architecture/training detail traces to the evaluated implementation/lock; no placeholder model is substituted. |
| T30 / M | T17, T22, T28 | Draft facts and Fact Anchor with an example assertion and invalid-anchor path. | Explain the Common dependency, validity checks, anchor action and provenance without implying an economic veto at this stage. |
| T31 / M | T13, T28, T29, T30 | Draft utility estimation and revision policy; create the action decision tree and a worked veto/acceptance example. | CASH→LONG and LONG→CASH quantiles are correct; raw proposal, final action, valid bypass and technical failure are distinct. |
| T32 / M | T18, T25, T26, T27, T29, T31 | Draft prompt/context projection and annotate the fields received by each Decision family. | Whole-membership statistics versus shown exemplars are clear; character limits and schema are checked against actual builders. |
| T33 / M | T22, T27, T31, T32 | Draft §4.9: eight-role DAG and three end-to-end algorithms for context, method/policy and paired evaluation. | Dependencies run in order, upstream is reused, fallback does not create a fake call, and outcomes join only after forecasts are durable. |
| T34 / M | T17, T32, T33 | Draft operational controls in §4.10: prompt budget, retry, schema repair, stage checkpoints, resume and UNKNOWN. | Show the lifecycle of a successful, unsupported and interrupted point; no technical error is silently reclassified as CASH. |
| T35 / M | T16, T33, T34 | Draft the application workflow and close the running example from input to action and later outcome. Add versioned UI screenshots only if available and checked. | The complete system is understandable without UI images; application acceptance is reported accurately and does not imply profitable deployment. |

### P4. Experimental design, results and discussion

| ID / size | Depends on | Work and deliverable | Acceptance condition |
| --- | --- | --- | --- |
| T36 / M | T03, T15, T22, T33 | Draft §5.1 and the study-scope table separating component and historical-context evidence. | Study names, cohorts, responses, freeze points and exposed-history limitations are not mixed. |
| T37 / M | T03, T17, T23, T36 | Draft §5.2 and data/split/coverage tables, including exclusions and bank/sentiment coverage. | Counts, dates, stock support, warm-up and missingness reconcile to the recorded artifacts. |
| T38 / M | T03, T29, T33, T34, T36 | Draft §5.3 with model/runtime options, fits, repeats, scheduling and request accounting. | Distinguish 102 points, 51 accounts, three repeats, 2,448 slots, responses and HTTP attempts; use frozen study settings. |
| T39 / M | T22, T27, T33, T36 | Draft §5.4: comparator families, bridge contrasts, numerical controls and completed component interventions. | Each contrast has a defined treatment/control and common support; Base/Common and always-LONG/continuous hold are not conflated. |
| T40 / M | T10, T15, T36, T38, T39 | Draft §5.5 with equations, averaging order, denominators, cost/exposure metrics and paired resampling conventions. | Each study retains its own estimator and risk-ratio convention; descriptive bands are not promoted to confirmatory significance. |
| T41 / M | T03, T37, T39, T40 | Draft §5.6 and reproduce the component-study main comparison table from existing values. | Every cell has a source; narrative matches direction, magnitude, units and support, including unfavorable outcomes. |
| T42 / M | T03, T37, T39, T40 | Draft §5.7 and the historical-context comparison table for all roles and economic controls. | All results, support and fallback remain visible; mean account return and BA aggregation agree with the source. |
| T43 / M | T40, T42 | Prepare the Native/Common contrast plots and associated narrative, with simultaneous descriptive bands and bridge comparisons. | Same families/indices/units as the recorded analysis; no selective family reporting or spliced independent-account equity curve. |
| T44 / M | T25, T26, T27, T31, T42 | Draft mechanism analysis: coverage, age/similarity if recorded, fallback, anchor agreement and policy interventions. | Recorded versus unavailable diagnostics are distinguished; student-specific causal attribution is not inferred from aggregate differences. |
| T45 / M | T07, T35, T41, T42, T44 | Write a small set of traceable cases covering supported context, insufficient support, disagreement/veto and error. | Cases follow the declared selection rule; facts/proposals/actions/outcomes are separately visible and incorrect predictions are included. |
| T46 / M | T03, T34, T40, T41, T42 | Write robustness and resource analysis using completed panels/sensitivities and recorded usage. | Costs, latency and missing usage have correct definitions; separate panel supports and execution assumptions are preserved. |
| T47 / M | T36, T41, T43, T44, T45, T46 | Finish §5.9 and the RQ answer matrix; enumerate unperformed ablations and material threats to validity. | Native causal failure, provenance gaps, negative returns, sample dependence and historical exposure constrain the conclusions explicitly. |

### P5. Literature review and positioning

| ID / size | Depends on | Work and deliverable | Acceptance condition |
| --- | --- | --- | --- |
| T48 / M | T04 | Read/verify primary sources, maintain claim-to-citation notes and populate `references.bib`. | Referenced metadata and supporting passages are checked; unresolved/unread sources are not presented as established support. |
| T49 / M | T11, T48 | Draft §2.1 on technical analysis, alpha construction and quantitative comparators. | Explain similarities and differences relevant to this implementation; avoid an unsupported catalog of methods. |
| T50 / M | T16, T22, T48 | Draft §2.2 on LLM/VLM and multi-agent systems, especially inherited QuantAgent components. | Attribution identifies what was reused, adapted and added; novelty statements have a defensible scope. |
| T51 / M | T12, T13, T14, T29, T48 | Draft §§2.3–2.5 on regimes, Bayesian context and MT-BICL/student–teacher work. | Explain connections and implementation departures without equating all retrieval or few-shot prompting with Bayesian multi-task learning. |
| T52 / M | T15, T40, T48 | Draft §2.6 on backtesting, dependence, ablations, reproducibility and prospective evaluation. | Sources support the actual evaluation rationale and limitations, rather than implying guarantees absent from this design. |
| T53 / M | T27, T31, T47, T49, T50, T51, T52 | Draft §2.7 and the related-work comparison/gap table. | All comparisons are source-backed, and the gap describes the implemented contribution without unsupported superiority claims. |

### P6. Introduction, conclusions and argument consistency

| ID / size | Depends on | Work and deliverable | Acceptance condition |
| --- | --- | --- | --- |
| T54 / M | T02, T10, T47, T53 | Draft §§1.1–1.2: motivation and problem statement for a general technical reader. | The reader understands the practical task, available information and evaluation target before specialist terminology. |
| T55 / M | T02, T47, T53, T54 | Draft §§1.3–1.5: RQs, challenges, boundaries, contributions and chapter roadmap. | Each contribution points to an actual chapter/evidence item; inherited work and unperformed studies are qualified. |
| T56 / M | T47, T55 | Draft §§6.1–6.2 with an explicit answer to each research question. | Answers agree with Chapter 5 and do not introduce new results or stronger claims. |
| T57 / M | T47, T56 | Draft §§6.3–6.4: limitations and a prioritized future-work agenda. | Future work addresses specific missing evidence; causal repair, ablations and prospective evaluation remain separate future tasks. |
| T58 / S | T53, T55, T56, T57 | Read the introduction–method–results–conclusion chain and revise transitions/repeated definitions. | Title, RQs, contribution list, terminology and conclusions align without unexplained scope changes. |

### P7. Front matter and appendices

| ID / size | Depends on | Work and deliverable | Acceptance condition |
| --- | --- | --- | --- |
| T59 / M | T47, T55, T56 | Write the abstract and keywords in `frontmatter.md`, within the confirmed length constraint if supplied. | Problem, method, design, principal results and limitations agree with the thesis; no fabricated benefit or prospective claim. |
| T60 / M | T01, T05, T58 | Complete cover metadata, acknowledgements, declaration text, abbreviations and notation in `frontmatter.md`. | Personal details and required wording are confirmed; no copied sample identity, fabricated signature or unreceived endorsement. |
| T61 / M | T10, T15, T17, T23 | Write Appendix A with compact schemas, time mapping, label rules and missingness conventions. | Examples and schema fields agree with the described version; main-text references point to the right details. |
| T62 / M | T18, T25, T27, T30, T32 | Write Appendix B with representative prompts, BRPP, schemas and response examples. | Remove secrets; retain original request identity; English translations are marked as presentation translations, not measured English prompts. |
| T63 / M | T20, T24, T25, T26, T29, T31, T38 | Write Appendix C with formulas, configuration, hyperparameters and training/inference settings. | Every numeric setting is source-backed and tied to the correct study/profile; defaults are not substituted for observed values. |
| T64 / M | T41, T42, T43, T44, T46 | Write Appendix D with extended stock/fold/repeat and sensitivity tables. | Totals and denominators reconcile with main tables; studies and unavailable metrics remain distinct. |
| T65 / M | T03, T15, T34, T47 | Write Appendix E documenting test/audit scope and retained counterexamples. | State which checks were historically run and on what source; do not infer full-system certification from passing scoped tests. |
| T66 / M | T03, T35, T38, T65 | Write Appendix F with offline reproduction, resource prerequisites and the application workflow. | Commands refer to known artifacts and correct working directories; distinguish metric replay, fresh inference and pending UI validation. |

### P8. LaTeX implementation and document assembly

| ID / size | Depends on | Work and deliverable | Acceptance condition |
| --- | --- | --- | --- |
| T67 / M | T01, T08 | Build a minimal clean LaTeX shell from required template conventions, with English metadata placeholders only where unresolved. Record engine/toolchain. | Minimal document compiles; sample topic/macros/personal metadata are removed; unresolved institutional rules remain listed. |
| T68 / M | T09, T10, T11, T12, T13, T14, T15, T35, T67 | Transfer Chapters 3–4, equations and algorithms into LaTeX; attach editable diagrams. | Equations and running-example logic match reviewed prose; all symbols, floats and algorithm references resolve. |
| T69 / M | T47, T64, T67 | Transfer Chapter 5 and result tables/plots with fixed precision and source-aware captions. | Compare every numeric table/plot value to its source; row/column labels, percent units and support notes survive typesetting. |
| T70 / M | T53, T58, T59, T60, T67 | Transfer Chapters 1, 2 and 6 plus front matter; connect bibliography and generated lists. | Complete English front matter and all chapters render; references are ordered/styled consistently and citations resolve. |
| T71 / M | T61, T62, T63, T64, T65, T66, T67 | Transfer Appendices A–F and connect forward/back references, figures and tables. | Appendices are legible and referenced; long schemas/prompts do not crowd the main narrative or overflow pages. |
| T72 / S | T68, T69, T70, T71 | Assemble the full document and record the Markdown-to-LaTeX authority transfer in the README. | One canonical submission source exists; all content is included once and source paths work without the sample directory. |

### P9. Scientific, language, reader and visual review

| ID / size | Depends on | Work and deliverable | Acceptance condition |
| --- | --- | --- | --- |
| T73 / M | T72 | Audit every headline claim, contribution, result and conclusion against the evidence register. | Claims have sources and correct scope; negative findings, missing support and unperformed experiments remain explicit. |
| T74 / M | T72 | Conduct the first-time-reader review using Section 3; repair missing explanations in Chapters 3–4. | All comprehension questions are answerable from the text. Record whether the review was internal or independent; never invent reviewer feedback. |
| T75 / M | T72 | Edit English grammar, terminology, tense, paragraph flow, captions and abbreviation usage across all material. | Consistent academic English; no untranslated explanatory prose, unexplained acronyms, planning IDs or repository-history narration in the body. |
| T76 / M | T72, T73 | Check bibliography, quotations, figure attribution, data/software rights and any required assistance disclosure. | Every citation is present and relevant, copied material is attributed, and unresolved rights affecting release are identified. Do not promise public distribution without permission. |
| T77 / M | T73, T75 | Independently reconcile formulas, units, counts, percentages, risk conventions and table/plot precision. | No arithmetic/label/support mismatch; rounded display values do not change the interpretation or silently replace exact source values. |
| T78 / M | T74, T75, T76, T77 | Clean-build the document; inspect logs, cross-references, pagination, lists, bookmarks and text extraction. | No missing citations/references/assets, clipped formulas or unresolved build errors; warnings are fixed or explicitly inspected. |
| T79 / M | T78 | Render and visually inspect every page, including tables, plots, algorithms and appendices; fix layout and recheck affected pages. | No unreadable text, overlapping elements, broken fonts, cropped visuals or unintentional blank pages; final full-page pass uses the final build. |
| T80 / M | T79 | Incorporate actual author/supervisor feedback if provided; otherwise record that external review has not occurred and complete an internal revision pass. | Feedback items have resolutions and locators. Changed text/assets receive relevant checks again; external review is never marked complete without evidence. |

### P10. Reproducible release and handover

| ID / size | Depends on | Work and deliverable | Acceptance condition |
| --- | --- | --- | --- |
| T81 / M | T80 | Freeze the final manuscript revision and assemble a self-contained source archive, bibliography, assets and build instructions. | Package excludes credentials and unnecessary/private raw data; included resources have clear permissions; no absolute paths or untracked sample dependency. |
| T82 / M | T81 | Extract into a clean directory, build offline where supported, and verify the PDF against the reviewed release. Record toolchain and file hashes in one manifest. | Build succeeds from the package; content/page/figure checks agree. If timestamps prevent byte-identical PDFs, document the difference rather than claiming byte identity. |
| T83 / S | T82 | Deliver `thesis.pdf`, the source archive and concise reproduction/readme guidance; list any external approval/submission items still pending. | Delivered files exist and match the manifest. Delivery does not imply supervisor acceptance or institutional submission. |
| T84 / S | T83 | Close the writing checklist with source commit, deliverable paths and checks. Record external submission/acceptance only if the user supplies or authorizes that event. | Internal completion is distinguishable from submitted/accepted status. No email, upload, signature or submission is performed merely because this plan exists. |

## 6. Figure, table and algorithm production register

Use conceptual diagrams for explanations and standard plotting tools for scientific charts. Every final visual needs English labels, readable print sizing, a self-contained caption, units where relevant and an explicit source or illustration designation. Stable IDs here are planning aids; final numbering is generated by LaTeX.

| Asset | Main message | Owner | Location / evidence |
| --- | --- | --- | --- |
| F01. Trading timeline | What is visible at `t`, entry at `t+1`, exit at `t+3` | T09–T10 | Chapter 3; engine/target contract. |
| F02. Chronological partitions | Fit/validation/test and maturity/purge boundaries | T15, T37 | Chapters 3/5; protocol and split records. |
| F03. System overview | Entire path, with training/inference/policy/evaluation separated | T16 | Chapter 4; graph, registry and adapters. |
| F04. Chart inputs | Different evidence supplied to Pattern and Trend | T19 | Chapter 4; archived chart pair or labeled illustration. |
| F05. Episode and retrieval flow | Eligible memory → matching/ranking → prefix/fallback | T23–T25 | Chapter 4; bank/retriever. |
| F06. MT task and training flow | Prior/target/query, teacher, student and frozen inference | T28–T29 | Chapter 4; evaluated task/model locks. |
| F07. Policy tree | Facts, support, anchor, proposal, utility veto and final action | T30–T31 | Chapter 4; policy traces. |
| F08. Dependency DAG | Shared upstream and per-repeat role dependencies | T33 | Chapter 4; registry and protocol. |
| F09. Contrasts | Difference estimates and descriptive bands | T43 | Chapter 5; frozen analysis artifacts. |
| F10. Coverage and action changes | Effective context support and fallback/policy behavior | T44 | Chapter 5; traces and support records. |
| F11. Application workflow | User input → progress → interpretable result | T35 | Chapter 4/Appendix F; verified versioned screenshots if available. |
| A01–A03. Algorithms | PIT context; method/policy execution; paired forecast/evaluation | T33 | Chapter 4; complete inputs, outputs and error/fallback behavior. |
| B01. Notation | Symbols and units used throughout | T05, T60 | Front matter/Chapter 3. |
| B02. Component contracts | Component purpose, inputs, time boundaries and outputs | T17–T22 | Chapter 4. |
| B03. Method comparison | Native/Common and historical-context differences | T22, T27, T33 | Chapter 4. |
| B04. Data/configuration | Cohort, partitions, bank, missingness, model/runtime | T37–T38 | Chapter 5. |
| B05–B06. Main results | Separate component and context studies | T41–T42 | Chapter 5; exact frozen values. |
| B07. Mechanism/cases | Context, raw proposal, policy and outcome | T44–T45 | Chapter 5. |
| B08. Literature comparison | Supported similarities, differences and research gap | T53 | Chapter 2; verified primary sources. |
| B09. RQ answer matrix | Supported answer and remaining uncertainty | T47, T56 | Chapters 5/6. |

Do not regenerate hosted reports merely to obtain a prettier example. Translate explanatory captions, not the scientific identity of measured inputs. If an archived prompt is Vietnamese, label its English rendering as a translation.

## 7. Milestone review gates

These gates organize writing checks; they are not the software system's four runtime gates and do not re-certify historical research.

| Gate | Required work | Pass condition | If it does not pass |
| --- | --- | --- | --- |
| G1. Evidence-ready drafting | T02–T08; T01 issues recorded | Sources are reachable or gaps declared; terminology, scope and example are coherent. | Draft independent sections; do not invent missing evidence or personal metadata. |
| G2. Method explanation | T09–T35 | Complete Chapter 3/4 draft, diagram contracts, worked example and policy algorithms agree. | Repair missing concepts or split oversized sections before making claims about the method. |
| G3. Evidence-backed argument | T36–T58 | Results, related work, RQs and conclusions agree; claims stay within source scope. | Correct the narrative or narrow the claim; identify optional new research separately. |
| G4. Complete source | T59–T72 plus resolved required T01 items | Front matter, chapters, references and appendices are assembled and compile. | Keep a visible issue list; no final release with placeholder identities or mandatory sections missing. |
| G5. Reviewed candidate | T73–T80 | Scientific, comprehension, English, attribution, numerical and visual checks pass; actual external-review status is honest. | Reopen the affected task and its dependent checks; do not repeat unrelated runtime suites. |
| G6. Internal completion | T81–T84 | Final PDF and self-contained sources are delivered, clean-built and identified by manifest. | State exactly what is missing. Submitted/accepted status needs separate real-world evidence. |

## 8. Common blockers and scope decisions

| Issue | Action within writing scope | What must not be inferred |
| --- | --- | --- |
| Missing author, supervisor, deadline or official layout | Record in T01, request the specific information when needed and continue technical drafting. | Template metadata is not the user's identity or an institutional requirement. |
| Frozen asset unavailable or hash differs | Use the existing restoration guide; preserve expected/actual identities and narrow unsupported claims. | A similarly named live artifact is not an equivalent source. |
| An ablation is implemented but unrun | Document capability and move its causal question to future work. | Code existence does not supply results. |
| Negative or inconclusive results | Report them with correct support and descriptive uncertainty. | Thesis completion does not require a profitable strategy. |
| Native row-wise causality remains failed | Explain the failure, scope of the common projection and impact on interpretation. | Passing cutoff checks do not certify the whole system. |
| UI/browser review remains pending | Explain the architecture and use checked assets only; report the limitation. | A documentation milestone does not close F11 or certify the application. |
| External feedback is unavailable | Finish internal checks and clearly identify external review as not received. | An internal check is not lecturer approval. |
| New findings arrive during drafting | Version the evidence register and assess affected chapters/claims before incorporating them. | Older result receipts do not automatically certify newer code or data. |

## 9. Final definition of done

The thesis is **internally complete** only when all mandatory parts are written in English; a first-time reader can follow the complete method; every substantive claim and reported number is traceable; all material limitations are retained; citations, formulas and cross-references are correct; the final PDF has been inspected page by page; and the supplied source package builds independently of the sample directory.

No placeholder content, invented metadata, missing mandatory section, unresolved material numerical error or unverified release dependency may be hidden by marking tasks done. External submission, supervisor approval and institutional acceptance are separate statuses and remain unclaimed until their actual evidence exists.
