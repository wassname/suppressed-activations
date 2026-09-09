---
requested_model: moonshotai/kimi-k3
max_tokens: 20000
final_tokens: 20000
reasoning_effort: low
input_bytes: 42632
trace: /workspace/2026/suppressed-activations/slop/reviews/2026-09-09_kimi-k3_brainstorm_kimi_r2.trace.jsonl
generated: 2026-09-09T08:00:01.911338+00:00
---

# bounded completion

## First call reasoning

Produce the brainstorm: observed vs inferred, mechanisms (implementation error, objective/gradient mismatch, learning dynamic analogues here—inference-only so "unintended dynamic" = autoregressive feedback/correction loop), falsifiable predictions, cheapest checks, intervention construction sweep.
## First call answer

# Reconstructing the situation

## Observed (from records)

- **Old local-dog, L20-selected/edit-at-20**: coherent dog answer + description. Same edit layer, equal perturbation norm (18.94), but **L25-selected** basis produces a correction loop ("The animal that spins webs is called a dog… wait…"). Basis choice, not edit strength, flips the outcome.
- **Old ant, L24**: frozen donor replacement gives first-token 6 but "spider" body; synchronized (donor state re-read at each step, fed the *generated* token) gives coherent ant. Same first logits in both.
- **Band L22/23/24 with proper wrapper and fixed prompts**: leg prompts give "4/dog" and "6/ant" coherently (dog has one factual slip: two legs run/jump, two support weight). Naming prompts emit the donor name first token ("狗 (Dog)", "蚂蚁 (Ant)") then **self-correct back to spider**.
- **Norm-matched random spans**: 3/8 dog and 1/8 ant random directions exceed the selected digit log-odds shift, yet all random continuations stay spider; selected continuations describe dog/ant. So log-odds shift ≠ semantic transfer; the selected direction carries something random directions don't, but the digit-shift metric doesn't certify it.
- Wrapper-correct steered runs elsewhere stay fully spider → bare first-token mass is not semantic transfer.
- Source hashes differ between old successes and current tree for the local-dog and ant cases; only the fixed-band runs match current source. The pseudocode describes the *current* selector (raw template-contrast attenuation), not the original vocabulary rise-and-fall detector.

## Inferred (not established)

- The current selector plausibly selects different directions than the original detector (the brief warns exactly this).
- Naming prompts invoke a strong "answer → verify against question" circuit; the edit carries the answer token but not enough identity context to survive verification.
- Synchrony matters because generated tokens drift off the donor manifold; frozen donor states stop matching after the first token.
- The band's factual slip (dog legs) suggests property-level transfer is partial even where identity transfer passes.

---

# Candidate mechanisms

## M1 — Implementation/selector regression (implementation error)
The current attenuation selector (raw residual contrasts, no normalization, template-mean) finds a different subspace than the original gain-weighted unembedding rise-and-fall detector. The band successes may survive because multi-layer rank-4 replacement is brute-force enough to work with either basis, while single-layer conditions silently fail.

- **Falsifiable prediction**: Implement the original vocabulary detector alongside the current one on the same templates; their top-r subspaces will have low principal-angle overlap at the layers where old/new outcomes diverge (e.g., L20-selected vs L25-selected local-dog), and high overlap where both work.
- **Cheapest check**: No generation needed. Compute both bases from recorded templates, report principal angles and the per-direction gain-weighted unembedding scores of each basis's vectors. One forward pass over 4 template pairs.

## M2 — Objective mismatch: digit log-odds and first-token mass proxy the wrong quantity (objective mismatch)
The selection metric (digit log-odds shift, first-token mass) is satisfiable by directions that don't encode identity. Random spans already beat the selected shift on 4/16 rows while producing zero transfer. Optimizing/believing this metric accepts identity-free directions.

- **Falsifiable prediction**: A scoring rule based on *multi-token semantic coherence* (e.g., donor-animal mention in sentence 2–3, absence of "wait/incorrect" corrections) will rank the selected direction above all 16 random directions, even though digit log-odds does not.
- **Cheapest check**: Reuse the already-recorded random-span runs if continuations exist; otherwise one batch of 16 short generations (cap 40 tokens) with the loaded model, scored by string match for dog/ant/spider/wait. No new basis fitting.

## M3 — Correction-loop dynamic: identity edited at the answer slot is overridden by question-conditioned verification (unintended dynamic)
Both naming cases show the same pattern: donor name emitted, then "Wait, that is incorrect… spider." The L25 local-dog failure is the same loop. The edit lands on the answer representation, but the next tokens re-read the *question* ("spins webs"), whose unedited representation reasserts spider. The leg-question runs avoid this because the answer is a digit and the descriptive continuation isn't checked against a name.

