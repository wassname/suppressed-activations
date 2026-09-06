---
condition_id: "028_intervention_layer_18"
axis: "intervention_layer"
value: "18"
is_default: false
swap_log_odds_shift: 0.4375
valid_answer_mass: 0.0003102905466221273
p4: 9.249862387150642e-07
p8: 0.0003093655686825514
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/028_intervention_layer_18/run.md"
---

# 028_intervention_layer_18

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
  "intervention_layer": 18,
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
[' 인프라', '\tspin', 'Integrated', 'seh', ' Presents', ' факта', '盐酸', 'edata']
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

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.081  | 0.922206 | +0.015            |
| 2      | 'Based'  | -3.081  | 0.045914 | -0.360            |
| 3      | 'Sp'     | -5.331  | 0.004839 | +0.265            |
| 4      | 'Most'   | -5.331  | 0.004839 | +0.265            |
| 5      | 'An'     | -5.581  | 0.003769 | +0.515            |
| 6      | 'To'     | -5.581  | 0.003769 | +0.140            |
| 7      | '**'     | -6.206  | 0.002017 | +0.015            |
| 8      | 'Anim'   | -6.456  | 0.001571 | +0.515            |
| 9      | 'First'  | -6.956  | 0.000953 | +0.265            |
| 10     | 'Animal' | -6.956  | 0.000953 | +0.140            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
