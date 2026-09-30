---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
reverse: true
swap_logits: false
plural: true
k: 32
strength: 1
prompt_slice: '-3:'
continuous: true
max_new_tokens: 32
seed: 0
donor_checkpoint: out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: skeleton
expected_answer: 'inside'
n_tokens: 32
answer_0: 'outside'
answer_1: 'inside'
answer_log_odds_shift: 0.0
answer_pair_mass: 3.7790068745380268e-06
r2: 0.032258064516129004
---
# Base

Input:
```text
"Fact: The skeleton of the animal that barks and is called man's best friend is on the "
```

Prefill readout: [' seventh', ' page', ' sixth', ' eighth', ' fifth', ' fourth', ' list', '第', '___', ' Guinness', ' ninth', ' Biology', ' Floor', ' Planet', ' Page', ' tenth', ' planet', ' Science', ' Seventh', ' second', ' nth', ' website', ' Museum', ' List', ' Plate', ' third', ' pages', ' Body', ' Earth', ' biology', ' Fifth', ' bones']

Generation (32 tokens):
```text
10th floor of the building.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the 
```

| token                    |    log p |          p |   delta log p |
|:-------------------------|---------:|-----------:|--------------:|
| 1                        | -1.14451 | 0.318381   |             0 |
| 2                        | -1.76951 | 0.170417   |             0 |
| 3                        | -2.14451 | 0.117126   |             0 |
| 4                        | -2.26951 | 0.103363   |             0 |
| 5                        | -2.51951 | 0.0804993  |             0 |
| 6                        | -2.95701 | 0.0519743  |             0 |
| 7                        | -3.20701 | 0.0404776  |             0 |
| 9                        | -3.33201 | 0.0357214  |             0 |
| 8                        | -3.45701 | 0.031524   |             0 |
| ........................ | -6.26951 | 0.00189316 |             0 |

Final-decode readout: [' floor', ' fifth', ' basement', ' tenth', ' seventh', ' ninth', ' sixth', ' hallway', ' fourth', ' upstairs', ' eighth', ' kitchen', ' third', ' bathroom', ' Floor', ' elevator', ' ceiling', ' hotel', ' lobby', ' Fifth', ' floors', ' downstairs', ' rooftop', ' bedroom', ' stairs', ' second', ' hospital', ' next', ' restaurant', ' door', ' mansion', ' same']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
