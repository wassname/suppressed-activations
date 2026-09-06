---
conditions: 12
metric: "swap_log_odds_shift"
---

# One-at-a-time intervention sweep

Each section varies one axis while all other values stay at the single default. Rows are in
enumeration order, not sorted by outcome. Each log contains the exact prompt, readouts,
top-token distribution, and generated continuation.

| axis                 | value                              | default   | swap log-odds ↑   | p(4)+p(8) ↑   | repeat bigrams ↓   | first token   | donor readout overlap ↑   | log                                                                                                                                          |
|:---------------------|:-----------------------------------|:----------|:------------------|:--------------|:-------------------|:--------------|:--------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------|
| persistent_direction | aggregation=persistent,L=24,C=1    |           | -0.125            | 0.945         | 0.032              | '8'           | 0.000                     | [000_persistent_direction_aggregation=persistent_L=24_C=1](conditions/000_persistent_direction_aggregation=persistent_L=24_C=1/run.md)       |
| persistent_direction | aggregation=persistent,L=24,C=2    |           | +0.000            | 0.946         | 0.032              | '8'           | 0.125                     | [001_persistent_direction_aggregation=persistent_L=24_C=2](conditions/001_persistent_direction_aggregation=persistent_L=24_C=2/run.md)       |
| persistent_direction | aggregation=persistent,L=24,C=4    |           | +0.375            | 0.936         | 0.032              | '8'           | 0.250                     | [002_persistent_direction_aggregation=persistent_L=24_C=4](conditions/002_persistent_direction_aggregation=persistent_L=24_C=4/run.md)       |
| persistent_direction | aggregation=persistent,L=24+26,C=1 |           | -0.125            | 0.946         | 0.032              | '8'           | 0.000                     | [003_persistent_direction_aggregation=persistent_L=24_26_C=1](conditions/003_persistent_direction_aggregation=persistent_L=24_26_C=1/run.md) |
| persistent_direction | aggregation=persistent,L=24+26,C=2 |           | -0.250            | 0.948         | 0.032              | '8'           | 0.125                     | [004_persistent_direction_aggregation=persistent_L=24_26_C=2](conditions/004_persistent_direction_aggregation=persistent_L=24_26_C=2/run.md) |
| persistent_direction | aggregation=persistent,L=24+26,C=4 |           | -0.250            | 0.904         | 0.032              | '8'           | 0.250                     | [005_persistent_direction_aggregation=persistent_L=24_26_C=4](conditions/005_persistent_direction_aggregation=persistent_L=24_26_C=4/run.md) |
| persistent_direction | aggregation=union,L=24,C=1         |           | +0.750            | 0.937         | 0.032              | '8'           | 0.250                     | [006_persistent_direction_aggregation=union_L=24_C=1](conditions/006_persistent_direction_aggregation=union_L=24_C=1/run.md)                 |
| persistent_direction | aggregation=union,L=24,C=2         |           | +2.750            | 0.899         | 0.032              | '4'           | 0.625                     | [007_persistent_direction_aggregation=union_L=24_C=2](conditions/007_persistent_direction_aggregation=union_L=24_C=2/run.md)                 |
| persistent_direction | aggregation=union,L=24,C=4         |           | +4.875            | 0.399         | 0.032              | '6'           | 0.625                     | [008_persistent_direction_aggregation=union_L=24_C=4](conditions/008_persistent_direction_aggregation=union_L=24_C=4/run.md)                 |
| persistent_direction | aggregation=union,L=24+26,C=1      |           | +1.125            | 0.933         | 0.032              | '8'           | 0.250                     | [009_persistent_direction_aggregation=union_L=24_26_C=1](conditions/009_persistent_direction_aggregation=union_L=24_26_C=1/run.md)           |
| persistent_direction | aggregation=union,L=24+26,C=2      |           | +3.750            | 0.940         | 0.032              | '4'           | 0.500                     | [010_persistent_direction_aggregation=union_L=24_26_C=2](conditions/010_persistent_direction_aggregation=union_L=24_26_C=2/run.md)           |
| persistent_direction | aggregation=union,L=24+26,C=4      |           | +6.188            | 0.655         | 0.032              | '4'           | 0.375                     | [011_persistent_direction_aggregation=union_L=24_26_C=4](conditions/011_persistent_direction_aggregation=union_L=24_26_C=4/run.md)           |

-- Codex/gpt-5.6-sol
