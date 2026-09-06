---
condition_id: "006_lexical_surface_pair=2_C=4"
axis: "lexical_surface"
value: "pair=2,C=4"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.20755033195018768
p4: 0.003733043558895588
p8: 0.20381729304790497
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/006_lexical_surface_pair=2_C=4/run.md"
---

# 006_lexical_surface_pair=2_C=4

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
  "intervention_layer": 1,
  "intervention_positions": "all",
  "strength": 4.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "pair_2",
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
['-spin', 'Spin', ' Spin', 'ปั่น', 'spin', '\tspin', ' Presents', ' Ủy']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class *Arachnida*, which
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -1.091  | 0.336038 | +0.131            |
| 2      | 'The'    | -1.216  | 0.296552 | +0.006            |
| 3      | '8'      | -1.591  | 0.203817 | -0.369            |
| 4      | 'Fact'   | -2.216  | 0.109096 | +0.506            |
| 5      | 'Number' | -3.966  | 0.018958 | +0.131            |
| 6      | '###'    | -4.091  | 0.016730 | +0.131            |
| 7      | '4'      | -5.591  | 0.003733 | -0.244            |
| 8      | '6'      | -6.466  | 0.001556 | +0.506            |
| 9      | '1'      | -6.466  | 0.001556 | -0.119            |
| 10     | 'Eight'  | -6.716  | 0.001212 | +0.131            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
