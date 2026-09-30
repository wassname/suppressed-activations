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
prompt_slice: '-3:'
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
answer_log_odds_shift: 6.374999523162842
answer_pair_mass: 0.6718761920928955
swap_log_odds_shift: 6.374999523162842
bare_answer_mass: 0.6718761920928955
r2: 0.06451612903225812
---
# full donor contrast

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: [' dogs', '.\\', '____', ' Dogs', ' canine', '___', 'dogs', '__', '.\\"', ' dog', '犬', '__.', '\\"\\', ' ____', ' pets', ' paw', 'dog', ' leash', '宠物', '狗', ' Dog', 'Dog', '\\"', ' __', '。\\', ' pet', '\\n', ').\\', ' animals', ' ___', ' ______', '狗的']

Generation (32 tokens):
```text
4.
Question: What is the name of the animal that spins the dog's name?
Options: A. A dog.
B. A cat
```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       4 | -0.423981 | 0.654436   |     2.45094   |
|       2 | -1.79898  | 0.165467   |     3.20094   |
|       1 | -2.79898  | 0.060872   |     1.82594   |
|       0 | -3.04898  | 0.0474072  |     3.45094   |
|       3 | -3.92398  | 0.0197623  |     1.20094   |
|       8 | -4.04898  | 0.0174401  |    -3.92406   |
|       6 | -4.04898  | 0.0174401  |    -0.424062  |
|       5 | -4.79898  | 0.00823814 |     0.825938  |
|       9 | -5.42398  | 0.00440956 |     1.13844   |
|       7 | -5.67398  | 0.00343417 |     0.0759382 |

Final-decode readout: [' dogs', ' dog', ' Dogs', ' pets', ' cats', ' Dog', ' animals', ' puppy', ' puppies', ' canine', 'dogs', ' Cats', 'dog', ' horses', ' wolves', ' Pets', ' pet', ' собаки', ' kenn', ' horse', ' Animals', '犬', ' sheep', ' cows', 'animals', ' pigs', ' cat', ' chickens', ' veterinary', ' veterinarian', ' Hunde', ' Puppy']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
