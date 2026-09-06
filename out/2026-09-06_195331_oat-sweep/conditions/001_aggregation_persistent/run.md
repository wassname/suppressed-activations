---
condition_id: "001_aggregation_persistent"
axis: "aggregation"
value: "persistent"
is_default: false
swap_log_odds_shift: 0.25
valid_answer_mass: 0.9849433302879333
p4: 0.041454024612903595
p8: 0.9434893131256104
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/001_aggregation_persistent/run.md"
---

# 001_aggregation_persistent

Resolved config:

```json
{
  "aggregation": "persistent",
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
[' miejs', 'edata', '民政部门', ' ГИБДД', '取締', '车床', ' polskich', 'emiş']
```

Unmodified donor readout:

```python
[' Tricks', ' Unik', '直肠癌', ' ακό', 'しら', 'raad', ' vergel', 'dach']
```

Generation (4 tokens, verbatim):

```text
8<|im_end|>
<|endoftext|>
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '8'       | -0.058  | 0.943489 | -0.007            |
| 2      | '4'       | -3.183  | 0.041454 | +0.243            |
| 3      | '6'       | -4.808  | 0.008163 | -0.132            |
| 4      | '<think>' | -6.183  | 0.002064 | -0.382            |
| 5      | '1'       | -6.558  | 0.001418 | -0.007            |
| 6      | '2'       | -7.308  | 0.000670 | +0.368            |
| 7      | 'Eight'   | -7.433  | 0.000591 | -0.132            |
| 8      | '3'       | -7.808  | 0.000406 | +0.118            |
| 9      | '0'       | -8.246  | 0.000262 | +0.243            |
| 10     | '5'       | -8.371  | 0.000232 | +0.056            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
