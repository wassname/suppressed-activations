---
condition_id: "094_layer_position_strength_L=26_positions=1_C=16"
axis: "layer_position_strength"
value: "L=26,positions=1,C=16"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.3112099766731262
p4: 0.004950226750224829
p8: 0.30625975131988525
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/094_layer_position_strength_L=26_positions=1_C=16/run.md"
---

# 094_layer_position_strength_L=26_positions=1_C=16

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
['ปั่น', '-spin', ' Ủy', 'Spin', ' Presents', 'seh', ' Spin', ' laba']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `094_layer_position_strength_L=26_positions=1_C=16`).

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.183  | 0.306260 | +0.038            |
| 2      | '8'      | -1.183  | 0.306260 | +0.038            |
| 3      | '**'     | -1.308  | 0.270273 | -0.087            |
| 4      | 'Fact'   | -2.683  | 0.068336 | +0.038            |
| 5      | 'Number' | -4.058  | 0.017278 | +0.038            |
| 6      | '###'    | -4.308  | 0.013456 | -0.087            |
| 7      | '4'      | -5.308  | 0.004950 | +0.038            |
| 8      | '1'      | -6.308  | 0.001821 | +0.038            |
| 9      | 'Answer' | -6.933  | 0.000975 | +0.038            |
| 10     | 'Eight'  | -6.933  | 0.000975 | -0.087            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
