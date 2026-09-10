# Recovery decision: the common candidate and what remains untested

Part 1 of the recovery assignment. One decision, evidence-backed. PI[claude].

## The candidate

L20 span-corrected template-attenuation replacement, C=1.5 (sweep `span-correction-sweep`,
condition index 3). Exact recovered config: detector_layers (18, 20, 32), rank 8,
persistent_rank 4, intervention_layer [20], intervention_positions 3, readout_positions 4,
template_contrast=True, template_state_span="attenuation", aggregation union, delta_component
"difference", match_component_norm=True, restore_residual_norm=False, span_correction=True,
continue_generation=True, prompt_mode chat-assistant-prefill, 128 max_new_tokens. Source: config
block in `out/2026-09-10_naming-dog-C1.5/result.json` row 0, from `slop/naming_c1_batch.json`
condition_index 3.

Why best-supported: it is the only construction with clean verified transfers on BOTH animals
for TWO question types -- naming (dog: "狗 (Dog) ... The dog is a domesticated canine ...";
ant: "Ant ... The ant is a small, social insect ... colonies") and legs (dog: "4 ... The animal
is a dog, which is a domesticated canine"; ant: "6 ... The ant is a small, hardworking insect
... colonies ... pherom[ones]", p_tgt 0.969/0.982). Property is answered (ant "Yes", dog "No")
but property transfer is answer-movement, not established concept transfer; the corrected
answer-position measurements put the yes/no decision largely outside the edited span.

## State-dependent behavior it already has

The span-correction equation is h' = h + C(Δ − UUᵀh). The −UUᵀh term is evaluated at every
patched position and every cached decode step from the CURRENT state, so the removal part is
already position- and step-adaptive: what gets removed depends on what the model is currently
representing. The donor term Δ is fixed (frozen donor coordinates).

## Genuinely distinct prior construction that was omitted: synchronized donor updating

Job 743 (2026-09-08, `out/2026-09-08_131500_synchronized-attenuation-ant`) ran the SAME
replacement with donor coordinates updated during generation from the source-selected generated
tokens (its own cache). Identical settings, donor updating flipped the ant outcome from spider
identity ("The animal is a spider, a member of the class Insecta") to ant identity ("The animal
is an ant ... colonies ... pheromones"), same first-token probabilities. Dog still failed
(first token "2." before dog prose). This is materially different (the donor side is also
state-dependent) and was not carried into the frozen candidate. It must be preserved as the
one distinct adaptive construction with a demonstrated identity-preserving effect -- on one
animal, one layer (L24), one strength, unvalidated readouts.

Also recovered: distributed L16-20 half-template edits (job 549 cond 27) produced complete,
naturally-ending ant and dog explanations at C=1 (p6 0.963, p4 0.928) -- full-residual
multi-layer, not suppressed-only, and not carried forward either; clamps (jobs 547/548) did not
solve both demos and their threshold is not an established semantic detector.

## What remains UNTESTED (not "conclusively tested")

The user's layer/token adaptation has NOT been conclusively tested by the static pair selectors:
the max-agreement/consensus selectors were rank-1, applied at fixed last-3+decode positions.
Untested: (a) synchronized (state-updated) donor coordinates composed with the L20 candidate;
(b) multi-layer distributed edits on the current detector construction; (c) token-local edits
at the pair's own positions rather than the decision window; (d) property transfer under any
construction. The selector family's one cross-concept continuation (dog question, donor answer
4 first) is donor-answer leakage via a decision position -- possible explanation, not
established.

## Decision

Freeze the L20 C=1.5 span-corrected candidate as the common procedure for the reliability
evaluation, with donor information fixed (donor prompt residual difference at the L20 readout
positions; no answer tokens, no continuation content from the donor). Proceed to replay +
regression verification now. Record synchronized donor updating as the preserved distinct
construction and the four untested items above as the honest boundary of the freeze.
