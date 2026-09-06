---
condition_id: "014_intervention_layer_4"
axis: "intervention_layer"
value: "4"
is_default: false
swap_log_odds_shift: 0.0625004768371582
valid_answer_mass: 0.002020713407546282
p4: 4.143967089476064e-06
p8: 0.0020165694877505302
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/014_intervention_layer_4/run.md"
---

# 014_intervention_layer_4

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
  "intervention_layer": 4,
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
['web', 'Integrated', '-web', 'mmm', '_rsp', ' 인프라', '丝绸', 'มาน']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**. Spiders are arachnids, which means they have **eight** legs.

Therefore, the
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.081  | 0.921864 | +0.015            |
| 2      | 'Based'  | -2.956  | 0.052008 | -0.235            |
| 3      | '**'     | -5.331  | 0.004837 | +0.890            |
| 4      | 'Sp'     | -5.831  | 0.002934 | -0.235            |
| 5      | 'To'     | -5.831  | 0.002934 | -0.110            |
| 6      | 'An'     | -6.081  | 0.002285 | +0.015            |
| 7      | '8'      | -6.206  | 0.002017 | +1.265            |
| 8      | 'That'   | -6.456  | 0.001571 | +1.140            |
| 9      | 'First'  | -6.581  | 0.001386 | +0.640            |
| 10     | 'Spider' | -6.956  | 0.000953 | +0.765            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
