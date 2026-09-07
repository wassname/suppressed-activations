---
condition_id: "024_layer_position_strength_L=12_positions=2_C=16"
axis: "layer_position_strength"
value: "L=12,positions=2,C=16"
is_default: false
swap_log_odds_shift: 0.6249997615814209
valid_answer_mass: 0.28281575441360474
p4: 0.008289959281682968
p8: 0.27452579140663147
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/024_layer_position_strength_L=12_positions=2_C=16/run.md"
---

# 024_layer_position_strength_L=12_positions=2_C=16

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

[Full diagnostic data](../../result.json) (`rows` → `024_layer_position_strength_L=12_positions=2_C=16`).

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class *Arachnida*, which
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -1.043  | 0.352498 | +0.179            |
| 2      | '8'      | -1.293  | 0.274526 | -0.071            |
| 3      | 'The'    | -1.418  | 0.242268 | -0.196            |
| 4      | 'Fact'   | -2.918  | 0.054057 | -0.196            |
| 5      | '###'    | -3.543  | 0.028935 | +0.679            |
| 6      | 'Number' | -3.918  | 0.019887 | +0.179            |
| 7      | '4'      | -4.793  | 0.008290 | +0.554            |
| 8      | '1'      | -6.043  | 0.002375 | +0.304            |
| 9      | 'Answer' | -6.293  | 0.001850 | +0.679            |
| 10     | '6'      | -6.418  | 0.001632 | +0.554            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
