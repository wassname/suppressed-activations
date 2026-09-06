---
condition_id: "029_intervention_layer_19"
axis: "intervention_layer"
value: "19"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.22115644812583923
p4: 0.00397776672616601
p8: 0.21717868745326996
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/029_intervention_layer_19/run.md"
---

# 029_intervention_layer_19

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
  "intervention_layer": 19,
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
['Spin', '\tspin', ' веб', ' webové', ' webView', 'สปิน', ' HttpContext', ' mdi']
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
| 1      | 'The'    | -0.777  | 0.459767 | +0.444            |
| 2      | '**'     | -1.527  | 0.217179 | -0.306            |
| 3      | '8'      | -1.527  | 0.217179 | -0.306            |
| 4      | 'Fact'   | -2.902  | 0.054911 | -0.181            |
| 5      | '###'    | -4.027  | 0.017827 | +0.194            |
| 6      | 'Number' | -4.152  | 0.015732 | -0.056            |
| 7      | '4'      | -5.527  | 0.003978 | -0.181            |
| 8      | 'Answer' | -6.777  | 0.001140 | +0.194            |
| 9      | '6'      | -6.777  | 0.001140 | +0.194            |
| 10     | '1'      | -6.777  | 0.001140 | -0.431            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
