# Bounded selector×site spec (for review — NOT queued)

2026-09-12, PI[glm-5p3-flash]. Deliverable requested by supervisor: exact equation, index
mapping, condition count, and predicted semantic effects vs failure.

## Equation and construction (identical for both selectors)

    # selector S in {snapshot3, increment} (selection differs ONLY in the score that picks
    # the per-position top-8 vocabulary; everything downstream identical)
    B_t^S = QR(center((u[top8(score^S_t)])·g))          # per window position (last-4)
    U_s^S = SVD-union_support([B_t^S over source window]);  U_d^S = same on donor window
    P_joint^S = support-filtered span([U_s^S | U_d^S])  # removal contains the injection
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
| C0 (identity) | — | — | 12 |
| random@h8, random@h20 (rank-matched random vocab, same construction; DESCRIPTIVE, not norm-matched) | | | 24 |
| **total** | | | **84** |

One model load; full 128/EOS continuations; expected_strength=1.5 + expected_condition
per spec entry (pre-dispatch contract validation via the runner's validate_specs — the
2154/1151 failure classes caught before load); exact rendered-input hashes from the
exact-input bank (task 1174) — the runner renders identically (asserted).

## Predicted semantic effects vs failure (registered per branch)

- **P1 (trajectory selection matters)**: increment@h8 or increment@h20 produces persistent
  donor identity on naming/legs (≥ the 1149-B profile: 3/12 full passes) where snapshot@
  same-site does not — supports the build-window selection hypothesis.
- **P2 (selection irrelevant at these sites)**: both selectors fail identically (spider
  everywhere) — the selection direction difference (Jaccard 0.02) does not reach behavior;
  the locus must be elsewhere (norm/site/policy).
- **P3 (site effect dominates)**: h8 arms differ from h20 arms in ANY direction — early
  intervention changes outcomes (supports the "intervene before buildup" idea);
  site-null results weaken it.
- Failure/ambiguity modes registered: transient flips scored as transfer (rubric: identity
  must persist); loops counted separately from caps; randoms may move more at higher
  cumulative dose (declared descriptive); h8 edits may simply wash out (ρ/ρ_P recorded).

## Smallest-falsification note

P1 vs P2 is decided by the 2×(selector) comparison at EACH site; P3 by the site main
effect. 84 cells answers both with one load.
