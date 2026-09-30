---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
reverse: false
swap_logits: false
plural: true
k: 32
strength: 1
decode_scale: 1.0
prompt_slice: '-1:'
continuous: true
max_new_tokens: 32
seed: 0
donor_checkpoint: out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: legs
expected_answer: '4'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: 3.125
answer_pair_mass: 0.5047656297683716
swap_log_odds_shift: 3.125
bare_answer_mass: 0.5047656297683716
r2: 0.032258064516129004
---
# norm-matched J donor projection

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: ['___', '____', ' ___', '.\\', ' ____', ' ______', ' __', '\\"', ' dogs', '__', ' claws', ' paw', '__.', '_________', '\\n', '?\\', '.\\"', '________', ' animals', '\\"\\', ' ________', ' Dogs', ' _____', ' \\"', '爪子', '____________', 'dogs', '_____', '_.', ').\\', '\\_', '。\\']

Generation (32 tokens):
```text
6.
Question: How many legs does the animal that spins webs have?
Options:
A. 4
B. 6
C.
```

|   token |    log p |          p |   delta log p |
|--------:|---------:|-----------:|--------------:|
|       6 | -1.08178 | 0.33899    |      2.54313  |
|       4 | -1.20678 | 0.299158   |      1.66813  |
|       8 | -1.58178 | 0.205608   |     -1.45687  |
|       2 | -2.95678 | 0.0519858  |      2.04314  |
|       1 | -3.20678 | 0.0404866  |      1.41814  |
|       0 | -3.83178 | 0.0216709  |      2.66814  |
|       3 | -3.95678 | 0.0191245  |      1.16814  |
|       5 | -4.70678 | 0.00903378 |      0.918135 |
|       7 | -5.20678 | 0.00547927 |      0.543135 |
|       9 | -5.83178 | 0.00293284 |      0.730635 |

Final-decode readout: [' Unknown', ' unknown', ' Cannot', ' Depends', ' unspecified', ' Anything', ' Dogs', ' unsure', ' None', 'Unknown', ' Undefined', 'unknown', ' undefined', ' dogs', ' undecided', ' uncertain', ' Unsure', ' Something', '未知', ' Dog', ' indefinite', ' depends', ' Doesn', ' unclear', ' UNKNOWN', ' cannot', 'Cannot', ' anything', '不确定', ' dog', ' none', ' Nothing']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
