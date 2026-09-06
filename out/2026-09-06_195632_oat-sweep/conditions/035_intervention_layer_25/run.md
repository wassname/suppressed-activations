---
condition_id: "035_intervention_layer_25"
axis: "intervention_layer"
value: "25"
is_default: false
swap_log_odds_shift: 0.2499995231628418
valid_answer_mass: 0.000569696887396276
p4: 1.4086451756156748e-06
p8: 0.0005682882620021701
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/035_intervention_layer_25/run.md"
---

# 035_intervention_layer_25

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
  "intervention_layer": 25,
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
[' spinning', ' spin', ' spins', 'web', '在校园', '纺', '-spin', 'Spin']
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

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | 'The'   | -0.098  | 0.906756 | -0.002            |
| 2      | 'Based' | -2.723  | 0.065685 | -0.002            |
| 3      | 'To'    | -5.473  | 0.004199 | +0.248            |
| 4      | 'Most'  | -5.473  | 0.004199 | +0.123            |
| 5      | 'Sp'    | -5.973  | 0.002547 | -0.377            |
| 6      | 'An'    | -5.973  | 0.002547 | +0.123            |
| 7      | '**'    | -6.098  | 0.002248 | +0.123            |
| 8      | 'Anim'  | -7.098  | 0.000827 | -0.127            |
| 9      | 'First' | -7.098  | 0.000827 | +0.123            |
| 10     | 'There' | -7.098  | 0.000827 | -0.002            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
