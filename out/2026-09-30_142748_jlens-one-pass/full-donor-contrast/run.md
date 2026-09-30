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
expected_answer: ' outside'
n_tokens: 32
answer_0: ' outside'
answer_1: ' inside'
answer_log_odds_shift: -0.25
answer_pair_mass: 0.45282694697380066
r2: 0.032258064516129004
---
# full donor contrast

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' ____', ' underside', '____', '___', ' _____', ' ________', ' lowest', ' side', ' ___', ' upside', '_____', ' ______', '________', ' lower', ' highest', ' outer', ' bottom', ' __', ' abdomen', ' middle', ' longest', ' left', ' inside', '_.', ' outskirts', '_\\', '__', ' largest', ' _.', '__.', ' smallest', ' right']

Generation (32 tokens):
```text
 outside.
Question: Which of the following is true?
Options:
A. The skeleton of the animal that barks and is called man's best
```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| outside | -1.42484 | 0.240546  |     0.0665296 |
| inside  | -1.54984 | 0.212281  |    -0.18347   |
| surface | -3.29984 | 0.0368889 |     0.50403   |
| left    | -3.36234 | 0.0346539 |    -0.12097   |
| ground  | -3.42484 | 0.0325544 |     0.19153   |
| right   | -3.98734 | 0.0185489 |    -0.43347   |
| bottom  | -3.98734 | 0.0185489 |     0.19153   |
| far     | -4.11234 | 0.0163694 |    -0.18347   |
| head    | -4.17484 | 0.0153776 |     0.25403   |
| outer   | -4.23734 | 0.0144459 |     0.25403   |

Final-decode readout: [' dogs', ' pets', 'dogs', ' Dogs', '犬', ' humans', ' wolves', '宠物', ' cats', '____', ' puppies', '狗狗', 'animals', ' mammals', ' dog', ' собаки', ' puppy', ' rabbits', ' animals', 'dog', 'pets', ' Humans', '狗的', '___', '狗', ' domest', ' lions', ' chiens', 'Humans', 'Pets', '养犬', ' ____']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
