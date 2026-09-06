---
condition_id: "118_layer_position_strength_L=28_positions=4_C=8"
axis: "layer_position_strength"
value: "L=28,positions=4,C=8"
is_default: false
swap_log_odds_shift: -0.25
valid_answer_mass: 0.2970171272754669
p4: 0.0036924141459167004
p8: 0.29332470893859863
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/118_layer_position_strength_L=28_positions=4_C=8/run.md"
---

# 118_layer_position_strength_L=28_positions=4_C=8

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
  "intervention_layer": 28,
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
[' spinning', ' spin', ' spins', ' atingir', ' spiders', 'web', '纺', '.Sp']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "28": {
    "residual_norm": 69.62222290039062,
    "perturbation_norm": 49.911434173583984,
    "relative_perturbation_by_position": [
      0.9472841024398804,
      0.9240022301673889,
      0.37156352400779724,
      0.4984666705131531
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
| 1      | '8'      | -1.226  | 0.293325 | -0.005            |
| 2      | 'The'    | -1.226  | 0.293325 | -0.005            |
| 3      | '**'     | -1.226  | 0.293325 | -0.005            |
| 4      | 'Fact'   | -2.601  | 0.074164 | +0.120            |
| 5      | 'Number' | -4.101  | 0.016548 | -0.005            |
| 6      | '###'    | -4.351  | 0.012888 | -0.130            |
| 7      | '4'      | -5.601  | 0.003692 | -0.255            |
| 8      | '1'      | -6.351  | 0.001744 | -0.005            |
| 9      | 'Answer' | -6.976  | 0.000934 | -0.005            |
| 10     | 'Eight'  | -7.101  | 0.000824 | -0.255            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
