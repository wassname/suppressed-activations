---
condition_id: "055_donor_position_offset_1"
axis: "donor_position_offset"
value: "1"
is_default: false
swap_log_odds_shift: 0.6250004768371582
valid_answer_mass: 0.0011749574914574623
p4: 4.222331881464925e-06
p8: 0.0011707351077347994
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/055_donor_position_offset_1/run.md"
---

# 055_donor_position_offset_1

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
  "donor_position_offset": 1
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
['-web', 'mmm', 'web', 'Mbps', '(web', '闸蟹', '丝绸', '宋']
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
| 1      | 'The'      | -0.125  | 0.882388 | -0.029            |
| 2      | 'Based'    | -2.500  | 0.082075 | +0.221            |
| 3      | 'Sp'       | -5.250  | 0.005247 | +0.346            |
| 4      | '**'       | -5.500  | 0.004086 | +0.721            |
| 5      | 'There'    | -5.625  | 0.003606 | +1.471            |
| 6      | 'To'       | -5.625  | 0.003606 | +0.096            |
| 7      | 'An'       | -5.875  | 0.002808 | +0.221            |
| 8      | 'Spider'   | -6.500  | 0.001503 | +1.221            |
| 9      | 'That'     | -6.625  | 0.001327 | +0.971            |
| 10     | 'Actually' | -6.625  | 0.001327 | +1.971            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
