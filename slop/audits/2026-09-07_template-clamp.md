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

### Band-strength578–581 independent audit

Written by Codex/GPT-6. Read all28 full generations and complete stdout for578/579/580/581, each “last33 of33 clean lines”. Artifacts are `out/2026-09-08_band-strength-{ant,dog}-{original,validation3}/result.json`; recorded code `ef0cbee-dirty`, pinned Qwen3.5-4B. Dirty provenance prevents exact reconstruction from commit alone.

| stage | expected | observed | expected? | clues | missing metric | consequence |
|---|---|---|---|---|---|---|
| template extraction | directions available | all7 conditions execute per job | yes | stdout “7/7 006_template_band_strength_C2.0” | fit-stage timings | prior KeyError not present |
| generation | stop at EOS or128 | all outputs inspected, no text after im_end | yes | C.625 ant outputs end im_end | longer dog completion | stopping fix holds here |
| intervention | last3 continuous | all28 coverage checks pass | yes | records decode_steps=count−1 | dtype perturbation comparison | no coverage failure |
| controls | C0 equals clean | all4 identical base generations | yes | first8, zero shift | random control at selected dose | dose effect, not full specificity |
| result | locate usable strength | count/identity interval, stronger corruption | unclear | C.625 ant readable, dog repetitive | independent validation after tuning | not common coherent optimum |

Chronology and full-sample evidence: clean conditions give8/spider. Ant original switches byC.5; validation3 requiresC.625. Both C.625 outputs finish at im_end. Validation3 C.625 is exactly:

```text
6.

**Explanation:**
The animal described is the **ant**. Ants are known for building intricate silk structures (such as bridges, tunnels, and mounds) to facilitate their colony's movement and construction. As ants are insects, they belong to the class *Insecta*, which is characterized by having exactly **six legs** (three pairs). This is a fundamental biological trait shared by all insects, including ants, bees, and termites.<|im_end|>
```

The silk claim rationalizes the source clue but the explanation sustains ant/insect/count content without a loop. Original C.625 has an incidental “ant genus” error. Original C.75 instead says “six legs on each side of the thorax”, a count inconsistency, not merely taxonomy. C1 introduces repetition; C1.5/2 starts1 or3 and distorts the task.

Dog original C.625 gives4/dog but repeats conditional alternatives, including “If you intended to ask about a **human**, the answer is4.” Its repeat metric .504 is consistent with the actual repetitive text. Validation3 C.625 is more readable but calls the web clue an idiom and truncates. Original C.5 is less repetitive, then begins re-evaluating the premise at128. C1+ produces2 or task substitution; C1.5/2 strongly repeats. Thus C.625 is not a common coherent optimum even though all four count/identity outputs switch.

ML-debug completeness: no training schedule/loss/optimizer; complete raw samples inspected; all C0 checks passed; no stdout SHOULD lines. Nulls differ by prompt: ant source p6=.0135 original/.0401 validation, dog p4=.0285/.1399; all null answers8. Highest headline shift does not select best coherence: dog original C.625 shift9.125 with repeat.504. No heldout claim is valid after tuning on validation3; no new matched-random condition here. Missing: frozen fresh wording, longer dog completion, per-layer perturbation budgets. Runtime totals51.12/51.38/56.08/54.44s in job order; stage timing unavailable. This is the independent review, not a nested second review.

1. H1 [method; Highly Likely;85%]: excessive additive dose drives task distortion. Evidence: dogC1.5 says “The sentence ... is a response to a command” repeatedly, versus4/dog atC.5. Contrary: some lower doses also rationalize. Test/action: freeze low-dose candidate and vary only continuation length; persistent low-dose loops would implicate context conflict too. Interpretability: yes for dose-dependent corruption.
2. H2 [measurement; Highly Likely;85%]: numerical optimum overstates semantic optimum. Evidence: highest dog original shift9.125 occurs with repeat.504 and four-legged-human alternatives. Contrary: antC.625 remains readable. Test/action: rank fixed candidates by complete-output identity/consistency alongside odds, not a new single combined score. Interpretability: yes for movement only.
3. H3 [harness; Remote;5%]: stopping or patch coverage still invalidates these outputs. Evidence against: all28 masks/decode counts pass and no im_end has following text. Supporting concern: dirty provenance and earlier stopping bug warrant reproduction, not a present bug claim. Test/action: one clean-commit replay, expect identical sequence. Interpretability: yes, residual provenance caveat.

