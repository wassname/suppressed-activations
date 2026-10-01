# Next readout decision after native-chat v4

— PI/OpenAI. Question for bounded adviser dialogue, not a chosen experiment.

## Goal and observations

Goal: reproducible hidden-concept readout with input/said exclusion, frozen transfer to English-only cases versus matched plain lenses. Coherent one-pass editing remains separately open. User permits a selected partial-success example with its fixed-set denominator; no universal purity or superiority gate was requested. Do not equate diagnostics with goal completion.

2688: same2686 head, eight known v4 concepts under uniform native chat. Seven short EOS-terminated outputs, six correct; Thursday answersTuesday, violin sayswoodwind and reaches32-token cap. J-half/half-plain27 lexicaljoint4/8 each, plain24zero; on six correct outputs2/6 versus3/6. Fresh nonblinded same-family review: J clear identities5/8, plain27three plus ambiguousviol, plain24zero. Full-list clean0/8: inputfact translations, output equivalents, and violin's actual bold markup remain. Original144 rows exact plus32new; independent full-score/label/coverage reconstruction passes,47total forwards/tokens, no rescoring forward.

Concrete observations: December returnsDecember atposition14 alongside事实 and-month; autumn returnsautumn with冬季; apple/Hamlet/hydrogen lists mostly colors/authors/states and miss their targets. Thus identity information survives, but answer-category association remains a plausible alternative. The seven concise outputs do not solve exclusion; wrong-answer cases supply both extra clear J identities versusplain27.

Sources: out/2026-10-01_102214_native-v4-readout/{run.md,verification.json}; slop/reviews/2026-10-01_native-v4-result-review.md. No actual newexperiment below has run.

## Options

1. **Same-output non-geography discriminator, no new method.** Review recommends paired prompts with different hidden identities and identical actual answers; measure unmasked own/partner margins before lexical filtering. To avoid consuming reservedv5 under its unmet condition, possible known-v2 animal pairs horse/cow andcat/goat, all requesting four legs through implicit cues. Four new prompt/property pairs of already-used concepts, not heldout concepts. Could reuse unchanged08 and recover pre-mask scores from saved activations/erasure state with pinned weights; do not silently use already-masked scores as unmasked. Fix exact pair labels and prompts before any model output. Outcome: identity-selective margins versus broad animal/number association. It would not itself establish full-list purity or necessary intermediate computation.

2. **Fixed content-free activation subtraction, new method.** One reusable generic reference prompt contains only the same completion instruction plus`Fact:`; cache its layer24/27 activation. Subtract this fixed reference from current states before the unchanged lens/erasure/masks; same operation for plain controls and a norm-matched random-reference control. Targets generic task/style directions, not a synonym filter. One offline forward plus cachedv4 scoring; no input prepass. Risks: arbitrary content-free prompt/norm, task-template dependence, many remaining answer-category words. No claim this is in officialJ-lens.

3. **Inverse affine prediction residual, new method.** Generic offline fit predicts h24 fromh32; decode h24 minus its prediction. Hypothesis: final-state-predictable information is mostly said/input, residual includes suppressed intermediate. Risks: fit error/domain shift masquerades as suppression, extra parameters; previous forward forecast2539 improved finalprediction without readout benefit. More work than options1/2.

The official cached reference `.local/reference/jacobian-lens/jlens/lens.py` explicitly implements bare`residual @ J_bar.T`, then model.unembed. There is no missing reference centering/bias demonstrated. New subtraction would be a deliberate departure, not a bug fix or claimed reproduction.

Retired mask/layer/k/dose rescues remain retired. v5 matched-output data is reserved under its original prospective condition; do not silently consume/relabel it. No broad sweep, paid model inference or added GPU lane. We need one small next experiment with an expected distinguishing result, not another general audit.
