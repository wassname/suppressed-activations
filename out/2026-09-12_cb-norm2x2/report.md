# Norm-vs-direction factorial at fixed L20/P_ref (task 1152, 60 cells)

2026-09-12, PI[claude]. Run: pueue 1152, `slop/common_basis_norm2x2_batch.json`, one model
load, 571 s; protocol `slop/norm_factorial_protocol.md`. Fixed: L20 single site, P_ref
removal (rank 4), C=1.5, frozen donor, last-3 + all-decode, 12 dev questions. Varied:
injection direction {δ_ref′, v} × injection norm {own, cross-rescaled per-position}.
Rescaling asserted per position (direction cos = 1.0 exact, target norm exact; saved per
cell). Raw: `out/2026-09-12_cb-norm2x2/{condition}-{cell}/result.json`.

## Factorial (swap means over 12; splits 4 cells)

| direction \ norm | ‖v‖ ≈ 1.9/1.8 (low) | ‖δ_ref′‖ ≈ 6.8/5.7 (high) |
|---|---:|---:|
| **δ_ref′ direction** | +1.01 | **+10.01** (A replay) |
| **v direction** | +0.43 (C replay) | **+3.54** |

Norm-target checks: max rel err 0.0, min cos 1.0 (both scaled arms). C0 exact identity.

## Semantic adjudication (full continuations read)

- δ_ref′ at v-norm: clean spider everywhere (name/legs/prop; r2 ≤ 0.01) — NO transfer;
  the +1.01 swap never entered behavior.
- v at δ-norm: DEGRADED or partial — name-N1-dog `蜘蛛 (Spider)…The spider is an arachin
  that lives in the water. It fetches the water…` (incoherent, early EOS 37t); legs-L1-dog
  `6.` (wrong digit) + `arthrop虫` (broken token); ONE partial identity bleed: name-N2-dog
  `1. A dog is a loyal and intelligent animal…` (the description moved to dog) — not a
  coherent answer to the naming question.

## Verdict (registered prediction: branch (c) with a direction-quality residual)

Direction and magnitude are JOINTLY needed, and the δ direction is additionally special:
- (a) δ direction at low norm: no transfer — direction alone insufficient at ‖v‖.
- (b) v at high norm: no COHERENT transfer (degradation + one partial identity bleed) —
  magnitude alone with the v direction produces instability, not transfer.
- (c) only high-norm δ_ref′ transfers coherently — direction × sufficient magnitude joint
  requirement; AND at matched high norm, δ_ref′ (+10.01) still exceeds v (+3.54, mostly
  degenerate) ~2.8× — a direction-quality advantage that magnitude alone does not explain.
Caveats: equalized injection magnitude at matched site/position only — total edits still
depend on direction+source state; per-position rescale; single site/selector.

## 1149 B per-row adjudications (pending item; saved `B_per_row_verdicts.json`)

B (δ_ref′ + Ps removal): **3/12 FULL PASS** — legs-L2-dog (digit 4 CORRECT + coherent dog
identity — a pass, not collapsible), name-N1-dog, name-N2-dog. legs-L1/L2-ant: digit wrong
(3, not 6) but ANT IDENTITY moves coherently ("The red ant…", "the ant… lives in
colonies") — identity-without-digit. name-N1-ant: honey bee (wrong insect). A: 6/12
(legs digits 4/4 + naming-dog 2/2; ant-naming loops). The removal span interacts with
WHICH content survives: A (P_ref removal) transfers digits; B (Ps removal) transfers
naming/leg identity without digits — hypothesis-grade, one comparison.

## Standing

The template-label direction at sufficient norm through the reference removal span remains
the only coherent-transfer construction (audited 6/12 on the fresh set). Magnitude and
direction are jointly necessary; neither alone suffices at this operating point.
