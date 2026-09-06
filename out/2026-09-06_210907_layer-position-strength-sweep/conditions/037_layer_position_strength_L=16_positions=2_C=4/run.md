---
condition_id: "037_layer_position_strength_L=16_positions=2_C=4"
axis: "layer_position_strength"
value: "L=16,positions=2,C=4"
is_default: false
swap_log_odds_shift: 0.2500002384185791
valid_answer_mass: 0.3073681890964508
p4: 0.006249519530683756
p8: 0.3011186718940735
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/037_layer_position_strength_L=16_positions=2_C=4/run.md"
---

# 037_layer_position_strength_L=16_positions=2_C=4

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
  "intervention_positions": 2,
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
['ปั่น', '-spin', ' Ủy', 'Spin', ' Presents', 'seh', ' Spin', ' laba']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "16": {
    "residual_norm": 14.143196105957031,
    "perturbation_norm": 6.066242218017578,
    "relative_perturbation_by_position": [
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
| 1      | '8'      | -1.200  | 0.301119 | +0.021            |
| 2      | '**'     | -1.200  | 0.301119 | +0.021            |
| 3      | 'The'    | -1.325  | 0.265736 | -0.104            |
| 4      | 'Fact'   | -2.575  | 0.076135 | +0.146            |
| 5      | 'Number' | -3.950  | 0.019250 | +0.146            |
| 6      | '###'    | -4.200  | 0.014992 | +0.021            |
| 7      | '4'      | -5.075  | 0.006250 | +0.271            |
| 8      | '1'      | -6.325  | 0.001791 | +0.021            |
| 9      | 'Eight'  | -6.575  | 0.001394 | +0.271            |
| 10     | 'Answer' | -6.700  | 0.001231 | +0.271            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
