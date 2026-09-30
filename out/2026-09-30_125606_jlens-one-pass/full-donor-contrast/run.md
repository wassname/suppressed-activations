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
answer_log_odds_shift: 3.375
answer_pair_mass: 0.5165567398071289
swap_log_odds_shift: 3.375
bare_answer_mass: 0.5165567398071289
r2: 0.12903225806451613
---
# full donor contrast

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: ['.\\', '____', '___', '.\\"', '\\"\\', '__.', '。\\', ').\\', '__', '\\"', ' claws', ' ____', ' __', '\\n', ' ___', ' spiders', ' ______', '.__', '爪子', ' paw', ' \\"', '?\\', '\\")', ' dogs', '.*', '\\""', '_________', ' animals', '\\_', '____________', '_.', ' Dogs']

Generation (32 tokens):
```text
4.
Question: What is the name of the animal that spins webs?
Answer: The animal that spins webs is a dog.
The answer is
```

|   token |    log p |          p |   delta log p |
|--------:|---------:|-----------:|--------------:|
|       4 | -1.08927 | 0.336462   |      1.78565  |
|       6 | -1.21427 | 0.296926   |      2.41065  |
|       8 | -1.71427 | 0.180095   |     -1.58935  |
|       2 | -2.46427 | 0.0850708  |      2.53565  |
|       1 | -3.08927 | 0.0455351  |      1.53565  |
|       0 | -3.83927 | 0.0215093  |      2.66065  |
|       3 | -4.08927 | 0.0167514  |      1.03565  |
|       5 | -4.71427 | 0.0089664  |      0.910649 |
|       7 | -5.33927 | 0.00479937 |      0.410649 |
|       9 | -6.08927 | 0.00226706 |      0.473149 |

Final-decode readout: [':\\"', ' answers', ' answer', ':\\', '____', '?\\', '正确答案', 'answer', ' correct', ' isn', ' ____', ':"', '-answer', '是否正确', '答案', '\\"\\', ' incorrect', '的答案', '.\\', '\\n', ':', '...\\', ' Answer', ' should', ':__', ' seems', '=\\"', 'correct', 'answers', ' was', '\\":', '\\"']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
