---
condition_id: "027_lexical_surface_pair=7_C=8"
axis: "lexical_surface"
value: "pair=7,C=8"
is_default: false
swap_log_odds_shift: 0.375
valid_answer_mass: 0.26278579235076904
p4: 0.006038126070052385
p8: 0.25674766302108765
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/027_lexical_surface_pair=7_C=8/run.md"
---

# 027_lexical_surface_pair=7_C=8

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
  "lexical_forms": "pair_7",
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
['-spin', 'ปั่น', ' Ủy', 'Spin', ' Presents', 'seh', ' Spin', ' laba']
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
| 1      | '**'     | -1.110  | 0.329671 | +0.112            |
| 2      | 'The'    | -1.360  | 0.256748 | -0.138            |
| 3      | '8'      | -1.360  | 0.256748 | -0.138            |
| 4      | 'Fact'   | -2.235  | 0.107028 | +0.487            |
| 5      | 'Number' | -4.110  | 0.016413 | -0.013            |
| 6      | '###'    | -4.360  | 0.012783 | -0.138            |
| 7      | '4'      | -5.110  | 0.006038 | +0.237            |
| 8      | '1'      | -6.485  | 0.001527 | -0.138            |
| 9      | 'Eight'  | -6.735  | 0.001189 | +0.112            |
| 10     | '6'      | -6.860  | 0.001049 | +0.112            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
