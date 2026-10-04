# Suppressed Activation Challenges: Find Where Llamas Work

<img width="1448" height="1086" alt="Cartoon titled 'How can we find a model's hidden thoughts?', subtitle 'Models can think in English even when translating from French to Chinese.' A French speaker asks a robot 'Peux-tu traduire ceci en chinois ?'. The robot thinks 'Okay — first I understand it in English.' and says to a Chinese speaker '好的，我来翻译成中文。'. Labels: French (input), Model, Chinese (output). Lower panel: a magnifying glass over the robot's head shows English words (understand, translate, answer). Text: 'Knowing that we are looking for English, we can search for general transforms that isolate it.'" src="https://github.com/user-attachments/assets/73da1994-7dd6-41f4-af6b-166a40f3f115" />

I was searching for a way to test whether [Wes Gurnee's](https://x.com/wesg52)
["suppression neurons"](https://arxiv.org/abs/2401.12181) can be found in the residual
stream.

For the test, I tried to isolate the suppressed English from the output language in the
["Do Llamas Work in English?"](https://arxiv.org/abs/2402.10588) plot.

<img width="480" alt="Line plot from Wendler et al. (2024), Figure 2: Llama-2-70B translating into Chinese. x-axis: layer 0 to 80; y-axis: logit-lens probability 0 to 1. The English word (orange) is near zero until layer 40, rises to about 0.4 by layer 50, stays there, then falls to zero by layer 80. The Chinese answer (blue) stays near zero until layer 60 and rises to about 0.5 at layer 80. A colour bar on top shows entropy falling from high to low around layer 45." src="https://arxiv.org/html/2402.10588v4/70b_zh_probas_ent.png" />

*Llama-2-70B translating into Chinese ([Wendler et al. 2024](https://arxiv.org/html/2402.10588v4), Fig. 2): the English word (orange) rises mid-network, then falls as the Chinese answer (blue) rises.*

## The challenge

In AI models we want to find the thoughts and concepts and planning. It should be possible: unlike humans, we have every single byte of "brain activity" available in giant inscrutable tensors. The problem is that we don't understand them.

If we could crack this, it would change everything. We could steer models toward genuine virtue and better character. We could catch them being evaluation-aware and train that out. We could crank up honesty to reveal their true values. We could finally stop guessing and start building deeply aligned, kind, good AI with actual confidence.

### The translation trick

There is a delightful finding from the paper ["Do Llamas Work in English?"](https://arxiv.org/abs/2402.10588). When a multilingual model translates between two non-English languages, say Russian to Korean, it often appears to think in English along the way. It takes a detour through English concepts.

This is our way in. If a model translating Arabic to Hindi reliably activates English words in its hidden states, we have a target to aim at.

### The rule: no cheating

Of course we can't cheat and find the English words by looking up English words. We are searching for a calculation that precisely isolates the activation subspace that corresponds to English words, but not to other languages. This way any winning calculation will generalise to other settings.

We use Qwen3.5-4B, a model trained mostly on English and Chinese. We only test translation between Russian, Korean, Arabic, Hindi and Thai. We never use English or Chinese as the input or output language, but if the hidden word shows up in either, we count it.

## Leaderboard

We use the F1 score to measure which transform best isolates the hidden English.

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

### How it is scored

For each prompt, we take the model's activations, apply the transform to get a score for every token, and keep the top eight words. A transform should ideally catch all the hidden English and none of the input and output language words. If the hidden word (English, or its Chinese translation) is in the top eight, that is a true positive (TP); if we miss it, a false negative (FN). If the method instead shows words from the input language, the output language, or the token the model is about to say, that is a false positive (FP); if it avoids all of those, a true negative (TN). Counting over prompts, F1 = 2TP / (2TP + FP + FN).

The logit lens applies the model's output head directly to a layer's activations. Rise-and-fall scores words whose logit rises from layer 22 to a later layer and falls by the output. The [J-lens](https://transformer-circuits.pub/2026/workspace/) first maps a layer to the last layer with a large learned matrix from outside the model, so its rows are in a separate table.

### Where we are

The plain logit lens finds the hidden word about as often as the best methods (TPR 0.93). But in about a fifth of prompts it also shows input or output words (FPR 0.22).

The italic rows are controls: the logit lens, the input word itself, a random subspace, and the mean WikiText activation, which ignores the prompt. They tell us whether a method finds something or just gets lucky. A random subspace of rank 1024 (of 2560) keeps most of the logit lens and scores 0.85. Among the simple methods, only layer-change PCA (0.88–0.93) is clear of it.

None of the methods work yet on English-only questions, where the input and output are already English (F1 0.09 at best). That is the open problem. If we can solve that, we might have a general way to read what a model thinks.

## Enter

Add a function to [`transforms.py`](scripts/challenge/transforms.py):

```python
@transform("my transform", settings=[(27,), (28,)], fitted="nothing")
def mine(s, layer):  # s["res"]: residual stream at the last prompt token, [33 layers, 2560]
    return readout(s["res"][layer])  # a score for each vocabulary token
```

`s` also holds `"attn"` (layer 23 attention output) and `"logits"` (the model's next-token logits). Then run, on one GPU:

```sh
uv run scripts/challenge/score.py  # downloads the model and data on first run
```

Rules:

- Use only `s["res"]`, `s["attn"]` and `s["logits"]`. (`s["input"]` is there for the input-word control only.)
- No word lists, language labels or test prompts. You may fit on generic text, like the WikiText sample in `data/challenge/`.
- List each setting you tried in `settings`. They are compared on ru→ko only, then frozen for the test.
- Entries that use a learned matrix from outside the model, like the J-lens, go in the J-lens table.
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

<!-- PI/OpenAI 2026-10-04: table from out/2026-10-04_182050_leaderboard, generated by scripts/challenge/score.py. -->

## Citation

If you use the method or figure, please cite
[`CITATION.cff`](CITATION.cff). GitHub exposes this as **Cite this repository**.

## References

- Gurnee, Wes, et al. ["Universal Neurons in GPT2 Language Models."](https://arxiv.org/abs/2401.12181) 2024.
- Wendler, Chris, et al. ["Do Llamas Work in English? On the Latent Language of Multilingual Transformers."](https://arxiv.org/abs/2402.10588) 2024.
- Gurnee, Wes, et al. ["Verbalizable Representations Form a Global Workspace in Language Models."](https://transformer-circuits.pub/2026/workspace/) 2026.

<!-- Drafted from Michael J. Clark's public thread and edited by PI/claude-opus-4.6 and PI/gpt-5.4.
2026-09-29 restructure by Claudypoo[opus-4.8]: challenge framing, results table, collapsed demos. -->
