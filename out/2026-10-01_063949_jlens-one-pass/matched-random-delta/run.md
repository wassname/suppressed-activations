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
expected_answer: 'control'
n_tokens: 32
answer_0: ' outside'
answer_1: ' inside'
answer_log_odds_shift: -0.125
answer_pair_mass: 0.46873506903648376
r2: 0.032258064516129004
---
# matched-random delta

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' underside', ' upside', ' side', ' lowest', '___', '____', ' ____', ' lower', ' highest', ' ________', ' inside', ' abdomen', '________', ' ___', ' outer', ' bottom', ' _____', ' ______', '_____', ' skull', ' left', '_.', ' right', ' middle', ' upper', ' longest', ' bones', ' bone', ' outskirts', ' downside', '__.', ' center']

Generation (32 tokens):
```text
 inside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the outside.
Is the hypothesis true
```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| outside | -1.45086 | 0.234368  |     0.0405091 |
| inside  | -1.45086 | 0.234368  |    -0.0844909 |
| left    | -3.26336 | 0.0382594 |    -0.0219908 |
| right   | -3.51336 | 0.0297965 |     0.0405092 |
| ground  | -3.57586 | 0.0279912 |     0.0405092 |
| surface | -3.76336 | 0.0232055 |     0.0405092 |
| far     | -3.88836 | 0.0204788 |     0.0405092 |
| same    | -4.07586 | 0.0169775 |     0.0405092 |
| end     | -4.07586 | 0.0169775 |    -0.0219908 |
| bottom  | -4.13836 | 0.0159489 |     0.0405092 |

Final-decode readout: ['?\\', '?**', '?”', '**?', '？**', ' true', ' TRUE', '?“', '?</', '”?', ' logically', '？”', '?', '?”,', ' **“', '()?', 'true', 'TRUE', '?",', ')?', '?)', ' logical', '.?', '?’', '？', ' True', '?$', '?<', '?:', 'True', ' truthful', ' Logical']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
