---
condition_id: "010_rank_16"
axis: "rank"
value: "16"
is_default: false
swap_log_odds_shift: 2.125
valid_answer_mass: 0.49317896366119385
p4: 0.10983102023601532
p8: 0.3833479583263397
repeated_bigram_fraction: 0.0
generation_tokens: 4
first_token: "4"
readout_overlap: 0.0
log: "conditions/010_rank_16/run.md"
---

# 010_rank_16

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
  "rank": 16,
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
[' När', '(Bundle', ' Ponadto', 'Islam', '_Begin', ' Bố', 'urdy', '的场所', ' enseignants', ' sprzedaży', 'љи', 'かったので', ' Allgemeine', 'Force', '伊斯兰', ' responseData']
```

Unmodified donor readout:

```python
[' собаки', ' Hunde', 'compan', '友達', ' Austr', ' perro', 'amax', ' NHÀ', '契', 'iht', 'friends', '录像', '吠', 'ạch', '_gold', '레이션']
```

Generation (4 tokens, verbatim):

```text
4<|im_end|>
<|endoftext|>
```

| rank   | token     | log p   | p        | change in log p   |
|:-------|:----------|:--------|:---------|:------------------|
| 1      | '8'       | -0.959  | 0.383348 | -0.907            |
| 2      | '6'       | -1.334  | 0.263471 | +3.343            |
| 3      | '4'       | -2.209  | 0.109831 | +1.218            |
| 4      | '1'       | -2.459  | 0.085536 | +4.093            |
| 5      | '2'       | -2.834  | 0.058788 | +4.843            |
| 6      | '0'       | -3.459  | 0.031467 | +5.030            |
| 7      | '3'       | -3.584  | 0.027770 | +4.343            |
| 8      | '5'       | -4.584  | 0.010216 | +3.843            |
| 9      | 'The'     | -5.209  | 0.005468 | +4.030            |
| 10     | '<think>' | -5.209  | 0.005468 | +0.593            |

TODO validate: semantic replacement requires a donor-like post-intervention readout and
selective transfer beyond this development prompt.

-- Codex/gpt-5.6-sol
