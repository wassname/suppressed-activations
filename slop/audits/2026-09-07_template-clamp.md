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
