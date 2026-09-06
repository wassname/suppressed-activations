---
condition_id: "016_intervention_layer_6"
axis: "intervention_layer"
value: "6"
is_default: false
swap_log_odds_shift: -1.0
valid_answer_mass: 0.5190528631210327
p4: 0.003068156773224473
p8: 0.5159847140312195
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.0
log: "conditions/016_intervention_layer_6/run.md"
---

# 016_intervention_layer_6

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
  "intervention_layer": 6,
  "intervention_positions": "all",
  "strength": 4.0,
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
[' laba', '\tspin', 'Integrated', 'يلات', '盐酸', ' fär', ' mdi', 'Spin']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. While spiders are arachnids (which have eight legs), they are
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -0.662  | 0.515985 | +0.560            |
| 2      | 'The'    | -1.412  | 0.243734 | -0.190            |
| 3      | '**'     | -1.787  | 0.167516 | -0.565            |
| 4      | 'Fact'   | -3.287  | 0.037378 | -0.565            |
| 5      | 'Number' | -4.787  | 0.008340 | -0.690            |
| 6      | '###'    | -5.037  | 0.006495 | -0.815            |
| 7      | '4'      | -5.787  | 0.003068 | -0.440            |
| 8      | '1'      | -5.787  | 0.003068 | +0.560            |
| 9      | 'Eight'  | -6.037  | 0.002389 | +0.810            |
| 10     | 'Answer' | -6.662  | 0.001279 | +0.310            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
