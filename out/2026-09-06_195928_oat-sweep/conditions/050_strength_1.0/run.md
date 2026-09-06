---
condition_id: "050_strength_1.0"
axis: "strength"
value: "1.0"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.27522215247154236
p4: 0.004377791192382574
p8: 0.27084437012672424
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/050_strength_1.0/run.md"
---

# 050_strength_1.0

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
  "donor_position_offset": 0
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
['Spin', 'spin', '-spin', '\tspin', ' Spin', '_spin', '盐酸', ' laba']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class *Arachnida*, which
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.181  | 0.306907 | +0.040            |
| 2      | '**'     | -1.181  | 0.306907 | +0.040            |
| 3      | '8'      | -1.306  | 0.270844 | -0.085            |
| 4      | 'Fact'   | -2.681  | 0.068480 | +0.040            |
| 5      | 'Number' | -4.181  | 0.015280 | -0.085            |
| 6      | '###'    | -4.306  | 0.013485 | -0.085            |
| 7      | '4'      | -5.431  | 0.004378 | -0.085            |
| 8      | '1'      | -6.431  | 0.001610 | -0.085            |
| 9      | 'Answer' | -6.681  | 0.001254 | +0.290            |
| 10     | 'Eight'  | -6.681  | 0.001254 | +0.165            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
