# Next coherent one-pass concept-edit attempt

— PI/OpenAI. Decision brief, not a result or permission to change frozen jobs.

Goal: use reusable offline preparation to change a hidden animal concept coherently within the current inference. No current-input prepass/backward or later-layer observer feedback. Reuse08; local queued GPU, initially300s. We need useful new behavior, not another report or parameter sweep. Both research goals stay open.

## Observations

The complete reviewed evidence is `slop/reviews/2026-10-01_indirect-donor-result-review.md`; audit `slop/audits/2026-10-01_job2687.md`. Eight offline description contexts ended in the same ` It` token. Mean spider-minus-dog at block15 was added naturally at the last prompt position and at0.25 strength during all cached decode calls. Observer block23 did not control edits. No prepass. Eight preparation calls plus ten32-token conditions; numerical state/edit/coverage checks passed.

- Reverse legs: Base4; indirect4; literal-name control4; random4. Donors later proposed an NLI hypothesis ending8, not an affirmed8.
- Reverse skeleton: Baseinside; indirectinside; literaloutside; randominside. This is a control-specific local positive, not success of the indirect donor.
- Indirect arithmetic retains4 but changes continuation formatting.
- Literal natural norm1.430336, indirect1.957303; random matches indirect. This is not orientation-only evidence.
- Prefill readouts did not become spider-dominated. Final readouts differed with later text and cannot isolate concept replacement.
- Reviewer: “The selected prompt tokens are the trailing space for legs/arithmetic and ` the` for skeleton—not the offline donor's ` It`.”

Historical selected full-donor forward run changed8 to4 and later said the web-spinning animal was a dog, but only1/4 tested property/direction combinations changed initial answers. Preserve that partial positive and selection history, not a general rate. Other local coordinate swaps, naming-VJP and context-projected/reflection preparations have not produced broad coherent transfer. Do not reintroduce the old current-input two-pass replacement.

The observed mismatch could reflect context-dependent direction transfer, a weak perturbation crossing the shallow inside/outside boundary, or actual concept change that is insufficient for another property. The NLI completion frame also complicates assessing coherence. These are hypotheses, not diagnosed causes.

## Decision requested

Choose one small next causal experiment, with exact prospective prompts, preparation and controls. Compare two or three mechanistically distinct options, not a dose/layer/k search; then choose one. One possible option is a native-chat, concise joint-property task with offline preparation at the same assistant-start role. Do not assume it is best: it changes the frame and may merely make outputs easier to score. Another is to exploit the existing donor with a better-designed property test; explain what new causal evidence it could provide.

Keep hidden concepts out of the actual input and requested output where feasible, but require enough output to judge target-consistent behavior rather than a digit alone. Known dog/spider concepts are development cases, not unseen transfer. Account for baseline correctness, partial/wrong/capped outputs, unrelated-task preservation and matched-control limitations. Do not turn a universal two-property success threshold into a user requirement.

Ask the parent your highest-impact unresolved choice before finalizing. No code changes, inference, shell, network or delegation. Read named files only; source08 functions `prepare_donors` and the intervention part of `main` (roughly lines1540–1920) are available for feasibility. Job2705 is independently evaluating a new readout on cached cases; do not modify its pinned helpers or use pending results as known evidence.
