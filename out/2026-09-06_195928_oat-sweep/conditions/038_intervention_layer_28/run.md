---
condition_id: "038_intervention_layer_28"
axis: "intervention_layer"
value: "28"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.29997122287750244
p4: 0.004218683578073978
p8: 0.29575252532958984
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
readout_overlap: 0.0
log: "conditions/038_intervention_layer_28/run.md"
---

# 038_intervention_layer_28

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
  "intervention_layer": 28,
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
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.218  | 0.295753 | +0.003            |
| 2      | 'The'    | -1.218  | 0.295753 | +0.003            |
| 3      | '**'     | -1.218  | 0.295753 | +0.003            |
| 4      | 'Fact'   | -2.718  | 0.065991 | +0.003            |
| 5      | 'Number' | -4.093  | 0.016685 | +0.003            |
| 6      | '###'    | -4.343  | 0.012994 | -0.122            |
| 7      | '4'      | -5.468  | 0.004219 | -0.122            |
| 8      | '1'      | -6.343  | 0.001759 | +0.003            |
| 9      | 'Answer' | -6.968  | 0.000941 | +0.003            |
| 10     | 'Eight'  | -6.968  | 0.000941 | -0.122            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
