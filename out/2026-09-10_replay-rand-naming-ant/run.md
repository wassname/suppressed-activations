---
conditions: 1
metric: "swap_log_odds_shift"
---

# Intervention sweep

Model: `Qwen/Qwen3.5-4B` at revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`.
Code: `v0.1.1-386-g0b9ad07`. [Full provenance and measurements](result.json).

Rows are sorted by target-vs-source log-odds movement, in nats. Grid axes and all resolved
settings are in each condition log. C=0 rows are identity controls.
Answer mass and repetition are diagnostics, not semantic success.
Each log contains exact prompts, readouts, top-token distribution, and continuation.

| condition                                                                                                    | swap log-odds↑   | p(Ant)↑   | p(Spider)↓   | p(Ant)+p(Spider) ↑   | repeat bigrams↓   | first token   | donor readout overlap↑   |
|:-------------------------------------------------------------------------------------------------------------|:-----------------|:----------|:-------------|:---------------------|:------------------|:--------------|:-------------------------|
| [006_span_correction_sweep_inspan_seed0_C2.0](conditions/006_span_correction_sweep_inspan_seed0_C2.0/run.md) | +4.563           | 0.0001    | 0.0209       | 0.021                | 0.465             | '8'           | 0.125                    |

-- Codex/GPT-6; renderer originally Codex/gpt-5.6-sol
