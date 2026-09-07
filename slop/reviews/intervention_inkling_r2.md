**Revised findings (corrections accepted)**

1. Reflection is exact: `w=(v_s-v_t)/||w||`, `h←h-2w(w·h)`; `C=1` preserves norm, `pinv(V)` is correct for unit columns. QR on `B` yields orthonormal `U`; `P=mean(BB^T)` is projector mean; SVD is exact. No hidden-state covariance claim intended.
2. `C=0` controls exist (4); readouts come from hooked generation states, not stale donors. Shadow pass is for adaptive direction estimation only.
3. Continuous steering is required; do not propose stopping.
4. `κ(V)` and projection ratios logged (`ant` raw cos `.137`, proj `.667`; proj SV `1.291, .577`; `dog` proj SV `1.202, .745`; norm fractions `ant` `.267,.321`, `dog` `.281,.835`). No ill-conditioning.
5. ReLU has a kink but is continuous; no gradient training through it here.
6. Prior grids had 32+ controls/decompositions; current named-swap family lacks matched fresh random controls—accepted limitation, will add to selection, not declare failure.
7. `C=4` ant drives word choice to “ant” but does not alone prove semantic replacement vs direct logit bias. Cross-task consequences required; global cosine is uninformative.

**Choice: matched template contrast, not VJPs**
Corpus-averaged future-effect VJPs need backward passes, diverse contexts, and averaging over future steps—expensive and noisy. The template contrast needs only forward passes: prompts differ by one token (`ant`/`dog`/`spider`), identical suffix; extract at layers `L∈{4,8,16,24}` (align with queued sweep); average `h_donor−h_source` over templates and last 3 suffix positions. No leg-count digits in extraction—avoids colony/web semantic confounds.

**Exact edit and calibration**
- Build `N=6` prompts per pair (e.g. “The creature is an [X]. It behaves by …”), suffix fixed 8 tokens.
- At each `L`, compute `d_L = mean(h_target) − mean(h_source)` over `N` prompts and suffix positions `t−2:t`.
- Normalize: `u_L = d_L / ||d_L||`.
- Calibrate magnitude to current swap: compute `Δ_ref = v_t − v_sp` (norm ≈1.31 for ant); scale `C·u_L` so `||C·u_L|| = ||C·Δ_ref||` → use same `C∈{0.25,0.5,1,2,4}`.
- Apply continuously at `L` on all decode steps (keep prompt unpatched or match current coverage).
- Two arms per `L`: **Full residual** `h += C·u_L`; **Projected** `h += C·U(U^T u_L)`. Log `||P_u||/||u||`; compare to current `.267/.321` ratios.
- Add fresh null: random `u_null∈U` at same `C`.

**Retained disagreement**
Even with clean `d_L`, a vocabulary-level push (`ant` token up) can still explain coherence without true concept substitution. I agree run this first—it’s the cheapest compelling test (`~2s/condition`, 72 conditions align with queued sweep)—but cross-task verification (e.g., leg-count consistency under a different framing prompt) remains necessary to rule out direct logit bias per your point 8.