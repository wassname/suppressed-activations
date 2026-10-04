| transform                                                                      |      F1↑ |    90% CI |     TPR↑ |     FPR↓ |   English-only F1↑ | setting   |   tried |
|:-------------------------------------------------------------------------------|---------:|----------:|---------:|---------:|-------------------:|:----------|--------:|
| [layer-change PCA](scripts/challenge/transforms.py#L112)                       | **0.91** | 0.88–0.93 | **0.95** |     0.14 |               0.00 | 27/1024   |       9 |
| [AntiPaSTO suppressed subspace](scripts/challenge/transforms.py#L137)          |     0.87 | 0.84–0.90 |     0.87 |     0.12 |               0.00 | 27/1024   |       3 |
| [logit lens minus output-layer PCA](scripts/challenge/transforms.py#L142)      |     0.87 | 0.84–0.90 |     0.91 |     0.19 |               0.00 | 28/16     |       9 |
| *[logit lens](scripts/challenge/transforms.py#L87)*                            |     0.87 | 0.84–0.90 |     0.93 |     0.22 |           **0.03** | 27        |      12 |
| [rise-and-fall token span (rank 32)](scripts/challenge/transforms.py#L169) ★   |     0.85 | 0.81–0.88 |     0.82 |     0.11 |               0.00 | 27        |       1 |
| *[random subspace (control)](scripts/challenge/transforms.py#L107)*            |     0.85 | 0.82–0.88 |     0.89 |     0.21 |               0.00 | 27/1024   |       3 |
| [rise-and-fall](scripts/challenge/transforms.py#L159) ★                        |     0.83 | 0.78–0.87 |     0.74 |     0.06 |               0.00 | 27        |       1 |
| [MLP write minus next MLP read](scripts/challenge/transforms.py#L117)          |     0.82 | 0.78–0.86 |     0.73 |     0.05 |               0.00 | 27/256    |       9 |
| [added then removed](scripts/challenge/transforms.py#L132)                     |     0.77 | 0.74–0.81 |     0.85 |     0.36 |               0.00 | 27/1024   |       3 |
| [variance gone by the output (PCA)](scripts/challenge/transforms.py#L122)      |     0.71 | 0.66–0.77 |     0.59 |     0.07 |               0.01 | 27/1024   |       3 |
| [directions the output head reads least](scripts/challenge/transforms.py#L127) |     0.50 | 0.44–0.55 |     0.55 |     0.66 |               0.00 | 27/1024   |       3 |
| *[input word (control)](scripts/challenge/transforms.py#L102)*                 |     0.44 | 0.37–0.50 |     0.38 |     0.34 |               0.00 | 8         |       4 |
| *[mean WikiText activation (control)](scripts/challenge/transforms.py#L97)*    |     0.00 | 0.00–0.00 |     0.00 | **0.00** |               0.00 | 28        |       1 |

<sub>Table: Qwen3.5-4B. Test = ar→hi, hi→th, th→ru, ko→ar (149 prompts); setting = layer, or layer/rank. Each row's settings (tried) are compared only on ru→ko, a pair not in the test, so trying more settings does not see the test prompts. 90% CI = bootstrap over test prompts. TP, FN, FP, TN as in the README, counted over prompts; F1 = 2TP/(2TP+FP+FN). English-only F1 = F1 on 102 English-only TwoHopFact questions, where the hidden word is the bridge entity and input/output words are the question's words and its answer. ★ = picks tokens per prompt from vocabulary scores. Italic = control. 49 prompts skipped because the model's next token was whitespace or punctuation. Commit b2dff57c, [rows](out/2026-10-04_182050_leaderboard/rows.json.gz).</sub>

### Using the J-lens

| transform                                                                            |      F1↑ |    90% CI |     TPR↑ |     FPR↓ |   English-only F1↑ | setting   |   tried |
|:-------------------------------------------------------------------------------------|---------:|----------:|---------:|---------:|-------------------:|:----------|--------:|
| [rise-and-fall, J-lens](scripts/challenge/transforms.py#L164) ★                      | **0.96** | 0.94–0.98 |     0.93 | **0.01** |               0.05 | 28        |       4 |
| [rise-and-fall token span (rank 32), J-lens](scripts/challenge/transforms.py#L175) ★ |     0.94 | 0.91–0.96 | **0.93** |     0.06 |               0.06 | 28        |       4 |
| [J-lens minus output-layer PCA](scripts/challenge/transforms.py#L148)                |     0.89 | 0.87–0.92 |     0.91 |     0.13 |               0.03 | 28/256    |       9 |
| [layer-23 attention output, J-lens](scripts/challenge/transforms.py#L181)            |     0.89 | 0.86–0.92 |     0.89 |     0.11 |           **0.09** | 23        |       1 |
| [J-lens](scripts/challenge/transforms.py#L92)                                        |     0.85 | 0.81–0.89 |     0.79 |     0.07 |               0.01 | 23        |      12 |
