---
condition_id: "064_layer_position_strength_L=23_positions=1_C=16"
axis: "layer_position_strength"
value: "L=23,positions=1,C=16"
is_default: false
swap_log_odds_shift: 0.25
valid_answer_mass: 0.28596028685569763
p4: 0.005814245902001858
p8: 0.2801460325717926
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.5
log: "conditions/064_layer_position_strength_L=23_positions=1_C=16/run.md"
---

# 064_layer_position_strength_L=23_positions=1_C=16

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
['compan', 'seh', ' Ủy', 'amax', ' Uỷ', ' Hunde', '友達', 'สุนัข']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `064_layer_position_strength_L=23_positions=1_C=16`).

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal most commonly associated with spinning webs is the **spider
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.147  | 0.317447 | +0.074            |
| 2      | '**'     | -1.272  | 0.280146 | -0.051            |
| 3      | '8'      | -1.272  | 0.280146 | -0.051            |
| 4      | 'Fact'   | -2.647  | 0.070832 | +0.074            |
| 5      | 'Number' | -4.022  | 0.017909 | +0.074            |
| 6      | '###'    | -4.272  | 0.013948 | -0.051            |
| 7      | '4'      | -5.147  | 0.005814 | +0.199            |
| 8      | '1'      | -6.397  | 0.001666 | -0.051            |
| 9      | 'Answer' | -6.897  | 0.001010 | +0.074            |
| 10     | 'Eight'  | -7.022  | 0.000892 | -0.176            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
