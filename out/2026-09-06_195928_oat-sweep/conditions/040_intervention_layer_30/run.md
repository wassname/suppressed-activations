---
condition_id: "040_intervention_layer_30"
axis: "intervention_layer"
value: "30"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.2884780168533325
p4: 0.005188626702874899
p8: 0.2832894027233124
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/040_intervention_layer_30/run.md"
---

# 040_intervention_layer_30

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
  "intervention_layer": 30,
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
[' spinning', ' spin', ' spins', '纺', 'ปั่น', ' Ủy', '.Sp', '-spin']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal most commonly associated with spinning webs is the **spider
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.136  | 0.321009 | +0.085            |
| 2      | '**'     | -1.261  | 0.283289 | -0.040            |
| 3      | '8'      | -1.261  | 0.283289 | -0.040            |
| 4      | 'Fact'   | -2.761  | 0.063210 | -0.040            |
| 5      | 'Number' | -4.136  | 0.015982 | -0.040            |
| 6      | '###'    | -4.261  | 0.014104 | -0.040            |
| 7      | '4'      | -5.261  | 0.005189 | +0.085            |
| 8      | '1'      | -6.261  | 0.001909 | +0.085            |
| 9      | 'Answer' | -6.886  | 0.001022 | +0.085            |
| 10     | 'Eight'  | -6.886  | 0.001022 | -0.040            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
