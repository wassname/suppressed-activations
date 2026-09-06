---
condition_id: "029_lexical_surface_union_C=2_divide=1"
axis: "lexical_surface"
value: "union,C=2,divide=1"
is_default: false
swap_log_odds_shift: 0.5
valid_answer_mass: 0.27071067690849304
p4: 0.007026932667940855
p8: 0.2636837363243103
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/029_lexical_surface_union_C=2_divide=1/run.md"
---

# 029_lexical_surface_union_C=2_divide=1

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
  "strength": 2.0,
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
['Spin', '-spin', 'spin', '\tspin', ' Spin', 'ปั่น', '_spin', 'seh']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.208  | 0.298793 | +0.014            |
| 2      | '**'     | -1.208  | 0.298793 | +0.014            |
| 3      | '8'      | -1.333  | 0.263684 | -0.111            |
| 4      | 'Fact'   | -2.583  | 0.075547 | +0.139            |
| 5      | 'Number' | -3.708  | 0.024526 | +0.389            |
| 6      | '###'    | -4.208  | 0.014876 | +0.014            |
| 7      | '4'      | -4.958  | 0.007027 | +0.389            |
| 8      | '1'      | -6.083  | 0.002281 | +0.264            |
| 9      | '6'      | -6.583  | 0.001384 | +0.389            |
| 10     | 'Eight'  | -6.583  | 0.001384 | +0.264            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
