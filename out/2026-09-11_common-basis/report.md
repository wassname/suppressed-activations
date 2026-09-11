# Common-basis descriptive table (CPU, trajectory bank only)

Written 2026-09-11 by PI[claude]. No intervention run; all numbers computed GPU-free from the saved
bank. Sources: `out/2026-09-10_trajbank/{source,dog,ant,control}_detector.pt` (per-token rank-8
orthonormal bases, built by QR of centered norm-gain-scaled unembedding rows selected by top-8
suppression scores over layers 23/25/32), `out/2026-09-10_trajbank/*_residuals.pt` (33 layers ×
seq × 2560 clean residuals), `manifest.json`. Script: `scripts/common_basis_table.py`;
raw numbers: `table.json`, `capture_by_basis.json` in this directory.

Construction under test (user's union(A,B) proposal): concatenate per-token orthonormal bases over
a token window, M = [B_t1 | … | B_tN] ∈ R^(2560×8N), SVD, common projector from the LEFT singular
vectors (eigenvectors of the average projector Σ_t B_t B_tᵀ). Windows are end-aligned: `last2`,
`last4` (…, ' is', ' '), `tail` (everything after ' that'), `all`.

## 1. Union spectrum: weak shared projector concentration

Note: `det['basis']` is ONE detector-selected basis per token (selection criterion computed over
layers 23/25/32), reused across all layers. The by-layer table below therefore measures residual
projection onto a FIXED selected span, not changing layer-local subspaces.

| union (prompt:window) | n tokens | cols | s1 | s8/s1 | eff. rank | E(top4) | E(top8) | E(top16) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| source:last4 | 4 | 32 | 1.207 | 0.870 | 31.2/32 | 0.162 | 0.302 | 0.562 |
| dog:last4 | 4 | 32 | 1.246 | 0.838 | 31.3/32 | 0.158 | 0.297 | 0.556 |
| ant:last4 | 4 | 32 | 1.542 | 0.679 | 28.6/32 | 0.194 | 0.333 | 0.592 |
| control:last4 | 4 | 32 | 1.265 | 0.826 | 31.2/32 | 0.160 | 0.299 | 0.556 |
| source:last2 | 2 | 16 | 1.073 | 0.935 | 15.9/16 | 0.272 | 0.525 | 1.000 |
| dog:tail | 11 | 88 | 2.061 | 0.656 | 57.6/88 | 0.158 | 0.256 | 0.375 |
| ant:tail | 12 | 96 | 1.999 | 0.623 | 75.3/96 | 0.112 | 0.183 | 0.293 |
| source:all | 14 | 112 | 1.742 | 0.678 | 97.8/112 | 0.082 | 0.135 | 0.231 |

The average-projector spectrum is nearly FLAT: effective rank ≈ the full 8N everywhere, s8/s1
0.62–0.94. This supports weak shared projector concentration between per-token bases, i.e. the
union behaves close to a direct sum; it does not by itself rule out a smaller shared component
below top-8. For 2 near-orthogonal 8-dim bases the TOP8-TRUNCATED union captures 0.525 of each
basis (full union captures 1.0 by construction); the observed 0.525–0.536 ≈ 0.5 + small overlap
is consistent with near-orthogonality rather than a shared axis.

## 2. What a common top8 projector captures

Per-token capture = fraction of each token's own basis inside the common top-k span (mean over
window); residual energy = mean over window tokens of the per-token energy fraction
‖P r_t‖²/‖r_t‖² at L25 (from `capture_by_basis.json`). The `table.json` `resid_frac_L25` field is
the mean NORM fraction ‖P r_t‖/‖r_t‖ — a different unit; do not square one to get the other.

| prompt:last4 | capture(top8) | capture(top32) | own-basis energy L25 | full-union energy L25 | top8-union energy L25 |
|---|---:|---:|---:|---:|---:|
| source | 0.302 | 1.000 | 0.022 | 0.051 | 0.021 |
| dog | 0.297 | 1.000 | 0.020 | 0.041 | 0.021 |
| ant | 0.333 | 1.000 | 0.015 | 0.033 | 0.011 |
| control | 0.299 | 1.000 | 0.018 | 0.030 | 0.010 |

A top8 common projector keeps ~30% of each per-token basis and ~2% of residual energy at L25
(≈14% of residual norm). The full union (rank 32) contains every per-token basis exactly
(capture 1.0) and captures ~3–5% of residual energy. The suppressed subspaces are small slices
of the residual stream at every layer.

## 3. Layer profile (top8 union, last4): fraction of residual norm / mean raw norm

