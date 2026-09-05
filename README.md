# A suppressed activation subspace isolates hidden English in Qwen

I was searching for a way to test whether [Wes Gurnee's](https://x.com/wesg52)
["suppression neurons"](https://arxiv.org/abs/2401.12181) can be found in the residual
stream.

For the test, I tried to isolate the suppressed English from the output language in the
["Do Llamas Work in English?"](https://arxiv.org/abs/2402.10588) plot.

This particular method works very well on Qwen3.5-4B.

![Qwen reads out English before Chinese; a per-sample suppressed activation subspace isolates that English](figs/suppressed_activations.png)

*Figure 1: Language readouts at the final prompt position during Qwen3.5-4B
German-to-Chinese word translation. The line in every panel is the same mean logit-lens
probability over 105 input texts. Error bars in a are 95% Gaussian confidence intervals.
In b and c, the orange fill is the English probability multiplied by the signed share of
the linear English readout inside a rank-32 subspace, measured on the held-out 53 prompts.
This puts the diagnostic share against the familiar curve; it is not an additive
decomposition of probability. The gap below the orange line is the share outside the
subspace. Chinese is not filled because the two fills would overlap; its share at L32 is
printed instead. A useful detector fills English near L27 while keeping the printed
Chinese share low. The own-prompt subspace contains 0.947 of English at L27
and 0.205 of Chinese at L32. A fixed different-prompt pairing contains 0.040 and -0.015.
The subspace is constructed from vocabulary directions that rise and fall, so this remains
a correlational result rather than evidence that those directions cause suppression.*

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
>
> <img width="292" height="184" alt="image" src="https://github.com/user-attachments/assets/28ab1795-4a8a-4752-b4cb-337ed360075a" />


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

The vocabulary search chooses the directions. `S` is an orthonormal basis in the residual
stream. The complete PyTorch functions are in
[`suppressed_activation_subspace.py`](suppressed_activation_subspace.py).

```python
h_inside = component(h, S)
h_removed = remove(h, S, restore_norm=True)
h_amplified = steer(h, S, strength=0.5, restore_norm=True)
h_replaced = replace(h, S, h_target, S_target, restore_norm=True)
```

These operations depend on the projector `S @ S.T`, not the individual QR columns. The
extraction is sample-specific and needs an unmodified residual trajectory through the
output layer. You can then read or modify that same trajectory. Applying it during
open-ended generation requires an unsteered first pass or a basis learned from other
samples.

The method receives no English or Chinese answer tokens. On the held-out half of this run,
its top-32 vocabulary rows contain an English answer token for 42 of 53 prompts and a
Chinese answer token for 1 of 53.

| prompt gets subspace from | signed share: English at L27 | signed share: Chinese at L32 |
|---|---:|---:|
| same prompt | **0.947** | 0.205 |
| different prompt | 0.040 | -0.015 |

These are signed shares of a readout, so they need not lie between zero and one. A negative
share points against the full readout.

## Can changing this subspace change the answer?

We follow the spider/ant demonstration in [Gurnee et al., Figures
12–13](https://transformer-circuits.pub/2026/workspace/#fig-latent-patching):

> When we swap the spider lens vector for ant, the model's top output changes from “8”
> to “6”, the number of legs on an ant.

Their vectors come from the Jacobian lens. The experiment below uses only the LM-head
rise-and-fall method above.

The source prompt is:

> **Fact: The number of legs on the animal that spins webs is**

Its rank-8 readout contains the unspoken `Spider` plus several variants of the prompt's
web word:

```text
[丝绸, -web, Web, Disc, 的战, Spider, web, WEB]
```

For each complete prompt, an unmodified first pass extracts a separate subspace. We then
change one residual vector, at L26 and the final source-prompt token:

```python
source = h_spider @ S_spider @ S_spider.T
target = h_target @ S_target @ S_target.T
target = target * norm(source) / norm(target)
h_replaced = match_norm(h_spider + C * (target - source), h_spider)
```

`C=1` is the constructed source-to-target component replacement. `C=4` extrapolates
three times as far past it. L23/L25/L32 extraction, rank 8, L26 intervention, and C=4 were
selected during exploration on these prompts. They are demo settings, not defaults.

### What changed

| target prompt | C | answer | Δlog odds target/8↑ | p(target)↑ | p(8)↓ | ‖Δh‖/‖h‖↓ |
|:---|---:|---:|---:|---:|---:|---:|
| *clean spider* | *0* | *8* | *0.000* | *—* | *0.883* | *0.000* |
| ant | 1 | 8 | +0.375 | 0.038 | 0.870 | 0.199 |
| ant | 4 | **6** | **+3.750** | **0.487** | 0.379 | 0.679 |
| dog | 1 | 8 | +0.500 | 0.089 | 0.847 | 0.208 |
| dog | 4 | **4** | +3.250 | **0.490** | **0.297** | 0.720 |

<sub>Table: Qwen3.5-4B next-token probabilities. The ant prompt asks about an animal that
lives in colonies and follows pheromone trails. The dog prompt asks about an animal that
barks and is called man's best friend. Each clean target prompt answers 6 or 4.</sub>

The readouts themselves are useful counterevidence. Dog is visible in its target subspace,
but ant is not. Re-extracting after either C=4 edit still returns spider and web rows:

| trajectory | selected vocabulary rows |
|:---|:---|
| spider, before | 丝绸, -web, Web, Disc, 的战, Spider, web, WEB |
| ant, target | ;font, _unix, Kate, สถาบัน, Soldier, división, 在校园, соци |
| spider after ant, C=4 | Silk, Spider, spiders, 丝绸, silk, -web, spider, Spider |
| dog, target | 吠, собаки, 狗粮, dog, Dog, Dog, สุนัข, canine |
| spider after dog, C=4 | Silk, Spider, spiders, 丝绸, silk, -web, spider, Spider |

The 64-token greedy continuations begin:

<details>
<summary>Clean, ant C=4, and dog C=4</summary>

```text
[clean]
8.
Hypothesis: The animal that spins webs has 8 legs.
Does the hypothesis follow from the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 8."
```

```text
[ant C=4]
6.
Hypothesis: The animal that spins webs has 6 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 6."
```

```text
[dog C=4]
4.
Hypothesis: The animal that spins webs has 4 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Fact: "The number of legs on the animal that spins webs is 4."
```

</details>

### What the controls say

| target | Δlog odds↑ | random below↑ | random top target↓ | answer-only Δlog odds |
|:---|---:|---:|---:|---:|
| ant → 6 | **+3.750** | 238/256 (92.97%) | 19/256 | +8.375 from “three plus three” |
| dog → 4 | +3.250 | 235/256 (91.80%) | 27/256 | +3.250 from “two plus two” |

Both effects failed the preregistered 95% matched-random criterion. The arithmetic prompts
reproduced or exceeded them. Each C=4 continuation also exactly matched the continuation
obtained by forcing its first digit without any residual intervention.

The operation changes this prompt's next-answer state. This experiment does not show that
ant or dog identity was transferred, or that the rise-and-fall subspace is more causal than
a matched random subspace. The [executed notebook](nbs/demo.ipynb) shows both targets,
negative and positive strengths, and every exact continuation. The [fixed run
report](out/2026-09-05_211609_causal-confirmation/recovered_log.md) contains all 256 random
controls, arithmetic controls, byte controls, position controls, and raw-output links.

## Limits

- This is a diagnostic result. It does not yet show that the subspace causes hidden English
  computation or suppression.
- The method uses the LM head to find the subspace and to measure its contents.
- The three layers were chosen from the aggregate English curve. A transfer test should
  choose them on held-in prompts or use a fixed model-level rule.
- Each trajectory gets its own subspace. The different-prompt control shows that the basis
  is mostly path-dependent. An intervention on the same sample can use an unsteered first
  pass; a transferable intervention would need to combine many extraction trajectories.
- The English-only demo settings came from a 64-condition layer, rank, and dose screen.
  C=4 changes 68–72% of the residual norm and is an extrapolation. The demo does not
  estimate a held-out success rate.
- The C=4 answer changes did not meet the preregistered matched-random criterion. Arithmetic
  target prompts reproduced them, so the supported interpretation is next-answer-state
  transfer rather than animal identity.

## [Next: steering](https://github.com/wassname/suppressed-activations/issues/1)

The next test is to project a steering vector into `S` and evaluate it on
[Steering-Lite](https://github.com/wassname/steering-lite). Constructing `S` for a new
prompt uses its later residuals, so an adaptive intervention would require an unsteered
first pass. The test below instead uses `S` only on extraction prompts and applies one
fixed vector to held-out prompts:

```python
projected_differences = []
for positive_trajectory, negative_trajectory in extraction_pairs:
    midpoint_trajectory = (positive_trajectory + negative_trajectory) / 2
    S_i = suppressed_activation_subspace(midpoint_trajectory)
    difference_i = positive_trajectory[layer] - negative_trajectory[layer]
    projected_differences.append(S_i @ S_i.T @ difference_i)

v_suppressed = mean(projected_differences)
h_steered = h + strength * v_suppressed
```

The midpoint keeps the subspace selection from seeing which member of the pair is positive.
Each extraction trajectory supplies its own basis, while their projected differences form
one vector that can be applied to new prompts. Compare this with the full mean difference,
the orthogonal complement, a random rank-32 subspace, and different-prompt pairing. This
would test whether the diagnostic also identifies a transferable causal intervention.

## Try it in a notebook

[`nbs/demo.ipynb`](nbs/demo.ipynb) is an executed Qwen3.5-4B notebook paired with the
editable [`nbs/demo.py`](nbs/demo.py). One configuration cell holds the prompts, layers,
rank, strengths, and generation length. It shows ant and dog target prompts at
`C = -1, 0, 1, 2, 4, 8`, including all exact 64-token continuations and the failed
matched-random criterion.

```bash
just notebook-run
```

## Reproduce the figure

```bash
uv run scripts/figure.py
```

The plotted aggregates and their provenance are in [`data/`](data/). The SVG version is
[`figs/suppressed_activations.svg`](figs/suppressed_activations.svg).

## Citation

If you use the method or figure, please cite
[`CITATION.cff`](CITATION.cff). GitHub exposes this as **Cite this repository**.

## References

- Gurnee, Wes, et al. ["Universal Neurons in GPT2 Language Models."](https://arxiv.org/abs/2401.12181) 2024.
- Wendler, Chris, et al. ["Do Llamas Work in English? On the Latent Language of Multilingual Transformers."](https://arxiv.org/abs/2402.10588) 2024.
- Gurnee, Wes, et al. ["Verbalizable Representations Form a Global Workspace in Language Models."](https://transformer-circuits.pub/2026/workspace/) 2026.

<!-- Drafted from Michael J. Clark's public thread and edited by PI/claude-opus-4.6 and PI/gpt-5.4. -->
