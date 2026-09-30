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
prompt_slice: '-1:'
continuous: true
steering_schedule: prompt and continuous decode
max_new_tokens: 32
seed: 0
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-09-30_133218_jlens-one-pass/donors.pt
donor_norm: None
donor_reflection: true
equal_donor_norm: false
relation: skeleton_body
expected_answer: 'control'
n_tokens: 32
answer_0: ' outside'
answer_1: ' inside'
answer_log_odds_shift: 0.0
answer_pair_mass: 0.4800933003425598
r2: 0.032258064516129004
---
# matched-random reflection control

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' underside', ' upside', ' side', ' lowest', '___', '____', ' ____', ' lower', ' highest', ' ________', ' inside', ' abdomen', ' ___', '________', ' outer', ' bottom', ' _____', '_____', ' ______', ' skull', ' left', ' middle', '_.', ' right', ' upper', ' longest', ' bones', ' bone', ' outskirts', ' downside', '__.', ' center']

Generation (32 tokens):
```text
 inside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the outside.
Is the hypothesis true
```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| inside  | -1.36637 | 0.25503   |             0 |
| outside | -1.49137 | 0.225063  |             0 |
| left    | -3.24137 | 0.0391101 |             0 |
| right   | -3.55387 | 0.0286136 |             0 |
| ground  | -3.61637 | 0.02688   |             0 |
| surface | -3.80387 | 0.0222843 |             0 |
| far     | -3.92887 | 0.0196658 |             0 |
| end     | -4.05387 | 0.017355  |             0 |
| same    | -4.11637 | 0.0163035 |             0 |
| bottom  | -4.17887 | 0.0153157 |             0 |

Final-decode readout: ['?\\', '?**', '?”', '**?', '？**', ' true', ' TRUE', '?“', '?</', '”?', ' logically', ' **“', '？”', '?”,', '?', '()?', 'true', '?",', ' logical', 'TRUE', '?)', ')?', '.?', ' True', '?’', '?$', '？', '?<', ' truthful', '?:', 'True', ' Logical']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Source-side calls: 7; calls with nonzero applied updates: 7. Sum of requested/applied delta norms: 6.920554/6.921530. Per-call margins and doses are in interventions.json.

Written by PI/OpenAI.
