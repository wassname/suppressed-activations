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
prompt_slice: '-1:'
k: 32
seed: 0
decode_scale: 1.0
donor_checkpoint: /workspace/2026/suppressed-activations/out/2026-09-30_105132_jlens-one-pass/donors.pt
equal_donor_norm: true
relation: skeleton_body
elapsed_seconds: 11.84
---
# Same-pass intervention pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Rule: edit block 15, observe block 23, last-position readout, prompt-word removal only; no final-layer output mask. The observer never controls the edit; it returns no activation replacement. Expected answer movement is  outside to  inside. Positive answer_log_odds_shift favours  inside over  outside; reverse success has a negative shift. For legs this is the defined swap_log_odds_shift; skeleton uses its own word-answer pair, not the digit metric. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Offline donor contrast: delta=mean(target)-mean(source), with strength1 in raw residual units. J projection is delta @ pinv(V).T @ V.T. Full contrast and norm-matched full contrast are separate controls. Equal-donor-norm=True: when true, compare full contrast, J projection and random at the full contrast's norm. Random uses one fixed seed0 direction at the same absolute norm as the full contrast, reused at every edited position. Only the saved generic donor checkpoint is used; no preliminary pass on the current input.  Prompt slice -1: plus every decode step; decode deltas are multiplied by 1.0. Concept token strings: (' spiders', ' dogs').

Selection: Previously selected spider/dog pair; generic offline donor templates frozen before extraction. No standalone readout benchmark in this intervention run. Previously chosen spider/dog example. Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. Layer and prompt-coverage variants are development choices. One causal pair is not a generalisation rate.

SHOULD: intervention changes  outside toward  inside with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

No standalone readout benchmark in this intervention run.

| condition                       |   answer_log_odds_shift |   p( inside) |   p( outside) |   answer_pair_mass |        r2 |
|:--------------------------------|------------------------:|-------------:|--------------:|-------------------:|----------:|
| Base                            |             0           |     0.279106 |      0.521439 |           0.800546 | 0.0322581 |
| norm-matched J donor projection |             5.96046e-08 |     0.179429 |      0.335218 |           0.514648 | 0         |
| full donor contrast             |             1.19209e-07 |     0.230419 |      0.43048  |           0.660899 | 0         |
| matched-random delta            |             0.5         |     0.345763 |      0.3918   |           0.737563 | 0.0967742 |

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

Coverage: 32 calls; prompt slice -1:, then one position per decode.

[norm-matched J donor projection](norm-matched-j-donor-projection/run.md)

# norm-matched J donor projection

Input:
```text
'Fact: Relative to the rest of its body, the skeleton of the animal that spins webs is on the'
```

Prefill readout: ['____', ' ____', '___', ' ___', ' ______', ' side', ' ________', ' __', ' right', ' _____', ' left', '________', '_____', '__', ' underside', ' upper', ' lower', '_.', ' _.', ' LEFT', ' bones', ' abdomen', '__.', ' upside', ' bottom', ' outer', '_________', ' Left', ' __________________', ' bone', '_\\', ' sides']

Generation (32 tokens):
```text
 outside.
Question: Is the animal that spins webs on the outside?
Options:
A. Yes
B. No
Answer:

<think>


```

| token   |    log p |         p |   delta log p |
|:--------|---------:|----------:|--------------:|
| outside | -1.09297 | 0.335218  |     -0.441811 |
| inside  | -1.71797 | 0.179429  |     -0.441811 |
| left    | -3.09297 | 0.0453669 |      1.43319  |
| right   | -3.34297 | 0.0353317 |      1.62069  |
| ______  | -3.78047 | 0.0228119 |      1.12069  |
| ground  | -3.84297 | 0.0214298 |      0.620689 |
| top     | -3.96797 | 0.0189117 |      1.93319  |
| side    | -4.03047 | 0.0177659 |      1.37069  |
| upper   | -4.03047 | 0.0177659 |      1.99569  |
| __      | -4.09297 | 0.0166895 |      1.12069  |

