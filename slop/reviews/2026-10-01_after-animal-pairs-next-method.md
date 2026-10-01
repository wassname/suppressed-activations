# Next method: fixed generic normalized-state subtraction

**Decision:** Choose normalized-decoder-state subtraction, followed by the existing current-output half-erasure. This is one prospective new method, not restoration of missing reference centering. Nothing was executed or queued; v5 remains unrun.

## Evidence and interpretation

The supplied fresh semantic review reports **0/4 returned identities and 0/4 strict joint passes for every animal-pairs method**, with **0/2 preference reversals**. Only cat/goat has identical complete scoring text; horse explicitly says its identity.

The preregistration, `slop/audits/2026-10-01_animal-pairs-preregistration.md`, correctly distinguishes:

> “PositiveD without reversals is partial discrimination with label bias.”

Generic prior bias is therefore plausible, not established as the failure’s cause. Direct cue association, inadequate identity computation, and capture/scoring errors remain alternatives. Neither positive D nor successful subtraction would establish **necessary hidden reasoning**.

The parent additionally reports that the current 2694 numerical checker failed and root-cause inspection is pending. I have not inspected that failure; do not describe numerical verification as passed.

## Choice and supervisor discussion

| Option | Intended effect | Main drawback |
|---|---|---|
| Raw residual subtraction before transport/norm | Remove shared residual activity | Nonlinear normalization entangles subtraction with residual magnitude |
| **Normalized decoder-state subtraction** | Remove a fixed decoded prior | Can remove useful shared concept signal; cannot distinguish association from reasoning |

I proposed the second option through the supervisor. The parent agreed, including fixed **pre-projection** random-reference norm matching, and required reporting post-projection/BF16 norms without claiming those remain matched.

The reference review, `slop/reviews/2026-10-01_native-v4-reference-check.md`, states:

> “Adding activation centering or a transport bias would be a new method, not restoration of a missing reference operation.”

## Frozen specification

Generic user content, selected before its activations or scores are observed:

`Complete the fact with only the missing word or phrase:\nFact:`

Use the existing native-chat rendering, thinking disabled, generation prompt enabled. Reuse `generate_readout` in `scripts/english/08_jlens_one_pass.py:403–421` with `max_new_tokens=1`: **one generic prefill**, no cached continuation calls. Its computed greedy token is discarded and must not affect preparation or scoring.

Capture final-prefill residual24 and residual27. For each representation \(R\), define:

- J24 transport: \(T_R(h)=h_{\mathrm{FP32}}J^\top\).
- Plain24/plain27: \(T_R(h)=h_{\mathrm{FP32}}\).
- \(z_R=\mathrm{FP32}(N(\mathrm{BF16}(T_R(h))))\), using the actual model norm.
- Generic reference \(z_{0,R}\): identical transformation of the generic state.
- \(w_x\): FP32 unembedding row of the **current case’s original final-prefill greedy token**.
- \(P_x(v)=v-\tfrac12(v\cdot w_x)/(w_x\cdot w_x)\,w_x\).
- Candidate scores: \(\mathrm{FP32}(\mathrm{head}(\mathrm{BF16}(P_x(z_R-z_{0,R}))))\).

Thus: **transport → native norm → FP32 subtraction → FP32 half-projection → BF16 cast → head**. No second norm. Do not substitute separately BF16-rounded logit subtraction.

This extends the inspected production ordering: `08_jlens_one_pass.py:883–885` uses `h.float() @ matrix.T`; `:1177–1194` normalizes before projecting and casts the erased state before the head.

Keep the original input-prefix mask, greedy-output mask1, residual24 J rule, final-prefill position and k32. Labels and saved generations enter evaluation only—not reference construction, projection, masks, or rankings.

## Controls and cost

Rescore **all twelve cached cases**: eight native-v4 plus four animal cases. Preserve original outputs and scores unchanged.

For J24, plain24 and plain27, compare:

1. Generic-reference subtraction.
2. Fixed seed0 isotropic random-reference subtraction.
3. Existing unsubtracted half-erasure.

Use one shared FP32 random unit direction, separately scaled to each \(z_{0,R}\) norm. Freeze it across cases; no per-case rescaling. Apply identical projection order, dtype and masks. Retain original mask-only J separately.

Record reference norms before projection, after projection and after BF16 casting. Matching is **before projection only**, not score-space matching or an orientation-only experiment.

Maximum initial neural cost: one generic prefill; cached scoring must reject transformer calls. No current-input prepass, backward pass, new generations, dose/layer/k/mask tuning, or per-case winner selection.

## What guides the next attempt

The useful outcome is **newly returned identities with input/actual-said exclusion**, assessed symmetrically on complete lists—not improved diagnostic counts alone. Report paired gains/losses against old J, equally transformed plain and random controls, separately for /8 and /4; horse remains in the denominator.

If generic subtraction yields clean recoveries beyond these controls, freeze the rule for a separately authorized new-example test. If only alias margins/AUROC improve, the readout goal remains unmet. If random/plain improvements match it, generic-prior removal is not specifically supported. If identities disappear, shared-signal removal becomes more plausible; do not rescue this run by tuning.

Before interpreting results, resolve the reported checker failure and verify zero-reference parity, subtraction/projection arithmetic, cache provenance and unchanged masks. No smoke, numerical reconstruction, or runtime validation was performed here. Training/init/loss/schedule checks are inapplicable; independent-family adjudication remains absent.

**Signed: PI/OpenAI**