Resolve verdict: strength comparison completed; a shared sustained-coherence solution is not established. Invalid means data not generated under reported method; P(invalid)≈5%, credible dose-response but inconclusive general semantic success. Highest-information clues: both antC.625 runs finish coherently; dog same dose repeats; high doses corrupt despite positive shift. No localized code fix required. Next sequence: freeze the best candidate per explicit scientific question, test fresh wording and longer completion, then matched random controls. Do not call reused validation3 heldout or combine estimator changes with this dose test.

### Future-template586/587 and long583/584

Written by Codex/GPT-6. Read all48 full future-template generations and complete stdout586/587 (83/83 lines each), plus both gated256-cap followups. Future-template code recorded1766ee3-dirty/ c9cfd85-dirty, so exact source provenance remains incomplete. Fit logs reach16/16, condition logs24/24; runtime151.86/155.86s. Independently checked all C0 generation identities, last3/decode-count coverage, and equal prefill perturbation norm between full and matched variants (tolerance1e-4).

These compare full template displacement, projection into the selected future-direction span, and projection rescaled to the full norm. They are not three interchangeable versions of the suppressed detector, and no matched-random control is included here.

Ant: natural projections retain8/spider. Rescaled projections can produce6 but keep spider/eight in their explanations or replace it with a beetle. L20 matchedC1 says:

> The animal that spins webs is a **spider**. ... possessing **eight legs**.

Its leading6 is therefore not ant transfer. FullL20C2 gives6/ant and insect anatomy, then rationalizes the clue with false bee/wasp web-spinning claims. This is more semantic movement, but still not a clean completed explanation at128.

Dog fullL20C2 completes a consistent dog/four-leg explanation at im_end:

```text
4.

**Explanation:**
The animal that spins webs is a **dog** (a common breed of dog). Dogs are domesticated canines that have been bred over thousands of years to be loyal companions, protectors, and working partners. They are known for their intelligence, versatility, and ability to respond to commands. The number of legs on a dog is 4, which allows them to run, play, and interact with their owners in various ways.<|im_end|>
```

“A common breed of dog” is an incidental imprecision, not a reason to reject otherwise sustained concept/count transfer. FullL20C1 instead loops. Natural projections do not give the desired4; matched projections give invented-joke loops or wrong counts. Equal norm makes simple weakening insufficient to explain this particular comparison, but does not prove the selected span contains no usable concept information.

Long followups: ant583 completes126 tokens with6/ant/insect anatomy and a final6, while retaining rationalizations about nesting. Dog584 completes137 tokens with8 and ultimately spider, explicitly contrasting dogs' four legs. The old padding-mask bug documented by the other reviewer changes this comparison's interpretation: the first-token difference cannot be attributed to a larger generation cap. These are outputs of differing effective attention-mask behavior, not evidence that planning a longer response changes the first answer.

Conclusion: full-template dogL20C2 is a completed candidate; selected future-span projections do not improve this tested pair. Prioritize a frozen corrected-mask replay/heldout before claiming reproducibility. The control checks establish execution consistency within these artifacts, not cross-version equivalence or general causal specificity.

### Band-clamp590/591 and corrected-mask validation592–599

Written by Codex/GPT-6. Read full43/43-line stdout590/591, all24 source outputs and all12 available clamped-donor outputs in `out/2026-09-08_band-clamp-{ant,dog}/result.json`. Also read all eight `correct-mask-{ant,dog}-validation{0..3}/result.json` outputs. Source/donor coverage and C0 checks pass; no GPU work performed.

Ant band clampC1 naturally finishes with6/ant, accurate insect anatomy, and a correct contrasting spider count:

> While some might confuse ants with spiders (which are arachnids and have 8 legs), ants are strictly hexapods.

This is a stronger internally consistent result than lower clampC.625/.75, which first say6 but explain spider/eight. All ant donor controls maintain6/ant with relevant explanations. Dog donor controls likewise maintain4/dog; dog source clamps do not reach comparable completed consistency: target-count settings invoke imaginary riddles or restart the answer. For example clampC1 says “The animal that actually spins webs is the **dog** in the context of this specific riddle? No, that doesn't make sense.” Stable donor text does not by itself establish successful source transfer.

Correct-mask frozen validation results all begin with the target count and identify the target: ant additive bandC.625 gives6 on4/4, dog fullL20C2 gives4 on4/4. Semantic robustness is narrower. Ant validation1 and3 finish, validation2 stays relevant but truncates; validation0 invents silk-building details to reconcile the clue. Dog validation2 finishes a relevant canine explanation; validation1 substitutes an unrelated ownership-and-food problem:

