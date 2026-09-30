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
answer_log_odds_shift: -0.12499994039535522
answer_pair_mass: 0.0843074768781662
r2: 0.032258064516129004
---
# norm-matched J donor projection

Input:
```text
'Fact: Relative to the rest of its body, the skeleton of the animal that spins webs is on the'
```

Prefill readout: [' ____', '____', '___', ' ___', ' __', ' ______', ' ________', ' _____', '__', '_____', ' left', '________', ' right', ' side', '_.', ' LEFT', ' _.', '__.', ' Left', ' __________________', '_________', '____________', ' _', '________________', ' RIGHT', ' upper', '_\\', ' bones', ' abdomen', '_', ' center', ' Right']

Generation (32 tokens):
```text
 left side.
Question: Is the animal that spins webs on the left side?
Options:
A. Yes
B. No
Answer:


```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| left    | -1.23516 | 0.290789  |       3.29101 |
| right   | -1.86016 | 0.155648  |       3.10351 |
| outside | -2.86016 | 0.0572598 |      -2.20899 |
| ______  | -3.23516 | 0.0393541 |       1.66601 |
| side    | -3.23516 | 0.0393541 |       2.16601 |
| same    | -3.48516 | 0.030649  |       2.16601 |
| inside  | -3.61016 | 0.0270476 |      -2.33399 |
| ____    | -3.73516 | 0.0238695 |       1.91601 |
| __      | -3.92266 | 0.0197885 |       1.29101 |
| top     | -4.04766 | 0.0174633 |       1.85351 |

Final-decode readout: ['____', '?\\', '  \n\n', '?', ' ____', '___', '\n\n', '_____', '？', '   \n\n', ' \n\n', '()?', ' ______', '?**', '  \n', '__', '_________', ' Answer', '________', '？**', '\\n', '.?', ' __', ' ___', '**?', '?:', '()', '   \n', '?(', '=?', ' _____', '?”']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
