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
expected_answer: 'control'
n_tokens: 32
answer_0: ' outside'
answer_1: ' inside'
answer_log_odds_shift: 1.375
answer_pair_mass: 0.43647700548171997
r2: 0.22580645161290325
---
# matched-random delta

Input:
```text
'Fact: Relative to the rest of its body, the skeleton of the animal that spins webs is on the'
```

Prefill readout: [' abdomen', ' underside', ' upside', ' spider', '___', ' side', ' belly', ' dorsal', ' ________', ' bones', ' ____', '-body', ' _____', ' ___', ' shell', ' legs', ' neck', ' limbs', ' skull', ' ______', ' lower', ' torso', '____', ' highest', ' scaffold', ' backbone', ' outskirts', ' skeletal', ' abdominal', ' same', ' jaw', ' upper']

Generation (32 tokens):
```text
 inside.
Question: The animal that spins webs is on the inside.
Is the following statement true or false?
The animal that spins webs is on
```

| token     |    log p |         p |   delta log p |
|:----------|---------:|----------:|--------------:|
| inside    | -1.21589 | 0.296446  |     0.0602717 |
| outside   | -1.96589 | 0.140031  |    -1.31473   |
| ground    | -2.09089 | 0.123577  |     2.37277   |
| underside | -3.46589 | 0.0312452 |     1.37277   |
| head      | -3.71589 | 0.0243338 |     1.43527   |
| vent      | -3.77839 | 0.0228595 |     1.68527   |
| bottom    | -3.77839 | 0.0228595 |     1.24777   |
| abdomen   | -3.96589 | 0.0189511 |     1.68527   |
| surface   | -4.02839 | 0.017803  |     1.37277   |
| upper     | -4.02839 | 0.017803  |     1.99777   |

Final-decode readout: [' inside', 'inside', ' located', ' Inside', ' indoors', 'Inside', ' outside', ' ___', ' internally', ' housed', 'located', ' internal', ' NOT', ' within', '___', ' ________', ' alive', ' __', ' really', ' _____', '_inside', '内部的', ' ______', ' actually', ' situated', ' mammals', ' positioned', ' inner', ' underneath', ' внутри', ' animals', ' not']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
