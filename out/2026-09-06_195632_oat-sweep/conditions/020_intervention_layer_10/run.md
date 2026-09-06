---
condition_id: "020_intervention_layer_10"
axis: "intervention_layer"
value: "10"
is_default: false
swap_log_odds_shift: 1.125
valid_answer_mass: 0.00042515157838352025
p4: 2.513100298529025e-06
p8: 0.00042263849172741175
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
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
'<|im_start|>user\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['Spin', '丝绸', '盐酸', 'ปั่น', '\tspin', ' krém', 'seh', '웹']
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
| 1      | 'The'   | -0.144  | 0.865893 | -0.048            |
| 2      | 'Based' | -2.269  | 0.103416 | +0.452            |
| 3      | 'To'    | -5.144  | 0.005834 | +0.577            |
| 4      | 'Most'  | -5.519  | 0.004010 | +0.077            |
| 5      | 'Sp'    | -5.769  | 0.003123 | -0.173            |
| 6      | 'An'    | -6.019  | 0.002432 | +0.077            |
| 7      | '**'    | -6.144  | 0.002146 | +0.077            |
| 8      | 'There' | -6.519  | 0.001475 | +0.577            |
| 9      | 'That'  | -6.769  | 0.001149 | +0.827            |
| 10     | 'This'  | -6.894  | 0.001014 | +0.952            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
