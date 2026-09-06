---
condition_id: "117_layer_position_strength_L=28_positions=4_C=4"
axis: "layer_position_strength"
value: "L=28,positions=4,C=4"
is_default: false
swap_log_odds_shift: -0.25
valid_answer_mass: 0.3103959858417511
p4: 0.0038587346207350492
p8: 0.3065372407436371
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/117_layer_position_strength_L=28_positions=4_C=4/run.md"
---

# 117_layer_position_strength_L=28_positions=4_C=4

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
  "intervention_layer": 28,
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
'<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
[' spinning', ' spin', ' spins', '纺', 'ปั่น', ' Ủy', '.Sp', '-spin']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "28": {
    "residual_norm": 69.62222290039062,
    "perturbation_norm": 30.762245178222656,
    "relative_perturbation_by_position": [
      0.6032431125640869,
      0.5859467387199402,
      0.19335734844207764,
      0.26768091320991516
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
| 1      | 'The'    | -1.182  | 0.306537 | +0.039            |
| 2      | '8'      | -1.182  | 0.306537 | +0.039            |
| 3      | '**'     | -1.307  | 0.270518 | -0.086            |
| 4      | 'Fact'   | -2.682  | 0.068398 | +0.039            |
| 5      | 'Number' | -4.057  | 0.017294 | +0.039            |
| 6      | '###'    | -4.307  | 0.013468 | -0.086            |
| 7      | '4'      | -5.557  | 0.003859 | -0.211            |
| 8      | '1'      | -6.307  | 0.001823 | +0.039            |
| 9      | 'Answer' | -6.932  | 0.000976 | +0.039            |
| 10     | 'Eight'  | -6.932  | 0.000976 | -0.086            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
