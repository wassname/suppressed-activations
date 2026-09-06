---
condition_id: "048_strength_0.25"
axis: "strength"
value: "0.25"
is_default: false
swap_log_odds_shift: 4.76837158203125e-07
valid_answer_mass: 0.0006469929357990623
p4: 1.2465843610698357e-06
p8: 0.0006457463605329394
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/048_strength_0.25/run.md"
---

# 048_strength_0.25

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
  "strength": 0.25,
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
['Spin', '-spin', 'spin', 'seh', '盐酸', 'ปั่น', '\tspin', '_spin']
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
| 1      | 'The'    | -0.095  | 0.909279 | +0.001            |
| 2      | 'Based'  | -2.720  | 0.065868 | +0.001            |
| 3      | 'Sp'     | -5.595  | 0.003716 | +0.001            |
| 4      | 'Most'   | -5.720  | 0.003279 | -0.124            |
| 5      | 'To'     | -5.845  | 0.002894 | -0.124            |
| 6      | 'An'     | -6.095  | 0.002254 | +0.001            |
| 7      | '**'     | -6.220  | 0.001989 | +0.001            |
| 8      | 'Animal' | -7.095  | 0.000829 | +0.001            |
| 9      | 'Anim'   | -7.095  | 0.000829 | -0.124            |
| 10     | 'There'  | -7.220  | 0.000732 | -0.124            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
