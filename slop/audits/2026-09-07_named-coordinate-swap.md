# Named-coordinate swap

Written by Codex, 2026-09-07.

User request: "do the proepr swap and measure the results".

The local global-workspace paper, methods "Writing", specifies
`c = pinv(V) @ h; h_new = h + V @ (flip(c) - c)`.
Here V has two normalized, centered, RMS-gain-weighted unembedding columns,
for ` spider` and ` ant` or ` dog`. The projected variant first projects both
columns into the shared persistent source/donor span (four vectors each).
This reproduces the swap operation, not the paper's J-lens estimator.

Jobs 512 and 513 use Qwen3.5-4B, official assistant-prefill formatting, L24,
last three prompt positions and all cached decode positions, 32 output tokens.
C = 0, .25, .5, 1, 2, 4 scales the displacement, with no norm restoration.
C=1 exchanges coordinates; C=.5 equalizes them; C>1 extrapolates.
Only one layer is edited, so repeated swaps across layers cannot cancel directly.

Question: does named-coordinate exchange give selective, coherent animal transfer?
The raw-direction comparison removes the suppression-space constraint; the
projected comparison retains it. Both use identical generation and evaluation.
Expectations: C0 identity and coordinate exchange follow algebra and are tested.
Semantic transfer is an unvalidated hypothesis. Wrong directions, source removal,
and target-to-source reversal during decode can all prevent useful transfer.
The coordinate trace distinguishes reversal from an inactive hook.

Independent review by Codex (`swap_review`):
> With unit-length source/target vectors, C=1 is a reflection along their difference.
> It preserves residual norm naturally. C=.5 removes the source-target contrast;
> C>1 extrapolates.

> Dynamic swapping during generation can turn a target-dominant state back toward
> source. This is mathematically correct swapping, not persistent target clamping.

Production-hook synthetic tests pass: nonorthogonal coordinates exchanged,
orthogonal complement and untouched prefix unchanged, swap twice returns input,
and cached singleton edited. Real runs assert exact C0 logits and generation,
three prefill positions and one hook call per subsequent generated token.
Logs retain all continuations and per-step coordinates. A correct digit alone
does not establish a coherent donor concept. No new random controls in this grid.
