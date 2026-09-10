---
requested_model: moonshotai/kimi-k3
max_tokens: 4000
final_tokens: 20000
reasoning_effort: low
input_bytes: 4930
trace: /workspace/2026/suppressed-activations-batchwork/slop/reviews/2026-09-10_kimi-k3_moa_brainstorm_kimi_crosstoken_nulls.trace.jsonl
generated: 2026-09-10T08:50:53.338448+00:00
---

# bounded completion

## First call reasoning

The user wants a bounded decision? Actually the system prompt says "Answer the user's bounded decision request... state the decision, strongest objection, and next check." But the user message is a brainstorm request with 5 questions. I should follow the system prompt: give a decision, strongest objection, next check — while addressing the questions compactly. Let me answer the questions substantively but frame as decision.

Key content:

Q1: A statistic that survives: compute alignment at peak layer on the subspace orthogonal to the shared mean — i.e., remove the mean direction, then test residual alignment. But more direct: per-position-pair signed cosine at L25 of c_p against source c_p (source-vs-donor, source-vs-control), with norm weighting, and a matched-random-direction null via permutation over vocabulary directions. The distinguishing statistic: distribution of per-pair cosines (not means), specifically whether the top pair(s) exceed the max of the random null distribution, and whether the same token pair shows it across source and both donors but not control. Refutation: if max pair cosine at peak ≤ random null max, or if alignment is driven by a shared mean direction (subtract mean and alignment dies → "shared mean" explanation). Support: alignment survives mean-removal and is token-identity-specific (webs/legs positions, not punctuation).

Q2: Measure at peak 25 (and 26-ish), but circularity: detector selects tokens by rise-to-peak, so scoring alignment of those tokens' directions at the peak is partly selection-on-noise (winner's curse). Control: split — select tokens on one half of prompts/contexts, measure alignment on held-out contexts; or use fixed named tokens (spider/dog/ant) chosen a priori rather than detector-selected. Peak-vs-early increase shows the rise is shared-structure, not that it's concept-level — could be shared "any noun being suppressed" state. Distinguish via same-form control and different-animal donors.

Q3: Positions: "webs" (property phrase), "animal", "spins", "legs"? Actually the prompt: "Fact: The number of legs on the animal that spins webs is ". Concept positions: "webs", "animal", "legs". Final "is " is syntax/decision position. Distinguish concept from syntax: same-format control with different animal (dog) shares syntax; if alignment appears at webs/animal positions only for spider and not control, it's concept. Also swap property: animal that barks vs spins webs — same syntax positions, different concept.

Q4: Cheapest causal follow-up: activation edit at peak layer only (L25), adding/subtracting the consensus direction at the concept position(s), with fixed replacement procedure, matched-random direction control and orthogonal control, on both spider→dog and dog→spider, measure p(8)/p(4) and full continuations. Selector change only: swap which direction is injected, keep everything else.

Q5: If nothing survives: test the "suppression state is per-token/per-layer, not a shared direction" hypothesis — i.e., the mechanism is distributed: measure whether a per-position rank-1 edit at peak works locally (single-position, per-position own direction, not consensus) — if each position's own top suppressed direction edit changes output but consensus doesn't, suppression is token-specific state, not reusable concept. Distinguish from detector noise: test-retest reliability of detector scores across paraphrases/seeds; if detector scores are stable but directions don't transfer, it's token-specific state; if scores unstable, detector is noise. Cheap: split-half reliability of the detector ranking + single-position causal edits.

Decision: build the bank as planned but gate the causal edit on a mean-removed, pair-level, peak-layer statistic with held-out selection to avoid the winner's curse.

Strongest objection: the peak-layer measurement is selection-contaminated — the detector picks tokens that rise at 25, so agreement at 25 of selected tokens is partly guaranteed; without split-half selection the whole planned analysis may reproduce a null-like artifact of a different kind.

Next check: split-half token selection (select on half the prompts, measure on other half) — cheapest, kills the circularity before any causal spend.

Format: headers per question, concise, mark observed vs inferred.
## First call answer

# Decision

