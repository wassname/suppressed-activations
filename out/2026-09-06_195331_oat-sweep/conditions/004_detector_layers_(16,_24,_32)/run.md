---
condition_id: "004_detector_layers_(16,_24,_32)"
axis: "detector_layers"
value: "(16, 24, 32)"
is_default: false
swap_log_odds_shift: -0.25
valid_answer_mass: 0.9770030379295349
p4: 0.025360414758324623
p8: 0.951642632484436
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.125
log: "conditions/004_detector_layers_(16,_24,_32)/run.md"
---

# 004_detector_layers_(16,_24,_32)

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    16,
    24,
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
['でご', ' simptom', 'のレストラン', 'ੂ', ' Добро', ' Dreh', '.toolStripButton', ' користу']
```

Unmodified donor readout:

```python
[' kulinar', 'kontakt', ' متاب', '新', 'carat', 'owment', ' éduc', 'でご']
```

Generation (4 tokens, verbatim):

```text
8<|im_end|>
<|endoftext|>
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '8'       | -0.050  | 0.951643 | +0.002            |
| 2      | '4'       | -3.675  | 0.025360 | -0.248            |
| 3      | '6'       | -4.425  | 0.011979 | +0.252            |
| 4      | '<think>' | -5.425  | 0.004407 | +0.377            |
| 5      | '1'       | -6.175  | 0.002082 | +0.377            |
| 6      | '2'       | -7.300  | 0.000676 | +0.377            |
| 7      | 'Eight'   | -7.487  | 0.000560 | -0.186            |
| 8      | '3'       | -7.550  | 0.000526 | +0.377            |
| 9      | '0'       | -7.737  | 0.000436 | +0.752            |
| 10     | '5'       | -8.112  | 0.000300 | +0.314            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
