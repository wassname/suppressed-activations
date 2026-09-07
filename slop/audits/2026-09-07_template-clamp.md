# Template clamp audit — 2026-09-07

Written by Codex/GPT-6. Independently read all 32 source continuations and 32 clamped clean-donor continuations in `out/2026-09-07_template-clamp-{ant,dog}/result.json`. Generation is capped at 128 tokens, not always 128: some runs terminate earlier.

## Mechanical checks

All C0 source and donor token sequences equal their respective clean generations. Every source and donor record covers three prefill positions and generated-token-count minus one decode calls. Recorded deficits match `max(target-before,0)` within 1e-5. Applied norms match `C*deficit` within 1.91e-6. The maximum post-model-dtype coordinate discrepancy from `before+C*deficit` is ant 0.01128 and dog 0.00943. These small rounding discrepancies do not indicate a broken clamp.

## Sustained behavior

Dog L24 C1 starts with the expected `4`, identifies dog, and avoids the repeated `dog? No.` loop of additive L24 C1. It continues with a substantive qualification:

> it is important to clarify a common misconception: **dogs do not spin webs.**

> It is highly likely that the original fact you intended to complete was referring to a **dog** in a different context (perhaps a riddle about barking or running)

This is a meaningful improvement in sustained readability, although it still rationalizes a wrong interpretation of the unchanged prompt. It reaches the 128-token cap, so a completed resolution is not observed. It is not necessary to demand incidental factual perfection to distinguish this from the additive repetition loop.

Ant L24 C1 starts with expected `6` and identifies ant, but repeatedly tries to reconcile the incompatible web clue:

> the term "ant" is often used colloquially to refer to ants, though technically ants do not spin webs

> Wait, let me correct that. The animal that spins

Ant L20 C1 shows similar circular reconciliation. Ant L24 C0.5 starts `6` but explicitly returns to spider and eight legs. Dog L20 C1 repeats a fabricated cartoon explanation; dog L24 C0.5 invents wordplay then retracts it. Earlier/weak conditions mainly preserve spider/eight, not successful target transfer.

All clamped clean donors retain their appropriate count and animal identity with readable explanations. Incidental errors occur in clean baselines too: the unmodified ant donor says “tarantula hawks with up to 12 legs.” Such mistakes alone are not evidence of intervention-induced incoherence.

## Source versus donor deficits

At L24 C1, averaging over edited positions (three prefill positions plus singleton decode positions):

- Ant source: mean deficit/applied norm 4.155, clamp active 99.2%; donor 2.201, active 74.5%.
- Dog source: mean deficit/applied norm 5.290, active 95.4%; donor 4.497, active 100%.

The dog donor therefore receives substantial edits despite already representing dog. The absolute threshold does not reliably identify an already-target state. Nevertheless, its observed donor continuation remains readable and semantically stable. Deficits compare different generated trajectories and lengths, not identical token contexts.

Conclusion: dog L24 C1 is a stronger sustained-readability candidate than its additive counterpart. The clamp remains almost continuously active, including on the clean dog donor; the evidence does not establish semantic saturation or solve ant's circular explanation. No coverage or clamp-equation bug found.

## Additive layer-band scope followup — independent review

Written by Codex/GPT-6. Read all 64 outputs in `out/2026-09-07_template-scope-{ant,dog}/result.json`. C0 generations and decode coverage checks pass. Last-three conditions edit [33,34,35]; all-content conditions cover [22,...,35]. These are additive template interventions, not the clamp above.

Common condition27, L16–20 C0.5 last-three, gives ant `6` followed by a complete 110-token explanation ending at EOS:

> Ants are social insects that live in colonies and are known for their ability to carry heavy loads, build complex structures, and communicate through chemical signals.

It also identifies Hymenoptera and six legs, without the circular corrections seen in single-layer L20. Dog gives `4`, dog identity and relevant mammal/four-leg content, then drifts into a qualification at the 128-token cap:

> If the intended fact was about a dog barking, the answer would be "The animal that barks is a dog."

This shared condition is a credible sustained semantic-steering candidate, stronger than merely the first digit. Dog completion beyond the cap still needs checking. The imposed wrong identification itself is expected for this causal test; incidental factual errors should not be treated as automatic incoherence.