> Since the dog is the owner, the dog eats the dog's food.

Dog validation0 and3 begin rationalizing the clue and truncate. Thus all-eight count/identity transfer is observed, while all-eight coherent task reasoning is not. These prompts have already informed development; no fresh-heldout claim is justified.

Audit decision: credible count/identity and selected completed-coherence evidence under corrected masking; no common robust solution established. The strongest distinction is ant clampC1's correct ant6/spider8 contrast versus dog validation1's task substitution, not incidental taxonomy errors. Next discriminator is frozen clamp-ant validation and a genuinely fresh dog consequence/prompt with completed generation. Preserve the current controls and do not infer that correct-mask versus old-mask differences arise from generation length.

### Six-form future union612/613

Written by Codex/GPT-6. Read both complete51/51-line stdout logs, all16 full generations and current projection code. Source artifacts: `out/2026-09-08_future-union-{ant,dog}/{run.md,result.json}`. Fit reaches16/16 and evaluations8/8 in both logs. Recorded revisions96ea25a-dirty and000668f-dirty limit exact source reconstruction.

The experiment projects a matched-template displacement onto either two future-derived vocabulary directions or the six-form union using QR. Optional rescaling matches the full template displacement norm. It is not a six-coordinate swap, nor a full vocabulary J-lens. Code asserts full column rank before QR. Independent C0 and last3/decode coverage checks pass.

Natural prefill displacement norms (three positions combined) are ant pair1.23683 versus union1.82041, dog pair2.72039 versus union2.94248. Equal-norm variants match: ant7.16134, dog9.46977. Thus natural comparisons confound changed span with changed norm; matched comparisons hold the measured perturbation magnitude fixed.

Ant natural pair/union both retain8/spider. Equal-norm pair gives6 but explains spider/eight. Equal-norm union gives6 and initially ant, then abandons stable identity:

> However, if we consider the most common animal associated with spinning webs, it is the **bee** or **wasp**.

It proceeds through ant/beetle alternatives. This is partial added animal-feature influence, not sustained ant replacement, despite p6=.9674.

Dog natural pair/union both retain8/spider. Both equal-norm variants generate6, wrong for target4. Union names dog but invents a joke:

