---
condition_id: "005_detector_layers_(20,_26,_32)"
axis: "detector_layers"
value: "(20, 26, 32)"
is_default: false
swap_log_odds_shift: 2.125
valid_answer_mass: 0.6544545888900757
p4: 0.1457471400499344
p8: 0.5087074637413025
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/005_detector_layers_(20,_26,_32)/run.md"
---

# 005_detector_layers_(20,_26,_32)

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    20,
    26,
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
[' устанавли', 'ツール', ' vrijeme', ' Физи', ' petugas', ' нену', '상황', ' положитель']
```

Unmodified donor readout:

```python
['ॉ', ' Hunde', ' собаки', ' interessiert', ' Descrição', ' собак', 'ército', ' Democracy']
```

Generation (4 tokens, verbatim):

```text
8<|im_end|>
<|endoftext|>
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '8'       | -0.676  | 0.508707 | -0.625            |
| 2      | '6'       | -1.426  | 0.240296 | +3.250            |
| 3      | '4'       | -1.926  | 0.145747 | +1.500            |
| 4      | '1'       | -3.051  | 0.047317 | +3.500            |
| 5      | '2'       | -4.051  | 0.017407 | +3.625            |
| 6      | '3'       | -4.426  | 0.011964 | +3.500            |
| 7      | '0'       | -4.551  | 0.010558 | +3.938            |
| 8      | '5'       | -5.051  | 0.006404 | +3.375            |
| 9      | '7'       | -6.051  | 0.002356 | +2.313            |
| 10     | '<think>' | -6.176  | 0.002079 | -0.375            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
