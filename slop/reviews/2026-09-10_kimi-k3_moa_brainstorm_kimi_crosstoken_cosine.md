---
requested_model: moonshotai/kimi-k3
max_tokens: 4000
final_tokens: 20000
reasoning_effort: low
input_bytes: 4758
trace: /workspace/2026/suppressed-activations-batchwork/slop/reviews/2026-09-10_kimi-k3_moa_brainstorm_kimi_crosstoken_cosine.trace.jsonl
generated: 2026-09-10T07:06:04.029968+00:00
---

# bounded completion

## First call reasoning

Let me reconstruct and answer. Need to give mechanisms including implementation error, objective/gradient mismatch, unintended learning dynamic, each with falsifiable prediction and cheapest check. Answer questions 1-5. State observed vs inferred. Don't choose winner... actually the system prompt says "state the decision, strongest objection, next check" but the user says "do not choose a winner." I'll give a recommendation-lite framing: decision on cheapest next check perhaps. System prompt says be skeptical, state decision, strongest objection, next check. The user says don't choose a winner among mechanisms — I can comply with both: state a decision on what to do next, not which mechanism is true.

Observed vs inferred:

Observed:
- token_persistent_subspace = thin SVD of stacked per-token orthonormal bases → eigenvectors of average projector; persistence = σ²/N; sign-invariant.
- Fixed rank-1 run: source_remove strong, combined weaker, donor_add ~0. Continuation still says spider.
- L20 answer-position residual identical between dog property pair and spider (diff 0.000) in at least one check.
- Intervention over 32 generated tokens.

Inferred:
- Removal moves log-odds but doesn't transfer identity → removing source-suppressed direction ≠ adding donor content.
- Identical L20 residual suggests either intervention isn't reaching that layer/position, or edit cancels, or measurement at wrong site — possibly implementation error.
- Combined < source_remove suggests donor_add direction partially undoes removal (antagonistic directions within subspace).

Mechanisms:

A. Implementation error: edit applied at wrong positions/layer, or donor direction computed from mismatched position alignment; evidenced by diff norm 0.000 at L20 answer position. Prediction: logit-lens on edited run shows no perturbation propagated; check: compare residual diff at intervention layer immediately after edit — should be nonzero; if zero at intervention layer itself → code bug.

B. Objective/metric mismatch: avg-projector selects span, not signed direction; two tokens can share a subspace while their c_p point opposite; rank-1 SVD sign is arbitrary per token, so donor_add may inject a direction whose sign is wrong for transfer. Prediction: c_p cosines across positions are bimodal (±) while principal angles are high. Check: compute signed cosines; if |mean cos| ≪ mean |cos| → sign instability, need sign alignment.

C. Unintended learning/dynamic: suppression subspace encodes a generic "suppress the currently-true concept" gating direction, position-dependent nuisance (e.g., syntax/article direction), so removal just un-suppresses noise; identity lives elsewhere (attention-mediated, or MLP). Prediction: removing the subspace in a control prompt with no suppressed concept also shifts log-odds; check: apply same remove to a matched non-animal prompt.

D. Single dominating token / shared mean: cosine agreement driven by one position with huge ||c_p|| or by shared mean component. Prediction: cosine agreement collapses after mean-centering c_p and after dropping max-norm position; check: recompute.

E. Donor_add null because magnitude mismatch: donor component norm tiny relative to source residual, or direction orthogonal to the readout unembedding for target tokens. Prediction: scaling donor_add by α shows threshold; check: sweep α.

Question 1: Yes genuinely different. Principal angles/avg-projector is sign- and coefficient-invariant — it measures span overlap only. Signed cosine of c_p measures actual vector agreement within spans. Falsifiable prediction: if subspace overlap already captures the reusable direction, then the top principal vector and the mean signed c_p agree (cos ≈ ±1 between mean normalized c_p and first singular vector after sign alignment), and selecting by signed agreement yields no behavioral difference vs avg-projector selection. If signed cosine selects a different direction and the continuation changes (transfers "dog"/"ant" or changes token-level log-odds at answer position), they're distinct. Concretely: compute correlation between cross-token signed cosine of c_p projected onto candidate directions vs persistence ranking; if rank correlation ~1, no new info.

