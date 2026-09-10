---
requested_model: moonshotai/kimi-k3
max_tokens: 4000
final_tokens: 20000
reasoning_effort: low
input_bytes: 8060
trace: /workspace/2026/suppressed-activations/slop/reviews/2026-09-09_kimi-k3_span_pass1_kimi.trace.jsonl
generated: 2026-09-09T14:12:22.912784+00:00
---

# bounded completion

## First call reasoning

We need produce the review.
## First call answer

# Independent review: span-corrected reflection, identity–attribute dissociation, and the C=2 overshoot question

## 1. Reconstruction of the method (what the pseudocode and files directly show)

**Offline stage.** Fit an orthonormal basis $U$ (rank $r=4$, at layer 20) from template residuals. Compute the template mean difference $d = \mu_{\text{target}} - \mu_{\text{spider}}$, project it: $\Delta = UU^\top d$, then rescale so $\|\Delta\| = \|d\|$ ("match_component_norm" — note this restores the *pre-projection* norm, so the in-span delta can be longer than a genuine projection; the residual energy of $d$ outside the span is effectively folded into the span direction).

**Online stage.** At the edited position, every decode step:

$$\hat h = h + C(\Delta - Ph), \quad P = UU^\top$$

In-span: $P\hat h = (1-C)\,Ph + C\Delta$. At $C=1$ this *sets* the span component to a constant; at $C=2$ it *reflects*: $P\hat h = 2\Delta - Ph$. The off-span component $(I-P)h$ is untouched at every strength. Random control: same reflection equation, $\Delta$ replaced by a norm-matched Gaussian direction.

**Protocol facts shown:** source prompt always the spider prompt; four edits per animal (prefill last 3, decode last 1); continuous steering; C=0 identity cells verified (steered == Base); random-direction deltas in earlier naming work had ~8× larger applied norms than real deltas and produced garbage — i.e., random is a *stronger* disruption, so random-control success can't be dismissed as weak perturbation.

## 2. What the primary evidence directly shows

1. **Identity transfers at C=2, attributes do not.** legs-dog-C2: text names and describes a dog, first digit is `2` while the text itself states dogs have four legs. prop-dog-C2: text says "Dogs are mammals" and answers "No" to the mammal question. This is a within-generation contradiction — the model asserts the attribute in prose and denies it in the answer slot.
2. **The dissociation can be inverted.** legs-dog-RAND: digit moves to `4` (target-correct) while the text retains spider identity ("the animal is known as a spider"). So the digit answer is not slaved to named identity, and the name is not slaved to the digit. A *random* direction achieved attribute-movement-without-identity-movement.
3. **legs-ant-C2 works cleanly** (first=`6`, coherent ant text, no loop), so the identity/attribute split is not universal across targets. legs-ant-RAND stayed at `8` (source-correct), unlike legs-dog-RAND.
4. **prop-ant-C2 loops** (r2=0.370, self-contradictory "Unlike ants, the ant…" repetition), a qualitatively different failure mode from prop-dog-C2's clean contradiction.
5. **Naming-only probes (base, same construction) were clean**: coherent dog/ant paragraphs to EOS, no correction loop. So the pathology appears on *property-judgment prompts*, not on free naming.

## 3. My inferences (labeled as such)

**(I1) The name is cheaper to move than the binding.** The U-span appears to contain a direction along which the *referring expression* ("the animal is a dog") is controlled, while the decision variable for the yes/no or digit answer is computed from coordinates that the C=2 reflection moves inconsistently — or that live partly off-span and are driven by the (unedited) spider prompt's earlier context. This is an inference; the evidence only shows behavioral separation.

**(I2) The two named hypotheses are not exhaustive.** The question asks: name-pointer-without-bindings vs. reflection overshoot of attribute coordinates. A third structure fits the data at least as well: **the answer slot is conditionally decoupled**. Notice the dog-C2 answers are not merely wrong — they are *internally contradicted by the same generation*. That looks less like "attributes moved too far" and more like "the proposition being evaluated is still about the spider" — i.e., the answer head reads a *binding variable* (which entity the question is about) that the edit does not move, while the *surface description* reads the edited coordinates. Under this reading there is no "attribute vector" being overshot at all; the yes/no head is evaluating (spider, mammal?)→No and (spider, antennae?)→No, which are both correct-for-spider. Both C=2 property answers are exactly the spider-correct answers. That is a striking regularity the overshoot hypothesis does not naturally predict.

