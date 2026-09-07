---
condition_id: "020_persistent_generation_L=24_26_positions=4_C=0.25"
axis: "persistent_generation"
value: "L=24+26,positions=4,C=0.25"
is_default: false
swap_log_odds_shift: -4.76837158203125e-07
valid_answer_mass: 0.0005702096386812627
p4: 1.0986422012138064e-06
p8: 0.000569110969081521
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/020_persistent_generation_L=24_26_positions=4_C=0.25/run.md"
---

# 020_persistent_generation_L=24_26_positions=4_C=0.25

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
    24,
    26
  ],
  "intervention_positions": 4,
  "strength": 0.25,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
  "lexical_divisor": 1,
  "continue_generation": true
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
['seh', 'Integrated', ' факта', '在校园', '웹', ' Ủy', '盐酸', '丝绸']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `020_persistent_generation_L=24_26_positions=4_C=0.25`).

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.096  | 0.908069 | -0.000            |
| 2      | 'Based'  | -2.721  | 0.065780 | -0.000            |
| 3      | 'Sp'     | -5.596  | 0.003711 | -0.000            |
| 4      | 'Most'   | -5.596  | 0.003711 | -0.000            |
| 5      | 'To'     | -5.721  | 0.003275 | -0.000            |
| 6      | 'An'     | -5.971  | 0.002551 | +0.125            |
| 7      | '**'     | -6.221  | 0.001986 | -0.000            |
| 8      | 'Anim'   | -6.971  | 0.000938 | -0.000            |
| 9      | 'There'  | -7.096  | 0.000828 | -0.000            |
| 10     | 'Animal' | -7.096  | 0.000828 | -0.000            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
