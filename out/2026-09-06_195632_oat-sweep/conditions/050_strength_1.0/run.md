---
condition_id: "050_strength_1.0"
axis: "strength"
value: "1.0"
is_default: false
swap_log_odds_shift: -0.1250004768371582
valid_answer_mass: 0.0006587073439732194
p4: 1.1202777159269317e-06
p8: 0.0006575870793312788
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/050_strength_1.0/run.md"
---

# 050_strength_1.0

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
  "strength": 1.0,
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
['Spin', 'web', '-spin', 'spin', '\tspin', '_spin', ' Spin', 'edata']
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

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | 'The'     | -0.077  | 0.925951 | +0.019            |
| 2      | 'Based'   | -2.952  | 0.052239 | -0.231            |
| 3      | 'Sp'      | -5.452  | 0.004288 | +0.144            |
| 4      | 'To'      | -5.952  | 0.002601 | -0.231            |
| 5      | 'An'      | -6.077  | 0.002295 | +0.019            |
| 6      | '**'      | -6.327  | 0.001788 | -0.106            |
| 7      | 'Most'    | -6.452  | 0.001577 | -0.856            |
| 8      | '<think>' | -7.202  | 0.000745 | +0.269            |
| 9      | 'Animal'  | -7.202  | 0.000745 | -0.106            |
| 10     | '8'       | -7.327  | 0.000658 | +0.144            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
