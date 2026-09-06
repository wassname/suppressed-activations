---
condition_id: "002_layer_combo_L=24_positions=1_C=4"
axis: "layer_combo"
value: "L=24,positions=1,C=4"
is_default: false
swap_log_odds_shift: 4.875
valid_answer_mass: 0.398831844329834
p4: 0.35628023743629456
p8: 0.04255160689353943
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "6"
first_answer: null
source_fact_preserved: true
readout_overlap: 0.625
log: "conditions/002_layer_combo_L=24_positions=1_C=4/run.md"
---

# 002_layer_combo_L=24_positions=1_C=4

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
['狗粮', '吠', ' canine', 'สุนัข', ' собаки', ' собак', '狗狗', ' perros']
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
    "perturbation_norm": 17.819171905517578,
    "relative_perturbation_by_position": [
      0.7501310706138611
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
| 1      | '6'     | -0.782  | 0.457473 | +2.843            |
| 2      | '4'     | -1.032  | 0.356280 | +1.843            |
| 3      | '1'     | -3.032  | 0.048217 | +1.593            |
| 4      | '8'     | -3.157  | 0.042552 | -3.032            |
| 5      | '2'     | -3.157  | 0.042552 | +1.843            |
| 6      | '3'     | -4.032  | 0.017738 | +1.093            |
| 7      | '0'     | -4.157  | 0.015654 | +2.343            |
| 8      | '9'     | -5.032  | 0.006525 | +1.530            |
| 9      | '7'     | -5.157  | 0.005759 | +0.593            |
| 10     | '5'     | -5.282  | 0.005082 | +0.343            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
