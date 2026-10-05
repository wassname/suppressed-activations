# Hidden Thought Challenge: find the concepts in giant inscrutable matrices

<img src="figs/cartoon.png" width="720" alt="Schematic, not data. Title: When a model translates Arabic to Russian, it thinks in English. Subtitle: Challenge: can you isolate the hidden thought, without using a dictionary? Three shaded shapes over layers, each labelled inside: grey ARABIC (input) with قطة كلب, high early, arrow not this; orange ENGLISH (hidden) with cat dog, peaking in the middle, arrow isolate the English part; blue RUSSIAN (output) with кошка собака, rising at the end, arrow or this. A dotted line under the English peak: one layer: a mix of all three.">

In AI models we want to find the thoughts and concepts and planning. It should be possible: unlike humans, we have every single byte of "brain activity" available in giant inscrutable tensors. The problem is that we don't understand them.

The goal is to find a way to isolate the subspace with concepts. We have a nice and quick way to test it.

If we could crack this, it would change everything. We could steer models toward genuine virtue and better character. We could catch them being evaluation-aware and train that out. We could crank up honesty to reveal their true values. We could finally stop guessing and start building deeply aligned, kind, good AI with actual confidence.

## The translation trick

There is a delightful finding from the paper ["Do Llamas Work in English?"](https://arxiv.org/abs/2402.10588). When a multilingual model translates between two non-English languages, say Russian to Korean, it often appears to think in English along the way. It takes a detour through English concepts.

This is our way in. If a model translating Arabic to Hindi reliably activates English words in its hidden states, we have a target to aim at.

<img width="1448" height="1086" alt="Cartoon titled 'How can we find a model's hidden thoughts?', subtitle 'Models can think in English even when translating from French to Chinese.' A French speaker asks a robot 'Peux-tu traduire ceci en chinois ?'. The robot thinks 'Okay — first I understand it in English.' and says to a Chinese speaker '好的，我来翻译成中文。'. Labels: French (input), Model, Chinese (output). Lower panel: a magnifying glass over the robot's head shows English words (understand, translate, answer). Text: 'Knowing that we are looking for English, we can search for general transforms that isolate it.'" src="https://github.com/user-attachments/assets/73da1994-7dd6-41f4-af6b-166a40f3f115" />

<img width="480" alt="Line plot from Wendler et al. (2024), Figure 2: Llama-2-70B translating into Chinese. x-axis: layer 0 to 80; y-axis: logit-lens probability 0 to 1. The English word (orange) is near zero until layer 40, rises to about 0.4 by layer 50, stays there, then falls to zero by layer 80. The Chinese answer (blue) stays near zero until layer 60 and rises to about 0.5 at layer 80. A colour bar on top shows entropy falling from high to low around layer 45." src="https://arxiv.org/html/2402.10588v4/70b_zh_probas_ent.png" />

*Llama-2-70B translating into Chinese ([Wendler et al. 2024](https://arxiv.org/html/2402.10588v4), Fig. 2): the English word (orange) rises mid-network, then falls as the Chinese answer (blue) rises.*

I was searching for a way to test whether [Wes Gurnee's](https://x.com/wesg52)
["suppression neurons"](https://arxiv.org/abs/2401.12181) can be found in the residual
stream.

For the test, I tried to isolate the suppressed English from the output language in the
["Do Llamas Work in English?"](https://arxiv.org/abs/2402.10588) plot.

## The rule: no cheating

Of course we can't cheat and find the English words by looking up English words. We are searching for a calculation that precisely isolates the activation subspace that corresponds to English words, but not to other languages. This way any winning calculation will generalise to other settings.

We use Qwen3.5-4B, a model trained mostly on English and Chinese. We only test translation between Russian, Korean, Arabic, Hindi and Thai. We never use English or Chinese as the input or output language, but if the hidden word shows up in either, we count it.

## Leaderboard

We are looking for internal geometry: a projection or other map of the activations, found without the output head,
token lists or dictionaries, that happens to hold the hidden English words. We use the F1 score to measure which
transform best isolates the hidden English.

| transform                                                                                       |      F1↑ |    90% CI |            Δ vs random |     TPR↑ |     FPR↓ |   English-only F1↑ | fitted on   |
|:------------------------------------------------------------------------------------------------|---------:|----------:|-----------------------:|---------:|---------:|-------------------:|:------------|
| [minus this prompt's early and output states](scripts/challenge/transforms.py#L253)             | **0.92** | 0.89–0.94 | +0.07 (+0.04 to +0.10) |     0.93 |     0.09 |               0.00 | nothing     |
| [layer-change PCA](scripts/challenge/transforms.py#L164)                                        |     0.91 | 0.88–0.93 | +0.06 (+0.03 to +0.09) | **0.95** |     0.14 |               0.00 | WikiText    |
| [net-change PCA (AntiPaSTO without the output-head step)](scripts/challenge/transforms.py#L189) |     0.90 | 0.87–0.92 | +0.05 (+0.02 to +0.08) |     0.93 |     0.14 |               0.00 | WikiText    |
| [layer-change PCs gated by attention](scripts/challenge/transforms.py#L272)                     |     0.89 | 0.86–0.92 | +0.04 (+0.00 to +0.07) |     0.87 |     0.09 |               0.00 | WikiText    |
| [minus output-layer PCA](scripts/challenge/transforms.py#L199)                                  |     0.87 | 0.84–0.90 | +0.02 (-0.01 to +0.05) |     0.91 |     0.19 |               0.00 | WikiText    |
| *[identity (logit lens)](scripts/challenge/transforms.py#L139)*                                 |     0.87 | 0.84–0.90 | +0.02 (-0.01 to +0.05) |     0.93 |     0.22 |               0.03 | nothing     |
| [signed rise-fall coupling](scripts/challenge/transforms.py#L243)                               |     0.85 | 0.82–0.88 | +0.00 (-0.03 to +0.03) |     0.90 |     0.22 |               0.00 | WikiText    |
| *[random subspace (control)](scripts/challenge/transforms.py#L159)*                             |     0.85 | 0.82–0.88 |                        |     0.89 |     0.21 |               0.00 | random seed |
| [signed rise-fall coupling, shuffled (control)](scripts/challenge/transforms.py#L248)           |     0.83 | 0.80–0.87 | -0.01 (-0.04 to +0.02) |     0.88 |     0.23 |               0.00 | WikiText    |
| [MLP write minus next MLP read](scripts/challenge/transforms.py#L169)                           |     0.82 | 0.78–0.86 | -0.02 (-0.07 to +0.02) |     0.73 |     0.05 |               0.00 | nothing     |
| [layer-change PCs gated by rise and fall](scripts/challenge/transforms.py#L262)                 |     0.80 | 0.75–0.84 | -0.05 (-0.09 to -0.00) |     0.71 |     0.07 |               0.00 | WikiText    |
| [output-unexplained residual (ridge)](scripts/challenge/transforms.py#L280)                     |     0.79 | 0.74–0.83 | -0.06 (-0.11 to -0.01) |     0.72 |     0.11 |           **0.03** | WikiText    |
| [added then removed](scripts/challenge/transforms.py#L184)                                      |     0.77 | 0.74–0.81 | -0.08 (-0.11 to -0.04) |     0.85 |     0.36 |               0.00 | WikiText    |
| [variance gone by the output (PCA)](scripts/challenge/transforms.py#L174)                       |     0.71 | 0.66–0.77 | -0.13 (-0.19 to -0.08) |     0.59 |     0.07 |               0.01 | WikiText    |
| *[input word (control)](scripts/challenge/transforms.py#L154)*                                  |     0.44 | 0.37–0.50 | -0.41 (-0.48 to -0.35) |     0.38 |     0.34 |               0.00 | nothing     |
| [variance ratio, layer 27 vs output](scripts/challenge/transforms.py#L305)                      |     0.31 | 0.25–0.37 | -0.54 (-0.60 to -0.48) |     0.27 |     0.46 |               0.00 | WikiText    |
| *[mean WikiText activation (control)](scripts/challenge/transforms.py#L149)*                    |     0.00 | 0.00–0.00 | -0.85 (-0.88 to -0.82) |     0.00 | **0.00** |               0.00 | WikiText    |

Qwen3.5-4B, 149 test prompts (ar→hi, hi→th, th→ru, ko→ar). Each row's layer and rank were chosen on ru→ko only. 90% CI: bootstrap over prompts. Δ vs random: F1 minus the random subspace on the same prompts. English-only F1: 102 two-hop questions (TwoHopFact). [Per-prompt rows](out/2026-10-05_002148_leaderboard/rows.json.gz).

### Reference: methods that use the output head, token scores or the J-lens

| transform                                                                            |      F1↑ |    90% CI |            Δ vs random |     TPR↑ |     FPR↓ |   English-only F1↑ | fitted on        |
|:-------------------------------------------------------------------------------------|---------:|----------:|-----------------------:|---------:|---------:|-------------------:|:-----------------|
| [rise-and-fall, J-lens](scripts/challenge/transforms.py#L226)                        | **0.96** | 0.94–0.98 | +0.11 (+0.08 to +0.14) |     0.93 | **0.01** |               0.05 | J-lens           |
| [calibrated rise-and-fall](scripts/challenge/transforms.py#L286)                     | **0.96** | 0.94–0.98 | +0.11 (+0.08 to +0.14) |     0.93 | **0.01** |               0.00 | WikiText         |
| [calibrated rise-and-fall, attention-weighted](scripts/challenge/transforms.py#L299) |     0.95 | 0.93–0.98 | +0.11 (+0.08 to +0.13) |     0.92 | **0.01** |               0.00 | WikiText         |
| [calibrated rise-and-fall, last line](scripts/challenge/transforms.py#L292)          |     0.94 | 0.91–0.96 | +0.09 (+0.06 to +0.12) |     0.90 |     0.02 |               0.00 | WikiText         |
| [rise-and-fall token span (rank 32), J-lens](scripts/challenge/transforms.py#L237)   |     0.94 | 0.91–0.96 | +0.09 (+0.06 to +0.12) | **0.93** |     0.06 |               0.06 | J-lens           |
| [J-lens minus output-layer PCA](scripts/challenge/transforms.py#L204)                |     0.89 | 0.87–0.92 | +0.05 (+0.02 to +0.08) |     0.91 |     0.13 |               0.03 | J-lens, WikiText |
| [layer-23 attention output, J-lens](scripts/challenge/transforms.py#L318)            |     0.89 | 0.86–0.92 | +0.04 (+0.01 to +0.08) |     0.89 |     0.11 |           **0.09** | J-lens           |
| [AntiPaSTO suppressed subspace](scripts/challenge/transforms.py#L194)                |     0.87 | 0.84–0.90 | +0.02 (-0.01 to +0.06) |     0.87 |     0.12 |               0.00 | WikiText         |
| [J-lens](scripts/challenge/transforms.py#L144)                                       |     0.85 | 0.81–0.89 | +0.00 (-0.04 to +0.04) |     0.79 |     0.07 |               0.01 | J-lens           |
| [rise-and-fall token span (rank 32)](scripts/challenge/transforms.py#L231)           |     0.85 | 0.81–0.88 | +0.00 (-0.04 to +0.04) |     0.82 |     0.11 |               0.00 | nothing          |
| [logit lens minus read and said](scripts/challenge/transforms.py#L310)               |     0.84 | 0.80–0.88 | -0.01 (-0.05 to +0.03) |     0.86 |     0.19 |               0.00 | nothing          |
| [rise-and-fall](scripts/challenge/transforms.py#L221)                                |     0.83 | 0.78–0.87 | -0.02 (-0.07 to +0.02) |     0.74 |     0.06 |               0.00 | nothing          |
| [directions the output head reads least](scripts/challenge/transforms.py#L179)       |     0.50 | 0.44–0.55 | -0.35 (-0.41 to -0.29) |     0.55 |     0.66 |               0.00 | nothing          |

### How it is scored

<img src="figs/scoring.svg" width="720" alt="Line plot, Qwen3.5-4B, 59 test prompts, logit-lens probability by layer at the last token. The hidden word (English or Chinese, orange) is near zero until layer 23, peaks at a median of 0.72 at layer 28, then falls to zero by layer 32. The output language (blue) stays low until layer 29 and reaches about 1 at layer 32. The input language (grey) stays near zero. A dashed line at layer 28 says a transform reads here. The orange curve is labelled positive: in the top 8 is TP, missing is FN. The blue and grey curves are labelled negative: in the top 8 is FP, absent is TN.">

The plot shows probabilities from the plain logit lens. Scoring looks only at the top 8 words after the transform:
the hidden word should be among them, and no input- or output-language word should be.

For each prompt, we take the model's activations, apply the transform to get a score for every token, and keep the top eight words. A transform should ideally catch all the hidden English and none of the input and output language words. If the hidden word (English, or its Chinese translation) is in the top eight, that is a true positive (TP); if we miss it, a false negative (FN). If the method instead shows words from the input language, the output language, or the token the model is about to say, that is a false positive (FP); if it avoids all of those, a true negative (TN). Counting over prompts, F1 = 2TP / (2TP + FP + FN).

Each entry returns a vector in activation space. Only then do we read that vector with the model's output head (the
logit lens), to check which words it holds. "Identity" reads the activations unchanged, so it is the plain logit
lens. The reference table lists methods that use the output head, token scores or the
[J-lens](https://transformer-circuits.pub/2026/workspace/) inside the transform. They show what is possible with
language-specific tools, but they are not entries.

### Where we are

The best geometry so far is also the simplest: take the layer-28 activation and remove the two directions of the
same prompt's layer-22 and output activations (F1 0.92, 0.07 above a random subspace on the same prompts). It needs
no fitting. Removing more of the prompt's own layers (16, 19, 30, 31) did not help on the dev pair. It finds the hidden word as often as the plain logit lens (TPR 0.93), but shows input or output words in
9% of prompts instead of 22%. Layer-change PCA (0.91) and net-change PCA (0.90) come next.

Most other geometry does no better than a random subspace of rank 1024, which keeps most of the logit lens (0.85).
That includes the signed rise-fall coupling, which also scores the same as its shuffled control. The reference rows
show that more is possible: rise-and-fall on calibrated token scores reaches 0.96. The gap between 0.92 and 0.96 is
what geometry has not found yet.

None of the methods work on English-only questions, where the input and output are already English (F1 0.09 at best,
from a reference row). That is the open problem. If we can solve that, we might have a general way to read what a
model thinks.

## Enter

Add a `@geometry` function to [`transforms.py`](scripts/challenge/transforms.py). It gets the activations and returns
a vector in activation space:

```python
@geometry("my subspace", settings=[(27, 256), (28, 256)], fitted="WikiText")
def mine(s, layer, rank):  # s["res"]: residual stream at the last prompt token, [33 layers, 2560]
    return project(bases["my basis"][:, :rank], s["res"][layer])  # a vector, [2560]
```

`s` also holds `"attn"` (layer 23 attention output). Fit any basis in `fit_bases()`. Then run, on one GPU:

```sh
uv run scripts/challenge/score.py  # downloads the model and data on first run
```

Rules:

- Return an activation-space vector. Do not use the output head (unembedding), token ids, logits, word lists,
  dictionaries or language labels. The scorer applies the output head afterwards, only to check the answer.
- You may fit on generic text, like the WikiText sample in `data/challenge/`, and use the model's other weights.
- List each setting you tried in `settings`. They are compared on ru→ko only, then frozen for the test.
- Rows whose 90% intervals overlap are not separated. We may also score entries on language pairs not listed here.

Open an issue or a pull request with your transform and its row, and we will add it to the leaderboard.

## Related work

- [Dumas et al. 2024](https://arxiv.org/abs/2411.08745) use the same word-translation setup and patch activations: "we can change the concept without changing the language and vice versa through activation patching alone."
- [Bayazit et al. 2026](https://arxiv.org/abs/2609.00155) compare probes: "decoding-based probes, which rely on output-space decodability, retain sharper language-specific and more English-biased signals."
- [Schut et al. 2025](https://arxiv.org/abs/2502.15603) find an English pivot in open-ended generation.
- [Wu et al. 2024](https://arxiv.org/abs/2411.04986) describe a shared middle-layer "semantic hub" across languages.
- [Zhong et al. 2025](https://aclanthology.org/2025.findings-acl.1350/) find that models trained on several languages can use more than one latent language.
- [Yang et al. 2024](https://aclanthology.org/2024.acl-long.550.pdf) made TwoHopFact, the English-only questions here.
- [Patchscopes](https://arxiv.org/abs/2401.06102), [LatentQA](https://arxiv.org/abs/2412.08686) and the [tuned lens](https://arxiv.org/abs/2303.08112) are other readouts.

<!-- PI/OpenAI 2026-10-04: table from out/2026-10-05_002148_leaderboard, generated by scripts/challenge/score.py. -->

## Citation

If you use the method or figure, please cite
[`CITATION.cff`](CITATION.cff). GitHub exposes this as **Cite this repository**.

## References

- Gurnee, Wes, et al. ["Universal Neurons in GPT2 Language Models."](https://arxiv.org/abs/2401.12181) 2024.
- Wendler, Chris, et al. ["Do Llamas Work in English? On the Latent Language of Multilingual Transformers."](https://arxiv.org/abs/2402.10588) 2024.
- Gurnee, Wes, et al. ["Verbalizable Representations Form a Global Workspace in Language Models."](https://transformer-circuits.pub/2026/workspace/) 2026.

<!-- Drafted from Michael J. Clark's public thread and edited by PI/claude-opus-4.6 and PI/gpt-5.4.
2026-09-29 restructure by Claudypoo[opus-4.8]: challenge framing, results table, collapsed demos. -->
