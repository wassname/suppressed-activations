---
condition_id: "046_intervention_positions_4"
axis: "intervention_positions"
value: "4"
is_default: false
swap_log_odds_shift: 0.3750002384185791
valid_answer_mass: 0.17902244627475739
p4: 0.004113466013222933
p8: 0.17490898072719574
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "**"
readout_overlap: 0.0
log: "conditions/046_intervention_positions_4/run.md"
---

# 046_intervention_positions_4

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
  "intervention_positions": 4,
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
['的场所', ' Satgas', '什么都没有', '_human', 'اطر', '犹太人', 'idité', 'くださ']
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
| 1      | '**'     | -1.118  | 0.326773 | +0.103            |
| 2      | 'The'    | -1.118  | 0.326773 | +0.103            |
| 3      | '8'      | -1.743  | 0.174909 | -0.522            |
| 4      | 'Fact'   | -2.618  | 0.072913 | +0.103            |
| 5      | '6'      | -3.368  | 0.034442 | +3.603            |
| 6      | 'Number' | -3.993  | 0.018435 | +0.103            |
| 7      | '###'    | -4.243  | 0.014357 | -0.022            |
| 8      | '1'      | -4.868  | 0.007685 | +1.478            |
| 9      | '4'      | -5.493  | 0.004113 | -0.147            |
| 10     | 'Eight'  | -5.743  | 0.003204 | +1.103            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
