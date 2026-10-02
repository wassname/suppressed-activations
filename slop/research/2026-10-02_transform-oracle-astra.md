## Assessment

The most diagnostic observation is that **removing more final-layer predictions deletes the English hidden word**. “Not said” is not equivalent to “unlikely at the output”: an intermediate concept can remain output-compatible. Together with frequent spoken-answer intrusion, this favors **role-conditioned readouts**, not generic suppression of late-layer content. The punctuation-dominated variance directions independently suggest that generic WikiText covariance measures the wrong distinction.

I would test these three constructions, in order. Each produces a fixed readout after offline fitting; none uses language identity at inference.

### 1. Contrastively supervised hidden-versus-spoken readout

**Construction.** Generate a few hundred training chains with known intermediate and final words, including varied task templates. Cache normalized residuals \(x\) at the final prompt position, initially at layers 27–29. Fit a low-rank residual adapter \(A=I+UV^\top\) before a frozen lens \(L\), with scores \(s=L(Ax)\):

\[
\mathcal L=-\log p_s(h)+\lambda[m+s(o)-s(h)]_+.
\]

Here \(h\) is the intermediate target and \(o\) the spoken target. Include matched tasks where the same vocabulary items occupy different roles. This uses **semantic-role supervision offline**, not language labels.

**Rationale.** It directly trains the distinction missing from the current objective: intermediate versus final answer, even when both are English. The adapter is more constrained than a fresh vocabulary classifier.

**Cheap falsification.** Hold out both templates and intermediate entities. Compare with the frozen lens and a shuffled-role-label control. Improvement only on familiar templates/entities would indicate memorized task structure rather than a reusable hidden-content transform.

### 2. Remove a paired, task-specific output subspace

**Construction.** Build prompt families sharing an intermediate answer while requesting different final attributes—for example, identify Sweden implicitly, then ask for its capital versus currency. At one layer, estimate within-family differences:

\[
D=\operatorname{Cov}(x_{g,j}-\bar x_g),\qquad
P=I-U_rU_r^\top,
\]

where \(U_r\) contains the leading eigenvectors of \(D\). Read \(L(Px)\); sweep small ranks such as 1, 4, 16 and 32. Fit on varied paired tasks, not generic text.

**Rationale.** These directions are candidates for final-answer/task variation while the intermediate entity is held constant. Unlike final-token blacklisting, projection need not erase a hidden word merely because it is output-plausible.

**Cheap falsification.** On held-out families, measure hidden recall and spoken intrusion separately against random rank-matched projections. Reject if spoken suppression costs comparable hidden recall. Important confound: within-family differences also encode instruction wording; paraphrase controls are essential.

### 3. Learn a fixed cross-layer contrast

**Construction.** Fit

\[
z=\sum_{\ell\in\{22,25,27,29,32\}}B_\ell\,\mathrm{rms}(h_\ell),
\qquad s=L(z),
\]

using strongly regularized low-rank \(B_\ell\) and the role objective above. Cache all layers in one pass per training prompt.

**Rationale.** An intermediate may survive as a distributed state change without its individual vocabulary logit rising and falling. A learned cross-layer contrast can distinguish these trajectories without assuming disappearance by layer 32.

**Cheap falsification.** Compare against an equally parameterized single-layer adapter on identical held-out splits. No gain means the trajectory hypothesis lacks practical support.

## Framing and scoring

The brief does not establish that the designated intermediate is actually computed as a discrete word; alternative reasoning routes remain possible. Evaluate hidden recall, spoken intrusion, and input intrusion separately, with prespecified tokenization and alias rules. Tiny English sets and layer/rank selection warrant a fresh holdout. Finally, supervised English role fitting should be reported separately from **translation-only transfer**: success on the former does not establish the latter.

— OpenAI (Pi)