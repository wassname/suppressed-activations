# Handover (compact, 2026-09-12, context pressure)

## State

- The worker resumed SOLE implementation ownership (Astra stopped; the reviewer c45f5369
  read-only).
- Intercom UNAVAILABLE in this session (tool lookup fails) — reports via
  `slop/research/2026-09-12_resume-report.md` (the channel the supervisor reads) + the
  final tool-return artifacts.

## What's DONE (all committed)

- F1–F7 (the evidence-review fixes): implemented + executed; the checker
  `scripts/notebook_check_evidence.py` (228 rows verified; escape-aware text/plain
  parsing). The notebook changes ON DISK in main (the commit blocked by the shared
  index.lock — the supervisor handles it).
- The complete-edit ladder: implemented, contract-validated, run 3× (1245's results stand;
  the kfull arm was top8-in-disguise; fixed in bb240c7).
- The full-support regression: tests/test_complete_edit.py (through the PRODUCTION
  complete_edit_bases fn — factored from run_with_bundle; the old-bug mutation Pj 16 vs
  57; nesting; k8 unchanged).
- The runtime ml-debug controls (scripts/runtime_controls.py + the log): the self-donor
  identity, C0 logits equality, cached/uncached same-history placement — all PASS through
  the PRODUCTION hooks.

## The pending item

- The RANK LADDER GPU rerun with the fixed full flag (bb240c7): NOT queued — waiting for
  the supervisor's go.

## The key facts

- The donor-projection direction family (v = Pd d) is exhausted at the tested settings
  (sites h8/h20, depths h8/h20/h25 anchors, ranks 1–8, selectors): never a coherent donor
  transfer; 1/12 at the best tested point (the high-norm v).
- The template-label δ_ref′ direction: the only transferring injection (A 6/12 fresh,
  B 3/12 dev, injection-only sufficiency at its C).
- The rank ladder's dose-response: the loop collapse tracks the injected dose (edit fracs
  1.1–2.5); no rank transfers.

## The open questions

- The early-repetition mechanism (H7) — the C dose sweep at fixed h1 is the probe.
- The full-support ladder's behavior (the fixed flag; not yet run).
- The tuned-lens/half-life framing — untested.

## The runtime-control implications (post-controls)

The production hooks PASS: the self-donor identity, C0 equality, the cached/uncached
placement. The runtime mechanics are NOT the repetition's cause (per the ml-debug form's
cheapest discriminator). The remaining repetition hypotheses: the repeated FROZEN donor
injection's semantic effect (C) — the dose sweep at fixed h1 (the audit's probe) is the
next test; no repetitions interpretation yet.

## The next bounded GPU candidates (awaiting the supervisor's go)

1. The rank-ladder RERUN with the fixed full flag (bb240c7): the kfull arm now the full
   supported bases.
