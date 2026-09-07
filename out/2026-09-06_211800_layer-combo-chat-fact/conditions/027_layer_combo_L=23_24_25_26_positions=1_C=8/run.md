---
condition_id: "027_layer_combo_L=23_24_25_26_positions=1_C=8"
axis: "layer_combo"
value: "L=23+24+25+26,positions=1,C=8"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.0006497607100754976
p4: 1.1050626653741347e-06
p8: 0.0006486556376330554
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.375
log: "conditions/027_layer_combo_L=23_24_25_26_positions=1_C=8/run.md"
---

# 027_layer_combo_L=23_24_25_26_positions=1_C=8

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
  "intervention_layer": [
    23,
    24,
    25,
    26
  ],
  "intervention_positions": 1,
  "strength": 8.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1
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
['狗粮', 'สุนัข', ' dogs', ' собаки', '狗的', ' собак', ' Dogs', '狗狗']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `027_layer_combo_L=23_24_25_26_positions=1_C=8`).

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | 'The'   | -0.091  | 0.913375 | +0.005            |
| 2      | 'Based' | -2.841  | 0.058390 | -0.120            |
| 3      | 'Most'  | -5.466  | 0.004230 | +0.130            |
| 4      | 'Sp'    | -5.591  | 0.003733 | +0.005            |
| 5      | 'To'    | -5.591  | 0.003733 | +0.130            |
| 6      | 'An'    | -5.966  | 0.002565 | +0.130            |
| 7      | '**'    | -6.216  | 0.001998 | +0.005            |
| 8      | 'There' | -6.966  | 0.000944 | +0.130            |
| 9      | 'First' | -7.091  | 0.000833 | +0.130            |
| 10     | 'Anim'  | -7.091  | 0.000833 | -0.120            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
