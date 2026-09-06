---
condition_id: "055_donor_position_offset_1"
axis: "donor_position_offset"
value: "1"
is_default: false
swap_log_odds_shift: 1.0
valid_answer_mass: 0.10096847265958786
p4: 0.004249533638358116
p8: 0.0967189371585846
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/055_donor_position_offset_1/run.md"
---

# 055_donor_position_offset_1

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
  "match_component_norm": true,
  "restore_residual_norm": true,
  "donor_position_offset": 1
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
['誇る', ' Bốn', '.DOM', 'ISA', '型号的', ' Allgemeine', '内容的真实性', ' luksus']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', 'amax', ' perro', ' NHÀ']
```

Generation (32 tokens, verbatim):

```text
**8**

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class Arachnida, which is
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | '**'     | -0.961  | 0.382531 | +0.261            |
| 2      | 'The'    | -1.086  | 0.337582 | +0.136            |
| 3      | '8'      | -2.336  | 0.096719 | -1.114            |
| 4      | 'Fact'   | -2.336  | 0.096719 | +0.386            |
| 5      | '###'    | -3.461  | 0.031400 | +0.761            |
| 6      | 'Number' | -4.086  | 0.016807 | +0.011            |
| 7      | '1'      | -4.836  | 0.007939 | +1.511            |
| 8      | '6'      | -5.086  | 0.006183 | +1.886            |
| 9      | '4'      | -5.461  | 0.004250 | -0.114            |
| 10     | '2'      | -6.211  | 0.002007 | +1.511            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
