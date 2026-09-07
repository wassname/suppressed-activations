---
condition_id: "149_layer_position_strength_L=32_positions=4_C=16"
axis: "layer_position_strength"
value: "L=32,positions=4,C=16"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.2995504140853882
p4: 0.0047647650353610516
p8: 0.29478564858436584
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "8"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/149_layer_position_strength_L=32_positions=4_C=16/run.md"
---

# 149_layer_position_strength_L=32_positions=4_C=16

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
  "intervention_layer": 32,
  "intervention_positions": 4,
  "strength": 16.0,
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
[' spinning', 'web', ' WEB', ' spin', ' atingir', ' spins', ' spiders', '-web']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `149_layer_position_strength_L=32_positions=4_C=16`).

Generation (32 tokens, verbatim):

```text
8

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is characterized by
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '8'      | -1.222  | 0.294786 | +0.000            |
| 2      | 'The'    | -1.222  | 0.294786 | +0.000            |
| 3      | '**'     | -1.222  | 0.294786 | +0.000            |
| 4      | 'Fact'   | -2.722  | 0.065776 | +0.000            |
| 5      | 'Number' | -4.097  | 0.016631 | +0.000            |
| 6      | '###'    | -4.222  | 0.014677 | +0.000            |
| 7      | '4'      | -5.347  | 0.004765 | +0.000            |
| 8      | '1'      | -6.347  | 0.001753 | +0.000            |
| 9      | 'Eight'  | -6.847  | 0.001063 | +0.000            |
| 10     | '6'      | -6.972  | 0.000938 | +0.000            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
