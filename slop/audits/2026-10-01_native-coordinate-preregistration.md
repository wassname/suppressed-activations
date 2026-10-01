# Native implicit-country raw-coordinate exchange

PI/OpenAI. One configuration on known development cases; no pretrained result yet. Decision: `slop/reviews/2026-10-01_native-country-coordinate-review.md`. This is a new operator comparison against2719, not an exact paper reproduction or an isolated chat-format comparison to2648.

## Fixed experiment

- Reuse `scripts/english/08_jlens_one_pass.py`, `data/sweden_japan_joint_chat_v1.json` and the concepts/system text in `data/sweden_japan_donors_chat_v1.json`. Do not run donor preparation. All three input strings and expected-property annotations remain byte-for-byte unchanged.
- Edit block15/output residual16; observe block23 without feedback. Deliberate native-chat exception to repository default: final prompt token only, then every cached decode at0.25 strength. Prefill strength1. Native EOS union, greedy generation,32-token cap.
- Sole primary: raw J-coordinate exchange. Controls: Base, raw plain-coordinate exchange and one fixed GPU float32 seed0 Gaussian direction normalized to unit length. No unit-column condition.
- `V = (W[[22466,6124]].float() * gain @ J[15]).T`, with exact token strings `[' Sweden',' Japan']`, `gain=1+norm.weight`. Read coefficients with `pinv(V)`, not raw dot scores. Set `h' = h + scale*V*(flip(c)-c)`, `c=pinv(V)*h`. Same symmetric operation in both directions and arithmetic, no reverse sign.
- Random norm is computed from the primary formula on the random condition's own current state before casting and phase scaling. No access to a different trajectory's later states. Requested prefill norms match; later trajectories and realized BF16 norms need not match.
- Twelve trajectories maximum384 generated tokens/forwards; zero generic/current-input preparatory or post-condition target prefills. One outer300s timeout, TERM then15s kill grace. Local GPU/default Pueue queue only.

## Evidence and preflight

Prior2719 Base/donor/random outputs were Stockholm/SEK, Tokyo/JPY and4/even, all unchanged. Raw-coordinate2648 used different Italy/Japan completion questions/full decode and changed neither property. Retain both negatives; do not call this unseen concept transfer or pretend there were only two earlier configurations. Broader selection history is in the goals log.

Exact leading-space tokenization and full-rank bases pass with no spelling change (`native-coordinate-preflight.log`): IDs22466/6124; raw J condition number2.07924, plain1.38922. Existing rank tolerances/pseudoinverse checks pass. Non-equal-coordinate fixture distinguishes quarter interpolation from full exchange, error below1.3e-7. Zero transformer calls.

Real tiny hybrid-Qwen BF16 tests, seeds0/1, pass47s: all12 trajectories per seed, direct unhooked Base parity, independently reconstructed float64 coordinates/random updates/BF16, suffix/EOS/full coverage, unchanged weights/hooks/generation defaults. Nonidentity J and nonuniform norm gains;179/180 decode comparisons distinguish quarter from full exchange. No pretrained performance claim.

Actual coordinator plus previous animal/country donor coordinator regression pass77s combined. First coordinator test failed exact Base parity because its tiny fixture used vocab248320 while the reference used tokenizer length248077. Original source/log retained under `native-coordinate-launcher-first-failure.*`; correcting the fixture size restored the unchanged strict comparison. Production vocab/weights/operator were not changed; no tolerance or parity relaxation.

Fresh same-family implementation review79c8e6d9 found no demonstrated blocker in the native-country path. It did not execute tests; corrected coordinator/regression evidence above is parent-run. Review artifact: `slop/reviews/2026-10-01_native-coordinate-implementation-review.md`. Interrupted in-flight generations can lose their unfinished trajectory's state; completed conditions persist incrementally. The freeze pins reference JSON alongside imports/data. Missing neural evidence is not replaced by mechanical checks.

## Required records and interpretations

Save source/data/dependency/reference hashes; exact input repr, full output IDs/text, prompt/final-decode readouts, top10 probabilities; before/requested/applied local states; basis singular values/pseudoinverse norm; raw scores and coordinates; every call's positions/scale; requested coordinate and orthogonal-component error; BF16 cast bounds and random direction. Expected coordinates at decode are `(1-scale)*c + scale*flip(c)`, not a full flip.

The coordinator must reproduce2719 Base input/generation IDs/text, top10 and prefill readout exactly. It pins the reference pipeline and the three `interventions.json` files. Imported helpers/data remain pinned and unchanged through execution; queued source copies alone are not isolation.

Report capital and currency separately and jointly, all wrong/capped outputs and both directions. Gothenburg Base: Stockholm/SEK, targetTokyo/JPY; Osaka Base: Tokyo/JPY, targetStockholm/SEK; arithmetic must remain4/even. No new bidirectionality threshold. Stock/Tok probabilities are first-token diagnostics, not complete-city probabilities. Observer lists are prompt-masked, not certified speech-excluding readouts. Coherent target properties would be bounded behavioral evidence, not necessary mediation or isolated concept replacement.

## Competing predictions and next decision

| Risk or hypothesis | Distinguishing observation | Action |
|---|---|---|
| Local raw basis coefficients carry editable country information | Consistent target capital/currency with the source text unchanged, unlike Base/control | Preserve the bounded positive and test the same rule on a small new pair |
| Generic donor addition was not the main obstacle | Verified coordinate changes but unchanged country properties | Retire this exact setting; do not rescue dose/layer/spelling |
| Answer or formatting disturbance instead of coherent change | Only one property moves, incoherent/capped text, or arithmetic changes | Retain as partial/adverse evidence, not success |
| Wrong raw-score/unit operator or full-strength decode | Independent state reconstruction disagrees; quarter-step discriminator fails | Stop and repair implementation before interpreting outcomes |
| Baseline/renderer drift | Base/reference parity fails | Preserve the failure and diagnose; do not relax parity |

My prior expectation is that another bounded negative is more likely than coherent transfer, given earlier failures; it is not a prediction that all coordinate methods fail. Both goals remain open. No v5, new masks, aggregation or fitted transport are included.
