# L25 common-basis OAT + L20 support-corrected replay (task 1073, 96 cells)

Written 2026-09-11 by PI[claude]. Run: pueue task 1073, `slop/common_basis_l25_batch.json`,
one model load, 889 s, model Qwen/Qwen3.5-4B rev 851bf6e8. 84 L25 cells (per_token /
full_union / top8_union at L25 with the SAME construction: detector 23/25/32 unchanged,
C=1.5, window 4, positions 3, continuous coverage, + random_shared8/shared32/perpos8 + C0)
and 12 L20 support-corrected full_union replay cells. The L20 recovered reference is
historical and distinct (not rerun, not moved). Randoms are rank-matched seeded Gaussian
projectors with real donor states — DESCRIPTIVE controls, NOT applied-norm matched.
Per-cell: `result.json` + `run.md` in this directory.

## Matched layer comparison (means over 12 cells; type splits are 4 cells each)

| condition (L25) | swap ↑ | p_tgt | total norm | legs ↑ | naming ↑ | property ↑ |
|---|---:|---:|---:|---:|---:|---:|
| per_token C1.5 | +1.95 | 0.013 | 533.0 | +0.03 | **+5.40** | +0.42 |
| full_union C1.5 (support-corrected) | +2.85 | 0.041 | 787.0 | +1.38 | **+6.30** | +0.86 |
| top8_union C1.5 | +2.22 | 0.015 | 635.5 | +0.25 | **+6.23** | +0.18 |
| random_shared8 | −0.01 | 0.006 | 184.2 | −0.09 | +0.10 | −0.05 |
| random_shared32 | +0.27 | 0.007 | 417.0 | −0.16 | +0.96 | +0.01 |
| random_perpos8 | +0.12 | 0.009 | 213.5 | +0.31 | +0.03 | +0.02 |
| C0 | 0.00 | 0.007 | 0.0 | 0.00 | 0.00 | 0.00 |

At L20 (task 1072) the same three constructions gave +0.20/+0.60/+0.25 with naming
+0.20/+1.36/+0.32. The movement is concentrated in naming-dog cells
(full_union name-N1-dog +11.36, name-N2-dog +13.91; per_token +9.73/+12.22;
top8 +11.42/+12.91). Naming-ant and property cells stay ≈ 0 at both layers.

## Component scale at L20 vs L25 (per_token, means over cells/offsets; norm fractions)

| layer | source state | source span | donor state | donor proj | proj/state |
|---|---:|---:|---:|---:|---:|
| L20 | 15.2 | 1.01 | 15.3 | 0.95 | 0.062 |
| L25 | 26.2 | 4.31 | 26.0 | 4.30 | 0.165 |

The suppressed subspaces hold ~2.7× more of the donor state at L25 and the applied edits are
~4× larger (total norm 533–787 vs 128–443 at L20), matching the trajectory-bank layer profile
(top8 fraction peaks at L25–28). Site and magnitude changed together in this OAT; they are
not separated by it.

## Observed continuations at L25 (complete excerpts, verbatim)

full_union name-N1-dog (91 tokens; swap +11.36):

```text
狗 (Dog)

Wait, that is incorrect. The animal known for spinning webs to catch insects is the **spider**.

The spider is a small, eight-legged arachnid that lives in various environments ...
```

per_token name-N2-dog (94 tokens; swap +12.22):

```text
狗 (Dog)

Wait, the description "spinning webs to catch insects" does not match a dog. The correct answer is a **spider**.

**Corrected Answer:** Spider
```

full_union legs-L1-dog (swap +3.75, p_tgt 0.263):

```text
6

The spider is an arachnid characterized by having eight legs, not six, so the correct answer to the question ...
```

full_union name-N1-ant (swap +0.16): `蜘蛛 (Spider)

The spider is an arachnid ...` — ant cells unmoved at both layers.

Pattern: at L25 the dog-naming cells flip the FIRST answer token to the donor answer
(`狗 (Dog)`), then the continuation self-corrects back to spider within a sentence.
Legs-dog moves intermediate mass (p_tgt up to 0.263) and can emit a wrong digit (`6`)
before self-correcting. Coherence is preserved overall (r2 means 0.06–0.11, 1–2/12 cells
capped at 128, EOS terminations elsewhere); this is transient answer-token movement, NOT a
persistent identity replacement.

## L20 support-corrected full_union replay (12 cells)

| cell | replay swap | support src/tgt | original (invalid) swap |
|---|---:|---|---:|
| legs-L1-ant | −0.12 | 31/31 | −0.62 |
| legs-L1-dog | +0.25 | 31/30 | +1.00 |
| legs-L2-ant | +0.12 | 32/31 | 0.00 |
| legs-L2-dog | +0.62 | 32/31 | +0.50 |
| name-N1-ant | +0.05 | 31/31 | −0.02 |
| name-N1-dog | +0.38 | 31/28 | +2.41 |
| name-N2-ant | +0.09 | 29/29 | +1.55 |
| name-N2-dog | +0.52 | 29/24 | +1.52 |
| prop-P1-spinneret-ant | +0.41 | 28/30 | +0.47 |
| prop-P1-spinneret-dog | +0.59 | 28/26 | +0.72 |
| prop-P2-liveyoung-ant | 0.00 | 25/26 | 0.00 |
| prop-P2-liveyoung-dog | +0.12 | 25/24 | −0.38 |

The replay confirms: L20 full_union does not move the answer with or without the arbitrary
null columns (all |swap| ≤ 0.62). The original name-N1-dog +2.41 collapsed to +0.38 — that
cell's movement was carried by the invalid null columns, not the union.

## What this comparison establishes (observations)

1. Site matters: the SAME construction, C, window, and coverage moves dog-naming answers at
   L25 (+5.4 to +6.3 mean swap, first-token flips) but not at L20 (≤ +1.4 naming mean).
2. The L25 movement is direction-specific relative to the descriptive randoms (−0.01 to
   +0.27 at L25), with the caveat that random projectors also capture less donor state
   (norms 184–417 vs 533–787) — reduced, not eliminated, magnitude confound.
3. The transfer is unstable: first-token flips followed by self-correction to spider; ant
   cells and property cells unmoved; legs-dog can emit a wrong intermediate digit.
4. Component scale rises ~4× at L25 (proj/state 0.165 vs 0.062), consistent with the bank
   table; site and magnitude co-vary and remain unseparated.

## Is per-call magnitude normalization still informative? (assessment, labelled)

Partially answered, not decided: at L25 the construction norms (533–787) are already
comparable to the L20 reference's total (778) and behavior moves — so magnitude alone is no
longer the obvious blocker. What the L25 failure mode shows is instability (self-correcting
continuations) and dog-only scope, which per-call norm matching at L20 would not address.
A norm-matched L20 run would still cleanly separate site from magnitude at fixed layer, but
the evidence now points more toward persistence/coverage or donor-state policy as the
binding constraint. Decision deferred to review.

## Provenance

- Spec: `slop/common_basis_l25_batch.json` (96 entries; common-basis-l25 indices 0–6,
  common-basis index 2 for the replay).
- Per-cell: `out/2026-09-11_cb-l25-batch/{cond}-{cell}/result.json` (+ `run.md`);
  replay cells `L20-fullunion-support-{cell}`.
- State/projection norms at L20 and L25: per-cell `persistence.state_norms_L20_L25`.
- Prior batch: `out/2026-09-11_cb-batch/` (task 1072) and its corrected `report.md`.
