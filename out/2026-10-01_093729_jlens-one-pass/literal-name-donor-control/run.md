---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
block_index: 15
readout_block_index: 23
indirect_donor: true
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
vjp_checkpoint: None
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-10-01_093711_jlens-one-pass/donors.pt
reflection_coordinate_checkpoint: None
donor_norm: None
donor_reflection: false
equal_donor_norm: false
relation: skeleton_body
expected_answer: ' outside'
n_tokens: 32
answer_0: ' outside'
answer_1: ' inside'
answer_log_odds_shift: -0.25
answer_pair_mass: 0.4763234257698059
r2: 0.032258064516129004
---
# literal-name donor control

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' underside', '___', ' lowest', '____', ' ____', ' upside', ' side', ' ________', ' lower', ' highest', '________', ' ___', ' _____', ' outer', ' inside', ' abdomen', ' bottom', '_____', ' ______', ' longest', '_.', ' middle', ' outskirts', ' left', '__.', ' __', ' right', '_\\', '__', ' downside', ' upper', ' skull']

Generation (32 tokens):
```text
 outside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the inside.
Is the hypothesis true
```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| outside | -1.37426 | 0.253027  |    0.117117   |
| inside  | -1.49926 | 0.223296  |   -0.132883   |
| left    | -3.31176 | 0.0364521 |   -0.0703831  |
| ground  | -3.56176 | 0.0283889 |    0.0546169  |
| surface | -3.62426 | 0.0266689 |    0.179617   |
| right   | -3.68676 | 0.0250531 |   -0.132883   |
| far     | -3.93676 | 0.0195114 |   -0.00788307 |
| end     | -4.06176 | 0.0172187 |   -0.00788307 |
| same    | -4.12426 | 0.0161755 |   -0.00788307 |
| bottom  | -4.12426 | 0.0161755 |    0.0546169  |

Final-decode readout: ['?\\', '?**', '?”', '**?', '？**', ' TRUE', '?“', ' true', '?</', '”?', ' logically', '?', '?”,', '？”', ' **“', '()?', ' logical', 'true', '?",', 'TRUE', '?’', ')?', '?)', '?<', '？', '?$', ' True', '.?', ' Logical', '?:', 'True', '?*']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
