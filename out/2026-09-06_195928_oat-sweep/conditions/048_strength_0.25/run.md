---
condition_id: "048_strength_0.25"
axis: "strength"
value: "0.25"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.3006150722503662
p4: 0.004781701136380434
p8: 0.29583337903022766
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.0
log: "conditions/048_strength_0.25/run.md"
---

# 048_strength_0.25

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
  "strength": 0.25,
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
['-spin', 'Spin', 'ปั่น', ' Ủy', ' Spin', '\tspin', 'seh', 'spin']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.218  | 0.295833 | +0.004            |
| 2      | 'The'    | -1.218  | 0.295833 | +0.004            |
| 3      | '**'     | -1.218  | 0.295833 | +0.004            |
| 4      | 'Fact'   | -2.718  | 0.066009 | +0.004            |
| 5      | 'Number' | -4.218  | 0.014729 | -0.121            |
| 6      | '###'    | -4.343  | 0.012998 | -0.121            |
| 7      | '4'      | -5.343  | 0.004782 | +0.004            |
| 8      | '1'      | -6.343  | 0.001759 | +0.004            |
| 9      | 'Eight'  | -6.718  | 0.001209 | +0.129            |
| 10     | 'Answer' | -6.843  | 0.001067 | +0.129            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
