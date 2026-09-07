---
condition_id: "119_layer_position_strength_L=28_positions=4_C=16"
axis: "layer_position_strength"
value: "L=28,positions=4,C=16"
is_default: false
swap_log_odds_shift: -0.375
valid_answer_mass: 0.30810225009918213
p4: 0.0033851023763418198
p8: 0.30471715331077576
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/119_layer_position_strength_L=28_positions=4_C=16/run.md"
---

# 119_layer_position_strength_L=28_positions=4_C=16

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
[' spinning', 'web', ' WEB', ' spin', ' atingir', ' spins', ' spiders', '-web']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `119_layer_position_strength_L=28_positions=4_C=16`).

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | 'The'      | -1.188  | 0.304717 | +0.033            |
| 2      | '8'        | -1.188  | 0.304717 | +0.033            |
| 3      | '**'       | -1.313  | 0.268912 | -0.092            |
| 4      | 'Fact'     | -2.563  | 0.077045 | +0.158            |
| 5      | 'Number'   | -4.063  | 0.017191 | +0.033            |
| 6      | '###'      | -4.438  | 0.011815 | -0.217            |
| 7      | '4'        | -5.688  | 0.003385 | -0.342            |
| 8      | '1'        | -6.313  | 0.001812 | +0.033            |
| 9      | 'Answer'   | -6.938  | 0.000970 | +0.033            |
| 10     | 'Complete' | -7.188  | 0.000755 | +0.033            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
