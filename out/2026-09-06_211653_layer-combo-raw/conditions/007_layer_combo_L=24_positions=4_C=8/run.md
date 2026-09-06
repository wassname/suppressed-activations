---
condition_id: "007_layer_combo_L=24_positions=4_C=8"
axis: "layer_combo"
value: "L=24,positions=4,C=8"
is_default: false
swap_log_odds_shift: 3.5
valid_answer_mass: 0.061829373240470886
p4: 0.041993193328380585
p8: 0.019836178049445152
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "6"
first_answer: null
source_fact_preserved: true
readout_overlap: 0.625
log: "conditions/007_layer_combo_L=24_positions=4_C=8/run.md"
---

# 007_layer_combo_L=24_positions=4_C=8

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
['狗粮', '吠', ' canine', 'สุนัข', ' собак', '狗狗', ' собаки', ' собака']
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
  }
}
```

Generation (32 tokens, verbatim):

```text
6.
Hypothesis: The animal that spins webs has 6 legs.
Does the fact entail the hypothesis?

<think>
Thinking Process:


```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '6'     | -0.420  | 0.656884 | +3.205            |
| 2      | '3'     | -2.545  | 0.078454 | +2.580            |
| 3      | '2'     | -2.545  | 0.078454 | +2.455            |
| 4      | '1'     | -2.670  | 0.069235 | +1.955            |
| 5      | '4'     | -3.170  | 0.041993 | -0.295            |
| 6      | '8'     | -3.920  | 0.019836 | -3.795            |
| 7      | '0'     | -4.045  | 0.017505 | +2.455            |
| 8      | '9'     | -4.420  | 0.012031 | +2.142            |
| 9      | '7'     | -4.420  | 0.012031 | +1.330            |
| 10     | '5'     | -4.420  | 0.012031 | +1.205            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