**(I3) The RAND legs-dog cell is the most diagnostic single observation and it cuts against pure overshoot.** If C=2 reflection generically overshot attribute coordinates into garbage, a random direction shouldn't land the digit precisely on `4`. A norm-matched random direction moving the digit to the target-correct value suggests the digit answer is controlled by a *low-dimensional, easy-to-nudge* variable (plausibly a number/logit feature that many directions can flip at this magnitude), whereas identity naming requires the specific Δ direction. This asymmetry — name hard, digit easy — reframes the question: maybe nothing "encodes a name pointer without attributes"; maybe the two readouts have different sensitivity curves $f_{\text{name}}(C, \theta)$, $f_{\text{digit}}(C, \theta)$ in direction space.

**(I4) legs-ant-RAND staying at `8` weakens (I3) only partially.** It shows the digit is not *always* movable by random directions; movability may be target/prompt-specific (dog `4` vs ant `6` vs spider `8` — 4 is the modal "animal leg count" in the corpus; flipping to 4 may be far easier than flipping to 6). This is a confound the current cells cannot separate.

## 4. Distinctions the current design does not yet make

- **Setting vs. reflection.** C=2 is chosen presumably because C=1 failed or was untested, but the C-sweep is not shown. If C=1 (set span to Δ) also transfers name without attributes, the "reflection overshoot" hypothesis dies immediately — nothing is overshot at C=1. This is the single most important missing cell.
- **Answer-head readout vs. prose readout.** The contradiction "Dogs are mammals … answer: No" implies the *token position of the answer* reads different information than the prose positions. Probing only at the edited position may hide this.
- **Direction identity vs. norm.** Random controls matched for norm but sampled one seed ("random0"). A single random direction is an anecdote, not a control distribution.
- **Digit movement ≠ attribute binding.** "4" appearing first could be a surface bias (dog contexts → "four legs" collocations) rather than a bound attribute. Conversely, "2" in legs-dog-C2 is not even the spider-correct value (spiders have 8) — it's unexplained by *either* hypothesis as stated. This `2` is an anomaly worth flagging: name=dog, digit=2, prose=4. Three inconsistent readouts in one generation.

## 5. Assumptions embedded in the construction

1. The mean template difference is the right direction — assumes linearity and that context-averaged means commute with per-instance steering.
2. Rank-4 span suffices; everything attribute-relevant either lies in it or is safely untouched.
3. Norm-matching to the *unprojected* $d$ is justified — if the true projection is much shorter than $\|d\|$, Δ is artificially inflated, which at C=2 doubles the inflation. Quantify: report $\|UU^\top d\|/\|d\|$.
4. The same (U, Δ, C) is valid for both animals and both prompt types — the legs/property divergence between dog and ant already strains this.
5. The edited-position-only intervention leaves all key/value context of the spider prompt intact upstream of layer 20 in other positions — the model retains a full spider representation the answer head can read.

## 6. Cheap discriminating tests

**T1 — C-sweep (discriminates overshoot vs. pointer-without-bindings).**
Run $C \in \{0, 0.5, 1.0, 1.5, 2.0\}$ on legs-dog and prop-dog.
- *Overshoot predicts:* an intermediate C (likely C=1) where name *and* attribute both transfer, with attribute degrading as C moves past 1 — a non-monotone attribute curve.
- *Pointer-without-bindings (or decoupled answer slot, I2) predicts:* name transfers at C=1 (and below), attribute never transfers at any C — a flat attribute curve.
This is the cheapest decisive experiment; no new machinery.

