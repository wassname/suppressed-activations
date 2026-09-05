# Figure data

`qwen_logit_lens_de_zh.csv` contains means and 95% Gaussian confidence intervals over
105 German-to-Chinese word-translation prompts. Values are the probability mass assigned
to each word's accepted token prefixes by `lm_head(final_norm(h_layer))`.

`suppressed_subspace_by_layer.csv` contains the complete and inside-subspace linear
readouts drawn in Figure 1b-c. Each is divided by the residual norm before averaging.

`suppressed_subspace_scores.csv` contains ratios of mean readout inside the rank-32
per-sample subspace to mean full readout. It uses the held-out 53 of those prompts. The
intervals are percentile intervals from 20,000 prompt bootstraps with seed 0. The subspace
uses L22 as early, L27 as peak, and L32 as output.

Model: [`Qwen/Qwen3.5-4B`](https://huggingface.co/Qwen/Qwen3.5-4B). Prompt format and
token-prefix sets follow [Wendler et al.](https://github.com/epfl-dlab/llm-latent-language).
The model run used seed 0 and four in-context examples. Its metadata recorded
`29d4ae5-dirty`; the later subspace calculation used the saved residual stream and the
function published in this repository.

`causal_demo.json` contains the source and target prompts, selected token IDs, next-token
distributions, 32 matched-random controls, 64-token generations, and intervention norms
for Figure 2. Pueue job 63 generated it from commit `67c683e` with
[`scripts/demo.py`](../scripts/demo.py). The full run log is
[`slop/audits/job_63_full.log`](../slop/audits/job_63_full.log).

<!-- Written by PI/claude-opus-4.6 and PI/gpt-5.4 for Michael J. Clark. -->
