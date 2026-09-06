---
condition_id: "024_intervention_layer_14"
axis: "intervention_layer"
value: "14"
is_default: false
swap_log_odds_shift: 0.625
valid_answer_mass: 0.11462291330099106
p4: 0.003359853057190776
p8: 0.11126305907964706
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/024_intervention_layer_14/run.md"
---

# 024_intervention_layer_14

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
  "intervention_layer": 14,
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
[' Presents', '\tspin', 'Spin', 'ปั่น', '哈密', 'kab', '领头羊', ' laba']
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

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | 'The'      | -0.946  | 0.388346 | +0.276            |
| 2      | '**'       | -1.071  | 0.342714 | +0.151            |
| 3      | '8'        | -2.196  | 0.111263 | -0.974            |
| 4      | 'Fact'     | -2.571  | 0.076470 | +0.151            |
| 5      | '###'      | -3.321  | 0.036122 | +0.901            |
| 6      | 'Number'   | -3.821  | 0.021909 | +0.276            |
| 7      | '4'        | -5.696  | 0.003360 | -0.349            |
| 8      | 'Complete' | -5.946  | 0.002617 | +1.276            |
| 9      | '1'        | -6.446  | 0.001587 | -0.099            |
| 10     | 'Answer'   | -6.571  | 0.001401 | +0.401            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
