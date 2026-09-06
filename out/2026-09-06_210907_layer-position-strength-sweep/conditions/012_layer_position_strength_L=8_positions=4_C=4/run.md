---
condition_id: "012_layer_position_strength_L=8_positions=4_C=4"
axis: "layer_position_strength"
value: "L=8,positions=4,C=4"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.2625010907649994
p4: 0.004175445530563593
p8: 0.25832563638687134
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/012_layer_position_strength_L=8_positions=4_C=4/run.md"
---

# 012_layer_position_strength_L=8_positions=4_C=4

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
['-spin', 'Spin', 'ปั่น', 'spin', ' Spin', 'seh', '\tspin', ' Spinner']
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
    "perturbation_norm": 6.04319429397583,
    "relative_perturbation_by_position": [
      0.5901776552200317,
      0.4171447157859802,
      0.37404605746269226,
      0.2730550467967987
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

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -1.104  | 0.331697 | +0.118            |
| 2      | 'The'    | -1.229  | 0.292721 | -0.007            |
| 3      | '8'      | -1.354  | 0.258326 | -0.132            |
| 4      | 'Fact'   | -2.729  | 0.065315 | -0.007            |
| 5      | 'Number' | -4.104  | 0.016514 | -0.007            |
| 6      | '###'    | -4.229  | 0.014574 | -0.007            |
| 7      | '4'      | -5.479  | 0.004175 | -0.132            |
| 8      | '6'      | -5.729  | 0.003252 | +1.243            |
| 9      | '1'      | -6.229  | 0.001972 | +0.118            |
| 10     | 'Answer' | -6.854  | 0.001056 | +0.118            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
