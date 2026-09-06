---
condition_id: "022_intervention_layer_12"
axis: "intervention_layer"
value: "12"
is_default: false
swap_log_odds_shift: 0.6250002384185791
valid_answer_mass: 0.21232371032238007
p4: 0.006223683245480061
p8: 0.20610003173351288
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/022_intervention_layer_12/run.md"
---

# 022_intervention_layer_12

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
  "intervention_layer": 12,
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
['Spin', '\tspin', ' Presents', 'ปั่น', ' Ủy', '_spin', ' laba', '资讯网']
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
| 1      | '**'     | -0.954  | 0.385046 | +0.267            |
| 2      | 'The'    | -1.204  | 0.299874 | +0.017            |
| 3      | '8'      | -1.579  | 0.206100 | -0.358            |
| 4      | '###'    | -3.079  | 0.045987 | +1.142            |
| 5      | 'Fact'   | -3.829  | 0.021723 | -1.108            |
| 6      | 'Number' | -4.079  | 0.016918 | +0.017            |
| 7      | '4'      | -5.079  | 0.006224 | +0.267            |
| 8      | '6'      | -5.954  | 0.002594 | +1.017            |
| 9      | '1'      | -6.079  | 0.002290 | +0.267            |
| 10     | '#'      | -6.454  | 0.001574 | +0.767            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
