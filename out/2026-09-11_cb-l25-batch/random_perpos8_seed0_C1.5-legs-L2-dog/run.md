---
conditions: 1
metric: "swap_log_odds_shift"
---

# Intervention sweep

Model: `Qwen/Qwen3.5-4B` at revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`.
Code: `v0.1.1-412-ga930685`. [Full provenance and measurements](result.json).

Rows are sorted by target-vs-source log-odds movement, in nats. Grid axes and all resolved
settings are in each condition log. C=0 rows are identity controls.
Answer mass and repetition are diagnostics, not semantic success.
Each log contains exact prompts, readouts, top-token distribution, and continuation.

| condition                                                                                                          | swap log-odds↑   | p(4)↑   | p(8)↓   | p(4)+p(8) ↑   | repeat bigrams↓   | first token   | donor readout overlap↑   |
|:-------------------------------------------------------------------------------------------------------------------|:-----------------|:--------|:--------|:--------------|:------------------|:--------------|:-------------------------|
| [005_common_basis_l25_random_perpos8_seed0_C1.5](conditions/005_common_basis_l25_random_perpos8_seed0_C1.5/run.md) | +0.250           | 0.0108  | 0.9677  | 0.978         | 0.025             | '8'           | 0.000                    |

-- Codex/GPT-6; renderer originally Codex/gpt-5.6-sol