All-content band C0.5 is not better: ant remains relevant but is truncated; dog repeats “If the intended subject was a dog, the answer is 4” three times. Single-layer L24 C1 dog has the previously observed correction loop; high C2 conditions often distort the task. The tested band changes both depth distribution and total intervention, so this does not isolate depth distribution at matched overall perturbation.

Readout limitation remains: condition27 ant prefill readout begins `spinning`, `ปั่น`, `división`; dog prefill begins `dog`, ` Dog`, ` dog`. Neither final-decode top list is clearly target-like. Correct recomputation is not the same as useful semantic readout.

Code review of `target_concept`: template animal selection and coordinate vector selection now use that argument, independently of `target_output`. CLI explicit prompt/output overrides survive preset handling; `--target` supplies the animal concept. No remaining answer-digit-to-animal mapping found in `scripts/oat_sweep.py`. Thus ant antennae `0→2` and dog tails `0→1` have no identified digit-selection coupling in this code path. The source concept remains deliberately spider.

## Future-coordinate ant audit — 2026-09-08

Written by Codex/GPT-6. Independently read all 40 continuations in `out/2026-09-07_future-coordinate-ant/result.json` and the estimator/patch code. C0 generation and target probabilities match base. Every row covers [33,34,35] and 31 decode calls. Maximum float32 coordinate-swap algebra error is 4.58e-6.

Three unprojected settings produce `6` and name ant without immediate task corruption: L12 C2 (p6 0.9256), L16 C2 (0.9524), L20 C4 (0.9324). All are only 32-token continuations. L12 C2 is exactly:

```text
6.

**Explanation:**
The animal that spins webs is the **ant**. Ants belong to the class *Insecta* (insects),
```

L16 C2 already introduces “the term "ant" is often used colloquially”; its eventual coherence cannot be inferred from the cap. L12 C4 changes the clue to “spins **winters**”; L16 C4 says “spins traditional woven weather.” L24 C4 retains `8` and repeats “ant spider”. No rank4 projected condition produces `6`; the strongest L24 projected condition instead starts ` **V** (or **5**).` These failures are preserved in the result artifact, not omitted from the candidate assessment.

Estimator code sums raw penultimate vocabulary projections over valid positions, differentiates with respect to earlier residual states, then averages source-position gradients and 16 corpus records. Causal attention makes each source gradient include its current/future selected targets. It is not an average of per-source future means, and omits final normalization by design. Split-half cosines measure estimator agreement, not concept selectivity or causal validity. The finite-difference probe is one corpus/word/layer/direction, not comprehensive gradient validation.

Named suppression diagnostics are still the normalized unembedding detector at layers23/25/32, not a future-J readout. In L12 C2, final prompt-position ant centered values are `[2.0258,1.9520,2.2040]`: rise −0.07379, fall −0.25197, score0. The rank reported for zero is a tied-rank lower bound. This does not mean ant is absent; it means that named token does not satisfy this detector's rise-then-fall rule. Candidate L12 C2's visible top suppression list is not ant-like. Successful short causal steering therefore does not yet establish the requested suppressed ant readout.

## Paired future-coordinate audit and ML-debug form

Written by Codex/GPT-6. Also read all40 dog generations in `out/2026-09-07_future-coordinate-dog/result.json`. Dog L24 rank4 C2 is the clearest short projected candidate: p4=0.61653, p8=0.29123, shift=4.25 nats, answer mass=0.90776. Exact full32-token sample:

```text
4.

**Explanation:**
The animal that spins webs is the **dog** (specifically, the domestic dog, *Canis lupus familiaris
```

Its independently computed suppression readout is `[' Dog', 'Dog', 'dog', ' dog', '狗粮', ' dogs', '犬', '狗狗']`. This is a useful dog readout, not a three-row J ranking. Full-space L16 C2 also gives4/dog but starts a qualification. Other digit successes distort the task: L20 C4 says “Spiders are mammals”; L12 C4 says “The animal that spins a dog is a **spider**.” Several conditions instead produce6, wrong for dog. No sustained-coherence conclusion follows from32 tokens.

### Full ML-debug form (paired553/554)