Question 2: Cheapest: reuse existing stored residuals? We don't know residuals stored; but one forward pass per prompt is cheap. Compute per-position c_p, then: (i) mean cosine matrix with sign, (ii) mean-center c_p across positions and recompute, (iii) leave-one-position-out. Also compare against within-prompt shuffled controls: cosine between c_p from spider prompt and c_q from an unrelated prompt (cross-prompt baseline). Discriminating check: if cos(c_p,c_q) high within prompt but equally high across unrelated prompts → shared mean/syntax, not concept. Cheapest discriminating check overall: mean-center and compare to cross-prompt baseline using residuals from a single forward pass each on ~5 prompts — no generation needed.

Question 3: Alternative explanations for identity not transferred: (a) edit magnitude insufficient — log-odds shift of 6 was for digit; identity readout needs larger or different layer; (b) intervention at wrong layer for identity (identity encoded at later layer or via attention patterns, not residual at peak suppressed layer); (c) donor_add direction has wrong sign (sign-invariant selection), actively cancelling — consistent with combined (5.38) < source_remove (6.13); (d) the suppressed subspace is a "don't say X" erasure direction, and the model defaults to the semantically supported answer (spider) from context elsewhere; the residual edit can't overwrite evidence carried by attention from earlier tokens. Control: flip sign of donor_add (should be free, just negate) — if identity transfers with one sign and not the other, sign is the issue, not absence of reusable component. Also control: remove-only plus prompt-level paraphrase. And a "concept present but suppressed" probe: check whether source model's logits for "dog" increase under donor_add even if continuation unchanged.

Question 4: Cheaper/more decisive: sign-flip donor_add (zero GPU beyond existing pipeline, just rerun edit with −d). Norm-of-component breakdown: report ||c_p|| fraction; if suppressed components are <1% residual norm, editing them is implausible to transfer identity. Donor-specific vs generic control: take the same subspace from a prompt pair with no animal (e.g., syntax-matched filler) and edit spider→that; if continuation changes similarly, the effect is generic. Also steering via unembedding: directly test whether B directions have nonzero logit effect on "dog"/"ant" tokens (project onto W_U rows) — pure linear algebra, no GPU.

Question 5 false positives: shared mean across positions; one dominating token (weight cosine matrix by norms); generic syntax position embeddings leakage; rank-1 collapse where all positions project onto the first PC of anything (high anisotropy of residual stream — random vectors have high cosine in high-dim anisotropic space); autoregressive carryover — later positions' residuals contain earlier content, so agreement reflects copy not concept; the window (last-3 prefill) positions may all attend to the same token. Null: random direction baseline cosine distribution in same subspace dims; rotate B_p by random orthogonal within residual space.

Also gradient mismatch: objective used log-odds of digit token p(6); the intervention objective (identity transfer) is different — optimizing digit log-odds doesn't constrain the continuation. That's an objective mismatch worth listing: metric mismatch between steering target (answer digit) and evaluation (free continuation).

Structure answer:
- Observed vs inferred
- Mechanisms A–E w/ prediction + cheapest check
- Answers to Q1–5
- Decision (what to do next per system prompt), strongest objection, next check.

Keep reasonably concise but thorough. Use headers and bullets.
## First call answer

# Reconstruction: observed vs. inferred

**Observed (measured):**
- `token_persistent_subspace` = thin SVD of stacked per-token orthonormal bases → eigenvectors of the *average projector*. Persistence = σ²/N. Sign-invariant by construction.
- Rank-1 persistent run: source_remove p(6)=0.79 / shift 6.13; combined 0.67 / 5.38; donor_add ≈ 0 effect. Continuation still self-identifies "spider."
- L20 answer-position residual diff (dog pair vs spider) = 0.000 in at least one check.
- Edit spans 32 generated tokens.

**Inferred (not measured):**
- Removal moves the *digit* logit but not *identity* → the suppressed subspace modulates a readout, not the concept representation.
- Combined < source_remove (5.38 < 6.13) → donor_add is not inert; it partially *antagonizes* removal. That is weak evidence of a sign/alignment problem inside the selected direction, since the selector is sign-blind.
- Diff norm exactly 0.000 at a site where an active edit should leave a trace → either the edit never touches that site (implementation), or the measurement site is wrong.