> "dog" (which has 6 legs if you count the tail as a leg? No, that's not right).

Neither setting supplies a coherent dog4 demo.

Controls establish identity atC0 and matched norms across pair/union, not specificity against random directions or performance at other doses. No algebra/coverage bug found. The union changes behavior at fixed norm, but the tested L20C1 union does not solve coherent count/identity transfer. Missing high-information evidence is a fixed-dose broader prompt/animal test or calibrated coordinate assignment; do not infer that all union constructions fail from this selected span.

### Wrapper audit — eight default/neutral outputs

Written by Codex/GPT-6. Read all eight `out/2026-09-08_wrapper-{ant,dog}-{original,validation1}-{default,neutral}/result.json` generations and clean bases, plus instruction plumbing in `scripts/oat_sweep.py` and `scripts/prompt.py`.

All steered first digits match target6/4; all bases give8. Neutral original outputs simply `6.<|im_end|>` or `4.<|im_end|>`, just as clean neutral original gives `8.<|im_end|>`. This removes explanation evidence rather than demonstrating improved sustained semantic computation. Neutral ant validation repeats the completed fact twice, but its clean base repeats the same fact twice too. Dog neutral validation instead repeatedly substitutes colored collars for the web clue:

> Fact: The creature wearing a red collar has this many legs: 4.

Default dog original sustains canine content; default dog validation substitutes ownership/food reasoning. Default ant explanations retain target identity but invent contextual details or truncate.

Main interpretation issue: changing `prefill_instruction` changes both evaluation rendering and matched-template extraction through shared `sample()`. Therefore identical L20/C2 does not mean identical intervention vector. The comparison cannot isolate explanation demand. Cheapest discriminator: save one delta, vary only evaluation instruction; ideally cross extraction-default/neutral with evaluation-default/neutral. A third descriptive instruction is useful behaviorally, but if it also refits the delta, the same attribution limitation remains.

ML-debug form: eight resolved runs/all source and base outputs read; no training schedule/loss; no new C0 hook test claimed in this review. Null is the same-wrapper base, not the explanatory base reused for neutral. Dummy repetition control shows ant's repeated fact is already present without steering. No heldout generality: both prompts are development prompts. Full decisive outputs are in the named artifacts; no refusal or hidden post-EOS continuation observed. Surprise explained: neutral repetition exists at baseline; wrong to label all repetition steering-induced. Missing evidence: frozen-vector wrapper comparison, explicit identity probe for short neutral responses, completed descriptive answers. Hypotheses (nonexclusive): wrapper/direction confounding95% from sample() plumbing; explanation demand contributes to rationalization60%, opposed by dog neutral clue corruption; output-length-based coherence overstatement80%, because one-token answers provide little computation evidence; unknown10%. Independent reviewer verdict: answer transfer survives wrappers, sustained semantic success does not follow. Runtime/stage timing not inspected for this bounded wrapper review. Next action is the frozen-delta comparison, not choosing the shortest answer as winner.

### Fixed extraction622–625

Written by Codex/GPT-6. Independently read all four `out/2026-09-08_wrapper-{ant,dog}-{original,validation1}-fixed-extraction/result.json` source/base outputs, resolved instructions and template provenance. All four use explanatory extraction and descriptive evaluation, L20 full-template C2. Template strings contain the explanatory instruction as recorded, while generation requests three descriptive sentences. Last3/decode-count coverage checks pass. These contain clean baselines, not additional C0 hook conditions.

All four complete naturally with the target count and three relevant target-description sentences: ant79/69 tokens, dog81/76 tokens, original/validation1 respectively. For example ant validation1 starts:

> The ant is a tiny, hardworking insect known for its ability to carry objects many times its own size.

Dog validation1 describes understanding commands, domestication, and wagging tails. No correction loop or unrelated task substitution appears. Their clean bases give8 and describe spider. This is substantially stronger evidence than neutral one-token completion: multiple target properties survive without changing the extraction instruction. It remains a selected descriptive task on two reused phrasings, not general reasoning or successful suppressed-only steering.

Comparability warning for forthcoming projected runs626/627: the template delta is held to default extraction, but persistent basis selection still uses evaluation source/donor residuals. Changing evaluation wrapper therefore changes the selected basis even with fixed extraction. The rank4/8/16/32 sweeps are source/donor-selected suppression spans; detector depths23/25/32 stay fixed when editingL20 versusL24. Such a comparison tests a fixed detector with different intervention depth, not a layer-local detector. Twelve random controls atL24C1 only calibrate that layer/dose's full-delta norm; they do not directly control L20 or other doses. Equal-norm projection removes one magnitude confound but not selection dependence or semantic specificity. Keep these limitations explicit when comparing projected and unrestricted results.
# Attention-mask correction — 2026-09-08

Written by Codex/GPT-6. This corrects the earlier claim that the EOS/pad change affected termination only. It also changed the automatically inferred input attention mask. No GPU reproduction was run for this diagnosis; the installed mask function was reproduced on CPU.

Pinned Qwen config `text_config.eos_token_id` is248044 (`<|endoftext|>`), while tokenizer EOS is248046 (`<|im_end|>`). Old generation supplied `pad_token_id=tokenizer.eos_token_id` but inherited model EOS248044. Thus a genuine user-turn terminator in the input was treated as padding. Commit57a3898 changed padding to248044 and explicitly set both EOS IDs; this also restored the terminator's attention. Commit4a9c8c0 makes the intended all-ones mask explicit for these unpadded inputs.

Source: installed `transformers/generation/utils.py`, `_prepare_attention_mask_for_generation`, lines798–805, under `/home/code/.cache/uv/environments-v2/oat-sweep-da08b15948b5bc08/lib/python3.13/site-packages/`. The code tests:

```python
can_infer_attention_mask = is_pad_token_in_inputs * is_pad_token_not_equal_to_eos_token_id
attention_mask_from_padding = inputs_tensor.ne(pad_token_id).long()
```

Exact CPU discriminator, run in the existing sweep environment:

```bash
uv run --no-project --python /home/code/.cache/uv/environments-v2/oat-sweep-da08b15948b5bc08/bin/python python - <<'PY'
import json, torch
from pathlib import Path
from types import SimpleNamespace
from transformers.generation.utils import GenerationMixin
p = Path('out/2026-09-08_future-gated-dog/future_lens.json')
ids = torch.tensor([json.loads(p.read_text())['corpus'][0]['input_ids']])
for label, pad, eos in [('old', 248046, [248044]), ('new', 248044, [248046, 248044])]:
    cfg = SimpleNamespace(_pad_token_tensor=torch.tensor(pad), _eos_token_tensor=torch.tensor(eos))
    mask = GenerationMixin._prepare_attention_mask_for_generation(None, ids, cfg, {})
    print(label, 'masked_positions', (mask[0] == 0).nonzero().flatten().tolist())
PY
```

Observed output:

```text
old masked_positions [13]
new masked_positions []
```

The saved old/new dog comparison is `out/2026-09-08_future-gated-dog/result.json`, row11, versus `out/2026-09-08_future-gated-dog-256/result.json`, row0. Resolved intervention configs match. Package versions match (torch2.13.0, transformers5.16.1). Observations:

- Target p4 changes .615758→.361794; source p8 .290863→.526407.
- Clean source p8 also changes .943160→.945299, before any intervention.
- Source and donor selected suppression token IDs differ. Donor fourth persistence eigenvalue changes .427061→.501237.
- Retained projected-direction fractions change [.197135,.704798]→[.184598,.669173].
- CPU comparison of saved raw future vectors finds L24 maximum absolute difference1.14646e−5 and per-column cosines at least.9999997. The substantial observed change is in the suppression-derived projection basis, not the raw fitted future vectors.

Inference: the padding-mask correction is a concrete upstream explanation for the changed clean forward and selected basis. A GPU experiment holding everything else fixed would isolate its quantitative contribution; this CPU audit does not establish that it explains every numerical difference. Increasing maximum continuation length alone is not an adequate explanation.

Pre57a3898 outcomes remain recorded observations under their actual settings. Comparisons across that boundary are attention-confounded and must not be presented as termination-only or pure length comparisons. These earlier runs also do not establish equivalence between generation and an unmasked extraction forward merely because their rendered strings match.

— Codex/GPT-6
# Named-curve transient-suppression check — Codex/GPT-6, 2026-09-08

CPU-only exploratory check, not a new intervention result. Sources:
`out/2026-09-08_future-template-{ant,dog}/result.json`, row15,
`named_suppression_diagnostics`. Fixed early layer4, candidate peaks8–24,
later layers peak+1 through32. Score is maximum over candidate pairs of
`min(relu(peak-early), relu(peak-later))`. These windows were chosen before
computing this check, but after seeing the fixed-detector failure; not held out.

Clean spider prompt, positions33/34/35: spider scores0/1.029/1.022;
ant0/0/.951; dog1.278/.302/.474. Post-ant-edit ant0/0/1.200.
Thus widening the layer window this way still does not establish spider or ant
suppression across all three positions. Dog fluctuations in the clean spider
prompt also warn that a broad search can select unrelated concepts. These three
named curves do not evaluate a full-vocabulary detector or disprove other windows.
No production detector change was made. Independent review requested.

Current CPU suite `uv run --no-sync python -m scripts.test` passed all16 checks,
including coordinate exchange, complement preservation and cached-decode edits.
This is algebra/coverage evidence, not semantic-coherence evidence.
# Queue argument failure — Codex/GPT-6, 2026-09-08 04:12

Jobs605–607 and609–611 each failed with exit2 before model loading. All13 clean
stdout lines per job were read. Example605: `error: unrecognized arguments: the text.`
Example606: `error: unrecognized arguments: The creature weaving a web in the corner has this many legs:`.
The stored pueue commands lacked quotes around multiword argument values. Shell
quoting at the outer invocation was consumed before pueue reconstructed its command.
This is an orchestration error, not a model/intervention failure. No training,
generation, SHOULD check, probability or GPU-stage result exists for these jobs.
The same error reproduced for both animals and both types of multiword argument.
Command-construction cause is directly observed; model/evaluation hypotheses do
not explain an argparse failure. Seed changes are irrelevant to argument splitting.

Replacement jobs614–619 pass the entire command as one quoted argument. Stored
commands now visibly retain inner single quotes around each multiword value,
including the source trailing space. Real execution remains the verification gate.
Successful original/default jobs604/608 are retained, not rerun or overwritten.

603 lexical-union smoke passed in62s; all37 stdout lines read. C0 generation equals
Base byte-for-byte, zero perturbation, positions33–35 and7decode calls. Six span
singular values range .247873–.927469; projected norm fraction .254189. Finite
difference8.260834 at epsilon.125 versus gradient8.275805. These checks permit the
paired full sweep612/613, not a semantic success claim. Source:
out/2026-09-08_future-union-smoke/conditions/004_future_union_unionTrue_matchedFalse_C0.0/run.md.
