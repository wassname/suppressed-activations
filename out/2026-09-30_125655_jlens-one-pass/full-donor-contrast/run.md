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
prompt_slice: '-3:'
continuous: true
max_new_tokens: 32
seed: 0
donor_checkpoint: out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: skeleton_body
expected_answer: ' inside'
n_tokens: 32
answer_0: ' outside'
answer_1: ' inside'
answer_log_odds_shift: 0.6250000596046448
answer_pair_mass: 0.24421730637550354
r2: 0.06451612903225812
---
# full donor contrast

Input:
```text
'Fact: Relative to the rest of its body, the skeleton of the animal that spins webs is on the'
```

Prefill readout: ['____', ' ____', '___', ' __', ' ______', ' ___', ' ________', ' _____', '________', '__', '__.', '_____', ' __________________', '_.', '.__', ' bones', '____________', ' skeletal', ' abdomen', '_________', ' skull', ' _.', '.\\', ' bone', '.\\"', '._', '_\\', ' \\"', ' belly', '(__', ' position', '________________']

Generation (32 tokens):
```text
 left.
Question: Is the dog in the picture?
Options: A. Yes
Options: B. No
Answer:

<think>

</think>


```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| left    | -1.97784 | 0.138367  |      2.54832  |
| outside | -2.10284 | 0.122109  |     -1.45168  |
| inside  | -2.10284 | 0.122109  |     -0.826682 |
| right   | -2.85284 | 0.05768   |      2.11082  |
| top     | -3.66534 | 0.0255954 |      2.23582  |
| back    | -3.72784 | 0.0240446 |      2.98582  |
| head    | -3.72784 | 0.0240446 |      1.42332  |
| upper   | -3.79034 | 0.0225878 |      2.23582  |
| ground  | -3.79034 | 0.0225878 |      0.673318 |
| side    | -3.79034 | 0.0225878 |      1.61082  |

Final-decode readout: [' **', '  \n\n', ' Based', '\\n', '*\\', '\\"\\', ';**', '**', 'Based', '(**', 'Dog', '  \n\n\n', ' Dogs', '()\\', '<think>', '%\\', '</think>', ' \n\n', '狗', ' (**', '.\\', '  \n  \n', ' \n\n\n', '根据', '>\\', '...\\', '<|im_end|>', '\t\n\n', '\\")', '   \n\n', ' \n    \n', '  \n']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
