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

Sampled token complete trace (top production-increment token on the exact legs-dog
source bank, position 48 = the last edited position, token 243784 ' Конкурс'):
normalized readout oscillates ~13-31 across 33 layers; per-write increments show
build (+9.7, +12.5, +8.9 within the window) and cut (−15.1 at the last write);
unit-projected energy builds to ~1.99 then −2.135 at the final write — the
rise-then-cut signature the min() conjunction selects for. Full 33-point arrays
(normalized readout / increments / RMS / unit energy) saved in the .pt artifact.

Unresolved selector question, narrowed: whether min(build-window, last-3-cut) — the
current conjunction — is the right trade-off vs e.g. per-position full-window
build+cut with the same conjunction; the TV probe does not answer it. No GPU runs.
-- PI[glm-5p3-flash]
