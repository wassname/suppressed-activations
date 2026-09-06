---
condition_id: "057_donor_position_offset_3"
axis: "donor_position_offset"
value: "3"
is_default: false
swap_log_odds_shift: -0.375
valid_answer_mass: 0.15261805057525635
p4: 0.0016768062487244606
p8: 0.15094123780727386
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/057_donor_position_offset_3/run.md"
---

# 057_donor_position_offset_3

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
  "donor_position_offset": 3
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
['盐酸', 'må', ' laba', '犹太人', ' Infant', 'くださ', 'ränkt', 'rsp']
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
| 1      | '**'     | -0.891  | 0.410301 | +0.331            |
| 2      | 'The'    | -1.391  | 0.248860 | -0.169            |
| 3      | '8'      | -1.891  | 0.150941 | -0.669            |
| 4      | 'Fact'   | -2.016  | 0.133205 | +0.706            |
| 5      | 'Number' | -4.141  | 0.015909 | -0.044            |
| 6      | '###'    | -4.266  | 0.014040 | -0.044            |
| 7      | '6'      | -4.766  | 0.008516 | +2.206            |
| 8      | '1'      | -5.891  | 0.002765 | +0.456            |
| 9      | '4'      | -6.391  | 0.001677 | -1.044            |
| 10     | 'Eight'  | -6.516  | 0.001480 | +0.331            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
