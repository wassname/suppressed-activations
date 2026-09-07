---
condition_id: "026_layer_combo_L=23_24_25_26_positions=1_C=4"
axis: "layer_combo"
value: "L=23+24+25+26,positions=1,C=4"
is_default: false
swap_log_odds_shift: -0.0625004768371582
valid_answer_mass: 0.0006451781373471022
p4: 1.1679080671456177e-06
p8: 0.0006440102006308734
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.375
log: "conditions/026_layer_combo_L=23_24_25_26_positions=1_C=4/run.md"
---

# 026_layer_combo_L=23_24_25_26_positions=1_C=4

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
  "strength": 4.0,
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
['狗粮', 'สุนัข', ' собаки', ' dogs', '狗的', ' собак', ' canine', ' Dogs']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `026_layer_combo_L=23_24_25_26_positions=1_C=4`).

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.098  | 0.906834 | -0.002            |
| 2      | 'Based'  | -2.723  | 0.065691 | -0.002            |
| 3      | 'Most'   | -5.473  | 0.004199 | +0.123            |
| 4      | 'Sp'     | -5.598  | 0.003706 | -0.002            |
| 5      | 'To'     | -5.598  | 0.003706 | +0.123            |
| 6      | 'An'     | -6.098  | 0.002248 | -0.002            |
| 7      | '**'     | -6.223  | 0.001984 | -0.002            |
| 8      | 'Animal' | -7.098  | 0.000827 | -0.002            |
| 9      | 'Anim'   | -7.098  | 0.000827 | -0.127            |
| 10     | 'There'  | -7.098  | 0.000827 | -0.002            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
