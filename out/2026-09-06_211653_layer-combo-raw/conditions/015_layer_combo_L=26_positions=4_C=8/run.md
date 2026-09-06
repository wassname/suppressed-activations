---
condition_id: "015_layer_combo_L=26_positions=4_C=8"
axis: "layer_combo"
value: "L=26,positions=4,C=8"
is_default: false
swap_log_odds_shift: 5.25
valid_answer_mass: 0.4124503433704376
p4: 0.3811626136302948
p8: 0.03128772974014282
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "4"
first_answer: "4"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/015_layer_combo_L=26_positions=4_C=8/run.md"
---

# 015_layer_combo_L=26_positions=4_C=8

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
  "strength": 8.0,
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
    "perturbation_norm": 56.013797760009766,
    "relative_perturbation_by_position": [
      1.0998271703720093,
      1.0081344842910767,
      0.7098814249038696,
      1.0600086450576782
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
| 1      | '4'     | -0.965  | 0.381163 | +1.910            |
| 2      | '6'     | -1.840  | 0.158892 | +1.785            |
| 3      | '1'     | -2.090  | 0.123745 | +2.535            |
| 4      | '9'     | -2.465  | 0.085049 | +4.098            |
| 5      | '5'     | -2.715  | 0.066236 | +2.910            |
| 6      | '3'     | -2.840  | 0.058453 | +2.285            |
| 7      | '2'     | -2.840  | 0.058453 | +2.160            |
| 8      | '8'     | -3.465  | 0.031288 | -3.340            |
| 9      | '7'     | -3.465  | 0.031288 | +2.285            |
| 10     | '0'     | -5.465  | 0.004234 | +1.035            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
