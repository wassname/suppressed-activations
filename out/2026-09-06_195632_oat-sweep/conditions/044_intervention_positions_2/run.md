---
condition_id: "044_intervention_positions_2"
axis: "intervention_positions"
value: "2"
is_default: false
swap_log_odds_shift: 0.0625
valid_answer_mass: 0.0005030877073295414
p4: 1.0317038459106698e-06
p8: 0.0005020559765398502
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/044_intervention_positions_2/run.md"
---

# 044_intervention_positions_2

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
  "intervention_positions": 2,
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
['-spin', 'Spin', 'seh', 'ปั่น', ' 인프라', '盐酸', 'spin', ' факта']
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
| 1      | 'The'    | -0.097  | 0.907738 | -0.001            |
| 2      | 'Based'  | -2.722  | 0.065756 | -0.001            |
| 3      | 'Most'   | -5.472  | 0.004204 | +0.124            |
| 4      | 'Sp'     | -5.597  | 0.003710 | -0.001            |
| 5      | 'To'     | -5.722  | 0.003274 | -0.001            |
| 6      | 'An'     | -6.097  | 0.002250 | -0.001            |
| 7      | '**'     | -6.222  | 0.001986 | -0.001            |
| 8      | 'Animal' | -6.972  | 0.000938 | +0.124            |
| 9      | 'Anim'   | -6.972  | 0.000938 | -0.001            |
| 10     | 'There'  | -7.097  | 0.000828 | -0.001            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
