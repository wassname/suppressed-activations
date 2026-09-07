# Revised findings

## Withdrawals
- **C1 geometry:** For unit \(v_s,v_t\), \(h \leftarrow h+V(\mathrm{flip}(c)-c)\) **is** Householder in \(w=(v_s-v_t)/\|v_s-v_t\|\) and norm-preserving. QR on \(V\) only renames coordinates. Prior “ill-conditioned reflection / non-orthogonal repair” claim withdrawn.
- **\(P\) / SVD:** \(B[t]\) from orthonormal QR ⇒ \(P=\mathbb{E}[BB^\top]\) is a mean of projectors; thin SVD of concat is exact. No hidden covariance claim.
- **C0 / readouts / shadow:** Four exact C0 controls exist; post-hook generation states drive readouts. Shadow is only for *adaptive* bases, not validity of static-base per-token coordinates.
- **Steering:** Continuous decode steering stays mandatory; do not propose prompt-only or early stop.
- **Conditioning:** Logged cosines/SVs do not establish a bad pair. Ant raw cos 0.137 is well-separated; projection is optional geometry, not a fix.
- **Diagnosis:** Ant C4 name flip ≠ proven concept edit or pure logit bias; need cross-task effects. Global hidden cosine is non-diagnostic.

## What still stands
Named unembed swap can move surface animal tokens without reliable leg-count or coherent taxonomy (ant digit failure). That is under-complete transfer or task-circuit miss, not algebra error. Prior operator had random/source/target controls; **this family still needs matched-norm randoms in candidate selection**, without treating their absence as final failure. ReLU kink is irrelevant (no grad through score).

## Cheapest compelling next test
**Prefer matched template activation contrast over corpus VJPs.**

**Why:** Same suffix tokens after the animal isolate name→residual Δ with no colony/bark vs webs confound and no leg/digit in the extract set. One forward per template × layer; no backward pass. VJPs are richer but costlier (many contexts × future tails × backward) and should wait until contrast fails under the same apply schedule.

**Exact extract/edit/calibration**
```text
templates: N≥8, differ ONLY at animal token(s); identical suffix (≥3 toks)
layers: {8,12,16,20,24}  # align with your band queue
pos: last 3 suffix positions (not answer span)
d_ℓ = normalize(mean_{tmpl,pos}(h_donor - h_source)_ℓ)   # full residual
d_ℓ^U = normalize(U_ℓ U_ℓ^⊤ d_ℓ)                          # optional same suppressed space
# apply continuously (prompt last-3 + all decode), layer-specific d:
h ← h + C * α * d_ℓ     # or d_ℓ^U
# α: calibrate so ||Δh|| matches best raw named-swap hit (e.g. ant C4) per layer
# C ∈ {0, 0.5, 1, 2}; plus K matched-norm random unit controls
# one-sided variant: only add d if ⟨h,v_s⟩>⟨h,v_t⟩ (or ⟨h,d⟩<0)
```
**Success bar:** joint \(p(\mathrm{leg})\), target-name dominance, spider dropout, continuation coherence under web clue — same hooked generation path.

**Retain disagreement:** Unembed-named directions remain a weak causal estimator; contrast directions are the minimal fix before VJP. Keep running the queued raw/one-sided sweeps; splice contrast as the next **direction source**, not a reason to drop persistent steering.