---
condition_id: "039_layer_position_strength_L=16_positions=2_C=16"
axis: "layer_position_strength"
value: "L=16,positions=2,C=16"
is_default: false
swap_log_odds_shift: 0.7500002384185791
valid_answer_mass: 0.3185975253582001
p4: 0.010541113093495369
p8: 0.30805641412734985
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/039_layer_position_strength_L=16_positions=2_C=16/run.md"
---

# 039_layer_position_strength_L=16_positions=2_C=16

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
  "strength": 16.0,
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
    "perturbation_norm": 14.656210899353027,
    "relative_perturbation_by_position": [
      1.0728471279144287,
      0.991378128528595
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class *Arachnida*, which
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | '**'       | -1.052  | 0.349074 | +0.169            |
| 2      | '8'        | -1.177  | 0.308056 | +0.044            |
| 3      | 'The'      | -1.677  | 0.186846 | -0.456            |
| 4      | 'Fact'     | -2.427  | 0.088260 | +0.294            |
| 5      | 'Number'   | -3.677  | 0.025287 | +0.419            |
| 6      | '###'      | -4.302  | 0.013535 | -0.081            |
| 7      | '4'        | -4.552  | 0.010541 | +0.794            |
| 8      | '1'        | -6.052  | 0.002352 | +0.294            |
| 9      | 'Answer'   | -6.302  | 0.001832 | +0.669            |
| 10     | 'Complete' | -6.552  | 0.001427 | +0.669            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
