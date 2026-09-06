---
condition_id: "002_lexical_surface_pair=1_C=4"
axis: "lexical_surface"
value: "pair=1,C=4"
is_default: false
swap_log_odds_shift: 0.375
valid_answer_mass: 0.27053138613700867
p4: 0.006216099485754967
p8: 0.26431527733802795
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/002_lexical_surface_pair=1_C=4/run.md"
---

# 002_lexical_surface_pair=1_C=4

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
  "lexical_forms": "pair_1",
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
['-spin', 'Spin', 'ปั่น', ' Ủy', ' Presents', ' Spin', 'seh', ' laba']
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
| 1      | 'The'    | -1.206  | 0.299508 | +0.016            |
| 2      | '**'     | -1.206  | 0.299508 | +0.016            |
| 3      | '8'      | -1.331  | 0.264315 | -0.109            |
| 4      | 'Fact'   | -2.456  | 0.085811 | +0.266            |
| 5      | 'Number' | -4.081  | 0.016897 | +0.016            |
| 6      | '###'    | -4.331  | 0.013159 | -0.109            |
| 7      | '4'      | -5.081  | 0.006216 | +0.266            |
| 8      | '1'      | -6.331  | 0.001781 | +0.016            |
| 9      | 'Eight'  | -6.706  | 0.001224 | +0.141            |
| 10     | '6'      | -6.831  | 0.001080 | +0.141            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
