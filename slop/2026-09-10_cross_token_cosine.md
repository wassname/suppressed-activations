# Cross-token signed-cosine agreement of suppressed components

Goal 1, bounded first assignment. Question: does the user's proposal — "what if we need the
cosine overlap of suppressed activations from 2+ tokens have we tried that" — identify a
reusable, directionally consistent suppressed component that the existing shared-subspace
selection misses, and does steering along it behave differently from the avg-projector selector?

## Status

- Method built and smoke-tested on the tiny CPU model (`wassname/qwen3-5lyr-tiny-random`).
- GPU verification (spider→dog, spider→ant) queued on pueue `default` as jobs 990/991, behind a
  foreign LUCID3 train chain. Completion watcher armed (`pueue wait 990 991`).
- Brainstorm complete: two model families reviewed independently (links below).
- **First submission failed and was repaired** — see "Failed first submission" below.

## The missing distinction

`token_persistent_subspace` stacks each token's orthonormal suppressed basis and takes a thin
SVD. That yields eigenvectors of the *average projector*; "persistence" = squared singular
value / token count. It is a sign-invariant measure of shared subspace span.

The user's proposal is different: measure whether the *actual projected residual component
vectors* (c_p = component(residual_p, B_p)) agree in sign across token positions. A subspace can
have high principal-angle overlap while c_p and c_q are anti-aligned within the shared span.
Both reviewers independently confirmed this is a real, untested distinction.

## Implementation checks (verified, not assumed)

- `component(h, B)` = h @ (B Bᵀ) is exactly sign-invariant to per-column basis sign flips
  (numerically verified: max diff 0.0). QR sign ambiguity therefore cannot corrupt the signed
  cosines. This answers GLM's sign-convention objection directly.
- Reuses the verified `intervention_hooks` / `trajectory` / `generate` from `scripts/demo.py`.
- Existing subspace unit tests (`uv run --with torch --with numpy python -m scripts.test`) all
  pass; the new script is isolated and modifies no verified core code.

## Review convergence (GLM 5.3 Flash + Kimi K3)

- Signed cosine of c_p and subspace overlap carry mathematically disjoint information; both are
  needed, either alone is insufficient.
- A high raw cosine is weak evidence by itself: shared residual mean, one dominating token,
  generic syntax, and residual-stream anisotropy all inflate it. Mean-centering and a
  cross-prompt baseline are essential controls.
- Cheap gates before GPU generation: centered signed cosine, cross-prompt baseline, unembedding
  logit probe, norm fraction. These can reframe or kill the hypothesis at near-zero cost.
- The behavioral arm (does steering along signed-agreement vs avg-projector change the full
  continuation?) is the final discriminator.

Kimi's strongest objection: donor_add hurting removal (5.38 < 6.13 nats) plus the reported
"L20 diff = 0.000" may indicate a sign-blind selector or an application bug rather than a
missing cross-token measurement. I weight the L20-zero lightly: it came from a probe later
withdrawn for a scalar-index bug (plan Learning, 2026-09-10). The behavioral comparison tests
whether the edit reaches and changes the continuation regardless.

## Method (scripts/cross_token_cosine.py)

For a fixed intervention layer, over the last `readout_positions` token positions:
- Per-position suppressed subspace basis B_p from the detector (early, peak, output).
- Actual suppressed component c_p = component(residual_p, B_p).
- Signed cosine agreement: mean pairwise cos(c_p, c_q); norm-of-mean over mean-norm;
  mean-centered signed cosine (shared-mean control); drop-max-norm variant.
- Sign-invariant subspace overlap: avg-projector SVD spectrum; principal-angle cosines between
  consecutive per-position subspaces.
- Magnitude kept separate: per-position component norms, residual norms, component-norm fraction.
- Cross-prompt baseline: same-form neutral control prompt; cross-prompt mean cosine tests whether
  agreement is concept-specific or a shared mean / syntax edge.
- Unembedding logit probe: does each candidate direction raise the target concept token logit
  after RMSNorm + gain-weighted unembedding?
