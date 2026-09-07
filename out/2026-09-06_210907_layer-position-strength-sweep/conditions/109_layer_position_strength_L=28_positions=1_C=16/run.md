---
condition_id: "109_layer_position_strength_L=28_positions=1_C=16"
axis: "layer_position_strength"
value: "L=28,positions=1,C=16"
is_default: false
swap_log_odds_shift: -0.375
valid_answer_mass: 0.32334113121032715
p4: 0.003552529960870743
p8: 0.3197886049747467
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/109_layer_position_strength_L=28_positions=1_C=16/run.md"
---

# 109_layer_position_strength_L=28_positions=1_C=16

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
  "intervention_positions": 1,
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

[Full diagnostic data](../../result.json) (`rows` → `109_layer_position_strength_L=28_positions=1_C=16`).

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | '8'        | -1.140  | 0.319789 | +0.081            |
| 2      | 'The'      | -1.265  | 0.282212 | -0.044            |
| 3      | '**'       | -1.265  | 0.282212 | -0.044            |
| 4      | 'Fact'     | -2.640  | 0.071354 | +0.081            |
| 5      | 'Number'   | -4.140  | 0.015921 | -0.044            |
| 6      | '###'      | -4.390  | 0.012400 | -0.169            |
| 7      | '4'        | -5.640  | 0.003553 | -0.294            |
| 8      | '1'        | -6.265  | 0.001902 | +0.081            |
| 9      | 'Answer'   | -7.015  | 0.000898 | -0.044            |
| 10     | 'Complete' | -7.140  | 0.000793 | +0.081            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
