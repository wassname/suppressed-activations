---
condition_id: "036_intervention_layer_26"
axis: "intervention_layer"
value: "26"
is_default: false
swap_log_odds_shift: 0.3125004768371582
valid_answer_mass: 0.0004484957898966968
p4: 1.1802952712969272e-06
p8: 0.00044731548405252397
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/036_intervention_layer_26/run.md"
---

# 036_intervention_layer_26

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
  "intervention_layer": 26,
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
[' spinning', ' spin', ' spins', '在校园', ' måde', '纺', '-spin', 'Spin']
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
| 1      | 'The'    | -0.087  | 0.916451 | +0.009            |
| 2      | 'Based'  | -2.837  | 0.058587 | -0.116            |
| 3      | 'To'     | -5.587  | 0.003745 | +0.134            |
| 4      | 'Most'   | -5.587  | 0.003745 | +0.009            |
| 5      | 'An'     | -5.962  | 0.002574 | +0.134            |
| 6      | 'Sp'     | -6.087  | 0.002272 | -0.491            |
| 7      | '**'     | -6.212  | 0.002005 | +0.009            |
| 8      | 'Animal' | -7.087  | 0.000836 | +0.009            |
| 9      | 'There'  | -7.212  | 0.000737 | -0.116            |
| 10     | 'First'  | -7.212  | 0.000737 | +0.009            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
