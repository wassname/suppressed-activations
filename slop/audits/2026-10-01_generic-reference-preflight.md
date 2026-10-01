# Generic-reference preflight

— PI/OpenAI. No pretrained result yet. The frozen method and decision rule are in `2026-10-01_generic-reference-preregistration.md`.

Observation: animal run2694 returned 0/4 identities and 0/2 preference reversals with every method. Positive J-lens paired margins did not change that result. Native-v4 recovered some identities, but no reviewed fully clean lists. These observations motivate removing a fixed generic decoder-state component; they do not establish that this component caused the failures.

## Decision and predictions

Use one generic prefill, then score the12 saved cases without transformer calls. Retain unchanged methods, equally processed plain lenses and prematched random references. This is cheaper and more directly goal-directed than another score-only diagnostic. No training, optimizer, loss schedule or gradient updates occur.

- Generic-prior hypothesis: subtraction returns additional identities with input/actual-output exclusion, beyond unchanged/random controls.
- Weak or unused identity hypothesis: AUROC/margins can move without returned identities.
- Shared-signal hypothesis: previously recovered identities disappear.
- Random/plain matches would weaken a specific generic-prior explanation. Prematching norms does not match postprojection or score-space effects.

Subjective allocation over the main explanation for another poor result, not measured probabilities: implementation error5%, evaluation error5%, generic prior still dominates25%, weak/unused identity40%, useful shared signal removed15%, unknown10%. Existing tiny tests weigh against implementation errors but do not certify pretrained behavior. Full-list semantic review is still required because the lexical evaluator misses translations, fragments and formatting.

## Checks and evidence

- Static review: “One CLI blocker; two provenance/recovery gaps. No arithmetic defect found in the scoped scoring path.” All three findings were addressed. The parent's repair evidence is appended to `../reviews/2026-10-01_generic-reference-implementation-review.md`; this is not a second reviewer approval.
- Core smoke, seeds0/1,51s: “PASS real CLI options reach pre-model guards; incomplete preparation and altered same-revision provenance rejected; every norm field reconstructed”. Zero-reference parity,44 unchanged rows per seed,12 candidate rows, fixed prematched random and zero cached forwards also pass.
- Actual full launcher,87s: “PASS actual launcher/all12 fixed inputs: one generic prefill, three fresh tiny model loads,264 old rows exact+72 new, raw/masked score parity, unchanged outputs/states, zero case forwards,20 summary rows and12 animal pair records”. These are tiny random CPU results, not scientific retrieval evidence. Two earlier fixture failures remain archived.
- Frozen source/data/cache/helper hashes are in `2026-10-01_generic-reference-manifest.json`; its digest is checked by the launcher. Reference config, exact rendered input and IDs are saved before its attempted forward. Its computed token is discarded.
- SHOULD: one generic prefill, zero cached forwards, unchanged outputs/states and264 old rows, plus72 new rows. The real-run observations are pending.
- Full sample inputs/outputs are unchanged from2688/2694. The horse case explicitly says horse and stays in the denominator; Thursday and violin remain wrong. No interpretation of the tiny model's generated text is made.
- Empirical nulls are the unchanged masked readouts, plain lenses and seed0 random reference, not a uniform-vocabulary chance calculation. Semantic paired gains/losses are primary; pairD and AUROC are secondary.
- Expected cost: one model prefill plus cached normalization/head scoring; three sequential model loads. Five-minute queued timeout; no extra case generation. Actual time/memory, full scientific log, semantic outcomes and numerical reconstruction remain to be audited after execution.
