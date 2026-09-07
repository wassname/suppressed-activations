---
condition_id: "104_layer_position_strength_L=26_positions=4_C=16"
axis: "layer_position_strength"
value: "L=26,positions=4,C=16"
is_default: false
swap_log_odds_shift: 0.2500002384185791
valid_answer_mass: 0.27281633019447327
p4: 0.005547000095248222
p8: 0.2672693431377411
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
first_answer: "8"
source_fact_preserved: false
readout_overlap: 0.0
log: "conditions/104_layer_position_strength_L=26_positions=4_C=16/run.md"
---

# 104_layer_position_strength_L=26_positions=4_C=16

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
[' spinning', 'web', ' WEB', ' spin', ' atingir', ' spins', ' spiders', ' cotton']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `104_layer_position_strength_L=26_positions=4_C=16`).

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that is famous for spinning webs is the **spider**. Spiders belong to the class *Arachn
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | 'The'      | -1.194  | 0.302856 | +0.027            |
| 2      | '**'       | -1.194  | 0.302856 | +0.027            |
| 3      | '8'        | -1.319  | 0.267269 | -0.098            |
| 4      | 'Fact'     | -2.569  | 0.076574 | +0.152            |
| 5      | 'Number'   | -4.069  | 0.017086 | +0.027            |
| 6      | '###'      | -4.194  | 0.015078 | +0.027            |
| 7      | '4'        | -5.194  | 0.005547 | +0.152            |
| 8      | '1'        | -6.319  | 0.001801 | +0.027            |
| 9      | 'Answer'   | -6.944  | 0.000964 | +0.027            |
| 10     | 'Complete' | -7.194  | 0.000751 | +0.027            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
