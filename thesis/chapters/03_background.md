# Chapter 3. Theoretical Background and Problem Formulation

> **Draft status: structural skeleton only.** Definitions, equations and explanatory examples have not been written.
> The placeholders below identify the concepts and source checks still needed.

Writing aids: [chapter outline](../outline.md#chapter-3-theoretical-background-and-problem-formulation), [terminology and notation](../evidence.md#5-thuật-ngữ-tiếng-anh-ký-hiệu-và-quy-ước-diễn-đạt) and [shared evidence ledger](../evidence.md#8-khung-bản-thảo-và-đối-soát-luận-điểm).

## 3.1. Observations and time indexing

> **Not yet drafted.** Define OHLCV, observed sessions, cutoff, windows, warm-up and missing records. Explain the engine's window/decision/entry/exit indices and distinguish session offsets from calendar arithmetic; add the decision timeline and define every symbol before use.

## 3.2. Economic contract and prediction target

> **Not yet drafted.** Present the canonical multiplicative net-return equation and both-leg fees/slippage from the shared economic source. Explain LONG entry/exit, SHORT-to-CASH mapping, the strict positive-return label and zero-return handling. Add a clearly labeled illustrative LONG/CASH calculation without changing frozen legacy evidence.

## 3.3. Technical, alpha and sentiment signals

> **Not yet drafted.** Introduce MACD, RSI, Stochastic, Williams %R and ROC before report rules. Define alpha transformations, normalization, orientation and selection; explain dated sentiment and missingness separately. Distinguish votes, confidence, selection diagnostics and calibrated probabilities.

## 3.4. Hidden Markov models for market regimes

> **Not yet drafted.** Define hidden states, emissions, transitions, fitting and endpoint inference with primary citations. Introduce the evaluated VN-Index features, scaler/model cutoffs, state interpretation and fallback; explain why future observations cannot enter endpoint inference.

## 3.5. Bayesian summaries of historical evidence

> **Not yet drafted.** Derive Beta–Bernoulli updates, posterior means and credible intervals, then explain disjoint background shrinkage. Define every count and denominator, separate population support from displayed examples, and add an explicitly illustrative posterior calculation with appropriately limited interval interpretation.

## 3.6. Multi-task context and utility

> **Not yet drafted.** Define prior tasks, matured target observations, an unlabeled query, factual buckets and teacher/student roles. Explain why sign probability differs from expected net return, introduce gain/loss magnitudes and utility differences relative to an anchor, and give a clearly labeled numerical illustration.

## 3.7. Temporal validity and evaluation principles

> **Not yet drafted.** State the price/news cutoffs, exclusion of undated news, strict historical-exit condition and reserved-ID rules. Explain purging, row-wise causality versus outer-cutoff compliance, paired upstream and repeated decisions. Define classification/account evaluation units and undefined-denominator handling; add the chronological partition diagram.
