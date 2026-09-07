# Review: Coherent Suppressed-Concept Intervention

## Central assumptions
1. Spider is linearly readable in late-prompt/decode residuals via unembedding-aligned directions, and ant/dog are substitutable in the same 2D plane.
2. Suppressing spider and writing target in that plane flips the *fact* (leg count) and the *name* together, despite an unchanged “spins webs” clue.
3. A static V from final unembedding rows (not J-lens / causal vectors) is the right edit basis; shared U from last-4 prompt suppression spans is optional.
4. Patching L24 on last-3 prompt + all decode steps is late enough for commitment and early enough for coherence.
5. Success = digit matches target taxonomy **and** continuation names the target without spider relapse — conditional on accepting the counterfactual animal, not on “fixing” the web clue.

Assumption 5 is load-bearing and currently failed: name sometimes moves, digit almost never for ant; dog digit moves with mixed identity.

## Confounds and controls
- **No fresh random-direction / random-span controls** on this grid → cannot separate “any large edit at L24” from concept swap.
- **Donor text semantics leak** (colony/pheromone vs bark) while prompt still says webs → model may reconcile via “social spider,” hybrid, or digit–name split; that is prompt–edit conflict, not only operator failure.
- **C>1 extrapolation** and **C1 reflection** can invert already target-leaning states; grid confounds gain with geometry.
- **Raw V bypasses U** while scores/P are suppression-derived → two inconsistent theories of where the concept lives.
- **Single template, single layer, no shadow forward** → suppression readout after patch is stale; digit-only scoring ignores full-string coherence.
- **bf16 runtime vs fp32 traces** minor if errors <7e-6; not the main issue.
- Earlier **mean(donor)−mean(source) in U** beat named swap on digit but polluted wording → named directions and displacement operator are **both** under-identified; do not treat named swap as established.

Method misconception risk: treating “reverse coordinates in unembedding plane” as concept replacement. Missing-control risk: no identity-matched clean runs where webs clue is removed, and no causal direction estimate.

## Mathematical issues
- `score = min(relu(peak−early), relu(peak−output))` is a heuristic peak sharpness, not a causal effect; top-vocab span may be digit/punctuation dominated, not animal.
- `P = mean(B Bᵀ)` then leading eigenvectors: if B columns are unnormalized unembedding rows × gain, P mixes scale with direction; thin SVD of concat(B) ≠ eigen(P) unless columns are handled consistently.
- `c = pinv(V)@h` with `V = [v_s, v_t]` unit columns: if v_s≈v_t (insects/arachnids cluster) or both leave residual animal subspace, swap is ill-conditioned and under-complete.
- Full reverse `h += C V(reverse(c)−c)` is a Householder-like reflection in a 2D non-orthogonal embed; **source-dominant-only** `d=max(c_s−c_t,0); h+=C d(v_t−v_s)` is safer (no target→source bounce) but still assumes the concept difference is exactly `v_t−v_s`.
- Patching every decode step with **fixed** V/U computed from prompt does not track drift; no residual renorm can shift RMS-normed downstream reads.
- Leg count is a **downstream arithmetic/taxonomic inference**; editing animal name direction need not edit “legs” circuitry if those are linearly separate at L24.

## Annotated pseudocode (minimal, testable)
```python
# --- directions: prefer causal over static unembed ---
# J-lens sketch: avg VJP of future logp(target_tokens) - logp(spider_tokens)
# over diverse contexts; fallback = unit centered unembed rows * RMS gain
v_s, v_t = concept_dirs("spider", target)   # unit; optional QR vs shared U
v_delta = normalize(v_t - v_s)

def edit(h, mode="dom_swap", C=1.0):
    c_s, c_t = h@v_s, h@v_t                # or pinv([v_s,v_t])@h
    if mode == "reflect":                   # current: unstable if c_t > c_s
        c = np.array([c_s, c_t])
        h = h + C * np.c_[v_s,v_t] @ (c[::-1]-c)
    elif mode == "dom_swap":                # candidate: one-way source->target
        d = max(c_s - c_t, 0.0)
        h = h + C * d * (v_t - v_s)         # equiv. scale * v_delta
    elif mode == "clamp_donor":             # donor coord floor, no reflection
        h = h + C * max(tau - c_t, 0) * v_t - C * max(c_s - eps, 0) * v_s
    return h

# hook: chosen layer band, last_k prompt + decode; C=0 identity check
# shadow_forward: clean KV copy, same edit schedule, recompute scores[t] each step
# success: p(digit*), name logit/readout, web-conflict string flags — jointly
```

## One prioritized next experiment
**Do not run the full 6-layer × 6-C × 2-animal raw named-swap queue as primary.** It multiplies a weak operator.

**Priority (single small matrix):** At **L16 and L20 only** (commitment without full freeze), **source-dominant-only swap** + **C ∈ {0, 0.5, 1, 2}**, raw `v_t−v_s`, ant and dog; **n=8 random unit controls** matched for ‖Δh‖; patch last-3 prompt + decode; **shadow forward** each step to recompute suppression readout and stop if spider peak returns. Pre-register success: `p(correct leg) > 0.5`, target-name rank-1 in animal set, spider rank drop, and continuation free of spider/hybrid repair **or** explicitly mark web-clue conflict as expected conditional coherence.

**Why:** Tests the main geometric failure mode (reflection / target-dominant bounce, static unembed Δ) with controls, before layer sweeps, J-lens, or per-token U rebuilds. If dom-swap+controls still move name without legs, next is J-lens / future-effect directions — not denser C grids. If random matched-norm edits also flip digits, the effect is nonspecific and named “concept” framing is wrong.

**Defer:** full L4–L24 queue, projected U variants, template/covariance lens, band edits — until dom-swap vs random at 2 layers discriminates.