---
conditions: 1
metric: "swap_log_odds_shift"
---

# Intervention sweep

Model: `Qwen/Qwen3.5-4B` at revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`.
Code: `v0.1.1-421-g4668da5`. [Full provenance and measurements](result.json).

Rows are sorted by target-vs-source log-odds movement, in nats. Grid axes and all resolved
settings are in each condition log. C=0 rows are identity controls.
Answer mass and repetition are diagnostics, not semantic success.
Each log contains exact prompts, readouts, top-token distribution, and continuation.

| condition                                                                                                                      | swap log-odds↑   | p(No)↑   | p(Yes)↓   | p(No)+p(Yes) ↑   | repeat bigrams↓   | first token   | donor readout overlap↑   |
|:-------------------------------------------------------------------------------------------------------------------------------|:-----------------|:---------|:----------|:-----------------|:------------------|:--------------|:-------------------------|
| [005_common_basis_location_L30_randshared8_seed0_C1.5](conditions/005_common_basis_location_L30_randshared8_seed0_C1.5/run.md) | +0.156           | 0.0000   | 0.0008    | 0.001            | 0.043             | '1'           | 0.375                    |

-- Codex/GPT-6; renderer originally Codex/gpt-5.6-sol
