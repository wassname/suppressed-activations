---
condition_id: "005_lexical_surface_pair=2_C=2"
axis: "lexical_surface"
value: "pair=2,C=2"
is_default: false
swap_log_odds_shift: 0.2499997615814209
valid_answer_mass: 0.24903933703899384
p4: 0.005063554737716913
p8: 0.24397578835487366
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/005_lexical_surface_pair=2_C=2/run.md"
---

# 005_lexical_surface_pair=2_C=2

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
  "lexical_forms": "pair_2",
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
['-spin', 'Spin', 'ปั่น', ' Ủy', ' Spin', ' Presents', 'seh', 'spin']
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
| 1      | 'The'    | -1.161  | 0.313271 | +0.061            |
| 2      | '**'     | -1.161  | 0.313271 | +0.061            |
| 3      | '8'      | -1.411  | 0.243976 | -0.189            |
| 4      | 'Fact'   | -2.536  | 0.079207 | +0.186            |
| 5      | 'Number' | -4.161  | 0.015597 | -0.064            |
| 6      | '###'    | -4.161  | 0.015597 | +0.061            |
| 7      | '4'      | -5.286  | 0.005064 | +0.061            |
| 8      | '1'      | -6.411  | 0.001644 | -0.064            |
| 9      | 'Eight'  | -6.786  | 0.001130 | +0.061            |
| 10     | '6'      | -6.911  | 0.000997 | +0.061            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
