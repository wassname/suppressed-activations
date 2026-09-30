## Scope finding

The full-donor control provides a selected, coherent-looking one-pass continuation, stronger than a digit-only change. It does not establish hidden-component isolation or transferable concept replacement.

The user explicitly allows partial findings: “we can show it working in a demo, and show out best method that works X% of the time I guess” (`.local/status-check/current-user-voice.md`). Neither universal success nor bidirectionality is an explicit acceptance threshold. Conversely, `.pi/goals/aef0cd-v1.md` requires changing “a hidden concept coherently,” not merely obtaining a target answer.

## Four existing cases

Paths below identify complete `run.md` and `interventions.json` evidence.

| Case directory under `out/` | Base → full donor | J-projection primary | Interpretation |
|---|---|---|---|
| `2026-09-30_125606_jlens-one-pass/` | 8→4; “The animal that spins webs is a dog.” | 6 | Selected grammatical count/name counterfactual; random retains8 |
| `2026-09-30_132714_jlens-one-pass/` | 4→4; “How many legs does a dog have?” | 6 | Reverse answer probabilities move toward8, but neither method gives8 |
| `2026-09-30_132742_jlens-one-pass/` | outside→outside | outside | Forward body-property transfer absent |
| `2026-09-30_131556_jlens-one-pass/` | inside→inside | inside | Reverse body-property transfer absent |

Thus full donor achieves the intended initial answer in one of these four development cases; J projection achieves none. This is a descriptive denominator, not an unseen-pair success rate. The last case’s completed artifacts survive a reported process timeout; do not relabel the process successful.

## What is supported

`125606/source.py` applies `edited = selected + donor_deltas[mode]`. Its later observer only appends readouts. The saved traces support final-position prefill plus cached-decode editing, without using Base results or later-layer observations to construct the edit. “One inference pass” means one generation trajectory per condition, not one transformer call.

`105132/donors.json` records generic noun prompts, including “The animal is a {concept},” without leg-answer labels. Full donor was already a control; its positive output cannot promote it retrospectively to the J-projection primary.

The forward output supports local behavioral coherence. Its readout still contains both “spiders” and “dogs,” amid punctuation. Whole donor addition does not isolate the hidden component. Answer/name bias, donor-token/context effects, and genuine partial concept transfer remain competing explanations. The body cases already distinguish this result from demonstrated cross-property transfer.

Unsupported goal words remain “finds what the model thinks but does not say,” “changes the hidden concept” as an isolated causal mechanism, and the integrated transfer claim. “Coherently” has selected-output support, not a demonstrated general rate. Failed reverse/property cases limit scope without erasing that positive.

## Smallest useful next action

Clarify `README.md` using the existing forward quotation and four-case table, explicitly labeling full donor as a control and preserving selection history. No rerun is needed for that clarification. A future frozen component-specific intervention succeeding on another property would strengthen the mechanism claim; another fluent digit/name continuation alone would not.

Reproduction caveat: `125606/source.py` imports live helpers rather than archiving them. Exact replay therefore requires matching helper revisions; pinning/verifying those could resolve this uncertainty. No new schema defect observed.

PI/OpenAI. Same-family, read-only review; complete allowed files read. No numeric reconstruction, execution, or goal signoff.