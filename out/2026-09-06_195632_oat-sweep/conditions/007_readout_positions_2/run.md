---
condition_id: "007_readout_positions_2"
axis: "readout_positions"
value: "2"
is_default: false
swap_log_odds_shift: 0.75
valid_answer_mass: 0.00025091288262046874
p4: 1.021250000121654e-06
p8: 0.00024989162920974195
repeated_bigram_fraction: 0.0
generation_tokens: 32
first_token: "The"
readout_overlap: 0.0
log: "conditions/007_readout_positions_2/run.md"
---

# 007_readout_positions_2

Resolved config:

```json
{
  "aggregation": "union",
  "detector_layers": [
    23,
    25,
    32
  ],
  "readout_positions": 2,
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
'<|im_start|>user\nFact: The number of legs on the animal that spins webs is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n'
```

Donor input (`repr`):

```python
"<|im_start|>user\nFact: The number of legs on the animal that barks and is called man's best friend is <|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
```

Readout after intervention:

```python
['web', '-web', 'mmm', '_DM', 'Integrated', '网页', '-cancel', '资讯网']
```

Unmodified donor readout:

```python
['Dog', '狗粮', 'dog', ' собаки', 'สุนัข', 'DOG', ' Dog', ' chiens']
```

Generation (32 tokens, verbatim):

```text
The animal that spins webs is the **spider**.

Spiders are arachnids, which means they belong to a class of animals characterized by having
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | 'The'     | -0.107  | 0.898541 | -0.011            |
| 2      | 'Based'   | -2.482  | 0.083577 | +0.239            |
| 3      | 'Sp'      | -5.607  | 0.003672 | -0.011            |
| 4      | 'An'      | -6.107  | 0.002227 | -0.011            |
| 5      | 'To'      | -6.107  | 0.002227 | -0.386            |
| 6      | '**'      | -6.232  | 0.001966 | -0.011            |
| 7      | '<think>' | -6.982  | 0.000928 | +0.489            |
| 8      | 'Animal'  | -7.482  | 0.000563 | -0.386            |
| 9      | 'There'   | -7.607  | 0.000497 | -0.511            |
| 10     | 'Most'    | -7.732  | 0.000439 | -2.136            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
