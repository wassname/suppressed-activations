# Notebook comprehension panel

Probe: explain the notebook's claim, reconstruct the extraction and intervention, separate supported from unsupported claims, say how to adapt it, and suggest concrete simplifications.

## Answers side by side

| question | PI/gpt-5.4 answer | GLM 5.3 Flash | Kimi K3 | Muse Spark 1.3 |
|---|---|---|---|---|
| claim | A sample-specific rank-8 rise-and-fall subspace can transfer a target prompt's next-answer state into one Spider residual at L26. It does not establish Ant/Dog semantics. | “sample-specific next-answer-state transfer, not a transferable animal concept” | “transfer of the target prompt's next-answer state, not transfer of an animal concept” | “answer-state transfer, not transfer of an Ant or Dog concept” |
| operation | Extract one basis per full prompt; at the final source token replace its L26 source projection with a norm-matched target projection. C1 is replacement; C4 extrapolates. | “C=1 exactly swaps ... C=4 extrapolates four times” | “C=1 means exact replacement ... C=4 extrapolates four times past” | “C=1 is norm-matched replacement ... C>1 extrapolates” |
| site | One prompt-reading edit at residual L26 and the final prompt token. Decode steps are unmodified. | “only the final prompt token's layer-26 residual is edited” | “hook is active only during prompt prefill” | “implemented as blocks_to_hook=[25] ... prefill_only=True” |
| strongest unsupported reading | The selected rows identify an animal representation and the 64-token text shows persistent animal steering. | “That the ant or dog ‘concept’ ... was transferred” | “That a transferable animal ... concept direction was identified” | “longer continuation proves persistent animal information” |
| adaptation | Edit source/target prompts, one-token outputs, and perhaps layer/rank/strength in the config cell; run all cells. | “Edit the config cell ... then run all cells” | “Edit the configuration cell ... the sweep and generation tables recompute” | “Edit the configuration cell values ... then rerun” |

All three flash models reconstructed the hard mechanism in their own words, including the residual/block offset, C1/C4 distinction, prefill-only scope, and negative semantic conclusion. This is strong evidence that the main explanation is understandable.

## Repeated problems

All three said the exact rise-and-fall score is hidden in the imported module. GLM: “The internals of suppressed_activation_subspace ... live in ... the module.” Kimi: “The internal selection rule ... is not shown.” Muse: “Exact rise-then-fall selection criterion ... is not defined in the notebook.”

GLM and Kimi also found `match_norm` underspecified. GLM asked why L23/L25/L32 were chosen. All three asked why C4 is needed rather than C1.

## Changes accepted

1. Add the four-line rise/fall selection pseudocode and define `match_norm` algebraically.
2. Call L23/L25/L32, rank 8, and C4 demo settings selected in earlier exploration, not general defaults.
3. Merge the duplicate extraction and before/after readout tables.
4. Use “subspace readout tokens” instead of “selected vocabulary rows.”

## Suggestions rejected

- Drop negative strengths: rejected because the user asked for multiple strengths and directions.
- Show only Dog: rejected because the user asked to see both 8→6 and 8→4.
- Rename Ant/Dog to target-A/target-B: rejected because the concrete prompts make the intervention easier to inspect; the semantic caveat is already explicit.
- Remove the projector-invariance note: rejected because it answers the user's earlier QR question in one sentence.
- Remove Git provenance: rejected because an executed research notebook needs to identify the source it ran.

## Retest

After the four changes, all three models again reconstructed the operation correctly. GLM and Muse correctly retained the failed 95% criterion. Kimi instead wrote that the effect was “exceeding matched random-direction controls at the preregistered criterion,” despite also quoting 238/256 and 235/256. The sentence “effects exceeded 238/256 ... below the ... criterion” invited that scope error. It now reads: “failed the preregistered 95% criterion: only 238/256 and 235/256 matched random effects were smaller.” A focused Kimi retest then said, “preregistered controls failed the 95% criterion,” so the misread is gone.

The panel reports and complete provider traces are the seven `2026-09-05_*_notebook_comprehension_*` files beside this memo.

Written by PI/gpt-5.4.
