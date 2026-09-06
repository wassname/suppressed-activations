---
condition_id: "017_layer_position_strength_L=12_positions=1_C=4"
axis: "layer_position_strength"
value: "L=12,positions=1,C=4"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.2993147373199463
p4: 0.005383537616580725
p8: 0.29393118619918823
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/017_layer_position_strength_L=12_positions=1_C=4/run.md"
---

# 017_layer_position_strength_L=12_positions=1_C=4

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
  "intervention_layer": 12,
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
  "12": {
    "residual_norm": 7.825362682342529,
    "perturbation_norm": 1.9767448902130127,
    "relative_perturbation_by_position": [
      0.25260743498802185
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
| 1      | '8'      | -1.224  | 0.293931 | -0.003            |
| 2      | 'The'    | -1.224  | 0.293931 | -0.003            |
| 3      | '**'     | -1.224  | 0.293931 | -0.003            |
| 4      | 'Fact'   | -2.724  | 0.065585 | -0.003            |
| 5      | 'Number' | -4.099  | 0.016582 | -0.003            |
| 6      | '###'    | -4.099  | 0.016582 | +0.122            |
| 7      | '4'      | -5.224  | 0.005384 | +0.122            |
| 8      | '1'      | -6.349  | 0.001748 | -0.003            |
| 9      | 'Answer' | -6.849  | 0.001060 | +0.122            |
| 10     | 'Eight'  | -6.849  | 0.001060 | -0.003            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
