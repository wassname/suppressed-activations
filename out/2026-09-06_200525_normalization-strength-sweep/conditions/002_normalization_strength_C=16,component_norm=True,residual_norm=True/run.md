---
condition_id: "002_normalization_strength_C=16,component_norm=True,residual_norm=True"
axis: "normalization_strength"
value: "C=16,component_norm=True,residual_norm=True"
is_default: false
swap_log_odds_shift: 3.875
valid_answer_mass: 2.3677925128140487e-05
p4: 1.0366751666879281e-05
p8: 1.3311173461261205e-05
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/002_normalization_strength_C=16,component_norm=True,residual_norm=True/run.md"
---

# 002_normalization_strength_C=16,component_norm=True,residual_norm=True

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
  "strength": 16.0,
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
['病気', '爸', '阴性', '生病了', '中药材', '(Database', ' большой', ' Genome']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
**Fact:** The number of legs on the animal that **builds** webs is **eight**.

**Explanation:**
The animal described is the **tar
```

| rank   | token      | log p   | p        | change in log p   |
|:-------|:-----------|:--------|:---------|:------------------|
| 1      | '**'       | -0.602  | 0.547766 | +0.620            |
| 2      | 'The'      | -1.727  | 0.177834 | -0.505            |
| 3      | '###'      | -1.977  | 0.138497 | +2.245            |
| 4      | 'Fact'     | -2.477  | 0.084003 | +0.245            |
| 5      | 'Based'    | -4.227  | 0.014597 | +4.432            |
| 6      | 'Here'     | -4.852  | 0.007813 | +4.870            |
| 7      | 'It'       | -5.477  | 0.004182 | +5.245            |
| 8      | 'There'    | -5.602  | 0.003691 | +2.995            |
| 9      | 'Actually' | -6.477  | 0.001539 | +3.745            |
| 10     | 'I'        | -6.727  | 0.001198 | +4.307            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
