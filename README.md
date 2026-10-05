# Hidden Thought Challenge: find the concepts in giant inscrutable matrices

<img src="figs/cartoon.png" width="720" alt="Schematic, not data. Title: When a model translates Arabic to Russian, it thinks in English. Subtitle: Challenge: can you isolate the hidden thought, without using a dictionary? Three shaded shapes over layers, each labelled inside: grey ARABIC (input) with قطة كلب, high early, arrow not this; orange ENGLISH (hidden) with cat dog, peaking in the middle, arrow isolate the English part; blue RUSSIAN (output) with кошка собака, rising at the end, arrow or this. A dotted line under the English peak: one layer: a mix of all three.">

In AI models we want to find the thoughts and concepts and planning. It should be possible: unlike humans, we have every single byte of "brain activity" available in giant inscrutable tensors. The problem is that we don't understand them.

The goal is to find a way to isolate the subspace with concepts. We have a nice and quick way to test it.

If we could crack this, it would change many things. We could steer models toward genuine concepts like virtue using their own capable internal concepts. 

## How we test it: translation

There is a delightful finding from the paper ["Do Llamas Work in English?"](https://arxiv.org/abs/2402.10588). When a multilingual model translates between two non-English languages, say Russian to Korean, it often appears to think in English along the way. It takes a detour through English concepts.

This is our way in. If a model translating Arabic to Hindi reliably activates English words in its hidden states, we have a target to aim at.

<details><summary>Background: the "Do Llamas Work in English?" plot</summary>

I was searching for a way to test whether [Wes Gurnee's](https://x.com/wesg52)
["suppression neurons"](https://arxiv.org/abs/2401.12181) can be found in the residual
stream.

For the test, I tried to isolate the suppressed English from the output language in the
["Do Llamas Work in English?"](https://arxiv.org/abs/2402.10588) plot.

<img width="480" alt="Line plot from Wendler et al. (2024), Figure 2: Llama-2-70B translating into Chinese. x-axis: layer 0 to 80; y-axis: logit-lens probability 0 to 1. The English word (orange) is near zero until layer 40, rises to about 0.4 by layer 50, stays there, then falls to zero by layer 80. The Chinese answer (blue) stays near zero until layer 60 and rises to about 0.5 at layer 80. A colour bar on top shows entropy falling from high to low around layer 45." src="https://arxiv.org/html/2402.10588v4/70b_zh_probas_ent.png" />

*Llama-2-70B translating into Chinese ([Wendler et al. 2024](https://arxiv.org/html/2402.10588v4), Fig. 2): the English word (orange) rises mid-network, then falls as the Chinese answer (blue) rises.*

<img width="1448" height="1086" alt="Cartoon titled 'How can we find a model's hidden thoughts?', subtitle 'Models can think in English even when translating from French to Chinese.' A French speaker asks a robot 'Peux-tu traduire ceci en chinois ?'. The robot thinks 'Okay — first I understand it in English.' and says to a Chinese speaker '好的，我来翻译成中文。'. Labels: French (input), Model, Chinese (output). Lower panel: a magnifying glass over the robot's head shows English words (understand, translate, answer). Text: 'Knowing that we are looking for English, we can search for general transforms that isolate it.'" src="https://github.com/user-attachments/assets/73da1994-7dd6-41f4-af6b-166a40f3f115" />

</details>

## No dictionaries

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
| *[identity (logit lens)](scripts/challenge/transforms.py#L139)*                                 |     0.87 | 0.84–0.90 | +0.02 (-0.01 to +0.05) |     0.93 |     0.22 |               0.03 | nothing     |
| *[random subspace (control)](scripts/challenge/transforms.py#L159)*                             |     0.85 | 0.82–0.88 |                        |     0.89 |     0.21 |               0.00 | random seed |

Qwen3.5-4B, 149 test prompts (ar→hi, hi→th, th→ru, ko→ar). Each row's layer and rank were chosen on ru→ko only. 90% CI: bootstrap over prompts. Δ vs random: F1 minus the random subspace on the same prompts. English-only F1: 102 two-hop questions (TwoHopFact). [Per-prompt rows](out/2026-10-05_002148_leaderboard/rows.json.gz). [Full table, reference methods and per-layer results](docs/leaderboard.md).

<img src="figs/scoring.svg" width="720" alt="Line plot, Qwen3.5-4B, 59 test prompts, logit-lens probability by layer at the last token. The hidden word (English or Chinese, orange) is near zero until layer 23, peaks at a median of 0.72 at layer 28, then falls to zero by layer 32. The output language (blue) stays low until layer 29 and reaches about 1 at layer 32. The input language (grey) stays near zero. A dashed line at layer 28 says a transform reads here. The orange curve is labelled positive: in the top 8 is TP, missing is FN. The blue and grey curves are labelled negative: in the top 8 is FP, absent is TN.">

For each prompt we keep the transform's top 8 words. The hidden word (orange) should be among them; words from the
input or output language (grey, blue) should not. F1 combines the two.
<!-- Short scoring note and the README cut by PI/OpenAI, 2026-10-05; the details moved to docs/leaderboard.md. -->

The best geometry so far is also the simplest: take the layer-28 activation and remove the two directions of the
same prompt's layer-22 and output activations (F1 0.92, 0.07 above a random subspace on the same prompts). It needs
no fitting.

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
