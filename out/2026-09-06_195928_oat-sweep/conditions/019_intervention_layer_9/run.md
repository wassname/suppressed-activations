---
condition_id: "019_intervention_layer_9"
axis: "intervention_layer"
value: "9"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.3625841736793518
p4: 0.006521514616906643
p8: 0.356062650680542
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.0
log: "conditions/019_intervention_layer_9/run.md"
---

# 019_intervention_layer_9

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
  "intervention_layer": 9,
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
['-spin', 'Spin', 'ปั่น', 'spin', '纺', '\tspin', '_spin', ' Ủy']
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
| 1      | '8'      | -1.033  | 0.356063 | +0.189            |
| 2      | '**'     | -1.158  | 0.314224 | +0.064            |
| 3      | 'The'    | -1.783  | 0.168192 | -0.561            |
| 4      | 'Fact'   | -2.408  | 0.090027 | +0.314            |
| 5      | 'Number' | -3.783  | 0.022762 | +0.314            |
| 6      | '###'    | -3.908  | 0.020088 | +0.314            |
| 7      | '4'      | -5.033  | 0.006522 | +0.314            |
| 8      | '1'      | -5.408  | 0.004482 | +0.939            |
| 9      | '6'      | -6.158  | 0.002117 | +0.814            |
| 10     | 'Answer' | -6.658  | 0.001284 | +0.314            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
