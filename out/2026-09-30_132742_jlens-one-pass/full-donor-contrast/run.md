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
answer_log_odds_shift: 1.1920928955078125e-07
answer_pair_mass: 0.6608991622924805
r2: 0.0
---
# full donor contrast

Input:
```text
'Fact: Relative to the rest of its body, the skeleton of the animal that spins webs is on the'
```

Prefill readout: ['____', ' ____', '___', ' ______', ' __', ' ___', ' ________', '__', ' _____', '________', '__.', '_____', ' bones', ' side', '_.', ' underside', ' abdomen', ' __________________', ' lower', '____________', ' upper', '_\\', ' _.', ' skull', ' skeletal', ' bone', '.__', '(__', ' upside', '_________', ' right', ' left']

Generation (32 tokens):
```text
 outside.
Question: Does the animal that spins webs have a skeleton on the outside?
Options:
A. Yes
B. No
Answer:
```

| token   |     log p |         p |   delta log p |
|:--------|----------:|----------:|--------------:|
| outside | -0.842855 | 0.43048   |     -0.191692 |
| inside  | -1.46785  | 0.230419  |     -0.191692 |
| left    | -3.84285  | 0.0214323 |      0.683307 |
| end     | -4.03035  | 0.017768  |      0.995807 |
| ______  | -4.15535  | 0.0156802 |      0.745807 |
| ground  | -4.21785  | 0.0147302 |      0.245807 |
| upper   | -4.34285  | 0.0129994 |      1.68331  |
| top     | -4.46785  | 0.0114719 |      1.43331  |
| far     | -4.53035  | 0.0107768 |      1.37081  |
| side    | -4.53035  | 0.0107768 |      0.870807 |

Final-decode readout: [':\\"', ':', ':\\', '：', ':__', ':**', '.:', ':*', ':"', '____', '：**', ':`', ':<', ':")', ':_', '”:', '?:', '：“', ':&', ':\\\\', '\\":', ':A', '_:', ':(', '__:', '():', ':",', ':?', '?\\', '*:', ':".', ':)']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
