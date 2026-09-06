---
condition_id: "009_lexical_surface_pair=3_C=2"
axis: "lexical_surface"
value: "pair=3,C=2"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.26889997720718384
p4: 0.00483649130910635
p8: 0.2640634775161743
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/009_lexical_surface_pair=3_C=2/run.md"
---

# 009_lexical_surface_pair=3_C=2

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
  "lexical_forms": "pair_3",
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
['-spin', 'Spin', ' Spin', '\tspin', 'ปั่น', 'spin', ' Ủy', ' Presents']
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
| 1      | '**'     | -1.207  | 0.299223 | +0.015            |
| 2      | 'The'    | -1.207  | 0.299223 | +0.015            |
| 3      | '8'      | -1.332  | 0.264063 | -0.110            |
| 4      | 'Fact'   | -2.457  | 0.085729 | +0.265            |
| 5      | 'Number' | -4.082  | 0.016881 | +0.015            |
| 6      | '###'    | -4.207  | 0.014897 | +0.015            |
| 7      | '4'      | -5.332  | 0.004836 | +0.015            |
| 8      | '1'      | -6.332  | 0.001779 | +0.015            |
| 9      | '6'      | -6.457  | 0.001570 | +0.515            |
| 10     | 'Eight'  | -6.832  | 0.001079 | +0.015            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
