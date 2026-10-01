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
answer_log_odds_shift: 0.0
answer_pair_mass: 0.44695213437080383
r2: 0.032258064516129004
---
# indirect-description donor

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' underside', ' upside', ' side', '___', '____', ' ____', ' lowest', ' lower', ' ________', ' abdomen', '________', ' ___', ' bottom', ' highest', ' inside', ' outer', ' left', ' _____', ' ______', ' right', '_____', ' middle', ' outskirts', '_.', ' downside', ' upper', '__.', ' __', ' skull', ' _.', ' bones', '__']

Generation (32 tokens):
```text
 inside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the outside.
Is the hypothesis true
```

| token   |   log p |         p |   delta log p |
|:--------|--------:|----------:|--------------:|
| inside  | -1.4379 | 0.237425  |   -0.0715289  |
| outside | -1.5629 | 0.209527  |   -0.0715289  |
| left    | -3.0004 | 0.049767  |    0.240971   |
| right   | -3.3129 | 0.0364103 |    0.240971   |
| ground  | -3.6879 | 0.0250244 |   -0.0715289  |
| surface | -3.8129 | 0.022084  |   -0.00902891 |
| far     | -3.9379 | 0.019489  |   -0.00902891 |
| end     | -4.0629 | 0.017199  |   -0.00902891 |
| bottom  | -4.0629 | 0.017199  |    0.115971   |
| same    | -4.1254 | 0.016157  |   -0.00902891 |

Final-decode readout: ['?\\', '?**', '?”', '**?', ' true', '？**', ' TRUE', '?“', '?</', '”?', ' logically', '？”', 'true', '?', ' **“', '?”,', '()?', 'TRUE', ' True', '?",', ' logical', '?)', ')?', '.?', '?’', '？', '?$', '?<', 'True', ' truthful', '?:', ' Logical']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
