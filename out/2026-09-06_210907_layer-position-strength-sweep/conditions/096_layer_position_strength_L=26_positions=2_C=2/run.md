---
condition_id: "096_layer_position_strength_L=26_positions=2_C=2"
axis: "layer_position_strength"
value: "L=26,positions=2,C=2"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.285081684589386
p4: 0.004534621257334948
p8: 0.28054705262184143
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/096_layer_position_strength_L=26_positions=2_C=2/run.md"
---

# 096_layer_position_strength_L=26_positions=2_C=2

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
  "intervention_layer": 26,
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
  "26": {
    "residual_norm": 42.33536911010742,
    "perturbation_norm": 4.392184257507324,
    "relative_perturbation_by_position": [
      0.0874437689781189,
      0.12013620138168335
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal most commonly associated with spinning webs is the **spider
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.146  | 0.317901 | +0.075            |
| 2      | '**'     | -1.271  | 0.280547 | -0.050            |
| 3      | '8'      | -1.271  | 0.280547 | -0.050            |
| 4      | 'Fact'   | -2.646  | 0.070933 | +0.075            |
| 5      | 'Number' | -4.021  | 0.017935 | +0.075            |
| 6      | '###'    | -4.271  | 0.013968 | -0.050            |
| 7      | '4'      | -5.396  | 0.004535 | -0.050            |
| 8      | '1'      | -6.396  | 0.001668 | -0.050            |
| 9      | 'Answer' | -6.896  | 0.001012 | +0.075            |
| 10     | 'Eight'  | -6.896  | 0.001012 | -0.050            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
