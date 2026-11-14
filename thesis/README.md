# Graduation thesis

This directory contains the independent thesis for **Regime-Aware Multi-Task Bayesian In-Context Learning for Multi-Agent LLM Stock Trading in the Vietnamese Stock Market**.

All thesis prose, planning documents, figure labels, table headings, captions and explanatory material will be written in **English**. Original identifiers and source titles may retain their original spelling. Vietnamese source excerpts, if needed as evidence, must be accompanied by an English explanation and a clear indication that the translation is for presentation.

## Reading order

1. [Thesis outline](outline.md): research questions, six chapters, appendices and connections to the implementation.
2. [Detailed writing plan](plan.md): small tasks, dependencies, deliverables, review gates and the path to a complete submission package.
3. [Task checklist](../docs/plan/week12/README.md#thesis-writing-checklist): the single location for task status and completion evidence. The writing plan defines tasks; it does not duplicate their status.

The proposed-method chapter is written for lecturers encountering this system for the first time. Readers should be able to trace a decision from dated inputs to reports, historical context, the LLM proposal, the final policy action and the account outcome without opening the repository.

## Template and evidence

The [sample LaTeX source](../Latex/main.tex) and [sample PDF](../23020332_Tran_Xuan_Bao.pdf) supply organizational and presentation references only. Their research content, author information and bibliography are not part of this thesis. The template suggests front matter, six chapters and references; tables, notation and appendices are adapted to this system.

The [project plan](../docs/plan/plan.md), [integration record](../docs/plan/week12/README.md), implementation and frozen research artifacts provide technical evidence. The [existing paper](../paper/) is an evidence locator, not a substitute for explaining the system from first principles.

The source inventory began at `develop:7a71d4da0dcccded03e46189ce42fea2896f6c80`. The English writing plan and directory migration use `develop:05892c3ec8799a8f3d23ce2eeaaaf0778ea09070` as their starting point, on 14 November 2026. Historical studies retain their own source/runtime pins.

## Scope of the writing work

The deliverable is a complete English thesis with traceable claims, reviewed figures and tables, references, appendices, reproducible LaTeX sources and a visually checked PDF. The plan covers preparation, drafting, revision, typesetting and handover. It does not treat preparation of a plan as completion of the manuscript or authorize new research collection by itself.

Existing negative findings, missing support, unresolved provenance and causal limitations must remain visible. A module implemented in code is not evidence that its corresponding ablation was executed. An offline replay is not a new hosted experiment.

The sample files are locally available but were not tracked by Git at the planning baseline. The final thesis source package must be self-contained and must not require those untracked files to build.

## Working conventions

- Keep manuscript content in `thesis/`; keep project progress in `docs/plan/`.
- Use the proposed file structure in the writing plan, creating files only when their tasks start.
- Maintain one shared evidence register rather than one report per writing task.
- Follow the repository branch and Conventional Commit rules. Documentation-only tasks require appropriate source, link and diff checks, not a fresh full runtime test suite.
- Treat unknown author/supervisor details, institutional requirements and external reviews as explicit open items. Continue independent drafting while those items remain unresolved.
