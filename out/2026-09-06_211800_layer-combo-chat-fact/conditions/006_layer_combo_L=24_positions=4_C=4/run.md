---
condition_id: "006_layer_combo_L=24_positions=4_C=4"
axis: "layer_combo"
value: "L=24,positions=4,C=4"
is_default: false
swap_log_odds_shift: 4.76837158203125e-07
valid_answer_mass: 0.0005752827855758369
p4: 1.1084179050158127e-06
p8: 0.0005741743952967227
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.5
log: "conditions/006_layer_combo_L=24_positions=4_C=4/run.md"
---

# 006_layer_combo_L=24_positions=4_C=4

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
['狗粮', 'สุนัข', 'DOG', 'seh', ' собак', 'ัข', ' собаки', ' cão']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `006_layer_combo_L=24_positions=4_C=4`).

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | 'The'   | -0.088  | 0.916148 | +0.009            |
| 2      | 'Based' | -2.838  | 0.058567 | -0.116            |
| 3      | 'Most'  | -5.588  | 0.003744 | +0.009            |
| 4      | 'To'    | -5.713  | 0.003304 | +0.009            |
| 5      | 'Sp'    | -5.838  | 0.002916 | -0.241            |
| 6      | 'An'    | -5.963  | 0.002573 | +0.134            |
| 7      | '**'    | -6.088  | 0.002271 | +0.134            |
| 8      | 'Anim'  | -7.213  | 0.000737 | -0.241            |
| 9      | 'First' | -7.213  | 0.000737 | +0.009            |
| 10     | 'There' | -7.213  | 0.000737 | -0.116            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
