---
condition_id: "010_layer_position_strength_L=8_positions=4_C=1"
axis: "layer_position_strength"
value: "L=8,positions=4,C=1"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.28853705525398254
p4: 0.005189687944948673
p8: 0.28334736824035645
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/010_layer_position_strength_L=8_positions=4_C=1/run.md"
---

# 010_layer_position_strength_L=8_positions=4_C=1

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
['-spin', 'ปั่น', 'Spin', ' Spin', ' Ủy', ' Presents', 'seh', 'spin']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

```json
{
  "8": {
    "residual_norm": 14.111225128173828,
    "perturbation_norm": 1.6203964948654175,
    "relative_perturbation_by_position": [
      0.163410484790802,
      0.11003244668245316,
      0.09736091643571854,
      0.06997082382440567
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal most famous for spinning webs is the **spider**.
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.136  | 0.321075 | +0.085            |
| 2      | '**'     | -1.261  | 0.283347 | -0.040            |
| 3      | '8'      | -1.261  | 0.283347 | -0.040            |
| 4      | 'Fact'   | -2.761  | 0.063223 | -0.040            |
| 5      | 'Number' | -4.136  | 0.015985 | -0.040            |
| 6      | '###'    | -4.261  | 0.014107 | -0.040            |
| 7      | '4'      | -5.261  | 0.005190 | +0.085            |
| 8      | '1'      | -6.386  | 0.001685 | -0.040            |
| 9      | '6'      | -6.886  | 0.001022 | +0.085            |
| 10     | 'Answer' | -6.886  | 0.001022 | +0.085            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
