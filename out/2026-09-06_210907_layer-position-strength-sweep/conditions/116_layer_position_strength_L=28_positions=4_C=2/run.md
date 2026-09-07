---
condition_id: "116_layer_position_strength_L=28_positions=4_C=2"
axis: "layer_position_strength"
value: "L=28,positions=4,C=2"
is_default: false
swap_log_odds_shift: -0.125
valid_answer_mass: 0.2853638827800751
p4: 0.004013251047581434
p8: 0.28135064244270325
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/116_layer_position_strength_L=28_positions=4_C=2/run.md"
---

# 116_layer_position_strength_L=28_positions=4_C=2

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
  "intervention_positions": 4,
  "strength": 2.0,
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
[' spinning', ' spin', ' spins', '纺', 'ปั่น', ' Ủy', '.Sp', '-spin']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `116_layer_position_strength_L=28_positions=4_C=2`).

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal most commonly associated with spinning webs is the **spider
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.143  | 0.318812 | +0.078            |
| 2      | '**'     | -1.268  | 0.281351 | -0.047            |
| 3      | '8'      | -1.268  | 0.281351 | -0.047            |
| 4      | 'Fact'   | -2.643  | 0.071137 | +0.078            |
| 5      | 'Number' | -4.143  | 0.015873 | -0.047            |
| 6      | '###'    | -4.268  | 0.014008 | -0.047            |
| 7      | '4'      | -5.518  | 0.004013 | -0.172            |
| 8      | '1'      | -6.393  | 0.001673 | -0.047            |
| 9      | 'Answer' | -6.893  | 0.001015 | +0.078            |
| 10     | 'Eight'  | -6.893  | 0.001015 | -0.047            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
