---
conditions: 1
metric: "swap_log_odds_shift"
---

# Intervention sweep

Model: `Qwen/Qwen3.5-4B` at revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`.
Code: `v0.1.1-526-gbaeb7d6-dirty`. [Full provenance and measurements](result.json).

Rows are sorted by target-vs-source log-odds movement, in nats. Grid axes and all resolved
settings are in each condition log. C=0 rows are identity controls.
Answer mass and repetition are diagnostics, not semantic success.
Each log contains exact prompts, readouts, top-token distribution, and continuation.

| condition                                                                                                        | swap log-odds↑   | p(Yes)↑   | p(No)↓   | p(Yes)+p(No) ↑   | repeat bigrams↓   | first token   | donor readout overlap↑   |
|:-----------------------------------------------------------------------------------------------------------------|:-----------------|:----------|:---------|:-----------------|:------------------|:--------------|:-------------------------|
| [002_common_basis_earlyloc_v25imported_h3_C1.5](conditions/002_common_basis_earlyloc_v25imported_h3_C1.5/run.md) | -2.750           | 0.0021    | 0.0107   | 0.013            | 0.966             | ' No'         | 0.750                    |

-- Codex/GPT-6; renderer originally Codex/gpt-5.6-sol
