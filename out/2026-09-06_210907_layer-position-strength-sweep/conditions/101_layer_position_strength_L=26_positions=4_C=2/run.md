---
condition_id: "101_layer_position_strength_L=26_positions=4_C=2"
axis: "layer_position_strength"
value: "L=26,positions=4,C=2"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.2973199486732483
p4: 0.005347659811377525
p8: 0.291972279548645
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/101_layer_position_strength_L=26_positions=4_C=2/run.md"
---

# 101_layer_position_strength_L=26_positions=4_C=2

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
  "intervention_positions": 4,
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
[' spinning', ' spin', ' spins', '纺', 'ปั่น', ' Ủy', '-spin', ' spun']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `101_layer_position_strength_L=26_positions=4_C=2`).

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.231  | 0.291972 | -0.010            |
| 2      | 'The'    | -1.231  | 0.291972 | -0.010            |
| 3      | '**'     | -1.231  | 0.291972 | -0.010            |
| 4      | 'Fact'   | -2.606  | 0.073822 | +0.115            |
| 5      | 'Number' | -4.106  | 0.016472 | -0.010            |
| 6      | '###'    | -4.231  | 0.014536 | -0.010            |
| 7      | '4'      | -5.231  | 0.005348 | +0.115            |
| 8      | '1'      | -6.356  | 0.001736 | -0.010            |
| 9      | 'Answer' | -6.856  | 0.001053 | +0.115            |
| 10     | 'Eight'  | -6.856  | 0.001053 | -0.010            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
