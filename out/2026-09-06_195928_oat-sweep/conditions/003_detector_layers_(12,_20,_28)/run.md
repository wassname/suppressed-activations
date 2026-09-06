---
condition_id: "003_detector_layers_(12,_20,_28)"
axis: "detector_layers"
value: "(12, 20, 28)"
is_default: false
swap_log_odds_shift: 0.3750002384185791
valid_answer_mass: 0.2071446180343628
p4: 0.004759639501571655
p8: 0.20238497853279114
repeated_bigram_fraction: 0.12903225806451613
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/003_detector_layers_(12,_20,_28)/run.md"
---

# 003_detector_layers_(12,_20,_28)

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    12,
    20,
    28
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
['增添', ' food', ' Figure', '折射', ' multiples', '-j', ' decreases', ' marker']
```

Unmodified donor readout:

```python
['三八', '带头作用', '而闻名', '장으로', '隔开', 'óricos', ' 한반', './']
```

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal that spins webs is the **spider**. Spiders
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.723  | 0.485496 | +0.499            |
| 2      | '8'      | -1.598  | 0.202385 | -0.376            |
| 3      | '**'     | -1.723  | 0.178604 | -0.501            |
| 4      | 'Fact'   | -2.473  | 0.084367 | +0.249            |
| 5      | '###'    | -4.223  | 0.014661 | -0.001            |
| 6      | 'Number' | -4.473  | 0.011418 | -0.376            |
| 7      | '4'      | -5.348  | 0.004760 | -0.001            |
| 8      | '1'      | -5.973  | 0.002548 | +0.374            |
| 9      | '6'      | -6.598  | 0.001364 | +0.374            |
| 10     | 'Eight'  | -6.598  | 0.001364 | +0.249            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
