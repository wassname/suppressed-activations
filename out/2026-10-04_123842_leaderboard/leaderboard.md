| transform                                                                       | setting   |   found↑ |   leaked↓ |   share↑ |   transfer found↑ |   tried |
|:--------------------------------------------------------------------------------|:----------|---------:|----------:|---------:|------------------:|--------:|
| [rise-and-fall, J-lens](scripts/challenge/transforms.py#L153) ★                 | 28        | **0.93** |      0.01 |     0.97 |              0.00 |       4 |
| [suppressed subspace (rank 32), J-lens](scripts/challenge/transforms.py#L164) ★ | 28        |     0.86 |      0.08 |     0.96 |              0.00 |       4 |
| [attention output, J-lens](scripts/challenge/transforms.py#L170) ★              | 23        |     0.86 |      0.08 | **0.97** |          **0.06** |       1 |
| [churn](scripts/challenge/transforms.py#L106)                                   | 27/1024   |     0.81 |      0.16 |     0.90 |              0.00 |       9 |
| [J-lens minus output subspace](scripts/challenge/transforms.py#L137) ★          | 28/256    |     0.80 |      0.15 |     0.94 |              0.00 |       9 |
| [suppressed subspace (rank 32)](scripts/challenge/transforms.py#L158) ★         | 27        |     0.76 |      0.11 |     0.91 |              0.00 |       1 |
| [J-lens](scripts/challenge/transforms.py#L86) ★                                 | 23        |     0.74 |      0.08 |     0.95 |              0.00 |      12 |
| *[plain lens](scripts/challenge/transforms.py#L81) ★*                           | 27        |     0.73 |      0.24 |     0.90 |              0.00 |      12 |
| [rise-and-fall](scripts/challenge/transforms.py#L148) ★                         | 27        |     0.73 |      0.07 |     0.93 |              0.00 |       1 |
| [write minus top-read](scripts/challenge/transforms.py#L111)                    | 24/1024   |     0.69 |      0.11 |     0.77 |              0.00 |       9 |
| [plain lens minus output subspace](scripts/challenge/transforms.py#L131)        | 28/16     |     0.69 |      0.27 |     0.91 |              0.00 |       9 |
| *[input word, J-lens (control)](scripts/challenge/transforms.py#L96) ★*         | 12        |     0.65 |      0.01 |     0.59 |              0.00 |       4 |
| [erased-variance](scripts/challenge/transforms.py#L116)                         | 27/1024   |     0.62 |      0.07 |     0.40 |              0.00 |       3 |
| [suppressed (AntiPaSTO)](scripts/challenge/transforms.py#L126)                  | 27/1024   |     0.61 |      0.35 |     0.88 |              0.00 |       3 |
| [weak-readout](scripts/challenge/transforms.py#L121)                            | 27/1024   |     0.27 |      0.69 |     0.64 |              0.00 |       3 |
| *[random subspace (floor)](scripts/challenge/transforms.py#L101)*               | 27/256    |     0.18 |      0.16 |     0.89 |              0.00 |       3 |
| *[fixed list (control)](scripts/challenge/transforms.py#L91) ★*                 | 28        |     0.00 |  **0.00** |     0.62 |              0.00 |       1 |

<sub>Table: Qwen3.5-4B. Test = ar→hi, hi→th, th→ru, ko→ar (74 prompts); setting = layer, or layer/rank, chosen on ru→ko. found = share of prompts whose top 8 distinct words include the English word or its Chinese translation, with no word in the input or output script and not the model's next word. leaked = share of lists with such a word. share = top-8 words in Latin or Han script, a weak check (random scores high on it). transfer found = found on 36 English-only TwoHopFact questions, for the hidden bridge entity. ★ = uses a lens or per-prompt vocabulary scores. Italic = control. 15 prompts skipped because the model's next token was whitespace or punctuation. Commit a15182e, [rows](out/2026-10-04_123842_leaderboard/rows.json.gz).</sub>
