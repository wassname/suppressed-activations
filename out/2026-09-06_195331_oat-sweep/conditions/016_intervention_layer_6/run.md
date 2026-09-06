---
condition_id: "016_intervention_layer_6"
axis: "intervention_layer"
value: "6"
is_default: false
swap_log_odds_shift: -0.25
valid_answer_mass: 0.9553349614143372
p4: 0.024797966703772545
p8: 0.9305369853973389
repeated_bigram_fraction: 0.0
generation_tokens: 4
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
'<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
[' laba', '盐酸', 'Integrated', ' mdi', '\tspin', 'må', 'يلات', ' HttpContext']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', ' perro', 'amax', ' NHÀ']
```

Generation (4 tokens, verbatim):

```text
8<|im_end|>
<|endoftext|>
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '8'       | -0.072  | 0.930537 | -0.021            |
| 2      | '6'       | -3.447  | 0.031841 | +1.229            |
| 3      | '4'       | -3.697  | 0.024798 | -0.271            |
| 4      | '1'       | -5.197  | 0.005533 | +1.354            |
| 5      | '<think>' | -5.947  | 0.002614 | -0.146            |
| 6      | '2'       | -7.072  | 0.000849 | +0.604            |
| 7      | '0'       | -7.197  | 0.000749 | +1.292            |
| 8      | '3'       | -7.447  | 0.000583 | +0.479            |
| 9      | '5'       | -7.759  | 0.000427 | +0.667            |
| 10     | '7'       | -8.009  | 0.000332 | +0.354            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
