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
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: skeleton_body
expected_answer: ' inside'
n_tokens: 32
answer_0: ' outside'
answer_1: ' inside'
answer_log_odds_shift: 5.960464477539063e-08
answer_pair_mass: 0.5146476626396179
r2: 0.0
---
# norm-matched J donor projection

Input:
```text
'Fact: Relative to the rest of its body, the skeleton of the animal that spins webs is on the'
```

Prefill readout: ['____', ' ____', '___', ' ___', ' ______', ' side', ' ________', ' __', ' right', ' _____', ' left', '________', '_____', '__', ' underside', ' upper', ' lower', '_.', ' _.', ' LEFT', ' bones', ' abdomen', '__.', ' upside', ' bottom', ' outer', '_________', ' Left', ' __________________', ' bone', '_\\', ' sides']

Generation (32 tokens):
```text
 outside.
Question: Is the animal that spins webs on the outside?
Options:
A. Yes
B. No
Answer:

<think>


```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| outside | -1.09297 | 0.335218  |     -0.441811 |
| inside  | -1.71797 | 0.179429  |     -0.441811 |
| left    | -3.09297 | 0.0453669 |      1.43319  |
| right   | -3.34297 | 0.0353317 |      1.62069  |
| ______  | -3.78047 | 0.0228119 |      1.12069  |
| ground  | -3.84297 | 0.0214298 |      0.620689 |
| top     | -3.96797 | 0.0189117 |      1.93319  |
| side    | -4.03047 | 0.0177659 |      1.37069  |
| upper   | -4.03047 | 0.0177659 |      1.99569  |
| __      | -4.09297 | 0.0166895 |      1.12069  |

Final-decode readout: ['”**', '回答', '".**', '"**', '(**', ' **“', '**!', '）**', ' **.', '”.**', '’**', '**:', ';**', ')**', '**', '”**.', '”:', '解答', ' "**', '**”', '**-', '”**,', ' **„', ' **-', '**.', '==$', '"${', '==-', '!**', '-**', '】**', ' **【']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
