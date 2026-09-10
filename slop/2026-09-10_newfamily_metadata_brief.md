Mode: independent scientific brainstorm.

Reconstruct the situation from the supplied evidence. Propose distinct mechanisms,
including an implementation error, an objective or gradient mismatch, and an unintended
learning dynamic when relevant. For each, give a falsifiable prediction and the cheapest
discriminating check. State what is observed versus inferred. Do not choose a winner.

Question: The span-correction subspace is built from an identity/prose template contrast
(dog/ant vs spider prose, peak L20 / output L32 attenuation). It reliably transfers animal
identity and the numeric legs answer, but NOT the yes/no property answer. Is the problem
that the subspace should be built from a contrast that includes the Yes/No answer tokens
(the ` Yes`/` No` unembedding rows), not just the identity prose? Propose the construction
change, and what cheap test distinguishes it from an alternative cause.

Full evidence chain:

1. C-sweep legs (digit): peaks at C=1.0-1.5 (dog 4 p_tgt 0.99, ant 6 p_tgt 0.96), degrades at
   C=2.0 (dog -> 2, p(4) 0.49 = overshoot). C=1.5 reliable operating point for naming+legs.

2. naming C=1.5: dog+ant coherent identity. naming C=1.0: dog OK, ant FAILS (stays spider).

3. property source-binding: prop-dog stays ' No' at EVERY tested C (p(No) 0.30->0.39->0.39;
   p(Yes) 0.066->0.208 at C=2 but No 0.388 still wins). prop-ant transfers at C=1.0
   (' Yes' 0.297 edges No 0.263) but reverts at C=2.0 (No 0.333).

4. M2 projection ratio (real model): ||U U^T d_answer|| / ||d_answer|| where
   d_answer = unembedding( Yes) - unembedding( No): dog 0.0326, ant 0.0410. Near-zero for
   both, ant > dog. So the yes/no decision direction is ~3-5% inside the identity-prose
   U-span. The patch moves identity/prose (near-in-span) but barely touches the yes/no
   decision (out-of-span).

5. M3 attention (eager attention, task 930): answer-position attention row at the first
   decode step attends to {43,42,41}=patched 'Answer',':',' ' AND {28,30,27}='Question',' Is'.
   So the answer head DOES attend to the patched Answer: region, yet ' No' stays dominant.
   Not pure-M3 (head doesn't ignore the patch).

6. in-span random control: dog delta random in-span -> digit 4 but text "domestic cat"
   (generic quadruped/4-legs prior); ant random in-span -> stays spider. So the dog digit is a
   generic readout; ant digit is direction-specific. In-span random at C=2 dog -> 4, text cat.

7. legs-ant-C2 (919) fully correct; legs-dog-C2 digit 2 (overshoot). property yes/no logits
   (specific-token p_source/p_target) degrade to ~0.000 but the actual top-k No/Yes
   distribution is informative (moves with C).

Constraints: source prompt unchanged; continuous steering; one rule both animals; dev
prompts only; no reserved strings (spinneret, limb-count, live-birth frozen); one-at-a-time.
The property source-binding is the last open goal-1 failure; the answer direction is nearly
out-of-span (M2), so the framing question is whether the construction should include answer
behavior in its contrast.

Request: propose the construction change (or argue the answer must leave the identity
subspace), a cheap discriminating test, and the falsifiable prediction. Also state whether
the ~5% ant > dog M2 gap is actionable or noise.

-- PI/[k3]
