# A suppressed activation subspace isolates hidden English in Qwen

I was searching for a way to test whether [Wes Gurnee's](https://x.com/wesg52)
["suppression neurons"](https://arxiv.org/abs/2401.12181) can be found in the residual
stream.

For the test, I tried to isolate the suppressed English from the output language in the
["Do Llamas Work in English?"](https://arxiv.org/abs/2402.10588) plot.

This particular method works very well on Qwen3.5-4B.

![Qwen reads out English before Chinese; a per-sample suppressed activation subspace isolates that English](figs/suppressed_activations.png)

*Figure 1: Language readouts at the final prompt position during Qwen3.5-4B
German-to-Chinese word translation. (a) The x-axis is layer index. The y-axis is the
probability, according to the logit lens, of the correct Chinese next token or its English
analog. Error bars are 95% Gaussian confidence intervals over 105 input texts. Panels b
and c use a different, linear quantity, answer readout divided by residual norm, because it
can be decomposed additively. The line is the complete readout; the fill is the part inside
the rank-32 suppressed activation subspace. These two panels share a scale and use the
held-out 53 prompts.
The own subspace contains 0.947 of English at L27 and 0.205 of Chinese at L32. A fixed
random pairing, with no prompt paired to itself, contains 0.040 and -0.015. The subspace is
constructed from vocabulary directions that rise and fall, so the fill is a correlational
decomposition rather than evidence that those directions cause suppression. Signed
components below zero are hatched.*

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

The vocabulary search chooses the directions. `S` is an orthonormal basis in the residual
stream, so it can be used for projection, ablation, or steering. The complete PyTorch
function is [`suppressed_activation_subspace.py`](suppressed_activation_subspace.py).

The method receives no English or Chinese answer tokens. On the held-out half of this run,
its top-32 vocabulary rows contain an English answer token for 42 of 53 prompts and a
Chinese answer token for 1 of 53.

| prompt gets subspace from | signed share: English at L27 | signed share: Chinese at L32 |
|---|---:|---:|
| same prompt | **0.947** | 0.205 |
| different prompt | 0.040 | -0.015 |

These are signed shares of a readout, so they need not lie between zero and one. A negative
share points against the full readout.

## Limits

- This is a diagnostic result. It does not yet show that the subspace causes hidden English
  computation or suppression.
- The method uses the LM head to find the subspace and to measure its contents.
- The three layers were chosen from the aggregate English curve. A transfer test should
  choose them on held-in prompts or use a fixed model-level rule.
- Each prompt gets its own subspace. The different-prompt control tests that dependence.

## [Next: steering](https://github.com/wassname/suppressed-activations/issues/1)

The next test is to project a steering vector into `S` and evaluate it on
[Steering-Lite](https://github.com/wassname/steering-lite):

```python
v = mean(h_positive - h_negative)
v_suppressed = S @ S.T @ v
h_steered = h + strength * v_suppressed
```

Compare this with the full steering vector, the orthogonal complement, a random rank-32
subspace, and another prompt's suppressed subspace. This would test whether the diagnostic
also identifies a useful causal intervention space.

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

<!-- Drafted from Michael J. Clark's public thread and minimally edited by PI/claude-opus-4.6. -->
