---
conditions: 1
metric: "swap_log_odds_shift"
---

# Intervention sweep

Model: `wassname/qwen3-5lyr-tiny-random` at revision `main`.
Code: `v0.1.1-333-g413e8a9-dirty`. [Full provenance and measurements](result.json).

Rows are sorted by target-vs-source log-odds movement, in nats. Grid axes and all resolved
settings are in each condition log. C=0 rows are identity controls.
Answer mass and repetition are diagnostics, not semantic success.
Each log contains exact prompts, readouts, top-token distribution, and continuation.

| condition                                                                                          | swap log-odds↑   | p(Ant)↑   | p(Spider)↓   | p(Ant)+p(Spider) ↑   | repeat bigrams↓   | first token   | donor readout overlap↑   |
|:---------------------------------------------------------------------------------------------------|:-----------------|:----------|:-------------|:---------------------|:------------------|:--------------|:-------------------------|
| [000_smoke_detector_D0_2_4_matchedFalse](conditions/000_smoke_detector_D0_2_4_matchedFalse/run.md) | -1.086           | 0.0000    | 0.0000       | 0.000                | 0.000             | 'acr'         | 0.125                    |

-- Codex/GPT-6; renderer originally Codex/gpt-5.6-sol