Build the trajectory bank as planned, but **gate everything on one statistic computed one way**: pair-level (not mean) signed cosines at the **peak layer**, on the **mean-removed** components, with **held-out token selection** (select suppressed tokens on half the contexts, measure alignment on the other half). The planned design as written will otherwise produce a clean-looking artifact at L25 and you'll spend the causal budget chasing it.

---

## Q1 — A statistic that actually distinguishes the hypotheses

**Observed:** all three first-screen statistics are at their mechanical nulls; no cross-token agreement has been demonstrated at any layer.

**The failure mode to design against:** "orthogonal-ish nuisance + shared mean" and "reusable signed direction" both produce nonzero raw alignment. They differ in where the alignment lives.

**Statistic, two-stage:**

1. **Shared-mean test.** Compute the mean component direction across positions/prompts, μ = normalize(Σ c_p). Project it out: c'_p = c_p − ⟨c_p, μ⟩μ. If the source's mean-subtracted alignment with donors collapses to the matched-random null while raw alignment was high → "shared mean" explains everything. This is cheap and decisive for that branch.
2. **Pair-level max statistic, not the mean.** The user's proposal is existential ("agreement from 2+ tokens"), so the right statistic is the **distribution of per-pair signed cosines** ⟨c'_source, c'_donor⟩ across all position pairs at L25, and specifically the max / top-quantile against the max of a null distribution. Null: matched random directions of identical norm drawn from the same layer-25 residual covariance (whiten by the empirical covariance, don't assume isotropy — residual streams are anisotropic and "random cosine ≈ 0" is often wrong in high-d anisotropic spaces).

- **Refutes the proposal:** max pair cosine at L25 ≤ null max, for spider-vs-dog AND spider-vs-ant, on held-out selection.
- **Supports it:** a small set of pairs exceeds the null max, the *same token identities* (e.g., webs↔webs) carry it in both donors, and it survives mean removal.

**Inferred, not established:** that any pair will clear the anisotropic random null. The rank-1 edit leaving p(8) untouched in *all* conditions including controls weakly suggests nothing causal was found at L23, which is consistent with either hypothesis.

## Q2 — Layer and the circularity problem

**Observed:** the detector is *defined* by rise 23→25 and fall 25→32. The first screen measured only at L23.

**Decision:** compute agreement at L25 primarily, L23 and L32 as contrast.

**The circularity is real and is the strongest objection to the whole plan (see below).** Selecting tokens *because* they rise at 25 and then measuring those tokens' directions *at* 25 is selection on the measurement — winner's curse. Even pure noise tokens selected this way will show inflated peak magnitude and possibly inflated mutual alignment if the selection correlates with anything shared.

**Controls needed, in order of cost:**
1. **Split-half selection** (mandatory): select top-suppressed tokens on one half of prompts/paraphrases, measure their alignment on the other half. Selection noise doesn't transfer across contexts; signal does.
2. **A priori named tokens** (spider/dog/ant/webs/legs), chosen without the detector. Zero selection bias; if detector-selected tokens align but named tokens don't, the detector is selecting peak noise.
3. **L32 as negative control layer:** the tokens fall by 32, so alignment *of the selected directions* at 32 should drop if the rise is real signal.

**What a peak-vs-early increase shows:** the rising direction has shared structure. **What it does not show:** that the structure is *concept-level*. "Any noun currently being suppressed" is also shared structure. That distinction is a position/control problem (Q3), not a layer problem.

## Q3 — Positions and the syntax confound

Prompt: "Fact: The number of legs on the animal that spins webs is "

**Plausible concept-bearing positions the last-3 window misses:** "webs", "animal", "spins", possibly "legs". The last-3 window ("webs", "is", " ") actually contains one concept token and two syntax/decision tokens.

**Distinguishing concept from syntax-position confound:**
- The same-format control (different animal, identical template) shares *all* syntax positions. If alignment at "webs"/"animal" appears for spider-vs-dog above control, it is not syntax.
- The decisive cheap test: **position-by-token-identity interaction**. A real concept signal should concentrate at the property-phrase positions and be token-specific (webs aligns with webs in the spider prompt; the "is " position should show no above-null alignment). If alignment is spread uniformly across positions including "Fact:" and "is", it's a format/syntax state, not a concept direction.
- A "barks" vs "spins webs" prompt pair (same syntax skeleton, different property) would fully dissociate, at the cost of one more prompt family.

