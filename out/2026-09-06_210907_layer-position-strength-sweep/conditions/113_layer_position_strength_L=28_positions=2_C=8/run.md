---
condition_id: "113_layer_position_strength_L=28_positions=2_C=8"
axis: "layer_position_strength"
value: "L=28,positions=2,C=8"
is_default: false
swap_log_odds_shift: -0.25
valid_answer_mass: 0.29955607652664185
p4: 0.003723976667970419
p8: 0.295832097530365
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/113_layer_position_strength_L=28_positions=2_C=8/run.md"
---

# 113_layer_position_strength_L=28_positions=2_C=8

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
['ปั่น', '-spin', ' Ủy', 'Spin', ' Presents', 'seh', ' Spin', ' laba']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `113_layer_position_strength_L=28_positions=2_C=8`).

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.218  | 0.295832 | +0.004            |
| 2      | 'The'    | -1.218  | 0.295832 | +0.004            |
| 3      | '**'     | -1.218  | 0.295832 | +0.004            |
| 4      | 'Fact'   | -2.718  | 0.066009 | +0.004            |
| 5      | 'Number' | -4.093  | 0.016690 | +0.004            |
| 6      | '###'    | -4.343  | 0.012998 | -0.121            |
| 7      | '4'      | -5.593  | 0.003724 | -0.246            |
| 8      | '1'      | -6.218  | 0.001993 | +0.129            |
| 9      | 'Answer' | -6.968  | 0.000942 | +0.004            |
| 10     | 'Eight'  | -7.093  | 0.000831 | -0.246            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
