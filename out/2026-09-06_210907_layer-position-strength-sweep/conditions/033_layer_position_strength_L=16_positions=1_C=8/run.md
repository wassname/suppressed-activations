---
condition_id: "033_layer_position_strength_L=16_positions=1_C=8"
axis: "layer_position_strength"
value: "L=16,positions=1,C=8"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.30670037865638733
p4: 0.005516375880688429
p8: 0.3011839985847473
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/033_layer_position_strength_L=16_positions=1_C=8/run.md"
---

# 033_layer_position_strength_L=16_positions=1_C=8

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
    "residual_norm": 9.578800201416016,
    "perturbation_norm": 6.507462501525879,
    "relative_perturbation_by_position": [
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
| 1      | '8'      | -1.200  | 0.301184 | +0.021            |
| 2      | '**'     | -1.200  | 0.301184 | +0.021            |
| 3      | 'The'    | -1.325  | 0.265794 | -0.104            |
| 4      | 'Fact'   | -2.575  | 0.076151 | +0.146            |
| 5      | 'Number' | -3.950  | 0.019254 | +0.146            |
| 6      | '###'    | -4.200  | 0.014995 | +0.021            |
| 7      | '4'      | -5.200  | 0.005516 | +0.146            |
| 8      | '1'      | -6.325  | 0.001791 | +0.021            |
| 9      | 'Answer' | -6.450  | 0.001580 | +0.521            |
| 10     | 'Eight'  | -6.575  | 0.001395 | +0.271            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
