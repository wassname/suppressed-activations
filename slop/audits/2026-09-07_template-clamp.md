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
