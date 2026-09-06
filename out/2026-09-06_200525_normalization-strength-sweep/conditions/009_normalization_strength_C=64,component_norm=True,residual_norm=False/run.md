---
condition_id: "009_normalization_strength_C=64,component_norm=True,residual_norm=False"
axis: "normalization_strength"
value: "C=64,component_norm=True,residual_norm=False"
is_default: false
swap_log_odds_shift: 4.75
valid_answer_mass: 6.023498281138018e-05
p4: 3.9234349969774485e-05
p8: 2.1000632841605693e-05
repeated_bigram_fraction: 0.12903225806451613
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/009_normalization_strength_C=64,component_norm=True,residual_norm=False/run.md"
---

# 009_normalization_strength_C=64,component_norm=True,residual_norm=False

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
  "strength": 64.0,
  "match_component_norm": true,
  "restore_residual_norm": false,
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
[' dług', ' الكيميائية', '挽救', ' lijek', ' Kara', ' economica', '审批', ' границ']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
The text you provided is a playful, recursive repetition of the word **"label"** (or in this case, **"label"** spelled as **"label"** but visually
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | 'The'     | -1.208  | 0.298657 | +0.013            |
| 2      | 'It'      | -1.458  | 0.232595 | +9.263            |
| 3      | 'This'    | -2.083  | 0.124499 | +7.951            |
| 4      | 'Your'    | -2.208  | 0.109870 | +10.263           |
| 5      | 'That'    | -2.833  | 0.058809 | +8.701            |
| 6      | 'You'     | -3.083  | 0.045801 | +8.763            |
| 7      | 'I'       | -4.208  | 0.014869 | +6.826            |
| 8      | 'There'   | -4.271  | 0.013968 | +4.326            |
| 9      | 'Hello'   | -4.333  | 0.013122 | +10.763           |
| 10     | 'Looking' | -4.708  | 0.009019 | +8.826            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
