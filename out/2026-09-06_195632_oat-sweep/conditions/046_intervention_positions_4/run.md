---
condition_id: "046_intervention_positions_4"
axis: "intervention_positions"
value: "4"
is_default: false
swap_log_odds_shift: 0.8125004768371582
valid_answer_mass: 0.0005441676476038992
p4: 2.357064431635081e-06
p8: 0.0005418105865828693
repeated_bigram_fraction: 0.032258064516129004
generation_tokens: 32
first_token: "The"
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
'<|im_start|>user\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['-web', 'web', 'mmm', ' факта', '丝绸', '闸蟹', '在校园', '_rsp']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, and all spiders have **8 legs**.

Therefore, the
```

| rank   | token    | log p   | p        | change in log p   |
|:-------|:---------|:--------|:---------|:------------------|
| 1      | 'The'    | -0.146  | 0.864509 | -0.049            |
| 2      | 'Based'  | -2.396  | 0.091119 | +0.326            |
| 3      | 'There'  | -4.896  | 0.007479 | +2.201            |
| 4      | 'To'     | -5.146  | 0.005825 | +0.576            |
| 5      | 'Sp'     | -5.271  | 0.005141 | +0.326            |
| 6      | 'First'  | -5.396  | 0.004537 | +1.826            |
| 7      | '**'     | -5.896  | 0.002752 | +0.326            |
| 8      | 'An'     | -6.021  | 0.002428 | +0.076            |
| 9      | 'It'     | -6.396  | 0.001669 | +2.951            |
| 10     | 'Spider' | -6.521  | 0.001473 | +1.201            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
