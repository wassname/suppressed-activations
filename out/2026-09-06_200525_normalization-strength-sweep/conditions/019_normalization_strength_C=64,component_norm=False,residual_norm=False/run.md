---
condition_id: "019_normalization_strength_C=64,component_norm=False,residual_norm=False"
axis: "normalization_strength"
value: "C=64,component_norm=False,residual_norm=False"
is_default: false
swap_log_odds_shift: 4.6875
valid_answer_mass: 8.278573659481481e-05
p4: 5.273706483421847e-05
p8: 3.004867357958574e-05
repeated_bigram_fraction: 0.22580645161290325
generation_tokens: 32
first_token: "It"
readout_overlap: 0.0
log: "conditions/019_normalization_strength_C=64,component_norm=False,residual_norm=False/run.md"
---

# 019_normalization_strength_C=64,component_norm=False,residual_norm=False

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
  "strength": 64.0,
  "match_component_norm": false,
  "restore_residual_norm": false,
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
['公务员考试', '_salt', '的一点', 'adowol', '房产税', '医学院', '这笔', '(utils']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
It looks like you've pasted a string of repeated words with inconsistent spacing and formatting:

> "claim fact claim fact claim fact claim fact claim fact claim
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | 'It'      | -0.913  | 0.401442 | +9.809            |
| 2      | 'The'     | -1.413  | 0.243487 | -0.191            |
| 3      | 'This'    | -2.163  | 0.115015 | +7.871            |
| 4      | 'Your'    | -2.413  | 0.089574 | +10.059           |
| 5      | 'That'    | -3.538  | 0.029080 | +7.996            |
| 6      | 'You'     | -3.788  | 0.022648 | +8.059            |
| 7      | 'There'   | -4.413  | 0.012122 | +4.184            |
| 8      | 'Looking' | -4.413  | 0.012122 | +9.121            |
| 9      | 'Hello'   | -4.538  | 0.010698 | +10.559           |
| 10     | 'Let'     | -4.850  | 0.007827 | +7.434            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
