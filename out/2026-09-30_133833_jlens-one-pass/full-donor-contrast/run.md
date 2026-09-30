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
n_tokens: 32
answer_0: '8'
answer_1: '4'
answer_log_odds_shift: 3.999999761581421
answer_pair_mass: 0.6045734882354736
swap_log_odds_shift: 3.999999761581421
bare_answer_mass: 0.6045734882354736
r2: 0.3548387096774194
---
# full donor contrast

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: ['___', '____', '__.', '__', '.\\', '\\"\\', ' ___', '_________', '\\"', ' ____', ' ______', ' __', '?\\', '____________', '.\\"', '________', '.__', '。\\', '\\n', '_.', ').\\', '________________', '\\""', '\\")', '_____', ' __________________', '(number', '\\.', ' ________', '2', '__:', '3']

Generation (32 tokens):
```text
4.
Question: Does the animal that spins webs have 4 legs?
Answer: Yes.
Question: Does the animal that spins webs have 
```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       4 | -0.755161 | 0.469935   |      2.11976  |
|       6 | -1.88016  | 0.152566   |      1.74476  |
|       2 | -1.88016  | 0.152566   |      3.11976  |
|       8 | -2.00516  | 0.134639   |     -1.88024  |
|       1 | -3.38016  | 0.034042   |      1.24476  |
|       3 | -3.63016  | 0.0265119  |      1.49476  |
|       5 | -4.38016  | 0.0125233  |      1.24476  |
|       0 | -4.75516  | 0.00860716 |      1.74476  |
|       7 | -5.38016  | 0.00460708 |      0.369758 |
|       9 | -6.38016  | 0.00169485 |      0.182258 |

Final-decode readout: [' fewer', ' dogs', '?\\', ' horns', ' animals', ' claws', '___', ' TWO', ' wings', ' pets', ' breasts', ' multiple', ' ___', ' cats', ' eyes', ' bones', ' ears', ' five', ' puppies', ' lungs', ' tails', ' feathers', ' THREE', ' muscles', ' snakes', ' three', '?', 'bones', ' Dogs', '?(', ' two', ' ANY']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
