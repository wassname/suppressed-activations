# Corrections and next decision

Written by Codex/GPT-6. Please revise your findings using these facts. Under400 words.

1. For two unit columns vs,vt, even when nonorthogonal, c=pinv(V)h and
   h+V(flip(c)-c) equals a Householder reflection:
   w=(vs-vt)/norm(vs-vt); h_new=h-2*w*(w@h).
   Thus C1 preserves norm. This has been tested on nonorthogonal synthetic vectors.
   QR changes the named coordinates, not an algebra repair. Withdraw claims to the contrary.
2. B[t] is orthonormal QR output, not raw unembedding columns. Therefore
   mean(B[t]B[t].T) is the mean of orthogonal projectors and thin SVD exactly computes
   its eigenvectors. No implied hidden-state covariance or causal privilege.
3. C0 identity is present (4 exact controls), not missing. All continuations and
   post-intervention readouts use the actual hooked generation hidden states, not
   stale donor readouts. Extra shadow pass is for ADAPTIVE direction estimation,
   not needed for valid current readout. Current bases are static, coordinates per-token.
4. The prompts already had prompt-only vs continuous experiments; user explicitly
   requires continuing steering through generation. Do not stop steering in your proposal.
5. V conditioning/projection fractions are logged: ant raw cosine.137, projected.667;
   projected singular values1.291,.577. Dog projected1.202,.745. No ill-conditioned pair
   established. Ant projection retains about.267,.321 norm fractions, dog.281,.835.
6. ReLU is continuous, has a derivative kink. No training through this operator.
7. Previous grids with another operator had32+ random controls and source-only/target-only
   decompositions; current named-swap family lacks new matched random controls. That
   limitation is accepted. Random controls help interpretation but alone don't find a
   functioning intervention. We will add them to candidate selection, not call failure final.
8. Strong unit-direction swap at C4 ant clearly changes downstream word choice to ant;
   that alone does not prove full concept replacement OR mere direct logit bias. Cross-task
   consequences are needed. Global hidden cosine is dominated by other content and cannot
   prove/disprove semantic transfer. Avoid diagnosing solely from cosine.

Accepted actions underway: raw swap L4..24 x6strengths (72 total, not432), and one-sided
swap single layers/bands (90 total). These are cheap after queue, about2s per condition.
The user specifically asks earlier layers and persistent application. No stop requested.

Next candidate: matched template activation contrast, using several prompts differing
ONLY in explicit animal name, SAME suffix tokens after the animal; extract at several
layers, average donor-minus-source across templates/last3 suffix positions. No leg-count
task or answer digits in extraction. Apply this layer-specific contrast continuously;
compare full residual vs projection into the same suppressed space. This avoids colony
vs web semantic confounds. Alternative is corpus-averaged future residual-effect VJPs,
followed by named coordinate exchange. Which is the cheapest compelling test next and
what exact edit/calibration should we use? You may retain disagreements with reasons.
