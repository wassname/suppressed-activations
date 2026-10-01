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
expected_answer: 'control'
n_tokens: 32
answer_0: ' outside'
answer_1: ' inside'
answer_log_odds_shift: 0.0
answer_pair_mass: 0.4575987458229065
r2: 0.032258064516129004
---
# matched-random delta

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' underside', ' upside', ' side', ' lowest', '___', ' lower', ' ____', '____', ' highest', ' ________', ' abdomen', ' inside', ' bottom', ' ___', '________', ' _____', ' outer', ' left', '_____', '_.', ' bones', ' ______', ' right', ' upper', ' skull', ' downside', ' bone', ' middle', ' outskirts', ' longest', ' same', '__.']

Generation (32 tokens):
```text
 inside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the outside.
Is the hypothesis true
```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| inside  | -1.41436 | 0.243081  |    -0.0479877 |
| outside | -1.53936 | 0.214518  |    -0.0479877 |
| left    | -3.10186 | 0.0449654 |     0.139513  |
| right   | -3.35186 | 0.0350191 |     0.202013  |
| ground  | -3.53936 | 0.0290319 |     0.0770125 |
| surface | -3.97686 | 0.0187444 |    -0.172987  |
| end     | -4.03936 | 0.0176087 |     0.0145125 |
| bottom  | -4.10186 | 0.0165419 |     0.0770125 |
| far     | -4.10186 | 0.0165419 |    -0.172987  |
| same    | -4.10186 | 0.0165419 |     0.0145125 |

Final-decode readout: ['?\\', '?**', '?”', '**?', '？**', '?“', ' true', '?</', ' TRUE', '”?', ' logically', ' **“', '？”', '?”,', '?', '()?', '?",', '?)', ' logical', '.?', ')?', '?’', 'true', '？', 'TRUE', '?$', '?<', '?:', ' True', ' truthful', '?*', ' Logical']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