| prompt | L0 | L8 | L16 | L20 | L23 | L25 | L28 | L32 |
|---|---|---|---|---|---|---|---|---|
| source | 0.41/1 | 0.07/7 | 0.05/11 | 0.06/17 | 0.07/23 | 0.14/28 | 0.13/35 | 0.11/66 |
| dog | 0.25/1 | 0.07/7 | 0.04/11 | 0.07/16 | 0.08/23 | 0.14/27 | 0.14/36 | 0.10/71 |
| ant | 0.21/1 | 0.05/7 | 0.04/11 | 0.04/16 | 0.04/24 | 0.10/28 | 0.08/36 | 0.06/74 |
| control | 0.32/1 | 0.05/7 | 0.05/10 | 0.05/16 | 0.06/24 | 0.10/28 | 0.09/37 | 0.06/70 |

Residual norms grow ~66–74× from L0 to L32 while the top8-union fraction stays ≤0.14 — the
suppression subspaces do not grow with the stream; the "increase" the user asked about is in the
raw residual norm, not in the subspace share. The top8 fraction peaks around L25–28 (0.10–0.14)
and falls by L32, matching the detector's peak-layer design.

## 4. Activation cosines (separate diagnostic; NOT the subspace metric)

Mean off-diagonal cosine between window tokens' residuals, raw vs projected onto the prompt's own
top8 union:

| prompt:last4 | L23 raw/proj | L25 raw/proj | L32 raw/proj |
|---|---|---|---|
| source | +0.49/+0.61 | +0.48/+0.84 | +0.47/+0.89 |
| dog | +0.42/+0.60 | +0.42/+0.83 | +0.52/+0.88 |
| ant | +0.50/+0.58 | +0.46/+0.77 | +0.52/+0.83 |
| control | +0.52/+0.38 | +0.47/+0.64 | +0.40/+0.28 |

Projected residuals inside the shared top8 are more aligned (0.6–0.9) than raw residuals
(0.4–0.5). Part of this rise can come from projection onto a common low-dim span alone
(shared-mean effect), so it is not by itself evidence of shared semantics; with only 4 prompts
the animal-vs-control difference (control collapses at L32: 0.28 vs 0.83–0.89) is suggestive,
not established.

## 5. Cross-prompt subspace affinity (mean cos² of principal angles, top8 unions)

8/2560 = 0.003 is the Haar-isotropic reference for two random 8-dim subspaces, NOT an empirical
null for unembedding-row-selected bases (which are centered and share the norm-gain geometry, so
their chance overlap can be higher). Treat the 10–20× margin accordingly.

| pair | last4 | tail |
|---|---:|---:|
| source–dog | 0.038 | 0.039 |
| source–ant | 0.056 | 0.044 |
| source–control | 0.037 | 0.037 |
| dog–ant | 0.030 | 0.053 |

Shared support between prompts is real (10–20× above chance) but small (~3–6% of variance), and
NOT specific to animal pairs — source–control is the same as source–dog. A common
source+donor basis is therefore mostly the direct sum, not a shared axis:
combined source+dog last4 union has eff. rank 58.9/64, E(top8) 0.188.

## What the table says for the paired comparison (inference, labelled)

- At the projector level the union is close to the direct sum of per-token projectors: weak
  shared concentration means a full-union projector at every position edits each token's
  residual by ~5% energy (own 2% + other tokens' ~3%), vs the per-token baseline's 2%.
- Top8 union is a smaller, different edit (~2% energy, 30% of each basis), concentrated where
  projected activity agrees (§4).
- Shared source–donor support is small and not animal-specific (§5), so a joint projector is
  unlikely to carry donor identity by itself; whether transfer rides the delta term or the
  shared span is what the paired comparison tests — the table does not decide it.

## First batch (GPU, one model load via batch-spec, NOT queued yet)

Common replacement procedure, identical to the frozen candidate except the projector basis:

```
U_c = left singular vectors of M(source:last4 bases ∥ donor:last4 bases)   # common basis
h'  = h + C (δ − U_c U_cᵀ h)        # same span-corrected equation, C = 1.5, L20
```

- δ unchanged: the frozen donor template-contrast attenuation delta (end-aligned positions).
- Positions: source last-3 prompt tokens + every decode step (continuous steering, full coverage,
  prefill + cached decode, coverage asserted).
- Conditions (5, spider source, dog donor first): A per-token baseline (frozen reference);
  B full union (rank 64); C top8 union; D matched-random: random direction INSIDE span(U_c),
  per-call applied-norm matched to the same-condition candidate per call (declared reference
  trajectory = the candidate's own trajectory, per the audit's per-call matching policy);
  E C0 identity. Full continuations to 128 tokens, swap_log_odds_shift, p_valid, r2, readouts,
  per-call norm logs, paired lengths reported.
- Discriminating read: if B ≈ A (predicted) but C diverges, the shared top8 span is where
  cross-token structure lives; if D at matched per-call norm still fails to carry identity,
  the magnitude confound from the fresh-eval audit is bounded.

## Limitations

Descriptive only: no causal claim. Bases are the bank's rank-8 detector bases (layers 23/25/32
selection criterion), layer-independent by construction; window choice is end-aligned and could
be re-run at other windows from the same bank. Single model (Qwen3.5-4B rev 851bf6e8), 4 prompts.
