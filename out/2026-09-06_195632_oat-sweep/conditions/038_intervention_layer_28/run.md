---
condition_id: "038_intervention_layer_28"
axis: "intervention_layer"
value: "28"
is_default: false
swap_log_odds_shift: 0.0625
valid_answer_mass: 0.00044424147927202284
p4: 9.110253245125932e-07
p8: 0.0004433304420672357
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/038_intervention_layer_28/run.md"
---

# 038_intervention_layer_28

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
  "intervention_layer": 28,
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
[' spinning', ' spin', ' spins', ' måde', '在校园', ' spiders', '纺', '-spin']
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
| 1      | 'The'    | -0.096  | 0.908287 | -0.000            |
| 2      | 'Based'  | -2.721  | 0.065796 | -0.000            |
| 3      | 'Most'   | -5.471  | 0.004206 | +0.125            |
| 4      | 'To'     | -5.596  | 0.003712 | +0.125            |
| 5      | 'Sp'     | -5.971  | 0.002551 | -0.375            |
| 6      | 'An'     | -5.971  | 0.002551 | +0.125            |
| 7      | '**'     | -6.221  | 0.001987 | -0.000            |
| 8      | 'Animal' | -6.971  | 0.000939 | +0.125            |
| 9      | 'Anim'   | -6.971  | 0.000939 | -0.000            |
| 10     | 'There'  | -7.096  | 0.000828 | -0.000            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
