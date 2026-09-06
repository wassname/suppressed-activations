---
condition_id: "034_intervention_layer_24"
axis: "intervention_layer"
value: "24"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.29685235023498535
p4: 0.004721850156784058
p8: 0.2921305000782013
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.75
log: "conditions/034_intervention_layer_24/run.md"
---

# 034_intervention_layer_24

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
  "intervention_layer": 24,
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
['compan', ' NHÀ', '友達', ' cão', ' собаки', 'amax', ' Austr', ' собака']
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
| 1      | '8'      | -1.231  | 0.292131 | -0.009            |
| 2      | 'The'    | -1.231  | 0.292131 | -0.009            |
| 3      | '**'     | -1.231  | 0.292131 | -0.009            |
| 4      | 'Fact'   | -2.606  | 0.073862 | +0.116            |
| 5      | 'Number' | -4.106  | 0.016481 | -0.009            |
| 6      | '###'    | -4.231  | 0.014544 | -0.009            |
| 7      | '4'      | -5.356  | 0.004722 | -0.009            |
| 8      | '1'      | -6.356  | 0.001737 | -0.009            |
| 9      | 'Answer' | -6.731  | 0.001194 | +0.241            |
| 10     | 'Eight'  | -6.731  | 0.001194 | +0.116            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
