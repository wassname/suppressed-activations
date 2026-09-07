---
condition_id: "103_layer_position_strength_L=26_positions=4_C=8"
axis: "layer_position_strength"
value: "L=26,positions=4,C=8"
is_default: false
swap_log_odds_shift: 0.25
valid_answer_mass: 0.28275105357170105
p4: 0.005748993717133999
p8: 0.2770020663738251
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/103_layer_position_strength_L=26_positions=4_C=8/run.md"
---

# 103_layer_position_strength_L=26_positions=4_C=8

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
  "intervention_layer": 26,
  "intervention_positions": 4,
  "strength": 8.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "detector",
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
[' spinning', 'web', ' spin', ' atingir', ' spins', ' spiders', '-web', '纺']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `103_layer_position_strength_L=26_positions=4_C=8`).

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal most commonly associated with spinning webs is the **spider
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.159  | 0.313884 | +0.063            |
| 2      | '**'     | -1.284  | 0.277002 | -0.062            |
| 3      | '8'      | -1.284  | 0.277002 | -0.062            |
| 4      | 'Fact'   | -2.534  | 0.079362 | +0.188            |
| 5      | 'Number' | -4.034  | 0.017708 | +0.063            |
| 6      | '###'    | -4.159  | 0.015627 | +0.063            |
| 7      | '4'      | -5.159  | 0.005749 | +0.188            |
| 8      | '1'      | -6.284  | 0.001866 | +0.063            |
| 9      | 'Answer' | -6.909  | 0.000999 | +0.063            |
| 10     | 'Eight'  | -7.034  | 0.000882 | -0.187            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
