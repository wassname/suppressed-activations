---
condition_id: "002_detector_layers_(8,_16,_24)"
axis: "detector_layers"
value: "(8, 16, 24)"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.9770272374153137
p4: 0.028638847172260284
p8: 0.948388397693634
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/002_detector_layers_(8,_16,_24)/run.md"
---

# 002_detector_layers_(8,_16,_24)

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    8,
    16,
    24
  ],
  "readout_positions": 4,
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
'<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
[' category', ' gioia', ' ใน', '_ME', '亚太', ' relevant', 'blems', ' 관련']
```

Unmodified donor readout:

```python
[' (', '(', ' inter', ' $', ' um', ' seminal', '&', ',']
```

Generation (4 tokens, verbatim):

```text
8<|im_end|>
<|endoftext|>
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '8'       | -0.053  | 0.948388 | -0.002            |
| 2      | '4'       | -3.553  | 0.028639 | -0.127            |
| 3      | '6'       | -4.303  | 0.013528 | +0.373            |
| 4      | '<think>' | -5.803  | 0.003019 | -0.002            |
| 5      | '1'       | -6.053  | 0.002351 | +0.498            |
| 6      | '2'       | -7.178  | 0.000763 | +0.498            |
| 7      | '3'       | -7.553  | 0.000525 | +0.373            |
| 8      | '0'       | -7.553  | 0.000525 | +0.936            |
| 9      | 'Eight'   | -7.990  | 0.000339 | -0.689            |
| 10     | '5'       | -8.053  | 0.000318 | +0.373            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