---

# Candidate mechanisms

**M1 — Implementation error.** The edit is applied at layers/positions that don't include the probed site, or per-position donor/source alignment is off-by-one, so donor_add lands on padding or the wrong span. The 0.000 diff is the tell.
- *Prediction:* residual diff at the intervention layer itself, immediately post-edit, is nonzero; at L20 it is zero because L20 is outside the edited span or upstream of it.
- *Cheapest check:* one forward pass, diff residuals at every layer pre/post edit. Pure tensor bookkeeping; no generation. If the diff vanishes at the *edited* layer, it's a bug.

**M2 — Objective/metric mismatch (the user's hypothesis, formalized).** Avg-projector SVD selects a *span*; rank-1 singular-vector signs are arbitrary per token. The actual suppressed components c_p may be anti-aligned across positions, so "donor_add" injects a direction whose sign (or composition) cancels removal — consistent with combined < source_remove.
- *Prediction:* cross-position signed cosines cos(c_p, c_q) are bimodal near ±1 or near 0 with high |cos| principal angles; mean signed cos ≪ mean |cos|.
- *Cheapest check:* compute c_p from existing basis + one forward pass of residuals (no generation); histogram the signed cosine matrix.

**M3 — Objective mismatch at the eval level.** The steering metric is digit log-odds p(6); the evaluation is free-continuation identity. A direction can be optimal for flipping a single answer token while carrying no concept content. Nothing in the selection objective constrains "dogness."
- *Prediction:* logit of "dog"/"ant" tokens under donor_add does not rise even when p(6) shifts.
- *Cheapest check:* read W_U logits for concept tokens under each edit condition from already-computed runs — pure linear algebra on stored logits if saved, else one forward pass.

**M4 — Unintended dynamic: suppression = generic erasure/gating, not concept.** The subspace encodes "suppress the currently-salient answer" (a position- or syntax-conditioned nuisance), shared as a span but not as a signed concept vector. Removing it unleashes the digit but identity is reconstructed downstream from attention over the prompt, which the edit never touched — hence "the animal that spins webs is the spider."
- *Prediction:* the same remove applied to a matched non-animal prompt (no suppressed concept) produces comparable log-odds shifts on its answer token.
- *Cheapest check:* run source_remove on 2–3 control prompts with no animal; compare shift magnitudes.

**M5 — Magnitude/norm failure.** ||c_p|| is a tiny fraction of the residual; donor_add at unit scale is below the readout's detection threshold, while remove works because erasure is asymmetric (killing a suppressor is easier than installing a concept).
- *Prediction:* sweeping donor_add scale α shows a delayed threshold or nonmonotonic (cancellation) behavior.
- *Cheapest check:* α-sweep at 3 scales on one pair.

---

# Answers to the questions

**Q1. Genuinely different?** Yes, mathematically disjoint information. Principal angles/avg-projector are invariant to the *coefficients* — they never see the residual at all, only the bases. c_p cosine uses the actual projected content. Two token positions can have identical spans and opposite c_p. **Falsifiable discriminator:** if the avg-projector already captures the reusable direction, then (a) the top signed-agreement direction coincides with the top persistence direction (|cos| ≈ 1 after sign alignment), and (b) re-selecting the intervention basis by signed agreement produces *no* change in the 32-token continuation vs. the existing selector. Either failing shows the measures differ *and* the difference is behaviorally relevant. Note (a) alone is not sufficient — only the behavioral arm separates "different number" from "different mechanism."

**Q2. Cheapest experiment separating reusable signed component vs. shared-span/different-nuisance.** One forward pass per prompt (no generation) on ~5 prompts: the spider/dog pair plus 3 unrelated fillers. Compute:
1. Signed cosine matrix of c_p within the target prompt.
2. Same after mean-centering the c_p (kills the shared-mean confound).
3. Cross-prompt baseline: cos(c_p^spider, c_q^filler).

Decision rule: reusable signed component ⇒ high *centered* within-prompt cosine that *exceeds* the cross-prompt baseline. Shared span without signed vector ⇒ high principal angles, near-zero or sign-symmetric centered cosines. Generic syntax/mean ⇒ high cosine everywhere including cross-prompt, collapsing after centering. This is strictly cheaper than the proposed intervention-selection experiment and gates it: if centered cosine ≈ baseline, the downstream edit comparison is not worth GPU.

**Q3. Alternative explanation for "digit changes, identity doesn't."** Several, all live: (a) sign error in donor_add (M2) — the combined < source_remove ordering is circumstantial evidence for this; (b) identity is carried by attention over prefill tokens and reconstructed downstream of the edit site, so no residual-only edit at one layer can overwrite it (M4); (c) magnitude threshold (M5); (d) wrong layer for identity even if right for the digit. **Cheapest separating control:** flip the sign of donor_add (negate the donor direction, rerun the identical edit). If one sign transfers identity and the other doesn't, the component exists and the selector's sign-blindness is the whole problem. If neither sign works and the L20 diff is genuinely zero post-edit, it's M1/M4, not "no reusable component." This control is nearly free and must precede any new measurement.

**Q4. Cheaper/more decisive measurements.** In order of cost:
1. **Sign-flip donor_add** (above) — reuses everything.
2. **Unembedding probe:** project each candidate basis vector onto W_U rows for "dog"/"ant"/"spider". If no basis direction has a positive logit effect on the target concept token, *no* scaling of donor_add can transfer identity — decisive negative for the whole approach at zero GPU.
3. **Norm breakdown:** report ||c_p||/||residual_p|| per position. If the suppressed component is <~1% of residual norm, the subspace is a modulator, not a carrier — reframe before running transfer experiments.
4. **Generic-direction control:** build the same subspace from a syntax-matched, animal-free prompt pair and edit spider→that. If the continuation changes comparably, the effect is generic syntax/gating (M4), not concept.

**Q5. False-positive sources for high cross-token cosine.**
- **Shared mean** (residual-stream anisotropy): random directions in this space already have high cosine; uncentered cosines are uninterpretable. Null: random-direction cosine distribution at matched dimensionality.
- **Single dominating token:** one position with large ||c_p|| drives any norm-weighted aggregate. Check: leave-one-position-out; cosine matrix should be uniformly high, not row-dominated.
- **Autoregressive carryover:** later positions contain copies of earlier token content via attention; agreement reflects copying, not a concept. Check: agreement should survive shuffling the *concept* but not the *positions*; if it tracks position distance rather than concept identity, it's carryover.
- **Rank-1 collapse:** with rank 1 and anisotropic residuals, any B_p will align with the dominant residual PC. Check: does the agreement persist at rank ≥ 3 on the second/third components?
- **Generic syntax direction:** last-3 prefill positions share grammatical role. The Q4.4 control covers this.

---

# Decision, objection, next check

**Decision:** Do not run the proposed basis-selection experiment yet. The Q2 forward-pass-only measurement (centered signed cosine + cross-prompt baseline) plus the sign-flip control and the W_U unembedding probe are each cheaper and jointly gate it: they can kill the hypothesis (no signed component, no logit path to concept tokens, or an implementation artifact behind the 0.000 diff) before any 32-token generation is spent.

**Strongest objection to the whole proposal:** the existing data already contain a counter-signal — donor_add *hurts* removal (5.38 < 6.13) and the L20 diff is exactly zero — which points at sign-blind selection or an application bug, not at a missing cross-token measurement. A new signed-cosine metric will not fix an edit that never reaches the measured site, and "identity not transferred" is fully explained by attention-mediated reconstruction from unedited prefill context without invoking any property of the subspace.

**Next check:** single forward pass, pre/post-edit residual diff at every layer (M1), and on the same pass, per-position c_p signed-cosine matrix, centered and against one unrelated prompt (Q2). Both come from one run; their joint outcome partitions M1/M2/M4 before further spend.

**Uncertainty:** I cannot verify from the supplied facts whether the 0.000 L20 diff is inside the edited span, whether residuals/logits from the prior run are stored (assumed not), or whether the rank-1 sign convention is fixed per token or per stack — each assumption above is flagged where load-bearing.

## Completion

- outcome: `complete`
- trace: `/workspace/2026/suppressed-activations-batchwork/slop/reviews/2026-09-10_kimi-k3_moa_brainstorm_kimi_crosstoken_cosine.trace.jsonl`
