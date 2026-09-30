## Inherited decisions

Both goals remain open: English hidden-thought readout and coherent, strictly one-pass editing. Offline preparation is allowed; a preliminary current-input pass is not. Retired configurations stay retired. v5 remains unused. Honest partial results remain reportable; neither 7/8 nor dominance over every baseline is required.

## Diagnosis

2657 completed successfully. Matching pursuit recovered **3/8**, versus **4/8** for cardinality-matched J unit-dot ranking, with no paired gains. Mean AUROC fell to .515. The checker covered 40 decompositions, 168 previous rows and 120 new rows, but did not independently establish full-dictionary greedy optimality or semantics.

The executed `nonnegative_matching_pursuit` only adds coefficients; it never revises previous allocations. December’s first selections were January (4.56529), then Months (2.82582). Correlated directions can therefore receive overlapping credit, distorting subsequent selection. Violin already appears before its identifying clue, so retaining it is not new clue-specific evidence.

## Drift / contradiction check

The paper specifies sparse nonnegative **gradient pursuit**. The public `lens.py` implements Jacobian transport/readout, not that solver; the supplied repository inventory contains no corresponding pursuit implementation. Neither prior matching pursuit nor coordinate swaps tested this algorithm. The proposal below is a specified interpretation, **not a faithful reproduction claim**.

A better reconstruction alone would be another diagnostic, not progress toward hidden-thought recovery.

## Recommendation: one active-coefficient gradient-pursuit test

Use the same eight cached v4 cases, full-vocabulary unit dictionaries, J24 primary, k=32 maximum iterations, masks and numerical precision. No new inference, generations, calibration, pooling or erasure. Retain the fixed early-prefix and pre-clue positions.

For dictionary columns \(D_t\), approximate \(h\) by \(Da\), minimizing \(\frac12\|h-Da\|^2\), subject to nonnegative sparse coefficients.

Initialize \(a=0,\ S=\varnothing,\ r=h\). Repeat at most 32 times:

1. Compute \(g=D^\top r\). Add the largest strictly positive \(g_t\) outside \(S\), if one exists; break ties by token ID.
2. Form the feasible restricted gradient:
   \[
   q_i=
   \begin{cases}
   g_i,&i\in S,\ a_i>0,\\
   \max(g_i,0),&i\in S,\ a_i=0,\\
   0,&i\notin S.
   \end{cases}
   \]
3. Stop if \(q=0\). Otherwise let \(p=Dq\), and take
   \[
   \alpha=\min\left(
   \frac{r^\top p}{p^\top p},
   \min_{q_i<0}\frac{-a_i}{q_i}
   \right),
   \]
   with the empty minimum equal to infinity.
4. Update \(a\leftarrow a+\alpha q\); set boundary-hitting coefficients exactly to zero; recompute \(r=h-Da\).

Keep selected indices in \(S\), including zero coefficients. Thus each iteration adds at most one direction and performs exactly one restricted gradient step. This is neither NNLS convergence nor OMP’s full least-squares refit.

Abort on nonfinite values, nonpositive line-search numerator/denominator with nonzero \(q\), or materially negative coefficients. Permit only rounding-sized corrections, bounded by \(32\epsilon\max(1,\|a\|_\infty)\). Abort if reconstruction error increases beyond \(32\epsilon\max(1,\|h\|^2)\); stop if the update leaves coefficients unchanged. Save every selection, coefficient revision and residual norm. These are numerical rules, not performance thresholds.

Apply masks only after decomposition. Rank positive coefficients divided by \(\|h\|\); return no zero-coefficient fillers.

**Mechanism:** revising earlier coefficients changes the residual used to select later words. It could undo shared month/answer allocations and expose a specific hidden month. This is a testable possibility, not an explanation established by December.

**Strongest alternative:** vocabulary directions reconstruct surface associations and nuisance variation rather than hidden concepts. Prediction: reconstruction improves but semantic joint recovery and clue association do not.

### Comparisons and decision

Run identical gradient pursuit for plain24/plain27. For each representation, retain matching pursuit, raw-dot and unit-dot controls truncated to the candidate’s returned cardinality, plus their full32 results and existing incumbents. Report all eight cases, expected-answer subset, joint counts, AUROC and unchanged semantic limitations. No control becomes the primary method.

Prospectively advance only if J gradient pursuit has positive net paired joint gain over its cardinality-matched unit-dot control **and** a reviewed new recovery relative to matching pursuit that is absent from both unmasked diagnostic inventories. Review gains, losses and input/output leakage symmetrically. Residual improvement alone fails. Failure retires this solver configuration without tuning.

Use one normally queued local-GPU job: **300 seconds plus 15-second kill grace**, including startup. v5 is not part of this job.

## Risks / need from main agent

Repeated v4 use is development, not generalisation. Nevertheless, this bounded test isolates an untested paper-grounded mechanism; new matched-output data alone would not improve the method. A positive result justifies considering fresh evaluation, not further v4 optimization. Editing remains a separate unresolved goal.

Supervisor confirmed readout-only scope. No executor handoff or run authorization is issued here.

— PI/OpenAI