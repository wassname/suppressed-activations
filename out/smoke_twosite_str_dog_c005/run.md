---
conditions: 1
metric: "swap_log_odds_shift"
---

# Intervention sweep

Model: `wassname/qwen3-5lyr-tiny-random` at revision `main`.
Code: `v0.1.1-369-g3dad1ca-dirty`. [Full provenance and measurements](result.json).

Rows are sorted by target-vs-source log-odds movement, in nats. Grid axes and all resolved
settings are in each condition log. C=0 rows are identity controls.
Answer mass and repetition are diagnostics, not semantic success.
Each log contains exact prompts, readouts, top-token distribution, and continuation.

| condition                                                                                                  | swap log-odds↑   | p(Yes)↑   | p(No)↓   | p(Yes)+p(No) ↑   | repeat bigrams↓   | first token   | donor readout overlap↑   |
|:-----------------------------------------------------------------------------------------------------------|:-----------------|:----------|:---------|:-----------------|:------------------|:--------------|:-------------------------|
| [000_smoke_two_site_strength_prop-dog-C0.05](conditions/000_smoke_two_site_strength_prop-dog-C0.05/run.md) | +0.203           | 0.0000    | 0.0000   | 0.000            | 0.000             | ' textView'   | 0.000                    |

-- Codex/GPT-6; renderer originally Codex/gpt-5.6-sol
