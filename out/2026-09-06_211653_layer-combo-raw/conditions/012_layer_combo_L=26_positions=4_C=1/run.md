---
condition_id: "012_layer_combo_L=26_positions=4_C=1"
axis: "layer_combo"
value: "L=26,positions=4,C=1"
is_default: false
swap_log_odds_shift: 0.75
valid_answer_mass: 0.9186896085739136
p4: 0.10951048135757446
p8: 0.8091791272163391
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/012_layer_combo_L=26_positions=4_C=1/run.md"
---

# 012_layer_combo_L=26_positions=4_C=1

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
  "strength": 1.0,
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
['Spider', '丝绸', '-web', ' WEB', 'Web', 'web', ' Silk', 'Disc']
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
    "perturbation_norm": 10.561470031738281,
    "relative_perturbation_by_position": [
      0.22049836814403534,
      0.18564507365226746,
      0.10713490843772888,
      0.21210573613643646
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Does the fact entail the hypothesis?

<think>
Thinking Process:


```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | '8'     | -0.212  | 0.809179 | -0.087            |
| 2      | '4'     | -2.212  | 0.109510 | +0.663            |
| 3      | '6'     | -3.212  | 0.040287 | +0.413            |
| 4      | '1'     | -4.337  | 0.013079 | +0.288            |
| 5      | '3'     | -4.962  | 0.007001 | +0.163            |
| 6      | '2'     | -4.962  | 0.007001 | +0.038            |
| 7      | '5'     | -5.337  | 0.004812 | +0.288            |
| 8      | '7'     | -5.712  | 0.003307 | +0.038            |
| 9      | '9'     | -6.149  | 0.002135 | +0.413            |
| 10     | '0'     | -6.524  | 0.001467 | -0.024            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
