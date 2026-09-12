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
