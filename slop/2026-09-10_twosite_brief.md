Mode: independent scientific brainstorm.

Reconstruct the situation from the supplied evidence. Propose distinct mechanisms,
including an implementation error, an objective or gradient mismatch, and an unintended
learning dynamic when relevant. For each, give a falsifiable prediction and the cheapest
discriminating check. State what is observed versus inferred. Do not choose a winner.

Question: A single-layer edit cannot carry the property yes/no answer (L20 alone: the answer
direction is only ~5-10% in-span and barely displaces the answer residual; L26 alone: it
corrupts the limb-count answer, generating a bone-count confabulation loop (`154`) instead of
the target digit `4`, and does not yield a clean property answer). A TWO-SITE edit is
proposed: the identity/limb-count span-correction at L20 (verified working) PLUS an
answer-direction patch at L26 using the property-prompt d_act direction (target minus source
answer-position residual at L26, where the valid H2 showed the answer identity forms). Is the
two-site construction principled and cheap enough to try before freezing, or should property
binding be judged out of reach and the rule frozen to naming+limb-count now? Also: prop-ant-L26
gave clean ant identity with a wrong numeral answer (`1` not Yes); is a C-sweep at L26 for ant
alone worth one more job?

Evidence chain (span-correction family, Qwen/Qwen3.5-4B rev 851bf6e806):

1. Frozen-rule candidate: L20 span-corrected delta, C=1.5, prefill last-3 + decode last-1.
   Verified clean for naming+legs BOTH animals (dog `4`/dog text, ant `6`/ant text; naming
   whole-name to EOS).

2. Property source-binding at L20: prop-dog stays ` No` at EVERY tested C (top-k p(No) 0.30
   to 0.39, p(Yes) 0.066 to 0.208 at C=2 but No still 0.388). prop-ant transfers at C=1.0
   top-k (` Yes` 0.297 edges No) but reverts at C=2; H5 ant C=1.0 first Yes but prose stays
   SPIDER (answer-movement without identity persistence).

3. Corrected (non-circular) d_act ratio: dog 0.0965, ant 0.0488 (yes/no answer direction is
   only ~5-10% inside the L20 U-span). cos(delta, d_act): dog 0.075, ant 0.032. Displacement
   of the L20 answer residual along d_act: dog 0.14, ant 0.066 (barely toward target).

4. Valid H2 per-layer decodability (fixed probe): the target-vs-source answer identity grows
   progressively and is strongest at L23-28, not complete at L20. |dog: L20 +3.13, L23 +7.21,
   L28 +13.54 (peak), L32 +5.87. ant: L20 +1.66, L23 +4.21, L28 +6.79 (peak), L32 +3.94.|

5. M3 eager-attention (task 930): answer head attends to BOTH patched Answer:/space AND the
   Question/Is tokens. H5 (patch Question/Is in addition to last-3 at L20): prop-dog still
   ` No` (position set NOT the culprit for dog).

6. L26 test (935): prop-dog-L26-C1.5 self-contradicting loop ("No, the animal that spins dogs
   is not a mammal. The animal that spins dogs is a dog, which is a mammal."). prop-ant-L26-C1.0
   first `1` (numeral, not Yes) but coherent ANT-identity prose (cleaner than H5's spider-stuck
   ant). legs-dog-L26-C1.5 BROKE (bone-count loop `154` instead of `4`).

7. Unknown: no two-site (L20 + L26) test has been run. The L26 d_act direction (target minus
   source at L26) is available from the property prompts and is exactly where the answer forms.

Constraints: source prompt unchanged; continuous steering; one rule both animals; dev prompts
only; no reserved strings; one-at-a-time. The two-site edit is the untested composition.
Assess: is it principled/cheap, or justify freezing.

-- PI/[k3]
