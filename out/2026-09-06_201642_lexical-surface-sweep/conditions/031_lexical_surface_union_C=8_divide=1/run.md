---
condition_id: "031_lexical_surface_union_C=8_divide=1"
axis: "lexical_surface"
value: "union,C=8,divide=1"
is_default: false
swap_log_odds_shift: 3.0
valid_answer_mass: 0.010399705730378628
p4: 0.0025488119572401047
p8: 0.007850893773138523
repeated_bigram_fraction: 0.12903225806451613
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/031_lexical_surface_union_C=8_divide=1/run.md"
---

# 031_lexical_surface_union_C=8_divide=1

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
  "strength": 8.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "union",
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
['Spin', '\tspin', 'rotation', '-spin', 'spin', '旋转', ' Rotation', 'Rotation']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
**Fact:** The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal that spins webs is a **spider
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | '**'       | -0.722  | 0.485718 | +0.499            |
| 2      | 'The'      | -1.347  | 0.259986 | -0.126            |
| 3      | '###'      | -2.472  | 0.084405 | +1.749            |
| 4      | 'Fact'     | -2.972  | 0.051194 | -0.251            |
| 5      | 'Number'   | -2.972  | 0.051194 | +1.124            |
| 6      | '8'        | -4.847  | 0.007851 | -3.626            |
| 7      | 'Based'    | -4.847  | 0.007851 | +3.812            |
| 8      | 'Complete' | -5.347  | 0.004762 | +1.874            |
| 9      | '6'        | -5.472  | 0.004202 | +1.499            |
| 10     | 'There'    | -5.472  | 0.004202 | +3.124            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
