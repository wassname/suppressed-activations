---
conditions: 1
metric: "swap_log_odds_shift"
---

# Intervention sweep

Model: `Qwen/Qwen3.5-4B` at revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`.
Code: `v0.1.1-411-g1aff515`. [Full provenance and measurements](result.json).

Rows are sorted by target-vs-source log-odds movement, in nats. Grid axes and all resolved
settings are in each condition log. C=0 rows are identity controls.
Answer mass and repetition are diagnostics, not semantic success.
Each log contains exact prompts, readouts, top-token distribution, and continuation.

| condition                                                                                      | swap log-odds↑   | p(Dog)↑   | p(Spider)↓   | p(Dog)+p(Spider) ↑   | repeat bigrams↓   | first token   | donor readout overlap↑   |
|:-----------------------------------------------------------------------------------------------|:-----------------|:----------|:-------------|:---------------------|:------------------|:--------------|:-------------------------|
| [002_common_basis_l25_top8_union_C1.5](conditions/002_common_basis_l25_top8_union_C1.5/run.md) | +11.422          | 0.0080    | 0.0052       | 0.013                | 0.000             | '蜘蛛'          | 0.500                    |

-- Codex/GPT-6; renderer originally Codex/gpt-5.6-sol
