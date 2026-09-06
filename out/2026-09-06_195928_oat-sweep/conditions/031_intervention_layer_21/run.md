---
condition_id: "031_intervention_layer_21"
axis: "intervention_layer"
value: "21"
is_default: false
swap_log_odds_shift: 0.125
valid_answer_mass: 0.28346481919288635
p4: 0.0050984579138457775
p8: 0.278366357088089
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/031_intervention_layer_21/run.md"
---

# 031_intervention_layer_21

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
  "intervention_layer": 21,
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
[' webView', ' веб', ' fär', ' HttpContext', 'må', ' pathMatch', 'SourceType', ' mdi']
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
| 1      | 'The'    | -1.154  | 0.315430 | +0.068            |
| 2      | '**'     | -1.279  | 0.278366 | -0.057            |
| 3      | '8'      | -1.279  | 0.278366 | -0.057            |
| 4      | 'Fact'   | -2.529  | 0.079753 | +0.193            |
| 5      | 'Number' | -4.154  | 0.015704 | -0.057            |
| 6      | '###'    | -4.279  | 0.013859 | -0.057            |
| 7      | '4'      | -5.279  | 0.005098 | +0.068            |
| 8      | '1'      | -6.404  | 0.001655 | -0.057            |
| 9      | 'Answer' | -6.779  | 0.001138 | +0.193            |
| 10     | 'Eight'  | -6.904  | 0.001004 | -0.057            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
