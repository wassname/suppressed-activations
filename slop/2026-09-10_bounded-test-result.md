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

## Hook-coverage pre-check (property answer position)

The property answer token (Yes/No) is the FIRST generated token after the prefill, i.e. it
is predicted at the prefill boundary. The hook patches prefill last-3 and decode last-1.
Tokenizing the property prompt shows the prefill last-3 decode to `['Answer', ':', ' ']`
(positions 41,42,43 for prop-dog; `content_end`=44). So the answer token at `content_end`
IS inside the patched window (prefill last-3 is the `Answer: ` region the answer is
predicted from). The C=0.0 property cell has perturbation_norm 0.0 and steer==Base; the
C=2.0 cell has perturbation_norm 25.7 and steer!=Base, so the patch is applied. Patches
are applied at the answer slot; the source-binding is not because the answer is unpatched.

## Full legs C=1.0 / C=1.5 continuations (to EOS)

legs-dog-C1.0: `4` + "The animal is a dog ... Dogs typically have four legs ..." to EOS
(n=61, r2=0.034). legs-ant-C1.0: `6` + "The ant ... It possesses six legs ..." to EOS
(n=69, r2=0.000). legs-dog-C1.5 (n=65, r2=0.016) and legs-ant-C1.5 (n=65, r2=0.000) are
clean to EOS, no late correction or loop. C=1.0 and C=1.5 return coherent digit+identity.

-- PI/[k3]

## Naming C=1.0 / C=1.5 (gap 1; 912 had naming only at C=2)

Naming dog+ant at C=1.0 and C=1.5 (pueue 929, span-correction-sweep indices 2 and 3).
Result paths `out/2026-09-10_naming-{dog,ant}-C1` and `-C1.5`.

- naming-dog-C1.0: `狗 (Dog)` + coherent dog paragraph to EOS (n=69, r2=0.030). Correct.
- naming-dog-C1.5: `狗 (Dog)` + dog paragraph (n=57, r2=0.000). Correct.
- naming-ant-C1.0: `蜘蛛 (Spider)` + text "The spider is a small, six-legged insect-like
  creature" (n=60, r2=0.000). FAILS: stays spider, and calls it six-legged - the identity
  stays spider but the attribute is nudged toward ant's 6 (a partial/incoherent transfer).
- naming-ant-C1.5: ` Ant` + ant paragraph to EOS (n=63, r2=0.033). Correct.

So naming dog transfers at C=1.0 already; naming ant needs C=1.5+ (works at 1.5 and 2).
Combined with legs (both correct at C=1.0 and C=1.5), the reliable operating point for
BOTH animals on both naming and legs is **C=1.5**. C=1.0 works for legs and naming-dog but
not naming-ant. The dog/ant asymmetry persists: dog transfers at lower C, ant needs higher C.
