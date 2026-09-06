---
condition_id: "037_lexical_surface_union_C=2_divide=4"
axis: "lexical_surface"
value: "union,C=2,divide=4"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.2993164360523224
p4: 0.005383568350225687
p8: 0.29393285512924194
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.0
log: "conditions/037_lexical_surface_union_C=2_divide=4/run.md"
---

# 037_lexical_surface_union_C=2_divide=4

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
  "strength": 0.5,
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
['-spin', 'Spin', 'ปั่น', ' Ủy', 'seh', ' Spin', ' Presents', '\tspin']
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
| 1      | '8'      | -1.224  | 0.293933 | -0.003            |
| 2      | 'The'    | -1.224  | 0.293933 | -0.003            |
| 3      | '**'     | -1.224  | 0.293933 | -0.003            |
| 4      | 'Fact'   | -2.724  | 0.065585 | -0.003            |
| 5      | 'Number' | -3.974  | 0.018791 | +0.122            |
| 6      | '###'    | -4.224  | 0.014634 | -0.003            |
| 7      | '4'      | -5.224  | 0.005384 | +0.122            |
| 8      | '1'      | -6.349  | 0.001748 | -0.003            |
| 9      | 'Answer' | -6.849  | 0.001060 | +0.122            |
| 10     | 'Eight'  | -6.849  | 0.001060 | -0.003            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
