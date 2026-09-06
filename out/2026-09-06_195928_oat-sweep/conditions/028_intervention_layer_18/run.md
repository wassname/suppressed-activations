---
condition_id: "028_intervention_layer_18"
axis: "intervention_layer"
value: "18"
is_default: false
swap_log_odds_shift: 0.25
valid_answer_mass: 0.21420776844024658
p4: 0.004355347249656916
p8: 0.2098524272441864
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/028_intervention_layer_18/run.md"
---

# 028_intervention_layer_18

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
  "intervention_layer": 18,
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
['Spin', '\tspin', 'ปั่น', '哈密', 'kab', '旋', ' Presents', ' fär']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal most famous for spinning webs is the **spider**.
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.811  | 0.444258 | +0.410            |
| 2      | '**'     | -1.436  | 0.237794 | -0.215            |
| 3      | '8'      | -1.561  | 0.209852 | -0.340            |
| 4      | 'Fact'   | -2.811  | 0.060124 | -0.090            |
| 5      | '###'    | -4.061  | 0.017226 | +0.160            |
| 6      | 'Number' | -4.311  | 0.013415 | -0.215            |
| 7      | '4'      | -5.436  | 0.004355 | -0.090            |
| 8      | '1'      | -6.561  | 0.001414 | -0.215            |
| 9      | '6'      | -6.936  | 0.000972 | +0.035            |
| 10     | 'Answer' | -6.936  | 0.000972 | +0.035            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
