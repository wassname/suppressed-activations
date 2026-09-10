---
requested_model: moonshotai/kimi-k3
max_tokens: 4000
final_tokens: 20000
reasoning_effort: low
input_bytes: 5674
trace: /workspace/2026/suppressed-activations/slop/reviews/2026-09-09_kimi-k3_edit_kimi.trace.jsonl
generated: 2026-09-09T12:48:32.766683+00:00
---

# bounded completion

## First call reasoning

Produce mechanisms, falsifiable predictions, cheapest checks, then one construction-level experiment.
## First call answer

# Mechanisms

## M1 — Implementation error: `fixed_delta` norm matching anchors to Δ, not live h
local-c003 scales Δ with `match_component_norm` on the template Δ itself, so decode-time applied magnitude is decoupled from the live source hidden state it lands on. On dog, the prior is strong enough that a fixed-magnitude add rides along; on ant, the same fixed vector lands on a drifting distribution and overshoots/undershoots per step — but we have **no per-decode applied_norm for 893/894**, so this is unverified.

- **Falsifiable prediction:** rerunning 894 with per-decode logging shows applied_norm (in the SVD span) fluctuating or growing relative to the live source span norm across steps, unlike frozen/sync which are subtract-referenced.
- **Cheapest check:** add applied_norm logging to the `fixed_delta` hook; rerun 894 ant only (one spec row, 128 tokens). No new steering construction.

## M2 — Objective mismatch: add-without-subtract leaves the live spider span intact
`h + CΔ` asks the residual to *both* keep spider content (never removed) *and* express ant content (added once, same vector). The naming token can be produced (Δ peak wins the head), but the paragraph generator re-reads the un-subtracted spider span and resolves the contradiction with Wait/loop. Frozen/sync subtract the source span, so their failure mode (908) is different: replacement toward **stale** coordinates — see M3.

- **Falsifiable prediction:** measure cosine of the live residual's spider-template component across decode in 894: it stays high (~prefill level) through the loop, whereas in 895 sync it decays. If the spider component in 894 actually decays on its own, M2 is weakened.
- **Cheapest check:** post-hoc projection of saved 894 residual stream (or a 32-token rerun) onto the template spider direction; no new intervention.

## M3 — Unintended dynamic: frozen replacement is a constant pull toward off-trajectory coordinates
908's decode target is the frozen donor-**prompt** final position, which never follows source-selected tokens. As the continuation diverges, `donor − source` stays large (applied_norm last 11.1, median 11.46, sum 1550) — the model is yanked every step toward a fixed point that is increasingly wrong for the current context, producing Wait/incorrect loops for **both** animals. Sync (895) self-attenuates (sum 184) because the donor history tracks source tokens — and it *does* achieve coherent naming, then reverts, i.e. the opposite failure.

- **Falsifiable prediction:** in 908, per-token steered-vs-Base logit divergence should *not* decay with step (constant injection, accumulating context damage), while in 895 it decays monotonically. If 908's divergence decays too, the "stale pull" story fails.
- **Cheapest check:** compute per-step KL(top-k) between steered and C=0 logits from existing 908 vs 895 saved runs — pure analysis, no GPU steering.

Note M2 and M3 are independently supported: 894 fails *with* the source span retained; 908 fails *with* it removed but a stale target. Neither is excluded.

---

# One construction-level experiment

**L20 attenuation projector + `shared_replace` toward synchronized donor (source-token-conditioned), C ∈ {0, 2}, dog + ant, naming questions, single `--batch-spec`.**

Rationale: every pairwise contrast so far changes **two** axes at once (layer AND subtraction/conditioning). The unbuilt cell is synchronized conditioning at **L20** — the layer where dog persistence was actually achieved (893). This isolates whether the subtract-and-track dynamic (which gave coherent ant naming at L24 but reverted) preserves 893's dog persistence at the layer that supports it.

- **Reference cells in the same family:** C=0 row in the same batch (identity check: steered IDs = Base, applied_norm 0, as in 908 C=0); 893/894 (L20 fixed_delta) and 895 (L24 sync) as saved-trace references — no rerun needed.
- **Constraints honored:** source prompt unchanged; continuous steering (C=2); common dog+ant rule; verified `--batch-spec` path (`synchronized-attenuation` already runs synchronized donor generation under batch-spec at L24 — only the layer argument differs); property/legs unselected.
- **Instrumentation:** per-decode applied_norm + `replacement_trace` (already emitted by `shared_replace`), so this run fills the exact logging gap that 893/894 left.

**Outcome map (no winner chosen):**

| outcome | reads as |
|---|---|
| ant coherent-persistent, dog kept | conditioning + L20 jointly suffice; 894 loop attributable to add-without-subtract at a layer where sync works (M2) |
| ant coherent-transient (reverts like 895), dog kept | conditioning alone gives transience regardless of layer; persistence gap lives elsewhere, M2's "layer-independent" version dies |
| dog breaks | dog persistence at 893 depended on the non-subtracting add; M1/M2 gain, subtraction itself implicated in dog loss |
| both loop like 908 | sync at L20 reproduces frozen pathology → the L20/L24 projector difference, not conditioning, dominates; M3 weakened |

First-step applied_norm vs 895/908 is expected to differ (different layer/projector) and is **not** to be read as decode equivalence.

## Completion

- outcome: `complete`
- trace: `/workspace/2026/suppressed-activations/slop/reviews/2026-09-09_kimi-k3_edit_kimi.trace.jsonl`
