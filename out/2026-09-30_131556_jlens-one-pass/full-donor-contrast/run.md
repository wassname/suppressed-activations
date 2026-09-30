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
donor_checkpoint: out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: skeleton_body
expected_answer: ' outside'
n_tokens: 32
answer_0: ' outside'
answer_1: ' inside'
answer_log_odds_shift: 0.25
answer_pair_mass: 0.4490574598312378
r2: 0.0
---
# full donor contrast

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: ['_____', ' ________', '________', '___', ' _____', ' ___', ' underside', '_________', ' upside', ' abdomen', '________________', ' spider', '＿＿', ' __________________', ' ____', ' ______', '____________', '\\xc', '_\\', ' _.', '____', ' highest', ' Spider', '_.', ' outskirts', ' lowest', '__.', ' middle', ' __________________________________', ' side', '＿', ' dors']

Generation (32 tokens):
```text
 inside.
Question: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the inside
```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| inside  | -1.32373 | 0.266141  |     0.0426462 |
| outside | -1.69873 | 0.182916  |    -0.207354  |
| ground  | -3.32373 | 0.0360183 |     0.292646  |
| side    | -3.63623 | 0.0263516 |     0.605146  |
| surface | -3.69873 | 0.024755  |     0.105146  |
| right   | -3.82373 | 0.0218462 |    -0.269854  |
| left    | -3.88623 | 0.0205226 |    -0.644854  |
| same    | -3.94873 | 0.0192792 |     0.167646  |
| floor   | -4.07373 | 0.0170138 |     0.667646  |
| dorsal  | -4.07373 | 0.0170138 |     1.29265   |

Final-decode readout: [' ________', ' ___', '________', ' _____', '_____', ' **(', ' __________________', ' **[', '___', ' ______', '_________', '________________', ' __', ' ____', ' **-', '____________', '**(', ' _(', ' __________________________________', ' **+', ' **“', '_[', ' _.', ' **.', '**?', ' **「', '＿＿', ' **', '____', '...**', '-**', ' inside']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
