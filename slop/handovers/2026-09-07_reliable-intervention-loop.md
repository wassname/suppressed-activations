# Active intervention research

Written by Codex/GPT-6. User is AFK. Harness goal remains ACTIVE: reliable coherent
dog AND ant demos, continuous steering and correctly recomputed readout. Do not
substitute digit-only success or full-residual transfer for suppressed-only evidence.

## Current state

### Latest checkpoint — 2026-09-08, Codex/GPT-6

This checkpoint supersedes the historical results and pending-job notes below.
Code51d9520 adds `--prefill-instruction`, default unchanged. Independent CPU
review confirms exact content/trailing space and propagation through source,
donor, matched templates and future corpus fitting. Generation uses the same IDs.
The option applies only to explicit `chat-assistant-prefill` mode.

Critical correction: pre-57a3898 generations auto-masked the user-turn
`<|im_end|>` because pad was incorrectly set to tokenizer EOS. Current code uses
explicit all-ones masks and correct stop IDs. Old/new comparisons are attention
confounded, not just different stopping. Do not reuse old numbers as current controls.

Current-mask results: full template L20 C2 gives a naturally completed dog4
explanation on original and validation2; other wordings still drift. Ant band
L16–20 C.625 switches all four reused validation wordings, but several invent
web-related biology. Band clamp C1 gives original ant6 with natural completion;
dog clamps still reconcile/restart. These are full-residual edits, not a solved
suppressed-only intervention. Two-column future projection did not improve identity.
Complete evidence is in template-clamp audit and `out/2026-09-08_*` logs.

Latest jobs, updated04:12 — Codex/GPT-6:
-603 smoke SUCCESS62s; all37 stdout lines read. Six singular values .2479–.9275,
 retained template norm .2542, C0 exact logits/tokens, positions33–35 and7decode.
 Its follower89485 is CLOSED. Full union grids612ant/613dog now queued/followed:
 612 finished105s; follower44021 CLOSED. All8 generations and51 stdout lines read:
 natural pair/union stay8/spider; equal-norm pair starts6 but explains spider8;
 equal-norm union p6=.9674 startsant6 then bee/wasp and repeated alternatives.
 Not sustained identity. swap_review independently agrees and will append paired audit.
 613 dog follower37894 still live, out/2026-09-08_future-union-{ant,dog}.
-604ant/608dog original default SUCCESS24/27s, reproduce earlier L20C2 outputs.
-605–607/609–611 FAILED argparse before model load: pueue lost quotes around
 multiword arguments. All six full13line logs read; no model results from these.
 Replacement commands pass the entire command as one shell-quoted argument;
 stored pueue argv checked to retain inner quotes and trailing source space.
-614ant original neutral follower11426.
-615ant validation1 default88731;616neutral12194.
-617dog original neutral83595.
-618dog validation1 default4088;619neutral22010.
 All603–611 followers are CLOSED; never poll them again.

Wrapper jobs use future-template index15 (FULL template L20 C2), last3 plus
every decode token, max128, official assistant-prefill. Neutral user instruction
is `Continue the text.`; default is `Complete the following fact, then explain your answer.`
Each owns `out/2026-09-08_wrapper-{animal}-{original|validation1}-{default|neutral}`.
Hypothesis: explanation instruction contributes to reconciliation loops; competing
cause is indiscriminate repeated steering. A bare digit then EOS is not success.
Compare full text, donor controls, post-edit readout and coverage, not only log odds.
GPU default lane remains1; other-repo600–602 precede these jobs. Do not modify them.

Future-union jobs612/613 compare pair/6-form span × natural/equal norm × C0/1,
L20,128tokens. Read all16 full generations before judging; preserve failures.
Current user README.md and .gitignore edits remain untouched.

## Model, methods, and checks

Pinned Qwen/Qwen3.5-4B revision851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a,
32layers. L20 means output of zero-based block19; token33 is not layer33.
Runner scripts/oat_sweep.py; hooks scripts/demo.py; rendering scripts/prompt.py.
CPU suite `uv run --no-sync python -m scripts.test` passed16 checks this turn.
Steering covers last3 prompt tokens and every decode token. C0 must preserve
exact logits/tokens; logs assert decode_steps=generated_tokens−1. Natural EOS
is allowed. Current max128, selected long confirmations256.

Full template differences average last3 aligned suffix states from8 paired
explicit-animal templates without leg-count tasks. Band strength is PER LAYER.
Clamp targets a clean-template coordinate, not validated semantic presence.
Clean donors are often edited too. Full-residual edits are not suppressed-only.

Future estimator contracts official mean-J with named vocabulary rows:
16seed0 eligible WikiText2 records,128content tokens before chat rendering.
Target-position SUM, source-position MEAN, then prompt MEAN; source layers
12/16/20/24 to raw penultimate residual31. Corpus includes one spider article
incidentally, not animal-free. Finite-difference/split-half evidence and reference:
slop/research/2026-09-07_future-vjp-reference.md. Three rows are not full J readout.
Lexical union adds capital/plural forms, giving6 columns per animal pair versus2.
QR projection logs singular values and retained norm; norm restoration is explicit.

603 corpus argument:
`/home/code/.cache/huggingface/datasets/Salesforce___wikitext/wikitext-2-raw-v1/0.0.0/b08601e04326c79dfdd32d625aee71d232d685c3/wikitext-train.arrow`.
Smoke path out/2026-09-08_future-union-smoke. Full stdout/rank/C0 coverage read;
full8condition union sweeps are now queued. See latest follower list above.

## Additional evidence and pitfalls

Full current-mask outputs:
- out/2026-09-08_future-template-{ant,dog}
- out/2026-09-08_band-clamp-{ant,dog}
- out/2026-09-08_correct-mask-{ant,dog}-validation0..3
- out/2026-09-08_future-gated-{ant,dog}-256

These runs finished and were read. Original full-template L20C2 dog p4=.841981
naturally completes; validation2 p4=.874737 also completes. Ant band clampC1
p6=.928239 naturally completes. These selected results do not establish a shared
reliable method. Current-mask future gated antL12C2 p6=.930556 completes126tokens
with questionable nesting claims; dogL24rank4C2 starts8 and corrects to spider8.
Old dog success was attention-confounded. Prior random controls do not transfer
automatically to corrected-mask settings. Consequence jobs563/564 had invalid
clean donors (ant antennae10, dog tails0), so cannot diagnose steering alone.

Readout uses suppression23→25→32. Earlier edits can introduce a concept before23
or leave it unsuppressed at32. Union readout also includes one unpatched position.
All-layer named curves distinguish these cases; do not choose layers post hoc to
make ant appear. CPU transient-window check (dff6afd): early4, peaks8–24, later
through32 gives clean spider scores0/1.029/1.022 at positions33/34/35. It does not
establish a common suppressed spider direction, nor disprove persistent concept
spaces generally. Three named curves cannot establish a full-vocabulary detector.
No production detector change made. See template-clamp audit for exact limits.

Agents continuous_review/svd_review/swap_review are available for followup.
Scientist panel already ran two rounds; /moa-scientist absent, external-review-v2
used instead. Reviews in slop/reviews. Do not repeat withdrawn swap-algebra
objections. Historical checkpoints are preserved in git, not repeated here.

— Codex/GPT-6
