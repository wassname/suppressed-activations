# job2721 result review

**PI/OpenAI — same-family review, not independent replication or sign-off.**

Read root `AGENTS.md`, goals/User voice, ml-debug skill, proposal/preflight, pipeline, all 474 console lines including 144 lists/six continuations, and archived direction/readout/scoring code.

**Conclusion:** This candidate does not demonstrate improved hidden-concept separation. It preserves useful identities on some inputs, but loses autumn at final and Thursday at boundary; the shared-seed random control preserves both old identities. This is evidence about this configuration—not a rejection of native geometry generally or a new baseline-dominance requirement.

## Observed comparisons

Below, “joint” means the grouped report’s alias-checked lexical score, **not verified semantic exclusion**. English denominator is four.

| Head | Final identities / joint | Boundary identities / joint | Preclue identities / joint |
|---|---:|---:|---:|
| Old half-J | 3/4 / 2/4 | 3/4 / 3/4 | 0/4 / 0/4 |
| Native-metric J | 2/4 / 2/4 | 2/4 / 2/4 | 0/4 / 0/4 |
| Matched random J | 3/4 / 2/4 | 3/4 / 3/4 | 0/4 / 0/4 |
| Old or candidate plain24 | 0/4 / 0/4 | 0/4 / 0/4 | 0/4 / 0/4 |
| Old or candidate plain27 | 2/4 / 2/4 | 3/4 / 3/4 | 0/4 / 0/4 |

Identity counts are my full-list reading, not additional scoring gates.

Evidence: `out/2026-10-01_170327_native-metric-readout/console-clean.log`, Cases 0–3:
- Old final autumn contains `" autumn"`, `"冬季"`, `"冬天"`; candidate loses autumn but retains `"寒冬"` (severe winter). Thus unchanged joint totals conceal an identity loss, not successful semantic cleanup.
- Old boundary Thursday contains `" Thursday"`; candidate instead ends with `"下一页", " lendemain"` and contains no Thursday identity. Random retains `" Thursday"`.
- Boundary apple remains `" apple"` at zero-based rank 6 for old/candidate/random J; plain27 starts `" apple"`. This is real boundary retrieval, not a candidate gain.
- Final apple still contains `"红色"` and `":red"` and no apple identity.

All six exact continuations are `January<|im_end|>`, `Tuesday<|im_end|>`, `winter<|im_end|>`, `red<|im_end|>`, `nuage<|im_end|>`, `Wolke<|im_end|>`. **Tuesday is the actual Thursday-prompt output; Friday is not a speech leak merely because it was expected.**

For translation, all compared heads identify cloud at final on both reciprocal prompts; joint remains **1/2**, with unscoreable `nuage` retained. At boundary they identify cloud on German→French but not French→German; joint is **0/2**. Preclue identifies neither. These are two prompts for **one concept**, not independent concept replications. English cloud translating the spoken foreign word is the intended translation-role target, not automatically a semantic failure.

## Top misconceptions and implementation assessment

1. **Lexical exclusion is narrower than the stated goal.** Boundary apple still returns `" poisonous"`, `" poisoning"`, `"毒药"` despite input “poisoned”; candidate December includes `"月份"` (months), and Thursday includes `"next"`/`"紧接着"` despite “immediately after.” These are concrete input-semantic overlaps, not proof that masks failed. At final, red/winter equivalents remain. No exhaustive multilingual-purity rate follows; I impose none.

2. **Higher AUROC is not stronger identity recovery.** Console preclue candidate plain24 reports **0.956 AUROC with 0/6 joint**. Archived `source.py:1579–1586` compares already-masked scores. Masked answer scores can make poor hidden rankings look favorable. Check unmasked ranks and same-mask nulls to distinguish this mechanism; AUROC alone cannot.

3. **Requested half-erasure is not exact realized half-erasure.** `source.py:689–732` implements the proposed held-scale `GJJᵀGw` direction, shared CPU seed0 Gaussian, and BF16 head without renormalization. No executed-path defect is established. However, `out/2026-10-01_170329_jlens-one-pass/native_metric_readouts/002.json` gives autumn-preclue before **0.137238**, requested **0.068619**, applied **0.096587**. Candidate/random match requested norms, not BF16/native/score-space behavior. Native minimum norm is a linearized geometric property, not semantic distance.

Preclue uses full-input masks and final-output direction (`source.py:1425–1463`); its failures do not establish independent early causal absence.

## Verification and implications

Pipeline reports **15 forwards/tokens, 15.065 seconds, 8.124 GiB**. `metric_reproduction.json` reports **180 exact old rows**, exact final states/generations, and explicitly calls earlier states a fresh capture. `verification.log` checks **144 selected rows/252 total**, masks/positions/coverage, maximum AUROC discrepancy **6.74e−8**, explicitly **“not neural replay or independent head reconstruction.”** I ran no processes.

Remaining checks: reconstruct directions/casts/head scores independently from pinned weights and saved states; disprove the reported losses by checking complete selected IDs, not aggregate totals. Semantic annotation remains non-exhaustive; one random seed gives no seed-distribution estimate.

**Goal 1 remains open:** useful location-dependent identity retrieval survives, but this change adds no demonstrated separation/generalisation gain on these development prompts. **Goal 2 remains open:** this is readout-only, with no intervention or coherent-transfer evidence. No new acceptance gates or automatic parameter rescue follow.