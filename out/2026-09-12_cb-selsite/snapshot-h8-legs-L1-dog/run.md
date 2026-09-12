---
conditions: 1
metric: "swap_log_odds_shift"
---

# Intervention sweep

Model: `Qwen/Qwen3.5-4B` at revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`.
Code: `v0.1.1-493-gf4d86a6-dirty`. [Full provenance and measurements](result.json).

Rows are sorted by target-vs-source log-odds movement, in nats. Grid axes and all resolved
settings are in each condition log. C=0 rows are identity controls.
Answer mass and repetition are diagnostics, not semantic success.
Each log contains exact prompts, readouts, top-token distribution, and continuation.

| condition                                                                                                | swap log-odds↑   | p(4)↑   | p(8)↓   | p(4)+p(8) ↑   | repeat bigrams↓   | first token   | donor readout overlap↑   |
|:---------------------------------------------------------------------------------------------------------|:-----------------|:--------|:--------|:--------------|:------------------|:--------------|:-------------------------|
| [000_common_basis_selsite_snapshot_h8_C1.5](conditions/000_common_basis_selsite_snapshot_h8_C1.5/run.md) | +0.125           | 0.0243  | 0.9104  | 0.935         | 0.000             | '8'           | 0.000                    |

-- Codex/GPT-6; renderer originally Codex/gpt-5.6-sol
