---
condition_id: "010_normalization_strength_C=4,component_norm=False,residual_norm=True"
axis: "normalization_strength"
value: "C=4,component_norm=False,residual_norm=True"
is_default: false
swap_log_odds_shift: -0.25
valid_answer_mass: 0.16751007735729218
p4: 0.0020824274979531765
p8: 0.16542765498161316
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/010_normalization_strength_C=4,component_norm=False,residual_norm=True/run.md"
---

# 010_normalization_strength_C=4,component_norm=False,residual_norm=True

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
  "strength": 4.0,
  "match_component_norm": false,
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
['盐酸', 'må', ' laba', ' Infant', ' webView', 'ränkt', '_keeper', ' Urbano']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class *Arachnida*, which
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -0.924  | 0.396840 | +0.297            |
| 2      | 'The'    | -1.424  | 0.240696 | -0.203            |
| 3      | '8'      | -1.799  | 0.165428 | -0.578            |
| 4      | 'Fact'   | -2.049  | 0.128835 | +0.672            |
| 5      | 'Number' | -3.924  | 0.019758 | +0.172            |
| 6      | '###'    | -3.924  | 0.019758 | +0.297            |
| 7      | '6'      | -4.799  | 0.008236 | +2.172            |
| 8      | 'Eight'  | -5.924  | 0.002674 | +0.922            |
| 9      | '1'      | -6.174  | 0.002082 | +0.172            |
| 10     | '4'      | -6.174  | 0.002082 | -0.828            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
