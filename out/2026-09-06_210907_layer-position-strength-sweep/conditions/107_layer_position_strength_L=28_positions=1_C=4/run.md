---
condition_id: "107_layer_position_strength_L=28_positions=1_C=4"
axis: "layer_position_strength"
value: "L=28,positions=1,C=4"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.31076252460479736
p4: 0.004370447248220444
p8: 0.3063920736312866
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/107_layer_position_strength_L=28_positions=1_C=4/run.md"
---

# 107_layer_position_strength_L=28_positions=1_C=4

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
  "intervention_layer": 28,
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

[Full diagnostic data](../../result.json) (`rows` → `107_layer_position_strength_L=28_positions=1_C=4`).

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.183  | 0.306392 | +0.039            |
| 2      | '8'      | -1.183  | 0.306392 | +0.039            |
| 3      | '**'     | -1.308  | 0.270390 | -0.086            |
| 4      | 'Fact'   | -2.683  | 0.068365 | +0.039            |
| 5      | 'Number' | -4.058  | 0.017285 | +0.039            |
| 6      | '###'    | -4.308  | 0.013462 | -0.086            |
| 7      | '4'      | -5.433  | 0.004370 | -0.086            |
| 8      | '1'      | -6.308  | 0.001822 | +0.039            |
| 9      | 'Answer' | -6.933  | 0.000975 | +0.039            |
| 10     | 'Eight'  | -6.933  | 0.000975 | -0.086            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
