---
condition_id: "016_lexical_surface_pair=5_C=1"
axis: "lexical_surface"
value: "pair=5,C=1"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.2908090054988861
p4: 0.005230550654232502
p8: 0.2855784595012665
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/016_lexical_surface_pair=5_C=1/run.md"
---

# 016_lexical_surface_pair=5_C=1

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
  "intervention_layer": 1,
  "intervention_positions": "all",
  "strength": 1.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "pair_5",
  "lexical_divisor": 1
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
['ปั่น', '-spin', ' Ủy', 'Spin', ' Presents', 'seh', ' Spin', '\tspin']
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
| 1      | 'The'    | -1.128  | 0.323603 | +0.093            |
| 2      | '**'     | -1.253  | 0.285578 | -0.032            |
| 3      | '8'      | -1.253  | 0.285578 | -0.032            |
| 4      | 'Fact'   | -2.878  | 0.056234 | -0.157            |
| 5      | 'Number' | -4.128  | 0.016111 | -0.032            |
| 6      | '###'    | -4.253  | 0.014218 | -0.032            |
| 7      | '4'      | -5.253  | 0.005231 | +0.093            |
| 8      | '1'      | -6.378  | 0.001698 | -0.032            |
| 9      | 'Answer' | -6.878  | 0.001030 | +0.093            |
| 10     | 'Eight'  | -6.878  | 0.001030 | -0.032            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
