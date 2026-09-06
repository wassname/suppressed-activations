---
condition_id: "023_lexical_surface_pair=6_C=8"
axis: "lexical_surface"
value: "pair=6,C=8"
is_default: false
swap_log_odds_shift: 0.3749997615814209
valid_answer_mass: 0.1861523985862732
p4: 0.004277291242033243
p8: 0.1818751096725464
repeated_bigram_fraction: 0.12903225806451613
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/023_lexical_surface_pair=6_C=8/run.md"
---

# 023_lexical_surface_pair=6_C=8

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
  "strength": 8.0,
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 0,
  "lexical_forms": "pair_6",
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
['Spin', '-spin', '\tspin', ' Spin', 'spin', '_spin', ' Presents', 'seh']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
The number of legs on the animal that spins webs is **8**.

**Explanation:**
The animal that spins webs is the **spider**. Spiders
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -1.079  | 0.339787 | +0.142            |
| 2      | '**'     | -1.204  | 0.299861 | +0.017            |
| 3      | '8'      | -1.704  | 0.181875 | -0.483            |
| 4      | 'Fact'   | -2.079  | 0.125001 | +0.642            |
| 5      | 'Number' | -4.079  | 0.016917 | +0.017            |
| 6      | '###'    | -4.329  | 0.013175 | -0.108            |
| 7      | '4'      | -5.454  | 0.004277 | -0.108            |
| 8      | '6'      | -5.454  | 0.004277 | +1.517            |
| 9      | '1'      | -6.329  | 0.001783 | +0.017            |
| 10     | 'Eight'  | -6.579  | 0.001389 | +0.267            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
