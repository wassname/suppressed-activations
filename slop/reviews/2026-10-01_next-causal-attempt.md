# Next causal attempt: one frozen concept-specific VJP direction

**Recommendation:** try offline, concept-specific vector–Jacobian products (VJPs), followed by a fixed additive intervention. Use **eight short generations**, not another calibration suite or sweep. This is a new preparation method, not a reference reproduction or literal hidden-component replacement.

Nothing was executed, changed, or queued. Readout2673 remains independent.

## Evidence behind the choice

Observed in the supplied logs:

- `out/2026-09-30_125606_jlens-one-pass/run.md`: full donor generates `4` and “The animal that spins webs is a dog.” Matched random retains `8`; the J projection generates `6`. This supports the disclosed selected count/name positive—not isolated concept replacement.
- `out/2026-09-30_142712_jlens-one-pass/run.md`: quarter-decode J projection changes dog’s initial answer to `8`, with `p(8)=0.642038`, versus Base `0.00720431` and random `0.00785263`.
- Under that same rule, `out/2026-09-30_142748_jlens-one-pass/run.md` still generates `inside`, despite a spider readout. Full donor instead generates `outside`, but retains `4` in the leg case. Thus neither intervention demonstrates common property transfer.

The paper provides motivation, not evidence this proposal works. `/workspace/2026/LUCID3_wikit/docs/papers/20260710_global_workspace.tex`, §Methods, distinguishes a concept’s “general disposition to verbalize” from “the particular use to which that concept is being put.” Its limitations also state that a bag of concepts does not reveal “how they are bound together.”

That distinction is this proposal’s main risk.

| Option | Assessment |
|---|---|
| Concept-specific VJP | Best next small attempt: changes the causal preparation distribution without adding a classifier threshold. |
| Generic concept probe | Admissible, but adds another correlational separation/transfer assumption after the documented donor-coordinate failures. |
| More fixed-J, layer, dose, or coverage variants | Do not reopen the retired configurations. |

## Prospective method

### Offline preparation

Keep Qwen3.5-4B at the existing pinned revision and **block15 output, residual16**.

Use the four templates in `data/dog_spider_donors_pronoun_v2.json`, instantiated for dog and spider: eight generic contexts. Append the fixed suffix ` is called a` to each. For example:

```text
'The animal is a dog. It is called a'
```

Differentiate the final-position naming contrast with respect to the block15 activation **at `It`**, before the naming suffix:

\[
g=\frac18\sum_{i=1}^{8}
\nabla_{h_{16,\mathrm{It}}^{(i)}}
\left[z_{\text{ spider}}^{(i)}-z_{\text{ dog}}^{(i)}\right],
\qquad
u=g/\|g\|.
\]

Use full-model logits, including the actual final normalization. Verify the two complete name strings are single tokens; do not silently substitute fragments.

Reasons:

- Both concepts and all four templates receive equal weight.
- The source position has the same token identity across pairs.
- The naming decision occurs later than the source position, rather than differentiating immediate name emission at the edited position.
- No leg counts, skeleton answers, evaluation prompts, or evaluation outputs enter preparation.

This still learns a **naming-sensitive direction**, not a proven referent representation. The delayed suffix reduces one immediate-output confound; it does not remove it.

### Freeze direction and scale

Let \(D=\mu_{\mathrm{spider}}-\mu_{\mathrm{dog}}\) be the existing **natural, unrescaled pronoun-donor difference** at residual16. Set

\[
a=D^\top u,\qquad \delta=a u.
\]

This is exactly the orthogonal projection of the donor difference onto the VJP direction. It supplies residual-unit scale without selecting a dose on evaluation outputs, and \(\|\delta\|\leq\|D\|\).

Require finite, nonzero gradients and record every gradient norm, \(a\), and the projection fraction. If \(a\leq0\), the donor-based scale contradicts the target-directed naming gradient: report that preparation failure rather than flipping its sign, replacing the donor, or increasing the dose.

For evaluation, freeze:

