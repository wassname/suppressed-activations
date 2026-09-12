---
conditions: 1
metric: "swap_log_odds_shift"
---

# Intervention sweep

Model: `Qwen/Qwen3.5-4B` at revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`.
Code: `v0.1.1-371-gf1b5147`. [Full provenance and measurements](result.json).

Rows are sorted by target-vs-source log-odds movement, in nats. Grid axes and all resolved
settings are in each condition log. C=0 rows are identity controls.
Answer mass and repetition are diagnostics, not semantic success.
Each log contains exact prompts, readouts, top-token distribution, and continuation.

| condition                                                                                      | swap log-odds↑   | p(Yes)↑   | p(No)↓   | p(Yes)+p(No) ↑   | repeat bigrams↓   | first token   | donor readout overlap↑   |
|:-----------------------------------------------------------------------------------------------|:-----------------|:----------|:---------|:-----------------|:------------------|:--------------|:-------------------------|
| [000_two_site_strength_prop-dog-C0.05](conditions/000_two_site_strength_prop-dog-C0.05/run.md) | +0.312           | 0.0012    | 0.0002   | 0.001            | 0.014             | ' No'         | 0.500                    |

-- Codex/GPT-6; renderer originally Codex/gpt-5.6-sol
