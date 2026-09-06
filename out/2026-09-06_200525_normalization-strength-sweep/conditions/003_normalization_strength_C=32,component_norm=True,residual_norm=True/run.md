---
condition_id: "003_normalization_strength_C=32,component_norm=True,residual_norm=True"
axis: "normalization_strength"
value: "C=32,component_norm=True,residual_norm=True"
is_default: false
swap_log_odds_shift: 4.0
valid_answer_mass: 0.0002508529869373888
p4: 0.00011759752669604495
p8: 0.0001332554529653862
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "It"
readout_overlap: 0.0
log: "conditions/003_normalization_strength_C=32,component_norm=True,residual_norm=True/run.md"
---

# 003_normalization_strength_C=32,component_norm=True,residual_norm=True

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
['Sampler', 'وائية', '中小学生', '判決', 'WhatsApp', ' Schles', ' методы', '(namespace']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
It looks like you've provided a string of text that mixes words, numbers, and symbols in a somewhat chaotic or patterned way. Let's break it down
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | 'It'      | -1.361  | 0.256470 | +9.361            |
| 2      | 'Let'     | -1.736  | 0.176269 | +10.548           |
| 3      | 'The'     | -2.111  | 0.121148 | -0.889            |
| 4      | 'Based'   | -2.236  | 0.106913 | +6.423            |
| 5      | 'Here'    | -2.361  | 0.094350 | +7.361            |
| 6      | 'Looking' | -2.611  | 0.073480 | +10.923           |
| 7      | 'To'      | -3.361  | 0.034709 | +6.611            |
| 8      | 'Your'    | -3.611  | 0.027032 | +8.861            |
| 9      | 'You'     | -3.986  | 0.018579 | +7.861            |
| 10     | 'This'    | -4.111  | 0.016396 | +5.923            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
