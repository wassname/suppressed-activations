# Independent donor/readout review — PI/OpenAI

**Verdict:** The donor experiment supports same-pass causal answer steering on one selected input, not coherent concept replacement. Readout results support limited lexical recovery, not demonstrated hidden computation. Output erasure is an unrun method change.

Paths below are relative to `/workspace/2026/suppressed-activations/`.

## 1. Readout “passes” still contain the spoken answer’s meaning

**Observed:** `out/2026-09-30_110305_jlens-one-pass/run.md:603–605` reports alias-checked recovery **10/16 J**, **6/16 plain27**, **1/16 plain24**; corresponding AUROCs are **0.833, 0.842, 0.804**. J therefore does not outperform plain27 on both metrics.

The Germany J readout contains `"柏林"` after generating Berlin (`run.md:183`); Austria, Thailand and cat have analogous leaks. `data/english_v2_answer_alias_audit.json:4` correctly calls its additions **“Posthoc annotations of four definite translated-answer leaks”**, not a held-out result.

The audit is asymmetric and incomplete: plain27’s Greece readout contains `"雅典"` (Athens; `run.md:225`), absent from the audit. Horse also merits inspection: output is “a colt,” while readouts contain young-horse terms; matching only foal/foals misses a valid answer synonym.

**Impact:** Neither 10/16 nor an adjusted count is verified semantic thought/speech separation. English bridge-concept exclusion and translation-language role separation are different criteria.

**Cheapest test:** Rescore saved top32 lists, without inference, using a blinded semantic audit applied equally to every method and actual answer. Preserve original scores and mark corrections posthoc. This could disprove particular leak judgments or alter the apparent method advantage.

## 2. Full-donor success lacks its matched-magnitude random control

**Observed:** `out/2026-09-30_105749_jlens-one-pass/interventions.json:737,1362,1987,2612` records prefill relative perturbations:

- J projection: **0.3164**
- Full donor: **0.6508**
- Norm-matched full donor: **0.3164**
- Random: **0.3164**

The full donor changes the first answer to **8**, with **p8=0.9202**; baseline is **4**, **p8=0.00720**. J projection instead generates **6**, **p6=0.7266**, despite a favorable **−5.25** swap-log-odds shift (`run.md:33–39`, J condition). Its answer-pair mass is only **0.2414**.

**Inference:** Full-donor success cannot establish superiority to equally strong random perturbation. Projection improves 8-versus-4 odds partly by suppressing 4 while promoting the wrong answer. A single random direction supplies no seed distribution.

Current `scripts/english/08_jlens_one_pass.py:460–464` adds equal-full-norm comparisons, but these are not results from this artifact.

**Cheapest useful causal test:** Full donor versus several full-norm random directions on the same input, then one independent property with the unchanged donor. Successful property transfer, absent in controls, would weaken the generic answer-bias explanation.

## 3. Donor preparation is admissible, but lexical transport is not identity replacement

`out/2026-09-30_105132_jlens-one-pass/donors.json:13–18` lists four generic templates ending in the explicit noun, including `"The animal is a {concept}"`. Current source extracts the **last token’s** residual and averages it (`08_jlens_one_pass.py:125–130`). Thus donor differences include explicit noun-token identity and contextual features; they are not isolated latent-animal components.

The projection formula, `"full_delta @ inverse_j.T @ vectors_j.T"` (`:454`), is the Euclidean projection onto the two selected J-derived vocabulary directions. I see no transpose error. It is not a general J-lens semantic subspace.

The measured full-donor continuation still says the barking animal has eight legs (`interventions.json:1254`). This demonstrates answer alteration with a spider-like observer readout, not consistent replacement of all animal properties.

**Timing assessment:** The intervention branch uses fixed offline deltas; its observer does not control editing (`:484–519`). Coverage records show one prefill plus 31 cached decode calls. “One pass” is defensible as **no preparatory current-input pass per condition**, not one forward call for the entire experiment. The readout benchmark separately calls `trajectory` and generation for scoring (`:275–278`); final-layer masking cannot guide the earlier edit.

## 4. Output erasure removes one logit direction, not the answer concept

Current source chooses `"direction = W[output_id].float()"`, projects the **normalised** lens activation off it, then unembeds (`:311–321`). This algebra zeros one token’s float32 dot product; it does not remove a semantic answer representation or guarantee suppression of translations. Correlated hidden-concept scores can also change.

For multi-token continuations such as **“ a calf”**, the greedy token can be an article; numeric responses can begin with whitespace. The implementation then erases that token, not calf or the digit. Its assertion occurs before the bfloat16 cast, so only the recorded post-cast score tests realised numerical erasure.

**Cheapest test:** On saved states, log selected token IDs, post-cast residual scores, hidden-label retention and all audited answer-alias ranks. Compare mask-only, erasure-only and erasure-plus-mask. If selected directions are formatting tokens, fix the experimental interpretation before another inference run.

## Evidence limits

Read all requested files, applicable instructions and ml-debug skill. No inference, network, edits or tests executed. Source revisions were supplied by the parent, not independently checked. Missing evidence includes historical-source diffs, multi-seed controls, independent-property success and measured erasure output. Labels remain supplied plausible intermediates; AUROC after masking can improve mechanically by setting negatives to −∞.