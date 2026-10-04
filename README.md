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

In AI models we want to find the thoughts and concepts and planning. It should be possible: unlike humans, we have every single byte of "brain activity" available in giant inscrutable tensors. The problem is that we don't understand them. If we could understand them, we could increase the model's virtue to give it a better character, see if it's eval aware (and make it not aware in a game or test), we could turn up honesty to find true values, and many other alignment tools to help us develop good, kind, deeply aligned models. 

Here we have a nice setup. In the famous paper ["Do Llamas Work in English?"](https://arxiv.org/abs/2402.10588) they showed that a model translating from X to Y thinks in English. In this setting we know that many of the inner concepts correspond to English, so this gives us a really nice way to read the model's mind and find the parts of their activations that correspond to English words.

Of course we can't cheat and find the English words by looking up English words. We are searching for a calculation that precisely isolates the activation subspace that corresponds to English words, but not to other languages. This way any winning calculation will generalise to other settings.

We test on translation between Russian, Korean, Arabic, Hindi and Thai. Qwen is trained mostly on English
and Chinese, so we use neither as the input or the output, and count the hidden word if it is
found in English or Chinese.

## Leaderboard

We use the F1 score to measure which transform best isolates the hidden English.

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

### How it is scored

A transform should ideally catch all the hidden English and none of the input and output language words. So we
frame it as classification on the transform's top 8 words for each prompt. If they include the hidden word
(English, or its Chinese translation), that is a true positive (TP); if not, a false negative (FN). If they
include an input or output word (any word in those languages, or the word the model is about to say), that is a
false positive (FP); if not, a true negative (TN). Counting over prompts, F1 = 2TP / (2TP + FP + FN).

A transform takes the activations from one forward pass and gives every token a score. Most rows use a lens to
turn a layer's activations into token scores. The logit lens applies the model's output head directly; the
[J-lens](https://transformer-circuits.pub/2026/workspace/) first maps the layer to the last layer. Rise-and-fall
scores words whose score rises from layer 22 to that layer and falls by the output.

The italic rows are controls: the plain logit lens; the input word read through the J-lens (no hidden step
needed); a random subspace; and a fixed list that ignores the prompt.

The plain lens finds the hidden word as often as the best rows (TPR 0.96) but shows input or output words in
a quarter of prompts (FPR 0.24). A random subspace of rank 1024 (of 2560) keeps most of the plain lens and scores
nearly as well, so subspace rows of that rank need to beat it. No row works on the English-only questions yet.
That is the open part.

## Enter

Add a function to [`transforms.py`](scripts/challenge/transforms.py):

```python
@transform("my transform", settings=[(27,), (28,)], per_prompt=False)
def mine(s, layer):  # s["res"]: residual stream at the last prompt token, [33 layers, 2560]
    return readout(s["res"][layer])  # a score for each vocabulary token
```

`s` also holds `"attn"` (layer 23 attention output) and `"logits"` (the model's next-token logits). Your transform
must not use word lists or language labels. Then run, on one GPU:

```sh
uv run scripts/challenge/make_word_lists.py  # once
uv run scripts/challenge/score.py            # about 7 minutes
```

Open an issue or a pull request with your transform and its row, and we will add it to the leaderboard.

## Related work

- [Dumas et al. 2024](https://arxiv.org/abs/2411.08745) use the same word-translation setup and patch activations: "we can change the concept without changing the language and vice versa through activation patching alone."
- [Bayazit et al. 2026](https://arxiv.org/abs/2609.00155) compare probes: "decoding-based probes, which rely on output-space decodability, retain sharper language-specific and more English-biased signals."
- [Schut et al. 2025](https://arxiv.org/abs/2502.15603) find an English pivot in open-ended generation.
- [Wu et al. 2024](https://arxiv.org/abs/2411.04986) describe a shared middle-layer "semantic hub" across languages.
- [Zhong et al. 2025](https://aclanthology.org/2025.findings-acl.1350/) find that models trained on several languages can use more than one latent language.
- [Yang et al. 2024](https://aclanthology.org/2024.acl-long.550.pdf) made TwoHopFact, the English-only questions here.
- [Patchscopes](https://arxiv.org/abs/2401.06102), [LatentQA](https://arxiv.org/abs/2412.08686) and the [tuned lens](https://arxiv.org/abs/2303.08112) are other readouts.

<!-- PI/OpenAI 2026-10-04: table from out/2026-10-04_140611_leaderboard, generated by scripts/challenge/score.py; not yet reviewed by wassname. -->

## Citation

If you use the method or figure, please cite
[`CITATION.cff`](CITATION.cff). GitHub exposes this as **Cite this repository**.

## References

- Gurnee, Wes, et al. ["Universal Neurons in GPT2 Language Models."](https://arxiv.org/abs/2401.12181) 2024.
- Wendler, Chris, et al. ["Do Llamas Work in English? On the Latent Language of Multilingual Transformers."](https://arxiv.org/abs/2402.10588) 2024.
- Gurnee, Wes, et al. ["Verbalizable Representations Form a Global Workspace in Language Models."](https://transformer-circuits.pub/2026/workspace/) 2026.

<!-- Drafted from Michael J. Clark's public thread and edited by PI/claude-opus-4.6 and PI/gpt-5.4.
2026-09-29 restructure by Claudypoo[opus-4.8]: challenge framing, results table, collapsed demos. -->
