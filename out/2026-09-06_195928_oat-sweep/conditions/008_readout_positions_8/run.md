---
condition_id: "008_readout_positions_8"
axis: "readout_positions"
value: "8"
is_default: false
swap_log_odds_shift: -0.375
valid_answer_mass: 0.13582535088062286
p4: 0.0014923049602657557
p8: 0.1343330442905426
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/008_readout_positions_8/run.md"
---

# 008_readout_positions_8

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    23,
    25,
    32
  ],
  "readout_positions": 8,
  "rank": 8,
  "intervention_layer": 1,
  "intervention_positions": "all",
  "strength": 4.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0
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
['盐酸', '_keeper', 'må', 'ografie', 'поле', 'vă', 'ピソード', ' medarbe']
```

Unmodified donor readout:

```python
['吠', ' Dogs', 'MAN', '薩', 'Manchester', 'compan', 'Overlay', '萨']
```

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -0.882  | 0.413775 | +0.339            |
| 2      | 'The'    | -1.257  | 0.284383 | -0.036            |
| 3      | '8'      | -2.007  | 0.134333 | -0.786            |
| 4      | 'Fact'   | -2.257  | 0.104619 | +0.464            |
| 5      | 'Number' | -3.882  | 0.020601 | +0.214            |
| 6      | '###'    | -3.882  | 0.020601 | +0.339            |
| 7      | 'Eight'  | -5.632  | 0.003580 | +1.214            |
| 8      | '1'      | -5.882  | 0.002788 | +0.464            |
| 9      | '4'      | -6.507  | 0.001492 | -1.161            |
| 10     | 'Answer' | -6.632  | 0.001317 | +0.339            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
