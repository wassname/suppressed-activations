---
condition_id: "041_intervention_layer_31"
axis: "intervention_layer"
value: "31"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.288085401058197
p4: 0.004582399968057871
p8: 0.283502995967865
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/041_intervention_layer_31/run.md"
---

# 041_intervention_layer_31

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
  "intervention_layer": 31,
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
[' spinning', 'web', ' spin', ' spins', '-web', '纺', '(web', 'ปั่น']
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
| 1      | 'The'    | -1.136  | 0.321251 | +0.086            |
| 2      | '**'     | -1.261  | 0.283503 | -0.039            |
| 3      | '8'      | -1.261  | 0.283503 | -0.039            |
| 4      | 'Fact'   | -2.761  | 0.063258 | -0.039            |
| 5      | 'Number' | -4.136  | 0.015994 | -0.039            |
| 6      | '###'    | -4.261  | 0.014115 | -0.039            |
| 7      | '4'      | -5.386  | 0.004582 | -0.039            |
| 8      | '1'      | -6.261  | 0.001910 | +0.086            |
| 9      | 'Eight'  | -6.761  | 0.001159 | +0.086            |
| 10     | 'Answer' | -6.886  | 0.001022 | +0.086            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
