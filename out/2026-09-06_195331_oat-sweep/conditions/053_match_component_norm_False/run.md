---
condition_id: "053_match_component_norm_False"
axis: "match_component_norm"
value: "False"
is_default: false
swap_log_odds_shift: 0.25
valid_answer_mass: 0.8266959190368652
p4: 0.034793753176927567
p8: 0.7919021844863892
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/053_match_component_norm_False/run.md"
---

# 053_match_component_norm_False

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
  "match_component_norm": false,
  "restore_residual_norm": true,
  "donor_position_offset": 0
}
```

Source input (`repr`):

```python
'<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['盐酸', ' laba', 'må', 'ピソード', ' webView', ' Urbano', '满怀', ' веб']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', ' perro', 'amax', ' NHÀ']
```

Generation (4 tokens, verbatim):

```text
8<|im_end|>
<|endoftext|>
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '8'       | -0.233  | 0.791902 | -0.182            |
| 2      | '6'       | -1.858  | 0.155935 | +2.818            |
| 3      | '4'       | -3.358  | 0.034794 | +0.068            |
| 4      | '1'       | -5.233  | 0.005336 | +1.318            |
| 5      | '<think>' | -5.733  | 0.003236 | +0.068            |
| 6      | '2'       | -5.983  | 0.002520 | +1.693            |
| 7      | 'Eight'   | -6.483  | 0.001529 | +0.818            |
| 8      | '3'       | -7.108  | 0.000818 | +0.818            |
| 9      | '0'       | -7.108  | 0.000818 | +1.380            |
| 10     | '5'       | -7.733  | 0.000438 | +0.693            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
