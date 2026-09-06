---
condition_id: "063_layer_position_strength_L=23_positions=1_C=8"
axis: "layer_position_strength"
value: "L=23,positions=1,C=8"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.29616326093673706
p4: 0.0047108884900808334
p8: 0.2914523780345917
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.5
log: "conditions/063_layer_position_strength_L=23_positions=1_C=8/run.md"
---

# 063_layer_position_strength_L=23_positions=1_C=8

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
  "intervention_layer": 23,
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
['compan', 'seh', 'amax', ' Ủy', ' Uỷ', 'สุนัข', ' Hunde', '友達']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "23": {
    "residual_norm": 22.3740177154541,
    "perturbation_norm": 11.739314079284668,
    "relative_perturbation_by_position": [
      0.5246851444244385
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
| 1      | '8'      | -1.233  | 0.291452 | -0.011            |
| 2      | 'The'    | -1.233  | 0.291452 | -0.011            |
| 3      | '**'     | -1.233  | 0.291452 | -0.011            |
| 4      | 'Fact'   | -2.608  | 0.073691 | +0.114            |
| 5      | 'Number' | -3.983  | 0.018632 | +0.114            |
| 6      | '###'    | -4.233  | 0.014511 | -0.011            |
| 7      | '4'      | -5.358  | 0.004711 | -0.011            |
| 8      | '1'      | -6.358  | 0.001733 | -0.011            |
| 9      | 'Answer' | -6.858  | 0.001051 | +0.114            |
| 10     | 'Eight'  | -6.858  | 0.001051 | -0.011            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
