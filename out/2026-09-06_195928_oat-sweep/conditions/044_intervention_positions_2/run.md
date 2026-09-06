---
condition_id: "044_intervention_positions_2"
axis: "intervention_positions"
value: "2"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.2969484031200409
p4: 0.00472337706014514
p8: 0.29222503304481506
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.0
log: "conditions/044_intervention_positions_2/run.md"
---

# 044_intervention_positions_2

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
  "intervention_positions": 2,
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
['ปั่น', '-spin', ' Ủy', 'Spin', ' Presents', 'seh', ' Spin', ' laba']
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
| 1      | '8'      | -1.230  | 0.292225 | -0.009            |
| 2      | 'The'    | -1.230  | 0.292225 | -0.009            |
| 3      | '**'     | -1.230  | 0.292225 | -0.009            |
| 4      | 'Fact'   | -2.605  | 0.073886 | +0.116            |
| 5      | 'Number' | -4.105  | 0.016486 | -0.009            |
| 6      | '###'    | -4.230  | 0.014549 | -0.009            |
| 7      | '4'      | -5.355  | 0.004723 | -0.009            |
| 8      | '1'      | -6.480  | 0.001533 | -0.134            |
| 9      | 'Eight'  | -6.730  | 0.001194 | +0.116            |
| 10     | 'Answer' | -6.855  | 0.001054 | +0.116            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
