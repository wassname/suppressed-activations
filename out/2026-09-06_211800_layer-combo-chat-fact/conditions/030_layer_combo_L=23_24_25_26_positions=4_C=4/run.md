---
condition_id: "030_layer_combo_L=23_24_25_26_positions=4_C=4"
axis: "layer_combo"
value: "L=23+24+25+26,positions=4,C=4"
is_default: false
swap_log_odds_shift: -0.375
valid_answer_mass: 0.0005709613906219602
p4: 7.565366217932024e-07
p8: 0.0005702048656530678
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: null
source_fact_preserved: false
readout_overlap: 0.375
log: "conditions/030_layer_combo_L=23_24_25_26_positions=4_C=4/run.md"
---

# 030_layer_combo_L=23_24_25_26_positions=4_C=4

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
  "intervention_positions": 4,
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
['狗粮', 'สุนัข', ' собаки', ' собак', '狗的', ' dogs', 'dogs', ' собака']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `030_layer_combo_L=23_24_25_26_positions=4_C=4`).

Generation (32 tokens, verbatim):

```text
The animal that is famous for spinning webs is the **spider**.

Spiders are arachnids, which means they have **eight** legs.
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | 'The'     | -0.095  | 0.909814 | +0.002            |
| 2      | 'Based'   | -2.720  | 0.065907 | +0.002            |
| 3      | 'To'      | -5.595  | 0.003718 | +0.127            |
| 4      | 'Most'    | -5.595  | 0.003718 | +0.002            |
| 5      | 'An'      | -5.970  | 0.002555 | +0.127            |
| 6      | '**'      | -6.220  | 0.001990 | +0.002            |
| 7      | 'Sp'      | -6.220  | 0.001990 | -0.623            |
| 8      | '<think>' | -7.095  | 0.000830 | +0.377            |
| 9      | 'First'   | -7.095  | 0.000830 | +0.127            |
| 10     | 'There'   | -7.095  | 0.000830 | +0.002            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
