---
condition_id: "042_layer_position_strength_L=16_positions=4_C=4"
axis: "layer_position_strength"
value: "L=16,positions=4,C=4"
is_default: false
swap_log_odds_shift: 0.375
valid_answer_mass: 0.29723042249679565
p4: 0.006829573307186365
p8: 0.2904008626937866
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/042_layer_position_strength_L=16_positions=4_C=4/run.md"
---

# 042_layer_position_strength_L=16_positions=4_C=4

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
'<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['Spin', '\tspin', ' Presents', 'ปั่น', '哈密', 'kab', '_spin', 'meldung']
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
    "perturbation_norm": 8.494707107543945,
    "relative_perturbation_by_position": [
      0.392088919878006,
      0.2994905412197113,
      0.4608314037322998,
      0.3878897428512573
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
| 1      | '8'      | -1.236  | 0.290401 | -0.015            |
| 2      | 'The'    | -1.236  | 0.290401 | -0.015            |
| 3      | '**'     | -1.236  | 0.290401 | -0.015            |
| 4      | 'Fact'   | -2.611  | 0.073425 | +0.110            |
| 5      | 'Number' | -3.986  | 0.018565 | +0.110            |
| 6      | '###'    | -4.236  | 0.014458 | -0.015            |
| 7      | '4'      | -4.986  | 0.006830 | +0.360            |
| 8      | '1'      | -6.236  | 0.001957 | +0.110            |
| 9      | '6'      | -6.736  | 0.001187 | +0.235            |
| 10     | 'Answer' | -6.736  | 0.001187 | +0.235            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
