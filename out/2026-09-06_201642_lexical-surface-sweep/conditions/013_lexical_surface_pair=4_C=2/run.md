---
condition_id: "013_lexical_surface_pair=4_C=2"
axis: "lexical_surface"
value: "pair=4,C=2"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.22617623209953308
p4: 0.004068051930516958
p8: 0.22210818529129028
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/013_lexical_surface_pair=4_C=2/run.md"
---

# 013_lexical_surface_pair=4_C=2

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
  "strength": 2.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "pair_4",
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
['-spin', 'Spin', 'ปั่น', ' Spin', '\tspin', ' Ủy', 'spin', ' Presents']
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
| 1      | 'The'    | -1.130  | 0.323166 | +0.092            |
| 2      | '**'     | -1.130  | 0.323166 | +0.092            |
| 3      | '8'      | -1.505  | 0.222108 | -0.283            |
| 4      | 'Fact'   | -2.505  | 0.081709 | +0.217            |
| 5      | 'Number' | -4.130  | 0.016089 | -0.033            |
| 6      | '###'    | -4.130  | 0.016089 | +0.092            |
| 7      | '4'      | -5.505  | 0.004068 | -0.158            |
| 8      | '1'      | -6.505  | 0.001497 | -0.158            |
| 9      | '6'      | -6.880  | 0.001029 | +0.092            |
| 10     | 'Answer' | -6.880  | 0.001029 | +0.092            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
