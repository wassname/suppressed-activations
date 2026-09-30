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
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-09-30_133218_jlens-one-pass/donors.pt
donor_norm: 6.9019775390625
equal_donor_norm: true
relation: legs
expected_answer: '4'
n_tokens: 29
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: 2.25
answer_pair_mass: 0.539240837097168
swap_log_odds_shift: 2.25
bare_answer_mass: 0.539240837097168
r2: 0.0
---
# norm-matched J donor projection

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: ['____', '.\\', '___', '?\\', ' claws', '\\"', '__.', ' ____', '\\"\\', ' ___', ' ______', ').\\', '。\\', ' paw', '_________', '爪子', '\\n', '.\\"', '__', '\\")', '________', '_.', '____________', '\\""', '...\\', ' __', '后腿', '_____', '________________', '__)', '\\_', '四肢']

Generation (29 tokens):
```text
6.
Question: How many legs does the animal that spins webs have?
Answer:
A:

<think>

</think>

6<|endoftext|>
```

|   token |    log p |          p |   delta log p |
|--------:|---------:|-----------:|--------------:|
|       6 | -0.96667 | 0.380347   |     2.65825   |
|       8 | -1.09167 | 0.335655   |    -0.966751  |
|       4 | -1.59167 | 0.203585   |     1.28325   |
|       1 | -3.71667 | 0.0243148  |     0.908249  |
|       2 | -3.71667 | 0.0243148  |     1.28325   |
|       3 | -4.59167 | 0.0101359  |     0.533249  |
|       0 | -4.96667 | 0.00696631 |     1.53325   |
|       5 | -5.21667 | 0.00542537 |     0.408249  |
|       7 | -5.59167 | 0.0037288  |     0.158249  |
|       9 | -6.46667 | 0.00155439 |     0.0957494 |

Final-decode readout: ['<|endoftext|>', '<|im_end|>', '**', '</think>', '  \n\n', '\n\n', ' \n\n', '<think>', '**.', '.', '\\n', '\n   \n', '\t\n\n', '\\', '\\")', '<|file_sep|>', '  \n', '</', '  \n\n\n', '.\\', '\t  \n', '**!', '<|im_start|>', '\\.', '.**', '\\"', '**。', '!**', '。', '   \n\n', '**;', '\n\n\n']

Coverage: 29 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
