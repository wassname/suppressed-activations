# Current-reference ablation: injection-only / removal-only (task 1158, 48 cells)

2026-09-12, PI[claude]. Run: pueue 1158 (retry of 1154; unique-attempt provenance: the
1154 partials were deleted by worker error — incident in the ARJ; supervisor's log
preservation: main `.local/verify_logs/pueue_1154_partial_deleted.log` SHA256 548fcb5b…),
one model load, 2617 s; protocol `slop/ablation_protocol.md`. L20 single site, C=1.5,
same 12 questions, the SAME applied δ_ref′/P_ref constructed once by the runtime sweep
code. Raw: `out/2026-09-12_cb-ablation/{condition}-{cell}/result.json`.

## Results (swap means over 12; splits 4 cells)

| condition | equation | swap ↑ | legs | naming | property | capped | loops |
|---|---|---|---:|---:|---:|---:|---:|
| injection-only | h + C·δ_ref′ | **+10.16** | +8.03 | +22.93 | −0.47 | 3/12 | 2/12 |
| removal-only | h − C·P_ref h | −0.19 | −0.38 | −0.14 | −0.05 | 0/12 | 0/12 |
| A replay (both) | h + C(δ_ref′ − P_ref h) | +10.29 | +6.73 | +24.60 | −0.47 | 3/12 | 1/12 |
| C0 | identity | 0.00 exact | | | | 0/12 | |

Applied-delta vector equality VERIFIED IN-RUN: `applied_delta_sha256` identical across
injection-only / removal-only / A (2 hashes = dog/ant concepts) — the same constructed
vector, per the protocol.

## Semantic outcomes (full continuations read; identity and predicate separate)

- injection-only retains A's successes: name-N1-dog `狗 (Dog)` + persistent dog identity
  (pass); legs-L1-ant `6` + `The red ant is a tiny, hardy insect…` — the DONOR DIGIT and
  ant IDENTITY together (pass-level); legs-L1-dog `2` + dog identity (identity moved,
  digit wrong — same partial as 1149's B arm); property spider-bound.
- removal-only: NOTHING — clean spider/8, correct predicates, no digit change, no identity
  change in any cell.

## Verdict (registered predictions)

- **"Injection-only retaining A's naming/legs successes supports sufficiency at these
  inputs"** — REALIZED: injection-only ≈ A (+10.16 vs +10.29); naming passes persist; the
  legs digit+identity case (legs-L1-ant `6` + red ant) appears in injection-only.
- **"Removal-only digit change without donor identity indicates answer bias"** — did NOT
  occur at this setting: removal-only did NOTHING (−0.19; clean spider everywhere). The
  historical job-500 pattern (removal-only carried the digit) does NOT transfer to this
  operator/era — motivational-only status confirmed by measurement.
- Net: **the injection term carries the entire effect at this operating point; the removal
  term is dispensable here** (C=1.5: removal-only writes h − 1.5·P_ref h — in-span
  coefficient −0.5 — with no behavioral consequence).

## Consistency with the earlier batches

Explains the 2×2: A ≈ B (both inject δ_ref′; removal span barely matters) and C ≈ D ≈ 0
(v injections do nothing). Explains the joint-removal stability result: δ_ref′ lives
inside its removal span (no accumulation), and the injection — not the removal — was doing
the work all along. The vector-map's orthogonality (cos(δ_ref′, v) ≈ 0.005) + this
sufficiency result together locate the active ingredient: the template-label direction,
injected at sufficient norm.

Scope: one site (L20), one C (1.5), 12 dev questions, alternate-wrapper diagnostics caveats
where bank-based; the runner-path causal batches are unaffected.
