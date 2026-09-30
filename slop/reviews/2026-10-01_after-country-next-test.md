## Inherited decisions
Country editing failed **0/2 properties**, despite valid Base answers and verified coordinate exchange. The checker now passes, with maximum requested-state reconstruction error \(2.82\times10^{-7}\); it does not independently verify full-output probabilities or semantics. Retire this setting and all previously retired candidates.

The user permits an honest demo plus “works X%.” Our7/8 screen was an advancement heuristic, **not a prerequisite for reporting partial findings**. Existing geography-limited English evidence can be reported with its denominator and limitations. No prior gate is reopened; both goals remain open.

## Diagnosis
Pair coordinates need not constitute the country representation. Likewise, independently ranking correlated vocabulary directions need not recover a useful feature inventory.

The supervisor approved **one nonnegative matching-pursuit readout attempt**: subtract already-explained components before selecting subsequent atoms. This is our specified algorithm, not a reproduction of the paper’s gradient pursuit or causal clamping.

## Recommendation: frozen contract

**Scope:** cached v4 states from2637; final-position residual24 J primary. One ≤300-second local job,15-second kill grace, **zero transformer forwards or generations**. No fitting, layer/window/strength search, or alternate-winner promotion.

For every vocabulary token \(t\), form
\[
v_t=J_{23}^{\top}\operatorname{diag}(1+\mathrm{norm.weight})W_t,\qquad
d_t=v_t/\|v_t\|.
\]
Zero-norm columns are ineligible; log their IDs/count. Abort on nonfinite values; do not truncate merely small norms.

Initialize \(r=h,\ a=0\). For at most32 steps:
1. Choose maximal \(d_t^\top r\), breaking ties by token ID.
2. Stop if that maximum is nonpositive.
3. Add the positive maximum to \(a_t\), then subtract that amount times \(d_t\) from \(r\).

Repeated atoms are allowed. Decompose using the **entire eligible vocabulary**, without prompt, output, language, or label filtering. Afterwards apply unchanged prompt and greedy-final-token masks. Return only positive accumulated coefficients, descending, at most32—never inactive zero ties.

**Controls:** identical plain24/plain27 pursuit using normalized effective unembedding columns without J. For each case/representation, compare equally masked raw and unit-dot rankings at that pursuit’s postmask cardinality \(n\); if \(n=0\), controls return empty lists. Retain existing full32 and best-incumbent comparisons. Cardinality controls prevent shorter lists masquerading as improved exclusion.

**Specificity diagnostics, not selection inputs:** retain the third-question-token control. Additionally run J pursuit immediately before these frozen identifying spans:

`Christmas Day`; `Thor`; `deciduous trees shed their leaves`; `poisoned in the story of Snow White`; `played by Sherlock Holmes`; `Danish prince asks 'To be, or not to be'`; `lightest chemical element`; `formed by joining three non-collinear points`.

Require each span to occur once. Select the last token ending at or before its start; assert no clue characters are included. Normalize any coefficient comparisons by the original state norm.

**Scoring/evidence:** preserve frozen aliases and eight-case denominators. Recovery requires actual returned-set membership. For AUROC, masked or inactive coefficients rank at \(-\infty\); ties receive0.5, with existing undefined-case rules and denominators retained. Save selected atoms, coefficients, residual norms, masks, cardinalities, diagnostic positions, and reconstruction evidence.

**Prospective advancement:** positive net paired joint-count gain over J’s cardinality-matched unit-dot control, plus at least one semantically reviewed new recovery absent from both diagnostic inventories but present at final. Review affected baseline cases/losses symmetrically. Report all plain/incumbent comparisons even if this criterion passes.

This establishes, at most, **temporal clue association**, not counterfactual necessity or superiority to every baseline. Only after this new numerical/semantic contract passes may frozen v5 be considered.

## Risks / need from main agent
Correlated atoms may still encode lexical priors; greedy decomposition may miss distributed features. Scope is settled. No implementation performed; no further scientific branch proposed.

— **PI/OpenAI**