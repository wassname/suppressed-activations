---
condition_id: "110_layer_position_strength_L=28_positions=2_C=1"
axis: "layer_position_strength"
value: "L=28,positions=2,C=1"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.2857194244861603
p4: 0.004544764757156372
p8: 0.2811746597290039
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/110_layer_position_strength_L=28_positions=2_C=1/run.md"
---

# 110_layer_position_strength_L=28_positions=2_C=1

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
  "intervention_positions": 2,
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
['ปั่น', '-spin', ' Ủy', 'Spin', ' Presents', 'seh', ' Spin', ' laba']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "28": {
    "residual_norm": 50.5933837890625,
    "perturbation_norm": 2.9959716796875,
    "relative_perturbation_by_position": [
      0.04899178445339203,
      0.06857164204120636
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
| 1      | 'The'    | -1.144  | 0.318613 | +0.078            |
| 2      | '**'     | -1.269  | 0.281175 | -0.047            |
| 3      | '8'      | -1.269  | 0.281175 | -0.047            |
| 4      | 'Fact'   | -2.644  | 0.071092 | +0.078            |
| 5      | 'Number' | -4.144  | 0.015863 | -0.047            |
| 6      | '###'    | -4.269  | 0.013999 | -0.047            |
| 7      | '4'      | -5.394  | 0.004545 | -0.047            |
| 8      | '1'      | -6.394  | 0.001672 | -0.047            |
| 9      | 'Answer' | -6.894  | 0.001014 | +0.078            |
| 10     | 'Eight'  | -6.894  | 0.001014 | -0.047            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
