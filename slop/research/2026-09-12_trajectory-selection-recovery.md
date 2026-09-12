# Recovery: the motivating evidence and the selection gap (trajectory vs 3 snapshots)

2026-09-12, PI[glm-5p3-flash]. Goal 1 recovery/selection report. Sources linked inline;
formulas verbatim from the code; proposed selections as pseudopy. CPU/read-only; no banks
reused without the exact-input checks required by the plan.

## 1. The motivating evidence chain (recovered, source-linked)

1. **Gurnee et al., "Suppression Neurons"** (arXiv:2401.12181): after ~halfway depth,
   prediction neurons become prevalent, then "a sudden shift towards a much larger number
   of suppression neurons" at the end (quoted in main `README.md`).
2. **Wendler et al., "Do Llamas Work in English?"** (arXiv:2402.10588): the latent answer's
   English token "begins a sharp rise [mid-layers] followed by a decline, while [the output
   language] slowly grows and, after a crossover, spikes on the last five layers" (README
   quotes their figure).
3. **This repo's figure** (main `README.md`, `figs/suppressed_activations.png`, script
   `scripts/figure.py`): German→Chinese translation on Qwen3.5-4B; a **per-sample rank-32
   suppressed-activation subspace** contains **0.947 of the signed English readout share at
   L27** (held-out 53 prompts; different-prompt control 0.040/−0.015; 42/53 held-out
   prompts' top-32 rows contain the English answer token).

The user's percentages map to this curve: the English token builds from ~40% to ~70% depth
(layers ~13–23 of 32) and is deleted in the last 3 blocks. **The FIGURE is computed from
the whole layer trajectory; the SELECTOR is not** (below) — that is the gap the new plan
targets.

## 2. Detector history (git, main repo)

| commit | change |
|---|---|
| d4e5995 | publish subspace result |
| 67c683e | sample-specific suppressed-subspace interventions |
| 48b6519 | English demo — **(early, peak, output) = (23, 25, 32), rank default 8 (env-overridable; figure used rank 32)** |
| b3f63d4 → 9d56a63 | persistent/union readout variants, normalized-basis alignment |

The 3-snapshot form `residuals[:, [early, peak, output]]` has been in
`suppressed_activation_scores` since the first demo. The batchwork era added per-token
bases, temporal union/top-k, and alternate selectors — the score itself never changed.

## 3. Existing selector — exact formula (verbatim semantics)

Given the trajectory h_0..h_32 (h_l = residual entering block l; h_0 embeddings, h_32
final), RMS+gain readout ϕ_i(l) = ⟨ĥ_l, u_i⟩/‖u_i g‖ (row-normalized), vocab-mean-centered:

    rise_i  = ϕ_i(25) − ϕ_i(23)          # two points only
    fall_i  = ϕ_i(25) − ϕ_i(32)
    score_i = min(rise_i⁺, fall_i⁺)      # ⁺ = clamp_min(0)
    tokens_i = top-8 argmin... topk(score);  B_i = QR(center(u_tokens))   # per position
    temporal union = SVD of [B_t1|…|B_tW], support-filtered; top-k truncation optional

The selector sees the trajectory ONLY at l ∈ {23, 25, 32} — a 3-sample sketch of the
rise-and-fall the motivating figure shows over all 33 depths. Everything between
(per-block build shape, where the rise starts, whether the fall is gradual or a cliff) is
invisible to selection.

## 4. Proposed whole-trajectory selections (pseudopy; to be compared, not assumed)

Let W_build = depths 40–70% ≈ l ∈ [13, 23]; W_sup = last-3 blocks' outputs l ∈ [30, 32];
anchor a = h at the window start (l = 13 or the earliest available).

    # (a) area version of the current score (integrates the same sign structure)
    rise_area_i  = Σ_{l∈W_build} relu(ϕ_i(l) − ϕ_i(13))     # build-up mass
    fall_area_i  = Σ_{l∈W_sup}  relu(ϕ_i(30) − ϕ_i(l))      # removal mass (signed base = h30)
    score_i = min(rise_area_i, fall_area_i)                  # both-phases requirement kept

    # (b) shape match: correlate each token's readout curve with the canonical rise-fall
    t_l = the mean normalized English-curve template from the motivating figure (or the
          mean over TOP-scoring tokens under (a) — declared choice)
    score_i = corr(ϕ_i(·), t) over l∈[13,32], clipped at 0

    # (c) per-block increment form (localizes WHERE build/removal happens)
    Δϕ_i(l) = ϕ_i(l+1) − ϕ_i(l)
    build_i  = Σ_{l∈W_build} relu(Δϕ_i(l));  cut_i = Σ_{l∈W_sup} relu(−Δϕ_i(l))
    score_i = min(build_i, cut_i)

Each keeps the user's multi-token union + SVD top-k downstream construction unchanged
(bases from selected vocab per position → temporal union → SVD top-k). The DIFFERENCE from
the existing selector is only which tokens/directions the trajectory evidence selects.

## 5. The four independent axes (kept explicit per the plan)

| axis | current default | user hypothesis / plan space |
|---|---|---|
| selection layers | 3 snapshots (23, 25, 32) | whole trajectory, windows ~[40%,70%] + last-3 |
| intervention layers | L20/L25 single, or 6-site interval | BEFORE the build-up (≤ L13?) through post-build references |
| selected token positions (basis) | last-4 prompt positions, end-aligned | per-token union retained; window is a separate axis |
| edited token positions | last-3 prefill + every decode | unchanged (continuous steering default) |

## 6. Specificity and the two fall-interpretations (distinguished, not assumed)

- **Specificity vs unrelated vocabulary**: the original demo's different-prompt control
  (0.040/−0.015 signed shares) is the template; for the dog/ant selector the analog is
  (i) does the selected vocab contain the donor's answer token more than chance, (ii) do
  cross-prompt unions score near zero, (iii) the matched-random behavioral controls.
  Selection's own criterion never counts as proof (the plan's rule).
