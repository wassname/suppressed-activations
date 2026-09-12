# Selector×site results (task 1182, 84 cells)

2026-09-12, PI[glm-5p3-flash]. Run: pueue 1182, `slop/common_basis_selsite_batch.json` (84
entries, all expected-field checks — strength/condition identity/selector — passed before model load), one model load, 766 s. Construction: ONE
accumulation-safe operator (joint removal, v contained asserted), the SELECTOR as the only
construction difference (snapshot 3-depth vs increment whole-window), sites h8 (early,
before the build window) / h20 (later reference), C=1.5, last-3 + all-decode, frozen donor.
Raw: `out/2026-09-12_cb-selsite/{condition}-{cell}/result.json`.

## Results (swap means over 12; splits 4 cells)

| condition | swap ↑ | legs | naming | property | capped | loops |
|---|---:|---:|---:|---:|---:|---:|
| snapshot-h8 | +0.00 | +0.09 | −0.12 | +0.03 | 0/12 | 0/12 |
| increment-h8 | +0.02 | +0.12 | −0.08 | +0.02 | 0/12 | 0/12 |
| snapshot-h20 | +0.26 | +0.41 | +0.32 | +0.06 | 2/12 | 0/12 |
| increment-h20 | +0.26 | +0.06 | +0.11 | +0.61 | 2/12 | 0/12 |
| random-h8 / random-h20 | −0.05 / +0.01 | | | | 0/12 | 0/12 |
| C0 | 0.00 exact | | | | 0/12 | |

## Semantic outcomes (full continuations read; per-row verdicts in the JSON to follow)

NO condition produces any donor answer or donor identity at either site: every naming/
legs/property continuation is clean spider (e.g. snapshot-h8 name-N1-dog `蜘蛛 (Spider)…
The spider is an arachnid…`; increment-h8 legs-L1-ant `8 … spider … eight legs`). The h8
arms are indistinguishable from C0.

## Registered predictions (resolved)

- **P1 (trajectory selection helps) — REJECTED at these sites**: no paired improvement;
  increment ≈ snapshot at both sites (swap and per-row outcomes), despite the Jaccard-0.02
  selection difference.
- **P2 (selection difference does not reach behavior here)** — REALIZED at h8/h20 with the
  joint operator: the increment selector's leg-topic selections do not reach behavior.
  Scoped: this does not imply the locus "must be elsewhere" — the increment selector may
  simply be inadequate at these sites.
- **P3 (early site)** — no support for useful early intervention: h8 arms show NO change at
  all (not even degradation). The donor state/norm site confound was recorded in the
  protocol (an h8 donor residual carries different content).

## Synthesis with the cycle's evidence

The v = Pd d injection is inert at every tested site/selector/removal (L20, L25, h8, h20;
~0 across all), while the template-label δ_ref′ injection transfers (A/B in the 2×2;
ablation: injection-only ≈ full). The selection-vs-site question is answered at these
settings: neither trajectory-based selection nor site choice reaches behavior for the
Pd-projected donor injection; the discriminating variable remains the injection direction.

## Status

All 84 cells' full texts saved; per-row verdicts to be added to
`out/2026-09-12_cb-selsite/per_row_verdicts.json`. No further runs queued; next direction
with the supervisor.

## Completed CPU audit (token-ID equality, actual edits, geometry; answers to the review)

**1. Exact equality vs each output's own base (token IDs)** — the h8 outputs are NOT
"indistinguishable from C0": continuations token-ID identical to base: snapshot-h8 1/12,
increment-h8 2/12, random-h8 2/12 — i.e. 10–11/12 DIFFER at h8; h20: 0/12 identical (all
12 differ). The earlier "no change at all" was wrong; the correct statement: many small
changes, no donor answers/identity. Factual imperfections persist in the "clean" texts
(increment-h8 legs-L2-ant: "eight limbs… arranged in two pairs of four"; liveyoung
generalizations) — each output differs from its own base and none is a clean control.

**2. Donor-answer correction**: ant liveyoung "No" IS the correct donor answer (appears in
several rows) — it is not evidence of transfer (fact-preserving control per plan); "no ANY
donor answer" was wrong as stated.

**3. Actual per-position edits and same-history ρ** (means; `edit_summary.json`):

| condition | prefill edit/residual | ρ (full) | ρ_P (in P) | donor-proj norm |
|---|---:|---:|---:|---:|
| snapshot-h8 | 0.067 | 0.020 | 0.002 | 0.28 |
| increment-h8 | 0.068 | 0.023 | 0.002 | 0.26 |
| snapshot-h20 | 0.105 | 0.051 | 0.010 | 1.14 |
| increment-h20 | 0.127 | 0.091 | 0.012 | 1.44 |

The h20 edits are ~1.6–1.9× larger with ~2.5–4.6× larger donor projections — the early
donor projection is SMALL (0.26–0.28 vs 1.1–1.4 at h20): the projected donor component at
h8 is tiny because the donor residual's h8 state has little of the (late-built) suppressed
content to project. Same-history ρ confirms the h8 edits barely reach h32 (ρ 0.02 vs 0.09).

**4. Geometry (actual, saved `geometry_audit.json`)**:
- Principal angles between snapshot-top8 and increment-top8 temporal unions: SOURCE mean
  0.158 / max 0.698; DONOR mean 0.195 / **max 0.998** — the two selectors' donor spans
  overlap SUBSTANTIALLY for some prompts (one pair near-identical) despite Jaccard-0.02
  token sets: token-set divergence ≠ span divergence.
- Donor-projection energy retained in top8 vs full union: **mean 0.407** (min 0.15,
  max 0.90) — the top8 keeps ~41% of the donor-projection energy (matching Astra's 41.5%
  full-union measure); half the donor activity was in the discarded ranks.

## Synthesis (scoped to these measurements)

Three candidate explanations for the h8/h20 null are now separated by measurement: (a) the
early donor projection is genuinely small (donor-proj norms 0.26–0.28 at h8); (b) top8
truncation discards ~59% of the donor-projection energy (0.407 retained); (c) token-set
changes between selectors do NOT proportionally change the spans (donor angle max 0.998).
The measured bottleneck for a subspace/rank test: **rank/truncation of the donor span**
(41% retained) interacting with site-dependent projection size.

## Next evidence-directed test (subspace/rank; NOT queued)

At h20 (where projections are non-trivial), same operator/policy/C: donor-span RANK
comparison — top8 vs FULL-support donor union (source span fixed top8), 2 conditions + C0 +
descriptive random = 36 cells... smallest version: 2 conditions × 12 + C0 = 36. Tests
whether the discarded 59% donor-projection energy carries transfer-relevant direction
under the accumulation-safe joint removal. Registered predictions: full-donor-rank improves
paired correct-facts+identity (P-yes) / identical spider outcomes (rank irrelevant) /
degradation (energy ≠ semantics).
