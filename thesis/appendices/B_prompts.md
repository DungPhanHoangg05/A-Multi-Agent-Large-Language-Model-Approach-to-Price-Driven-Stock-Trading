# Appendix B. Prompts and Responses

This appendix documents representative request families behind §§4.3,
4.6–4.8 and 4.10. Historical requests use Vietnamese. All natural-language
prompt/reply excerpts below are **English presentation translations**,
not bytes sent to or received from a hosted model. Machine IDs, enums,
numeric counts and the explicitly identified JSON projection retain their
stored values. The archived messages remain authoritative.[^b-source]

## B.1. Families, provenance and redaction

| Family | Content added to the shared reports | Recorded output / no-request distinction |
| --- | --- | --- |
| Component Full / Base | Component-specific information and prompt representations | Separate response collection; Base disables alpha/sentiment sections |
| Context Native / Common | Native versus Common alpha projection/instructions | Base seven-field trade schema; different profiles are declared |
| Bayesian v1 | BRPP population statistics and up to three matured examples | Base schema; Common inherited when retrieval is unavailable |
| C2 / A / B | Ready conditional statistics/examples under the branch's presentation | Base schema in the unified study; fallback if neither view is ready |
| Fact Anchor | Numerical fact card and required assertion IDs | Extended fact schema; NOT_APPLICABLE context; no utility veto |
| MT-BICL | Facts, anchor reference and numerical task/probability/utility projection | Extended fact schema; unsupported context bypasses the request |

The following requests are the stored EX01 point `FPT-2023-07-03`,
upstream realization 0 and Decision repeat 0. Each has one textual user
message. Length counts that message's characters, excluding JSON/HTTP
serialization and the separately supplied structured schema. These four
records are examples, not the study's maximum prompt measurement.

| Role | Original source request ID | Message characters | Request content SHA-256 |
| --- | --- | --- | --- |
| Common | e9cd5100-0f68-4677-8ca5-84a08e41386c | 4186 | b8bca42b5133b1db427cd434001f483f2d76b5a7a3709b4272f84472ab3f185f |
| Bayesian v1 | 4ccd3bbe-9004-468f-a5dd-8859a2c53c97 | 4556 | 8f08017b8031733248e74d73ad03435435f036d85ef70262800ee80e766bd03a |
| Fact Anchor | f7c7664b-69c7-4bef-a075-26c2d9c0d6e2 | 3916 | d2e3c8935e6d7c2a2b09a466bbeddc6c46c7780dfc7e3d5f62db469e4bb1a990 |
| MT-BICL | cc6bf729-784a-458a-8e40-07398fac513f | 4586 | c36361d6537c31a7232f12820c8d50cea837d5442d8d6610dbc1505a1c58476a |

The IDs identify original archived calls, not new executions. Full request
and response digests are bound in the forecast records. No credentials,
authorization headers, environment values or provider-account identifiers
are reproduced. Images and complete report blocks are omitted from these
excerpts; their omission is a presentation choice, not a claim that the
historical request used different reports. Translations and redaction
cannot be used to assert byte-identical replay.

## B.2. Representative decision instructions

**English presentation translation: selected Common instructions.** The
excerpt translates the economic and evidence instructions, not the entire
request or an independently validated market-rule statement.

```text
Choose only LONG or SHORT. LONG requires expecting a positive net result
after brokerage of 0.25% and slippage of 0.10% on each side. If the move
does not cover costs, is flat or is negative, choose SHORT to retain CASH;
do not short the stock or carry it into the next test.

Trend/Pattern describe direction, resistance/support and timing;
Indicator describes momentum. Alpha can veto a breakout lacking money
flow. Sentiment has the lowest priority. Return the required structured
decision and explain supporting and opposing evidence.
```

