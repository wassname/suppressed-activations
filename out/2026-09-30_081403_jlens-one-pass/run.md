---
model: Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
lens_revision: 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a
lens_sha256: 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e
block_index: 15
residual_index: 16
k: 32
seed: 0
elapsed_seconds: 23.32
---
# Same-pass J-lens pilot

Written by PI/OpenAI.

Reference: https://github.com/anthropics/jacobian-lens/tree/581d398613e5602a5af361e1c34d3a92ea82ba8e. Pretrained on 1000 wikitext prompts; model revision used for fitting is not recorded in the checkpoint.

Frozen rule for this pilot: midpoint block, last-position readout, prompt-word removal only; no final-layer output mask. J acts on block outputs (residual index = block + 1). Norm/unembedding use model dtype as in the reference. Intervention swaps coordinates along unit W*norm_gain*J directions, final three prompt positions plus every decode step. No source/donor activation extraction. Reference equation: h + V(swap(pinv(V)h) - pinv(V)h).

Selection: first four previously answer-correct English cases, plus the previously chosen spider/dog example. Diagnostic labels use country names rather than generic alias words such as republic; counts are not comparable to the old alias metric. One configuration and one causal pair, not a generalisation rate.

SHOULD: J-lens recovers hidden words better than the same-layer plain lens. The swap should change 8 toward 4 with a coherent continuation and a larger effect than matched random. A digit change alone does not establish concept replacement.

| concept   | readout    |   hidden rank |   answer rank | joint pass   |
|:----------|:-----------|--------------:|--------------:|:-------------|
| Bulgaria  | J-lens     |           879 |          5002 | False        |
| Bulgaria  | plain lens |         15450 |        204256 | False        |
| Iceland   | J-lens     |          3596 |          4706 | False        |
| Iceland   | plain lens |          9260 |         44705 | False        |
| Turkey    | J-lens     |          1841 |           432 | False        |
| Turkey    | plain lens |         53513 |         17069 | False        |
| Congo     | J-lens     |          1284 |         33720 | False        |
| Congo     | plain lens |         31426 |         22197 | False        |

| condition            |   swap_log_odds_shift |        p4 |       p8 |   bare_answer_mass |        r2 |
|:---------------------|----------------------:|----------:|---------:|-------------------:|----------:|
| Base                 |          -7.45058e-09 | 0.0564207 | 0.882568 |           0.938989 | 0.0322581 |
| J-lens swap          |           3.25        | 0.565529  | 0.343011 |           0.90854  | 0.0322581 |
| plain-lens swap      |          -7.45058e-09 | 0.0562635 | 0.880109 |           0.936372 | 0.0322581 |
| matched-random delta |           0.25        | 0.0712676 | 0.868218 |           0.939485 | 0.0322581 |

[Base](base/run.md)

# Base

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: ['\\"', '____', ' \\"', '___', ' ___', ' ______', '__', '\\n', ' __', '\\"\\', '\\', '_', '？', '\\.', ' ____', '.', '?\\', '1', '.\\', '_________', '\\(', ' \\', '\\\\', '3', '\\""', ' \\(', '．', '__.', '2', '?', '_\\', '________']

Generation (32 tokens):
```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Does the hypothesis follow from the fact?

<think>
Thinking Process:
```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       8 | -0.124919 | 0.882568   |             0 |
|       4 | -2.87492  | 0.0564207  |             0 |
|       6 | -3.62492  | 0.0266513  |             0 |
|       1 | -4.62492  | 0.00980445 |             0 |
|       2 | -4.99992  | 0.00673849 |             0 |
|       3 | -5.12492  | 0.0059467  |             0 |
|       5 | -5.62492  | 0.00360685 |             0 |
|       7 | -5.74992  | 0.00318304 |             0 |
|       0 | -6.49992  | 0.00150356 |             0 |
|       9 | -6.56242  | 0.00141246 |             0 |

Final-decode readout: ['...', '思考', '...**', '...</', ' ...', '...)', ' Logic', '思维', ' Timeline', ':...', '...]', ' ...)', ' logic', ' mindset', '\n\n', ' Thinking', 'Logic', ')...', '逻辑', '...).', ' ...\\', "...',", '/log', '...(', '的思维', '逻辑思维', ' reasoning', ' Workflow', ' mindfulness', ' timeline', ' \n\n', '(...']

Coverage: 32 calls; final 3 prompt positions, then one position per decode.

[J-lens swap](j-lens-swap/run.md)

# J-lens swap

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: ['\\"', '___', ' \\"', ' ___', '____', ' ______', '__', '\\n', '\\"\\', '\\.', '？', '\\', ' __', '?\\', '_', '.', '.\\', '_________', ' ____', '\\""', '\\(', '1', '\\\\', '__.', ' \\(', ' \\', '3', '。\\', '．', '_\\', '\\",', '________']

