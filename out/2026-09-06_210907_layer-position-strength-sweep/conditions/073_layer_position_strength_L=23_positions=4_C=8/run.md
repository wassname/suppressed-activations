---
condition_id: "073_layer_position_strength_L=23_positions=4_C=8"
axis: "layer_position_strength"
value: "L=23,positions=4,C=8"
is_default: false
swap_log_odds_shift: -0.625
valid_answer_mass: 0.30609074234962463
p4: 0.0026254889089614153
p8: 0.30346524715423584
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.5
log: "conditions/073_layer_position_strength_L=23_positions=4_C=8/run.md"
---

# 073_layer_position_strength_L=23_positions=4_C=8

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
  "intervention_positions": 4,
  "strength": 8.0,
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
['compan', ' Ủy', 'seh', '友達', ' Uỷ', ' NHÀ', ' ủy', 'amax']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `073_layer_position_strength_L=23_positions=4_C=8`).

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.192  | 0.303465 | +0.029            |
| 2      | '8'      | -1.192  | 0.303465 | +0.029            |
| 3      | '**'     | -1.317  | 0.267807 | -0.096            |
| 4      | 'Fact'   | -2.567  | 0.076728 | +0.154            |
| 5      | 'Number' | -4.067  | 0.017120 | +0.029            |
| 6      | '###'    | -4.192  | 0.015109 | +0.029            |
| 7      | '4'      | -5.942  | 0.002625 | -0.596            |
| 8      | '1'      | -6.317  | 0.001804 | +0.029            |
| 9      | 'Answer' | -6.942  | 0.000966 | +0.029            |
| 10     | 'Eight'  | -6.942  | 0.000966 | -0.096            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
