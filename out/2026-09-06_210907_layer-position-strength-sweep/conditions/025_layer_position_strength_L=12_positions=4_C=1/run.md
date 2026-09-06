---
condition_id: "025_layer_position_strength_L=12_positions=4_C=1"
axis: "layer_position_strength"
value: "L=12,positions=4,C=1"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.2993873357772827
p4: 0.0047621713019907475
p8: 0.2946251630783081
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/025_layer_position_strength_L=12_positions=4_C=1/run.md"
---

# 025_layer_position_strength_L=12_positions=4_C=1

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
  "intervention_positions": 4,
  "strength": 1.0,
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
['-spin', 'ปั่น', 'Spin', ' Ủy', ' Presents', ' Spin', 'seh', '\tspin']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "12": {
    "residual_norm": 18.060396194458008,
    "perturbation_norm": 1.5440094470977783,
    "relative_perturbation_by_position": [
      0.11353480815887451,
      0.07699049264192581,
      0.07132291048765182,
      0.06446266174316406
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
| 1      | '8'      | -1.222  | 0.294625 | -0.001            |
| 2      | 'The'    | -1.222  | 0.294625 | -0.001            |
| 3      | '**'     | -1.222  | 0.294625 | -0.001            |
| 4      | 'Fact'   | -2.722  | 0.065740 | -0.001            |
| 5      | 'Number' | -4.097  | 0.016622 | -0.001            |
| 6      | '###'    | -4.222  | 0.014669 | -0.001            |
| 7      | '4'      | -5.347  | 0.004762 | -0.001            |
| 8      | '1'      | -6.347  | 0.001752 | -0.001            |
| 9      | 'Answer' | -6.847  | 0.001063 | +0.124            |
| 10     | 'Eight'  | -6.847  | 0.001063 | -0.001            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
