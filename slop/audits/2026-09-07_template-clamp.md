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
