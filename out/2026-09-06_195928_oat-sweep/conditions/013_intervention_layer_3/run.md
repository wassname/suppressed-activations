---
condition_id: "013_intervention_layer_3"
axis: "intervention_layer"
value: "3"
is_default: false
swap_log_odds_shift: -1.125
valid_answer_mass: 0.31202903389930725
p4: 0.0016288309125229716
p8: 0.31040021777153015
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.0
log: "conditions/013_intervention_layer_3/run.md"
---

# 013_intervention_layer_3

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
  "intervention_layer": 3,
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
['seh', ' laba', ' эконом', '惋惜', 'må', 'ค้นหา', 'живания', '可达到']
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
| 1      | '8'      | -1.170  | 0.310400 | +0.052            |
| 2      | 'The'    | -1.295  | 0.273927 | -0.073            |
| 3      | '**'     | -1.295  | 0.273927 | -0.073            |
| 4      | 'Fact'   | -2.295  | 0.100772 | +0.427            |
| 5      | 'Number' | -4.420  | 0.012036 | -0.323            |
| 6      | '###'    | -4.670  | 0.009373 | -0.448            |
| 7      | '1'      | -5.545  | 0.003907 | +0.802            |
| 8      | 'Eight'  | -5.795  | 0.003043 | +1.052            |
| 9      | '4'      | -6.420  | 0.001629 | -1.073            |
| 10     | '2'      | -7.045  | 0.000872 | +0.677            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
