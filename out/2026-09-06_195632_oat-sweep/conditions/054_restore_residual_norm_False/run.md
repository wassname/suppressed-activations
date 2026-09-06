---
condition_id: "054_restore_residual_norm_False"
axis: "restore_residual_norm"
value: "False"
is_default: false
swap_log_odds_shift: 1.375
valid_answer_mass: 0.00040126635576598346
p4: 3.040491947103874e-06
p8: 0.00039822584949433804
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/054_restore_residual_norm_False/run.md"
---

# 054_restore_residual_norm_False

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
  "restore_residual_norm": false,
  "donor_position_offset": 0
}
```

Source input (`repr`):

```python
'<|im_start|>user\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['丝绸', '在校园', '的战', 'Kate', ' факта', '_rsp', '迪斯', ' división']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, and all spiders have **eight legs**. This distinguishes them
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | 'The'      | -0.203  | 0.815877 | -0.107            |
| 2      | 'Based'    | -2.078  | 0.125119 | +0.643            |
| 3      | 'There'    | -4.453  | 0.011638 | +2.643            |
| 4      | 'Sp'       | -4.828  | 0.007999 | +0.768            |
| 5      | 'To'       | -5.078  | 0.006229 | +0.643            |
| 6      | '**'       | -5.578  | 0.003778 | +0.643            |
| 7      | 'An'       | -5.828  | 0.002943 | +0.268            |
| 8      | 'Actually' | -5.828  | 0.002943 | +2.768            |
| 9      | 'It'       | -5.953  | 0.002597 | +3.393            |
| 10     | 'That'     | -5.953  | 0.002597 | +1.643            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
