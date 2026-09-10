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
representing. The donor term Δ is fixed (template-mean donor-minus-source residual difference
projected into the span). CORRECTION (supervisor review): the actual `span_corrected_delta`
branch (scripts/demo.py) never reads the `match_component_norm` config field -- the equation is
raw: no component-norm matching and no residual renormalization anywhere. An earlier draft of
this document and of the journal described the candidate as "template-mean Δ with norm
matching"; that was read from the config field, not the branch, and is wrong.

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


## Replay result (regression verification; tasks 1005/1006)

The C=0 identity controls pass on all six question/animal pairs (first answer equals the clean
base answer, swap_log_odds_shift exactly 0.0 -- logits identical to base). The candidate
reproduces the prior successes EXACTLY (bitwise-stable probabilities):

| condition | replay | original |
|---|---|---|
| legs-dog C1.5 | 4, p_tgt 0.9687 | 4, 0.9687 |
| legs-ant C1.5 | 6, p_tgt 0.9818 | 6, 0.9818 |
| naming-ant C1.5 | Ant, 0.0068 | Ant, 0.0068 |
| naming-dog C1.5 | 狗(Dog), 0.0062 | 狗(Dog), 0.0062 |

Property at C1.5 confirms the known failure with new detail: the answer stays No for both
animals while the identity moves -- dog ("The animal that spins webs is a dog, which is a
mammal" then answers No: self-contradiction, since a dog is a mammal) and ant (identity moves
to a honey bee, a THIRD animal). Property is identity-moves-answer-does-not, never coherent
transfer.

### Regression finding: the digit movement is not selector-specific

The in-span random direction control (C=2, one strength above the candidate's 1.5 -- the sweep
has no C1.5 random) moves legs-dog to 4 with HIGHER probability than the candidate (p_tgt
0.9851 vs 0.9687) while the identity becomes a cow; naming-dog becomes a cat (猫). So the digit
change is largely direction-agnostic: any in-span perturbation of this magnitude moves it. What
the semantic Δ adds is WHICH animal the continuation describes (dog/ant vs cow/cat/random), and
random edits also break identity (to a third animal) or degrade into repetition (bigram 0.46-0.56
on ant). The honest framing of the frozen candidate: the digit component of "success" is
non-specific; the donor concept's contribution is the identity substitution, and the property
type fails outright.

Note: random C=2 vs candidate C=1.5 is not strength-matched; no C1.5 random exists in the
sweep. This weakens the control and is recorded as a replay limitation.

### Verdict

Prior claimed successes REPRODUCE (regression verification passes; no fix needed before
freeze). The candidate's mechanism reading is corrected: it is a digit-mover (non-specific) +
identity-steerer (semantic), not a pure concept transfer, and property is a confirmed failure
with visible self-contradiction. This is regression evidence only, not reliability evidence.
