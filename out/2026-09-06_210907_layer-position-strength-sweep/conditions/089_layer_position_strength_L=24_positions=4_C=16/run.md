---
condition_id: "089_layer_position_strength_L=24_positions=4_C=16"
axis: "layer_position_strength"
value: "L=24,positions=4,C=16"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.3080967962741852
p4: 0.005541492719203234
p8: 0.30255529284477234
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: false
readout_overlap: 0.5
log: "conditions/089_layer_position_strength_L=24_positions=4_C=16/run.md"
---

# 089_layer_position_strength_L=24_positions=4_C=16

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
  "intervention_layer": 24,
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
['compan', ' собаки', ' Hunde', ' собак', ' chiens', ' собака', ' perros', ' perro']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `089_layer_position_strength_L=24_positions=4_C=16`).

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that is famous for spinning webs is the **spider**. Spiders belong to the class Arachnida, which
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.195  | 0.302555 | +0.026            |
| 2      | '8'      | -1.195  | 0.302555 | +0.026            |
| 3      | '**'     | -1.320  | 0.267004 | -0.099            |
| 4      | 'Fact'   | -2.570  | 0.076498 | +0.151            |
| 5      | 'Number' | -4.070  | 0.017069 | +0.026            |
| 6      | '###'    | -4.195  | 0.015063 | +0.026            |
| 7      | '4'      | -5.195  | 0.005541 | +0.151            |
| 8      | '1'      | -6.195  | 0.002039 | +0.151            |
| 9      | 'Answer' | -6.820  | 0.001091 | +0.151            |
| 10     | 'Eight'  | -7.070  | 0.000850 | -0.224            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
