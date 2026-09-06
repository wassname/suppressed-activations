---
condition_id: "009_rank_4"
axis: "rank"
value: "4"
is_default: false
swap_log_odds_shift: 1.125
valid_answer_mass: 0.7933611273765564
p4: 0.07564655691385269
p8: 0.7177145481109619
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "8"
readout_overlap: 0.0
log: "conditions/009_rank_4/run.md"
---

# 009_rank_4

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
  "rank": 4,
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
'<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nComplete this fact with only the number.\n\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
[' laba', 'idité', 'må', '的场所']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達']
```

Generation (4 tokens, verbatim):

```text
8<|im_end|>
<|endoftext|>
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '8'       | -0.332  | 0.717715 | -0.280            |
| 2      | '6'       | -1.832  | 0.160144 | +2.845            |
| 3      | '4'       | -2.582  | 0.075647 | +0.845            |
| 4      | '1'       | -3.832  | 0.021673 | +2.720            |
| 5      | '2'       | -4.582  | 0.010238 | +3.095            |
| 6      | '3'       | -5.582  | 0.003766 | +2.345            |
| 7      | '<think>' | -5.957  | 0.002588 | -0.155            |
| 8      | '0'       | -6.207  | 0.002016 | +2.282            |
| 9      | '5'       | -6.457  | 0.001570 | +1.970            |
| 10     | '7'       | -6.957  | 0.000952 | +1.407            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