- **Normalized-readout fall vs geometric removal**: a falling ϕ_i can be numerator loss
  (⟨h_l, u_i g⟩ down), denominator growth (RMS(h_l) up), or within-span rotation. The
  existing diagnostics separate these (numerator/RMS decomposition; signed block
  decomposition; complement projection) — reuse them on the trajectory-selected sets; do
  not read "suppressed" from the fall alone. Astra's exact-trace finding (the reference
  edit overshoots the clean donor distance 0.56–3.35 → 8.27–11.95 inside the rank-4 span,
  cos-to-donor-difference 0.765–0.975) is the standing caution for interpretation.

## 7. Bank caveats carried into this work (from Astra's audit)

The dev/template banks used the runner-default wrapper, not the dev batches' explicit
instruction — bank geometry is ALTERNATE-WRAPPER evidence; the vector-map "top8" actually
retained numerical ranks 24–32 (true top8 keeps a mean 41.5% of full-union donor-vector
energy). Any reuse here requires exact rendered-token-ID + wrapper + revision + tensor-
definition match; otherwise a bounded exact-input extraction spec goes to the supervisor
first (not yet queued).

## 8. Falsifiable expectations for trajectory vs 3-snapshot selection (proposed, not results)

- If the trajectory selectors (a)/(c) select materially different top-8 sets than the
  3-snapshot selector (Jaccard on selected tokens; principal angles between unions), the
  3-snapshot version was losing build-phase information — visible CPU-only on exact-input
  traces.
- If the selected sets coincide (Jaccard ≈ 1), the 3-snapshot selector already captured the
  trajectory and the user's "you might have forgotten the whole-trajectory idea" would be
  answered: it was the motivation, and the 3 samples were a sufficient sketch — testable
  before any intervention.
- Either outcome is a usable result; neither requires new hypotheses about intervention.

## Unresolved questions (carried, not decided here)

Whether the late decline on EXACT current inputs is geometric removal or readout change;
which whole-trajectory score isolates useful vs unrelated directions; whether early
intervention survives/transfers or is overwritten; which rank gives the on/off-target
trade-off. The extraction spec for exact-input traces is drafted separately for supervisor
review.
