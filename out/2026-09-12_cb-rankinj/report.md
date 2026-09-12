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

## Mechanical counts (from all48_adjudication.json; per-condition denominators = 12)

| k | initial answer donor-direction ↑ | explicit final answer-flip | spider mentioned | loops (r2>0.5) | token-ID = base | token-ID = k8 |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 0 | 12 | 0 | 0/12 | — |
| 2 | 2 | 1 | 12 | 0 | 0/12 | 0/12 |
| 4 | 2 | 0 | 12 | 1 | 0/12 | 0/12 |
| 8 | 2 | 0 | 12 | 1 | 0/12 | 0/12 (k8 vs ITSELF: 12/12, trivially) |

The paired k8-vs-k8 comparison is 12/12 by definition — the "0/12 identical to k8" claim
applied to k8 itself was an error; the nontrivial comparisons: k1/k2/k4 vs k8 = 0/12 each.

The 2 initial-donor-direction rows per k = the SPINNERET conditions: the initial answer is
the donor-correct "No" at EVERY rank, followed by spider reversion + FALSE factual claims.

## Representative contradictions (exact quotes, substring-verified in all48_adjudication.json)

1. k1 spinneret-dog: initial `1. No.` (donor-correct) → `"Spiders do not possess
   spinnerets; instead, they have specialized silk glands"` — spider identity + FALSE
   fact (spiders DO have spinnerets).
2. k2 spinneret-ant: initial `1. No.` → `"**Corrected Answer:** Yes, spiders have
   spinnerets."` — an explicit answer flip WITHIN one continuation (No → Yes).
3. k8 = 1194's imported arm EXACTLY (12/12 steered-hash + 12/12 text equal) — including its
   known self-contradictions; the k8 replay reproduces the documented problematic outputs.

## Corrected claims (scope)

- FALSE (withdrawn): "NO donor answer", "small token drift", "none on-target",
  "off-target minimal" — every k's spinneret rows give the donor-direction answer initially;
  on-target answer movement exists and then reverts/contradicts.
- SUPPORTED (narrower): lack of COHERENT DONOR TRANSFER — the donor-direction answer
  never persists with donor identity + correct facts in any k at this setting.
- k8 replay vs 1194: 12/12 hashes + 12/12 texts identical (the known contradiction pattern
  reproduces exactly — no recurrence surprise).
## Standing (tested settings)

The template-label δ_ref′ injection remains the only construction with coherent-transfer
outcomes (A/B: 6/12, 3/12 dev); the donor-projection family (Pd d, any site h8/h20, any
depth h8/h20/h25 anchor, any rank 1–8, any selector) produced 1/12 at its best tested
setting. Historical 6/12 untouched. No further runs queued.
