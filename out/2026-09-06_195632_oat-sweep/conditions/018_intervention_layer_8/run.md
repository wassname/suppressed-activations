---
condition_id: "018_intervention_layer_8"
axis: "intervention_layer"
value: "8"
is_default: false
swap_log_odds_shift: 0.6249995231628418
valid_answer_mass: 0.0013428803067654371
p4: 4.825776159123052e-06
p8: 0.0013380545424297452
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/018_intervention_layer_8/run.md"
---

# 018_intervention_layer_8

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
  "intervention_layer": 8,
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
['Spin', '盐酸', ' 인프라', 'edata', '丝绸', 'ปั่น', 'seh', '在校园']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | 'The'   | -0.117  | 0.889996 | -0.020            |
| 2      | 'Based' | -2.492  | 0.082783 | +0.230            |
| 3      | 'To'    | -5.617  | 0.003637 | +0.105            |
| 4      | 'An'    | -5.742  | 0.003210 | +0.355            |
| 5      | 'Sp'    | -5.992  | 0.002500 | -0.395            |
| 6      | 'Most'  | -6.242  | 0.001947 | -0.645            |
| 7      | '**'    | -6.367  | 0.001718 | -0.145            |
| 8      | '8'     | -6.617  | 0.001338 | +0.855            |
| 9      | 'First' | -6.617  | 0.001338 | +0.605            |
| 10     | 'There' | -6.742  | 0.001181 | +0.355            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
