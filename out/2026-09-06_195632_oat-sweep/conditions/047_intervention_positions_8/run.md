---
condition_id: "047_intervention_positions_8"
axis: "intervention_positions"
value: "8"
is_default: false
swap_log_odds_shift: 1.1875004768371582
valid_answer_mass: 0.0004277100379113108
p4: 2.690255769266514e-06
p8: 0.00042501979623921216
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/047_intervention_positions_8/run.md"
---

# 047_intervention_positions_8

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
  "intervention_positions": 8,
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
[' факта', '在校园', '-web', '_rsp', 'web', ' 인프라', '丝绸', '闸蟹']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, and all spiders have **8 legs**.

Therefore, the
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | 'The'   | -0.201  | 0.818015 | -0.105            |
| 2      | 'Based' | -2.076  | 0.125447 | +0.645            |
| 3      | 'There' | -4.326  | 0.013222 | +2.770            |
| 4      | 'To'    | -4.701  | 0.009087 | +1.020            |
| 5      | 'First' | -5.201  | 0.005512 | +2.020            |
| 6      | 'Sp'    | -5.326  | 0.004864 | +0.270            |
| 7      | 'It'    | -5.826  | 0.002950 | +3.520            |
| 8      | 'An'    | -5.951  | 0.002604 | +0.145            |
| 9      | '**'    | -6.076  | 0.002298 | +0.145            |
| 10     | 'That'  | -6.451  | 0.001579 | +1.145            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