**Inferred:** the final "is " position most likely carries the *answer-decision* state (numeric answer formation), not the animal concept — measuring only last-3 may have been measuring the wrong slot entirely.

## Q4 — Cheapest causal follow-up (only if Q1–Q3 survive)

Single intervention, everything else frozen:

- **Where:** peak layer only (L25), at the one or two concept positions identified in Q3.
- **What:** inject/ablade the held-out-derived consensus direction (derived on selection half, applied on measurement half).
- **Controls:** matched-random direction of equal norm; the orthogonal-to-consensus direction; donor direction applied to source and vice versa (spider-direction into dog prompt should push p toward 8 and "spider" continuations; dog-direction into spider prompt toward 4).
- **Selector change only:** the replacement procedure, positions, norm, and layer are identical across conditions; only which direction goes in changes.
- **Readout:** p(8)/p(4) plus full continuations for both animals — the first screen showed p can stay flat while identity is also unchanged, so require *both* a logit move and a semantic move in continuations before claiming anything.

If the consensus edit moves the donor but matched-random doesn't, and the effect is bidirectional, that's the minimal causal evidence for a reusable signed direction.

## Q5 — If nothing survives at any layer

**Honest next mechanism:** the suppression signal is **token- and layer-local state**, not a shared direction — each position suppresses via its own direction, and cross-token transfer was never the right unit of analysis.

**Distinguishing it from "the detector is noise" without a sweep — two cheap measurements:**

1. **Detector reliability (noise test):** split-half / paraphrase stability of the detector scores and rankings themselves. If the top-suppressed token set is unstable across paraphrases of the same fact, the detector is noise — stop, fix the detector, nothing downstream is interpretable.
2. **Local causal efficacy (token-specific-state test):** per-position edits along *each position's own* top suppressed direction at its own peak — no consensus, no transfer. If own-direction edits reliably change the output while cross-position/consensus edits never do, suppression is real but distributed per-token: the mechanism is "many local suppressors," and the right object of study is the per-token causal graph, not a shared concept direction.

**Decision rule:** (1) fails → detector noise. (1) passes + (2) passes → token-specific suppression state, user's other hypothesis confirmed, abandon cross-token direction hunt. (1) passes + (2) fails → the detector selects tokens that don't matter causally at all; the suppression framing itself is the problem.

---

## Strongest objection to this plan

The L25 measurement is **selection-contaminated by construction**: tokens are chosen for rising at 25, then alignment is measured at 25. Without split-half selection (or a priori named tokens), even the mean-removed pair-max statistic can clear its random null for reasons unrelated to any concept. This is the same class of error as the three nulls already found — a statistic whose null was mis-specified because the selection procedure wasn't in the null model. One round of this has already been spent.

## Next check (before building anything else)

Run the **split-half selection test on the existing screen setup** — it needs no new bank: select top-suppressed tokens on half the prompts, compute L25 pair cosines on the held-out half, compare against same-half selection. If held-out alignment collapses relative to same-half, the peak-layer circularity is confirmed and large, and the bank must be built with held-out selection baked in from the start.

## Uncertainties

- The anisotropy of L25 residuals for this model is unmeasured; all "random" nulls above assume a covariance-matched null that hasn't been constructed yet.
- Whether "8-legs" behavior is even suppression-mediated in this model is inferred from correlational detector scores plus one flat edit screen — the causal link is unestablished.
- T=3 mechanical nulls are settled; pair-level statistics over *all* positions have a different (larger, better-powered) null geometry that has not yet been computed.

## Completion

- outcome: `complete`
- trace: `/workspace/2026/suppressed-activations-batchwork/slop/reviews/2026-09-10_kimi-k3_moa_brainstorm_kimi_crosstoken_nulls.trace.jsonl`
