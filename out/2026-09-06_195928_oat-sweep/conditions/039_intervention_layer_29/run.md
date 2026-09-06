---
condition_id: "039_intervention_layer_29"
axis: "intervention_layer"
value: "29"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.2881547808647156
p4: 0.004583501257002354
p8: 0.2835712730884552
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/039_intervention_layer_29/run.md"
---

# 039_intervention_layer_29

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
  "intervention_layer": 29,
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
[' spinning', ' spin', ' spins', '纺', 'ปั่น', '.Sp', '-spin', ' spun']
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
| 1      | 'The'    | -1.135  | 0.321328 | +0.086            |
| 2      | '**'     | -1.260  | 0.283571 | -0.039            |
| 3      | '8'      | -1.260  | 0.283571 | -0.039            |
| 4      | 'Fact'   | -2.760  | 0.063273 | -0.039            |
| 5      | 'Number' | -4.135  | 0.015998 | -0.039            |
| 6      | '###'    | -4.260  | 0.014118 | -0.039            |
| 7      | '4'      | -5.385  | 0.004584 | -0.039            |
| 8      | '1'      | -6.385  | 0.001686 | -0.039            |
| 9      | 'Answer' | -6.885  | 0.001023 | +0.086            |
| 10     | 'Eight'  | -6.885  | 0.001023 | -0.039            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
