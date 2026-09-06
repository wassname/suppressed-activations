---
condition_id: "011_layer_position_strength_L=8_positions=4_C=2"
axis: "layer_position_strength"
value: "L=8,positions=4,C=2"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.2994195520877838
p4: 0.004762684460729361
p8: 0.2946568727493286
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/011_layer_position_strength_L=8_positions=4_C=2/run.md"
---

# 011_layer_position_strength_L=8_positions=4_C=2

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
  "intervention_layer": 8,
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
'<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['-spin', 'Spin', 'ปั่น', ' Spin', 'spin', 'seh', ' Ủy', ' Presents']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "8": {
    "residual_norm": 14.111225128173828,
    "perturbation_norm": 3.1991865634918213,
    "relative_perturbation_by_position": [
      0.32078710198402405,
      0.21788008511066437,
      0.19335994124412537,
      0.13927224278450012
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
| 1      | '8'      | -1.222  | 0.294657 | -0.000            |
| 2      | '**'     | -1.222  | 0.294657 | -0.000            |
| 3      | 'The'    | -1.222  | 0.294657 | -0.000            |
| 4      | 'Fact'   | -2.722  | 0.065747 | -0.000            |
| 5      | 'Number' | -4.097  | 0.016623 | -0.000            |
| 6      | '###'    | -4.222  | 0.014670 | -0.000            |
| 7      | '4'      | -5.347  | 0.004763 | -0.000            |
| 8      | '1'      | -6.347  | 0.001752 | -0.000            |
| 9      | '6'      | -6.597  | 0.001365 | +0.375            |
| 10     | 'Answer' | -6.847  | 0.001063 | +0.125            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