2. The C dose sweep at fixed h1/imported (the audit's H2 probe): C in {0.3, 0.7, 1.0, 1.5}.

## Correction (2026-09-13, worker f15929b4)

The "cached/uncached placement — all PASS" claim above rested on a VACUOUS test:
section 3 of scripts/runtime_controls.py ran generate_with_first_logits with EMPTY
hooks and max_new_tokens=1 (no cached decode) and asserted only the first token;
res1/logits1 were computed and never used. Rebuilt and executed for real
(slop/reviews/2026-09-13_runtime-controls-audit.md, spec
slop/2026-09-13_runtime-controls-spec.md): teacher-forced fixed-history comparison
over prefill + >=3 cached decode steps with a real nonzero production-hook edit
(uncached reference edits prompt-last3 AND all generated positions at the same
layer), in-run null-calibrated tolerances, wrong-mask/no-hook discrimination probes.
PASS on tiny CPU (bf16+fp32) and Qwen3.5-4B GPU (single layer L26, rank 256, C=8;
fp32 exact, bf16 within null noise, one exact-tie argmax flip explained). The
conclusion "runtime mechanics are not the repetition's cause" is now supported for
the tested single-layer mechanics only; multi-layer interval hooks remain untested.
The positive pinned reference was also re-executed via the exact existing
confirm_causal_demo.py path: generations byte-identical, clean/C0 exact, C4
probabilities reproduce to ~0.03 (top tokens and 256-random-control percentiles
agree). -- PI[glm-5p3-flash]


## Historical (withdrawn or stale) claims — do not cite as current

- The donor-projection direction family (v = Pd d) is exhausted at the tested settings

## Selector thinking deliverable (2026-09-13, CPU only, no model calls)

**One specific unresolved selector assumption**: the production selector scores tokens
from THREE sampled depths (early 18 / peak 20 / output 32 on the legs family) — it
assumes the rise-and-fall shape between and before those points carries no information.
The saved selected_traces (out/2026-09-12_selector-comparison-v2/selector_comparison.json)
confirm the arrays only store 4 layers per token — the full-depth behavior is not
observed anywhere in current selection evidence.

**Cheapest discriminator (ran on existing arrays, zero model calls)**: the exact-input
bank (out/2026-09-12_exact-input-bank-att3, h0..h32 float32 trajectories of the exact
legs prompts, spec/script hashes in its manifest) makes the full-trajectory score
computable on CPU. Quoted lines (fulltrajectory-vs-3snapshot.txt):

> top-32 overlap (snapshot vs full-trajectory): 2/32
> snapshot misses 30/32 of full-trajectory top; missed tokens' variation BEFORE layer
> 18 (mean share): 0.556
> top-32 overlap normalized-logit vs raw-energy: 8/32

**Reading**: (1) the three-point selector and the full-trajectory selector disagree on
30/32 top tokens — the assumption is load-bearing, not a formality; (2) the missed
tokens carry ~56% of their variation BEFORE the selector's earliest anchor (layer 18) —
directly relevant to the user's early-intervention plan (intervene at h1): selection
anchored at 18 cannot see build-up in layers 1-17; (3) normalized-logit readout and raw
projected energy select 8/32 agreement — they are different selectors, and the
normalized readout can fall while raw projected energy rises (RMS growth swamps it);
the goal's discriminator language requires keeping them separate.

**Next discriminator proposal (proposal only, no GPU queued)**: recompute the selection
on the same bank with the full-trajectory score and compare the resulting top-8
subspaces' causal behavior at h1 in the existing six-row design — one bounded batch,
only after review. -- PI[glm-5p3-flash]

## CORRECTED selector comparison (2026-09-13, replaces the strawman entry above)

The entry above compared against a SNAPSHOT STRAWMAN (18/20/32) — misdescribing the
current production selector. The ACTUAL production baseline
(`suppressed_activation_subspace.increment_scores`, used by common_selector='increment'
in all current families) is ALREADY whole-trajectory: normalized readout at every
layer, per-write increments dphi[b] = logits[b+1]−logits[b] VOCAB-CENTERED before
rectification, build = sum of positive increments over the ~40-70% window, cut = sum
over exactly the last-3 writes, score = min(build, cut). Anchors bound windows; the
score uses all increments within them.

Executed comparison (script + arrays SAVED: scripts/selector_increment_vs_tv.py,
out/2026-09-13_selector-increment-vs-tv/selector_comparison_arrays.pt; log
.local/verify_logs/demo-evidence/selector-increment-vs-tv.txt; input sha in-array):

> top-32 overlap production-increment vs total-variation: 0/32

My total-variation probe (all-layers positive variation, vocab-centered, no
min(build,cut) conjunction, oscillation-permissive) shares ZERO of 32 top tokens with
the production selector. The probe rewards any oscillation and magnitude, not the
build-then-cut shape; it is NOT a deleted-energy measure (no claim that variation
equals deletion). The earlier "2/32 vs snapshot" numbers compared the wrong baseline
and are retracted as a selector description.

Sampled token trace (CORRECTED axes — the previous version selected layer 0 across
vocab instead of the token across layers, and mislabeled the signed projection as
"energy"): top production-increment token on the exact legs-dog source bank = token
243784 ' Конкурс' at position 48. Full 33-point traces saved (normalized readout,
vocab-centered per-write increments, residual RMS, signed projection, energy=signed²;
arrays in out/2026-09-13_selector-increment-vs-tv/selector_comparison_arrays.pt with
the residual-file sha256 labeled as such and the manifest's input-ID hash separate).

Reading, per-token observation not a general claim: the normalized readout builds from
layer 20 (2.50 → 3.49 peak at layer 24) then falls to −1.655 at the final write (cut
−2.145 vocab-centered). The SIGNED projection goes 1.99 → −2.135 while the energy
(signed², nonnegative) PEAKS at the final layer (4.56) — for this token the last
write INVERTS the readout direction rather than removing projected energy. Also: the
first write's +10.7 increment is an RMS artifact (0.02→0.04). The production
min(build, cut) selects this token via the normalized shape; whether sign-flip vs
energy-removal is the general suppression mechanism is exactly the
normalized-readout/raw-energy distinction and is untested beyond this token.

Unresolved selector question, narrowed: whether min(build-window, last-3-cut) — the
current conjunction — is the right trade-off vs e.g. per-position full-window
build+cut with the same conjunction; the TV probe does not answer it. No GPU runs.
-- PI[glm-5p3-flash]

## Per-position selection class counts (2026-09-13, CPU, existing banks)

Among ACTUAL production-selected tokens (per-position top-8 with min(build,cut)>0
enforced; 24 selected per input over the 3 edited positions), the FINAL-WRITE behavior
classes (readout at last layer vs previous, same state):

> source (spider question): sign_flip 11, positive_fall 5, more_negative 8, energy_drop 12/24
> dog (donor question): sign_flip 13, positive_fall 10, more_negative 1, energy_drop 21/24
> ant (source file = same spider question as dog-source; files differ only by
> extraction-run hash, tensor sums exactly equal — deterministic extraction, so the
> identical counts are expected, not a bug)

Reading (counts, not proof): the dominant final-write behavior among selected
directions is SIGN FLIP (11-13/24), with energy drops in only 12/24 (spider) and
21/24 (dog) — i.e. for about half the spider-selected directions the final-layer
energy does NOT drop while the normalized readout still "cuts". This sharpens the
normalized-readout/raw-energy distinction: much of what the selector sees as a cut is
sign inversion, not removal. Examples with exact last-3 readouts saved in
per_position_class_counts.json. Also fixed this round: production eps (1e-6) in the
RMS, identity assert lg == full_lg[:, tok] (assert_close), and the aggregate-vs-pos48
rank labeling. -- PI[glm-5p3-flash]

## Exhaustive final-write classification (2026-09-13 v2, supersedes the counts above)

Previous counts retracted (classification tested historical max / lacked fall tests;
ant input was the ant-SOURCE not the ant DONOR). v2: exhaustive signed prev→last
classes (machine-partition-asserted, sum == n_selected), selection = the ACTUAL
production top-8 per position (score>0 mask recorded; ~217k/248k tokens have score>0 —
the top-8 is the real selection), raw signed/energy before-after values saved for ALL
72 selected pairs, ant = legs-L1-ant-donor (manifest-verified 'colonies' prompt):

> source_spider: pos->neg 11, neg->pos 0, nonneg-inc 2, nonneg-dec 3, nonpos-inc 0,
>   nonpos-dec 8, equal 0 | energy last<prev 5/24, last<start3 7/24
> dog_donor:     pos->neg 13, neg->pos 0, nonneg-inc 0, nonneg-dec 10, nonpos-inc 0,
>   nonpos-dec 1, equal 0 | energy last<prev 17/24, last<start3 20/24
> ant_donor:     pos->neg 16, neg->pos 0, nonneg-inc 0, nonneg-dec 1, nonpos-inc 0,
>   nonpos-dec 7, equal 0 | energy last<prev 4/24, last<start3 8/24

Reading (counts): neg->pos NEVER occurs. The dominant final-write class is pos->neg
(11-16/24). Energy at the final layer is LOWER than the previous layer in only 5/24
(spider) and 4/24 (ant) — for most source/ant selected directions the normalized-readout
cut is SIGN INVERSION, not an energy drop. Donor input differs (17/24, 20/24). Raw
before/after values for all pairs in per_position_class_counts.json (v2). No claim
about raw energy "removed" — the comparisons are last-vs-prev and last-vs-start3
explicitly. -- PI[glm-5p3-flash]

## h20-specificity discriminator DRAFT (proposal only, no GPU/queue)

Question: are the h1-selected directions the SAME semantic directions that made the
h20 historical rows work, or a different selection that merely shares the site?

Candidate discriminator with ACTUAL source formulas, CPU first:
1. Recompute via the production construction (no new method): the h1 basis = the
   saved artifacts (basis_*_C1.5.pt, joint 16); the h20 basis = re-run the SAME
   construction with intervention_layer=20 on the same bank residuals (CPU) — or
   reuse the h20 run's saved basis if a snapshot exists.
2. Compare: (a) principal angles between the h1 joint span (16-dim) and the h20 joint
   span on the same prompt/pairs — report per-position cosines and the
   contained-energy fraction ||P_h20 h||^2 / ||h||^2 for the h1-selected donor
   directions v25; (b) whether the h1-selected TOKEN SET overlaps the h20-selected
   set under the production score (sc computed at both layers from the same bank).
3. Semantic readout: for the overlapping vs h20-only directions, the normalized
   readout at the animal tokens (Spider/Dog/4/8) — do the h20-only directions carry
   the animal identity that h1 misses?

Existing formulas only: increment_scores + subspace_from_scores + joint_support; no
new score, no dose/site grid. One bounded batch IF reviewed. -- PI[glm-5p3-flash]

## Config-equation diff: historical h20 success vs current h1 failure (2026-09-13, CPU audit of saved artifacts)

One legs-dog pair; every line from the saved run configs / records (paths in-file):

| dimension | HISTORICAL success (out/2026-09-10_replay-C1.5-legs-dog, 65 tok coherent+EOS) | CURRENT failure (out/2026-09-13_...-125352/dog-k8_C1.5, 128 tok degenerate) |
|---|---|---|
| edit layer | h20 (intervention_layer [20]) | h1 ([1]) |
| donor anchor | layer 20 = edit layer (depth-matched) | layer 25 ≠ edit layer (mismatch 25→1) |
| detector | snapshot 18/20/32 (three-depth scores) | increment (windowed, vocab-centered, min(build,cut)) |
| removal span | source top-8 (8-dim) | joint support 16 (8+8) |
| injection | C(Δ − U Uᵀh), norm matching recorded-but-unused in BOTH | same formula |
| prompt wording | "the animal that spins webs have?" / "...barks and is called man's best friend have?" | "the animal known for spinning webs to catch insects have?" / "...known for barking while living as a domesticated pet have?" |
| token windows / decode policy / C | 3 positions, continue_generation TRUE (decode editing ON), C1.5 | same |

Relative magnitudes (from the saved intervention records): prefill edit/residual =
0.68-0.94 (h20: 22.0/26.6) vs 1.84-2.02 (h1: 7.42/3.91); decode edits ≈11-12.7/step
(h20) vs 4.16/step (h1). Decode editing was ON and coherent in the historical run —
decode editing per se is not the poison.

**Bridge hypothesis (one)**: the current recipe injects a depth-MISMATCHED donor
vector (anchor 25) into the layer-1 stream at ~2× its norm (and ~1.1× per decode
step), i.e. an out-of-scale, out-of-geometry patch repeated every step; the
historical recipe injected a depth-matched vector in-scale at h20. The policy
discriminator showed the same prefill edit without decode re-injection stays
coherent — the compounding factor is the repeated out-of-scale decode patch.

**Lowest-cost SINGLE confound control (proposal, no GPU queued)**: one row, current
recipe otherwise identical, donor anchor moved to the edit layer
(xdepth_anchor_layer 25→1, depth-matched). If degeneration persists (r2 ~0.98, no
EOS), depth mismatch is exonerated; if coherence returns, it is named as the
confound. Alternative (second choice): move the edit layer to 20 with anchor 20
(matched but changes site). -- PI[glm-5p3-flash]

## CORRECTION to the config-equation diff (2026-09-13): the historical column was wrong

Traced the ACTUAL historical producing branch: the 2026-09-10 replay's demo.py hash
(219bacf5…) = commit c3d0298; its `span_correction_sweep_configs` (c3d0298
scripts/oat_sweep.py lines 232-247) shows the successful recipe is NOT
"source-top8 + Pd donor-state":

- basis/projector: TEMPLATE-CONTRAST + template-state ATTENUATION span
  (template_contrast=True, template_state_span="attenuation", persistent_rank=4) — a
  projected template contrast with a persistent rank-4 template retention, detector
  layers 18/20/32
- injection: match_component_norm=True and ACTIVE in that branch (upstream norm
  matching) — my "identical C(Δ−UUᵀh), norm matching unused in both" line is RETRACTED
- the rest of the diff stands (edit layer 20 vs 1; donor anchor = edit layer vs 25;
  prompt wording; 3 positions; C1.5; decode editing ON; continue_generation)

Consequence: the historical success vs current failure differ in the DETECTOR+BASIS
FAMILY (template-contrast/attenuation vs increment/top8-joint), the NORM MATCHING
(active vs off), the edit layer, the donor anchor, AND the prompt wording — a recipe
diff, not a single-knob diff; my earlier "relative magnitude" comparison alone cannot
bridge them. The depth-matched anchor control remains a valid single descriptive
control within the CURRENT recipe. "Fixed selection basis should not become 'h1 vs h20
token sets' solely by moving edit layer" — accepted; withdrawn.
-- PI[glm-5p3-flash]

## BRIDGE MATRIX RESULT (2026-09-13, pueue 1344, 8 rows + 4 C0 + unhooked) — CORRECTED after the supervisor's full-text read

GATES: both historical replays (dog/ant) reproduce the 2026-09-10 continuations
BYTE-EXACTLY through current code.

Artifact-derived per-row facts (all 8 nonzero + 4 C0 read; canonical r2; NONE capped
at 128 — every row emitted EOS, so there is NO runaway repetition anywhere):

> dog-att-h20: init 4, identity dog, coherent (the historical success; "short
>   history" weakness) | r2 0.016
> dog-att-h8: init 8, IDENTITY DOG ("The animal described is a dog, specifically a
>   male who is likely to be the owner's best friend. Dogs have historically been the
>   most popular choice in the United States." — dubious claim; short EOS) — the
>   identity changed but the ANSWER STAYED 8: the exact user failure mode
>   (answer-source/name-target mismatch) | r2 0.000
> ant-att-h8: init 8, identity SPIDER with FALSE biology ("Spiders are small,
>   hardworking insects... organized groups... colonies" — arachnids, not social
>   insects): ant properties leaked WITHOUT the name change | r2 0.000
> increment rows (all four): init 8, identity spider, coherent; dog-inc-h8 short with
>   "some species may have more or fewer legs" (dubious); dog-inc-h20 mentions
>   "insects" (the web-building prey, not an identity error) | r2 0.000-0.111
> C0 rows: all init 8, spider, clean | r2 0.000

RETRACTED by the supervisor's read (I misread the matrix): "dog-att-h8 transfers
4/dog" (it answers 8 with dog identity — NOT a transfer); "all coherent/no
degeneration" (at most: NO RUNAWAY REPETITION — semantic coherence is not established
given the false-biology rows); "norm matching + small rank keep it sane" (causality
untested); "rank confound" (both selectors are rank 4 — no rank difference exists).

CORRECTED READING: h8 changes identity/properties WITHOUT a consistent transferred
answer; there is NO early complete legs transfer in this matrix. The h20 rows (both
donors) transfer correctly — the historical success is real and site-dependent.
-- PI[glm-5p3-flash]
