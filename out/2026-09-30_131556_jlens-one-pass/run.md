---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
block_index: 15
residual_index: 16
readout_block_index: 23
reverse: true
swap_logits: false
plural: true
prompt_slice: '-1:'
k: 32
seed: 0
decode_scale: 1.0
donor_checkpoint: out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: skeleton_body
elapsed_seconds: 62.23
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is  inside to  outside. Positive answer_log_odds_shift favours  inside over  outside; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Offline donor contrast: delta=mean(target)-mean(source), with strength1 in raw residual units. J projection is delta @ pinv(V).T @ V.T. Full contrast and norm-matched full contrast are separate controls. Equal-donor-norm=True: when true, compare full contrast, J projection and random at the full contrast's norm. Random uses one fixed seed0 direction at the same absolute norm as the full contrast, reused at every edited position. Only the saved generic donor checkpoint is used; no preliminary pass on the current input.  Prompt slice -1: plus every decode step; decode deltas are multiplied by 1.0. Concept token strings: (' spiders', ' dogs').

Selection: Previously selected spider/dog pair; generic offline donor templates frozen before extraction. No standalone readout benchmark in this intervention run. Previously chosen spider/dog example. Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes  inside toward  outside with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                       |   answer_log_odds_shift |   p( inside) |   p( outside) |   answer_pair_mass |        r2 |
|:--------------------------------|------------------------:|-------------:|--------------:|-------------------:|----------:|
| Base                            |                   0     |     0.25503  |      0.225063 |           0.480093 | 0.0322581 |
| norm-matched J donor projection |                   0.5   |     0.288834 |      0.154602 |           0.443436 | 0.0967742 |
| full donor contrast             |                   0.25  |     0.266141 |      0.182916 |           0.449057 | 0         |
| matched-random delta            |                   0.625 |     0.279845 |      0.132189 |           0.412035 | 0.0322581 |

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

Prefill readout: [' underside', ' spider', ' spiders', ' upside', ' middle', ' outskirts', ' abdomen', ' bottom', ' side', ' dorsal', ' highest', ' interior', ' Spider', ' outer', ' spine', ' inside', ' torso', ' lowest', '___', ' ceiling', ' axis', ' downside', '________', ' scale', ' sidelines', ' verge', ' same', ' backbone', ' biome', ' verte', ' _____', ' ________']

Generation (32 tokens):
```text
 inside.
Question: Which of the arthropods is the most likely candidate for the riddle?
Answer: The skeleton of the arthropod is
```

| token   |   log p |         p |   delta log p |
|:--------|--------:|----------:|--------------:|
| inside  | -1.2419 | 0.288834  |     0.124472  |
| outside | -1.8669 | 0.154602  |    -0.375528  |
| surface | -3.1169 | 0.0442942 |     0.686973  |
| ground  | -3.7419 | 0.023709  |    -0.125527  |
| left    | -3.7419 | 0.023709  |    -0.500527  |
| dorsal  | -3.9294 | 0.0196554 |     1.43697   |
| right   | -3.9294 | 0.0196554 |    -0.375527  |
| bottom  | -3.9919 | 0.0184646 |     0.186973  |
| same    | -4.0544 | 0.0173459 |     0.0619726 |
| floor   | -4.1169 | 0.0162949 |     0.624473  |

Final-decode readout: [' spiders', ' spider', ' Spider', '蜘蛛', 'Spider', '蛛', 'webs', ' webs', ' described', ' resembles', ' closest', ' pictured', '爬行', ' consists', ' crawled', ' crawling', ' пау', ' depicted', ' discussed', ' mentioned', ' whose', ' itself', ' crawl', ' insects', ' Webs', ' nearest', ' web', '爬虫', ' referred', ' ecosystem', ' corresponds', ' named']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

[full donor contrast](full-donor-contrast/run.md)

# full donor contrast

Input:
```text
"Fact: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the"
```

Prefill readout: ['_____', ' ________', '________', '___', ' _____', ' ___', ' underside', '_________', ' upside', ' abdomen', '________________', ' spider', '＿＿', ' __________________', ' ____', ' ______', '____________', '\\xc', '_\\', ' _.', '____', ' highest', ' Spider', '_.', ' outskirts', ' lowest', '__.', ' middle', ' __________________________________', ' side', '＿', ' dors']

Generation (32 tokens):
```text
 inside.
Question: Relative to the rest of its body, the skeleton of the animal that barks and is called man's best friend is on the inside
```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| inside  | -1.32373 | 0.266141  |     0.0426462 |
| outside | -1.69873 | 0.182916  |    -0.207354  |
| ground  | -3.32373 | 0.0360183 |     0.292646  |
| side    | -3.63623 | 0.0263516 |     0.605146  |
| surface | -3.69873 | 0.024755  |     0.105146  |
| right   | -3.82373 | 0.0218462 |    -0.269854  |
| left    | -3.88623 | 0.0205226 |    -0.644854  |
| same    | -3.94873 | 0.0192792 |     0.167646  |
| floor   | -4.07373 | 0.0170138 |     0.667646  |
| dorsal  | -4.07373 | 0.0170138 |     1.29265   |

Final-decode readout: [' ________', ' ___', '________', ' _____', '_____', ' **(', ' __________________', ' **[', '___', ' ______', '_________', '________________', ' __', ' ____', ' **-', '____________', '**(', ' _(', ' __________________________________', ' **+', ' **“', '_[', ' _.', ' **.', '**?', ' **「', '＿＿', ' **', '____', '...**', '-**', ' inside']

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
Question: What is the inside of the skeleton of the animal that barks and is called man's best friend?
Answer:

<think>

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

Final-decode readout: ['"**', '”**', '）**', 'Thinking', ' Thinking', '”**,', '”**.', '思考', ' "**', '】**', ' Thought', ';**', '==="', ')**', '»**', ' Think', '"""', '".**', '的思考', '...**', ' **“', '**)', ' **"', 'Thought', '」**', '**),', '**', '.AI', '."""', '\r\n\r\n\r\n\r\n', ')**,', 'thinking']

Coverage: 32 calls; prompt slice -1:, then one position per decode.
