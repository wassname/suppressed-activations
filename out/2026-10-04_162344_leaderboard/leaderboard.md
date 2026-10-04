| transform                                                                      |      F1↑ |     TPR↑ |     FPR↓ |   English-only F1↑ | setting   |   tried |
|:-------------------------------------------------------------------------------|---------:|---------:|---------:|-------------------:|:----------|--------:|
| [layer-change PCA](scripts/challenge/transforms.py#L112)                       | **0.90** | **0.96** |     0.16 |               0.00 | 27/1024   |       9 |
| *[logit lens](scripts/challenge/transforms.py#L87)*                            |     0.87 | **0.96** |     0.24 |               0.00 | 27        |      12 |
| [AntiPaSTO suppressed subspace](scripts/challenge/transforms.py#L137)          |     0.86 |     0.88 |     0.16 |               0.00 | 27/1024   |       3 |
| [logit lens minus output-layer PCA](scripts/challenge/transforms.py#L142)      |     0.85 |     0.95 |     0.27 |               0.00 | 28/16     |       9 |
| [rise-and-fall token span (rank 32)](scripts/challenge/transforms.py#L169) ★   |     0.85 |     0.82 |     0.11 |               0.00 | 27        |       1 |
| *[random subspace (control)](scripts/challenge/transforms.py#L107)*            |     0.85 |     0.93 |     0.26 |               0.00 | 27/1024   |       3 |
| [rise-and-fall](scripts/challenge/transforms.py#L159) ★                        |     0.83 |     0.76 |     0.07 |               0.00 | 27        |       1 |
| [MLP write minus next MLP read](scripts/challenge/transforms.py#L117)          |     0.82 |     0.77 |     0.11 |               0.00 | 24/1024   |       9 |
| [added then removed](scripts/challenge/transforms.py#L132)                     |     0.82 |     0.93 |     0.35 |               0.00 | 27/1024   |       3 |
| [variance gone by the output (PCA)](scripts/challenge/transforms.py#L122)      |     0.77 |     0.66 |     0.07 |               0.00 | 27/1024   |       3 |
| [directions the output head reads least](scripts/challenge/transforms.py#L127) |     0.52 |     0.59 |     0.69 |               0.00 | 27/1024   |       3 |
| *[input word (control)](scripts/challenge/transforms.py#L102)*                 |     0.43 |     0.35 |     0.27 |               0.00 | 8         |       4 |
| *[mean WikiText activation (control)](scripts/challenge/transforms.py#L97)*    |     0.00 |     0.00 | **0.00** |               0.00 | 28        |       1 |

<sub>Table: Qwen3.5-4B. Test = ar→hi, hi→th, th→ru, ko→ar (74 prompts); setting = layer, or layer/rank, chosen on ru→ko. TP, FN, FP, TN as in the README, counted over prompts; F1 = 2TP/(2TP+FP+FN). English-only F1 = F1 on 36 English-only TwoHopFact questions, where the hidden word is the bridge entity and input/output words are the question's words and its answer. ★ = picks tokens per prompt from vocabulary scores. Italic = control. 15 prompts skipped because the model's next token was whitespace or punctuation. Commit 96ec735, [rows](out/2026-10-04_162344_leaderboard/rows.json.gz).</sub>

### Using the J-lens

| transform                                                                            |      F1↑ |     TPR↑ |     FPR↓ |   English-only F1↑ | setting   |   tried |
|:-------------------------------------------------------------------------------------|---------:|---------:|---------:|-------------------:|:----------|--------:|
| [rise-and-fall, J-lens](scripts/challenge/transforms.py#L164) ★                      | **0.97** | **0.95** | **0.01** |               0.00 | 28        |       4 |
| [rise-and-fall token span (rank 32), J-lens](scripts/challenge/transforms.py#L175) ★ |     0.93 | **0.95** |     0.08 |               0.00 | 28        |       4 |
| [layer-23 attention output, J-lens](scripts/challenge/transforms.py#L181)            |     0.91 |     0.91 |     0.08 |           **0.10** | 23        |       1 |
| [J-lens minus output-layer PCA](scripts/challenge/transforms.py#L148)                |     0.90 |     0.93 |     0.15 |               0.00 | 28/256    |       9 |
| [J-lens](scripts/challenge/transforms.py#L92)                                        |     0.86 |     0.81 |     0.08 |               0.00 | 23        |      12 |
