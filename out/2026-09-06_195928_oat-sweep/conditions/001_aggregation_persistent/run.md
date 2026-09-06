---
condition_id: "001_aggregation_persistent"
axis: "aggregation"
value: "persistent"
is_default: false
swap_log_odds_shift: 0.25
valid_answer_mass: 0.058179162442684174
p4: 0.0011829192517325282
p8: 0.05699624493718147
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
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
'<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete the fact with the number first, then explain your answer.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['emiş', ' miejs', '取締', ' polskich', ' Estatal', ' localização', 'тры', ' آهن']
```

Unmodified donor readout:

```python
[' Emas', '口臭', 'dach', 'しら', 'ToolStrip', 'enso', ' Kepolisian', 'acqu']
```

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal most famous for spinning webs is the **spider**.
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | 'The'      | -0.615  | 0.540765 | +0.607            |
| 2      | '**'       | -1.490  | 0.225425 | -0.268            |
| 3      | 'Fact'     | -2.115  | 0.120661 | +0.607            |
| 4      | '8'        | -2.865  | 0.056996 | -1.643            |
| 5      | 'Number'   | -3.740  | 0.023760 | +0.357            |
| 6      | '###'      | -4.240  | 0.014411 | -0.018            |
| 7      | 'Complete' | -5.865  | 0.002838 | +1.357            |
| 8      | 'Eight'    | -6.365  | 0.001721 | +0.482            |
| 9      | 'Answer'   | -6.365  | 0.001721 | +0.607            |
| 10     | '4'        | -6.740  | 0.001183 | -1.393            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
