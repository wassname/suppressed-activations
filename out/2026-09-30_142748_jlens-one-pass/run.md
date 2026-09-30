---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
steering_schedule: prompt and continuous decode
block_index: 15
residual_index: 16
readout_block_index: 23
reverse: true
swap_logits: false
plural: true
prompt_slice: '-1:'
k: 32
seed: 0
decode_scale: 0.25
donor_norm: 6.9019775390625
donor_checkpoint: out/2026-09-30_133218_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: skeleton_body
elapsed_seconds: 18.47
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is  inside to  outside. Positive answer_log_odds_shift favours  inside over  outside; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Offline donor contrast: delta=mean(target)-mean(source) in raw residual units. Requested donor norm=6.9019775390625; a specified norm rescales this contrast and is not an unscaled component replacement. J projection is delta @ pinv(V).T @ V.T. Full contrast and norm-matched full contrast are separate controls. Equal-donor-norm=True: when true, compare full contrast, J projection and random at the full contrast's norm. Random uses one fixed seed0 direction at the same absolute norm as the full contrast, reused at every edited position. Only the saved generic donor checkpoint is used; no preliminary pass on the current input.  Schedule: prompt and continuous decode. Prompt slice -1:; decode deltas are multiplied by 0.25. Concept token strings: (' spiders', ' dogs').

Selection: Previously selected spider/dog pair; generic offline donor templates frozen before extraction. No standalone readout benchmark in this intervention run. Previously chosen spider/dog example. Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes  inside toward  outside with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                       |   answer_log_odds_shift |   p( inside) |   p( outside) |   answer_pair_mass |        r2 |
|:--------------------------------|------------------------:|-------------:|--------------:|-------------------:|----------:|
| Base                            |                   0     |     0.25503  |      0.225063 |           0.480093 | 0.0322581 |
| norm-matched J donor projection |                   0.125 |     0.256435 |      0.199712 |           0.456147 | 0.0322581 |
| full donor contrast             |                  -0.25  |     0.212281 |      0.240546 |           0.452827 | 0.0322581 |
| matched-random delta            |                   0.625 |     0.279845 |      0.132189 |           0.412035 | 0         |

[Base](base/run.md)

# Base

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

Final-decode readout: ['?\\', '?**', '?”', '**?', '？**', ' true', '?“', ' TRUE', '?</', '”?', ' logically', '？”', '?', '?”,', ' **“', '()?', '?",', 'true', 'TRUE', ')?', '.?', '?)', ' logical', '?’', '？', '?$', ' True', '?<', '?:', 'True', ' truthful', ' Logical']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

[norm-matched J donor projection](norm-matched-j-donor-projection/run.md)

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

[full donor contrast](full-donor-contrast/run.md)

# full donor contrast

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' ____', ' underside', '____', '___', ' _____', ' ________', ' lowest', ' side', ' ___', ' upside', '_____', ' ______', '________', ' lower', ' highest', ' outer', ' bottom', ' __', ' abdomen', ' middle', ' longest', ' left', ' inside', '_.', ' outskirts', '_\\', '__', ' largest', ' _.', '__.', ' smallest', ' right']

Generation (32 tokens):
```text
 outside.
Question: Which of the following is true?
Options:
A. The skeleton of the animal that barks and is called man's best
```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| outside | -1.42484 | 0.240546  |     0.0665296 |
| inside  | -1.54984 | 0.212281  |    -0.18347   |
| surface | -3.29984 | 0.0368889 |     0.50403   |
| left    | -3.36234 | 0.0346539 |    -0.12097   |
| ground  | -3.42484 | 0.0325544 |     0.19153   |
| right   | -3.98734 | 0.0185489 |    -0.43347   |
| bottom  | -3.98734 | 0.0185489 |     0.19153   |
| far     | -4.11234 | 0.0163694 |    -0.18347   |
| head    | -4.17484 | 0.0153776 |     0.25403   |
| outer   | -4.23734 | 0.0144459 |     0.25403   |

Final-decode readout: [' dogs', ' pets', 'dogs', ' Dogs', '犬', ' humans', ' wolves', '宠物', ' cats', '____', ' puppies', '狗狗', 'animals', ' mammals', ' dog', ' собаки', ' puppy', ' rabbits', ' animals', 'dog', 'pets', ' Humans', '狗的', '___', '狗', ' domest', ' lions', ' chiens', 'Humans', 'Pets', '养犬', ' ____']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: [' upside', ' underside', ' lower', ' lowest', ' side', '___', ' upper', ' highest', ' bottom', ' abdomen', ' bones', ' ________', ' bone', ' ____', ' same', ' downside', ' ___', ' right', ' skull', '____', ' inside', ' _____', ' left', ' dorsal', ' middle', '________', ' ______', ' torso', '_____', '_.', ' opposite', ' neck']

Generation (32 tokens):
```text
 inside.
Question: Is the skeleton of the animal that barks and is called man's best friend on the inside or outside?
Options:
A
```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| inside  | -1.27352 | 0.279845  |     0.0928547 |
| outside | -2.02352 | 0.132189  |    -0.532145  |
| left    | -3.27352 | 0.0378729 |    -0.032145  |
| right   | -3.27352 | 0.0378729 |     0.280355  |
| ground  | -3.33602 | 0.0355783 |     0.280355  |
| bottom  | -3.77352 | 0.0229711 |     0.405355  |
| upper   | -3.89852 | 0.0202719 |     0.530355  |
| side    | -3.96102 | 0.0190437 |     0.280355  |
| lower   | -4.08602 | 0.016806  |     0.467855  |
| head    | -4.14852 | 0.0157878 |     0.280355  |

Final-decode readout: [' Options', '选项', ' Option', ' Answer', 'Options', 'Option', 'options', ' options', '[A', '-option', 'option', '-options', '選項', '<option', 'answer', ' option', ' OPTIONS', ':<', ' answer', '(A', ' Answers', '回答', ':(', '.options', '/options', 'Answer', '\tA', '.Options', ' OPTION', ' Choice', ':A', ':[']

Coverage: 32 calls; prompt slice -1:, then one position per decode.
