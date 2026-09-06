---
condition_id: "023_layer_combo_L=24_26_positions=4_C=8"
axis: "layer_combo"
value: "L=24+26,positions=4,C=8"
is_default: false
swap_log_odds_shift: 5.13671875
valid_answer_mass: 1.8473634781912551e-06
p4: 1.6918319261094439e-06
p8: 1.5553153787095653e-07
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "狗粮"
first_answer: "4"
source_fact_preserved: false
readout_overlap: 0.5
log: "conditions/023_layer_combo_L=24_26_positions=4_C=8/run.md"
---

# 023_layer_combo_L=24_26_positions=4_C=8

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
['吠', '狗粮', ' собак', ' dogs', ' Dogs', 'สุนัข', ' собаки', ' chiens']
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
    "perturbation_norm": 45.59566879272461,
    "relative_perturbation_by_position": [
      0.9045671224594116,
      0.9282092452049255,
      0.6735281944274902,
      1.0742074251174927
    ]
  },
  "26": {
    "residual_norm": 61.63543701171875,
    "perturbation_norm": 73.16549682617188,
    "relative_perturbation_by_position": [
      1.2146939039230347,
      1.212886929512024,
      1.135793685913086,
      1.1886788606643677
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
狗粮
Question: How many legs does the animal that eats dog food have?
Options:
A. 4
B. 2
C.
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '狗粮'      | -1.758  | 0.172312 | +20.582           |
| 2      | 'web'     | -1.946  | 0.142852 | +15.710           |
| 3      | '吠'       | -2.508  | 0.081394 | +20.538           |
| 4      | 'ow'      | -3.383  | 0.033930 | +18.521           |
| 5      | ' canine' | -4.321  | 0.013287 | +16.015           |
| 6      | 'ous'     | -4.696  | 0.009132 | +8.304            |
| 7      | 'is'      | -5.008  | 0.006681 | +16.519           |
| 8      | 'we'      | -5.133  | 0.005896 | +15.648           |
| 9      | 'num'     | -5.196  | 0.005539 | +15.710           |
| 10     | "'"       | -5.321  | 0.004888 | +15.132           |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
