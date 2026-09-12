## Current-plan section: trajectory-selection comparison (2026-09-12, added without touching the historical sections above)

The historical 6/12 above is preserved unchanged. The 2026-09-12 plan tested whether the
suppressed subspace should be selected from the WHOLE layer trajectory (the user's
build ~40-70% / last-3-removal hypothesis) instead of the 3-snapshot approximation
(layers 23/25/32), and whether early intervention (h8, before the build) helps.

**Observed (12 dev questions, same injection/removal equation, C=1.5 where noted; all
counts from saved per-row adjudications in the batchwork repo):**

- The two selectors pick essentially different vocabulary (set Jaccard 0.020; executed
  regression: snapshot scores bitwise-equal the canonical `suppressed_activation_scores`
  on the same tensors — tolerance agreement).
- The increment selector's selections include topic tokens (` legs`, ` leg`, `-legged`)
  the 3-snapshot selector misses — consistent with an early build window — but at tested
  sites (h8/h20) NEITHER selector's subspace produced donor answers or identity
  (84-cell selector×site comparison; all spider-bound continuations).
- Ablation at the reference operating point: the injection term carries the effect
  (injection-only ≈ full edit) and removal-only did nothing — measured at C2.5 (an
  actual-strength mismatch vs the labeled C1.5; scoped to that setting).
- Norm/direction factorial at fixed L20/P_ref: the template-label direction transfers
  only at its own (higher) norm; the donor-projection direction at the same higher norm
  degrades rather than transfers (1/12 with one persistent dog-identity naming answer).
- Cross-depth donor import (late-built h25 component injected at h8, 14× larger):
  no transfer; donor-correct answers with spider identity + false factual claims
  (4/12) and loops (4/12).

**Caveats:** dev/template banks captured an alternate wrapper (labeled diagnostics);
three later families ran at actual C2.5 vs labeled C1.5 (withdrawn factorial
interpretations); token readouts are vocabulary-level statistics, not established
semantics; the historical 6/12 remains the reference intervention's measured reliability
on the declared fresh set.
