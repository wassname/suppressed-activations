## Verdict

**Worth one bounded development test after the cached leak diagnosis; no mathematical blocker found.** This is a defensible alternative metric, not yet a mechanism for separating thought from speech.

### Algebra and implementation alignment

In `slop/research/2026-10-01_output-erasure-geometry.md`, “minimum-native-residual-norm” is correct **conditional on held scale**. Write \(y=sBh\), \(a=B^\top w\). The constraint is \(s\,a^\top dh=c\); its minimum-norm solution is
\[
dh_*=\frac{c\,a}{s\|a\|^2},\qquad sBdh_*=\frac{cBB^\top w}{\|B^\top w\|^2}.
\]
Thus the proposed correction follows, provided \(a\neq0\). If \(a=0\), a nonzero constraint is infeasible; zero correction is appropriate when \(c=0\), rather than evaluating \(0/0\).

The source orientation agrees: `scripts/english/08_jlens_one_pass.py:1333` uses `"h[-1].float() @ J.T"`, so column notation is \(Jh\), and \(BB^\top w=GJJ^\top Gw\). Plain heads correctly give \(G^2w\), not \(Gw\).

The existing correction at lines1336–1341 projects the normalized state and then casts before the head. Lines676–686 similarly normalize transported states before erasure. Neither window establishes exact differentiability through casts; the proposal appropriately disclaims it.

### Main challenge: smaller native change is not less semantic collateral

The proposal acknowledges “New output-space norm can be larger.” More strongly, **it cannot be smaller**:
\[
\|\delta_{\rm new}\|^2
=c^2\bigl(\|w\|^{-2}+\|\mathrm{extra}\|^2\bigr)
\geq\|\delta_{\rm old}\|^2.
\]
Old erasure is already minimum output-Euclidean change. The candidate exchanges that guarantee for minimum native change. Nothing supplied establishes native Euclidean distance as semantic preservation. For any other token embedding \(t\), its score change is \(-t^\top\delta\); neither method guarantees less collateral suppression.

Affected inputs are all cases whose candidate has nonzero orthogonal extra. Evidence against the collateral hypothesis would be candidate gains accompanied by worse leakage, random-control ties, or similar preclue gains.

### Matching and numerical caveats

The proposed random control exactly matches requested norm and \(w\)-coordinate removal in real arithmetic: both `extra` and \(u\) are orthogonal to \(w\). Specify the random distribution; seed0 alone does not define it. Handle zero projected random norm and zero `extra` explicitly.

It does **not** match native norm, vocabulary-score perturbation, or BF16-realized correction. One shared random draw is a useful falsifier, not a reliable null distribution. BF16 can break coordinate equality and requested norm matching; the source assertion precedes the head cast. Requested-versus-realized traces are therefore essential, especially for near-zero denominators.

### One next action

Perform the proposed single six-case, three-position development comparison, after its synthetic and tiny-pipeline checks, preserving all180 existing rows. The discriminating observation is improved hidden readout without increased speech leakage, interpreted against matched random and preclue—not a new acceptance threshold.

Observed evidence is the proposal and source windows only; implementation, raw diagnostic artifacts, timings, and test results were not verified. Existing partial positives remain; v5 stays unrun and goals open.