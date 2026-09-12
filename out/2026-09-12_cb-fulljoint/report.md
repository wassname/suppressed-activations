# Full-temporal vs top8 joint removal (task 1142, 48 cells)

2026-09-12, PI[claude]. Run: pueue 1142 (requeue of 1140 after the containment-threshold
fix; failed-cell numerics + preserved partials in
`out/2026-09-12_cb-fulljoint-failed1140/`), one model load, 1463 s; protocol
`slop/fulljoint_protocol.md`. Interval h25..h30, C=1.5, frozen donor, selector (23,25,32)
asserted per cell, SAME injection v = Pd d in both C1.5 arms; ONE axis: temporal truncation
(top8 vs full support of U_s/U_d before the joint removal span). Raw:
`out/2026-09-12_cb-fulljoint/{condition}-{cell}/result.json`.

## Results (swap means over 12; splits 4 cells)

| condition | joint removal rank | swap ↑ | legs | naming | property | capped | looping |
|---|---|---:|---:|---:|---:|---:|---:|
| fulljoint C1.5 | 33–64 (per cell) | +1.66 | +1.00 | +5.91 | +0.77 | 3/12 | 0/12 |
| top8joint C1.5 (replay) | 16 | +1.86 | −0.16 | +5.52 | +0.20 | 1/12 | 0/12 |
| fulljoint random (descriptive) | per cell | +0.76 | +1.19 | +1.09 | −0.00 | 1/12 | 0/12 |
| fulljoint C0 | — | 0.00 exact identity | | | | 0/12 | |

No repetition loops anywhere (loop vs length-cap recorded separately; the 3 capped fulljoint
cells are long-coherent, r2 ≤ 0.13). Removal ranks: full-joint 33–64 (per-cell support),
top8-joint 16.

## Semantic adjudication (full continuations read)

- Naming: fulljoint and top8joint are behaviorally THE SAME — name-N1-dog pure spider
  (swap +10.80/+10.05 never entered the text); name-N2-dog transient `狗 (Dog)` flip then
  `**Corrected Answer:** Spider`; ant cells spider.
- Legs: top8joint clean spider/8; fulljoint legs-L1-dog emits `4` then self-corrects
  (`The spider is … eight legs, not four, so the answer…`) — a transient digit flip with
  spider identity retained, still a semantic FAIL by the rubric.
- Property: no coherent donor behavior in either.

## Verdict (registered prediction)

At matched operator/injection/site, TEMPORAL TRUNCATION DOES NOT CHANGE THE SEMANTIC
OUTCOME: full support (which retains the ~70% of donor-injection energy the top8 discards —
descriptive capture ~30%) does NOT improve persistent identity, does not loop, and leaves
spider unchanged apart from one transient legs-digit flip. The user's full-union-vs-top8
question is answered at this operating point: the truncation was not the binding
constraint for transfer. Rank/removal-rank/donor-content/norm co-varied (declared confound):
removal rank 33–64 vs 16; the random full-joint control (+0.76, naming +1.09) is slightly
above earlier site-randoms — descriptive only, not norm-matched, and still far below the
semantic arms. Prior full-union tests used a DIFFERENT removal operator (Ps-only) — labeled;
this comparison is operator-matched.

## Standing summary (all tested settings)

No tested construction achieves persistent coherent donor-identity transfer: transient
first-token effects (single-site/interval, both temporal truncations), degeneration at
unmatched cumulative dose (original interval operator), stability without transfer (joint
removal, both temporal supports). The recovered reference (different equation, audited 6/12
fresh) remains the best measured intervention. Bet table: H10 supported-with-confound;
temporal-truncation arm now closed at this operating point.
