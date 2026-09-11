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

| condition                                                                                      | swap log-odds↑   | p(Yes)↑   | p(No)↓   | p(Yes)+p(No) ↑   | repeat bigrams↓   | first token   | donor readout overlap↑   |
|:-----------------------------------------------------------------------------------------------|:-----------------|:----------|:---------|:-----------------|:------------------|:--------------|:-------------------------|
| [001_common_basis_l25_full_union_C1.5](conditions/001_common_basis_l25_full_union_C1.5/run.md) | +1.312           | 0.0010    | 0.0001   | 0.001            | 0.013             | '1'           | 0.750                    |

-- Codex/GPT-6; renderer originally Codex/gpt-5.6-sol
