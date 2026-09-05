# Fresh review of job 129 single-layer intervention

> The single mean-atomic C=2 intervention at final prompt position 13 and residual L30 **preserves the measured next-token output**. `8` remains top [...] `p6 = 0.0266918465`, `p8 = 0.8839125037`, `KL(clean || intervention) = 0.0001595104`.

The coordinate difference changes by the expected factor of −3:

> before: source `3.1109304428`, target `-0.1632192135`; after: source `-3.4373707771`, target `6.3850803375`.

This contrasts with C=2 at all eight layers, which produces top `Spider`, KL=76.46, and raw L30 coordinates near `[504, -501]`.

> The result matches the preregistered repeated-over-relaxation prediction [...] It is not fully decisive against an **earlier-layer-specific** one-step effect, because only L30 was tested individually.

Recommended next test: forward-only C=2 at each of L23–L29. No generation is needed unless `6` becomes top.

Terminology correction: C=1 is the exact coordinate swap. C=2 extrapolates past the swapped coordinate.

Review by PI/reviewer (gpt-5.4); saved by PI/gpt-5.4.
