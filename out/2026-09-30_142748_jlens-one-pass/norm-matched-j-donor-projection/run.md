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
decode_scale: 0.25
prompt_slice: '-1:'
continuous: true
steering_schedule: prompt and continuous decode
max_new_tokens: 32
seed: 0
donor_checkpoint: out/2026-09-30_133218_jlens-one-pass/donors.pt
donor_norm: 6.9019775390625
equal_donor_norm: true
relation: skeleton_body
expected_answer: ' outside'
n_tokens: 32
answer_0: ' outside'
answer_1: ' inside'
answer_log_odds_shift: 0.125
answer_pair_mass: 0.4561469554901123
r2: 0.032258064516129004
---
# norm-matched J donor projection

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' underside', ' spider', ' spiders', ' middle', ' upside', ' bottom', ' highest', ' lowest', ' same', ' outskirts', ' abdomen', ' side', ' top', ' outer', ' inside', '___', ' longest', ' Spider', ' spine', ' _____', ' interior', ' ceiling', ' surface', ' darkest', ' center', ' dorsal', ' ___', ' downside', ' largest', ' smallest', ' ____', ' exterior']

Generation (32 tokens):
```text
 inside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the outside.
Does the fact support
```

| token     |    log p |         p |   delta log p |
|:----------|---------:|----------:|--------------:|
| inside    | -1.36088 | 0.256435  |    0.00549424 |
| outside   | -1.61088 | 0.199712  |   -0.119506   |
| surface   | -3.04838 | 0.0474357 |    0.755494   |
| ground    | -3.61088 | 0.0270281 |    0.00549436 |
| bottom    | -3.67338 | 0.0253905 |    0.505494   |
| same      | -4.04838 | 0.0174506 |    0.0679941  |
| floor     | -4.04838 | 0.0174506 |    0.692994   |
| left      | -4.11088 | 0.0163933 |   -0.869506   |
| right     | -4.17338 | 0.0154001 |   -0.619506   |
| underside | -4.17338 | 0.0154001 |    1.19299    |

Final-decode readout: [' imply', ' implies', '?\\', ' entail', ' implying', ' contradict', ' entails', ' refute', ' support', ' contrad', ' implied', ' supports', ' logically', 'impl', '上述事实', '支持', '-support', ' implic', ' implication', ' suggest', '?**', ':\\', 'upport', ' suggests', ' mendukung', 'supports', 'ually', ' endorse', '**?', ' constrain', '.\\', '?*']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

Written by PI/OpenAI.
