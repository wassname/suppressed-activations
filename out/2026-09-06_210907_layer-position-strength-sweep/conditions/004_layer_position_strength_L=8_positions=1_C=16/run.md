---
condition_id: "004_layer_position_strength_L=8_positions=1_C=16"
axis: "layer_position_strength"
value: "L=8,positions=1,C=16"
is_default: false
swap_log_odds_shift: 0.2499997615814209
valid_answer_mass: 0.29231420159339905
p4: 0.005943433381617069
p8: 0.28637075424194336
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/004_layer_position_strength_L=8_positions=1_C=16/run.md"
---

# 004_layer_position_strength_L=8_positions=1_C=16

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
  "intervention_positions": 1,
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
  "8": {
    "residual_norm": 6.467163562774658,
    "perturbation_norm": 5.319822788238525,
    "relative_perturbation_by_position": [
      0.8225898146629333
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
| 1      | 'The'    | -1.125  | 0.324501 | +0.096            |
| 2      | '**'     | -1.250  | 0.286371 | -0.029            |
| 3      | '8'      | -1.250  | 0.286371 | -0.029            |
| 4      | 'Fact'   | -2.875  | 0.056390 | -0.154            |
| 5      | '###'    | -4.250  | 0.014258 | -0.029            |
| 6      | 'Number' | -4.375  | 0.012582 | -0.279            |
| 7      | '4'      | -5.125  | 0.005943 | +0.221            |
| 8      | '1'      | -6.250  | 0.001930 | +0.096            |
| 9      | '6'      | -6.875  | 0.001033 | +0.096            |
| 10     | 'Answer' | -6.875  | 0.001033 | +0.096            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
