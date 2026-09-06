---
condition_id: "003_layer_combo_L=24_positions=1_C=8"
axis: "layer_combo"
value: "L=24,positions=1,C=8"
is_default: false
swap_log_odds_shift: 2.875
valid_answer_mass: 0.07337214797735214
p4: 0.038975972682237625
p8: 0.03439617529511452
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "6"
first_answer: null
source_fact_preserved: true
readout_overlap: 0.625
log: "conditions/003_layer_combo_L=24_positions=1_C=8/run.md"
---

# 003_layer_combo_L=24_positions=1_C=8

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
    24
  ],
  "intervention_positions": 1,
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
['吠', '狗粮', ' canine', 'สุนัข', ' собак', ' собаки', '狗狗', ' собака']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

```json
{
  "24": {
    "residual_norm": 23.754743576049805,
    "perturbation_norm": 25.517520904541016,
    "relative_perturbation_by_position": [
      1.0742074251174927
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
6.
Hypothesis: The animal that spins webs has 6 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '6'     | -0.370  | 0.690866 | +3.255            |
| 2      | '3'     | -2.745  | 0.064261 | +2.380            |
| 3      | '2'     | -2.745  | 0.064261 | +2.255            |
| 4      | '1'     | -2.870  | 0.056710 | +1.755            |
| 5      | '4'     | -3.245  | 0.038976 | -0.370            |
| 6      | '8'     | -3.370  | 0.034396 | -3.245            |
| 7      | '5'     | -4.120  | 0.016248 | +1.505            |
| 8      | '7'     | -4.120  | 0.016248 | +1.630            |
| 9      | '9'     | -4.620  | 0.009855 | +1.943            |
| 10     | '0'     | -5.120  | 0.005977 | +1.380            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
