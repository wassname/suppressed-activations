---
condition_id: "009_rank_4"
axis: "rank"
value: "4"
is_default: false
swap_log_odds_shift: 2.6875
valid_answer_mass: 0.0001415392616763711
p4: 3.904400273313513e-06
p8: 0.00013763486640527844
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
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
'<|im_start|>user\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
[' факта', '在校园', ' 인프라', 'web']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, and all spiders have **8 legs**.

Therefore, the
```

| rank   | token   | log p   | p        | change in log p   |
|:-------|:--------|:--------|:---------|:------------------|
| 1      | 'The'   | -0.203  | 0.815946 | -0.107            |
| 2      | 'Based' | -2.203  | 0.110426 | +0.518            |
| 3      | 'There' | -3.953  | 0.019189 | +3.143            |
| 4      | 'To'    | -4.578  | 0.010271 | +1.143            |
| 5      | 'First' | -4.578  | 0.010271 | +2.643            |
| 6      | 'It'    | -5.328  | 0.004852 | +4.018            |
| 7      | '**'    | -5.453  | 0.004282 | +0.768            |
| 8      | 'Sp'    | -5.578  | 0.003779 | +0.018            |
| 9      | 'An'    | -5.828  | 0.002943 | +0.268            |
| 10     | 'This'  | -6.203  | 0.002023 | +1.643            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
