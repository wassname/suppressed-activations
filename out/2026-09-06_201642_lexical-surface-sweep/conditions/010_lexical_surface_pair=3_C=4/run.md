---
condition_id: "010_lexical_surface_pair=3_C=4"
axis: "lexical_surface"
value: "pair=3,C=4"
is_default: false
swap_log_odds_shift: 0.8750002384185791
valid_answer_mass: 0.17275312542915344
p4: 0.006448337808251381
p8: 0.1663047820329666
repeated_bigram_fraction: 0.12903225806451613
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/010_lexical_surface_pair=3_C=4/run.md"
---

# 010_lexical_surface_pair=3_C=4

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
['Spin', '-spin', '\tspin', 'spin', ' Spin', '_spin', ' Presents', 'seh']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal that spins webs is the **spider**. Spiders
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.044  | 0.352067 | +0.178            |
| 2      | '**'     | -1.169  | 0.310698 | +0.053            |
| 3      | '8'      | -1.794  | 0.166305 | -0.572            |
| 4      | 'Fact'   | -2.419  | 0.089017 | +0.303            |
| 5      | '6'      | -3.419  | 0.032747 | +3.553            |
| 6      | 'Number' | -4.294  | 0.013651 | -0.197            |
| 7      | '###'    | -4.419  | 0.012047 | -0.197            |
| 8      | '4'      | -5.044  | 0.006448 | +0.303            |
| 9      | '1'      | -5.544  | 0.003911 | +0.803            |
| 10     | 'Eight'  | -6.544  | 0.001439 | +0.303            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
