# Three-row future-effect Jacobian lens

Read-only reference audit by Codex/GPT-6, 2026-09-07. Official implementation inspected at commit `581d398613e5602a5af361e1c34d3a92ea82ba8e`. No GPU experiment in this audit.

## Exact estimator and its weighting

Anthropic's [fitting.py](https://github.com/anthropics/jacobian-lens/blob/581d398613e5602a5af361e1c34d3a92ea82ba8e/jlens/fitting.py#L11) says:

> the sum over later target positions; we take the mean over source positions

The code sets the cotangent to 1 at every valid target position (lines 177–186), calls `torch.autograd.grad` (187–192), then computes `grad[..., valid_positions, :].float().mean(dim=1)` (193–199). Its valid mask excludes the first 16 positions and final position (43–72). `fit` averages prompts equally, not weighted by their length.

For a fixed vocabulary vector u, the exact contraction of this estimator is:

$$v_\ell = \frac1P\sum_p\frac1{|V_p|}\sum_{t\in V_p}\sum_{t'\in V_p,\ t'\geq t}\left(\frac{\partial z_{t'}}{\partial h_{\ell,t}}\right)^\top u.$$

Here V is the valid-position mask and z is a raw target-block output. Causality makes terms with t'<t zero automatically. The target sum is NOT divided by the number of future positions. Earlier sources have more downstream terms. This differs from first choosing t uniformly and then averaging its future targets. Dividing by the triangular pair count is only a per-prompt scalar when sequence lengths are fixed; with varying lengths it changes cross-prompt weighting.

The local paper `/workspace/2026/LUCID3_wikit/docs/papers/20260710_global_workspace.tex`, methods around 158–174, writes an expectation over present/future positions. Its appendix pseudocode around 1234 explicitly injects at every position and means source gradients, agreeing with the repository. Appendix around 1187 says the Sonnet default uses the penultimate block, although official code defaults to final block. These are explicit variants, not interchangeable implementation details.

## Minimal differentiable implementation

Inference from linearity of differentiation: replace each one-hot output cotangent with a selected vocabulary row. This exactly computes three rows of W_U J without forming d×d J.

```python
model.eval().requires_grad_(False)
for prompt in corpus:
    # Same explicit tokenization/template for every corpus sample.
    # Record raw block outputs; earliest source output becomes a grad leaf.
    h, z = forward_with_graph(ids, source_layers, target_layer, use_cache=False)
    for i, u in enumerate(vocab_rows):  # spider, ant, dog; explicit token IDs
        scalar = (z[:, valid].float() @ u.float()).sum()
        gradients = torch.autograd.grad(
            scalar, tuple(h.values()), retain_graph=i < len(vocab_rows) - 1
        )
        for layer, gradient in zip(h, gradients):
            per_prompt[layer, i] = gradient[0, valid].float().mean(0)
vectors = mean(per_prompt, over_prompts)
```

One forward plus three backwards per prompt, with gradients to all requested source layers in each backward. Memory-saving option: this sequential version shares one forward graph. Official batch trick also applies: replicate the prompt three times, give each batch element its own u, and do one backward; this trades roughly threefold activation memory for batch throughput. Avoid `is_grads_batched=True` until hybrid attention backward supports its vmap path.

[hooks.py lines 16–28, 49–54](https://github.com/anthropics/jacobian-lens/blob/581d398613e5602a5af361e1c34d3a92ea82ba8e/jlens/hooks.py#L16) records block outputs and sets the earliest captured tensor `requires_grad_(True)`. No detach on later layers. This repository uses residual-layer L24 = output of block index23; official layer23 means that block output too. Target final raw output is residual L32 / block31; penultimate is L31 / block30.

## Normalization and limitations

- Exact W_U J rows use raw unembedding rows as u. For RMSNorm-aware ranking, a fixed gain-adjusted row `(W_U[token] * gain)` can instead be contracted; state this change. Do not differentiate actual normalized logits and call it the same estimator: that includes each context's nonlinear normalization Jacobian. The official [hf.py unembed](https://github.com/anthropics/jacobian-lens/blob/581d398613e5602a5af361e1c34d3a92ea82ba8e/jlens/hf.py#L171) applies normalization AFTER transporting h by the mean J.
- Three rows supply named-concept directions and relative linear scores. They cannot reproduce full-vocabulary lens probabilities or the denominator of norm(Jh) without more information.
- Use concept words, not answer digits, if testing concept transfer. Surface forms are separate explicit rows or a predeclared fixed average. Fitting only on spider/ant task prompts is a task-conditioned estimator; it does not reproduce the paper's broad corpus average.
- Future means downstream positions already present in each corpus sequence. No generation through discrete token sampling is differentiated. A sampled continuation can be frozen as teacher-forced input, but that defines a model-generated corpus.
- Strict future-only cannot be obtained by merely shifting one common valid mask: every source has a different excluded diagonal. The simplest exact variant samples a source t and differentiates the scalar summed only over t'>t, then reads gradient at t. Alternatively subtract an independently computed self-only estimator. Start with official present+future aggregation.

## Qwen3.5 checks before trusting it

Observed local Transformers code: `/home/code/.cache/uv/environments-v2/oat-sweep-da08b15948b5bc08/lib/python3.13/site-packages/transformers/models/qwen3_5/modeling_qwen3_5.py`, lines 507–535 chooses recurrent or chunked gated-delta computation; lines 248–327 implement the chunk path; lines 1161–1212 handle caches. The official HF adapter also uses `use_cache=False`.

Use an ordinary grad-enabled forward, not `generate` (no-grad) or this repo's no-grad `trajectory`. Freeze parameters; retain gradients only downstream of the earliest source. Verify a finite-difference directional derivative of the SAME masked scalar against the VJP before fitting a corpus. Hybrid attention can have distinct cached/no-cache paths: finite differences must use the exact differentiable path. Preserve the already-fixed actual-generation capture for evaluation; do not assume its activations numerically equal fitting forwards.

No claim yet that the installed gated-delta kernel backward works or that numerical finite differences pass. If a kernel lacks backward, diagnose and explicitly choose a differentiable implementation; do not silently change attention semantics. Start standard gradients, without frozen-QK: linear attention has additional gates/state, so copying a QK-stop-gradient recipe requires a separate definition.

Recommendation: three sequential VJPs on 10 fixed unrelated 128-token contexts, final or penultimate target stated explicitly; record per-prompt vector norms and convergence. This tests actual average downstream effects while avoiding a full Jacobian. The paper reports useful lenses with 10 contexts, but that does not guarantee this three-row Qwen construction works.

## Available generic corpus loader

Official [examples.py lines40–59](https://github.com/anthropics/jacobian-lens/blob/581d398613e5602a5af361e1c34d3a92ea82ba8e/jlens/examples.py#L40) provides `load_wikitext_prompts`: stream `Salesforce/wikitext`, configuration `wikitext-103-raw-v1`, train split; select the first n records with at least600 stripped characters. README lines103–104 says no text corpus is bundled. This is a usable loader recipe, not a random sample of independent topics: consecutive records can share an article.

For the user's chat-template constraint, render each selected generic text as an assistant prefill through the same official template used by the demo. Record this as templated WikiText, distinct from the raw reference corpus. Persist exact records, dataset revision, rendered inputs and token IDs. Truncate content before rendering to avoid cutting a chat-template boundary; report actual rendered length and valid mask. A16–32-record first trial remains a small, potentially topic-correlated corpus.

— Codex/GPT-6
