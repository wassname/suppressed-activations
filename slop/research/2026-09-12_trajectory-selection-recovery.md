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

The user's percentages (build ~40–70% depth, removed in the last 3 blocks) are a HYPOTHESIS
to verify on the current model/prompts — stated as such in the plan. They originate from the
Wendler curve as QUOTED IN main `README.md` (the original paper wording was not re-checked
against the arXiv source here); the README's own figure numbers (0.947@L27, 42/53, 0.040/
−0.015) come from `scripts/figure.py` + the held-out run recorded in the main repo. On
Qwen3.5-4B (32 blocks), 40–70% depth ≈ h13–h23 and the last-3 blocks are b29–b31 — a
hypothesis to measure, not a mapping to assume. **The FIGURE is computed from the whole
layer trajectory; the SELECTOR is not** (below) — that is the gap the new plan targets.

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
    tokens_i = topk(score_i, 8).indices  # LARGEST scores (the actual code), per position
    B_i = QR((u[tokens_i]·g − mean_v(u·g)))   # exact order: gain-scale rows, CENTER over
    #   vocab, THEN QR (subspace_from_scores); row-normalized variant divides ϕ by ||u·g||
    #   before differencing when normalize_unembedding_rows=True
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
    fall_area_i  = Σ_{l∈W_sup}  relu(ϕ_i(30) − ϕ_i(l))      # POST-PEAK fall (base = h30):
    #   omits the FIRST last-three write (b29's h29→h30, measured POSITIVE on dev inputs)
    fall_area_3_i = Σ_{b∈{29,30,31}} relu(−Δϕ_i(b))         # WHOLE last-3 variant: includes b29
    score_i = min(rise_area_i, fall_area_i)                  # both-phases requirement kept
    # LIMITATIONS (why only ONE candidate is carried forward, and neither (a)-variant is
    # 'the' selector): (i) area sums and increment sums are DIFFERENT functionals — areas
    # credit sustained elevation, increments credit local changes; (ii) min() over windows
    # of unequal length biases toward the shorter window; (iii) positive-increment sums
    # credit oscillation (up-down-up counts twice). A chosen variant must declare these.

    # (b) shape match: correlate each token's readout curve with the canonical rise-fall
    t_l = the mean normalized English-curve template from the motivating figure (or the
          mean over TOP-scoring tokens under (a) — declared choice)
    score_i = corr(ϕ_i(·), t) over l∈[13,32], clipped at 0

    # (c) per-block increment form (localizes WHERE build/removal happens)
    # block indexing: blocks b0..b31; block b writes Δh_b = h_{b+1} − h_b; the LAST-THREE
    # writes are: b29: h30−h29, b30: h31−h30, b31: h32−h31 (h33 does not exist).
    Δϕ_i(b) = ϕ_i(h_{b+1}) − ϕ_i(h_b)     # the readout change across block b's write
    build_i  = Σ_{b∈B_build} relu(Δϕ_i(b))          # B_build = b13..b23 (per the hypothesis)
    cut_i    = Σ_{b∈{29,30,31}} relu(−Δϕ_i(b))      # exactly the last-3 writes
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

- **Specificity vs unrelated vocabulary**: controls to DESCRIBE (no assumed chance
  baseline — what 'near zero' means for same-concept cross-prompt unions is itself
  unknown): (i) whether the selected vocabulary contains the donor's answer token (its
  presence is NOT independent concept specificity — the readout search favors answer-like
  tokens by construction); (ii) cross-prompt same-concept vs cross-concept union overlap
  and score distributions (descriptive); (iii) matched-random behavioral controls.
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

- DIFFERENT selected sets under a trajectory selector would show SELECTOR SENSITIVITY to
  the added trajectory evidence — NOT that the 3-snapshot version 'lost useful build
  information' (that requires held-out descriptive specificity differences or eventual
  behavioral differences to establish).
- SAME/near-same sets would NOT prove the 3 samples sufficient either — only that these
  selectors agree on these inputs; sufficiency is a claim about downstream behavior.
- Either outcome is a usable result; neither requires new hypotheses about intervention.

## Unresolved questions (carried, not decided here)

Whether the late decline on EXACT current inputs is geometric removal or readout change;
which whole-trajectory score isolates useful vs unrelated directions; whether early
intervention survives/transfers or is overwritten; which rank gives the on/off-target
trade-off. The extraction spec for exact-input traces is drafted separately for supervisor
review.
