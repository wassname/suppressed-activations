---
condition_id: "029_intervention_layer_19"
axis: "intervention_layer"
value: "19"
is_default: false
swap_log_odds_shift: -0.25
valid_answer_mass: 0.9823240041732788
p4: 0.025498539209365845
p8: 0.9568254947662354
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/029_intervention_layer_19/run.md"
---

# 029_intervention_layer_19

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
  "intervention_layer": 19,
  "intervention_positions": "all",
  "strength": 4.0,
  "match_component_norm": true,
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
['\tspin', 'Spin', ' webové', 'สปิน', ' веб', ' webView', ' niem', ' HttpContext']
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
| 1      | '8'       | -0.044  | 0.956825 | +0.007            |
| 2      | '4'       | -3.669  | 0.025499 | -0.243            |
| 3      | '6'       | -4.544  | 0.010629 | +0.132            |
| 4      | '<think>' | -5.919  | 0.002688 | -0.118            |
| 5      | '1'       | -6.919  | 0.000989 | -0.368            |
| 6      | 'Eight'   | -7.169  | 0.000770 | +0.132            |
| 7      | '2'       | -7.919  | 0.000364 | -0.243            |
| 8      | '3'       | -8.169  | 0.000283 | -0.243            |
| 9      | '5'       | -8.419  | 0.000221 | +0.007            |
| 10     | '7'       | -8.482  | 0.000207 | -0.118            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
