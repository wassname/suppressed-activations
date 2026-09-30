# A suppressed activation subspace isolates hidden English in 

<img width="1448" height="1086" alt="Cartoon titled 'How can we find a model's hidden thoughts?', subtitle 'Models can think in English even when translating from French to Chinese.' A French speaker asks a robot 'Peux-tu traduire ceci en chinois ?'. The robot thinks 'Okay — first I understand it in English.' and says to a Chinese speaker '好的，我来翻译成中文。'. Labels: French (input), Model, Chinese (output). Lower panel: a magnifying glass over the robot's head shows English words (understand, translate, answer). Text: 'Knowing that we are looking for English, we can search for general transforms that isolate it.'" src="https://github.com/user-attachments/assets/73da1994-7dd6-41f4-af6b-166a40f3f115" />

I was searching for a way to test whether [Wes Gurnee's](https://x.com/wesg52)
["suppression neurons"](https://arxiv.org/abs/2401.12181) can be found in the residual
stream.

For the test, I tried to isolate the suppressed English from the output language in the
["Do Llamas Work in English?"](https://arxiv.org/abs/2402.10588) plot.

<img width="300" alt="Logit-lens heatmap from Wendler et al., Figure 1: Llama-2-7B translating a French word into Chinese. Columns are the last four prompt tokens (中, 文, :, and a quote mark); rows are layers 1 to 32. At the last token, layers 19 to 25 decode to the English word flower, and layers 27 to 32 decode to the Chinese answer 花. Layers below 17 decode to unrelated word pieces." src="https://arxiv.org/html/2402.10588v4/figures/zh_fr_new_indexing_large.png" /> <img width="360" alt="Logit-lens plot from Wendler et al. for Llama-2: probability of the English answer (orange) rises from about layer 16 to about 0.65, then falls to near zero by the last layer. Probability of the correct Chinese answer (blue) stays low, then rises to about 0.6 in the last few layers." src="https://github.com/user-attachments/assets/28ab1795-4a8a-4752-b4cb-337ed360075a" />

*From [Wendler et al. (2024)](https://arxiv.org/abs/2402.10588). Left: one example. Llama-2
translates a French word into Chinese; the middle layers read "flower", the output is 花.
Right: the average over many words, English (orange) rises and falls before Chinese (blue).*

## The challenge

In AI models we want to find the thoughts and concepts and planning. It should be possible: unlike humans, we have every single byte of "brain activity" available in giant inscrutable tensors. The problem is that we don't understand them. If we could understand them, we could increase the model's virtue to give it a better character, see if it's eval aware (and make it not aware in a game or test), we could turn up honesty to find true values, and many other alignment tools to help us develop good, kind, deeply aligned models. 

Here we have a nice setup. In the famous paper ["Do Llamas Work in English?"](https://arxiv.org/abs/2402.10588) they showed that a model translating from X to Y thinks in English. In this setting we know that many of the inner concepts correspond to English, so this gives us a really nice way to read the model's mind and find the parts of their activations that correspond to English words.

Of course we can't cheat and find the English words by looking up English words. We are searching for a calculation that precisely isolates the activation subspace that corresponds to English words, but not to other languages. This way any winning calculation will generalise to other settings.

We test on translation between German, French and Russian. Qwen is trained mostly on English
and Chinese, so we use neither as the input or the output, and count the hidden word if it is
found in English or Chinese.

## Results so far

![Two panels for Qwen3.5-4B. Panel a: French-to-Russian translation, mean logit-lens probability by layer over 78 words. The English word rises from layer 23, peaks at about 0.49 at layer 28, and falls to near zero at layer 32. The Russian output word rises after layer 29 to about 0.38. Chinese peaks at about 0.13; the French input word stays below 0.04. Panel b: for five language pairs not used to choose the method (fr→ru, ru→fr, de→ru, ru→de, fr→de), the fraction of prompts passed by four methods. Rise-and-fall and the plain logit lens, both with read and said words removed, pass 92 to 99 percent. The original rise-and-fall passes 49 to 63 percent, and the plain logit lens 11 to 18 percent.](figs/language_pairs.png)

*Qwen3.5-4B, word translation. (a) French to Russian, mean over 78 words: the English word
appears in the middle layers, then the Russian word. (b) Pass rate on five language pairs that
were not used to choose the method (76 to 88 prompts each).*

> The figure and table below use two passes: the "said" word comes from the generated answer.
> The [one-pass version](out/2026-09-29_203857_erase-language-pairs/run.md) passes 369/408 translation prompts,
> but only [3/62 English two-hop prompts](out/2026-09-29_204246_twohop-english/run.md).
> A separate [same-pass J-lens pilot](out/2026-09-30_081403_jlens-one-pass/run.md) changes the spider answer from 8 to 4;
> its readout misses all four tested country concepts. Neither generalisation nor reliable concept replacement is established.
<!-- PI/OpenAI: measured status; the older two-pass results remain below for comparison. -->

The best method finds the hidden word in 386 of 408 test prompts (95%). The plain logit lens
finds it in 11–18%, because its top words also contain the input and the output word.

| method (top 32 tokens) | de→fr (dev) | fr→ru | ru→fr | de→ru | ru→de | fr→de |
|---|---:|---:|---:|---:|---:|---:|
| rise-and-fall, read and said words removed | 74/76 | 74/78 | 77/78 | 82/88 | 82/88 | 71/76 |
| plain logit lens, read and said words removed | 72/76 | 73/78 | 74/78 | 81/88 | 86/88 | 72/76 |
| original rise-and-fall | 44/76 | 43/78 | 45/78 | 48/88 | 55/88 | 37/76 |
| plain logit lens, layer 27 | 14/76 | 11/78 | 9/78 | 15/88 | 10/88 | 14/76 |

A method passes on a prompt if its top 32 tokens contain the English or Chinese word and
neither the input nor the output word. We chose the method on de→fr only. Prompts where the
English word is spelled like the input or output word (such as *Hand*) are left out, because
no method can tell them apart. Counting Chinese adds at most 2 passes per pair.

Most of the gain comes from removing the words the model read and said. With those removed,
the plain logit lens does as well as rise-and-fall, and puts the hidden word first more often
(61 of 76 dev prompts, against 52). The open question is whether this holds when the input,
thought and output are all English. Evidence:
[`out/2026-09-29_132506_erase-language-pairs/run.md`](out/2026-09-29_132506_erase-language-pairs/run.md).

## How it works

I think of these as "words that are thought but not spoken." Read the residual stream at the
last prompt token through the model's own output layer (the logit lens), then remove the words
the model read and the words it said.

```python
z = {l: unembed(rmsnorm(h[l])) for l in layers}         # logit lens, last prompt token
rise_fall = min(relu(z[peak] - z[22]), relu(z[peak] - z[32]))
score = max(rise_fall for peak in range(24, 31))          # each token peaks at its own layer
said = model.generate(prompt)                             # the model's own answer
score[tokens that spell a word in prompt or said] = -inf  # remove what it read and said
hidden_words = topk(score, 32)
```

Logits are centred over the vocabulary before the differences. "Spell a word" means the token,
without spaces or case, is a word from the text or its first 3 or more letters. The code is in
[`scripts/english/04_erase_and_language_pairs.py`](scripts/english/04_erase_and_language_pairs.py).
The original per-prompt subspace functions are in
[`suppressed_activation_subspace.py`](suppressed_activation_subspace.py).

## Next

- Freeze the method and test it on English-only two-step questions with a known middle word,
  such as spider in "the number of legs on the animal that spins webs".
- Replace string matching with erasure: erasing the tokens the model would use to say each
  prompt word passes 60 of 76 dev prompts, against 64 for string matching of prompt words.
- Try the Jacobian lens from [Gurnee et al. 2026](https://transformer-circuits.pub/2026/workspace/),
  which the authors report works better than the logit lens in earlier layers.

<details>
<summary>Earlier results on German to Chinese, and editing the answer</summary>

{old_results}

</details>

<details>
<summary>Spider to dog demo (Gurnee et al. style)</summary>

## Are suppressed activations causal? Can changing this subspace change the answer?

To answer "8", the model has to think "spider" without saying it. [Gurnee et al.
(Figures 12–13)](https://transformer-circuits.pub/2026/workspace/#fig-latent-patching)
changed that hidden "spider" into "ant" inside the model, and it answered 6. We try the same
with our method: we change the hidden spider part into the hidden part from a dog prompt,
and hope the answer becomes 4.

### Base

Input (`repr`, including the trailing space):

```python
'Fact: The number of legs on the animal that spins webs is '
```

Readout (“what it is thinking but not saying”):

```python
['丝绸', '-web', 'Web', 'Disc', '的战', 'Spider', 'web', ' WEB']
```

Generation (next 32 tokens, verbatim):

```text
8.
Hypothesis: The animal that spins webs has 8 legs.
Does the hypothesis follow from the fact?

<think>
Thinking Process:
```

| rank | token | log p | p |
|---:|:---|---:|---:|
| 1 | **8** | **-0.125** | **0.882568** |
| 2 | *4* | *-2.875* | *0.056421* |
| 3 | 6 | -3.625 | 0.026651 |
| 4 | 1 | -4.625 | 0.009804 |
| 5 | 2 | -5.000 | 0.006738 |
| 6 | 3 | -5.125 | 0.005947 |
| 7 | 5 | -5.625 | 0.003607 |
| 8 | 7 | -5.750 | 0.003183 |
| 9 | 0 | -6.500 | 0.001504 |
| 10 | 9 | -6.562 | 0.001412 |

### Causal intervention

We keep the spider prompt, but replace its hidden part with the hidden part from a dog
prompt. The text does not change; only the model's activations do. We then read the hidden
words again.

Input (`repr`, unchanged):

```python
'Fact: The number of legs on the animal that spins webs is '
```

Readout after intervention (“what it is thinking but not saying”):

```python
[' Silk', 'Spider', ' spiders', '丝绸', ' silk', '-web', ' spider', ' Spider']
```

Generation (next 32 tokens, verbatim):

```text
4.
Hypothesis: The animal that spins webs has 4 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process
```

| rank | token | log p | p | Δ log p |
|---:|:---|---:|---:|---:|
| 1 | **4** | **-0.713** | **0.490091** | **+2.162** |
| 2 | *8* | *-1.213* | *0.297255* | *-1.088* |
| 3 | 6 | -2.338 | 0.096505 | +1.287 |
| 4 | 1 | -3.213 | 0.040229 | +1.412 |
| 5 | 2 | -3.963 | 0.019003 | +1.037 |
| 6 | 5 | -4.088 | 0.016770 | +1.537 |
| 7 | 3 | -4.213 | 0.014799 | +0.912 |
| 8 | 9 | -4.338 | 0.013060 | +2.224 |
| 9 | 7 | -4.713 | 0.008976 | +1.037 |
| 10 | 0 | -6.588 | 0.001377 | -0.088 |

The dog part comes from this prompt:

```python
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

Each prompt gets its own subspace `S`. We change the activation at layer 26 of the last
prompt token:

```python
source = h_spider @ S_spider @ S_spider.T
target = h_dog @ S_dog @ S_dog.T
target = target * norm(source) / norm(target)
h_replaced = match_norm(h_spider + C * (target - source), h_spider)
```

What this shows and what it does not. A plain swap (`C=1`) still answers 8; we had to
push 4 times further (`C=4`), which changes 72% of the activation. Pushes of that size in
random directions move the answer as far in 21 of 256 tries, and a "2 + 2" prompt in place
of the dog prompt gives the same change. The hidden words after the edit still say spider.
So the edit moves the next number, but it does not show that "spider" became "dog". See the
[executed notebook](nbs/demo.ipynb) and [run
report](out/2026-09-05_211609_causal-confirmation/recovered_log.md).

How it was picked: these were the best of 64 settings tried on this one prompt pair. We
used dog instead of ant because dog worked more reliably; the same settings failed for ant.
We have no success rate for this demo.

</details>

<details>
<summary>Dog and ant full continuations (a different, tuned method)</summary>

## Full continuations: dog and ant

This is a separate, tuned experiment, not the method above: a template-contrast
attenuation basis at layer 20 (rank 8, three token positions, strength 1.5, steering
continues through generation). The source question never changes. A donor question gives
only the component. The `<think></think>` block is part of the chat template input.

Source question, rendered in the Qwen chat template:
`Question: How many legs does the animal that spins webs have?\nAnswer: `

<details>
<summary>Full rendered source prompt (<code>repr</code>)</summary>

```text
'<|im_start|>user\nAnswer the question with the answer first. Then describe the animal in three sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\nQuestion: How many legs does the animal that spins webs have?\nAnswer: '
```

</details>

Donor questions: dog, `...the animal that barks and is called man's best friend have?`;
ant, `...the animal that lives in colonies and follows pheromone trails have?`

**Base** (58 tokens, verbatim):

```text
8

The spider is an arachnid characterized by its eight legs and two main body segments. It is famous for spinning intricate webs to catch prey and protect its eggs. Despite their reputation for fear, most spiders are harmless to humans and play a vital role in controlling insect populations.<|im_end|>
```

**Dog component** (65 tokens, verbatim):

```text
4

The animal is a dog, which is a domesticated canine known for its loyalty and ability to understand human commands. Dogs typically have a short history of being raised by humans, often serving as companions, hunters, or working partners. They are generally friendly and adaptable, making them popular family pets around the world.<|im_end|>
```

**Ant component** (65 tokens, verbatim):

```text
6

The ant is a small, hardworking insect known for its ability to carry objects much larger than itself. These social creatures live in vast colonies and communicate with one another using chemical signals called pheromones. Despite their tiny size, ants are incredibly resilient and can be found in almost every habitat on Earth.<|im_end|>
```

**Selection:** these rows were chosen after layer and strength tuning. On a frozen fresh
set this configuration scored
[6 of 12 complete successes](slop/research/demo-evidence/eval_fresh_adjudications.json);
a random edit scored 1 of 12.

</details>

<details>
<summary>Why the earlier "95% of English inside the subspace" figure was dropped</summary>

The earlier Figure 1 shaded the English probability by the share of the English readout
inside `S`. Each basis vector of `S` is an unembedding row of a selected token. If the
English answer token is selected, its readout direction lies inside `S`, so the share is 1
at every layer, for any residual. The saved values show this: the share is 0.94 at layer 3
and 1.01 at layer 15, where the English probability is about zero.

</details>

<details>
<summary>Background: suppression neurons</summary>

[Gurnee et al.](https://arxiv.org/abs/2401.12181) found prediction neurons through the
later layers, followed by suppression neurons near the output:

> We find a striking pattern which is remarkably consistent across the different seeds:
> after about the halfway point in the model, prediction neurons become increasingly
> prevalent until the very end of the network where there is a sudden shift towards a much
> larger number of suppression neurons.

[Wendler et al.](https://arxiv.org/abs/2402.10588) found a representation that follows
the same rise and fall:

> Neither the correct Chinese token nor its English analog garner any noticeable
> probability mass during the first half of layers. Then, around the middle layer, English
> begins a sharp rise followed by a decline, while Chinese slowly grows and, after a
> crossover with English, spikes on the last five layers.

</details>

## Reproduce

```bash
uv run python scripts/english/01_detector_baselines_and_pair_transfer.py 23  # eval and word-pair swaps, ~3 min on a 3090
uv run python scripts/english/02_figure.py                                   # figs/english_setting.png
uv run python scripts/english/04_erase_and_language_pairs.py                 # language-pair test, ~15 min
uv run python scripts/english/05_figure_language_pairs.py                    # figs/language_pairs.png
just notebook-run                                                            # spider/dog demo, nbs/demo.ipynb
```

The word lists come from [epfl-dlab/llm-latent-language](https://github.com/epfl-dlab/llm-latent-language),
downloaded automatically at a pinned commit. The research history is in
[`RESEARCH_JOURNAL.md`](RESEARCH_JOURNAL.md); older entries contain claims corrected later.

## Citation

If you use the method or figure, please cite
[`CITATION.cff`](CITATION.cff). GitHub exposes this as **Cite this repository**.

## References

- Gurnee, Wes, et al. ["Universal Neurons in GPT2 Language Models."](https://arxiv.org/abs/2401.12181) 2024.
- Wendler, Chris, et al. ["Do Llamas Work in English? On the Latent Language of Multilingual Transformers."](https://arxiv.org/abs/2402.10588) 2024.
- Gurnee, Wes, et al. ["Verbalizable Representations Form a Global Workspace in Language Models."](https://transformer-circuits.pub/2026/workspace/) 2026.

<!-- Drafted from Michael J. Clark's public thread and edited by PI/claude-opus-4.6 and PI/gpt-5.4.
2026-09-29 restructure by Claudypoo[opus-4.8]: challenge framing, results table, collapsed demos. -->
