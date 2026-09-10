---
requested_model: moonshotai/kimi-k3
max_tokens: 4000
final_tokens: 20000
reasoning_effort: low
input_bytes: 4682
trace: /workspace/2026/suppressed-activations/slop/reviews/2026-09-09_kimi-k3_propbind_kimi.trace.jsonl
generated: 2026-09-09T14:57:36.656162+00:00
---

# bounded completion

## First call reasoning

Produce brainstorm: mechanisms for why yes/no head stays source-bound while prose identity transfers. Observed vs inferred, mechanisms: (1) answer token position not actually patched (but obs 7 says it is patched — so refuted, but still list as implementation hypothesis with check). (2) yes/no decision encoded outside U-span (rank-4 projector misses the answer subspace; prose identity lives in U-span). (3) answer determined at earlier positions / prefill, decode-last-1 patch too late — decision committed before answer token. (4) degenerate logits (obs 6) — yes/no head saturated, steering signal swamped. (5) reflection at C=2 overshoots (obs 2,4). Give falsifiable predictions + cheapest checks.
## First call answer

# Reconstruction

**Observed (from the evidence):**
- The span-correction edit `h + C(Δ − UUᵀh)` at L20 transfers *prose identity* (dog/ant naming, coherent text) at C=1–2, and transfers the *numeric* legs answer at C=1 (overshooting at C=2).
- The yes/no property head does **not** transfer: prop-dog stays `No` at all C; the mirror property returns source-correct `Yes`; prop-ant transfers at C=1 but reverts at C=2.
- The answer token *is* inside the patched window (prefill last-3 = `Answer`,`:`,` `; decode last-1 = the answer position itself; perturbation_norm 25.7 at C=2). So "position unpatched" is **refuted as stated** — the patch is applied at the answer position.
- Yes/no logits at the answer position are degenerate: p_source ≈ p_target ≈ 0.000 in every property cell.

**Inferred, not observed:**
- That the yes/no decision is represented in the rank-4 U-span at all.
- That the yes/no decision is still undecided at the decode-last-1 position (vs. committed earlier in the prefill).
- That the degenerate logits are a measurement artifact (wrong logit slice) vs. a real saturation of the head.

# Distinct mechanisms

**M1 — Implementation error: the patched tensor is not the tensor the head reads.**
The hook fires and perturbs *something* (norm 25.7), but the yes/no logit may be computed from a different stream (e.g., patched position is the prefill's last token, while the answer logit is read from the *generated* token's position, or a layer/position off-by-one between prefill and decode indexing). Obs 7 checks tokenization, not which activation the LM head consumes.
- *Falsifiable prediction:* directly patching the residual at the exact position whose logits are read (verified by ablating that position to zero and watching the yes/no distribution collapse) will move p(Yes)/p(No).
- *Cheapest check:* at the answer position, replace h with the target-animal's h from a clean target run (full activation swap, no projector). If yes/no still source-bound, the head isn't reading that position → M1 confirmed.

**M2 — Objective/gradient mismatch: the yes/no direction lives outside the rank-4 U-span.**
The projector is fit from template means that capture *identity/prose* variance. The yes/no decision may be encoded in a direction orthogonal to U (or in a different layer). Then `Δ − UUᵀh` rewrites the identity subspace while leaving the answer subspace untouched — exactly the observed dissociation (prose transfers, answer doesn't). The legs digit transferring at C=1 shows *some* answer content is in-span; yes/no may be a sharper, lower-variance direction the rank-4 fit misses.
- *Falsifiable prediction:* a probe (logistic regression Yes vs. No) on L20 residuals at the answer position will find a separating direction with near-zero projection onto U; adding that direction to the basis (rank 5) makes the answer transfer.
- *Cheapest check:* compute ‖U Uᵀ d_answer‖ / ‖d_answer‖ where d_answer is the probe direction or the mean Yes−No difference. Near 0 → M2.

**M3 — Unintended learning/computation dynamic: the decision is committed before the patched window.**
The model may resolve "is it a mammal?" during the prefill (at the question tokens or the animal mention), and the answer position only *reads out* a cached decision via attention. Patching the last-3 prefill tokens and the answer token rewrites local identity but not the upstream key/value the answer position attends to. Prose identity transfers because prose is generated *from* the patched position; the yes/no is copied *to* it. This also explains obs 5 (mirror property returns source-correct `Yes` while prose says ant) — the answer is retrieved from an unpatched source representation.
- *Falsifiable prediction:* patching *all* prefill positions (or at least the animal-mention and question positions) transfers the yes/no answer; patching only the answer token never does.
- *Cheapest check:* attention knockout — block attention from the answer position to the animal-mention positions in the steered run. If the answer flips or collapses, the decision is upstream → M3.

**M4 — Degenerate logit readout (measurement or saturation).**
Obs 6 (p_source ≈ p_target ≈ 0.000) means the yes/no tokens are both near-zero probability at the answer position — the "source-bound" Yes/No may be a fallback argmax among near-zero logits, or the logit extraction is reading the wrong slice. A saturated head can be insensitive to a 25.7-norm perturbation if the decision margin is set elsewhere.
- *Falsifiable prediction:* the top-10 logits at the answer position contain neither Yes nor No under any C; the emitted Yes/No comes from a constrained sampler or a later re-read. Alternatively, logit lens at L20 shows the Yes/No margin forming at a different layer.
- *Cheapest check:* print the full top-k distribution at the answer position for one property cell at C=0 and C=2. If Yes/No aren't in top-k, the "answer head" framing is measuring the wrong thing.

**M5 — Reflection artifact at C=2 (overshoot), distinct from source-binding.**
Obs 2 and 4 (digit `2`, prop-ant reverting at C=2, r2=0.370 loop) are consistent with the algebra: C=2 reflects P h about Δ, overshooting past target. This explains C=2 anomalies but *not* prop-dog staying `No` at C=1 — so M5 is a co-occurring mechanism, not the whole story.
- *Falsifiable prediction:* C=0.5 and C=1.0 should be the best-transfer points for every behavior; any behavior that is source-bound at C=1 is not explained by M5.
- *Cheapest check:* a C-sweep {0.5, 0.75, 1.0, 1.5} on prop-dog only.

# Discriminating order (cheapest first)
1. Top-k logit inspection (M4) — one forward pass.
2. ‖U Uᵀ d_answer‖/‖d_answer‖ (M2) — no generation, just projections.
3. Full activation swap at the answer position (M1) — one patched run.
4. Attention knockout to animal-mention positions (M3) — one patched run.
5. C-sweep (M5) — already partially done; fill in C<1.

No winner chosen: M1–M4 each independently predict source-binding of the yes/no head while sparing prose identity; M5 explains only the C=2 regressions.

## Completion

- outcome: `complete`
- trace: `/workspace/2026/suppressed-activations/slop/reviews/2026-09-09_kimi-k3_propbind_kimi.trace.jsonl`
