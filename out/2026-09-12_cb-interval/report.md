# Interval-wise re-correction results (task 1136, 60 cells)

2026-09-12, PI[claude]. Run: pueue 1136, `slop/common_basis_interval_batch.json`, one model
load, 587 s; protocol saved before execution (`slop/interval_protocol.md`). Interval condition:
common_replace at EVERY residual boundary h25..h30 (six sites per call, blocks 24..29),
fixed shared top8 projectors (bank selector 23/25/32), per-layer donor residuals, frozen
decode policy, C1.5. Raw: `out/2026-09-12_cb-interval/{arm}-{cell}/result.json`.

## Aggregate (swap means over 12; splits 4 cells)

| condition | swap ↑ | legs | naming | property | capped | r2 |
|---|---:|---:|---:|---:|---:|---:|
| interval h25..h30 | +4.14 | +1.28 | +10.69 | +0.45 | **12/12** | ~0.99 |
| L25-only (replay) | +2.22 | +0.25 | +6.23 | +0.18 | 2/12 | |
| L30-only (replay) | +1.63 | +0.06 | +4.67 | +0.16 | 0/12 | |
| C0 interval | 0.00 exact identity | | | | 0/12 | |
| random interval | −0.10 | −0.09 | −0.16 | −0.03 | 0/12 | |

Endpoint replays reproduce 1130 (L25 +2.22, L30 +1.63) — regression check passed.

## Semantic adjudication (full continuations read; quotes in raw files)

The interval arm is DEGENERATE: all 12 continuations are single-token repetition loops
(r2 ≈ 0.99, every cell capped at 128), several with donor-flavored loop tokens:
name-N1-dog `chien chien chien…` (swap +19.3), name-N2-dog `狗粮狗粮…` (dog food; +23.1),
legs-L1-dog `ogs ogs ogs…` (+5.9), name-N1-ant `regal regal…`, legs-L1-ant
`8 | vaya vaya…`. Property: `**False** (False, because spiders have **falseFalseFalse…`.
NO coherent donor answer, NO donor identity, NO transfer — the loop tokens are lexical
debris, not semantic carry.

Per-layer per-call edit norms (interval, one cell): total applied 594/476/426/516/546/613
across L25..L30 — cumulative ≈ 3170, ~4.2× the single-site total (~759). The random
interval condition (same six-site structure, random projectors) does NOT degenerate (−0.10, 0 caps),
so the specific bases' cumulative edit is what breaks generation — but with cumulative
intervention ~4× larger, this is NOT a pure timing effect and cannot show whether
maintaining through the interval would help at matched total edit.

## Verdict (registered prediction: "unchanged source or degradation ⇒ interval/procedure
insufficient")

**DEGRADATION — the interval/procedure is insufficient at this operating point.** The
prediction's failure branch is realized: no improved persistent identity; all continuations
degenerate. Cumulative dose and site count are confounded by design (declared in the
protocol), so this does not test matched-dose interval maintenance, and it says nothing
about other adaptive policies. The standing summary is unchanged: NO tested construction
(single-site L3/L20/L25/L30/L32, both selectors, sync donor, interval) achieves persistent
coherent identity transfer; the recovered reference (different equation, audited 6/12 on
the fresh set) remains the best measured intervention.

## Scope notes carried forward

Random intervals are descriptive, not dose-matched; smaller/larger projected norms are not
total-edit or semantic-strength claims; ρ/ρ_P are residual-based. Open: H8 (anomaly
framing), H9 (magnitude-matched randoms), matched-dose interval, other adaptive policies.