- Behavioral comparison: `replace` edit (same layer, same strength) along three rank-1 bases —
  signed-agreement direction, avg-projector span direction (recovered reference), matched-random
  control — each with a full 32-token continuation.

## Prior evidence recovered

- 2026-09-07 SVD token-persistence (rank 1, L24, 4 tokens, C=12): source_remove p(6)=0.79 /
  swap shift 6.13 nats; combined 0.67 / 5.38; donor_add 0.01 / 0.0. Removal dominates and the
  continuation still writes "the animal that spins webs is the spider" — identity not
  transferred. [Audit](audits/2026-09-07_svd-token-persistence.md).
- 208 development conditions on the corrected generation-capture path; random and dog-directed
  settings also produce 6, weakening target specificity. Development search, not validation.

## Failed first submission (correction record)

Jobs 985/986 were queued referencing `slop/cross_token_cosine_run.sh` before verifying the
launcher existed on disk; that write had silently failed, and 985's argv also carried an
unquoted apostrophe in `man's`. Both failed without exercising the experiment (exit 2 and 127).
Logs: [job 985](audits/2026-09-10_crosstoken-failed-jobs/job985_unquoted_apostrophe.log),
[job 986](audits/2026-09-10_crosstoken-failed-jobs/job986_missing_launcher.log).
Repair: launcher now takes only `dog|ant` as argv with prompts hardcoded inside (no quoting
failure possible), verified on disk, `bash -n` clean, and executed end-to-end on the tiny model
before requeueing as jobs 990/991.

## Supervisor code review — repairs before GPU spend (2026-09-10)

Before any GPU execution, six causal-comparison invalidities were found by direct code
inspection and repaired:

1. **Shared absolute positions.** `window`/positions were derived from the source length and
   reused for donor/control, sampling unrelated positions when prompt lengths differ. Each
   prompt now uses its own end-aligned window; the smoke artifact shows source [12,14),
   donor [19,21), control [14,16).
2. **Missing positions argument.** `run_selector` never passed `positions`, so prefill patched
   one position while logging three. Now passed, and per-call coverage (prefill positions,
   decode calls, generated tokens) is recorded and asserted. Zero-strength identity is asserted
   against base logits (observed: "logits identical to base").
3. **Weak random control.** The random control was an unmatched rank-1 basis that skipped
   generation. It now generates and its per-position perturbation norms match the semantic
   avg-projector edit (smoke ratios exactly 1.0), kind-aware: prefill matches per-position
   semantic norms, decode calls match the semantic mean decode norm.
4. **Rank-1 norm-matching degeneracy.** With one shared rank-1 basis, `match_component_norm`
   rescales the donor onto the source's own magnitude: verified exactly — equal-sign edits are
   a no-op (residual 5.96e-8) and opposite-sign edits a pure reflection (2|sc| exactly). That
   erases the signed distinction under test. Replaced with shared-coordinate replacement
   without component-norm matching and without residual-norm restore; donor magnitude is kept
   and perturbation/residual norms are logged per call so norm growth is visible.
5. **Unsupported causal claim** in the unembedding-probe comment removed; it is labelled a
   linear readout diagnostic, not a causal statement.
6. **Revision pinning.** Tokenizer and model now both pin revision 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a
   for real runs (tiny smoke still overridable via env).

An interim bug found while verifying (3): the matched control applied the strength a second
time on top of strength-including reference norms (observed ratios 0.125 = strength); fixed so
control perturbation equals the semantic perturbation exactly.

First-round smoke outputs from the flawed script were replaced by uniquely named v2/v3 smoke
dirs (`out/*_smoke_crosstoken_v2`, `out/*_smoke_crosstoken_v3`); the flawed form was never run
on GPU.

## Result

Pending GPU (jobs 990/991). Will be filled from
`out/2026-09-10_crosstoken_dog/result.json` and `out/2026-09-10_crosstoken_ant/result.json`.

## Verification

- Smoke (tiny CPU): `out/2026-09-10_*_smoke_cross_token_cosine/result.json`.
- GPU: `out/2026-09-10_crosstoken_{dog,ant}/result.json` (queued).

-- PI[claude]
