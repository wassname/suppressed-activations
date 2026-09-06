---
condition_id: "051_strength_2.0"
axis: "strength"
value: "2.0"
is_default: false
swap_log_odds_shift: 0.3125004768371582
valid_answer_mass: 0.0004519991634879261
p4: 1.1895150464624749e-06
p8: 0.00045080966083332896
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/051_strength_2.0/run.md"
---

# 051_strength_2.0

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
  "strength": 2.0,
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
['web', 'Spin', '-web', '-spin', '\tspin', '_spin', 'mmm', 'edata']
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
| 1      | 'The'     | -0.079  | 0.923610 | +0.017            |
| 2      | 'Based'   | -2.829  | 0.059044 | -0.108            |
| 3      | 'To'      | -5.704  | 0.003331 | +0.017            |
| 4      | 'Sp'      | -6.204  | 0.002020 | -0.608            |
| 5      | '**'      | -6.204  | 0.002020 | +0.017            |
| 6      | 'An'      | -6.329  | 0.001783 | -0.233            |
| 7      | 'First'   | -7.329  | 0.000656 | -0.108            |
| 8      | '<think>' | -7.329  | 0.000656 | +0.142            |
| 9      | 'Animal'  | -7.329  | 0.000656 | -0.233            |
| 10     | 'That'    | -7.454  | 0.000579 | +0.142            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
