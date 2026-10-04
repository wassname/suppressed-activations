| transform                                                                       |      F1↑ |     TPR↑ |     FPR↓ |   English-only F1↑ | setting   |   tried |
|:--------------------------------------------------------------------------------|---------:|---------:|---------:|-------------------:|:----------|--------:|
| [rise-and-fall, J-lens](scripts/challenge/transforms.py#L153) ★                 | **0.97** |     0.95 |     0.01 |               0.00 | 28        |       4 |
| [suppressed subspace (rank 32), J-lens](scripts/challenge/transforms.py#L164) ★ |     0.93 |     0.95 |     0.08 |               0.00 | 28        |       4 |
| [attention output, J-lens](scripts/challenge/transforms.py#L170) ★              |     0.91 |     0.91 |     0.08 |           **0.10** | 23        |       1 |
| [churn](scripts/challenge/transforms.py#L106)                                   |     0.90 | **0.96** |     0.16 |               0.00 | 27/1024   |       9 |
| [J-lens minus output subspace](scripts/challenge/transforms.py#L137) ★          |     0.90 |     0.93 |     0.15 |               0.00 | 28/256    |       9 |
| *[plain lens](scripts/challenge/transforms.py#L81) ★*                           |     0.87 | **0.96** |     0.24 |               0.00 | 27        |      12 |
| [J-lens](scripts/challenge/transforms.py#L86) ★                                 |     0.86 |     0.81 |     0.08 |               0.00 | 23        |      12 |
| [plain lens minus output subspace](scripts/challenge/transforms.py#L131)        |     0.85 |     0.95 |     0.27 |               0.00 | 28/16     |       9 |
| [suppressed subspace (rank 32)](scripts/challenge/transforms.py#L158) ★         |     0.85 |     0.82 |     0.11 |               0.00 | 27        |       1 |
| *[random subspace (floor)](scripts/challenge/transforms.py#L101)*               |     0.85 |     0.93 |     0.26 |               0.00 | 27/1024   |       3 |
| [rise-and-fall](scripts/challenge/transforms.py#L148) ★                         |     0.83 |     0.76 |     0.07 |               0.00 | 27        |       1 |
| [write minus top-read](scripts/challenge/transforms.py#L111)                    |     0.82 |     0.77 |     0.11 |               0.00 | 24/1024   |       9 |
| [suppressed (AntiPaSTO)](scripts/challenge/transforms.py#L126)                  |     0.82 |     0.93 |     0.35 |               0.00 | 27/1024   |       3 |
| *[input word, J-lens (control)](scripts/challenge/transforms.py#L96) ★*         |     0.78 |     0.65 |     0.01 |               0.00 | 12        |       4 |
| [erased-variance](scripts/challenge/transforms.py#L116)                         |     0.77 |     0.66 |     0.07 |               0.00 | 27/1024   |       3 |
| [weak-readout](scripts/challenge/transforms.py#L121)                            |     0.52 |     0.59 |     0.69 |               0.00 | 27/1024   |       3 |
| *[fixed list (control)](scripts/challenge/transforms.py#L91) ★*                 |     0.00 |     0.00 | **0.00** |               0.00 | 28        |       1 |

<sub>Table: Qwen3.5-4B. Test = ar→hi, hi→th, th→ru, ko→ar (74 prompts); setting = layer, or layer/rank, chosen on ru→ko. TP, FN, FP, TN as in the README, counted over prompts; F1 = 2TP/(2TP+FP+FN). English-only F1 = F1 on 36 English-only TwoHopFact questions, where the hidden word is the bridge entity and input/output words are the question's words and its answer. ★ = uses a lens or per-prompt vocabulary scores. Italic = control. 15 prompts skipped because the model's next token was whitespace or punctuation. Commit 3544d46, [rows](out/2026-10-04_140611_leaderboard/rows.json.gz).</sub>