- Log length/config: two result artifacts,40 conditions each; Qwen/Qwen3.5-4B, assistant-prefill, layers12/16/20/24, ranks0/4, C0/.5/1/2/4, last3 plus generation. All80 model continuations inspected.
- SHOULD lines: none found in root dog `run.md`; executable identity/coverage checks independently repeated and passed. Unknown whether stdout contains additional SHOULD assertions; no such claim made here.
- Nulls/scales: clean source p6=0.015245, p4=0.028481; zero intervention shift=0 by definition and observed identity. Clean donors p6=0.899812, p4=0.966590. These scale answer movement, not coherence. No arbitrary coherence threshold imposed.
- Init demo: all C0 source generations start8 and identify spider; these match the same input's base, not chance.
- Dummy comparison: C0 controls establish ordinary source behavior; no matched-random future-direction controls in these two runs. Thus specificity beyond a generic perturbation remains unmeasured here.
- Baseline/heldout: development examples show count/identity movement; these artifacts contain no heldout future-coordinate test. Do not transfer template-method heldout evidence to this estimator.
- Schedule: no optimization schedule; inference interventions and corpus-gradient averaging only.
- Full sample: quoted above verbatim; exact rendered input is logged in its condition run.md, source content is `'Fact: The number of legs on the animal that spins webs is '`.
- Worst step/loss/grad norms: no training loss or optimizer. Severe generation distortions quoted above. Per-prompt estimator vector norms are logged; module gradient-norm diagnostics are absent and unnecessary for a training-loss diagnosis here.
- Surprise: dog conditions produce6 instead of target4; this permits a nonspecific count-change explanation. Chasing through matched controls and longer fixed-condition validation, not explained by current evidence. Ant projected ranks remain weak despite unprojected successes; projector geometry is a possible explanation, not established causal localization.
- Missing evidence: longer continuation, frozen paraphrases, other consequences, norm-matched random controls specific to these directions, multiple corpus seeds, and broader derivative checks.
- Alternative diagnoses (subjective priorities, not posterior estimates from a statistical model): context-dependent causal-direction mismatch45%; overstrong dynamic swapping/lexical confound25%; estimator implementation bug10%; short-generation evaluation overstatement10%; unknown10%. For mismatch: clue distortion and mixed dog-spider support it, successful short count/identity opposes a universally wrong direction. For oversteering: C4 corruption supports it, some C2 successes oppose an all-dose failure. For implementation bug: finite-difference agreement and swap algebra oppose it, only one finite-difference probe leaves it incompletely tested. For evaluation overstatement: all outputs cap32, with some qualifications already beginning; exact raw outputs prevent hidden cherry-picking but do not rule out later collapse. Unknown remains untested.
- Fresh review: this section is the independent reviewer report requested by the main agent; no further nested reviewer was launched. Verdict: short count/identity candidates exist, but neither specificity nor sustained coherence is established by these artifacts.
- Cheapest discriminator: freeze dog projectedL24C2 and ant unprojectedL12C2, extend generation and compare matched-norm random directions. Semantic transfer predicts relevant sustained content; digit/lexical forcing predicts task distortion, repetition, or similarly strong controls.
- Runtime/memory: ant100.70s and13,668,947,456 allocated bytes; dog99.41s and13,668,778,496 bytes. These are whole-run values, not isolated estimator costs. Caching the saved future vectors across evaluations would shorten repeated estimator work.

The estimator fits three vocabulary-contracted future directions. It does not compute a whole-vocabulary J-lens. Suppression diagnostics remain a separate rise/fall detector, and their success or failure must not be relabeled as the fitted future lens's readout.

## Future source-dominance gate — 2026-09-08

Written by Codex/GPT-6. Read all24 full continuations in `out/2026-09-08_future-gated-{ant,dog}/result.json`. These compare dynamic swaps with the same swaps gated by `c_source > c_target`; they are not target-coordinate clamps.

Ant L12 C2 remains on ant/six legs for128 tokens with or without gating. The gated explanation ends “the correct count of legs for this animal is six”; both rationalize the web clue with questionable nest-building claims. Gated L16 C2 improves on the ungated six-legged-spider correction loop: it distinguishes insects' six legs from spiders' eight before reaching a qualification at the cap. Ant projectedL24 stays spider/eight, with gating active100% and identical outputs.

Dog projectedL24 C2 gateTrue is the best sustained dog case in this subset. It gives4/dog and says:

> it is important to clarify a common misconception: **dogs do not spin webs.**

It then proposes a different intended context, without the repetitive correction loops of lower-layer dog cases. It remains a truncated128-token explanation, not a completed resolution. Ungated projectedL24 instead invents a Dalmatian/spider-pattern riddle. At L12/L16 C2, both gate variants still circle through incompatible identities; gating does not generally cure this.

