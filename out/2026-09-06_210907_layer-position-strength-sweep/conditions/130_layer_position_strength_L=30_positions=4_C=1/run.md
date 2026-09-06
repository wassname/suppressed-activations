---
condition_id: "130_layer_position_strength_L=30_positions=4_C=1"
axis: "layer_position_strength"
value: "L=30,positions=4,C=1"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.29951906204223633
p4: 0.00476426724344492
p8: 0.2947548031806946
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/130_layer_position_strength_L=30_positions=4_C=1/run.md"
---

# 130_layer_position_strength_L=30_positions=4_C=1

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
  "intervention_layer": 30,
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
'<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['纺', 'ปั่น', ' Ủy', '-spin', ' spun', 'Spin', ' Presents', 'seh']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "30": {
    "residual_norm": 89.86124420166016,
    "perturbation_norm": 9.636384963989258,
    "relative_perturbation_by_position": [
      0.142621710896492,
      0.14756417274475098,
      0.045886944979429245,
      0.06778505444526672
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.222  | 0.294755 | -0.000            |
| 2      | 'The'    | -1.222  | 0.294755 | -0.000            |
| 3      | '**'     | -1.222  | 0.294755 | -0.000            |
| 4      | 'Fact'   | -2.722  | 0.065769 | -0.000            |
| 5      | 'Number' | -4.097  | 0.016629 | -0.000            |
| 6      | '###'    | -4.222  | 0.014675 | -0.000            |
| 7      | '4'      | -5.347  | 0.004764 | -0.000            |
| 8      | '1'      | -6.347  | 0.001753 | -0.000            |
| 9      | 'Eight'  | -6.847  | 0.001063 | -0.000            |
| 10     | '6'      | -6.972  | 0.000938 | -0.000            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