The archive header contains legacy `T → T+2` and settlement-related
wording. Its presence is recorded rather than silently repaired. The
actual study's entry/exit indices and two-sided cost oracle are those in
§3.2 and [Appendix A.3](A_contracts.md#a3-time-mapping-and-economic-labels):
Open(t+1) to Close(t+3), three observed sessions. Translating a prompt does
not authenticate its regulatory wording or substitute its labels for the
canonical evaluator. Reports can also be compressed before Decision;
these excerpts do not imply that all upstream prose survived the cap.

## B.3. BRPP and anchored context

The stored v1 BRPP excerpt has **369 characters** when
the following report separator is excluded. Its English presentation
translation is below. The translation has a different character length
and is not evidence of compliance with the historical 600-character cap.

```text
[BRPP v1] R=CONSOLIDATION; n=19; k=3
LONGwin=9/19(47.4%); Trap=9/18(50.0%); TrendFail=7/14(50.0%); PatternFail=9/18(50.0%)
T/P/A/I: + bullish, - bearish, 0 neutral; W/L=net LONG after costs;
SHORT=CASH; S=unavailable news.
FPT@2022-04-07 R=CONSOLIDATION T/P/A/I=+++- W +0.88%
FPT@2022-04-18 R=CONSOLIDATION T/P/A/I=++0- L -4.53%
FPT@2022-04-13 R=CONSOLIDATION T/P/A/I=++-- L -0.44%
```

The three examples are not the population size: `n=19` concerns eligible
historical support, while the metric denominators differ and `k=3` counts
displayed records. These rounded presentation values are not replacements
for stored full-precision returns or maturity checks. C2/A/B similarly
render only ready evidence; their statistics and examples have independent
readiness conditions (§4.7).

**English presentation translation: anchored instruction excerpt.**

```text
FACTS are point-in-time numerical values. Copy all three fact IDs and
assertions; distinguish MACD below zero from MACD below Signal. Agent
reports are not themselves proven numerical facts. LONG buys at Open(t+1)
and closes at Close(t+3), paying costs on each leg; SHORT means CASH.
The final reply must satisfy the declared JSON contract.
```

Fact Anchor receives the fact card but no MT task projection, numerical
probability or utility distribution. MT receives its permitted numerical
projection and a short anchor/source reference in addition to facts.
Those contexts are not interchangeable prefixes. The external resolver
checks eligibility and assertions and decides whether to retain or revise
the anchor; a model's favorable explanation does not bypass that policy.

## B.4. Reply schemas and recorded example

**Table B-app1. Base seven-field interface.** This is a compact field
description of `TradeDecisionOutput`, not a replacement JSON Schema.

| Field | Type / restriction | Meaning |
| --- | --- | --- |
| `decision` | LONG or SHORT | Raw proposal, before external action mapping |
| `forecast_horizon` | String | Reported horizon; evaluator uses the study contract |
| `confidence` | String | Self-reported category/text, not a calibrated probability |
| `risk_reward_ratio` | Number in [1,5] | Reported R:R, not account Sharpe or an alternative exit rule |
| `evidence_for`, `evidence_against`, `justification` | Strings | Explanatory evidence, not independently verified ground truth |

The anchor/MT schema `utility_icl_reply_v3` additionally requires
`version`, three unique `fact_ids`, the exact `fact_assertions` object and
`context_reason`. `MACD_SIGNAL` and `PRICE_SMA20` admit
ABOVE/BELOW/EQUAL/UNKNOWN; `MACD_ZERO` admits
POSITIVE/NEGATIVE/ZERO/UNKNOWN. The context enum is NOT_APPLICABLE,
SUPPORTED, UTILITY_UNSUPPORTED, QUERY_FEATURE_UNAVAILABLE, UNKNOWN_BUCKET
or TARGET_COLD_START. Application rules constrain which reason is valid
for each branch; enum membership alone is insufficient.

A separate `TradeDecisionPriorOutput` builder also defines strict
`prior_use` metric/example IDs and an assessment. Its existence is not a
claim that the unified eight-role study used that extra trace schema or
completed a C3/matched ablation.

The following is an **exact machine-field projection** of EX01's MT
reply for original request `cc6bf729-784a-458a-8e40-07398fac513f`.
It omits horizon, confidence and explanatory strings, so it is not a
complete reply to validate against the full schema.

```json
{
  "version": "utility_icl_reply_v3",
  "decision": "LONG",
  "risk_reward_ratio": 1.5,
  "fact_ids": [
    "MACD_SIGNAL",
    "MACD_ZERO",
    "PRICE_SMA20"
  ],
  "fact_assertions": {
    "MACD_SIGNAL": "BELOW",
    "MACD_ZERO": "POSITIVE",
    "PRICE_SMA20": "ABOVE"
  },
  "context_reason": "SUPPORTED"
}
```

The stored confidence is a Vietnamese categorical word, translated as
“High”; it is not a numerical sign probability. An English translation
of the justification is: “The combination of MACD_SIGNAL BELOW and
PRICE_SMA20 ABOVE favors entering LONG at Open(t+1) and closing at
Close(t+3).” This is the model's assertion. The actual policy reason is
`KEEP_PROPOSED_SAME`: the proposal already equals the anchor. As §4.10.5
shows, this LONG later has a negative net outcome. Neither the schema's
validity nor the translated explanation changes that result.

## B.5. Budgets, repair and interpretation

| Object | Locked limit / measurement | Scope |
| --- | --- | --- |
| Backtest Trend / Pattern / Indicator report caps | 800 characters each | Common-based historical requests |
| Backtest Alpha / Sentiment caps | 1,100 / 500 characters | Distilled/capped report blocks |
| Signal-prior prefix / fact card / anchor card | 600 / 700 / 80 characters | Distinct builders; not a shared 600-character allowance |
| Final assembled text | Strictly fewer than 6,500 characters, including repair additions | Checked before dispatch; not a token limit |
| Recorded U08 maximum | 4,750 characters including repair | Historical source-scoped measurement, not these four examples alone |

`_distill_report` and `_cap_report` retain their historical behavior.
Format repair adds instructions only under the recorded attempt contract;
it is not a new market point, a retry for action agreement or authority to
weaken the schema. Transport limits, client retries and historical HTTP
attempt scopes remain distinct (§4.10 and Appendix E).

[^b-source]: Frozen Decision source, `mt_bicl_decision.py`/`mt_bicl_contracts.py`, `mt_bicl.schema.json`, EX01 prepare/forecast/raw IDs, and U08 prompt audit; ledger CL035–CL037/CL089–CL101/CL106–CL110, §9.16–§9.20 and §13.5. Original message/reply bytes remain in the pinned U08 archive; no fresh inference or translated request is sent.
