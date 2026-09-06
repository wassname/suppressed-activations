---
condition_id: "008_normalization_strength_C=32,component_norm=True,residual_norm=False"
axis: "normalization_strength"
value: "C=32,component_norm=True,residual_norm=False"
is_default: false
swap_log_odds_shift: 4.625
valid_answer_mass: 0.0002800559450406581
p4: 0.0001743234315654263
p8: 0.00010573250619927421
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/008_normalization_strength_C=32,component_norm=True,residual_norm=False/run.md"
---

# 008_normalization_strength_C=32,component_norm=True,residual_norm=False

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
['ńcz', 'ię', 'ждан', '得我', 'ynı', '是人体', '申领', ' военной']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
The phrase you provided is a classic example of a **palindrome** (specifically, a sentence that reads the same forwards and backwards, ignoring spaces, punctuation
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | 'The'     | -1.655  | 0.191169 | -0.433            |
| 2      | 'It'      | -1.780  | 0.168706 | +8.942            |
| 3      | 'Let'     | -2.030  | 0.131388 | +10.254           |
| 4      | 'Here'    | -2.280  | 0.102325 | +7.442            |
| 5      | 'Your'    | -2.280  | 0.102325 | +10.192           |
| 6      | 'You'     | -2.530  | 0.079691 | +9.317            |
| 7      | 'This'    | -3.155  | 0.042656 | +6.879            |
| 8      | 'Looking' | -3.905  | 0.020149 | +9.629            |
| 9      | 'There'   | -3.905  | 0.020149 | +4.692            |
| 10     | 'To'      | -4.155  | 0.015692 | +5.817            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
