# Fixed boundary development test

— PI/OpenAI. Post2718 rule; same captures, masks and heads. Two reciprocal translations share cloud. Native translation wrapper is new. No unseen or semantic-success claim. Preclue uses final-output direction/full-input masks too.

| Group                 | Method                                           | Lexical joint↑   |   Unscored |
|:----------------------|:-------------------------------------------------|:-----------------|-----------:|
| English non-geography | end-pass input-prefix erased0.5 J-lens           | 2/4              |          0 |
| English non-geography | end-pass input-prefix erased0.5 plain24          | 0/4              |          0 |
| English non-geography | end-pass input-prefix erased0.5 plain27          | 2/4              |          0 |
| English non-geography | end-pass input-prefix J-lens                     | 2/4              |          0 |
| English non-geography | end-pass boundary input-prefix J-lens            | 3/4              |          0 |
| English non-geography | end-pass boundary input-prefix erased0.5 J-lens  | 3/4              |          0 |
| English non-geography | end-pass boundary input-prefix erased0.5 plain24 | 0/4              |          0 |
| English non-geography | end-pass boundary input-prefix erased0.5 plain27 | 3/4              |          0 |
| English non-geography | end-pass preclue input-prefix J-lens             | 0/4              |          0 |
| English non-geography | end-pass preclue input-prefix erased0.5 J-lens   | 0/4              |          0 |
| English non-geography | end-pass preclue input-prefix erased0.5 plain24  | 0/4              |          0 |
| English non-geography | end-pass preclue input-prefix erased0.5 plain27  | 0/4              |          0 |
| translation           | end-pass input-prefix erased0.5 J-lens           | 1/2              |          1 |
| translation           | end-pass input-prefix erased0.5 plain24          | 1/2              |          1 |
| translation           | end-pass input-prefix erased0.5 plain27          | 1/2              |          1 |
| translation           | end-pass input-prefix J-lens                     | 1/2              |          1 |
| translation           | end-pass boundary input-prefix J-lens            | 0/2              |          1 |
| translation           | end-pass boundary input-prefix erased0.5 J-lens  | 0/2              |          1 |
| translation           | end-pass boundary input-prefix erased0.5 plain24 | 0/2              |          1 |
| translation           | end-pass boundary input-prefix erased0.5 plain27 | 0/2              |          1 |
| translation           | end-pass preclue input-prefix J-lens             | 0/2              |          1 |
| translation           | end-pass preclue input-prefix erased0.5 J-lens   | 0/2              |          1 |
| translation           | end-pass preclue input-prefix erased0.5 plain24  | 0/2              |          1 |
| translation           | end-pass preclue input-prefix erased0.5 plain27  | 0/2              |          1 |

All exact inputs, continuations and72 full lists: /workspace/2026/suppressed-activations/out/2026-10-01_160913_jlens-one-pass/run.md
