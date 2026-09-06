---
condition_id: "022_layer_combo_L=24_26_positions=4_C=4"
axis: "layer_combo"
value: "L=24+26,positions=4,C=4"
is_default: false
swap_log_odds_shift: 7.375
valid_answer_mass: 0.5852891802787781
p4: 0.5796068906784058
p8: 0.005682264920324087
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "4"
first_answer: "4"
source_fact_preserved: true
readout_overlap: 0.375
log: "conditions/022_layer_combo_L=24_26_positions=4_C=4/run.md"
---

# 022_layer_combo_L=24_26_positions=4_C=4

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
['狗粮', '吠', ' perros', ' собак', ' cães', ' chien', ' собаки', ' chiens']
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
    "perturbation_norm": 29.293386459350586,
    "relative_perturbation_by_position": [
      0.5622907280921936,
      0.5872013568878174,
      0.38306188583374023,
      0.7501310706138611
    ]
  },
  "26": {
    "residual_norm": 57.71877670288086,
    "perturbation_norm": 46.750640869140625,
    "relative_perturbation_by_position": [
      0.8187748789787292,
      0.8844865560531616,
      0.6388750672340393,
      0.90286785364151
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
4.
Hypothesis: The animal that spins webs has 4 legs.
Does the hypothesis follow from the fact?

<think>
Thinking Process:
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '4'       | -0.545  | 0.579607 | +2.330            |
| 2      | '吠'       | -1.670  | 0.188171 | +21.376           |
| 3      | '5'       | -3.670  | 0.025466 | +1.955            |
| 4      | '0'       | -3.670  | 0.025466 | +2.830            |
| 5      | '1'       | -3.670  | 0.025466 | +0.955            |
| 6      | '3'       | -3.983  | 0.018631 | +1.142            |
| 7      | '2'       | -4.233  | 0.014510 | +0.767            |
| 8      | 'four'    | -4.295  | 0.013631 | +11.142           |
| 9      | '狗粮'      | -4.420  | 0.012029 | +17.920           |
| 10     | ' canine' | -5.108  | 0.006049 | +15.228           |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
