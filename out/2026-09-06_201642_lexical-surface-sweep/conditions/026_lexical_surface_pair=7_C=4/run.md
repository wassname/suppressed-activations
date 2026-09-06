---
condition_id: "026_lexical_surface_pair=7_C=4"
axis: "lexical_surface"
value: "pair=7,C=4"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.2895680069923401
p4: 0.005208231508731842
p8: 0.28435978293418884
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/026_lexical_surface_pair=7_C=4/run.md"
---

# 026_lexical_surface_pair=7_C=4

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
  "strength": 4.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "pair_7",
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
['-spin', 'ปั่น', ' Ủy', 'Spin', ' Presents', 'seh', ' Spin', ' laba']
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
| 1      | '**'     | -1.133  | 0.322222 | +0.089            |
| 2      | '8'      | -1.258  | 0.284360 | -0.036            |
| 3      | 'The'    | -1.383  | 0.250947 | -0.161            |
| 4      | 'Fact'   | -2.383  | 0.092318 | +0.339            |
| 5      | 'Number' | -4.008  | 0.018179 | +0.089            |
| 6      | '###'    | -4.383  | 0.012494 | -0.161            |
| 7      | '4'      | -5.258  | 0.005208 | +0.089            |
| 8      | '1'      | -6.383  | 0.001691 | -0.036            |
| 9      | 'Eight'  | -6.758  | 0.001162 | +0.089            |
| 10     | 'Answer' | -6.883  | 0.001026 | +0.089            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
