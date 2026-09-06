---
condition_id: "043_layer_position_strength_L=16_positions=4_C=8"
axis: "layer_position_strength"
value: "L=16,positions=4,C=8"
is_default: false
swap_log_odds_shift: 0.5
valid_answer_mass: 0.29207319021224976
p4: 0.007581448648124933
p8: 0.28449174761772156
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/043_layer_position_strength_L=16_positions=4_C=8/run.md"
---

# 043_layer_position_strength_L=16_positions=4_C=8

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
  "intervention_layer": 16,
  "intervention_positions": 4,
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
'<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['\tspin', ' fär', 'สปิน', 'Longrightarrow', ' ಭ', 'ambung', ' Bốn', 'meldung']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "16": {
    "residual_norm": 22.285104751586914,
    "perturbation_norm": 14.860926628112793,
    "relative_perturbation_by_position": [
      0.6879270076751709,
      0.5511814951896667,
      0.7761197686195374,
      0.6793609261512756
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.257  | 0.284492 | -0.036            |
| 2      | '**'     | -1.257  | 0.284492 | -0.036            |
| 3      | 'The'    | -1.257  | 0.284492 | -0.036            |
| 4      | 'Fact'   | -2.507  | 0.081508 | +0.214            |
| 5      | 'Number' | -3.882  | 0.020609 | +0.214            |
| 6      | '###'    | -4.132  | 0.016050 | +0.089            |
| 7      | '4'      | -4.882  | 0.007581 | +0.464            |
| 8      | '6'      | -5.632  | 0.003581 | +1.339            |
| 9      | '1'      | -5.757  | 0.003160 | +0.589            |
| 10     | 'Eight'  | -6.632  | 0.001317 | +0.214            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
