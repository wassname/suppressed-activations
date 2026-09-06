---
condition_id: "020_intervention_layer_10"
axis: "intervention_layer"
value: "10"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.4263121783733368
p4: 0.005995495244860649
p8: 0.4203166961669922
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.0
log: "conditions/020_intervention_layer_10/run.md"
---

# 020_intervention_layer_10

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
  "intervention_layer": 10,
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
['Spin', 'ปั่น', '\tspin', '哈密', '_spin', ' laba', ' Ủy', 'seh']
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
| 1      | '8'      | -0.867  | 0.420317 | +0.355            |
| 2      | '**'     | -1.367  | 0.254935 | -0.145            |
| 3      | 'The'    | -1.492  | 0.224979 | -0.270            |
| 4      | 'Fact'   | -3.367  | 0.034502 | -0.645            |
| 5      | 'Number' | -3.742  | 0.023713 | +0.355            |
| 6      | '###'    | -4.117  | 0.016297 | +0.105            |
| 7      | '4'      | -5.117  | 0.005995 | +0.230            |
| 8      | '1'      | -5.492  | 0.004121 | +0.855            |
| 9      | 'Answer' | -6.242  | 0.001946 | +0.730            |
| 10     | '6'      | -6.492  | 0.001516 | +0.480            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
