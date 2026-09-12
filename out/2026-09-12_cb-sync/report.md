# Donor-state updating vs frozen donor (task 1134, 48 cells)

2026-09-12, PI[claude]. Run: pueue 1134, `slop/common_basis_sync_batch.json` (selector
assertion in-spec), one model load, 661 s. Protocol (saved before execution):
`slop/sync_donor_protocol.md`. Construction frozen: common_replace
h' = h + 1.5(P_d d − P_s h), bank selector (23/25/32), top8_union, L25 (block 24), window 4,
positions 3 + continuous decode. The ONLY change: the SYNC arm teacher-forces the donor on
exactly the source-selected tokens (separate caches, token-ID histories asserted equal per
step, no ground-truth answer fed) and at each decode projects the donor's CURRENT h25 with
the FIXED U_d8. Randoms referenced descriptively from 1130 L25 rows (identical config).

## Construction check (not outcome evidence)

Frozen-vs-sync steered first-step logits: bitwise hash match 12/12 (and base hashes 12/12);
first tokens equal. Expected by design (step-0 donor state = final prefill state); confirms
the two arms differ only in decode-time donor evolution.

## Aggregate table — READ WITH THE CONSTRUCTION CHECK IN MIND

| arm | swap ↑ | legs | naming | property | ρ | ρ_P | capped |
|---|---:|---:|---:|---:|---:|---:|---:|
| sync-C1.5 | +2.22 | +0.25 | +6.23 | +0.18 | 0.249 | 0.072 | 1/12 |
| frozen-C1.5 (replay) | +2.22 | +0.25 | +6.23 | +0.18 | 0.249 | 0.072 | 2/12 |
| C0-sync / C0-frozen | 0.00 exact identity (both execution paths) | | | | | | |

The swap/ρ columns are BITWISE-identical across arms BY CONSTRUCTION (they are computed from
the prefill/first-step logits, which the construction check guarantees equal). They are NOT
evidence of similarity; the arms differ in the continuations (per-call donor_proj norms
vary per decode in sync: 1.41/1.26/1.32… vs frozen constant 4.70). The frozen replay also
reproduces 1130's L25-top8 swap (+2.22) — regression check passed.

## Pair-level semantic outcomes (all 12 pairs read; the actual comparison)

| cell | frozen | sync | semantic outcome |
|---|---|---|---|
| legs-L1/L2-dog, legs-L1/L2-ant | spider/8 | spider/8 | no transfer in either arm (4 pairs) |
| name-N1-dog | 蜘蛛 (Spider) | 蜘蛛 (Spider) | no flip in either |
| name-N2-dog | 狗 flip → self-correct (121t) | 狗 flip → self-correct (96t) | BOTH revert; sync 25 tokens shorter, same outcome |
| name-N1/N2-ant | 蜘蛛 (Spider) | 蜘蛛 (Spider) | no transfer (2 pairs) |
| prop-P1-spinneret-dog | No + "spiders do not have spinnerets" (false), 128t | No + spider prose, 128t | donor-direction answer, spider identity, false claim — both arms |
| prop-P1-spinneret-ant | No (donor-direction), spider identity | Yes (source-bound) | donor-direction answer LOST in sync |
| prop-P2-liveyoung-dog | No, rambles to 128t | No, ends 75t | same answer; sync less rambling |
| prop-P2-liveyoung-ant | No (fact-preserving control) | No (control) | same |

**Self-correction incidence: unchanged.** The one reverting naming cell (name-N2-dog)
reverts in BOTH arms; no cell where sync preserves an induced identity that frozen loses.
One donor-direction property answer (spinneret-ant No) is LOST under sync. Scope notes
(supervisor): this does NOT exclude a stale donor as a contributor — a fixed P_d can misread
current states and multiple causes can co-occur; and the smaller per-decode ‖P_d d‖ (~1.3)
is the MEASURED PROJECTED NORM only — it is not proof of a smaller total edit
‖P_d d − P_s h‖ nor of less semantic donor representation. ρ/ρ_P are residual-based
diagnostics, not computed from logits.

## Verdict (per the registered prediction)

Both arms revert where reversion occurs → **frozen-state staleness does NOT explain the
self-corrections; per-decode current-state projection with fixed P_d is INSUFFICIENT as the
adaptive policy.** This does not rule out adaptive steering generally (per the protocol).
A mechanistic observation consistent with the failure: the teacher-forced donor's current
h25 carries a SMALLER projected donor component per decode (~1.3 norm) than the frozen
final-prefill state (4.70) — once conditioned on source-selected tokens (e.g. after `8` or
蜘蛛), the donor prompt's internal donor-answer representation shrinks, so the sync policy
injects a weaker edit, not a stronger or better-timed one.

Bet table: H7 (per-decode donor state resolves self-correction) REJECTED for this policy
scope; H8/H9 unchanged; interval-wise re-correction remains untested (different candidate).

Raw: `out/2026-09-12_cb-sync/{arm}-{cell}/result.json` (+ run.md, synchronized_history
token IDs per cell).
