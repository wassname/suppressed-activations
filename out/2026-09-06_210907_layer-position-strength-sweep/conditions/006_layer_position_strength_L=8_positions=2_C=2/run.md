---
condition_id: "006_layer_position_strength_L=8_positions=2_C=2"
axis: "layer_position_strength"
value: "L=8,positions=2,C=2"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.29987940192222595
p4: 0.005393694620579481
p8: 0.2944857180118561
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/006_layer_position_strength_L=8_positions=2_C=2/run.md"
---

# 006_layer_position_strength_L=8_positions=2_C=2

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
  "intervention_layer": 8,
  "intervention_positions": 2,
  "strength": 2.0,
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
  "8": {
    "residual_norm": 9.613831520080566,
    "perturbation_norm": 1.64412522315979,
    "relative_perturbation_by_position": [
      0.19335994124412537,
      0.13927224278450012
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
| 1      | '8'      | -1.223  | 0.294486 | -0.001            |
| 2      | 'The'    | -1.223  | 0.294486 | -0.001            |
| 3      | '**'     | -1.223  | 0.294486 | -0.001            |
| 4      | 'Fact'   | -2.723  | 0.065709 | -0.001            |
| 5      | 'Number' | -4.098  | 0.016614 | -0.001            |
| 6      | '###'    | -4.223  | 0.014662 | -0.001            |
| 7      | '4'      | -5.223  | 0.005394 | +0.124            |
| 8      | '1'      | -6.348  | 0.001751 | -0.001            |
| 9      | 'Answer' | -6.848  | 0.001062 | +0.124            |
| 10     | 'Eight'  | -6.848  | 0.001062 | -0.001            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
