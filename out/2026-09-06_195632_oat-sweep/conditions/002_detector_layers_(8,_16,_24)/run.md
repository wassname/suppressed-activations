---
condition_id: "002_detector_layers_(8,_16,_24)"
axis: "detector_layers"
value: "(8, 16, 24)"
is_default: false
swap_log_odds_shift: 0.9375
valid_answer_mass: 0.0009073445689864457
p4: 4.450892902241321e-06
p8: 0.0009028936619870365
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
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
'<|im_start|>user\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['_id', ' category', '-black', ' methyl', ' през', ' things', 'things', ' ultrasound']
```

Unmodified donor readout:

```python
[' seminal', ' inter', ' damp', '挟', ' neut', ' um', ' (', 'лом']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have eight legs. Therefore, the number of
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.135  | 0.873798 | -0.039            |
| 2      | 'Based'  | -2.260  | 0.104360 | +0.461            |
| 3      | 'To'     | -5.885  | 0.002781 | -0.164            |
| 4      | 'Sp'     | -6.135  | 0.002166 | -0.539            |
| 5      | '**'     | -6.135  | 0.002166 | +0.086            |
| 6      | 'An'     | -6.260  | 0.001911 | -0.164            |
| 7      | 'Most'   | -6.260  | 0.001911 | -0.664            |
| 8      | 'Animal' | -7.010  | 0.000903 | +0.086            |
| 9      | '8'      | -7.010  | 0.000903 | +0.461            |
| 10     | 'There'  | -7.135  | 0.000797 | -0.039            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