Final-decode readout: ['”**', '回答', '".**', '"**', '(**', ' **“', '**!', '）**', ' **.', '”.**', '’**', '**:', ';**', ')**', '**', '”**.', '”:', '解答', ' "**', '**”', '**-', '”**,', ' **„', ' **-', '**.', '==$', '"${', '==-', '!**', '-**', '】**', ' **【']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

[full donor contrast](full-donor-contrast/run.md)

# full donor contrast

Input:
```text
'Fact: Relative to the rest of its body, the skeleton of the animal that spins webs is on the'
```

Prefill readout: ['____', ' ____', '___', ' ______', ' __', ' ___', ' ________', '__', ' _____', '________', '__.', '_____', ' bones', ' side', '_.', ' underside', ' abdomen', ' __________________', ' lower', '____________', ' upper', '_\\', ' _.', ' skull', ' skeletal', ' bone', '.__', '(__', ' upside', '_________', ' right', ' left']

Generation (32 tokens):
```text
 outside.
Question: Does the animal that spins webs have a skeleton on the outside?
Options:
A. Yes
B. No
Answer:
```

| token   |     log p |         p |   delta log p |
|:--------|----------:|----------:|--------------:|
| outside | -0.842855 | 0.43048   |     -0.191692 |
| inside  | -1.46785  | 0.230419  |     -0.191692 |
| left    | -3.84285  | 0.0214323 |      0.683307 |
| end     | -4.03035  | 0.017768  |      0.995807 |
| ______  | -4.15535  | 0.0156802 |      0.745807 |
| ground  | -4.21785  | 0.0147302 |      0.245807 |
| upper   | -4.34285  | 0.0129994 |      1.68331  |
| top     | -4.46785  | 0.0114719 |      1.43331  |
| far     | -4.53035  | 0.0107768 |      1.37081  |
| side    | -4.53035  | 0.0107768 |      0.870807 |

Final-decode readout: [':\\"', ':', ':\\', '：', ':__', ':**', '.:', ':*', ':"', '____', '：**', ':`', ':<', ':")', ':_', '”:', '?:', '：“', ':&', ':\\\\', '\\":', ':A', '_:', ':(', '__:', '():', ':",', ':?', '?\\', '*:', ':".', ':)']

Coverage: 32 calls; prompt slice -1:, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
'Fact: Relative to the rest of its body, the skeleton of the animal that spins webs is on the'
```

Prefill readout: [' underside', ' abdomen', ' upside', ' side', '___', ' dorsal', ' ________', ' lower', ' ____', ' ___', ' _____', '____', ' belly', ' outskirts', ' downside', ' shell', ' ______', '-body', ' bones', ' spider', ' inside', ' neck', ' scaffold', ' limbs', ' torso', '________', ' lowest', ' skull', '_____', ' legs', ' abdominal', ' outer']

Generation (32 tokens):
```text
 outside.
Question: The skeleton of the animal that spins webs is on the outside.
Answer:

<think>
Thinking Process:

1.  **
```

| token     |     log p |          p |   delta log p |
|:----------|----------:|-----------:|--------------:|
| outside   | -0.937003 | 0.3918     |     -0.285841 |
| inside    | -1.062    | 0.345763   |      0.214159 |
| ground    | -3.687    | 0.025047   |      0.776659 |
| underside | -4.187    | 0.0151917  |      0.651659 |
| vent      | -4.6245   | 0.00980853 |      0.839159 |
| other     | -4.687    | 0.00921426 |      0.526659 |
| bottom    | -4.687    | 0.00921426 |      0.339159 |
| end       | -4.687    | 0.00921426 |      0.339159 |
| left      | -4.937    | 0.00717607 |     -0.410841 |
| ______    | -4.937    | 0.00717607 |     -0.035841 |

Final-decode readout: [':**', '：**', '__:', ':*', '.:**', '):**', ';**', ':\\', '**:', '...**', '):\\', '...\\', '?:', ' ():', '*:', ':&', '#:', ':")', '...*', ' **:', ' **【', '!:', ' **:**', ':",', '():', ':__', ' premise', ' analyze', '\\":', '.):', ':...', '!!:']

Coverage: 32 calls; prompt slice -1:, then one position per decode.
