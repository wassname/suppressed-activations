---
condition_id: "013_normalization_strength_C=32,component_norm=False,residual_norm=True"
axis: "normalization_strength"
value: "C=32,component_norm=False,residual_norm=True"
is_default: false
swap_log_odds_shift: 4.3125
valid_answer_mass: 0.00011511341290315613
p4: 6.293689511949196e-05
p8: 5.217651778366417e-05
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/013_normalization_strength_C=32,component_norm=False,residual_norm=True/run.md"
---

# 013_normalization_strength_C=32,component_norm=False,residual_norm=True

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
  "strength": 32.0,
  "match_component_norm": false,
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
[' Indústria', '打动', ' Abonn', ' Nordrhein', '河镇', 'éspedes', 'の一', ' Transpar']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
The phrase you provided is a classic **anagram puzzle** often attributed to the mathematician **Leonhard Euler**.

Here is the breakdown:

1.
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | 'The'     | -1.423  | 0.240899 | -0.202            |
| 2      | 'It'      | -1.423  | 0.240899 | +9.298            |
| 3      | 'This'    | -2.298  | 0.100422 | +7.736            |
| 4      | 'Let'     | -2.673  | 0.069019 | +9.611            |
| 5      | 'Your'    | -2.673  | 0.069019 | +9.798            |
| 6      | 'You'     | -2.798  | 0.060909 | +9.048            |
| 7      | 'Looking' | -3.048  | 0.047436 | +10.486           |
| 8      | 'Here'    | -3.548  | 0.028771 | +6.173            |
| 9      | 'To'      | -3.673  | 0.025391 | +6.298            |
| 10     | 'Based'   | -4.048  | 0.017451 | +4.611            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
