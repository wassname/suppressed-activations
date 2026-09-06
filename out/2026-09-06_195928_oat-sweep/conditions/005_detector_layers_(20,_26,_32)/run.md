---
condition_id: "005_detector_layers_(20,_26,_32)"
axis: "detector_layers"
value: "(20, 26, 32)"
is_default: false
swap_log_odds_shift: 1.625000238418579
valid_answer_mass: 0.034084733575582504
p4: 0.0025856064166873693
p8: 0.03149912878870964
repeated_bigram_fraction: 0.12903225806451613
generation_tokens: 32
first_token: "**"
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
'<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
[' dateFormat', ' vrijeme', ' Физи', ' inneh', ' Spanien', ' getragen', ' människor', ' Negócios']
```

Unmodified donor readout:

```python
['ॉ', ' Hunde', ' собаки', ' Descrição', ' Montage', ' interessiert', 'ército', ' Democracy']
```

Generation (32 tokens, verbatim):

```text
**Fact:** The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal that spins webs is the **spider
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | '**'       | -0.833  | 0.434832 | +0.389            |
| 2      | 'The'      | -1.333  | 0.263739 | -0.111            |
| 3      | '###'      | -2.208  | 0.109943 | +2.014            |
| 4      | 'Fact'     | -2.333  | 0.097024 | +0.389            |
| 5      | '8'        | -3.458  | 0.031499 | -2.236            |
| 6      | 'Number'   | -3.958  | 0.019105 | +0.139            |
| 7      | '6'        | -4.958  | 0.007028 | +2.014            |
| 8      | '1'        | -5.083  | 0.006203 | +1.264            |
| 9      | 'Complete' | -5.333  | 0.004831 | +1.889            |
| 10     | 'Based'    | -5.708  | 0.003320 | +2.951            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
