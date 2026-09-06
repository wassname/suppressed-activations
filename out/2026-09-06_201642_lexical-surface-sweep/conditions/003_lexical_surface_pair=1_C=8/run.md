---
condition_id: "003_lexical_surface_pair=1_C=8"
axis: "lexical_surface"
value: "pair=1,C=8"
is_default: false
swap_log_odds_shift: 0.25
valid_answer_mass: 0.177755668759346
p4: 0.003614191198721528
p8: 0.17414148151874542
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/003_lexical_surface_pair=1_C=8/run.md"
---

# 003_lexical_surface_pair=1_C=8

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
  "lexical_forms": "pair_1",
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
['-spin', 'Spin', 'ปั่น', ' Presents', ' Ủy', 'seh', '\tspin', '_spin']
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
| 1      | '**'     | -1.123  | 0.325339 | +0.099            |
| 2      | 'The'    | -1.123  | 0.325339 | +0.099            |
| 3      | '8'      | -1.748  | 0.174141 | -0.526            |
| 4      | 'Fact'   | -2.248  | 0.105622 | +0.474            |
| 5      | '6'      | -4.123  | 0.016198 | +2.849            |
| 6      | 'Number' | -4.123  | 0.016198 | -0.026            |
| 7      | '###'    | -4.123  | 0.016198 | +0.099            |
| 8      | '1'      | -5.498  | 0.004095 | +0.849            |
| 9      | '4'      | -5.623  | 0.003614 | -0.276            |
| 10     | 'Eight'  | -6.748  | 0.001173 | +0.099            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
