---
condition_id: "087_layer_position_strength_L=24_positions=4_C=4"
axis: "layer_position_strength"
value: "L=24,positions=4,C=4"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.2858624756336212
p4: 0.004547040909528732
p8: 0.2813154458999634
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.75
log: "conditions/087_layer_position_strength_L=24_positions=4_C=4/run.md"
---

# 087_layer_position_strength_L=24_positions=4_C=4

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
  "intervention_layer": 24,
  "intervention_positions": 4,
  "strength": 4.0,
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
['compan', '友達', ' NHÀ', ' собаки', ' cão', 'amax', ' Austr', ' собака']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `087_layer_position_strength_L=24_positions=4_C=4`).

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal most commonly associated with spinning webs is the **spider
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.143  | 0.318772 | +0.078            |
| 2      | '**'     | -1.268  | 0.281315 | -0.047            |
| 3      | '8'      | -1.268  | 0.281315 | -0.047            |
| 4      | 'Fact'   | -2.643  | 0.071128 | +0.078            |
| 5      | 'Number' | -4.143  | 0.015871 | -0.047            |
| 6      | '###'    | -4.268  | 0.014006 | -0.047            |
| 7      | '4'      | -5.393  | 0.004547 | -0.047            |
| 8      | '1'      | -6.393  | 0.001673 | -0.047            |
| 9      | 'Answer' | -6.893  | 0.001015 | +0.078            |
| 10     | 'Eight'  | -6.893  | 0.001015 | -0.047            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
