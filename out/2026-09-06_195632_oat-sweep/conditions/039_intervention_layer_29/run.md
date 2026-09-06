---
condition_id: "039_intervention_layer_29"
axis: "intervention_layer"
value: "29"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.0005036838119849563
p4: 9.704650665298686e-07
p8: 0.0005027133738622069
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/039_intervention_layer_29/run.md"
---

# 039_intervention_layer_29

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
  "intervention_layer": 29,
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
[' spinning', ' spin', ' spins', '在校园', '纺', '-spin', 'Spin', ' måde']
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
| 1      | 'The'    | -0.095  | 0.908927 | +0.001            |
| 2      | 'Based'  | -2.720  | 0.065842 | +0.001            |
| 3      | 'Most'   | -5.470  | 0.004209 | +0.126            |
| 4      | 'To'     | -5.720  | 0.003278 | +0.001            |
| 5      | 'An'     | -5.970  | 0.002553 | +0.126            |
| 6      | 'Sp'     | -6.095  | 0.002253 | -0.499            |
| 7      | '**'     | -6.220  | 0.001988 | +0.001            |
| 8      | 'Animal' | -6.970  | 0.000939 | +0.126            |
| 9      | 'Anim'   | -6.970  | 0.000939 | +0.001            |
| 10     | 'There'  | -7.095  | 0.000829 | +0.001            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
