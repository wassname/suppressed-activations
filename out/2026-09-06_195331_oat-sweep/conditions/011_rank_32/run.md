---
condition_id: "011_rank_32"
axis: "rank"
value: "32"
is_default: false
swap_log_odds_shift: 2.375
valid_answer_mass: 0.4196554124355316
p4: 0.1128627359867096
p8: 0.306792676448822
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "6"
readout_overlap: 0.0
log: "conditions/011_rank_32/run.md"
---

# 011_rank_32

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
  "rank": 32,
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
[' Ponadto', '满怀', ' эконом', '伊斯兰', ' состава', 'más', ' Azienda', 'urdy', 'Browse', 'έ', '单元的', ' enseignants', '更新时间', 'NEG', '상황', '中国文化', ' responseData', 'とのこと', '_multiplier', '电脑上', '(Bundle', '尽是', '年春节', ' DISCLAIMED', ' ബ', 'affer', ' islam', ' passiert', '来的时候', '_Begin', 'ツール', ' voller']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', ' perro', 'amax', ' NHÀ', '契', 'iht', 'friends', '录像', '吠', 'ạch', '_gold', '레이션', '统战部', 'Overlay', ' DISCLAIM', '村', '的祝福', ' Тов', '粗糙', 'สุนัข', 'Austr', '省份', ' pupper', '디지털', ' Stuttgart', ' perros', ' Más', 'qualification']
```

Generation (4 tokens, verbatim):

```text
6<|im_end|>
<|endoftext|>
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '6'       | -0.932  | 0.393930 | +3.745            |
| 2      | '8'       | -1.182  | 0.306793 | -1.130            |
| 3      | '4'       | -2.182  | 0.112863 | +1.245            |
| 4      | '1'       | -2.557  | 0.077569 | +3.995            |
| 5      | '2'       | -3.182  | 0.041520 | +4.495            |
| 6      | '0'       | -3.807  | 0.022224 | +4.682            |
| 7      | '3'       | -3.932  | 0.019613 | +3.995            |
| 8      | '<think>' | -5.057  | 0.006367 | +0.745            |
| 9      | '5'       | -5.182  | 0.005619 | +3.245            |
| 10     | 'The'     | -6.182  | 0.002067 | +3.057            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
