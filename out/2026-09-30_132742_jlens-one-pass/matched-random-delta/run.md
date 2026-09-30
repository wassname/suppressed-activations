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
expected_answer: 'control'
n_tokens: 32
answer_0: ' outside'
answer_1: ' inside'
answer_log_odds_shift: 0.5000000596046448
answer_pair_mass: 0.7375627756118774
r2: 0.09677419354838712
---
# matched-random delta

Input:
```text
'Fact: Relative to the rest of its body, the skeleton of the animal that spins webs is on the'
```

Prefill readout: [' underside', ' abdomen', ' upside', ' side', '___', ' dorsal', ' ________', ' lower', ' ____', ' ___', ' _____', '____', ' belly', ' outskirts', ' downside', ' shell', ' ______', '-body', ' bones', ' spider', ' inside', ' neck', ' scaffold', ' limbs', ' torso', '________', ' lowest', ' skull', '_____', ' legs', ' abdominal', ' outer']

Generation (32 tokens):
```text
 outside.
Question: The skeleton of the animal that spins webs is on the outside.
Answer:

<think>
Thinking Process:

1.  **
```

| token     |     log p |          p |   delta log p |
|:----------|----------:|-----------:|--------------:|
| outside   | -0.937003 | 0.3918     |     -0.285841 |
| inside    | -1.062    | 0.345763   |      0.214159 |
| ground    | -3.687    | 0.025047   |      0.776659 |
| underside | -4.187    | 0.0151917  |      0.651659 |
| vent      | -4.6245   | 0.00980853 |      0.839159 |
| other     | -4.687    | 0.00921426 |      0.526659 |
| bottom    | -4.687    | 0.00921426 |      0.339159 |
| end       | -4.687    | 0.00921426 |      0.339159 |
| left      | -4.937    | 0.00717607 |     -0.410841 |
| ______    | -4.937    | 0.00717607 |     -0.035841 |

Final-decode readout: [':**', '：**', '__:', ':*', '.:**', '):**', ';**', ':\\', '**:', '...**', '):\\', '...\\', '?:', ' ():', '*:', ':&', '#:', ':")', '...*', ' **:', ' **【', '!:', ' **:**', ':",', '():', ':__', ' premise', ' analyze', '\\":', '.):', ':...', '!!:']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
