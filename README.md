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

## Results so far

![Three panels for Qwen3.5-4B, German-to-Chinese word translation. Panel a: logit-lens probability by layer; the English word rises at layers 24 to 27 and falls to zero at layer 32; the Chinese word rises to about 0.6 at layer 32. Panel b: for four selectors, the fraction of 120 prompts whose top-32 tokens contain the English word, the Chinese word, the German word, and the English word without the other two. Rise-and-fall has the highest isolation, about 0.47. The plain logit lens contains Chinese in about 0.87 of prompts. Panel c: fraction of 50 word pairs where replacing a component at the last prompt token makes the model output the other word's Chinese translation, for 8-layer windows starting at layers 15, 19, 23 and 25. Replacing the whole residual vector works best, the Chinese-token directions reach 1.0 at layers 25 to 32, the rise-and-fall selector reaches 0.44, and random edits stay at 0.](figs/english_setting.png)

*Qwen3.5-4B on 120 German-to-Chinese word prompts. (a) The English word appears in the middle
layers before the Chinese word. (b) Black bars are passes: English found, Chinese and German
left out. (c) Replacing the found component with another word's component, by layer window.*

The method below finds the hidden word and passes on 56 of 120 prompts. The plain logit
lens passes on 4, because it also returns the Chinese word the model is about to say.

| method (top 32 tokens) | passes | English in | Chinese (said) in | German (input) in |
|---|---:|---:|---:|---:|
| rise-and-fall, best peak layer per token (24–30), prompt words removed | **92/120** | 95 | 4 | 0 |
| rise-and-fall (this repo) | 56/120 | 94 | 3 | 37 |
| fall only | 51/120 | 69 | 2 | 17 |
| plain logit lens, layer 27 | 4/120 | 116 | 105 | 70 |

With the original method, 37 of the 64 failures contain the German input word, such as
` Herz` or ` Licht`: it finds words that are read or thought and then not said, and the input
is one of those. The top row fixes this by dropping any token that spells a word from the
prompt, and lets each token peak at its own layer. We picked it from 42 variants on half the
prompts (46/60) and it scored the same on the other half (46/60). 8 of its 28 failures are
words spelled the same in German and English (Hand, Ball, Person), which no method can tell
apart from the input. Evidence: [`out/2026-09-29_115749_selector-search/run.md`](out/2026-09-29_115749_selector-search/run.md).

Replacing the found component with another word's component changes
the output word in 16 of 50 fixed word pairs. Random edits of the same size change 0 of 50.
Using the Chinese answer tokens' own directions works better (41 of 50), so the English
component is not the best place to edit.

The heart to school demo below was hand-picked; the same setup works for 16 of the 50
pairs. The spider to dog demo (collapsed below) was the best of 64 settings on one prompt
pair, and the same settings did not work for spider to ant.

```text
Base:         心" (xīn), which means "heart" in English.
Heart→school: 学校" (xué xiào), which means "school" in English. This is a common mistake, as "
```

Evidence: [`out/2026-09-29_070913_english-baselines-L23/run.md`](out/2026-09-29_070913_english-baselines-L23/run.md).

## How it works

I think of these as "words that are thought but not spoken." For each sample, project the
residual stream into vocabulary space and find token logits that rise in the middle but
fall before they can be sampled.

```python
z_early, z_peak, z_output = unembed(rmsnorm(h[[early, peak, output]]))  # layers 22, 27, 32

rise = center_over_vocab(z_peak - z_early)
fall = center_over_vocab(z_peak - z_output)
suppressed_score = minimum(relu(rise), relu(fall))

suppressed_tokens = topk(suppressed_score, k=32)
S = orthogonal_basis(center(unembedding[suppressed_tokens]).T)
h_suppressed = h @ S @ S.T
```

A token scores high only if its logit both rose and then fell. `h` is the residual stream at
the last prompt token. The PyTorch functions are in
[`suppressed_activation_subspace.py`](suppressed_activation_subspace.py).

## Next

- Leave out tokens that already appear in the prompt. This uses no language information and
  should remove most German errors.
- Choose the layers by a fixed rule instead of from the English curve.
- Try the Jacobian lens from [Gurnee et al. 2026](https://transformer-circuits.pub/2026/workspace/),
  which the authors report works better than the logit lens in earlier layers.
- Freeze the best method and test it on English-only two-step questions with a known middle
  word, such as spider in "the number of legs on the animal that spins webs".

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
