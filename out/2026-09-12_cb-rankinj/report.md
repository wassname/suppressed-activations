# Injection-rank results (task 1208, 60 cells)

2026-09-12, PI[glm-5p3-flash]. Run: pueue 1208, `slop/common_basis_rankinj_batch.json` (every expected-field assertion — strength/condition identity/rank/anchor/removal/selector — checked before model load; 120/120 input list-equality), one model load, 638 s.
Design: FIXED P_joint8 removal in every condition (fingerprint-identical across ranks);
ONLY the injection basis varies — v_k = Ud_k Ud_kᵀ d25 (k ∈ {1,2,4,8}), all contained; h8
site, donor anchor 25 frozen at decode offset-1, C=1.5, increment selector, last-3 + all
decode. Raw: `out/2026-09-12_cb-rankinj/{condition}-{cell}/result.json`.

## Results (swap means over 12; splits 4 cells)

| k | inj. energy vs k8 (CPU table) | swap ↑ | legs | naming | property | capped | loops |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.277 | −0.29 | −0.75 | −0.03 | −0.09 | 1/12 | 0/12 |
| 2 | 0.450 | −0.17 | −0.53 | +0.09 | −0.05 | 2/12 | 0/12 |
| 4 | 0.721 | +0.05 | −0.38 | +0.30 | +0.22 | 1/12 | 1/12 |
| 8 | 1.0 | +0.13 | −0.16 | +0.22 | +0.33 | 2/12 | 1/12 |
| C0 | — | 0.00 exact | | | | 0/12 | |

## Per-row changes vs own base and k8 (no automatic labels)

- NO condition produces any donor answer or donor identity: every continuation is
  spider-bound (name-N1-dog `蜘蛛 (Spider)…`, legs `8 … spider … eight legs` at every k).
- Token-ID identical to base: 0/12 for every k — each rank's edit changes the output
  slightly, but the changes are small token-level drift, not semantic movement.
- Token-ID identical to k8: 0/12 — the rank slice changes the outputs (k1 ≠ k8 behaviorally)
  without producing transfer at any rank.
- Off-target effects at low k: k1 legs-L1-ant swap −1.75 with clean spider prose (no
  incoherence: r2 ≤ 0.05 across all k).

## Verdict (observed, tested settings)

**No injection rank (1/2/4/8) of the donor-projected vector produces donor transfer at h8
with fixed removal** — the rank axis is exhausted at this operating point: the
donor-projection direction family (across ranks 1–8, norms ~0.4–0.9 of h8) does not carry
the transfer-relevant content. Small output changes exist everywhere (never identical to
base), none on-target. The registered Pareto question ("some k yields correct fact +
identity with fewer unwanted effects") — answer: none at h8 with this construction.

## Standing (tested settings)

The template-label δ_ref′ injection remains the only construction with coherent-transfer
outcomes (A/B: 6/12, 3/12 dev); the donor-projection family (Pd d, any site h8/h20, any
depth h8/h20/h25 anchor, any rank 1–8, any selector) produced 1/12 at its best tested
setting. Historical 6/12 untouched. No further runs queued.
