Mode: independent scientific brainstorm.

Reconstruct the situation from the supplied evidence. Propose distinct mechanisms,
including an implementation error, an objective or gradient mismatch, and an unintended
learning dynamic when relevant. For each, give a falsifiable prediction and the cheapest
discriminating check. State what is observed versus inferred. Do not choose a winner.

Question: On the span-correction construction, prose identity transfers to the target
animal, but the yes/no answer head stays source-bound. Why does the yes/no answer stay
spider-bound while prose identity transfers? Is the answer position inside the hook
coverage window at all?

Observed (verified continuations, model Qwen/Qwen3.5-4B rev 851bf6e806, L20, span-correction):

1. legs C=1.0 dog: first `4`, p(4)=0.990, text "The animal is a dog ... Dogs typically have
   four legs" to EOS, coherent. legs C=1.0 ant: first `6`, p(6)=0.963, "The ant ... six legs".
   legs C=1.5 both clean. So digit AND identity transfer at C=1.
2. legs C=2.0 dog: first `2` (p(4) drops to 0.491), text "Dogs typically have four legs, not
   two" -- digit over-shoots past target while identity stays dog. Reproduction of the `2`.
3. prop-dog C=2.0: first `No`, but text "The animal that spins webs is a dog ... Dogs are
   mammals", answered `No` to "is it a mammal". prop-dog C=1.0 also `No`. prop-dog stays `No`
   at every C.
4. prop-ant C=1.0 and C=1.5: first `Yes` (correct: ant has antennae). prop-ant C=2.0: first
   `No`, r2=0.370 (loop). So prop-ant DOES transfer at C=1 but reverts at C=2.
5. Mirror property (eight-legs; source spider=Yes, target ant=No): C=2.0 first `Yes`
   (source-correct), text "the ant ... possesses eight legs". Answer head returned
   source-correct `Yes`, not target `No`.
6. Property Yes/No answer-position logits: p_source and p_target are ~0.000 for every
   property cell (dog and ant, all C). The yes/no logits are degenerate at the answer position.
7. Hook-coverage pre-check: the property answer token (Yes/No) is the first token generated
   after the prefill. The hook patches prefill last-3 and decode last-1. Tokenizing the
   property prompt, the prefill last-3 decode to `['Answer',':', ' ']` (positions 41,42,43,
   content_end=44). So the answer token at content_end IS inside the patched window; the patch
   is applied (C=2.0 cell perturbation_norm 25.7, steer != Base). The source-binding is NOT
   because the answer position is unpatched.
8. Naming (912): both animals named coherently at C=2. In-span random dog at C=1 gives digit 4
   but text "a domestic cat" (quadruped/cat prior), ant stays spider. So the dog digit readout
   is generic; dog identity requires the real delta.

Constraints: source prompt unchanged; continuous steering; one rule both animals; dev
prompts only; no reserved strings; one-at-a-time. The yes/no answer head is the open problem.

-- PI/[k3]
