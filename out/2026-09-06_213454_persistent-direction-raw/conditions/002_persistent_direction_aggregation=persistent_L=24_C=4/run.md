---
condition_id: "002_persistent_direction_aggregation=persistent_L=24_C=4"
axis: "persistent_direction"
value: "aggregation=persistent,L=24,C=4"
is_default: false
swap_log_odds_shift: 0.375
valid_answer_mass: 0.9357997179031372
p4: 0.07963566482067108
p8: 0.8561640381813049
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.25
log: "conditions/002_persistent_direction_aggregation=persistent_L=24_C=4/run.md"
---

# 002_persistent_direction_aggregation=persistent_L=24_C=4

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
  "strength": 4.0,
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
[' doga', ' Quantidade', 'Attack', '高中阶段', 'ปั่น', ' instytuc', ' 장치', '民政部门']
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
    "perturbation_norm": 11.30860710144043,
    "relative_perturbation_by_position": [
      0.4760567843914032
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
| 1      | '8'     | -0.155  | 0.856164 | -0.030            |
| 2      | '4'     | -2.530  | 0.079636 | +0.345            |
| 3      | '6'     | -3.530  | 0.029296 | +0.095            |
| 4      | '1'     | -4.655  | 0.009511 | -0.030            |
| 5      | '3'     | -5.030  | 0.006537 | +0.095            |
| 6      | '2'     | -5.155  | 0.005769 | -0.155            |
| 7      | '5'     | -5.530  | 0.003965 | +0.095            |
| 8      | '7'     | -5.655  | 0.003499 | +0.095            |
| 9      | '0'     | -6.093  | 0.002259 | +0.407            |
| 10     | '9'     | -6.843  | 0.001067 | -0.280            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
