---
condition_id: "074_layer_position_strength_L=23_positions=4_C=16"
axis: "layer_position_strength"
value: "L=23,positions=4,C=16"
is_default: false
swap_log_odds_shift: -1.125
valid_answer_mass: 0.30429399013519287
p4: 0.0015884527238085866
p8: 0.3027055263519287
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.625
log: "conditions/074_layer_position_strength_L=23_positions=4_C=16/run.md"
---

# 074_layer_position_strength_L=23_positions=4_C=16

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
['compan', 'seh', ' Ủy', '友達', ' собаки', ' собака', 'amax', ' Hunde']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `074_layer_position_strength_L=23_positions=4_C=16`).

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.195  | 0.302706 | +0.027            |
| 2      | '8'      | -1.195  | 0.302706 | +0.027            |
| 3      | '**'     | -1.320  | 0.267137 | -0.098            |
| 4      | 'Fact'   | -2.570  | 0.076536 | +0.152            |
| 5      | 'Number' | -3.945  | 0.019351 | +0.152            |
| 6      | '###'    | -4.195  | 0.015071 | +0.027            |
| 7      | '1'      | -6.320  | 0.001800 | +0.027            |
| 8      | '6'      | -6.320  | 0.001800 | +0.652            |
| 9      | '4'      | -6.445  | 0.001588 | -1.098            |
| 10     | 'Answer' | -6.945  | 0.000963 | +0.027            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
