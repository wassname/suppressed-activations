---
condition_id: "133_layer_position_strength_L=30_positions=4_C=8"
axis: "layer_position_strength"
value: "L=30,positions=4,C=8"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.2875014543533325
p4: 0.004573109559714794
p8: 0.28292834758758545
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/133_layer_position_strength_L=30_positions=4_C=8/run.md"
---

# 133_layer_position_strength_L=30_positions=4_C=8

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
  "intervention_layer": 30,
  "intervention_positions": 4,
  "strength": 8.0,
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
[' spinning', ' spin', ' atingir', ' spins', ' spiders', '纺', 'web', '.Sp']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `133_layer_position_strength_L=30_positions=4_C=8`).

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal most commonly associated with spinning webs is the **spider
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.138  | 0.320600 | +0.084            |
| 2      | '**'     | -1.263  | 0.282928 | -0.041            |
| 3      | '8'      | -1.263  | 0.282928 | -0.041            |
| 4      | 'Fact'   | -2.763  | 0.063130 | -0.041            |
| 5      | 'Number' | -4.013  | 0.018087 | +0.084            |
| 6      | '###'    | -4.263  | 0.014086 | -0.041            |
| 7      | '4'      | -5.388  | 0.004573 | -0.041            |
| 8      | '1'      | -6.263  | 0.001906 | +0.084            |
| 9      | 'Eight'  | -6.888  | 0.001020 | -0.041            |
| 10     | 'Answer' | -7.013  | 0.000900 | -0.041            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
