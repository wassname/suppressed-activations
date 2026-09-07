---
condition_id: "044_layer_position_strength_L=16_positions=4_C=16"
axis: "layer_position_strength"
value: "L=16,positions=4,C=16"
is_default: false
swap_log_odds_shift: 1.125
valid_answer_mass: 0.14004729688167572
p4: 0.00664186617359519
p8: 0.1334054321050644
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/044_layer_position_strength_L=16_positions=4_C=16/run.md"
---

# 044_layer_position_strength_L=16_positions=4_C=16

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
  "intervention_layer": 16,
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
['誇る', ' Bốn', 'の商品', 'の部分', 'slider', ' Banj', '报警器', 'Processor']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `044_layer_position_strength_L=16_positions=4_C=16`).

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class *Arachnida*, which
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -1.014  | 0.362634 | +0.207            |
| 2      | 'The'    | -1.389  | 0.249234 | -0.168            |
| 3      | '8'      | -2.014  | 0.133405 | -0.793            |
| 4      | '6'      | -2.139  | 0.117730 | +4.832            |
| 5      | 'Fact'   | -2.639  | 0.071407 | +0.082            |
| 6      | 'Number' | -3.639  | 0.026269 | +0.457            |
| 7      | '###'    | -4.389  | 0.012409 | -0.168            |
| 8      | '4'      | -5.014  | 0.006642 | +0.332            |
| 9      | '1'      | -5.264  | 0.005173 | +1.082            |
| 10     | '#'      | -6.639  | 0.001308 | +0.582            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
