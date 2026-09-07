---
condition_id: "057_layer_position_strength_L=20_positions=4_C=4"
axis: "layer_position_strength"
value: "L=20,positions=4,C=4"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.27406641840934753
p4: 0.004359407816082239
p8: 0.2697070240974426
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
first_answer: "8"
source_fact_preserved: true
readout_overlap: 0.0
log: "conditions/057_layer_position_strength_L=20_positions=4_C=4/run.md"
---

# 057_layer_position_strength_L=20_positions=4_C=4

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
  "intervention_layer": 20,
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
['\tspin', ' webView', ' веб', 'kab', ' webové', 'สปิน', ' fär', 'seh']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Measured intervention norms:

[Full diagnostic data](../../result.json) (`rows` → `057_layer_position_strength_L=20_positions=4_C=4`).

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class *Arachnida*, which
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.185  | 0.305618 | +0.036            |
| 2      | '**'     | -1.185  | 0.305618 | +0.036            |
| 3      | '8'      | -1.310  | 0.269707 | -0.089            |
| 4      | 'Fact'   | -2.685  | 0.068193 | +0.036            |
| 5      | 'Number' | -4.060  | 0.017242 | +0.036            |
| 6      | '###'    | -4.185  | 0.015216 | +0.036            |
| 7      | '4'      | -5.435  | 0.004359 | -0.089            |
| 8      | '1'      | -6.435  | 0.001604 | -0.089            |
| 9      | 'Eight'  | -6.685  | 0.001249 | +0.161            |
| 10     | 'Answer' | -6.810  | 0.001102 | +0.161            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
