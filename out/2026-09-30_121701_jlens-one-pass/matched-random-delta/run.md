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
relation: legs
expected_answer: 'control'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: 0.625
answer_pair_mass: 0.8807305693626404
swap_log_odds_shift: 0.625
bare_answer_mass: 0.8807305693626404
r2: 0.12903225806451613
---
# matched-random delta

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '___', '爪子', ' humans', ' mammals', ' ears', ' dogs', ' canine', '四肢', ' tails', ' leash', ' Humans', ' animals', ' Dogs', '尾巴', 'dogs', ' teeth', '__.', ' furry', ' Gecko', ' ___', '__', ' human', ' limbs', ' Animals', ' pets', '____', ' mamm', '.\\', ' humanoid', ' Feet']

Generation (32 tokens):
```text
4.
Question: How many legs does the animal that barks and is called man's best friend have?
Answer: The animal that barks and
```

|   token |     log p |           p |   delta log p |
|--------:|----------:|------------:|--------------:|
|       4 | -0.131082 | 0.877146    |    -0.0730065 |
|       2 | -2.88108  | 0.0560741   |     1.42699   |
|       1 | -4.00608  | 0.0182046   |     0.426993  |
|       0 | -4.00608  | 0.0182046   |     0.926993  |
|       3 | -4.13108  | 0.0160655   |     0.926993  |
|       6 | -5.38108  | 0.00460284  |    -0.198007  |
|       8 | -5.63108  | 0.00358469  |    -0.698007  |
|       5 | -5.75608  | 0.00316348  |     0.426993  |
|       9 | -6.75608  | 0.00116378  |     0.301993  |
|       7 | -7.13108  | 0.000799853 |    -0.0730066 |

Final-decode readout: ['且具有', '并具有', '并且', ' &&', ' và', '且', '并能', ' has', ' are', ' refers', '.\\"', '且在', ',and', ' consists', '并被', 'และมี', '?\\', '...\\', ' belongs', '.\\', '.and', '且有', ' isn', ' и', '-and', ',is', 'และ', ':\\"', '_and', '&&', ' was', ' és']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
