## Inherited decisions
- Both goals remain open. Diagnostics must advance the goal, not substitute for it.
- Offline donors are allowed; edits must use only current-layer information.
- A changed word or digit is insufficient: the same method must transfer a property coherently.
- Parent approved **B**, full-strength conditional reflection, without subsequent recentering or dose selection.

## Diagnosis
**Observed:** `142748/run.md` shows projected steering reading “spider” while retaining “inside.” Its full-donor alternative barely flips the property: outside .241 versus inside .212. `150958/run.md` shows no reverse answer movement from the layer-20 coordinate swap. `151032/run.md` records failed logit-contrast recovery.

**Inference:** Another layer search or readout reranker would not resolve whether the donor representation generalizes to these question states. B tests that assumption while attempting the actual intervention goal. It does not establish that adaptive magnitude can repair missing semantic content.

## Drift / contradiction check
Quarter-strength reflection would leave a negative coordinate negative: \(a'=a/2\). The approved full-strength rule instead gives \(a'=|a|\).

This revises the intervention—not merely one setting of 2612. It uses raw donor means, not the prior 6.9 rescaling, and is **not** the paper’s sparse J-space clamp.

## Recommendation
Run **one frozen B experiment**:

- Block15 output; final prompt position; full-strength conditional updates throughout cached decoding.
- Reverse **legs** and **skeleton_body**, unchanged prompts.
- Four conditions each: Base, conditional reflection, natural mean-difference addition, adaptive random control.
- Cap each continuation at32 tokens: at most256 generated tokens total.
- After all interventions, run the two clean spider-target prefills without generation, with intervention hooks removed. These are evaluation-only and must not influence edits.

Required checks:

1. Offline means satisfy donor coordinates \(-\|\mu_t-\mu_s\|/2\) and \(+\|\mu_t-\mu_s\|/2\).
2. Before casting, reflection gives \(a'=|a|\), preserves components perpendicular to \(u\), and is idempotent. Record realized BF16 deviations.
3. Log per-call margins, gate activation, requested/applied norms, and coverage—even when the gate produces zero updates. Respect early EOS.
4. Report initial answers, both answer probabilities, log-odds movement, exact continuations, and separately labelled prefill/final readouts.

**Adaptive random control:** sufficient for this bounded pilot, not definitive specificity evidence. Use one fixed isotropic random direction; compute its magnitude from the proposed reflection displacement evaluated on **its own current state**. First-prefill requested norms should match reflection exactly. Later trajectories differ, so gate frequencies and cumulative doses need not match. Report those differences; do not call this a trajectory-dose-matched control or borrow the reflection run’s state.

## Risks / interpretation
- Dog-negative and spider-positive **prefill** margins on both properties support midpoint applicability, not semantic sufficiency.
- Same-side or reversed clean margins expose domain mismatch. Do not repair the center after inspecting them.
- Correct margins and correctly realized folds without both answer changes reject this frozen candidate’s sufficiency.
- Enforced positive coordinates are algebraic outcomes, **not successes**.
- Success requires the same reflection rule yielding both **8** and **outside**, with coherent continuations and a specificity advantage over random. Even that remains selected development evidence, not goal sign-off.
- Later NLI hypotheses need not be true; do not confuse them with initial answers or grammatical failure.

## Need from main agent
None; the consequential choices were settled through supervisor dialogue.

## Suggested execution prompt
No separate worker handoff warranted. Parent implements and validates the frozen test above. Defer A and C until this result is interpreted.

— PI/OpenAI