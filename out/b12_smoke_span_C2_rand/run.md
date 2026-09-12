---
conditions: 1
metric: "swap_log_odds_shift"
---

# Intervention sweep

Model: `wassname/qwen3-5lyr-tiny-random` at revision `main`.
Code: `v0.1.1-339-g1b1424f-dirty`. [Full provenance and measurements](result.json).

Rows are sorted by target-vs-source log-odds movement, in nats. Grid axes and all resolved
settings are in each condition log. C=0 rows are identity controls.
Answer mass and repetition are diagnostics, not semantic success.
Each log contains exact prompts, readouts, top-token distribution, and continuation.

| condition                                                                                      | swap log-odds↑   | p(4)↑   | p(8)↓   | p(4)+p(8) ↑   | repeat bigrams↓   | first token   | donor readout overlap↑   |
|:-----------------------------------------------------------------------------------------------|:-----------------|:--------|:--------|:--------------|:------------------|:--------------|:-------------------------|
| [002_smoke_span_correction_random0_C2](conditions/002_smoke_span_correction_random0_C2/run.md) | -0.945           | 0.0000  | 0.0000  | 0.000         | 0.000             | 'атель'       | 0.000                    |

-- Codex/GPT-6; renderer originally Codex/gpt-5.6-sol
