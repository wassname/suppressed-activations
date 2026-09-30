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
expected_answer: 'control'
n_tokens: 32
answer_0: ' outside'
answer_1: ' inside'
answer_log_odds_shift: 1.8125001192092896
answer_pair_mass: 0.1827644556760788
r2: 0.032258064516129004
---
# matched-random delta

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' upside', ' underside', ' bones', ' abdomen', ' same', ' lower', ' lowest', ' highest', ' bone', ' skull', '___', ' upper', ' side', ' bottom', ' ________', ' ____', ' _____', ' backbone', ' ___', ' middle', ' neck', '____', ' ______', ' jaw', ' torso', ' belly', ' dorsal', ' skeletal', ' nose', ' front', ' right', '________']

Generation (32 tokens):
```text
 inside.
Question: What is the inside of the skeleton of the animal that barks and is called man's best friend?
Answer:

<think>

```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| inside  | -1.83414 | 0.15975   |      -0.46777 |
| ground  | -2.08414 | 0.124414  |       1.53223 |
| bottom  | -3.02164 | 0.0487211 |       1.15723 |
| upper   | -3.02164 | 0.0487211 |       1.40723 |
| head    | -3.27164 | 0.037944  |       1.15723 |
| lower   | -3.33414 | 0.0356451 |       1.21973 |
| floor   | -3.33414 | 0.0356451 |       1.40723 |
| top     | -3.33414 | 0.0356451 |       0.90723 |
| outside | -3.77164 | 0.0230142 |      -2.28027 |
| right   | -3.83414 | 0.0216198 |      -0.28027 |

Final-decode readout: ['"**', '”**', '）**', 'Thinking', ' Thinking', '”**,', '”**.', '思考', ' "**', '】**', ' Thought', ';**', '==="', ')**', '»**', ' Think', '".**', '"""', ' **“', ' **"', '的思考', '...**', '**)', '**),', '**', '」**', '.AI', 'Thought', '\r\n\r\n\r\n\r\n', '*****', ')**,', ' \n\n\n\n']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

Written by PI/OpenAI.
