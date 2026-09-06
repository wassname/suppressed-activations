---
condition_id: "022_lexical_surface_pair=6_C=4"
axis: "lexical_surface"
value: "pair=6,C=4"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.24599984288215637
p4: 0.003912968561053276
p8: 0.24208687245845795
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/022_lexical_surface_pair=6_C=4/run.md"
---

# 022_lexical_surface_pair=6_C=4

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
  "lexical_forms": "pair_6",
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
['-spin', 'Spin', 'ปั่น', ' Ủy', ' Spin', '\tspin', ' Presents', 'spin']
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
| 1      | '**'     | -1.168  | 0.310846 | +0.053            |
| 2      | 'The'    | -1.168  | 0.310846 | +0.053            |
| 3      | '8'      | -1.418  | 0.242087 | -0.197            |
| 4      | 'Fact'   | -2.418  | 0.089059 | +0.303            |
| 5      | 'Number' | -4.168  | 0.015476 | -0.072            |
| 6      | '###'    | -4.293  | 0.013658 | -0.072            |
| 7      | '4'      | -5.543  | 0.003913 | -0.197            |
| 8      | '1'      | -6.543  | 0.001440 | -0.197            |
| 9      | '6'      | -6.668  | 0.001270 | +0.303            |
| 10     | 'Eight'  | -6.793  | 0.001121 | +0.053            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