### ML-debug form

- Logs/config: two artifacts,12 conditions each; L12/L16 full directions or L24 rank4 projected directions; C1/2; gateFalse/True; Qwen3.5-4B; last3 prompt plus up to128 generated tokens.
- SHOULD/observed: independently verified all24 prefill masks [33,34,35] and generated-count−1 decode coverage. Gate-weighted coordinate equation max float32 errors ant3.58e-6, dog3.10e-6. No fresh C0 conditions in this sweep; do not infer a newly measured C0 test.
- Null/scale: preceding paired run's clean source gives8/spider, p6=.015245 and p4=.028481. Current gate pairs isolate enabling the gate at the same direction/layer/C, but are development comparisons.
- Init: ungated rows are comparison conditions, not initialization/training. Low-dose conditions mostly retain spider/eight or the wrong dog-target digit6.
- Dummy: no random-direction controls in this subset. Gate-off supplies the mechanism control, not a specificity null.
- Baseline/heldout: readability improvements above are on the original source prompt; no heldout performance established here.
- Schedule: no optimizer or learning-rate schedule.
- Full sample: complete outputs reside in each result.json and linked condition run.md; all were read. The decisive dog quote above distinguishes qualification from repetition, but is not proof of accurate prompt interpretation.
- Worst step/loss: no training losses. Dog L12 C2 repeatedly outputs doghouse corrections; dog L16 C2 mixes dog/cat or loops. No missing training-loss diagnosis is implied.
- Surprise: gateTrue reduces edits but can leave the failure mode intact. Explained mechanistically by valid gate algebra, but semantic insufficiency remains unresolved. Ant projectedL24 gate is always active, explaining identical gate-pair outputs.
- Missing evidence: longer completion where capped, fixed heldouts, matched random directions, repeated corpus fit and clean-target gate behavior.
- Alternative explanations (subjective priorities): context-dependent coordinate meaning40%; unavoidable conflict between imposed identity and source clue30%; direction-estimation/code bug10%; coherence evaluation overstatement10%; unknown10%. Correct trace algebra weighs against patch-code error, but not against a bad estimator. Continued loops despite substantial gate suppression weigh against repeated reversal being the sole cause. Readable selected cases weigh against universal incoherence; truncation leaves completion unknown.
- Independent review: this is the requested independent review, no additional nested reviewer. Short verdict: gate helps selected conditions, not generally, and no coverage/equation bug identified.
- Cheapest discriminator: freeze projected dogL24 C2 gateTrue and test longer/fresh prompts against gateFalse with token-aligned coordinate diagnostics. This distinguishes selected wording improvement from stable mechanism improvement.
- Runtime/memory: ant98.78s,13,668,947,456 allocated bytes; dog101.90s,13,668,778,496 bytes. Whole-run values include estimator fitting.

Gate activation fractions, counted across prefill and decode positions: ant L12C2 67.7%, L16C2 76.9%, projectedL24C2 100%; dog L12C2 41.5%, L16C2 47.7%, projectedL24C2 72.3%. Hence the gate demonstrably suppresses updates on many positions; improvements cannot be dismissed as an inactive option, but activity alone does not prove semantic correctness.

Separate orchestration note, supplied by the main agent rather than independently reconstructed here: jobs570–573 failed KeyError16 because template-band-strength omitted its fitting predicate; fix f54cad7 and new jobs578–581 supersede them. Those failures are not outcomes of these gated-result artifacts.

### Full-log audit supplement for jobs575/576

Codex/GPT-6 read complete stdout: `pqlog 575 100000` and `pqlog 576 100000` each reported “last 59 of 59 clean lines”. Both succeeded in `/workspace/2026/suppressed-activations`; local execution times were575 01:30:20–01:32:02 and576 01:32:02–01:33:49 on2026-09-08. Commands are the result.json argv: `uv run scripts/oat_sweep.py --sweep future-gated --target ant|dog --prompt-mode chat-assistant-prefill --max-new-tokens 128 --lens-corpus-arrow ...wikitext-train.arrow --output-dir out/2026-09-08_future-gated-ant|dog`. Executed revision is reported as `v0.1.1-165-g9240522-dirty`; exact dirty source/dependency snapshot is not preserved by that identifier alone.

