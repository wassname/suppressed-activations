---
condition_id: "021_lexical_surface_pair=6_C=2"
axis: "lexical_surface"
value: "pair=6,C=2"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.2721167504787445
p4: 0.004328395705670118
p8: 0.2677883505821228
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/021_lexical_surface_pair=6_C=2/run.md"
---

# 021_lexical_surface_pair=6_C=2

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
['-spin', 'Spin', 'ปั่น', ' Ủy', ' Spin', ' Presents', 'seh', '\tspin']
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
| 1      | 'The'    | -1.193  | 0.303444 | +0.029            |
| 2      | '**'     | -1.193  | 0.303444 | +0.029            |
| 3      | '8'      | -1.318  | 0.267788 | -0.096            |
| 4      | 'Fact'   | -2.568  | 0.076723 | +0.154            |
| 5      | 'Number' | -4.068  | 0.017119 | +0.029            |
| 6      | '###'    | -4.318  | 0.013332 | -0.096            |
| 7      | '4'      | -5.443  | 0.004328 | -0.096            |
| 8      | '1'      | -6.443  | 0.001592 | -0.096            |
| 9      | 'Eight'  | -6.818  | 0.001094 | +0.029            |
| 10     | '6'      | -6.943  | 0.000966 | +0.029            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
