# Review: suppressed-concept swap on Qwen3.5-4B

## Central assumptions (all currently untested)

1. **Unembedding row = concept direction.** `v_spider` is a readout direction, not a generative-feature direction. Adding it to `h` directly raises the target logit whether or not the underlying concept changed. Your symptoms (digit flips, explanation stays spider; "punctuation readout" in projected conditions) are the textbook signature of **logit nudging, not concept replacement**.
2. **The swap is a reflection.** It isn't. `V`'s columns are unit-normed but not orthogonal; two animal unembedding rows are plausibly correlated (cos ≈ 0.1–0.4). With non-orthogonal `V`, `pinv(V)` makes `c_spider` depend on `h`'s component along `v_target`, and `V@(reverse(c)-c)` moves `h` partially *along* `v_spider` when you meant to remove it. Your float32 check verifies the algebra, not the geometry.
3. **Suppression span is a privileged frame.** Built from 2 prompts × 4 tokens × relu-truncated scores; `P` is near-degenerate, eigenvectors within a tied-eigenvalue block are arbitrary. Projected conditions degrading (ant→"2 and punctuation") suggests `U` is mostly noise.
4. **Late-layer, all-decode-step patching preserves coherence.** Patching 31 cached decode steps with a fixed direction while the prompt still says "spins webs" creates a train-inconsistent state at every step.

## Confounds and missing controls

- **No norm-matched random-direction control.** If a random unit vector at C=4 also shifts p8→p6, the effect is nonspecific damage. This is the single cheapest disambiguator of "method misconception vs. missing controls."
- **No negative-target control** (e.g., v_car, v_the). If non-animal targets also flip the digit, you're measuring fragility.
- **Dev-prompt overfitting:** 2 prompts, one template, no held-out animals. "No ant condition gives 6" may be ant-specific (donor description weakly evokes "6") rather than method-specific.
- **Metric conflation:** p6 is a logit-level metric; coherence is judged on one continuation. No vocab-KL or fluency side-effect measurement.
- **The "web clue" problem you flagged is real and must be settled by definition, not more sweeps:** define success as *self-consistency* (emitted digit, animal named, and leg-count explanation all agree with the target), evaluated on prompts where the animal is otherwise unconstrained (drop "that spins webs" in a counterfactual variant) to separate "correcting the prompt" from "incoherent edit."

## Mathematical issues

- **Fix the reflection:** QR-orthogonalize `V` (or whiten with `(V^TV)^{-1/2}`); then C=1 is a true reflection in the 2-D plane and C>1 extrapolation is interpretable.
- **`min(relu(...), relu(...))` scoring** discards magnitude and biases `B` toward directions suppressed at *both* ends; fine for detection, bad as an intervention basis.
- **No renormalization + RMSNorm:** the next RMSNorm rescales your edit, so effective dose varies with `‖h‖` across the 31 patched steps; report `C·‖Δ‖/‖h‖` per step.
- **pinv conditioning:** report `cos(v_spider, v_target)` and `cond(V)`; if cos > ~0.5 the swap is ill-posed as written.

## Annotated pseudocode

```python
# --- corrected swap with controls ---
Q, _ = qr(concat(v_spider, v_target))       # orthonormal plane; fixes reflection
c = Q.T @ h                                  # exact coordinates in-plane
c_swap = c[::-1] if c[0] > c[1] else c       # source-dominant gate: no reverse-flips
dh = C * Q @ (c_swap - c)                    # dh ⟂-plane correction only

for name, vec in [("target", dh),
                  ("random", randn_like(dh).mul_(dh.norm()/...)),  # SAME norm
                  ("nonanimal", dh_car)]:
    patch_and_measure(vec)
    # metrics: p_target, p_source, KL(full logits || C0 logits),
    # donor-likeness: cos(h_patched, h_donor_prompt) at same layer
```

## Prioritized next experiment

**Norm-matched random-direction control + donor-representation check at the one "working" condition (raw dog, C=2, L24), before the queued 432-condition sweep.** Three arms: dog swap, random unit vector scaled to identical `‖Δh‖`, and the C0 baseline. Measure (a) digit flip rate, (b) cosine of patched `h` against the hidden state from the actual clean dog-donor prompt at the same layer/token, (c) full-vocab KL. Outcomes:

- Random flips the digit too → the effect is nonspecific perturbation; the named-direction estimator is not established, and the queued sweep will produce a failure catalog, not evidence. Pivot to VJP/J-lens direction estimation.
- Only dog flips, but `h` is not donor-like (low cos) → logit nudging confirmed; swap operators won't yield coherence at any layer, prioritize layer-band modest edits + per-token suppression-space recompute.
- Dog flips and `h` is donor-like → method is sound; proceed with sweep and orthogonality fix.

This is ~6 conditions of your 2s budget and determines whether everything downstream is measuring concept editing or measurement artifact. Run it first.