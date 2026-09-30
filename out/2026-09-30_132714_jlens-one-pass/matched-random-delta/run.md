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
decode_scale: 1.0
prompt_slice: '-1:'
continuous: true
max_new_tokens: 32
seed: 0
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: legs
expected_answer: 'control'
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: -0.125
answer_pair_mass: 0.9154932498931885
swap_log_odds_shift: -0.125
bare_answer_mass: 0.9154932498931885
r2: 0.12903225806451613
---
# matched-random delta

Input:
```text
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Prefill readout: [' paw', ' claws', '___', ' mammals', '爪子', '四肢', ' ears', ' humans', ' animals', ' dogs', ' canine', ' tails', '__.', '__', ' leash', '尾巴', ' Gecko', ' Dogs', ' Animals', ' ___', ' teeth', 'dogs', ' limbs', '____', ' Humans', ' furry', ' mamm', '.\\', ' humanoid', ' bones', '四条', '两只']

Generation (32 tokens):
```text
4.
Question: How many legs does the animal that barks and is called man's best friend have?
Answer: The animal that barks and
```

|   token |      log p |           p |   delta log p |
|--------:|-----------:|------------:|--------------:|
|       4 | -0.0969068 | 0.907641    |    -0.0388313 |
|       2 | -3.47191   | 0.0310578   |     0.836169  |
|       1 | -3.97191   | 0.0188375   |     0.461169  |
|       0 | -4.34691   | 0.0129468   |     0.586169  |
|       3 | -4.59691   | 0.010083    |     0.461169  |
|       8 | -4.84691   | 0.00785263  |     0.0861688 |
|       6 | -5.22191   | 0.00539703  |    -0.0388312 |
|       5 | -5.84691   | 0.00288882  |     0.336169  |
|       9 | -6.84691   | 0.00106274  |     0.211169  |
|       7 | -6.97191   | 0.000937863 |     0.0861688 |

Final-decode readout: ['且具有', '并具有', '并且', ' &&', ' và', '且', '并能', ' has', ' are', '.\\"', ' refers', '且在', ',and', '并被', 'และมี', '且有', '.and', '...\\', ' и', ' belongs', '?\\', '.\\', ' consists', ' isn', '-and', ',is', 'และ', '&&', '_and', '并保持', ':\\"', ' és']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