**T2 — Swap which stream is edited.** Steer the *answer-token position* only (not the prefill), or steer only prefill and not decode. If the answer slot reads an unedited binding variable, decode-only steering should fix the answer without touching prose; prefill-only steering should leave the contradiction. This directly tests (I2).

**T3 — Patch the answer readout, not the representation.** Take a clean *target-prompt* run ("How many legs does a dog have?"), and at the answer position transplant its span component $Ph_{\text{target}}$ into the steered spider run's answer position. If the digit flips to 4, the answer head's input exists and is localized; if not, the binding lives off-span or in attention from unedited positions.

**T4 — Random-direction distribution, not one seed.** Sample $k\ge 20$ random deltas, matched norm, C=2, legs-dog. Report the distribution of first digits. If many land on `4`, digit is a generic easy readout (supports I3). If legs-dog-RAND's `4` was a fluke, the "inverse dissociation" claim should be softened.

**T5 — The anomalous `2`.** Score the logit ranking of digits {2,4,6,8} at the answer position across C. If `2` rises monotonically with C, the reflection is moving a *number* coordinate through intermediate values (spider 8 → … → dog 4 via 2? no — 2 is not between 4 and 8). Actually `2` being off the interpolation path is evidence *against* any linear-overshoot story in digit space; quantify this rather than treating `2` as noise.

**T6 — Off-span ablation.** Apply $h + C(d_{\text{full}} - d_{\text{span-part}})$ variants: steer with the off-span residual of $d$ alone. If attributes transfer with off-span steering while name transfers with in-span steering, the "pointer in span, bindings off span" picture is confirmed directly.

## 7. Failure modes of the construction itself

- **Reflection instability:** at C=2, $P\hat h = 2\Delta - Ph$ amplifies any time-varying $Ph$; the prop-ant loop (r2=0.370) is consistent with the edited position fighting its own context step to step.
- **Inflated Δ from norm-matching** (§5.3) making C=2 effectively a >2× intervention.
- **Single template context:** Δ estimated from one (or few) template phrasings; "mammal" and "antennae" judgments may need directions never present in the template contrast.
- **Answer=None parsing** (legs-dog-C2): `first='2'` but `answer=None` — the harness's answer extraction failed; some reported dissociation may be partially a parsing artifact. Check the extraction rule before interpreting.

## 8. Missing evidence

- C=1 cells (critical).
- Logit-level data at the answer position (all claims rest on sampled text).
- Multiple random seeds; C-sweeps for RAND.
- Layer sensitivity (only L20 tested).
- The reserved strings (spinneret naming, limb count, live birth) remain unused — fine — but no replacement binding probe that isn't yes/no or a digit (e.g., open-ended "how many…" forced-choice vs. free) exists yet.
- n's differ across cells (56–128) with no stated stopping rule; r2 given but no per-cell power analysis.

## 9. What would change my mind

- If T1 shows attribute transfer peaking at C=1 and collapsing at C=2, I'd adopt the overshoot account and drop (I2).
- If T2/T3 show the answer slot's behavior is fully determined by the span component at the answer position, I'd drop the "off-span binding variable" inference.
- If T4 shows random directions almost never move the digit, I'd retract (I3) and treat legs-dog-RAND as a coincidence, which would restore the Δ-direction-specific view of attribute encoding.
- If the `2` in legs-dog-C2 turns out to be a parsing artifact of a malformed first token, the three-way inconsistency collapses and the case for decoupled readouts weakens.

## 10. Summary position (no winner picked)

The data robustly show identity and attribute readouts are separable under this intervention, in both directions (C2-real vs. C2-random). But the current cells cannot distinguish (a) a name-only pointer in the span, (b) C=2 overshooting attribute coordinates, or (c) an unedited binding/context variable feeding the answer head — and (c) fits the "both property answers are exactly spider-correct" regularity better than either offered hypothesis. The C-sweep (T1) plus answer-position patching (T3) are the cheap discriminating experiments, and both are runnable with the existing harness.

## Completion

- outcome: `complete`
- trace: `/workspace/2026/suppressed-activations/slop/reviews/2026-09-09_kimi-k3_span_pass1_kimi.trace.jsonl`
