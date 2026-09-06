---
condition_id: "057_donor_position_offset_3"
axis: "donor_position_offset"
value: "3"
is_default: false
swap_log_odds_shift: 1.3750004768371582
valid_answer_mass: 0.0004290783836040646
p4: 3.2512321013200562e-06
p8: 0.0004258271655999124
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/057_donor_position_offset_3/run.md"
---

# 057_donor_position_offset_3

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
  "donor_position_offset": 3
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
['mmm', 'Mbps', '在校园', '闸蟹', '-web', ' 인프라', ' отве', 'ocup']
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
| 1      | 'The'      | -0.261  | 0.769914 | -0.165            |
| 2      | 'Based'    | -1.761  | 0.171791 | +0.960            |
| 3      | 'Sp'       | -4.511  | 0.010982 | +1.085            |
| 4      | 'To'       | -4.636  | 0.009692 | +1.085            |
| 5      | 'There'    | -5.261  | 0.005188 | +1.835            |
| 6      | 'An'       | -5.511  | 0.004040 | +0.585            |
| 7      | 'Anim'     | -5.511  | 0.004040 | +1.460            |
| 8      | '**'       | -5.511  | 0.004040 | +0.710            |
| 9      | 'It'       | -6.386  | 0.001684 | +2.960            |
| 10     | 'Actually' | -6.386  | 0.001684 | +2.210            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
