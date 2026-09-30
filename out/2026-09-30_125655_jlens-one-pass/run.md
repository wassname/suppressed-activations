---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
block_index: 15
residual_index: 16
readout_block_index: 23
reverse: false
swap_logits: false
plural: true
prompt_slice: '-3:'
k: 32
seed: 0
decode_scale: 1.0
donor_checkpoint: out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: skeleton_body
elapsed_seconds: 13.66
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is  outside to  inside. Positive answer_log_odds_shift favours  inside over  outside; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Offline donor contrast: delta=mean(target)-mean(source), with strength1 in raw residual units. J projection is delta @ pinv(V).T @ V.T. Full contrast and norm-matched full contrast are separate controls. Equal-donor-norm=True: when true, compare full contrast, J projection and random at the full contrast's norm. Random uses one fixed seed0 direction at the same absolute norm as the full contrast, reused at every edited position. Only the saved generic donor checkpoint is used; no preliminary pass on the current input.  Prompt slice -3: plus every decode step; decode deltas are multiplied by 1.0. Concept token strings: (' spiders', ' dogs').

Selection: Previously selected spider/dog pair; generic offline donor templates frozen before extraction. No standalone readout benchmark in this intervention run. Previously chosen spider/dog example. Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes  outside toward  inside with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                       |   answer_log_odds_shift |   p( inside) |   p( outside) |   answer_pair_mass |        r2 |
|:--------------------------------|------------------------:|-------------:|--------------:|-------------------:|----------:|
| Base                            |                   0     |    0.279106  |     0.521439  |          0.800546  | 0.0322581 |
| norm-matched J donor projection |                  -0.125 |    0.0270476 |     0.0572598 |          0.0843075 | 0.0322581 |
| full donor contrast             |                   0.625 |    0.122109  |     0.122109  |          0.244217  | 0.0645161 |
| matched-random delta            |                   1.375 |    0.296446  |     0.140031  |          0.436477  | 0.225806  |

[Base](base/run.md)

# Base

Input:
```text
'Fact: Relative to the rest of its body, the skeleton of the animal that spins webs is on the'
```

Prefill readout: [' underside', '___', '____', ' abdomen', ' ____', ' upside', ' ________', ' side', ' _____', '________', ' ___', ' ______', '_____', ' inside', ' outer', ' skull', ' __', ' outskirts', ' bones', ' dorsal', ' __________________', ' lower', ' downside', ' backbone', ' neck', '_.', ' _.', ' shell', ' belly', ' skeletal', ' right', ' left']

Generation (32 tokens):
```text
 outside.
Question: The skeleton of the animal that spins webs is on the outside relative to the rest of its body.
Is the question factually correct
```

| token     |     log p |          p |   delta log p |
|:----------|----------:|-----------:|--------------:|
| outside   | -0.651162 | 0.521439   |             0 |
| inside    | -1.27616  | 0.279106   |             0 |
| ground    | -4.46366  | 0.0115201  |             0 |
| left      | -4.52616  | 0.0108221  |             0 |
| underside | -4.83866  | 0.00791764 |             0 |
| ______    | -4.90116  | 0.00743793 |             0 |
| right     | -4.96366  | 0.00698729 |             0 |
| end       | -5.02616  | 0.00656395 |             0 |
| bottom    | -5.02616  | 0.00656395 |             0 |
| head      | -5.15116  | 0.00579267 |             0 |

Final-decode readout: ['?\\', '?”,', '?",', '()?', '?”', '”?', '?“', ' correct', ')?', '**?', '?**', '?...', ' accurate', '?*', '?):', 'correct', '?)', '?”.', '.?', '?[', '>?', '?', '?(', '"?', '正确的', '？”', '?</', '?"', ' Correct', 'accur', '?".', '正确']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

[norm-matched J donor projection](norm-matched-j-donor-projection/run.md)

# norm-matched J donor projection

Input:
```text
'Fact: Relative to the rest of its body, the skeleton of the animal that spins webs is on the'
```

Prefill readout: [' ____', '____', '___', ' ___', ' __', ' ______', ' ________', ' _____', '__', '_____', ' left', '________', ' right', ' side', '_.', ' LEFT', ' _.', '__.', ' Left', ' __________________', '_________', '____________', ' _', '________________', ' RIGHT', ' upper', '_\\', ' bones', ' abdomen', '_', ' center', ' Right']

