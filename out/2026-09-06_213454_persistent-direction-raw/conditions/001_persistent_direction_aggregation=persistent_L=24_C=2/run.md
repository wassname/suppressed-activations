---
condition_id: "001_persistent_direction_aggregation=persistent_L=24_C=2"
axis: "persistent_direction"
value: "aggregation=persistent,L=24,C=2"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.9456207156181335
p4: 0.056819185614585876
p8: 0.8888015151023865
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.125
log: "conditions/001_persistent_direction_aggregation=persistent_L=24_C=2/run.md"
---

# 001_persistent_direction_aggregation=persistent_L=24_C=2

Resolved config:

```json
{
  "aggregation": "persistent",
  "detector_layers": [
    23,
    25,
    32
  ],
  "readout_positions": 4,
  "rank": 8,
  "intervention_layer": [
    24
  ],
  "intervention_positions": 1,
  "strength": 2.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1,
  "continue_generation": false
}
```

Source input (`repr`):

```python
'Fact: The number of legs on the animal that spins webs is '
```

Donor input (`repr`):

```python
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Readout after intervention:

```python
[' doga', 'edata', 'ปั่น', 'Attack', '高中阶段', ' 장치', '的战', ' måde']
```

Unmodified donor readout:

```python
[' doga', ' patologie', ' verlassen', ' Emas', ' Quantidade', '_approval', ' Unik', ' врач']
```

Measured intervention norms:

```json
{
  "24": {
    "residual_norm": 23.754743576049805,
    "perturbation_norm": 5.980884075164795,
    "relative_perturbation_by_position": [
      0.25177639722824097
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '8'     | -0.118  | 0.888802 | +0.007            |
| 2      | '4'     | -2.868  | 0.056819 | +0.007            |
| 3      | '6'     | -3.743  | 0.023686 | -0.118            |
| 4      | '1'     | -4.743  | 0.008714 | -0.118            |
| 5      | '2'     | -5.243  | 0.005285 | -0.243            |
| 6      | '3'     | -5.243  | 0.005285 | -0.118            |
| 7      | '5'     | -5.618  | 0.003632 | +0.007            |
| 8      | '7'     | -5.868  | 0.002829 | -0.118            |
| 9      | '0'     | -6.368  | 0.001716 | +0.132            |
| 10     | '9'     | -6.868  | 0.001041 | -0.305            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
