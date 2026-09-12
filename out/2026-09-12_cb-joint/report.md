# Same-injection comparison: original vs joint-span removal vs restricted (task 1138)

2026-09-12, PI[claude]. Run: pueue 1138, `slop/common_basis_joint_batch.json`, one model
load, 684 s; protocol saved before execution (`slop/joint_removal_protocol.md`). Interval
h25..h30 (six sites per call, blocks 24..29), C=1.5, frozen donor, bank selector (23/25/32)
asserted per cell, top8 temporal bases then joint support. Same injection vector v = Pd d
in all C=1.5 conditions; only the removal span / injection projection differ. 48 cells.
Raw: `out/2026-09-12_cb-joint/{condition}-{cell}/result.json`.

## Results (swap means over 12; splits 4 cells)

| condition | removal | injection | swap ↑ | naming ↑ | capped | r2 range |
|---|---|---|---:|---:|---:|---:|
| original (replay) | Ps (rank 8) | Pd d | +4.14 | +10.69 | 12/12 | 0.84–0.99 (loops) |
| **joint removal** | **P_union (rank 16)** | **Pd d (same)** | **+1.86** | +5.52 | **1/12** | **0.00–0.10** |
| restricted injection | Ps | Ps(Pd d) | +0.09 | +0.48 | 1/12 | 0.00–0.48 |
| joint C0 | P_union | — | 0.00 exact identity | | 0/12 | |

## Semantic adjudication (full continuations read)

- **Original**: replicates 1136's degeneration — all 12 continuations are repetition loops
  (`ogs ogs…`, `vaya vaya…`).
- **Joint removal**: LOOPS GONE (r2 0.00–0.10, 1/12 capped vs 12/12). Continuations are
  coherent — but SPIDER: name-N1-dog pure spider (swap +10.05 never entered the text);
  name-N2-dog transient `狗 (Dog)` flip then self-correction (`**Corrected Answer:**
  Spider`); ant/property spider-bound (one property cell has a "Wait, I misunderstood…
  Let me re-read" reset, still spider).
- **Restricted injection**: ≈ nothing (+0.09; the donor signal was largely in the discarded
  outside-Ps part — consistent with the 80%/70% outside measurements).

## Verdict (registered prediction, both branches)

1. **"Joint removes the toy accumulation; if transformer loops also drop it supports
   utility"** — REALIZED: removing the accumulation stopped the degeneration (12/12 loops →
   1/12; r2 0.84–0.99 → 0.00–0.10). The accumulation mechanism behind the interval loops is
   now supported by an INTERVENTION, not just algebra.
2. **"Only coherent donor identities improve the goal"** — NOT met: joint removal is
   behaviorally STABLE but shows no persistent donor identity (one transient flip, same as
   single-site arms). **Stability improvement distinguished from transfer** — the loops
   were an artifact of the operator's accumulation, and removing them recovers the
   single-site behavior (clean spider + transient flips), not transfer.

Confounds explicit (per protocol): joint removes ~16 dims vs 8; restricted injects ~36% of
the injection energy — the pair brackets the mechanism but is not a pure accumulation test.

## Standing summary (tested settings)

Across all tested constructions/sites/selectors/policies: transient first-token effects or
degeneration; never persistent coherent donor identity. The joint-removal operator is the
first interval-capable variant (stable under continuous application, toy-verified fixed
point, loop-free in the transformer) — a stability prerequisite for any future transfer
work, not itself a transfer mechanism. Open: H9 (magnitude-matched randoms), the
tuned-lens/half-life framing, per-decode donor variants beyond the tested policy.
