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

Each row is a transform: one forward pass in, a score for every token out. The model translates between two
languages that share no letters with English or Chinese (Russian, Korean, Arabic, Hindi, Thai). A row
passes a prompt if its top 8 words include the English word for the meaning, or its Chinese translation, and
none of the 8 is from the input or output language or is the word the model is about to say.

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

Reading the input word itself, before any hidden step, already scores 0.65, so rows below that line may only read the input. No row finds the hidden word in English-only questions yet (transfer found is about 0). That is the open part.

To enter, add a function to [`transforms.py`](scripts/challenge/transforms.py):

```python
@transform("my transform", settings=[(27,), (28,)], lens_based=False)
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

- [Dumas et al. 2024](https://arxiv.org/abs/2411.08745), same word-translation setup: "we can change the concept without changing the language and vice versa through activation patching alone." Patching, not a readout.
- [Bayazit et al. 2026](https://arxiv.org/abs/2609.00155): "decoding-based probes, which rely on output-space decodability, retain sharper language-specific and more English-biased signals." Every row here reads through the output head, so this applies.
- [Schut et al. 2025](https://arxiv.org/abs/2502.15603): English pivot in open-ended generation.
- [Wu et al. 2024, Semantic Hub](https://arxiv.org/abs/2411.04986): a shared middle-layer space across languages.
- [Zhong et al. 2025](https://aclanthology.org/2025.findings-acl.1350/): models trained on several languages can use more than one latent language. This is why Chinese counts as hidden.
- [Yang et al. 2024, TwoHopFact](https://aclanthology.org/2024.acl-long.550.pdf): the English-only transfer questions.
- [Patchscopes](https://arxiv.org/abs/2401.06102), [LatentQA](https://arxiv.org/abs/2412.08686), [tuned lens](https://arxiv.org/abs/2303.08112): other readouts. The first two need a second prompt or a trained decoder; the tuned lens is trained to predict the output, so it would read what is said.

We did not find an earlier leaderboard of label-free readouts scored this way.

<!-- PI/OpenAI 2026-10-04: table from out/2026-10-04_123842_leaderboard, generated by scripts/challenge/score.py; not yet reviewed by wassname. -->

## Citation

If you use the method or figure, please cite
[`CITATION.cff`](CITATION.cff). GitHub exposes this as **Cite this repository**.

## References

- Gurnee, Wes, et al. ["Universal Neurons in GPT2 Language Models."](https://arxiv.org/abs/2401.12181) 2024.
- Wendler, Chris, et al. ["Do Llamas Work in English? On the Latent Language of Multilingual Transformers."](https://arxiv.org/abs/2402.10588) 2024.
- Gurnee, Wes, et al. ["Verbalizable Representations Form a Global Workspace in Language Models."](https://transformer-circuits.pub/2026/workspace/) 2026.

<!-- Drafted from Michael J. Clark's public thread and edited by PI/claude-opus-4.6 and PI/gpt-5.4.
2026-09-29 restructure by Claudypoo[opus-4.8]: challenge framing, results table, collapsed demos. -->
