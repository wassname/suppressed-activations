---
condition_id: "003_detector_layers_(12,_20,_28)"
axis: "detector_layers"
value: "(12, 20, 28)"
is_default: false
swap_log_odds_shift: 0.5625
valid_answer_mass: 0.00058734294725582
p4: 1.9832293673971435e-06
p8: 0.0005853596958331764
repeated_bigram_fraction: 0.0
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
'<|im_start|>user\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
[' لش', '增添', ' food', ' кост', ' marker', ' decreases', '-j', ' Figure']
```

Unmodified donor readout:

```python
['三八', 'identité', ' memiliki', '带头作用', ' 한반', '장으로', '减轻', 'óricos']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they have **8 legs**. This distinguishes them
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | 'The'   | -0.068  | 0.933995 | +0.028            |
| 2      | 'Based' | -3.193  | 0.041037 | -0.472            |
| 3      | 'Most'  | -5.443  | 0.004325 | +0.153            |
| 4      | 'Sp'    | -5.693  | 0.003369 | -0.097            |
| 5      | 'To'    | -6.068  | 0.002315 | -0.347            |
| 6      | 'An'    | -6.068  | 0.002315 | +0.028            |
| 7      | '**'    | -6.318  | 0.001803 | -0.097            |
| 8      | 'There' | -6.818  | 0.001094 | +0.278            |
| 9      | 'First' | -7.193  | 0.000752 | +0.028            |
| 10     | 'That'  | -7.318  | 0.000663 | +0.278            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
