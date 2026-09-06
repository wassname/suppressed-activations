---
condition_id: "069_layer_position_strength_L=23_positions=2_C=16"
axis: "layer_position_strength"
value: "L=23,positions=2,C=16"
is_default: false
swap_log_odds_shift: 0.375
valid_answer_mass: 0.28654664754867554
p4: 0.006584088318049908
p8: 0.27996256947517395
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.375
log: "conditions/069_layer_position_strength_L=23_positions=2_C=16/run.md"
---

# 069_layer_position_strength_L=23_positions=2_C=16

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
  "intervention_layer": 23,
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
['compan', 'seh', ' Ủy', 'amax', ' Uỷ', ' Hunde', ' компре', 'สุนัข']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "23": {
    "residual_norm": 32.133758544921875,
    "perturbation_norm": 25.32521629333496,
    "relative_perturbation_by_position": [
      0.7330233454704285,
      0.8427296876907349
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
| 1      | 'The'    | -1.148  | 0.317239 | +0.073            |
| 2      | '**'     | -1.273  | 0.279963 | -0.052            |
| 3      | '8'      | -1.273  | 0.279963 | -0.052            |
| 4      | 'Fact'   | -2.648  | 0.070786 | +0.073            |
| 5      | 'Number' | -4.023  | 0.017897 | +0.073            |
| 6      | '###'    | -4.273  | 0.013939 | -0.052            |
| 7      | '4'      | -5.023  | 0.006584 | +0.323            |
| 8      | '1'      | -6.398  | 0.001665 | -0.052            |
| 9      | 'Answer' | -6.898  | 0.001010 | +0.073            |
| 10     | 'Eight'  | -7.023  | 0.000891 | -0.177            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
