| transform                                                                       | setting   |   unsaid↑ |   share↑ |   leaked↓ |   found↑ |   transfer found↑ |   tried |
|:--------------------------------------------------------------------------------|:----------|----------:|---------:|----------:|---------:|------------------:|--------:|
| [rise-and-fall, J-lens](scripts/challenge/transforms.py#L148) ★                 | 28        |  **0.96** |     0.97 |      0.01 | **0.93** |              0.00 |       4 |
| [attention output, J-lens](scripts/challenge/transforms.py#L165) ★              | 23        |      0.90 | **0.97** |      0.08 |     0.86 |          **0.06** |       1 |
| [suppressed subspace (rank 32), J-lens](scripts/challenge/transforms.py#L159) ★ | 28        |      0.89 |     0.96 |      0.08 |     0.86 |              0.00 |       4 |
| [J-lens](scripts/challenge/transforms.py#L86) ★                                 | 23        |      0.88 |     0.95 |      0.08 |     0.74 |              0.00 |      12 |
| [rise-and-fall](scripts/challenge/transforms.py#L143) ★                         | 27        |      0.87 |     0.93 |      0.07 |     0.73 |              0.00 |       1 |
| [J-lens minus output subspace](scripts/challenge/transforms.py#L132) ★          | 28/256    |      0.82 |     0.94 |      0.15 |     0.80 |              0.00 |       9 |
| [suppressed subspace (rank 32)](scripts/challenge/transforms.py#L153) ★         | 27        |      0.82 |     0.91 |      0.11 |     0.76 |              0.00 |       1 |
| [write minus top-read](scripts/challenge/transforms.py#L106)                    | 27/256    |      0.79 |     0.83 |      0.05 |     0.64 |              0.00 |       9 |
| *[random subspace (floor)](scripts/challenge/transforms.py#L96)*                | 27/256    |      0.77 |     0.89 |      0.16 |     0.12 |              0.00 |       3 |
| *[plain lens](scripts/challenge/transforms.py#L81) ★*                           | 20        |      0.71 |     0.89 |      0.22 |     0.18 |              0.00 |      12 |
| [plain lens minus output subspace](scripts/challenge/transforms.py#L126)        | 28/64     |      0.67 |     0.90 |      0.30 |     0.66 |              0.00 |       9 |
| [churn](scripts/challenge/transforms.py#L101)                                   | 29/256    |      0.65 |     0.80 |      0.19 |     0.20 |              0.00 |       9 |
| *[fixed list (control)](scripts/challenge/transforms.py#L91) ★*                 | 28        |      0.62 |     0.62 |  **0.00** |     0.00 |              0.00 |       1 |
| [suppressed (AntiPaSTO)](scripts/challenge/transforms.py#L121)                  | 27/1024   |      0.60 |     0.88 |      0.35 |     0.61 |              0.00 |       3 |
| [erased-variance](scripts/challenge/transforms.py#L111)                         | 27/1024   |      0.36 |     0.40 |      0.07 |     0.61 |              0.00 |       3 |
| [weak-readout](scripts/challenge/transforms.py#L116)                            | 27/1024   |      0.24 |     0.64 |      0.69 |     0.26 |              0.00 |       3 |

<sub>Table: test = ar→hi, hi→th, th→ru, ko→ar (74 prompts); each setting chosen on ru→ko. unsaid = share of the top 8 distinct words written in English or Chinese, 0 if any is in the input or output script or is the model's next word. leaked = share of lists with such a word. found = share of lists holding the exact English word without a leak. transfer found = the same on 36 English-only TwoHopFact questions, for the hidden bridge entity. ★ = uses a lens or per-prompt vocabulary scores. Italic = control. 15 prompts skipped because the model's next token was whitespace or punctuation. Commit 2f627e0, [rows](out/2026-10-03_193426_leaderboard/rows.json.gz).</sub>