- **Falsifiable prediction**: If the edit is extended to the *question-descriptor span* ("the animal that spins webs") rather than only the final 3 positions, the correction loop disappears even at the layers/strengths that currently loop. Conversely, editing only the descriptor and not the answer span should yield spider-first-token but donor-consistent description (partial transfer).
- **Cheapest check**: Two conditions × two animals = 4 generations, reusing the fitted band basis, only changing `source_positions` in the hook. Reuses the loaded model.

## M4 — Position/span mismatch: final-3-positions ≠ answer-token positions across prompts
The old local-dog edited positions [32,33,34] of a chat-prefill where the answer token sits inside that span; the band uses [38–40]/[42–44] on different wrappers. If the span covers instruction or whitespace tokens rather than the token where identity is computed, the edit is diluted.

- **Falsifiable prediction**: Perturbation norm per *answer token* (not per span) predicts success better than per-span norm; aligning the span to the actual answer-token index recovers old local-dog behavior at L25 selection.
- **Cheapest check**: Log which positions in the edited span correspond to answer vs instruction tokens (pure tokenization, no forward pass), then one generation with the span re-centered.

## M5 — Norm-matched random is not a null for direction quality (analysis artifact)
Random norms are computed from the *random-condition's own* trajectory state, not the selected trajectory (noted in pseudocode). So "equal norm" is only nominal; the comparison understates or overstates the true matched perturbation.

- **Falsifiable prediction**: Recomputing random edits with norms taken along the selected trajectory changes the log-odds ranking of the 8 random rows.
- **Cheapest check**: Instrumentation-only rerun of existing random conditions with dual norm logging; 16 short forwards.

## M6 — Frozen-vs-synchronized divergence as donor-trajectory drift (dynamic)
Frozen donor states encode the donor's *own* continuation; after the first generated token the source trajectory diverges from the donor's, so frozen states become stale. Synchrony re-conditions the donor on the actual prefix. The old ant pair directly demonstrates this; whether the band needs it is untested.

- **Falsifiable prediction**: A frozen band run will show first-token transfer with spider reversion (mirroring old frozen ant); a hybrid (synchronized for the first k tokens, frozen after) will show transfer decaying at k.
- **Cheapest check**: The frozen band condition is a one-flag config change; 2 animals × 2 conditions = 4 generations.

---

# Intervention construction sweep (one rule for both animals, inference-only)

All respect: unchanged source prompt, continuous steering during generation, serial small runs, full provenance.

1. **Span-targeted synchronized edit**: band basis, but edit the question-descriptor span *and* the answer span at every step. Tests M3/M4.
2. **Answer-token-locked edit**: dynamically locate the position that will be attended to produce the first answer token (last position of the answer template) and edit only it, synchronized. Minimal-footprint version of (1).
3. **Dual-detector basis**: QR-concatenate original-vocabulary-detector directions and current attenuator directions, rank-match at 8, run band. If loops vanish, selector identity (M1) is implicated; cheap because both bases come from one template forward.
4. **Per-layer norm rebalancing**: band norms are wildly uneven (L24 ≈ 5–10× L23). Normalize per-layer perturbation to equal norms, or inverse-weight. Tests whether L24 dominates and L22/23 are decorative.
5. **Layer ablation ladder on the band**: {24}, {22,24}, {22,23,24} under synchrony, naming prompt. Directly connects old single-layer successes to the band and isolates which layer carries naming vs property content.
6. **Property-probe prompt battery** (no new formulation): legs, habitat, sound, diet, each as separate prompts with the same fitted basis, scoring factual coherence (catches the "two legs run/jump" partial-transfer case systematically).
7. **Anti-correction prefill**: append "Answer without correcting yourself." — if the loop is prompt-triggered verification (M3), this removes it with zero basis change; a control, not a mechanism fix.
8. **Positive control calibration**: pure full-state donor replacement at one layer, as the ceiling reference; everything else reported as fraction-of-control. Explicitly *not* claimed as suppressed-subspace evidence.

# Notebook/readout requirements

Each run must print: which selector produced the basis (and its hash), hook fire counts per layer per step, per-step perturbation norms at the edited positions, principal angles to the alternate basis, full Base/donor/intervened continuations, and the scoring rule applied (string-level identity + correction-phrase flags), so that "what was measured" is unambiguous.

# Priority ordering (cheapest discrimination first)

1. Principal-angle comparison of old-detector vs current-selector bases (no generation) → M1.
2. Token-position audit of edited spans (no forward pass) → M4.
3. Descriptor-span edit, 4 generations → M3 (the strongest observed regularity: two independent correction loops).
4. Layer ablation ladder → connects old and new regimes.
5. Frozen-band rerun → M6.

No winner chosen: the correction-loop pattern (M3) is the most *visually* striking regularity across two independent cases, but M1 is compatibly upstream of it — a wrong basis could produce exactly the weak-identity edits that verification then overrides — and the span-position confound (M4) is not excluded by any recorded field.

## Completion

- outcome: `complete`
- trace: `/workspace/2026/suppressed-activations/slop/reviews/2026-09-09_kimi-k3_brainstorm_kimi_r2.trace.jsonl`
