---
condition_id: "038_lexical_surface_union_C=4_divide=4"
axis: "lexical_surface"
value: "union,C=4,divide=4"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.29549717903137207
p4: 0.005314873531460762
p8: 0.29018229246139526
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.0
log: "conditions/038_lexical_surface_union_C=4_divide=4/run.md"
---

# 038_lexical_surface_union_C=4_divide=4

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
  "intervention_layer": 1,
  "intervention_positions": "all",
  "strength": 1.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "union",
  "lexical_divisor": 4
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
['-spin', 'Spin', 'ปั่น', ' Spin', '\tspin', ' Ủy', 'spin', 'seh']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.237  | 0.290182 | -0.016            |
| 2      | 'The'    | -1.237  | 0.290182 | -0.016            |
| 3      | '**'     | -1.237  | 0.290182 | -0.016            |
| 4      | 'Fact'   | -2.612  | 0.073370 | +0.109            |
| 5      | 'Number' | -3.862  | 0.021021 | +0.234            |
| 6      | '###'    | -4.237  | 0.014447 | -0.016            |
| 7      | '4'      | -5.237  | 0.005315 | +0.109            |
| 8      | '1'      | -6.237  | 0.001955 | +0.109            |
| 9      | 'Answer' | -6.737  | 0.001186 | +0.234            |
| 10     | 'Eight'  | -6.737  | 0.001186 | +0.109            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