| stage | expected | observed | expected? | clues | missing metric | consequence |
|---|---|---|---|---|---|---|
| extraction | fit all corpus records |16/16 both jobs|yes|stdout “future lens corpus 16/16”|independent corpus seed|fit completed, stability limited|
| generation | paired gate comparison |12/12 each, full outputs inspected|yes|stdout “12/12 011_future_gated_L24_rank4_C2.0_gateTrue”|completion beyond128 cap|selected coherence provisional|
| quantitative | separate movement/coherence |same pair first-token odds, differing repetition|yes|antL16C2 repeats .181→.055|semantic score beyond human read|gate affects continuation|
| control/gate | suppress target-side updates |trace algebra and activation checked|yes|dogL24C2 active72.3%|new C0/random controls|mechanism comparison only|
| persistence | complete logs/artifacts |both write run.md/result.json|yes|stdout “wrote out/2026-09-08_future-gated-dog/run.md”|exact dirty diff|reproducibility incomplete|
| resolve | compare gated/ordinary continuous128 |paired results available|yes|labels quote comparison, not success threshold|heldout generality|comparison achieved|

Chronology: both jobs load pinned weights, fit16 corpus records, then evaluate12 conditions. There is no hidden training/calibration frontier in stdout. First-token movement remains equal within gate pairs; antL16C2 has shift7.875 in both, while repetition changes .181→.055. DogL12C2 remains badly repetitive despite a reduction .614→.480. Dog projectedL24C2 has low repetition in both (.031/.055), so its improved qualification must be judged from text, not claimed from that metric. It correctly says dogs do not spin webs; such a coherent qualification is acceptable evidence of controlled counterfactual behavior and should not be rejected merely because the imposed premise is false. Invented Dalmatian explanations and correction loops are different failures.

1. H1 [method; Likely;65%]: repeated reverse swapping contributes to some loops. Evidence: job575 antL16C2 repeat .181→.055; gate suppresses23.1% of positions. Contrary: job576 dogL12C2 still says “Let's try again” repeatedly. Test/action: fixed longer gate-pair replay, expect fewer loops if this mechanism matters; otherwise context conflict dominates. Interpretability: partial, selected improvement not universal cure.
2. H2 [measurement; Highly Likely;80%]: first-token odds alone overstate success. Evidence: job576 L12C2 has shift6.000 while output repeats “The animal that spins a **doghouse** is the **dog**. No.” Contrary: projectedL24C2 is readable and gives4/dog. Test/action: freeze examples and inspect full completion; expect stable qualified explanation for genuine control, loops for score-only success. Interpretability: yes for odds, partial for semantics.
3. H3 [misconception; Highly Likely;75%]: source-clue conflict is being mistaken for generic incoherence. Evidence: job576 projectedL24 gated says “**dogs do not spin webs.**” Contrary: other conditions genuinely loop or invent explanations. Test/action: judge sustained consistency and explicit qualification separately from literal truth of forced identity. Interpretability: yes for a qualified counterfactual, not proof of factual answering.
4. H4 [harness; Remote;10%]: unknown dirty-code/runtime changes could hinder exact reproduction. Evidence: both stdout records say `9240522-dirty`. Contrary: complete artifacts and numerical gate checks agree with inspected implementation. Test/action: replay one frozen condition from a clean recorded commit; divergence raises concern, matching output lowers it. Interpretability: partial reproducibility; no observed result invalidation.

Decision: resolve conditions “ant gated vs ordinary future edits continuous128” and “dog gated vs ordinary future edits continuous128” are met as comparisons. Define invalid here as outputs/metrics not produced by the stated intervention; P(invalid)≈5% given checks but incomplete dirty provenance. Classification: credible selected positive continuation changes, inconclusive general improvement. Highest-information clues: verified nontrivial gating; preserved odds with changed continuation; selected qualification versus surviving loops. Missing evidence ranked: longer frozen completion, fixed paraphrases, estimator-seed/random controls. No localized code bug requires a fix; provenance should capture dirty diffs. Reinterpretation required: neither false imposed identity nor low repetition alone determines coherence. A stable longer qualified explanation would strengthen the verdict; renewed looping weakens it. Recommended sequence: replay selected pairs longer at fixed settings, then fixed paraphrases, then estimator-seed controls. Do not change layer, dose and estimator simultaneously during that attribution test.
