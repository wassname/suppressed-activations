# Generic normalized-state subtraction

— PI/OpenAI. New method, not missing reference-code restoration. Design: `slop/reviews/2026-10-01_after-animal-pairs-next-method.md`. Both research goals remain open; v5 remains reserved.

## Hypothesis and fixed method

Repeated generic/answer-category entries and persistent horse/cat preference could dominate a smaller useful identity signal. A single reusable generic reference may reduce that preference. Alternatives: no strong identity signal exists at this position; the model answersfour without a particular animal; subtraction removes useful shared content. Positive pairD alone is not successful hidden readout or necessary reasoning.

Reference user content is exactly `Complete the fact with only the missing word or phrase:\nFact:` (`data/generic_readout_reference_v1.json`). Standard native render, thinkingFalse. One offline generic prefill through08's existing `generate_readout(max_new_tokens=1)`, no cached decode. Discard its computed token. Save final-prefill residual24/27, exact input IDs/bytes, model/revision/config, coverage and hashes. No evaluation-case preparation.

For each current/reference representation, transportJ24 byFP32(h)@J.T; plain24/27 are unchanged. Apply actual model norm toBF16 state, then promote toFP32. Let z be current normalized decoder state and z0 the generic one. Letw be the unembedding row of the current case's original final-prefill greedy token. Candidate:

`head(BF16(v - 0.5 * (v @ w) / (w @ w) * w))`, where `v = z - z0`.

Preserve implementation operation order: form the full projected vector, then multiply by0.5. No second norm, no separately rounded logit subtraction. Same residual24 J, last-prefill position, k32, old input mask plus complete-input-prefix extension, original greedy-output mask1. Labels and generated text are evaluation-only. No new dose, layer, k, mask, reference-prompt search or per-case winner.

## Conditions and cases

Rescore all eight native-v4 cases from `out/2026-10-01_102219_jlens-one-pass` and all four animals from `out/2026-10-01_110004_jlens-one-pass`. References for unchanged old rows are102255 and110021 `_jlens-one-pass`. Same pinned model/tokenizer/J. No new case generations. Reject all transformer forwards during cached scoring.

Three centered representations: halfJ24 (primary), halfplain24/27. For each, compare generic reference with one fixed seed0 isotropic FP32 decoder-space direction scaled separately to its generic-reference norm. Same random unit direction across all methods/cases; no per-case rescaling. Both undergo identical half-projection after subtraction. Preserve original mask-onlyJ and all old scores/outputs as controls, not additional winners.

Matching is BEFORE projection only. Log reference norms beforeprojection, afterprojection, afterBF16, and realizeddecoder-delta norm versus the old half-erased decoder state. Do not claim postprojection/score-space equality or orientation-only attribution.

## Evidence and decision

SHOULD:1genericprefill total,0cached transformer calls, all12 old outputs/trajectories unchanged; original176+88 rows exact plus6newmethods×12cases=72newrows. Expected gains are newly returned identities with exclusions, not only higher margins/AUROC. Report paired gains/losses and full-list semantic identities/input/actual-said/formatting evidence separately for/8 and/4. Horse remains in/4 althoughitnamesitself. Preserve wrong and capped native-v4 cases. Animal exact-word own/partner scores are secondarydiagnostics using the frozen whole-word ID sets from2694.

If generic subtraction improves actual returned identity/exclusion beyond controls, freeze it before choosing a new-example test. If onlynumbers orD improve, goal remains unmet. If random/plain matchgains, generic-prior explanation is not specifically supported. If identities disappear, shared-signal removal becomes moreplausible. No tuning rescue; no automaticv5 consumption or universalhumanpassgate.

Before queue: directprojection/zero-reference parity; fixedrandom prematch and postprojectiondisclosure; realtiny-Qwen genericprefill pluscached-rescore test; oldscores exact; preservedhooks/weights; alteredreference/provenance and extra-forward failures tested. Preserve first failures. No pretrained reference observed yet.
