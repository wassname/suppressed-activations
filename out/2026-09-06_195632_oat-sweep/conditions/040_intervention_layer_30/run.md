---
condition_id: "040_intervention_layer_30"
axis: "intervention_layer"
value: "30"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.0005077813984826207
p4: 9.783600489754463e-07
p8: 0.0005068030441179872
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/040_intervention_layer_30/run.md"
---

# 040_intervention_layer_30

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
  "intervention_layer": 30,
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
[' spinning', ' spin', ' spins', ' måde', '在校园', '纺', '-spin', 'Spin']
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
| 1      | 'The'    | -0.087  | 0.916321 | +0.009            |
| 2      | 'Based'  | -2.837  | 0.058578 | -0.116            |
| 3      | 'Most'   | -5.587  | 0.003745 | +0.009            |
| 4      | 'To'     | -5.712  | 0.003305 | +0.009            |
| 5      | 'Sp'     | -5.962  | 0.002574 | -0.366            |
| 6      | 'An'     | -5.962  | 0.002574 | +0.134            |
| 7      | '**'     | -6.212  | 0.002004 | +0.009            |
| 8      | 'Animal' | -6.962  | 0.000947 | +0.134            |
| 9      | 'Anim'   | -6.962  | 0.000947 | +0.009            |
| 10     | 'There'  | -7.087  | 0.000836 | +0.009            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
