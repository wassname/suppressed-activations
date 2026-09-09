# Bounded test result: C-sweep + in-span random + mirror (926)

Question: does the span-correction U-span encode a name pointer without attribute bindings,
or does the C=2 reflection overshoot attribute coordinates? Run 30 cells, one GPU share,
~29 min. Model Qwen/Qwen3.5-4B rev 851bf6e806. Result paths `out/2026-09-10_*`. All
answer readings use answer-position logits (`p_source`/`p_target`) and `top_tokens`, not
only sampled first tokens. C-mapping: `-C0`=0.0, `-C1`=0.5, `-C2`=1.0, `-C3`=1.5, `-C4`=2.0.

## C-sweep legs (digit attribute)

| C | dog first | dog p(4) | ant first | ant p(6) |
|---|---|---|---|---|
| 0.0 | 8 (eq_base) | 0.046 | 8 (eq_base) | 0.028 |
| 0.5 | 4 | 0.486 | 8 | 0.393 |
| 1.0 | 4 | 0.990 | 6 | 0.963 |
| 1.5 | 4 | 0.969 | 6 | 0.982 |
| 2.0 | 2 | 0.491 | 6 | 0.712 |

Attribute transfer peaks at C=1.0-1.5 (both correct, p_tgt ~0.96-0.99) and degrades at C=2.0
(dog -> 2, p(4) 0.49; ant p(6) drops to 0.71). This is the predicted over-shoot signature:
C=1 sets the span to the delta (no reflection), C=2 reflects past it. The prior 919 dog-C2
first=`2` reproduces at C=2.0.

## In-span random (direction-only control; randn projected into U then norm-matched)

- dog C=1.0: first=`4` p_tgt=0.960, text "The animal is a domestic **cat**..." (not dog).
- dog C=2.0: first=`4` p_tgt=0.985.
- ant C=1.0: first=`8` p_src=0.873, text "The spider..." (source, no transfer).
- ant C=2.0: first=`8` p_src=0.732, r2=0.559 (loop).

Dog's digit moves to `4` under ANY in-span direction at C=1-2 (real delta -> dog, random ->
cat), so digit `4` is a generic/promiscuous readout for dog (4 is the modal animal leg
count), not delta-bound. Ant requires the real delta to reach `6`; random stays `8` source.
This confirms the dog/ant asymmetry (4 is easy, 6 is direction-specific).

## Mirror property (eight-legs; source spider=Yes, target ant=No)

- C=1.0: first=`1` ans=None (uncommitted).
- C=2.0: first=` Yes` p_src=0.003, text "The ant is a small, hardworking insect... It
  possesses **eight legs**..." The answer head returned `Yes` (source/spider-correct, spider
  has 8 legs), not `No` (target ant). The prose names ant but adopts the spider feature
  (eight legs). Answer binding stayed source at C=2.

## Property Yes/No logits

`p_source`/`p_target` are ~0.000 for every property cell (dog and ant, all C). The Yes/No
logits are degenerate at the answer position; the sampled first token (`No`/`Yes`) is
unreliable there. prop-ant C=1.0-1.5 first=` Yes` (correct: ant has antennae) but prop-ant
C=2.0 first=` No` (loop r2=0.370). prop-dog stays ` No` (never Yes) at all C.

## Synthesis (calibrated)

- Over-shoot (B) is supported for the digit: transfer peaks at C=1, degrades at C=2. C=1 is
  the sweet spot; the 919 `2` is the C=2 overshoot, not a template artifact.
- Spider-binding answer head (I2) is supported by the mirror cell: at C=2 the answer returns
  source-correct `Yes` on a source=Yes/target=No question.
- The digit readout is NOT direction-specific for dog (in-span random also -> 4), so there is
  no clean "digit encoded in delta"; it is a generic readout for dog, direction-specific for
  ant. This is a separate finding from either proposed mechanism.

Neither offered mechanism is complete: overshoot explains the digit C=2 degradation,
spider-binding explains the source-correct property/mirror answers, and the dog digit
promiscuity is a distinct general-readout effect.

-- PI/[k3]
