# Early-location results (task 1230, 144 cells)

2026-09-12, PI[glm-5p3-flash]. Run: pueue 1230, `slop/common_basis_earlyloc_batch.json`
(one model load, ~27 min), protocol `slop/earlyloc_protocol.md` (the declared 12-condition
list), attempt att1, code/spec hashes in `slop/research/earlyloc_code_hashes.txt`.
Increment selector (late-trajectory windows, NOT fitted at the intervention site), temporal
top8, joint removal, donor anchor h25 frozen at decode, C=1.5, the exact original 12 dev
questions/wrappers. Raw: `out/2026-09-12_cb-earlyloc/{condition}-{cell}/result.json`.

## Results (swap means over 12; splits 4 cells; edit = mean prefill perturbation/residual)

| condition | site | injected vector | swap ↑ | legs | naming | property | capped | loops | edit frac |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| v25imported | h1 | Pd d25 (14× import) | +1.14 | −0.33 | +3.43 | +0.32 | 9/12 | 10/12 | 2.52 |
| v25imported | h2 | ‖ = 2.12 | +0.79 | −1.02 | +2.58 | +0.80 | 10/12 | 11/12 | 2.12 |
| v25imported | h3 | 2.19 | +0.53 | +0.25 | +1.74 | −0.40 | 4/12 | 7/12 | 2.19 |
| v25imported | h8 | 0.91 | +0.13 | −0.16 | +0.22 | +0.33 | 2/12 | 1/12 | 0.91 |
| siterescaled | h1 | v1 dir @ ‖v25‖ | +0.40 | −0.17 | +2.23 | −0.87 | 10/12 | 11/12 | 2.45 |
| siterescaled | h2 | 2.06 | +1.09 | −0.25 | +3.01 | +0.50 | 10/12 | 10/12 | 2.06 |
| siterescaled | h3 | 2.14 | +0.16 | −0.44 | +1.77 | −0.84 | 7/12 | 7/12 | 2.14 |
| v8replay | h8 | Pd d8 | +0.02 | +0.12 | −0.08 | +0.02 | 0/12 | 0/12 | 0.07 |
| C0 ×4 | h1/h2/h3/h8 | identity | 0.00 exact | | | | 0/12 | 0/12 | 0.0 |

Baseline verification: the v8replay-h8 arm = 1194's v8-replay arm **12/12 first-logit
hashes identical** (and the imported-h8 arm = 1194's imported arm, same construction).

## Semantic outcomes (all 132 nonzero continuations read; word-boundary identity)

**ZERO cells with donor-identity mentions at any early site** (0/132); the dominant
outcome at h1/h2 is INCOHERENCE: 9–11/12 cells capped in repetition loops (r2 > 0.5) —
the imported late component (and the same-size site-vector control) DEGRADES generation
at h1/h2 rather than transferring. h3: intermediate (7/12 loops). h8: near-null (+0.13,
1 loop). No registered branch (improved persistent identity) is realized: the early-site
import degrades; the site-rescaled control ALSO degrades (so the degradation tracks the
injected SIZE ~2.1–2.5 edit-fraction, not the imported direction: siterescaled ≈ imported
at each site).

## Reading (labeled)

The early sites (h1/h2) cannot host the injected late component: the edit fraction ~2.1–2.5
(the injection is 2× the residual norm!) produces loop collapse, at matched size for BOTH
the imported and the site direction — a size-driven degradation at h1/h2, not a
direction-selection effect. The h3/h8 gradient (7 → 1 loops) tracks the declining injected
norm. The early-placement goal at C=1.5 with these constructions is not reachable by
import: the injected vector at early depths EXCEEDS the residual norm (edit frac > 2),
far beyond every previously tested operating point (≤ 0.9).

## Registered next comparison (rank, per the corrected algebra; NOT queued)

Complete-edit rank narrowing at the PREDECLARED fixed site h1 (both U_s/U_d truncated at
k ∈ {1,2,4,8,full}; P_joint(k) = span([U_s^k | U_d^k]); injection U_d^k d25): the edit
fraction at h1 shrinks with k (the k=full edit 2.5 → smaller k edits ~proportionally) —
the rank ladder may bring the h1 edit into the non-degenerate range WHILE testing the
user's early-intervention idea. k=full at h1 replays the earlyloc imported-h1 arm.
CPU pre-computation: the planned edit fracs per k. Not queued — supervisor review.
