---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
country_swap: false
coordinate_kind: None
reverse: true
swap_logits: false
plural: false
k: 32
strength: 1
decode_scale: 0.25
prompt_slice: '-1:'
continuous: true
steering_schedule: prompt and continuous decode
max_new_tokens: 32
seed: 0
vjp_checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_063925_jlens-one-pass/vjp.pt
donor_checkpoint: None
reflection_coordinate_checkpoint: None
donor_norm: None
donor_reflection: false
equal_donor_norm: false
relation: skeleton_body
expected_answer: ' outside'
n_tokens: 32
answer_0: ' outside'
answer_1: ' inside'
answer_log_odds_shift: -0.125
answer_pair_mass: 0.462313711643219
r2: 0.032258064516129004
---
# offline naming VJP

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' underside', ' upside', ' side', ' lowest', '___', '____', ' ____', ' lower', ' highest', ' ________', ' inside', ' abdomen', '________', ' ___', ' outer', ' bottom', ' _____', '_____', ' ______', ' left', '_.', ' upper', ' right', ' middle', ' skull', ' bones', ' bone', ' longest', ' outskirts', ' downside', '__.', ' center']

Generation (32 tokens):
```text
 inside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the outside.
Is the hypothesis true
```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| outside | -1.46466 | 0.231157  |     0.0267152 |
| inside  | -1.46466 | 0.231157  |    -0.0982848 |
| left    | -3.21466 | 0.040169  |     0.0267153 |
| right   | -3.46466 | 0.0312837 |     0.0892153 |
| ground  | -3.58966 | 0.0276078 |     0.0267153 |
| surface | -3.77716 | 0.0228876 |     0.0267153 |
| far     | -3.83966 | 0.0215009 |     0.0892153 |
| same    | -4.08966 | 0.0167449 |     0.0267153 |
| end     | -4.08966 | 0.0167449 |    -0.0357847 |
| bottom  | -4.15216 | 0.0157304 |     0.0267153 |

Final-decode readout: ['?\\', '?**', '?”', '**?', '？**', ' true', '?“', ' TRUE', '?</', '”?', ' logically', '？”', '?', '?”,', ' **“', '()?', '?",', 'true', 'TRUE', ')?', '?)', ' logical', '.?', '?’', '？', '?$', ' True', '?<', '?:', 'True', ' truthful', ' Logical']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
