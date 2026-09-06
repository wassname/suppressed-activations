---
condition_id: "004_detector_layers_(16,_24,_32)"
axis: "detector_layers"
value: "(16, 24, 32)"
is_default: false
swap_log_odds_shift: 0.0
valid_answer_mass: 0.20422488451004028
p4: 0.0032484817784279585
p8: 0.2009764015674591
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.125
log: "conditions/004_detector_layers_(16,_24,_32)/run.md"
---

# 004_detector_layers_(16,_24,_32)

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    16,
    24,
    32
  ],
  "readout_positions": 4,
  "rank": 8,
  "intervention_layer": 1,
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
[' simptom', 'でご', 'のレストラン', ' Добро', ' prefeit', ' Зи', ' aficion', '.toolStripButton']
```

Unmodified donor readout:

```python
[' kulinar', 'kontakt', '新', 'genesis', ' متاب', ' simptom', ' Territ', 'owment']
```

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class *Arachnida*, which
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | 'The'      | -1.105  | 0.331354 | +0.117            |
| 2      | '**'       | -1.105  | 0.331354 | +0.117            |
| 3      | '8'        | -1.605  | 0.200976 | -0.383            |
| 4      | 'Fact'     | -2.605  | 0.073935 | +0.117            |
| 5      | '###'      | -3.605  | 0.027199 | +0.617            |
| 6      | 'Number'   | -3.980  | 0.018694 | +0.117            |
| 7      | '4'        | -5.730  | 0.003248 | -0.383            |
| 8      | '1'        | -6.480  | 0.001534 | -0.133            |
| 9      | 'Complete' | -6.855  | 0.001055 | +0.367            |
| 10     | '#'        | -6.980  | 0.000931 | +0.242            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
