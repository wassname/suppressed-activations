---
condition_id: "014_layer_combo_L=26_positions=4_C=4"
axis: "layer_combo"
value: "L=26,positions=4,C=4"
is_default: false
swap_log_odds_shift: 3.875
valid_answer_mass: 0.7190737128257751
p4: 0.542839527130127
p8: 0.176234170794487
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "4"
first_answer: "4"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/014_layer_combo_L=26_positions=4_C=4/run.md"
---

# 014_layer_combo_L=26_positions=4_C=4

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    23,
    25,
    32
  ],
  "readout_positions": 4,
  "rank": 8,
  "intervention_layer": [
    26
  ],
  "intervention_positions": 4,
  "strength": 4.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1
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
[' Silk', 'Spider', ' spiders', '丝绸', ' silk', '-web', ' spider', ' Spider']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

```json
{
  "26": {
    "residual_norm": 57.977386474609375,
    "perturbation_norm": 37.23801040649414,
    "relative_perturbation_by_position": [
      0.7631722092628479,
      0.6643343567848206,
      0.40822598338127136,
      0.7297347187995911
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
4.
Hypothesis: The animal that spins webs has 4 legs.
Does the fact support the hypothesis?

<think>
Thinking Process:


```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '4'     | -0.611  | 0.542840 | +2.264            |
| 2      | '8'     | -1.736  | 0.176234 | -1.611            |
| 3      | '6'     | -1.861  | 0.155526 | +1.764            |
| 4      | '1'     | -3.236  | 0.039323 | +1.389            |
| 5      | '2'     | -3.861  | 0.021048 | +1.139            |
| 6      | '3'     | -3.986  | 0.018575 | +1.139            |
| 7      | '5'     | -4.111  | 0.016392 | +1.514            |
| 8      | '9'     | -4.111  | 0.016392 | +2.451            |
| 9      | '7'     | -4.611  | 0.009942 | +1.139            |
| 10     | '0'     | -6.361  | 0.001728 | +0.139            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
