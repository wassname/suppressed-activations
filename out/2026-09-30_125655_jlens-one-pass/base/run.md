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
expected_answer: ' outside'
n_tokens: 32
answer_0: ' outside'
answer_1: ' inside'
answer_log_odds_shift: 0.0
answer_pair_mass: 0.8005456924438477
r2: 0.032258064516129004
---
# Base

Input:
```text
'Fact: Relative to the rest of its body, the skeleton of the animal that spins webs is on the'
```

Prefill readout: [' underside', '___', '____', ' abdomen', ' ____', ' upside', ' ________', ' side', ' _____', '________', ' ___', ' ______', '_____', ' inside', ' outer', ' skull', ' __', ' outskirts', ' bones', ' dorsal', ' __________________', ' lower', ' downside', ' backbone', ' neck', '_.', ' _.', ' shell', ' belly', ' skeletal', ' right', ' left']

Generation (32 tokens):
```text
 outside.
Question: The skeleton of the animal that spins webs is on the outside relative to the rest of its body.
Is the question factually correct
```

| token     |     log p |          p |   delta log p |
|:----------|----------:|-----------:|--------------:|
| outside   | -0.651162 | 0.521439   |             0 |
| inside    | -1.27616  | 0.279106   |             0 |
| ground    | -4.46366  | 0.0115201  |             0 |
| left      | -4.52616  | 0.0108221  |             0 |
| underside | -4.83866  | 0.00791764 |             0 |
| ______    | -4.90116  | 0.00743793 |             0 |
| right     | -4.96366  | 0.00698729 |             0 |
| end       | -5.02616  | 0.00656395 |             0 |
| bottom    | -5.02616  | 0.00656395 |             0 |
| head      | -5.15116  | 0.00579267 |             0 |

Final-decode readout: ['?\\', '?”,', '?",', '()?', '?”', '”?', '?“', ' correct', ')?', '**?', '?**', '?...', ' accurate', '?*', '?):', 'correct', '?)', '?”.', '.?', '?[', '>?', '?', '?(', '"?', '正确的', '？”', '?</', '?"', ' Correct', 'accur', '?".', '正确']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
