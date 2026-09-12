---
conditions: 1
metric: "swap_log_odds_shift"
---

# Intervention sweep

Model: `Qwen/Qwen3.5-4B` at revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`.
Code: `v0.1.1-473-g31d3731`. [Full provenance and measurements](result.json).

Rows are sorted by target-vs-source log-odds movement, in nats. Grid axes and all resolved
settings are in each condition log. C=0 rows are identity controls.
Answer mass and repetition are diagnostics, not semantic success.
Each log contains exact prompts, readouts, top-token distribution, and continuation.

| condition                                                                      | swap log-odds↑   | p(No)↑   | p(Yes)↓   | p(No)+p(Yes) ↑   | repeat bigrams↓   | first token   | donor readout overlap↑   |
|:-------------------------------------------------------------------------------|:-----------------|:---------|:----------|:-----------------|:------------------|:--------------|:-------------------------|
| [003_common_basis_ablation_C0](conditions/003_common_basis_ablation_C0/run.md) | +0.000           | 0.0000   | 0.0005    | 0.000            | 0.043             | '1'           | 0.875                    |

-- Codex/GPT-6; renderer originally Codex/gpt-5.6-sol
