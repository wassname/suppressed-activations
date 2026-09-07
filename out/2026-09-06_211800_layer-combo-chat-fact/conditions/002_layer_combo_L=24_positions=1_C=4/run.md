---
condition_id: "002_layer_combo_L=24_positions=1_C=4"
axis: "layer_combo"
value: "L=24,positions=1,C=4"
is_default: false
swap_log_odds_shift: -0.0625
valid_answer_mass: 0.0005701297777704895
p4: 1.0320551382392296e-06
p8: 0.0005690976977348328
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.5
log: "conditions/002_layer_combo_L=24_positions=1_C=4/run.md"
---

# 002_layer_combo_L=24_positions=1_C=4

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
    24
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
['狗粮', 'สุนัข', 'seh', 'DOG', ' собаки', ' собак', ' perros', ' doga']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `002_layer_combo_L=24_positions=1_C=4`).

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.096  | 0.908048 | -0.000            |
| 2      | 'Based'  | -2.721  | 0.065779 | -0.000            |
| 3      | 'Sp'     | -5.596  | 0.003711 | -0.000            |
| 4      | 'Most'   | -5.596  | 0.003711 | -0.000            |
| 5      | 'To'     | -5.721  | 0.003275 | -0.000            |
| 6      | 'An'     | -6.096  | 0.002251 | -0.000            |
| 7      | '**'     | -6.221  | 0.001986 | -0.000            |
| 8      | 'Animal' | -6.971  | 0.000938 | +0.125            |
| 9      | 'Anim'   | -6.971  | 0.000938 | -0.000            |
| 10     | 'There'  | -7.096  | 0.000828 | -0.000            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
