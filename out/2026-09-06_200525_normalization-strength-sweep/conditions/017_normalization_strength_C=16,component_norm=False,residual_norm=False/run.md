---
condition_id: "017_normalization_strength_C=16,component_norm=False,residual_norm=False"
axis: "normalization_strength"
value: "C=16,component_norm=False,residual_norm=False"
is_default: false
swap_log_odds_shift: 4.3125
valid_answer_mass: 1.6028521713451482e-05
p4: 8.763404366618488e-06
p8: 7.265117346832994e-06
repeated_bigram_fraction: 0.09677419354838712
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/017_normalization_strength_C=16,component_norm=False,residual_norm=False/run.md"
---

# 017_normalization_strength_C=16,component_norm=False,residual_norm=False

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
  "strength": 16.0,
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
[' blandt', ' परि', 'ńskiej', '老乡', ' Localização', '豆角', 'HTML', '_html']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
**Fact:** The number of legs on the animal that tins webs is **0**.

**Explanation:**
The phrase "animal that tins webs"
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | '**'       | -0.895  | 0.408638 | +0.327            |
| 2      | 'The'      | -1.395  | 0.247851 | -0.173            |
| 3      | 'Fact'     | -1.645  | 0.193027 | +1.077            |
| 4      | '###'      | -3.145  | 0.043070 | +1.077            |
| 5      | 'There'    | -3.395  | 0.033543 | +5.202            |
| 6      | 'It'       | -3.395  | 0.033543 | +7.327            |
| 7      | 'I'        | -4.645  | 0.009610 | +6.389            |
| 8      | 'Based'    | -4.770  | 0.008481 | +3.889            |
| 9      | 'Actually' | -5.895  | 0.002753 | +4.327            |
| 10     | 'Here'     | -6.395  | 0.001670 | +3.327            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