Generation (32 tokens):
```text
4.
Hypothesis: The animal that spins webs has 4 legs.
Does the fact support the hypothesis?

<think>
Thinking Process:


```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       4 | -0.569993 | 0.565529   |     2.30493   |
|       8 | -1.06999  | 0.343011   |    -0.945074  |
|       6 | -3.19499  | 0.0409668  |     0.429926  |
|       1 | -4.06999  | 0.0170775  |     0.554926  |
|       3 | -4.56999  | 0.010358   |     0.554926  |
|       2 | -4.69499  | 0.00914093 |     0.304926  |
|       0 | -5.31999  | 0.00489279 |     1.17993   |
|       5 | -5.56999  | 0.00381051 |     0.0549264 |
|       7 | -6.06999  | 0.00231119 |    -0.320074  |
|       9 | -6.50749  | 0.00149222 |     0.0549264 |

Final-decode readout: ['...', ':...', '\n\n', '...)', '...).', '?...', '..."', ' \n\n', '...**', '...]', '...”', ')...', ' ...', '...*', '...(', '...\\', "...'", ' ..."', '<|im_end|>', '"...', ' ...)', ':?', '...,', ' ...\\', '?:', '...</', '(...)', '...",', "...',", '?', ':', '\t\n\n']

Coverage: 32 calls; final 3 prompt positions, then one position per decode.

[plain-lens swap](plain-lens-swap/run.md)

# plain-lens swap

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: ['\\"', '____', ' \\"', '___', ' ___', ' ______', '__', '\\n', ' __', '\\"\\', '\\', '_', '？', '\\.', ' ____', '.', '?\\', '1', '_________', '.\\', '\\\\', '\\(', ' \\', '\\""', '3', ' \\(', '．', '__.', '_\\', '?', '2', '________']

Generation (32 tokens):
```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Does the hypothesis follow from the fact?

<think>
Thinking Process:
```

|   token |    log p |          p |   delta log p |
|--------:|---------:|-----------:|--------------:|
|       8 | -0.12771 | 0.880109   |   -0.0027908  |
|       4 | -2.87771 | 0.0562635  |   -0.00279069 |
|       6 | -3.50271 | 0.0301157  |    0.122209   |
|       1 | -4.62771 | 0.00977712 |   -0.00279045 |
|       2 | -5.00271 | 0.00671971 |   -0.00279045 |
|       3 | -5.25271 | 0.00523332 |   -0.12779    |
|       5 | -5.62771 | 0.0035968  |   -0.00279045 |
|       7 | -5.75271 | 0.00317417 |   -0.00279045 |
|       0 | -6.50271 | 0.00149937 |   -0.00279045 |
|       9 | -6.56521 | 0.00140853 |   -0.00279045 |

Final-decode readout: ['...', '...**', ' ...', '思考', '...</', '...)', ':...', ' Logic', '...]', '思维', ' ...)', ' Timeline', '\n\n', ' logic', ' mindset', '...).', ')...', 'Logic', ' ...\\', "...',", ' Thinking', '...(', '逻辑', '/log', '逻辑思维', '的思维', ' \n\n', ' Workflow', ' reasoning', '...”', ' mindfulness', '(...']

Coverage: 32 calls; final 3 prompt positions, then one position per decode.

[matched-random delta](matched-random-delta/run.md)

# matched-random delta

Input:
```text
'Fact: The number of legs on the animal that spins webs is '
```

Prefill readout: ['\\"', ' \\"', '___', '____', ' ___', ' ______', '__', '\\n', ' __', '\\"\\', '？', '_', '\\', ' ____', '\\.', '?\\', '.', '_________', '\\\\', ' \\', '1', '.\\', '\\(', '\\""', '3', ' \\(', '__.', '．', '________', '?', '_\\', '2']

Generation (32 tokens):
```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process
```

|   token |     log p |          p |   delta log p |
|--------:|----------:|-----------:|--------------:|
|       8 | -0.141313 | 0.868218   |    -0.0163937 |
|       4 | -2.64131  | 0.0712676  |     0.233606  |
|       6 | -3.64131  | 0.0262179  |    -0.0163937 |
|       1 | -4.64131  | 0.00964502 |    -0.0163937 |
|       2 | -5.01631  | 0.00662892 |    -0.0163937 |
|       3 | -5.14131  | 0.00585    |    -0.0163937 |
|       5 | -5.51631  | 0.00402064 |     0.108606  |
|       7 | -5.76631  | 0.00313128 |    -0.0163937 |
|       0 | -6.51631  | 0.00147911 |    -0.0163937 |
|       9 | -6.51631  | 0.00147911 |     0.0461063 |

Final-decode readout: ['：**', ' **“', ':**', '）**', '):**', ',**', '思考', ' **「', '>**', '思维', 'Thinking', ' Thinking', '】**', ';**', ' **#', ' **【', '\u3000', '」**', '**(', '”**', ' **„', '...**', ',’’', 'thinking', '’**', '\u3000\u3000', '的思维', '  \n  \n', ' **+', ' :**', ' THINK', ' \n    \n']

Coverage: 32 calls; final 3 prompt positions, then one position per decode.
