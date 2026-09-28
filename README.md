# A suppressed activation subspace isolates hidden English in 

<img width="1448" height="1086" alt="Cartoon titled 'How can we find a model's hidden thoughts?', subtitle 'Models can think in English even when translating from French to Chinese.' A French speaker asks a robot 'Peux-tu traduire ceci en chinois ?'. The robot thinks 'Okay — first I understand it in English.' and says to a Chinese speaker '好的，我来翻译成中文。'. Labels: French (input), Model, Chinese (output). Lower panel: a magnifying glass over the robot's head shows English words (understand, translate, answer). Text: 'Knowing that we are looking for English, we can search for general transforms that isolate it.'" src="https://github.com/user-attachments/assets/73da1994-7dd6-41f4-af6b-166a40f3f115" />

<img width="292" height="184" alt="Logit-lens plot from Wendler et al. for Llama-2: probability of the English answer (orange) rises from about layer 16 to about 0.65, then falls to near zero by the last layer. Probability of the correct Chinese answer (blue) stays low, then rises to about 0.6 in the last few layers." src="https://github.com/user-attachments/assets/28ab1795-4a8a-4752-b4cb-337ed360075a" />

*When Llama-2 translates to Chinese, the logit lens reads the English word in the middle
layers, then the Chinese word at the output
([Wendler et al. 2024](https://arxiv.org/abs/2402.10588)).*

## Status · 2026-09-29 · draft

The goal is a method that finds what a model thinks but does not say, in any setting,
including settings where the input, the thought, and the output are all English.

In an all-English setting we cannot score such a method, because the hidden word and the
said word look the same. German-to-Chinese translation gives an answer key: the input is
German, the hidden thought is English, and the said output is Chinese. The method never
uses language. We use language only to score it: did it find the English word and exclude
the Chinese word?

| claim | status |
|---|---|
| **Readout:** find the hidden word, exclude the said word | Partly works on the translation eval: 56 of 120 prompts isolate the English word (plain logit lens: 4 of 120). The main error is selecting the German input word (37 of 120). |
| **Editing:** replacing the found component changes the answer | Secondary. Unsupervised rank-8 swap: 16 of 50 word pairs (random edit: 0 of 50). |
| **Generalisation:** the same frozen method on all-English tasks | Not tested on a fixed set yet. One example: the spider prompt readout contains `Spider`. |

---

I was searching for a way to test whether [Wes Gurnee's](https://x.com/wesg52)
["suppression neurons"](https://arxiv.org/abs/2401.12181) can be found in the residual
stream.

For the test, I tried to isolate the suppressed English from the output language in the
["Do Llamas Work in English?"](https://arxiv.org/abs/2402.10588) plot.

## Where the idea came from

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

This gives us known content that is readable in the middle and suppressed before the
output: the English word for the answer.

## The method

I think of these as "words that are thought but not spoken." For each sample, project the
residual stream into vocabulary space and find token logits that rise in the middle but
fall before they can be sampled.

```python
z_early, z_peak, z_output = unembed(rmsnorm(h[[early, peak, output]]))

rise = center_over_vocab(z_peak - z_early)
fall = center_over_vocab(z_peak - z_output)
suppressed_score = minimum(relu(rise), relu(fall))

suppressed_tokens = topk(suppressed_score, k=32)
S = orthogonal_basis(center(unembedding[suppressed_tokens]).T)
h_suppressed = h @ S @ S.T
```

The `fall` term removes the words the model is about to say. The complete PyTorch
functions, including `component`, `remove`, `steer`, and `replace`, are in
[`suppressed_activation_subspace.py`](suppressed_activation_subspace.py). The extraction is
per prompt and needs one unmodified forward pass through the output layer.

## Does it find the hidden word and exclude the said word?

![Three panels for Qwen3.5-4B German-to-Chinese translation. a: logit-lens probability of the English word rises at layers 24 to 27 and falls by layer 32, while the Chinese word rises to about 0.6 at layer 32. b: per selector, the fraction of 120 prompts whose top-32 tokens contain the English word, the Chinese word, the German word, and the English word without the other two; rise-and-fall has the highest isolation, about 0.47, and the logit lens includes Chinese in most prompts. c: fraction of 50 word pairs where swapping a component at the last prompt token makes the model output the other word's Chinese translation, by patched layer window; random edits stay at zero](figs/english_setting.png)

*Qwen3.5-4B, 120 German-to-Chinese word prompts in the Wendler et al. 4-shot format.
Layers: early 22, peak 27, output 32. Panel c is the next section; its layer windows overlap.*

"Isolates" means the top-32 tokens contain the English word, and contain neither the
Chinese word (said) nor the German word (input). AUROC ranks the whole vocabulary within
one prompt: the probability that an English-word token scores above a Chinese-word token.

| selector (top-32 tokens) | isolates hidden word | English (hidden) in | Chinese (said) in | German (input) in | median AUROC, English vs Chinese tokens |
|---|---:|---:|---:|---:|---:|
| rise-and-fall (this method) | **56/120** | 94/120 | 3/120 | 37/120 | 0.82 |
| fall only | 51/120 | 69/120 | 2/120 | 17/120 | 1.00 |
| plain logit lens at L27 | 4/120 | 116/120 | 105/120 | 70/120 | 0.09 |
| rise only | 6/120 | 114/120 | 101/120 | 61/120 | 0.11 |

The plain logit lens finds English in 116 of 120 prompts, but it also finds the Chinese
word in 105. In an all-English setting it would return the said word with the thought.
Rise-and-fall excludes the said word well, but in 37 of 120 prompts it also selects the
German input word (for example ` Herz`, ` Holz`, ` Licht`). Those are real German words,
not short-prefix matches: requiring 4 matching characters gives 60 of 120 isolated. So the
method finds words that are *read or thought but not said*, and the input is one of them.
Evidence: [`out/2026-09-29_070913_english-baselines-L23/run.md`](out/2026-09-29_070913_english-baselines-L23/run.md)
and [`scripts/scratch/german_hit_tokens.py`](scripts/scratch/german_hit_tokens.py).

<details>
<summary>Why the earlier "95% of English inside the subspace" figure was dropped</summary>

The earlier Figure 1 shaded the English probability by the share of the English readout
inside `S`. Each basis vector of `S` is an unembedding row of a selected token. If the
English answer token is selected, its readout direction lies inside `S`, so the share is 1
at every layer, for any residual. The saved values show this: the share is 0.94 at L3 and
1.01 at L15, where the English probability is about zero. The share restated the hit rate
and did not measure the residual stream. A version that leaves the answer tokens out of
`S` would measure it; that has not been run.

</details>

## Can editing the component change the answer?

This is the secondary claim. For a source word and a target word, we replace the source
prompt's component in `S` with the target prompt's component, at the last prompt token,
in residual layers 23 to 30. The prompt is
`'The Chinese translation of the German word "Herz" is "'`.

The first example we found was heart to school. It changes the top token from `心` to
`学校`, and the model then corrects itself:

```text
学校" (xué xiào), which means "school" in English. This is a common mistake, as "
```

**Selection:** heart to school was hand-picked. The same configuration on 50 fixed word
pairs (all words the model translates correctly, each paired with the next):

| replaced subspace (rank 8 unless stated) | top-1 becomes the target's Chinese word | median Δ log-odds (nats) |
|---|---:|---:|
| rise-and-fall selector (this method) | 16/50 | +9.1 |
| English answer tokens (oracle) | 28/50 | +11.1 |
| Chinese answer tokens (oracle) | **41/50** | +14.0 |
| random direction, same edit norm | 0/50 | 0.0 |
| whole residual vector | 49/50 | +20.1 |

Most rise-and-fall failures are selection failures: it worked in 11 of 16 pairs where the
English word was in both rank-8 selections and 5 of 34 otherwise. At no tested layer
window was the English direction a better handle than the Chinese direction (panel c).
At layers 25 to 32 the English-token swap makes the model say the target's English word
(44 of 50). Evidence:
[`out/2026-09-29_070913_english-baselines-L23/run.md`](out/2026-09-29_070913_english-baselines-L23/run.md).

In [Gurnee et al. 2026](https://transformer-circuits.pub/2026/workspace/), swaps use
Jacobian-lens directions at all token positions and flip 54–70% of 50 two-hop prompts. They
report that logit-lens directions flip the answer less often. Our swaps use logit-lens
directions at the last token only.

## Are suppressed activations causal? Can changing this subspace change the answer?

To see if this subspace allows causal replacement, we repeat the spider/dog demonstration
from [Gurnee et al., Figures
12–13](https://transformer-circuits.pub/2026/workspace/#fig-latent-patching) using our
suppressed-activation method.

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

Now we replace the suppressed component selected from the spider prompt with the component
selected from a dog prompt. The input stays unchanged. The readout below is recomputed after
the intervention.

Input (`repr`, unchanged):

```python
'Fact: The number of legs on the animal that spins webs is '
```

We swap `spider` with `dog` in the final prompt token.

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

The dog component comes from an unmodified pass over this target input:

```python
"Fact: The number of legs on the animal that barks and is called man's best friend is "
```

For each complete input, an unmodified first pass extracts a separate subspace. We then
change one residual vector at L26 and the final source-input token:

```python
source = h_spider @ S_spider @ S_spider.T
target = h_dog @ S_dog @ S_dog.T
target = target * norm(source) / norm(target)
h_replaced = match_norm(h_spider + C * (target - source), h_spider)
```

At `C=1`, the constructed replacement still generates `8` first. The displayed `C=4`
intervention extrapolates past that replacement. The readout after intervention remains
spider-related, so this does not establish a semantic `spider → dog` replacement. C=4
changes 72% of the residual norm, 21 of 256 matched-random interventions have
an equal or larger effect, and a `2 + 2` target produces the same first-token change. See
the [executed notebook](nbs/demo.ipynb) and [fixed run
report](out/2026-09-05_211609_causal-confirmation/recovered_log.md).

**Selection:** this configuration was the best of a 64-condition layer, rank, and strength
screen on this one pair. Dog was chosen over ant because it gave the more reliable demo.
The same fixed configuration did not transfer to an ant donor (0 of 1). There is no rate on
a fixed prompt set.

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

## Limits

- The three layers (22/27/32) were chosen from the aggregate English curve. A new setting
  needs a fixed layer rule, or the result partly depends on picking layers again.
- The subspace is per prompt. Editing during open-ended generation needs an unmodified
  first pass or a basis learned from other prompts.
- The spider C=4 edit changes 68–72% of the residual norm, 21 of 256 matched-random edits
  have an equal or larger effect, and a `2 + 2` target gives the same first-token change.
  It supports transfer of the next-answer state, not of animal identity.
- The earlier dog/ant successes use a different basis (template-contrast attenuation).
  They do not validate the rise-and-fall selector as an editing handle.

## Reproduce

```bash
uv run python scripts/english/01_detector_baselines_and_pair_transfer.py 23  # eval + pair swaps, ~3 min on a 3090
uv run python scripts/english/02_figure.py                                   # figs/english_setting.png
just notebook-run                                                            # spider/dog demo, nbs/demo.ipynb
```

The eval needs a clone of [epfl-dlab/llm-latent-language](https://github.com/epfl-dlab/llm-latent-language)
at `/tmp/llm-latent-language` for the word lists. The research history is in
[`RESEARCH_JOURNAL.md`](RESEARCH_JOURNAL.md); older entries contain claims corrected later.

## Citation

If you use the method or figure, please cite
[`CITATION.cff`](CITATION.cff). GitHub exposes this as **Cite this repository**.

## References

- Gurnee, Wes, et al. ["Universal Neurons in GPT2 Language Models."](https://arxiv.org/abs/2401.12181) 2024.
- Wendler, Chris, et al. ["Do Llamas Work in English? On the Latent Language of Multilingual Transformers."](https://arxiv.org/abs/2402.10588) 2024.
- Gurnee, Wes, et al. ["Verbalizable Representations Form a Global Workspace in Language Models."](https://transformer-circuits.pub/2026/workspace/) 2026.

<!-- Drafted from Michael J. Clark's public thread and edited by PI/claude-opus-4.6 and PI/gpt-5.4.
2026-09-29 draft restructure (eval framing, English pair results, selection counts) by Claudypoo[opus-4.8]. -->
