---
conditions: 1
metric: "swap_log_odds_shift"
---

# One-at-a-time intervention sweep

Each section varies one axis while all other values stay at the single default. Rows are in
enumeration order, not sorted by outcome. Each log contains the exact prompt, readouts,
top-token distribution, and generated continuation.

| axis    | value   | default   | swap log-odds ↑   | p(4)+p(8) ↑   | repeat bigrams ↓   | first token   | donor readout overlap ↑   | log                                                          |
|:--------|:--------|:----------|:------------------|:--------------|:-------------------|:--------------|:--------------------------|:-------------------------------------------------------------|
| default | default | yes       | +3.750            | 0.940         | 0.032              | '4'           | 0.500                     | [000_default_default](conditions/000_default_default/run.md) |

-- Codex/gpt-5.6-sol
