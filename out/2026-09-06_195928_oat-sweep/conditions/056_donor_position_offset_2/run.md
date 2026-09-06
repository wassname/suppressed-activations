---
condition_id: "056_donor_position_offset_2"
axis: "donor_position_offset"
value: "2"
is_default: false
swap_log_odds_shift: 0.8749997615814209
valid_answer_mass: 0.1611095666885376
p4: 0.006013716571033001
p8: 0.15509584546089172
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/056_donor_position_offset_2/run.md"
---

# 056_donor_position_offset_2

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
  "donor_position_offset": 2
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
['张掖', ' Bốn', 'må', '犹太人', 'Agama', '_human', '.ToolStripMenuItem', ' Urbano']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders are arachnids, not insects. Unlike insects
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -0.864  | 0.421594 | +0.358            |
| 2      | 'The'    | -1.364  | 0.255710 | -0.142            |
| 3      | '8'      | -1.864  | 0.155096 | -0.642            |
| 4      | 'Fact'   | -2.489  | 0.083017 | +0.233            |
| 5      | '6'      | -3.864  | 0.020990 | +3.108            |
| 6      | 'Number' | -4.114  | 0.016347 | -0.017            |
| 7      | '###'    | -4.239  | 0.014426 | -0.017            |
| 8      | '1'      | -4.739  | 0.008750 | +1.608            |
| 9      | '4'      | -5.114  | 0.006014 | +0.233            |
| 10     | '2'      | -6.364  | 0.001723 | +1.358            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
