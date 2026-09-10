---
conditions: 1
metric: "swap_log_odds_shift"
---

# Intervention sweep

Model: `Qwen/Qwen3.5-4B` at revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`.
Code: `v0.1.1-394-gb488cc0`. [Full provenance and measurements](result.json).

Rows are sorted by target-vs-source log-odds movement, in nats. Grid axes and all resolved
settings are in each condition log. C=0 rows are identity controls.
Answer mass and repetition are diagnostics, not semantic success.
Each log contains exact prompts, readouts, top-token distribution, and continuation.

| condition                                                                          | swap log-odds↑   | p(6)↑   | p(8)↓   | p(6)+p(8) ↑   | repeat bigrams↓   | first token   | donor readout overlap↑   |
|:-----------------------------------------------------------------------------------|:-----------------|:--------|:--------|:--------------|:------------------|:--------------|:-------------------------|
| [003_span_correction_sweep_C1.5](conditions/003_span_correction_sweep_C1.5/run.md) | +9.625           | 0.9870  | 0.0017  | 0.989         | 0.000             | '6'           | 0.375                    |

-- Codex/GPT-6; renderer originally Codex/gpt-5.6-sol
