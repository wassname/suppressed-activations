# Next bounded proposal: change output-removal geometry, not its strength

— PI/OpenAI. Prospective specification after2720 cached diagnosis. Same-family mathematical review found no blocker. Implementation and CPU checks are in progress; no pretrained candidate result.

User goal: frozen language-independent readout that finds hidden concepts while excluding input/output; equal plain controls. Current-input generation stays one pass. Generated text/gold aliases never choose masks/directions; only the original final-prefill greedy ID is used. V5 remains reserved. No universal multilingual-purity or baseline-dominance acceptance gate.

Observed2720: boundary J apple rank6 vs final314 after half-erasure. Boundary autumn28→71 and winter-equivalent冬季10→51 under erasure. At final, :red rank17 and红色 rank9 survive; masks are actually applied, but strip whitespace/case only. Thus pointwise endpoint max can restore speech leaks. A synonym filter is not appropriate globally: English cloud is the intended target even though it translates the spoken French/German word. Diagnostic: out/2026-10-01_160911_boundary-readout/output_variant_diagnostic.json.

Question: does the Euclidean metric in transported output space cause avoidable collateral suppression? Change the direction of the correction while keeping the same half-reduction of the greedy output coordinate. Do not change positions, k, masks, aliases or model.

Let h be the current captured state, J the frozen transport (identity for plain), G the diagonal final RMSNorm gain, y=norm(Jh) the current normalized readout, and w the greedy output-token embedding. Define B=GJ. Treat the current RMS scale as fixed for this correction; its scalar cancels. This is NOT differentiating the complete RMS-normalized network or rerunning norm after editing.

Existing output-space correction:

    c = 0.5 * dot(y,w)
    delta_old = c*w/dot(w,w)

Candidate:

    a = B.T @ w                 # pre-RMS output-numerator gradient
    v = B @ a
    delta_new = c*v/dot(v,w)
    scores = head(BF16(y-delta_new))

For J, compute v=G*(J@(J.T@(G*w))) with matrix-vector products; no dense extra B/K, model backward or fitting. For plain24/27, v=G²*w. Under the held-scale linear map, delta_new is induced by the minimum-native-residual-norm correction satisfying the same output-coordinate constraint. Do not claim exact minimum change through recomputed RMSNorm/BF16. Both corrections remove c from y·w before casting. New output-space norm cannot be smaller than the old minimum-Euclidean correction (in real arithmetic); no orientation-only attribution from this comparison alone.

Primary J matched control: one shared CPU float32 standard Gaussian vector r (`torch.Generator(device='cpu').manual_seed(0)`), moved to the direction's device/dtype and projected orthogonal to w:

    base = w/dot(w,w)
    extra = v/dot(v,w)-base
    u = unit(r-base*dot(r,w))
    delta_random = c*(base+norm(extra)*u)

Zero output embedding, zero gradient sensitivity or zero projected Gaussian norm rejects the run explicitly; no fallback/0÷0. Zero extra requires no normalization and yields the original correction; c=0 yields zero correction when sensitivity is nonzero. This matches the primary candidate's requested output-space norm AND output-coordinate removal, not native norm, BF16-realized norm or score-space behavior. Save both. Plain candidates are equal-operator comparators; no per-case method promotion.

One run through08: same six development cases, same three positions (final/boundary/preclue), candidate J/plain24/plain27 plus primary-J matched random, all existing180 rows preserved. No aggregation. Existing same-pass captures can be recaptured with exact generation/final-state/180-row parity; at most192 generated tokens, normally15, no input-specific preparatory pass. Preclue uses future masks/output direction, as before. All raw scores/deltas, output-coordinate errors, realized/requested norms and complete lists saved.

Before run: synthetic nonidentity-J tests of target-coordinate equality, native minimum-norm solution, orthogonal-J/G=I equivalence to old erasure, scale invariance, random norm/coordinate matching, and BF16 traces; actual tiny main pipeline seeds0/1. Observe all cases/heads, not only apple/autumn. Candidate gains tied by random or appearing at preclue weaken a geometric explanation. Stronger hidden ranks with more output leakage are not success. Failure retires this exact candidate, not every possible representation geometry.

Alternative not chosen: increase strength, union endpoints, or broaden masks. They confound the location/suppression problem or revisit prior settings. Main risk here: B's anisotropy could magnify irrelevant directions; logging the correction norm and matched random separates this from mere implementation failure. This test will not establish necessary reasoning or coherent causal editing.
