---
condition_id: "014_layer_position_strength_L=8_positions=4_C=16"
axis: "layer_position_strength"
value: "L=8,positions=4,C=16"
is_default: false
swap_log_odds_shift: 1.624999761581421
valid_answer_mass: 0.020810093730688095
p4: 0.001578615396283567
p8: 0.01923147775232792
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
first_answer: null
source_fact_preserved: false
readout_overlap: 0.0
log: "conditions/014_layer_position_strength_L=8_positions=4_C=16/run.md"
---

# 014_layer_position_strength_L=8_positions=4_C=16

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
['öm', 'elig', 'browse', ' tys', 'Islam', 'тная', '誇る', 'インストール']
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
    "perturbation_norm": 14.315516471862793,
    "relative_perturbation_by_position": [
      1.1820037364959717,
      1.0274521112442017,
      0.9820432066917419,
      0.8225898146629333
    ]
  }
}
```

Generation (32 tokens, verbatim):

```text
**6**

**Explanation:**
The phrase "the animal that ins" (likely a typo for "ins" or part of a common idiom like
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -0.951  | 0.386275 | +0.270            |
| 2      | 'The'    | -1.076  | 0.340886 | +0.145            |
| 3      | '6'      | -2.201  | 0.110670 | +4.770            |
| 4      | '###'    | -3.201  | 0.040713 | +1.020            |
| 5      | 'Number' | -3.826  | 0.021792 | +0.270            |
| 6      | 'Fact'   | -3.826  | 0.021792 | -1.105            |
| 7      | '1'      | -3.951  | 0.019231 | +2.395            |
| 8      | '8'      | -3.951  | 0.019231 | -2.730            |
| 9      | '2'      | -4.451  | 0.011664 | +3.270            |
| 10     | '0'      | -5.451  | 0.004291 | +4.583            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
