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
decode_scale: 0.25
prompt_slice: '-1:'
continuous: true
steering_schedule: prompt and continuous decode
max_new_tokens: 32
seed: 0
donor_checkpoint: out/2026-09-30_133218_jlens-one-pass/donors.pt
donor_norm: 6.9019775390625
equal_donor_norm: true
relation: skeleton_body
expected_answer: 'control'
n_tokens: 32
answer_0: ' outside'
answer_1: ' inside'
answer_log_odds_shift: 0.6249998807907104
answer_pair_mass: 0.4120345115661621
r2: 0.0
---
# matched-random delta

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' upside', ' underside', ' lower', ' lowest', ' side', '___', ' upper', ' highest', ' bottom', ' abdomen', ' bones', ' ________', ' bone', ' ____', ' same', ' downside', ' ___', ' right', ' skull', '____', ' inside', ' _____', ' left', ' dorsal', ' middle', '________', ' ______', ' torso', '_____', '_.', ' opposite', ' neck']

Generation (32 tokens):
```text
 inside.
Question: Is the skeleton of the animal that barks and is called man's best friend on the inside or outside?
Options:
A
```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| inside  | -1.27352 | 0.279845  |     0.0928547 |
| outside | -2.02352 | 0.132189  |    -0.532145  |
| left    | -3.27352 | 0.0378729 |    -0.032145  |
| right   | -3.27352 | 0.0378729 |     0.280355  |
| ground  | -3.33602 | 0.0355783 |     0.280355  |
| bottom  | -3.77352 | 0.0229711 |     0.405355  |
| upper   | -3.89852 | 0.0202719 |     0.530355  |
| side    | -3.96102 | 0.0190437 |     0.280355  |
| lower   | -4.08602 | 0.016806  |     0.467855  |
| head    | -4.14852 | 0.0157878 |     0.280355  |

Final-decode readout: [' Options', '选项', ' Option', ' Answer', 'Options', 'Option', 'options', ' options', '[A', '-option', 'option', '-options', '選項', '<option', 'answer', ' option', ' OPTIONS', ':<', ' answer', '(A', ' Answers', '回答', ':(', '.options', '/options', 'Answer', '\tA', '.Options', ' OPTION', ' Choice', ':A', ':[']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
