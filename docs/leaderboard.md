# Leaderboard details

The short version is in the [README](../README.md). Tables from
[`out/2026-10-05_002148_leaderboard`](../out/2026-10-05_002148_leaderboard/leaderboard.md), made by
[`score.py`](../scripts/challenge/score.py).

## All geometry entries

| transform                                                                                       |      F1↑ |    90% CI |            Δ vs random |     TPR↑ |     FPR↓ |   English-only F1↑ | fitted on   |
|:------------------------------------------------------------------------------------------------|---------:|----------:|-----------------------:|---------:|---------:|-------------------:|:------------|
| [minus this prompt's early and output states](../scripts/challenge/transforms.py#L253)             | **0.92** | 0.89–0.94 | +0.07 (+0.04 to +0.10) |     0.93 |     0.09 |               0.00 | nothing     |
| [layer-change PCA](../scripts/challenge/transforms.py#L164)                                        |     0.91 | 0.88–0.93 | +0.06 (+0.03 to +0.09) | **0.95** |     0.14 |               0.00 | WikiText    |
| [net-change PCA (AntiPaSTO without the output-head step)](../scripts/challenge/transforms.py#L189) |     0.90 | 0.87–0.92 | +0.05 (+0.02 to +0.08) |     0.93 |     0.14 |               0.00 | WikiText    |
| [layer-change PCs gated by attention](../scripts/challenge/transforms.py#L272)                     |     0.89 | 0.86–0.92 | +0.04 (+0.00 to +0.07) |     0.87 |     0.09 |               0.00 | WikiText    |
| [minus output-layer PCA](../scripts/challenge/transforms.py#L199)                                  |     0.87 | 0.84–0.90 | +0.02 (-0.01 to +0.05) |     0.91 |     0.19 |               0.00 | WikiText    |
| *[identity (logit lens)](../scripts/challenge/transforms.py#L139)*                                 |     0.87 | 0.84–0.90 | +0.02 (-0.01 to +0.05) |     0.93 |     0.22 |               0.03 | nothing     |
| [signed rise-fall coupling](../scripts/challenge/transforms.py#L243)                               |     0.85 | 0.82–0.88 | +0.00 (-0.03 to +0.03) |     0.90 |     0.22 |               0.00 | WikiText    |
| *[random subspace (control)](../scripts/challenge/transforms.py#L159)*                             |     0.85 | 0.82–0.88 |                        |     0.89 |     0.21 |               0.00 | random seed |
| [signed rise-fall coupling, shuffled (control)](../scripts/challenge/transforms.py#L248)           |     0.83 | 0.80–0.87 | -0.01 (-0.04 to +0.02) |     0.88 |     0.23 |               0.00 | WikiText    |
| [MLP write minus next MLP read](../scripts/challenge/transforms.py#L169)                           |     0.82 | 0.78–0.86 | -0.02 (-0.07 to +0.02) |     0.73 |     0.05 |               0.00 | nothing     |
| [layer-change PCs gated by rise and fall](../scripts/challenge/transforms.py#L262)                 |     0.80 | 0.75–0.84 | -0.05 (-0.09 to -0.00) |     0.71 |     0.07 |               0.00 | WikiText    |
| [output-unexplained residual (ridge)](../scripts/challenge/transforms.py#L280)                     |     0.79 | 0.74–0.83 | -0.06 (-0.11 to -0.01) |     0.72 |     0.11 |           **0.03** | WikiText    |
| [added then removed](../scripts/challenge/transforms.py#L184)                                      |     0.77 | 0.74–0.81 | -0.08 (-0.11 to -0.04) |     0.85 |     0.36 |               0.00 | WikiText    |
| [variance gone by the output (PCA)](../scripts/challenge/transforms.py#L174)                       |     0.71 | 0.66–0.77 | -0.13 (-0.19 to -0.08) |     0.59 |     0.07 |               0.01 | WikiText    |
| *[input word (control)](../scripts/challenge/transforms.py#L154)*                                  |     0.44 | 0.37–0.50 | -0.41 (-0.48 to -0.35) |     0.38 |     0.34 |               0.00 | nothing     |
| [variance ratio, layer 27 vs output](../scripts/challenge/transforms.py#L305)                      |     0.31 | 0.25–0.37 | -0.54 (-0.60 to -0.48) |     0.27 |     0.46 |               0.00 | WikiText    |
| *[mean WikiText activation (control)](../scripts/challenge/transforms.py#L149)*                    |     0.00 | 0.00–0.00 | -0.85 (-0.88 to -0.82) |     0.00 | **0.00** |               0.00 | WikiText    |

Qwen3.5-4B, 149 test prompts (ar→hi, hi→th, th→ru, ko→ar). Each row's layer and rank were chosen on ru→ko only. 90% CI: bootstrap over prompts. Δ vs random: F1 minus the random subspace on the same prompts. English-only F1: 102 two-hop questions (TwoHopFact). [Per-prompt rows](../out/2026-10-05_002148_leaderboard/rows.json.gz).

### Reference: methods that use the output head, token scores or the J-lens

| transform                                                                            |      F1↑ |    90% CI |            Δ vs random |     TPR↑ |     FPR↓ |   English-only F1↑ | fitted on        |
|:-------------------------------------------------------------------------------------|---------:|----------:|-----------------------:|---------:|---------:|-------------------:|:-----------------|
| [rise-and-fall, J-lens](../scripts/challenge/transforms.py#L226)                        | **0.96** | 0.94–0.98 | +0.11 (+0.08 to +0.14) |     0.93 | **0.01** |               0.05 | J-lens           |
| [calibrated rise-and-fall](../scripts/challenge/transforms.py#L286)                     | **0.96** | 0.94–0.98 | +0.11 (+0.08 to +0.14) |     0.93 | **0.01** |               0.00 | WikiText         |
| [calibrated rise-and-fall, attention-weighted](../scripts/challenge/transforms.py#L299) |     0.95 | 0.93–0.98 | +0.11 (+0.08 to +0.13) |     0.92 | **0.01** |               0.00 | WikiText         |
| [calibrated rise-and-fall, last line](../scripts/challenge/transforms.py#L292)          |     0.94 | 0.91–0.96 | +0.09 (+0.06 to +0.12) |     0.90 |     0.02 |               0.00 | WikiText         |
| [rise-and-fall token span (rank 32), J-lens](../scripts/challenge/transforms.py#L237)   |     0.94 | 0.91–0.96 | +0.09 (+0.06 to +0.12) | **0.93** |     0.06 |               0.06 | J-lens           |
| [J-lens minus output-layer PCA](../scripts/challenge/transforms.py#L204)                |     0.89 | 0.87–0.92 | +0.05 (+0.02 to +0.08) |     0.91 |     0.13 |               0.03 | J-lens, WikiText |
| [layer-23 attention output, J-lens](../scripts/challenge/transforms.py#L318)            |     0.89 | 0.86–0.92 | +0.04 (+0.01 to +0.08) |     0.89 |     0.11 |           **0.09** | J-lens           |
| [AntiPaSTO suppressed subspace](../scripts/challenge/transforms.py#L194)                |     0.87 | 0.84–0.90 | +0.02 (-0.01 to +0.06) |     0.87 |     0.12 |               0.00 | WikiText         |
| [J-lens](../scripts/challenge/transforms.py#L144)                                       |     0.85 | 0.81–0.89 | +0.00 (-0.04 to +0.04) |     0.79 |     0.07 |               0.01 | J-lens           |
| [rise-and-fall token span (rank 32)](../scripts/challenge/transforms.py#L231)           |     0.85 | 0.81–0.88 | +0.00 (-0.04 to +0.04) |     0.82 |     0.11 |               0.00 | nothing          |
| [logit lens minus read and said](../scripts/challenge/transforms.py#L310)               |     0.84 | 0.80–0.88 | -0.01 (-0.05 to +0.03) |     0.86 |     0.19 |               0.00 | nothing          |
| [rise-and-fall](../scripts/challenge/transforms.py#L221)                                |     0.83 | 0.78–0.87 | -0.02 (-0.07 to +0.02) |     0.74 |     0.06 |               0.00 | nothing          |
| [directions the output head reads least](../scripts/challenge/transforms.py#L179)       |     0.50 | 0.44–0.55 | -0.35 (-0.41 to -0.29) |     0.55 |     0.66 |               0.00 | nothing          |

## How it is scored

For each prompt, we take the model's activations, apply the transform to get a score for every token, and keep the top eight words. A transform should ideally catch all the hidden English and none of the input and output language words. If the hidden word (English, or its Chinese translation) is in the top eight, that is a true positive (TP); if we miss it, a false negative (FN). If the method instead shows words from the input language, the output language, or the token the model is about to say, that is a false positive (FP); if it avoids all of those, a true negative (TN). Counting over prompts, F1 = 2TP / (2TP + FP + FN).

Each entry returns a vector in activation space. Only then do we read that vector with the model's output head (the
logit lens), to check which words it holds. "Identity" reads the activations unchanged, so it is the plain logit
lens. The reference table lists methods that use the output head, token scores or the
[J-lens](https://transformer-circuits.pub/2026/workspace/) inside the transform. They show what is possible with
language-specific tools, but they are not entries.

## Where we are

The best geometry so far is also the simplest: take the layer-28 activation and remove the two directions of the
same prompt's layer-22 and output activations (F1 0.92, 0.07 above a random subspace on the same prompts). It needs
no fitting. Removing more of the prompt's own layers (16, 19, 30, 31) did not help on the dev pair. It finds the hidden word as often as the plain logit lens (TPR 0.93), but shows input or output words in
9% of prompts instead of 22%. Layer-change PCA (0.91) and net-change PCA (0.90) come next.

Most other geometry does no better than a random subspace of rank 1024, which keeps most of the logit lens (0.85).
That includes the signed rise-fall coupling, which also scores the same as its shuffled control. The reference rows
show that more is possible: rise-and-fall on calibrated token scores reaches 0.96. The gap between 0.92 and 0.96 is
what geometry has not found yet.

## Per layer

To see how your transform does at every layer, add it to `METHODS` in
[`layer_sweep.py`](../scripts/challenge/layer_sweep.py) (it opens as a notebook) and run it.

<img src="../figs/layers.png" width="900" alt="Three panels over layers 16 to 31, 149 test prompts: F1 with a 90% band, TPR and FPR, for five geometry transforms. All peak around layers 24 to 29 at F1 about 0.85 to 0.92. Net-change PCA (green) rises earliest, F1 0.61 at layer 20 and about 0.89 from layer 24, and falls least by layer 31. Identity (logit lens) and the random subspace are lower in the middle layers. Minus this prompt's x22 and x32 (orange) starts at layer 23 and peaks at 0.92 at layer 28. FPR rises steeply for all at layers 30 to 31.">

Per layer ([`layer_sweep.py`](../scripts/challenge/layer_sweep.py)), net-change PCA is the least sensitive to the choice of
layer: it already reaches F1 0.61 at layer 20, where the logit lens has 0.33. The orange line starts at layer 23
because it removes the layer-22 state. By layer 31 every method shows the output language (FPR rises).

<!-- Moved from the README by PI/OpenAI, 2026-10-05, when wassname asked for a shorter README. -->
