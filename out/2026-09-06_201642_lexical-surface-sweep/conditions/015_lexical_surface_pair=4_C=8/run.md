---
condition_id: "015_lexical_surface_pair=4_C=8"
axis: "lexical_surface"
value: "pair=4,C=8"
is_default: false
swap_log_odds_shift: 2.375
valid_answer_mass: 0.06886935234069824
p4: 0.010195913724601269
p8: 0.0586734376847744
repeated_bigram_fraction: 0.12903225806451613
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/015_lexical_surface_pair=4_C=8/run.md"
---

# 015_lexical_surface_pair=4_C=8

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
['Spin', '\tspin', '-spin', 'spin', ' Spin', '_spin', '旋', '转速']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal that spins webs is a **spider**. Spiders
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.961  | 0.382599 | +0.261            |
| 2      | '**'     | -1.086  | 0.337642 | +0.136            |
| 3      | 'Fact'   | -2.086  | 0.124212 | +0.636            |
| 4      | '8'      | -2.836  | 0.058673 | -1.614            |
| 5      | '6'      | -3.836  | 0.021585 | +3.136            |
| 6      | '###'    | -3.961  | 0.019048 | +0.261            |
| 7      | 'Number' | -3.961  | 0.019048 | +0.136            |
| 8      | '4'      | -4.586  | 0.010196 | +0.761            |
| 9      | '1'      | -5.336  | 0.004816 | +1.011            |
| 10     | '2'      | -6.086  | 0.002275 | +1.636            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
