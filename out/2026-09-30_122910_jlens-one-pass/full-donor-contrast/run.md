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
answer_log_odds_shift: 0.5000001192092896
answer_pair_mass: 0.37913691997528076
r2: 0.09677419354838712
---
# full donor contrast

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: ['_____', '________', ' ________', ' _____', '___', ' ___', ' underside', '_________', ' spider', '＿＿', '________________', ' highest', '\\xc', ' lowest', '____________', ' __________________', ' ______', ' Spider', ' abdomen', '_\\', ' ____', ' upside', ' longest', ' hardest', '...\\', '____', '?\\', ' webs', ' biome', ' fastest', '\\u', ' closest']

Generation (32 tokens):
```text
 inside of the body.
Question: Relative to the rest of the body, the skeleton of the animal that barks and is called man's best friend is
```

| token    |    log p |         p |   delta log p |
|:---------|---------:|----------:|--------------:|
| inside   | -1.39856 | 0.246953  |    -0.0321846 |
| outside  | -2.02356 | 0.132184  |    -0.532185  |
| same     | -3.02356 | 0.0486279 |     1.09282   |
| side     | -3.33606 | 0.0355769 |     0.905315  |
| surface  | -3.58606 | 0.0277073 |     0.217815  |
| other    | -3.77356 | 0.0229702 |     1.15532   |
| ground   | -3.89856 | 0.0202711 |    -0.282185  |
| dorsal   | -3.89856 | 0.0202711 |     1.46782   |
| opposite | -3.96106 | 0.0190429 |     0.530315  |
| right    | -4.27356 | 0.0139321 |    -0.719685  |

Final-decode readout: [' spiders', ' spider', ' Spider', '蜘蛛', 'Spider', ' ___', '蛛', '___', ' _____', ' ________', '_____', ' insects', '________', ' webs', ' __________________', ' **(', ' ______', '____________', ' ____', '________________', ' humans', '____', ' crawling', ' __', '_________', 'webs', ' mammals', ' web', ' ---', ' insect', ' consists', '?\\']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
