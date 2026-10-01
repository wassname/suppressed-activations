# Native-metric erasure preflight

— PI/OpenAI. Specification: `slop/research/2026-10-01_output-erasure-geometry.md`. No pretrained candidate result.

- Mathematical reviewf983d414 found no blocker, conditional on held RMS scale. Native distance is not semantic distance; new output-space correction cannot be smaller than ordinary projection. One seed0 CPU float32 Gaussian control matches requested primary-J norm/coordinate only.
- Zero embedding/sensitivity/projected-random norm rejects the run. Zero extra naturally returns the ordinary correction; no normalization of extra or silent fallback.
- Actual production direction helper passes synthetic seeds0/1 in2s: nonidentity-J/gain, constrained minimum-native-norm solution, coordinate equality, random norm matching, scaling invariance and identity/zero-extra equivalence.
- Actual tiny BF16 Qwen main passes seeds0/1 in70s with nonidentity J:180 original rows/full generations/final states exact+72 candidate rows; one-pass coverage; independently formed B-matrix corrections, BF16 states/head scores and matched norms. Fixtures retained in `.local/native-metric-{0,1}-*/`.
- Actual coordinator passes20s against retained seed1 reference: one fresh tiny model,252 rows/144 fixed-position lists,180-row/state/generation parity and grouped report. Tiny random models do not validate pretrained discrimination; learned norm gains are covered by algebra, not these zero-initialized RMSNorm weights.
- Six existing cases/three positions only; no pooling, mask/alias/k/strength/data changes or v5. Original final-prefill greedy output only; no generated-text ranking, preparatory current-input pass, backwards or editor feedback.
- Production repeats one capture per case (≤192 generated tokens;2720 used15), asserts all180 previous rows/full generations/final states exact, and records corrections before/after casting. Same source/data/helpers/reference files pinned through execution. Immutable entrypoints do not sandbox working imports.

Predictions: if correction geometry was causing avoidable collateral suppression, hidden retrieval can improve at the same output-coordinate reduction. Output leaks/random ties/preclue gains can instead reveal anisotropy or output-conditioned priors. Inspect all144 lists, not only apple/autumn. A better rank is not semantic separation or goal completion. No new numeric acceptance threshold. One default-lane300s job; both goals remain open.
