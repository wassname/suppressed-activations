---
condition_id: "030_intervention_layer_20"
axis: "intervention_layer"
value: "20"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.28235164284706116
p4: 0.004491196013987064
p8: 0.2778604328632355
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/030_intervention_layer_20/run.md"
---

# 030_intervention_layer_20

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
['\tspin', ' webView', ' веб', ' webové', 'kab', ' fär', 'สปิน', ' HttpContext']
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
| 1      | 'The'    | -1.156  | 0.314857 | +0.066            |
| 2      | '**'     | -1.281  | 0.277860 | -0.059            |
| 3      | '8'      | -1.281  | 0.277860 | -0.059            |
| 4      | 'Fact'   | -2.531  | 0.079608 | +0.191            |
| 5      | 'Number' | -4.031  | 0.017763 | +0.066            |
| 6      | '###'    | -4.281  | 0.013834 | -0.059            |
| 7      | '4'      | -5.406  | 0.004491 | -0.059            |
| 8      | '1'      | -6.406  | 0.001652 | -0.059            |
| 9      | 'Answer' | -6.781  | 0.001136 | +0.191            |
| 10     | 'Eight'  | -6.781  | 0.001136 | +0.066            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
