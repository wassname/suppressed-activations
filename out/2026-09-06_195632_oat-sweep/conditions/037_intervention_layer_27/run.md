---
condition_id: "037_intervention_layer_27"
axis: "intervention_layer"
value: "27"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.0005022945697419345
p4: 1.0963667591568083e-06
p8: 0.0005011982284486294
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/037_intervention_layer_27/run.md"
---

# 037_intervention_layer_27

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
  "intervention_layer": 27,
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
[' spinning', ' spin', ' måde', ' spins', ' spiders', '在校园', '纺', '-spin']
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
| 1      | 'The'    | -0.099  | 0.906188 | -0.002            |
| 2      | 'Based'  | -2.724  | 0.065644 | -0.002            |
| 3      | 'Most'   | -5.349  | 0.004755 | +0.248            |
| 4      | 'To'     | -5.474  | 0.004196 | +0.248            |
| 5      | 'An'     | -5.849  | 0.002884 | +0.248            |
| 6      | '**'     | -6.099  | 0.002246 | +0.123            |
| 7      | 'Sp'     | -6.099  | 0.002246 | -0.502            |
| 8      | 'Animal' | -6.974  | 0.000936 | +0.123            |
| 9      | 'There'  | -7.099  | 0.000826 | -0.002            |
| 10     | 'First'  | -7.099  | 0.000826 | +0.123            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