Generation (32 tokens):
```text
 left side.
Question: Is the animal that spins webs on the left side?
Options:
A. Yes
B. No
Answer:


```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| left    | -1.23516 | 0.290789  |       3.29101 |
| right   | -1.86016 | 0.155648  |       3.10351 |
| outside | -2.86016 | 0.0572598 |      -2.20899 |
| ______  | -3.23516 | 0.0393541 |       1.66601 |
| side    | -3.23516 | 0.0393541 |       2.16601 |
| same    | -3.48516 | 0.030649  |       2.16601 |
| inside  | -3.61016 | 0.0270476 |      -2.33399 |
| ____    | -3.73516 | 0.0238695 |       1.91601 |
| __      | -3.92266 | 0.0197885 |       1.29101 |
| top     | -4.04766 | 0.0174633 |       1.85351 |

Final-decode readout: ['____', '?\\', '  \n\n', '?', ' ____', '___', '\n\n', '_____', '？', '   \n\n', ' \n\n', '()?', ' ______', '?**', '  \n', '__', '_________', ' Answer', '________', '？**', '\\n', '.?', ' __', ' ___', '**?', '?:', '()', '   \n', '?(', '=?', ' _____', '?”']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

[full donor contrast](full-donor-contrast/run.md)

# full donor contrast

Input:
```text
'Fact: Relative to the rest of its body, the skeleton of the animal that spins webs is on the'
```

Prefill readout: ['____', ' ____', '___', ' __', ' ______', ' ___', ' ________', ' _____', '________', '__', '__.', '_____', ' __________________', '_.', '.__', ' bones', '____________', ' skeletal', ' abdomen', '_________', ' skull', ' _.', '.\\', ' bone', '.\\"', '._', '_\\', ' \\"', ' belly', '(__', ' position', '________________']

Generation (32 tokens):
```text
 left.
Question: Is the dog in the picture?
Options: A. Yes
Options: B. No
Answer:

<think>

</think>


```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| left    | -1.97784 | 0.138367  |      2.54832  |
| outside | -2.10284 | 0.122109  |     -1.45168  |
| inside  | -2.10284 | 0.122109  |     -0.826682 |
| right   | -2.85284 | 0.05768   |      2.11082  |
| top     | -3.66534 | 0.0255954 |      2.23582  |
| back    | -3.72784 | 0.0240446 |      2.98582  |
| head    | -3.72784 | 0.0240446 |      1.42332  |
| upper   | -3.79034 | 0.0225878 |      2.23582  |
| ground  | -3.79034 | 0.0225878 |      0.673318 |
| side    | -3.79034 | 0.0225878 |      1.61082  |

Final-decode readout: [' **', '  \n\n', ' Based', '\\n', '*\\', '\\"\\', ';**', '**', 'Based', '(**', 'Dog', '  \n\n\n', ' Dogs', '()\\', '<think>', '%\\', '</think>', ' \n\n', '狗', ' (**', '.\\', '  \n  \n', ' \n\n\n', '根据', '>\\', '...\\', '<|im_end|>', '\t\n\n', '\\")', '   \n\n', ' \n    \n', '  \n']

Coverage: 32 calls; prompt slice -3:, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
'Fact: Relative to the rest of its body, the skeleton of the animal that spins webs is on the'
```

Prefill readout: [' abdomen', ' underside', ' upside', ' spider', '___', ' side', ' belly', ' dorsal', ' ________', ' bones', ' ____', '-body', ' _____', ' ___', ' shell', ' legs', ' neck', ' limbs', ' skull', ' ______', ' lower', ' torso', '____', ' highest', ' scaffold', ' backbone', ' outskirts', ' skeletal', ' abdominal', ' same', ' jaw', ' upper']

Generation (32 tokens):
```text
 inside.
Question: The animal that spins webs is on the inside.
Is the following statement true or false?
The animal that spins webs is on
```

| token     |    log p |         p |   delta log p |
|:----------|---------:|----------:|--------------:|
| inside    | -1.21589 | 0.296446  |     0.0602717 |
| outside   | -1.96589 | 0.140031  |    -1.31473   |
| ground    | -2.09089 | 0.123577  |     2.37277   |
| underside | -3.46589 | 0.0312452 |     1.37277   |
| head      | -3.71589 | 0.0243338 |     1.43527   |
| vent      | -3.77839 | 0.0228595 |     1.68527   |
| bottom    | -3.77839 | 0.0228595 |     1.24777   |
| abdomen   | -3.96589 | 0.0189511 |     1.68527   |
| surface   | -4.02839 | 0.017803  |     1.37277   |
| upper     | -4.02839 | 0.017803  |     1.99777   |

Final-decode readout: [' inside', 'inside', ' located', ' Inside', ' indoors', 'Inside', ' outside', ' ___', ' internally', ' housed', 'located', ' internal', ' NOT', ' within', '___', ' ________', ' alive', ' __', ' really', ' _____', '_inside', '内部的', ' ______', ' actually', ' situated', ' mammals', ' positioned', ' inner', ' underneath', ' внутри', ' animals', ' not']

Coverage: 32 calls; prompt slice -3:, then one position per decode.
