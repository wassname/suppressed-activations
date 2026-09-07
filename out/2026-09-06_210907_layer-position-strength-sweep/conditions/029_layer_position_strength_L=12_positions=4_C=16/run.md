---
condition_id: "029_layer_position_strength_L=12_positions=4_C=16"
axis: "layer_position_strength"
value: "L=12,positions=4,C=16"
is_default: false
swap_log_odds_shift: 1.75
valid_answer_mass: 0.14879179000854492
p4: 0.012662039138376713
p8: 0.13612975180149078
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/029_layer_position_strength_L=12_positions=4_C=16/run.md"
---

# 029_layer_position_strength_L=12_positions=4_C=16

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
  "intervention_layer": 12,
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
['誇る', '前から', ' Catégorie', 'ılım', ' Ufficio', '项羽', ' Empresarial', ' Bốn']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `029_layer_position_strength_L=12_positions=4_C=16`).

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that naturally "spins webs" to catch prey is the **spider**. While spiders are arachn
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -0.869  | 0.419309 | +0.352            |
| 2      | 'The'    | -1.494  | 0.224440 | -0.273            |
| 3      | '8'      | -1.994  | 0.136130 | -0.773            |
| 4      | 'Fact'   | -2.994  | 0.050079 | -0.273            |
| 5      | '6'      | -3.244  | 0.039002 | +3.727            |
| 6      | '###'    | -3.244  | 0.039002 | +0.977            |
| 7      | 'Number' | -3.494  | 0.030375 | +0.602            |
| 8      | '1'      | -4.244  | 0.014348 | +2.102            |
| 9      | '4'      | -4.369  | 0.012662 | +0.977            |
| 10     | '2'      | -5.244  | 0.005278 | +2.477            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
