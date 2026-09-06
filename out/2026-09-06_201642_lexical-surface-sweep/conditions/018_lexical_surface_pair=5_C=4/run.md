---
condition_id: "018_lexical_surface_pair=5_C=4"
axis: "lexical_surface"
value: "pair=5,C=4"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.28541165590286255
p4: 0.004539869725704193
p8: 0.28087177872657776
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/018_lexical_surface_pair=5_C=4/run.md"
---

# 018_lexical_surface_pair=5_C=4

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
['-spin', 'Spin', 'ปั่น', ' Spin', ' Ủy', 'spin', '\tspin', ' Presents']
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
| 1      | '**'     | -1.145  | 0.318269 | +0.077            |
| 2      | 'The'    | -1.270  | 0.280872 | -0.048            |
| 3      | '8'      | -1.270  | 0.280872 | -0.048            |
| 4      | 'Fact'   | -2.645  | 0.071016 | +0.077            |
| 5      | 'Number' | -4.020  | 0.017956 | +0.077            |
| 6      | '###'    | -4.395  | 0.012341 | -0.173            |
| 7      | '4'      | -5.395  | 0.004540 | -0.048            |
| 8      | '1'      | -6.270  | 0.001892 | +0.077            |
| 9      | '6'      | -6.770  | 0.001148 | +0.202            |
| 10     | 'Answer' | -6.895  | 0.001013 | +0.077            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
