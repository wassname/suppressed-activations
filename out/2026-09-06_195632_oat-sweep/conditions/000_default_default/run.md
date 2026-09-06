---
condition_id: "000_default_default"
axis: "default"
value: "default"
is_default: true
swap_log_odds_shift: 1.0
valid_answer_mass: 0.0005271325935609639
p4: 2.751698502834188e-06
p8: 0.0005243808845989406
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/000_default_default/run.md"
---

# 000_default_default

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
  "restore_residual_norm": true,
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
['在校园', '丝绸', ' факта', '的战', '迪斯', '_rsp', 'Kate', ' 인프라']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, and all spiders have **8 legs**. This distinguishes them
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | 'The'      | -0.178  | 0.836698 | -0.082            |
| 2      | 'Based'    | -2.303  | 0.099929 | +0.418            |
| 3      | 'There'    | -4.553  | 0.010532 | +2.543            |
| 4      | 'Sp'       | -4.678  | 0.009295 | +0.918            |
| 5      | 'To'       | -4.928  | 0.007239 | +0.793            |
| 6      | '**'       | -5.553  | 0.003875 | +0.668            |
| 7      | 'Spider'   | -5.678  | 0.003419 | +2.043            |
| 8      | 'An'       | -5.803  | 0.003018 | +0.293            |
| 9      | 'That'     | -5.928  | 0.002663 | +1.668            |
| 10     | 'Actually' | -5.928  | 0.002663 | +2.668            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
