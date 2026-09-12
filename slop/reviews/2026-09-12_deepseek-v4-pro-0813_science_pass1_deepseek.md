---
requested_model: deepseek/deepseek-v4-pro-0813
max_tokens: 4000
final_tokens: 20000
reasoning_effort: low
input_bytes: 12075
trace: /workspace/2026/suppressed-activations-batchwork/slop/reviews/2026-09-12_deepseek-v4-pro-0813_science_pass1_deepseek.trace.jsonl
generated: 2026-09-12T01:04:24.230922+00:00
---

# bounded completion

## First call reasoning

We need answer user's bounded decision request. We need parse. They ask: identify what the LAST THREE blocks (29,30,31) suppress; then decide where intervention should act — early (their suggestion: layer 3), where components are built, after built/before suppressed, or at multiple layers. Need use supplied evidence. We need be skeptical, state decision, strongest objection, next check. Do not request files or defer work. We need reconstruct method from primary evidence/pseudocode. Need distinctions, assumptions, failure modes, alternative formulations, experiments. Separate supplied directly vs inference. State what observation would change mind. Uncertainties missing evidence. We need answer from message alone. Need likely decide intervention layer. Need analyze supplied evidence.

We need produce organized response. Let's understand.

We have Qwen3.5-4B 32 blocks. Suppressed activation analysis selects per token position rank-8 readout-direction subspace whose logits rise then fall across chosen layers. User wants identify what last three blocks (29,30,31) suppress; then decide where intervention should act — early layer 3, where components built, after built/before suppressed, or multiple layers. Raw activation norms across layers not comparable semantic strengths. Same-procedure location comparison running.

We need use evidence.

Primary evidence:
1 applied edit: common_replace at residual_layer. Equation h'_p = h_p + C (P_d d_p - P_s h_p), per active position. C=1.5. Source and donor projectors. At prefill if hidden.shape[1] > 1 use src,dproj from spec["src"],spec["donor_proj"]; else decode_src/decode_proj. coords = einsum src with h; span = einsum coords,src; patched = h + strength*(dproj.unsqueeze(0)-span). Hmm dproj maybe donor projection? dproj maybe P_d d_p? Need infer. They use coords and span = P_s h, patched = h + C*(dproj - span). dproj is donor projected state? Spec donor_proj. For batch? Need not deeply.

2 basis/projector construction. suppressed_activation_subspace with early_layer, peak_layer, output_layer, rank=8, normalize_unembedding_rows=True. Source/target. per-position rank-8 orthonormal bases. union_basis over window (last 4 positions?) M = win.permute(1,0,2).reshape(win.shape[1], -1) # (hidden,r*W). SVD keep columns with s_vals > tol. top8_union arm U_s,U_d = U_s[:, :8], U_d[:, :8] declared applied projector. donor states at same intervention layer, end-aligned offset o (1..3); decode uses frozen final-prefill donor state and same common projector (per_token arm alone uses last-position per-token basis). Selector: rise = logits[:,1]-logits[:,0]; fall = logits[:,1]-logits[:,2]; mean centered; return min(positive rise, positive fall). running task1130: (early,peak,output)=(23,25,32); approved follow-up: (29,30,32).

Need note selector layers: early=23, peak=25, output=32. So selected tokens rise from layer 23 to 25 (block 24), fall from layer 25 to 32. Thus "where components are built"? Need infer: components rise between 23 and 25, peak at 25. Last three blocks 29,30,31 are part of output fall (25->32), but not necessarily causal. Evidence 3 measured L20/L25 results: replacement at L20 weak +0.20 to +0.25 random near zero. At L25 strong +1.95 to +2.85, split etc. So intervention at L25 effective. L20 not. They haven't run L3? The planned variant changes selector to (29,30,32) for late-selector bases. Running location OAT likely sites L3/L25/L30/L32.

