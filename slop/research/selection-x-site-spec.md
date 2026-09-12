# Bounded selector×site spec (for review — NOT queued)

2026-09-12, PI[glm-5p3-flash]. Deliverable requested by supervisor: exact equation, index
mapping, condition count, and predicted semantic effects vs failure.

## Equation and construction (identical for both selectors)

    # selector S in {snapshot3, increment} (selection differs ONLY in the score that picks
    # the per-position top-8 vocabulary; everything downstream identical)
    # tokens: topk(score^S, 8) LARGEST, per position (the existing subspace_from_scores
    # with normalize_unembedding_rows=True: gain-scaled, vocab-centered, row-normalized)
    B_t^S = subspace_from_scores(score^S, ...)[0]       # (4, hidden, 8) per position
    U_s^S = SVD-union_support([B_t^S])[:, :8]           # TEMPORAL TOP8 (support then first 8)
    U_d^S = same on donor window
    P_joint^S = support-filtered span([U_s^S | U_d^S])  # ~16 = 8+8; contains the injection
    v^S_l,o = U_d^S (U_d^Sᵀ d_l,o)                      # per-layer donor residual projected
    h' = h + 1.5·(v^S_l,o − P_joint^S h)                # v contained in removal span (asserted)

Score^snapshot = min(relu(ϕ25−ϕ23), relu(ϕ25−ϕ32)) centered (the existing selector).
Score^increment = min(Σ_{b∈b13..b23} relu(Δϕ_b), Σ_{b∈{29,30,31}} relu(−Δϕ_b)) centered
before rectification (the one candidate; sawtooth caveat known).

## Index mapping (sites; block/residual boundary convention as in the recovery report)

- h8: residual entering block 8 — EARLY, before the hypothesis build window b13..b23.
- h20: residual entering block 20 — the later reference (the operating point of the
  successful runs).
- Both single sites; NO interval; positions last-3 prefill + every decode; frozen final-
  prefill donor state at decode (per-layer donor residual d_l,o from the ACTUAL site layer,
  end-aligned).

## Conditions and count

| condition | selector | site | cells |
|---|---|---|---:|
| snapshot@h8 | snapshot3 | h8 | 12 |
| increment@h8 | increment | h8 | 12 |
| snapshot@h20 | snapshot3 | h20 | 12 |
| increment@h20 | increment | h20 | 12 |
| C0 (identity; expected_strength=0, selector=snapshot/site=h8 explicit in the spec entry) | — | — | 12 |
| random@h8, random@h20 (seeded GAUSSIAN rank-8 source/donor bases, joint removal, real donor states; DESCRIPTIVE, not norm-matched — the same control family as prior batches, NOT a vocab-sampling control) | | | 24 |
| **total** | | | **84** |

One model load; full 128/EOS continuations; the spec entries carry expected_strength +
expected_condition + expected_detector_layers (validated pre-model by the runner's
validate_specs — regression fixtures in tests/); snapshot centering BEFORE relu explicit
in both selectors; all 84 rendered input-ID arrays asserted equal to the exact-input bank
(task 1174). Actual full/P downstream ρ on same-history prefill recorded where the
existing instrumentation provides it (no new instrumentation built for this).

## Predicted semantic effects vs failure (registered per branch)

- **P1 (trajectory selection helps)**: PAIRED improvement — the increment condition shows
  more correct-facts + persistent-identity + coherence cells than the snapshot condition at
  the SAME site, with on-target/off-target outcomes counted separately (no absolute
  threshold imported from other batches — different C/operator histories).
- **P2 (selection difference does not reach behavior here)**: both selectors fail
  similarly — this does NOT imply the locus 'must be elsewhere'; the increment selector may
  simply be inadequate at these sites.
- **P3 (early-site warning)**: ANY change at h8 (including degradation) does NOT support
  useful early intervention; the prediction is EARLY IMPROVES correct transfer WITHOUT
  disproportionate unrelated change/incoherence. Confound recorded: the donor state/norm
  co-varies with site (an h8 donor residual carries different content than an h20 one).
- Failure/ambiguity modes registered: transient flips scored as transfer (rubric: identity
  must persist); loops counted separately from caps; randoms may move more at higher
  cumulative dose (declared descriptive); h8 edits may simply wash out (ρ/ρ_P recorded).

## Smallest-falsification note

P1 vs P2 is decided by the 2×(selector) comparison at EACH site; P3 by the site main
effect. 84 cells answers both with one load.
