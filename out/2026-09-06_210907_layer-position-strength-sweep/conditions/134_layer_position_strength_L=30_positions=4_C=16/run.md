---
condition_id: "134_layer_position_strength_L=30_positions=4_C=16"
axis: "layer_position_strength"
value: "L=30,positions=4,C=16"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.3108896315097809
p4: 0.0043722353875637054
p8: 0.3065173923969269
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/134_layer_position_strength_L=30_positions=4_C=16/run.md"
---

# 134_layer_position_strength_L=30_positions=4_C=16

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
  "intervention_positions": 4,
  "strength": 16.0,
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
[' spinning', 'web', ' spin', ' atingir', ' spins', ' spiders', ' cotton', '-web']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "30": {
    "residual_norm": 89.86124420166016,
    "perturbation_norm": 84.8022689819336,
    "relative_perturbation_by_position": [
      1.1515873670578003,
      1.1525721549987793,
      0.6233463883399963,
      0.8071973323822021
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
| 1      | 'The'    | -1.182  | 0.306517 | +0.039            |
| 2      | '8'      | -1.182  | 0.306517 | +0.039            |
| 3      | '**'     | -1.307  | 0.270501 | -0.086            |
| 4      | 'Fact'   | -2.682  | 0.068393 | +0.039            |
| 5      | 'Number' | -4.057  | 0.017293 | +0.039            |
| 6      | '###'    | -4.307  | 0.013467 | -0.086            |
| 7      | '4'      | -5.432  | 0.004372 | -0.086            |
| 8      | '1'      | -6.432  | 0.001608 | -0.086            |
| 9      | 'Eight'  | -6.932  | 0.000976 | -0.086            |
| 10     | 'Answer' | -7.057  | 0.000861 | -0.086            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
