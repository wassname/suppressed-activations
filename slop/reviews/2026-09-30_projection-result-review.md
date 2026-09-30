## Independent read-only audit

Run directory **R = `out/2026-09-30_172257_jlens-one-pass/`**. Same-family review, not goal sign-off.

**Observed:** `R/run.md` reports “Candidate brackets: 2/8; raw: 0/8; candidate ordered: 7/8.” `R/result.json` additionally records raw ordering 8/8. The contract in `slop/reviews/2026-09-30_context-invariant-coordinate-decision.md` requires **8/8 brackets**, not ordering. `R/pipeline.json` has `"passed": false, "causal_runs": []`; `R/console.log` explicitly reports no causal generations. The launcher’s failure branch implements that gate.

### Top findings

1. **Projection does not merely repair offsets.** For `field-explicit-1`, `R/result.json` records raw gap **+0.165381**, projected gap **−0.038734**, with dog **+0.013418**, spider **−0.025316**. Projection reverses this pair. Thus neither a shifted cutoff nor “preserved semantic ordering” rescues these observed coordinates. Semantic-information removal is plausible, not established; context-dependent interactions also fit. Independent tensor reconstruction of this pair could disprove a reporting/scoring explanation.

2. **Training invariance is not transferable validity.** `R/source.py:nuisance_coordinate` uses `basis = Vh[:7]` on eight centered means, then removes their span. `R/run.md` reports training brackets 8/8 and midpoint error `1.1920928955078125e-07`; midpoint invariance is constructed, while bracket signs additionally require preserved orientation. Retained norm **0.983892** does not certify semantic preservation. The new-context failure rejects this frozen candidate’s gate—not nuisance projection generally.

3. **Checker “PASS” has narrower coverage than its label suggests.** `slop/audits/2026-09-30_check-projection-run.py` independently uses least squares, checks saved-source/config bytes against commit `4348227`, preparation hashes, basis algebra, all-position margins, bracket flags and gate consistency. `R/verification.json` reports maximum margin reconstruction error **1.0573e−6**. However, the checker trusts saved activations and recorded forward counts; it does not retokenize prompts, authenticate model execution, enforce unique/exhaustive sample/pair identities, or recompute reported ordering counts and pair-margin fields. Its causal loop is empty here; no causal coverage was tested. These are audit limitations, not demonstrated corruption.

No executed-path implementation defect was established. Bracketing could reflect lexical/context discrimination without finding suppressed thought; no generation, readout benchmark, causal transfer, or general semantic claim follows.