- final prompt position: \(h'=h+\delta\);
- every cached decode position: \(h'=h+0.25\delta\);
- observer: block23, recording only.

The quarter-decode schedule is inherited from the prior grammatical reverse-leg condition, not newly searched. Natural pronoun scale deliberately avoids restoring the much larger old noun-donor magnitude. It may be too weak; that is a substantive risk, not permission for a rescue sweep.

This remains **contrast addition**, not replacement of an identified component.

## Eight-generation experiment

Use greedy generation, at most32 tokens per condition. Freeze everything before any evaluation generation.

| Input | Conditions | Intended distinction |
|---|---|---|
| Existing dog leg prompt | Base; VJP addition; norm-matched random | `4`→`8`, with readable continuation |
| Existing dog body-relative skeleton prompt | Base; identical VJP addition; identical random direction | `inside`→`outside`, without property-specific changes |
| Irrelevant-referent arithmetic prompt below | Base; identical VJP addition | Arithmetic remains correct despite animal context |

Use the existing exact two property strings from `RELATIONS` in `scripts/english/08_jlens_one_pass.py`. The third prospective string is:

```text
'Fact: An animal that barks is nearby. The sum of 2 and 2 is '
```

Random uses one fixed seed0 unit direction, norm \(\|\delta\|\), and the same prefill/decode multipliers. This is a perturbation control, not a significance estimate.

The arithmetic pair tests whether animal steering indiscriminately corrupts an unrelated answer. It does **not** establish precise binding to one of multiple animal referents. A live global-J comparator is omitted to keep eight generations; historical results are context, not a matched causal comparison proving VJP superiority.

## What would support goal2?

The informative positive is the **same frozen intervention** producing spider-compatible answers on both properties, while retaining coherent continuations and arithmetic behavior. It would strengthen the case for reusable concept-level influence beyond name emission or a digit preference.

Report separately:

1. Target-answer movement on the fixed **two property attempts**, including failures.
2. Continuation coherence, with exact text—not repetition rate alone.
3. Arithmetic preservation.
4. Local applied deltas and later readouts.

A selected success may be shown with its disclosed denominator. One successful property is still partial positive evidence; there is no universal-success requirement. Conversely, target names in the readout or continuation alone do not establish hidden-component replacement. Generated hypothetical questions must not be mistaken for the model affirming contradictory facts.

Even a clean two-property positive would not prove a uniquely isolated hidden component. These are already-observed development prompts.

## Implementation and information boundary

The existing entry point is reusable, but **does not implement this proposal**. In `scripts/english/08_jlens_one_pass.py`, `main` sets:

> `torch.set_grad_enabled(False)`

and the donor hook currently applies:

> `edited = selected + donor_deltas[mode]`

Offline VJP preparation therefore needs an explicitly gradient-enabled stage, frozen model weights, an attached source activation, and verified backward support through the actual hybrid model. Gradient computation through the complete naming suffix must not be replaced silently with a detached lens approximation.

At evaluation, only the frozen vector, fixed schedule, and current activation are available. Base generations and block23 observations are evaluation evidence only. No backward pass, naming suffix, preliminary trajectory, or later-layer feedback is permitted on the current input.

Prospective budget: eight short offline forward/backward evaluations plus at most256 generated tokens, sequentially, within one ordinary300s local-GPU job. Actual backward runtime and memory are unknown. A timeout or unsupported backward path is an implementation failure, not a scientific negative; do not expand the budget or change the method silently.

## Predictions and residual risks

Illustrative planning weights—not measured probabilities:

- **45%:** naming/readout movement without shared property transfer.
- **25%:** negligible effect because the projected natural donor scale is small or the direction does not transfer.
- **15%:** useful cross-property behavioral transfer.
- **10%:** implementation, casting, or scoring defect.
- **5%:** other behavior.

The cheapest discriminator is the proposed generation test itself: naming bias predicts names without coordinated answers; concept-level influence predicts property-appropriate outputs under the same vector.

ML-debug review notes: all supplied logs and the complete entry point were read. Existing logs’ SHOULD—coherent movement exceeding random—is not established across properties. There is no new initialization, loss, optimizer schedule, gradient trace, memory measurement, smoke result, or independent implementation review to report. Before execution, the real tiny-model path should verify VJP gradients, finite-difference agreement, post-cast applied deltas, and one-prefill/cached-decode coverage. These are implementation checks, not another scientific selection gate.

**Decision:** proceed with this one bounded VJP proposal once implemented and checked. Do not claim it is likely to solve hidden-component replacement; it is the most useful small attempt among the supplied options.

— PI/OpenAI  
Same-family advice; no goal signoff.