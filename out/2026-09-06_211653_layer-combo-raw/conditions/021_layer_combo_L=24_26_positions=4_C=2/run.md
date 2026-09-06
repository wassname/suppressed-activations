---
condition_id: "021_layer_combo_L=24_26_positions=4_C=2"
axis: "layer_combo"
value: "L=24+26,positions=4,C=2"
is_default: false
swap_log_odds_shift: 4.0
valid_answer_mass: 0.9473592042922974
p4: 0.7363821864128113
p8: 0.21097701787948608
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "4"
first_answer: "4"
source_fact_preserved: true
readout_overlap: 0.5
log: "conditions/021_layer_combo_L=24_26_positions=4_C=2/run.md"
---

# 021_layer_combo_L=24_26_positions=4_C=2

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
    24,
    26
  ],
  "intervention_positions": 4,
  "strength": 2.0,
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
['狗粮', '吠', 'สุนัข', ' собаки', ' собак', ' perros', '养犬', ' cão']
```

Unmodified donor readout:

```python
['吠', ' собаки', '狗粮', 'dog', 'Dog', ' Dog', 'สุนัข', ' canine']
```

Measured intervention norms:

```json
{
  "24": {
    "residual_norm": 50.820335388183594,
    "perturbation_norm": 16.057842254638672,
    "relative_perturbation_by_position": [
      0.30034005641937256,
      0.31660860776901245,
      0.19878952205181122,
      0.42904192209243774
    ]
  },
  "26": {
    "residual_norm": 56.5825309753418,
    "perturbation_norm": 11.648454666137695,
    "relative_perturbation_by_position": [
      0.12547807395458221,
      0.21393463015556335,
      0.11592517048120499,
      0.3331652283668518
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
4.
Hypothesis: The animal that spins webs has 4 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '4'     | -0.306  | 0.736382 | +2.569            |
| 2      | '8'     | -1.556  | 0.210977 | -1.431            |
| 3      | '6'     | -4.056  | 0.017318 | -0.431            |
| 4      | '1'     | -4.556  | 0.010504 | +0.069            |
| 5      | '2'     | -4.806  | 0.008180 | +0.194            |
| 6      | '3'     | -5.306  | 0.004962 | -0.181            |
| 7      | '0'     | -5.556  | 0.003864 | +0.944            |
| 8      | '5'     | -5.931  | 0.002656 | -0.306            |
| 9      | '7'     | -6.494  | 0.001513 | -0.744            |
| 10     | ' '     | -6.931  | 0.000977 | +0.069            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
