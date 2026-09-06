---
condition_id: "099_layer_position_strength_L=26_positions=2_C=16"
axis: "layer_position_strength"
value: "L=26,positions=2,C=16"
is_default: false
swap_log_odds_shift: 0.2500002384185791
valid_answer_mass: 0.285969078540802
p4: 0.0058144256472587585
p8: 0.28015464544296265
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/099_layer_position_strength_L=26_positions=2_C=16/run.md"
---

# 099_layer_position_strength_L=26_positions=2_C=16

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
  "intervention_layer": 26,
  "intervention_positions": 2,
  "strength": 16.0,
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
['ปั่น', '-spin', ' Ủy', 'Spin', ' Presents', 'seh', ' Spin', ' laba']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "26": {
    "residual_norm": 42.33536911010742,
    "perturbation_norm": 28.617441177368164,
    "relative_perturbation_by_position": [
      0.60227370262146,
      0.7535394430160522
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal most commonly associated with spinning webs is the **spider
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.147  | 0.317457 | +0.074            |
| 2      | '**'     | -1.272  | 0.280155 | -0.051            |
| 3      | '8'      | -1.272  | 0.280155 | -0.051            |
| 4      | 'Fact'   | -2.647  | 0.070834 | +0.074            |
| 5      | 'Number' | -4.022  | 0.017910 | +0.074            |
| 6      | '###'    | -4.272  | 0.013948 | -0.051            |
| 7      | '4'      | -5.147  | 0.005814 | +0.199            |
| 8      | '1'      | -6.272  | 0.001888 | +0.074            |
| 9      | 'Answer' | -6.772  | 0.001145 | +0.199            |
| 10     | 'Eight'  | -7.022  | 0.000892 | -0.176            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