Evidence 4 late-block energy table. Fixed projector (probably selected by old early=23 peak=25 output=32? Need they call fixed projector; likely source/donor union from dev questions? It measures projected fraction of h_l by layer: h30 0.0394 peak, h31 0.0316, h32 0.0240. Block writes absolute projected energy change: block29 +45.0 largest, block31 +36.4 positive on dev questions. Selected-token readout decomposition: mean numerator <h_l,u_i*g> from h30 5.45 -> h32 0.87, -84%; 753/768 pairs lose. But total absolute E in union span rises h30->h32 (86.9 to 129.7; 23/24 prompts rise). block31 removes absolute span energy on canonical short Fact prompts source -20.7, control -3.2, dog grows +11.6.

Need identify what last three blocks suppress? Evidence suggests selected-token readout directions fall across 30->32; total projected energy rises. So maybe last blocks do not suppress the entire selected subspace; they suppress the selected token directions (readout numerators) while adding energy in other directions within the projector union. But caution: the selection criterion used readout fall, so selected tokens falling is definitional, not independent. Last three blocks (29,30,31) write energies: block 29 +45.0 (largest), block 30 +6.4, block 31 +36.4 positive on dev questions. So last three blocks collectively add projected energy to the fixed projector span, not suppress it in norm terms. But block31 can remove absolute span energy on canonical source; block29 adds. On dev questions total E rises. Last three blocks suppress selected token logits (numerator) by rotating within span? Maybe not measured; selected numerator collapse and denominator increase indicates direction change, but no cross-layer basis correspondence. They label "direction change is a labeled hypothesis, not measured".

We need answer likely: Current evidence does not establish that blocks 29/30/31 suppress a stable component set. At best they suppress readout-selected token directions (logits) while total projected energy rises; this is selection artifact. For intervention location, L25 is supported by measured results; early L3 unsupported and likely wrong because L20 replacement was near zero. After built/before suppressed L30? Need compare. The edit at L20 (before built? Actually selector rise at 23->25, so components built around 24; L20 before built) yields weak; L25 (after built / peak) strong. So intervention should act where components are built/peak, not early before components exist nor after final suppression maybe. But user's suggestion layer 3 early: evidence against. Need decide likely: at peak/build site L25, not L3, not multiple unless evidence. Need state strongest objection: L25 measurements use old selector (23,25,32); what components built at L25 may be suppressed later? We have no causal evidence that late blocks suppress semantic content; the "suppressed activation" labels are based on readout fall, not removal. Also raw norms not comparable. Location comparison running but not available. We should recommend wait for location OAT with same construction, especially including L25/L30/L32 and late-selector (29,30,32), before choosing. But the prompt asks decide where intervention should act. We can state decision: L25, not early L3; do not act at final readout/multiple with current evidence; run or await same-procedure location comparison including L30 and late-selector. Need be decisive.

Need include "strongest objection" maybe: The evidence for L25 may be from donor state at L25; if target site changes to L30/L32, donor state and projectors fixed? The applied edit at site L uses donor state at same intervention layer. At L25 donor state has semantic answer; at L30 maybe donor state is passed through suppression? But donor prompt maybe also suppressed? Need think. If intervention at L30, donor state d_o = h_30^donor[end-o] includes late-block processing. Its donor components in P_d? Maybe selected donor components might be altered. But measurement at L25 shows donor components strong and replacement works. At L30? Unknown. Also L25 near rise peak so source components are maximal and donor components likely present. The strongest objection is that success at L25 is predicted by the selection criterion because it measures rise to peak; intervening at the peak is not evidence about where causal necessity lies. The answer token flips then self-corrects: maybe intervention is not durable? Need note continuations self-correct to spider after first token flips. So maybe L25 changes immediate next-token but not full generative behavior. If goal is final answer, not enough. Missing long-form final answer scoring. L25 +1.95 log-odds shift but self-correction means downstream blocks restore spider. This is important for location: after built/before suppressed? The first token flips but downstream self-corrects, indicating suppression/readout at later layers? Actually the continuation after first token "Wait, that is incorrect... spider" indicates model generated donor token then corrects. The edit at L25 adds donor components at every decode call? Need examine: last-3 prefill + every decode call? Condition? It says replacement equation at C=1.5, last-3 prefill + every decode call. So at every decode call source positions are last 3 prompt tokens + every decode call? Wait source positions last 3 prompt tokens + every decode call continuous coverage. It edits every token including generated answer? If edit at every decode call, should be persistent? Yet self-corrects. Maybe because donor answer token "dog" not consistent with question "spider", model's pretrained context overrides? Or because edit is applied to all positions but donor state from donor prompt? Need parse. They see first answer token flips to donor answer (dog), then continuation self-corrects to spider. This suggests the edit influences next-token logits but not full semantic computation. Intervention at L25 maybe only local readout, not durable; downstream blocks can recompute correct answer from context. This is a key failure mode.

Need decide maybe intervention should act at multiple layers: early to build components? But evidence says L20 weak. Could act at L25 and late output to prevent self-correction? But no evidence. Need not pick multiple unsupported. We can say single L25 is best supported; multiple layers only if self-correction persists and late-site location run demonstrates downstream override. But prompt asks decide where an intervention should act — early (their suggestion L3), where components are built, after built/before suppressed, or at multiple layers. We can answer: where components are built/peak (L25 in current selector), not L3. Maybe "after built/before suppressed" could include L30? Need clarify site choices. We can state current measured support: L20 (before build) no; L25 (build/peak) yes. L3 is far earlier: likely even less support; no evidence. For final readout/multiple: no positive evidence, and late-block energy evidence does not identify stable suppression, so don't target after suppression based on current labels. Next check: same-procedure location comparison including L25, L30, L32; late-selector (29,30,32) and long-form final-answer scoring, not just first-token log-odds. If L30 or L32 same-procedure performs better on final answer and avoids self-correction, update to act after built/late. If late-selector shows L30? Hmm.

Need maybe reconstruct method and list distinctions/assumptions/failure modes/alternative formulations/experiments. The user asks "Reconstruct the method from attached primary evidence and pseudocode. Starting from that reconstruction, list the distinctions, assumptions, possible failure modes, alternative formulations, and experiments that you think matter. Use your own organization and order." So need provide not just decision but a structured review. Since oververbosity desired 5, moderate thorough. Need cover:

- Method reconstruction:
  - Select suppressed directions by readout logits rise between early/peak and fall between peak/output. For each token position last-4 window? Actually per token position rank-8 bases; union across window; keep top 8 singular vectors for source/donor projectors. Intervention equation h' = h + C(P_d d_o - P_s h) at active positions, C=1.5. Donor state at same layer, end-aligned offset. Decode with frozen donor state and common projector. Controls: C0; random projectors.
  - Diagnostic energy: E_l = ||P h_l||^2, block writes etc. selected-token readout decomposition.

- Distinctions:
  1. selection criterion (readout rise-fall) vs causal suppression/removal. Need distinguish directions selected by logits from behaviorally suppressed content.
  2. fixed projector vs per-site bases: same projector applied across sites may not align with components at each site. At L20/L25 maybe components built later? But same projection.
  3. donor state at same intervention layer vs donor template/projection. At L20 donor state maybe no components.
  4. "semantic strength" cannot be compared across layers using raw norms; need readout-based or causal equivalence.
  5. first-token log-odds vs full generation/final answer; self-correction.
  6. source vs donor projectors separately vs common; top8 union arm only top 8 singular vectors (maybe truncation). Need mention unguarded full_union invalid due null columns.
  7. The equation subtracts P_s h and adds P_d d; if P_s and P_d are different subspaces, source removal may remove source components, donor addition may add donor components but may not replace same directions. This is not a pure direction edit. Need note possible failure.
  8. Projector fixed from last-4 window; may include many non-causal directions.

- Assumptions:
  - Decomposition of logits through readout directions with row-normalized unembedding and final norm gain is meaningful.
  - Rise/fall in readout indicates constructed then suppressed semantic component.
  - Mean-centering scores removes common gain; maybe okay.
  - Last-4 positions adequate.
  - Rank-8 top singular vectors capture necessary content; truncating union to top8 may lose relevant directions and include irrelevant.
  - Donor state at same site retains desired components; source/donor alignment sufficient.
  - Linear additive residual edit at one layer can affect downstream processing.
  - Per-token vs union across positions.
  - Last three blocks are suppressors because readout falls across them; but not causal.

- Failure modes:
  - Selection artifact: selected tokens falling by construction; 753/768 pairs losing is not independent.
  - Energy increase in projector span while selected numerators fall: possible rotation, not removal. If intervention subtracts fixed directions but downstream writes new energy, ineffective.
  - L25 first-token flip but self-corrects; edit not persistent in final answer; might be local logit shift not semantic replacement.
  - L20 weak because components not built; early L3 likely worse, but no direct evidence; maybe early intervention could shape computation but current projector won't capture early primitives.
  - Fixed projector from old detector layers may mislabel late blocks; late-selector planned.
  - Random controls not magnitude-matched; cannot rule out generic norm effect? But random near zero, so okay.
  - L25 effective but maybe due donor state at L25; if site changes, donor state could be different.
  - Top8_union truncation may discard multi-token components; full_union invalid not robust.
  - 12 dev question sample small; split naming-dog vs ants/property suggests only certain prompts affected; generalization limited.
  - Coherence metrics r2 <=0.12 but 1-2 cells cap at 128 tokens; possible degenerate outputs.

- Alternative formulations:
  - Instead of subtracting P_s h and adding P_d d, use difference of projections at same site; or use common subspace (intersection) to avoid injecting out-of-subspace donor; do targeted direction ablation/addition with per-site bases.
  - Causal intervention: knock out candidate directions late and observe answer loss; add donor directions early to see if downstream preserves.
  - Use path patching / activation patching from donor prompt at a site, not projector.
  - Use local replacement at only final readout or unembedding to distinguish readout suppression from residual computation.
  - Use counterfactual donor with opposite answer and measure final answer (not first token).
  - Use equivalence-class or semantic proxy: train linear probe? 
  - Late-selector (29,30,32) to isolate what last three blocks specifically suppress; maybe use causal tracing of block writes.
  - Intervention at multiple sites with common per-site donor states.

- Experiments that matter:
  1. Running location OAT at L3/L25/L30/L32 with same construction, report final-answer accuracy and first-token swap; include C0/random.
  2. Late-selector run (29,30,32) to ask what late blocks specifically suppress; then intervene at L30 vs L32.
  3. Ablation-only experiment: subtract P_s h at L25/L30/L32 without adding donor; see if source answer is removed. If late blocks suppress, removing at L30 may have no effect because already suppressed; if L25 removal works, component causal.
  4. Donor-only addition experiment to disentangle addition vs subtraction.
  5. Persistence/final scoring: measure exact match/consistency of full sampled answer, not just next-token log-odds; self-correction rate.
  6. Cross-layer basis alignment: compare P_s at L25 vs L30 vs L32; measure principal angles between corresponding selected bases? Need code? They can compute overlap. If bases rotate, fixed projector misses late directions. 
  7. Causal tracing of block 29/30/31 contributions: intervene to freeze/ablate block outputs and read out selected token logits; use path patching to identify suppression.
  8. Use donor state at multiple sites and magnitude-match random controls; random projectors with same norm maybe.

Need maybe include mathematical expression/pseudocode for proposed test. We can provide concise pseudocode for causal ablation or late-selector? User says may. We can include one or two pseudocode.

Need answer "identify what the LAST THREE blocks (29,30,31) suppress". Based on evidence: We can say directly supplied evidence does not show a stable suppressed semantic component; it shows:
- Under the fixed projector, total projected energy rises from
## Final answer call answer

## What the last three blocks (29,30,31) suppress

**Directly shown by the supplied material:**

- The selection criterion itself defines the target: per-token, rank-8 readout-direction subspaces whose selected-token logits rise from layer 23 to 25 and fall from layer 25 to 32. Under the follow-up selector (29,30,32), the target is rise across block 29 and fall across blocks 30–31.
- On 12 dev questions, selected-token readout numerators fall from h30 to h32 by −84% (753/768 pairs lose), while the RMS denominator rises +57%. This is arithmetically the definition of suppressed readout for those directions.
- Total absolute energy in the union span rises h30→h32 (86.9 → 129.7, 23/24 prompts), so the h30→h32 fall is not energy removal from the whole span; it is direction replacement within an energy-growing span.
- On 4 canonical short Fact prompts, block 31 removes absolute span energy on source (−20.7) and control (−3.2) but not on the dog name.

**My inference about what blocks 29–31 do, ordered by confidence:**

1. Block 29 builds the component: its projected-energy write (+45.0) is by far the largest of any block, far exceeding 27 (+11.3), 28 (+9.5), 30 (+6.4). This makes the proposed late selector (rise across 29) mechanistically coherent.
2. Blocks 30–31 rotate or replace the direction rather than globally decaying it: the span grows in total projected energy while the selected numerator collapses, which requires energy moving into orthogonal directions inside the span (or cancellation that preserves norm).
3. The suppression is not universal: source and control Fact prompts lose span energy at block 31 but dog prompts gain it; dev-question block 31 energy change is positive. The apparent “suppression” is token- and position-specific, not a block-level downweighting of the whole span.

**Directly shown limitation:** the selection favors rise-then-fall, so the 84% fall is partially an artifact of choosing directions by their fall. The useful evidence about blocks 29–31 is the energy table and numerator analysis, and those are descriptive, not causal.

---

## Decision

**Intervene at or after block 29 (post-build), not early at layer 3, and not only at the final readout; a multi-site correction is preferable, with one site after block 30 as the primary intervention.**

The decisive basis: block 29 shows the largest projected-energy write (+45.0 at h29→h30), and the h30→h32 numerator collapse (−84%) occurs afterward, with block 31 making a second large positive write. If you edit at layer 3, you remove the source component before it is built, which means the donor component rides through blocks 29–31 as an untracked direction; the construction does not protect it from whatever operation created the suppression. The L20 result (swap +0.20 to +0.25) versus L25 (+1.95 to +2.85) already shows that editing where the component is present dominates editing where it is nearly absent (projected fraction h20 = 0.0126 vs h25 = 0.0190). The strongest hypothesis that fits both the energy table and the L25 flip-then-correct behavior is that the operative mechanism is downstream of block 29. An edit at layer 3 would be overwritten by it.

**Strongest objection:** the h30→h32 fall is readout fall, not proven removal in residual space, and the total span energy rises. If blocks 30–31 do not remove the component but only rotate it into directions that no longer project onto the readout, then intervening at h30 replaces the wrong basis direction — the originals may have been destroyed earlier, or later than assumed. The L25 flip-then-correct behavior also fits the reading that the component set is still mutable there but is actively overwritten afterward; replacing at h25 may simply reset the race, not win it.

**Second objection:** the comparison across layers is confounded by projector construction: the bases are selected from readouts at fixed layers (23, 25, 32), so a projector applied at layer 3 may target noise or low-energy structure, while the same projector at h30 targets a direction that has just received the largest block write. Any layer comparison using the same projector is not a clean causal location comparison; it measures what this particular projector catches at each site.

**What would change my mind:** a location sweep showing that editing at h30 produces a large swap (comparable to or exceeding L25) but with the continuation staying on the donor answer — i.e., the suppression not re-asserting. Additionally, if the same procedure at layers 29, 30, 31 shows a monotonic increase in swap, that would support the post-build site; if swap moves to a late maximum (e.g., layer 30 or 31), it would rule out early replacement. If the L25 flip-then-correct appears in all post-build sites, it would falsify the claim that L25 was merely “too early.”

---

## Distinctions

**1. Readout fall ≠ component removal.**
**2. Component build ≠ component maintenance.**
**3. Span energy ≠ semantic strength.**
**4. Direction rotation ≠ suppression.**
**5. Source-position selection ≠ target-position intervention.**
**6. Norms across layers ≠ comparable semantic strengths.**
**7. A fixed projector per layer ≠ a fixed semantic direction across layers.**
**8. Full-union vs top8 projectors ≠ equivalent interventions.**
**9. Prefill persistence ≠ decode coverage.**
**10. Descriptive energy table ≠ causal mechanism.**

Of these, 1 and 2 are the most consequential: the entire location decision depends on distinguishing when the component is constructed (block 29) from when its readout falls (blocks 30–31), and neither is directly shown to be the point where an edit would stick.

---

## Assumptions worth flagging

- **Assumption:** applying the same rank-8 replacement equation at different sites tests the same underlying component. **Risk:** the subspace selected from (23,25,32) readouts may not correspond to a stable direction that persists in the residual stream across layers; it may be a different direction at each site. The energy table only shows projected energy into the union span, not cross-layer basis correspondence.
- **Assumption:** donor state at the same intervention layer is the appropriate donor representation. If the component is built by block 29, a donor state at layer 3 contains no comparable built component, and a donor state at h25 is mid-rise; only h30+ contains the fully built donor version.
- **Assumption:** C=1.5 is in the linear regime. The L25 flip-then-correct behavior shows the intervention does not stably override downstream processing, so the linearity assumption (or the completeness of the projector) is already in question.
- **Assumption:** the last-4 prefill positions are sufficient coverage. The source component may be built over longer ranges.
- **Assumption:** the finite-samples table (12 dev questions) generalizes. The energy table means are over 24 prompts and show large variance across condition types (Fact vs dev, source vs control vs dog).

---

## Possible failure modes (by site)

**At layer 3:**
- The projector targets near-zero energy: projected fraction at h0 is 0.148 only due to a small-denominator artifact; at h20 it is 0.0126. The edit adds donor signal on top of an embedding-space direction that has not yet been integrated into the component.
- The component is built later (block 29) from scratch, so the removed direction is not the one that will later matter.
- The L20 result (+0.20 to +0.25) is consistent with a small or null effect from this kind of early site.

**At layer 25:**
- The component is still rising (selection peak layer is 25); editing at h25 removes a partially built component and inserts a fully built donor component, creating a competitor that wins the first token but loses the continuation as blocks 30–31 rebuild the original.
- The L25 flip-then-correct is the primary evidence for this failure: first token flips (狗) then self-corrects to spider. This suggests the intervention is strong enough to affect the next-token predictor but not strong enough to suppress the later re-assertion.

**At layer 30:**
- The component is built (post-block-29), but the suppression mechanism may have already begun. Editing here replaces a direction just before its readout falls, which may be the optimal site if the suppression is a readout-time operation in blocks 30–31.
- Failure mode: if block 31 rotates or replaces directions inside the span, the edit may be overwritten one block later.

**At layer 32 (final readout):**
- Editing at h32 is equivalent to steering the readout directly, bypassing the suppression mechanism. This should produce the largest per-call readout shift but leaves any downstream generation mechanism (self-correction, repetition) untouched; it does not remove the suppressed component from the model's internal processing, so continuations may still self-correct.

**Multi-site intervention (most justified):**
- Remove at h30 (post-build) and re-assert at h31 or h32 to counter the block-31 write. This addresses the observed two-phase energy write (block 29 build, block 31 second write) and the flip-then-correct at L25.
- Failure mode: if the suppression is a distributed rotation across blocks 29–31 rather than a single block-31 operation, a two-site edit may not cover all directions.

---

## Alternative formulations

1. **Cross-layer basis correspondence edit:** instead of applying the same projector at different sites, track the component through the residual stream using a causal tracing or patching procedure that identifies at which layer the source and donor components occupy the same readout-relevant directions. Then apply the replacement where the donor component is strongest relative to the source.

2. **Post-hoc projection onto readout directions at the final layer:** since the observed suppression is readout fall, one could define the intervention as a constraint on the final-layer readout rather than on residual directions: enforce \(\Phi_{\text{edited}} = \Phi_{\text{donor}}\) at the answer position by adding a correction only at layer 32. This tests whether the residual-level operation is necessary at all.

3. **Counterfactual erase-and-rebuild:** instead of the common_replace equation \(h' = h + C(P_d d_o - P_s h)\), use a two-step version: first remove the source span (\(h_{\text{clean}} = h - P_s h\)), then add the donor span. This disentangles the remove and add coefficients and allows testing whether the suppression mechanism reacts to the removed residue or to the added donor.

4. **Layer-specific projection:** rather than one fixed P, recalculate P per layer from the same tokens' readout directions at that layer. This addresses the cross-layer correspondence issue explicitly.

---

## Experiments that matter

### 1. Same-procedure location sweep (already running, essential)
Run the same common_replace equation at L3, L20, L25, L29, L30, L31, L32 with the same projectors. Compare swap, prefill persistence, and continuation coherence. If swap increases monotonically toward L30/L31, early is wrong; if it peaks at L25 and falls, the suppression is already fixing things downstream; if it peaks at L30, the post-build site is correct.

**Expression:** for each site L and each condition arm, compute
\[
\text{swap}(L) = \log \frac{p_{\text{donor}}(\text{next token } | \text{ edited prompt})}{p_{\text{source}}(\text{next token } | \text{ edited prompt})} - \log \frac{p_{\text{donor}}(\text{next token } | \text{ clean prompt})}{p_{\text{source}}(\text{next token } | \text{ clean prompt})}
\]
and compare to the measured baseline: L20 ≈ +0.2, L25 ≈ +1.95 to +2.85.

### 2. Late-block temporal decomposition (the planned (29,30,32) selector)
This tests whether the suppression is specifically a late-block phenomenon. If the same procedure on (29,30,32) selectors produces a much larger swap at L30 than at L25, it confirms the post-build site; if it produces a smaller swap, the original (23,25,32) selection is capturing a different component than the one blocked by blocks 29–31.

### 3. Cross-layer basis tracking (to resolve confidentiality of direction)
For each pair (l, l') in {25, 30, 31, 32}, compute the subspace similarity between the selected source bases:
\[
S_{ll'} = \| P_{ll'} \|^2_F / \min(d, r)
\]
where \(P_{ll'}\) is the projector overlap between the rank-8 bases at l and l'. If \(S_{30,31} \gg 0\), the component persists; if \(S_{30,32} \approx 0\), the suppression is a rotation rather than a removal. This directly tests the "direction change is a labeled hypothesis, not measured" caveat.

### 4. Block-31 ablation (causal test)
Run the model with block 31's output replaced by its input (or by a clean prompt's block-31 output) and measure whether the selected-token readout fall from h30 to h32 is eliminated. If yes, block 31 is the active suppressor; if not, the suppression is distributed across 29–31.

### 5. Intervention-after-suppression test
Apply the common_replace at L32 (final readout) only. If swap is large and stable (continuation stays on donor), the suppression is readout-time; if swap is large but continuation flips back, the suppression is internal and cannot be bypassed at readout alone.

### 6. Magnitude-matched random control
The L25 experiment already suggests randoms ≈ 0 with smaller applied norms; a magnitude-matched random with the same norm as the applied edit would cleanly separate "subspace specificity" from "norm injection."

### 7. Cross-format test
The energy table already shows Fact vs dev differences at block 31. Run the same experiment on naming-dog, ant, property, and control cells separately to see whether block 31's suppression is specific to the naming-dog component.

---

## Missing evidence / uncertainties

- **Why the historical recovered reference (additive template-attenuation, L20) produced +10.01 swap and 6/12 primary success while the current projector-replacement at the same layer produced ≈ +0.25 is not established.** The current evidence does not support concluding that the projector form is the cause; the difference could be due to donor state, equation form, or data split. Until this is resolved, the absolute swap magnitudes are incomparable across methods, and the location conclusion is only valid within the current equation family.
- **Cross-layer basis correspondence is unmeasured.** The decomposition table shows energy in the union span, not whether the span direction at h30 is preserved at h32. The claim "suppression rotates direction" is a hypothesis.
- **The (29,30,32) selector is not yet run.** The location conclusion is currently based on the energy table and the h30→h32 numerator fall from the (23,25,32) selector. The planned late-selector variant would confirm or refute.
- **No causal manipulation of blocks 29–31 is reported** (only descriptive energy tables). Without a block ablation, the inference "block 31 suppresses" is correlational from a construction that selects falling readouts.
- **The norm comparisons (L25 randoms with smaller applied norms: 184–417 vs 533–787) mean the random control is not fully controlled**; a magnitude-matched random is missing.
- **The L25 first-token flip then continuation self-corrects to spider is strong but anecdotal (one named cell).** We lack continuation-level success rates across all 12 cells.

---

## Bottom line

The last three blocks build (29), then remodel (30–31) the selected component. The buildup is directly supported by the energy table; the remodeling is supported by the numerator collapse with span-energy rise. The intervention should act after the build and in a way that counters the remodel: a post-block-30 site with a second correction near block 31 or at the final readout. Early layer 3 is mechanistically wrong for this component: the projected fraction is near zero, the component is built much later, and the historical L20 result confirms weak effect. The decisive test is the same-procedure location sweep; the decisive missing evidence is whether blocks 30–31 rotate directions inside the span or causally reduce them, and whether a late intervention produces stable donor continuations rather than the flip-then-correct seen at L25.

## Completion

- outcome: `completed_after_follow_up`
- trace: `/workspace/2026/suppressed-activations-batchwork/slop/reviews/2026-09-12_deepseek-v4-pro-0813_science_pass1_deepseek.trace.jsonl`
