---
condition_id: "056_donor_position_offset_2"
axis: "donor_position_offset"
value: "2"
is_default: false
swap_log_odds_shift: 0.8750004768371582
valid_answer_mass: 0.0008162941667251289
p4: 3.762768756132573e-06
p8: 0.0008125313906930387
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/056_donor_position_offset_2/run.md"
---

# 056_donor_position_offset_2

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
  "donor_position_offset": 2
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
['-web', 'web', 'mmm', 'Mbps', '(web', 'Web', '闸蟹', '宋']
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

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.115  | 0.891049 | -0.019            |
| 2      | 'Based'  | -2.490  | 0.082880 | +0.231            |
| 3      | 'Sp'     | -5.240  | 0.005298 | +0.356            |
| 4      | '**'     | -5.865  | 0.002836 | +0.356            |
| 5      | 'An'     | -5.990  | 0.002503 | +0.106            |
| 6      | 'To'     | -6.115  | 0.002209 | -0.394            |
| 7      | 'There'  | -6.365  | 0.001720 | +0.731            |
| 8      | 'Spider' | -6.490  | 0.001518 | +1.231            |
| 9      | 'That'   | -6.990  | 0.000921 | +0.606            |
| 10     | '8'      | -7.115  | 0.000813 | +0.356            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
