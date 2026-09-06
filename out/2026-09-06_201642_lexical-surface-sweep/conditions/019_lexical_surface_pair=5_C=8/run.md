---
condition_id: "019_lexical_surface_pair=5_C=8"
axis: "lexical_surface"
value: "pair=5,C=8"
is_default: false
swap_log_odds_shift: 0.2500002384185791
valid_answer_mass: 0.2738742232322693
p4: 0.0055685085244476795
p8: 0.2683057188987732
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/019_lexical_surface_pair=5_C=8/run.md"
---

# 019_lexical_surface_pair=5_C=8

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
  "strength": 8.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "pair_5",
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
['Spin', '-spin', ' Spin', 'spin', '\tspin', '_spin', 'ปั่น', ' Ủy']
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
| 1      | '**'     | -1.191  | 0.304030 | +0.031            |
| 2      | 'The'    | -1.191  | 0.304030 | +0.031            |
| 3      | '8'      | -1.316  | 0.268306 | -0.094            |
| 4      | 'Fact'   | -2.566  | 0.076871 | +0.156            |
| 5      | 'Number' | -4.066  | 0.017152 | +0.031            |
| 6      | '###'    | -4.566  | 0.010403 | -0.344            |
| 7      | '4'      | -5.191  | 0.005569 | +0.156            |
| 8      | '1'      | -6.316  | 0.001808 | +0.031            |
| 9      | '6'      | -6.441  | 0.001595 | +0.531            |
| 10     | 'Answer' | -7.066  | 0.000854 | -0.094            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
