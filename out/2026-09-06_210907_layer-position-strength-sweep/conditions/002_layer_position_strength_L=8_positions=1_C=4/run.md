---
condition_id: "002_layer_position_strength_L=8_positions=1_C=4"
axis: "layer_position_strength"
value: "L=8,positions=1,C=4"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.2880863845348358
p4: 0.004582415334880352
p8: 0.2835039794445038
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/002_layer_position_strength_L=8_positions=1_C=4/run.md"
---

# 002_layer_position_strength_L=8_positions=1_C=4

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
['ปั่น', '-spin', ' Ủy', 'Spin', ' Presents', 'seh', ' Spin', ' laba']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `002_layer_position_strength_L=8_positions=1_C=4`).

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal most commonly associated with spinning webs is the **spider
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.136  | 0.321252 | +0.086            |
| 2      | '**'     | -1.261  | 0.283504 | -0.039            |
| 3      | '8'      | -1.261  | 0.283504 | -0.039            |
| 4      | 'Fact'   | -2.761  | 0.063258 | -0.039            |
| 5      | 'Number' | -4.136  | 0.015994 | -0.039            |
| 6      | '###'    | -4.261  | 0.014115 | -0.039            |
| 7      | '4'      | -5.386  | 0.004582 | -0.039            |
| 8      | '1'      | -6.386  | 0.001686 | -0.039            |
| 9      | 'Answer' | -6.886  | 0.001022 | +0.086            |
| 10     | 'Eight'  | -6.886  | 0.001022 | -0.039            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
