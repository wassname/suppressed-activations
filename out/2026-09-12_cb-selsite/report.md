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
