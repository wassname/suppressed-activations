# Active intervention research

Written by Codex/GPT-6. User is AFK. Harness goal remains ACTIVE: reliable coherent
dog AND ant demos, continuous steering and correctly recomputed readout. Do not
substitute digit-only success or full-residual transfer for suppressed-only evidence.

## Current state

Code commit d23803b (plus later documentation commits). Preserve user README.md
and .gitignore edits; do not publish/push. Main runner scripts/oat_sweep.py, hooks
scripts/demo.py, tests scripts/test.py. Use pueue default GPU lane1; other repos
share it. User says attach followers and wait, do not check every minute.

Pinned Qwen/Qwen3.5-4B revision851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a,32layers.
Official assistant-prefill template in extraction and generation. Intervention
starts last3 prompt tokens and continues EVERY decode token. Up to128tokens now;
natural EOS allowed. Layer L24 means output of zero-based block23, not token33.

## Best evidence, not yet completion

- Full matched-template mean difference (8 paired explicit-animal templates,
  no leg-count tasks) L24C1 switches all4 validation phrasings per animal at32tokens.
  All24 selected-setting matched random controls remain8. Ant readout poor.
- Long L24 additive dog loops at128; ant gives biological details then beetle aside.
- BEST COMMON candidate: template-scope condition27, bandL16–20, C.5 perlayer,
  last3 plus all decode, no residual norm restoration, no suppression projection.
  Job549 ant p6=.963228,110tokens ending naturally with coherent ant/Hymenoptera/
  six-leg explanation. All5 layers109decodecalls. Job550 dog p4=.927658,
  dog/four-leg explanation with conditional aside, capped128, no loop.
  Ant readout still spinning/SOC/etc; dog readout dog-like.
  Full ant quote and links in latest RESEARCH_JOURNAL.md entry.
- All-content edits did not consistently improve. All64 scope outputs read.
- Clamp547/548: dogL24C1 readable qualification (dogs do not spin webs), repeat.055
  vs additive.488. Ant loops. Clean dog edited at100% positions despite readable
  output, so absolute template threshold is not an established semantic detector.
- Clean ant baseline itself invents12-legged insects. Separate normal factual
  errors from intervention-induced loops/identity/count contradiction.
- Equal-norm suppressed projection ranks4/8/16/32 still fails ant6; dog changes4
  with distorted text. Not merely weakened norm. Does not disprove all subspaces.
- Strong raw named swaps C6–32 produce ant6 often with spider/6 or taxonomy errors;
  dog often6 (wrong target) then lexical loops. Mere weakness is insufficient.

## New actual future-effect estimator

fit_future_rows implements contraction of official mean-J with3 raw vocabulary
rows (spider,dog,ant). Source12/16/20/24, raw penultimate residual31, target-position
SUM then source-position MEAN then prompt MEAN. Not average activation contrast.
16 seeded random eligible WikiText2 train records,128content tokens BEFORE official
chat rendering; actual150tokens, mask22..148. Corpus includes one jumping-spider
record incidentally; not animal-free, do not cherry-pick it away.

Smoke551 PASSED: finite differences8.219/8.200 at eps.125/.5 vs grad8.279 (~1%);
eps2=6.199 nonlinear. Split-half direction cosines.881–.980. Files:
out/2026-09-07_future-vjp-smoke/future_lens.json and future_lens_vectors.pt.
Full vocabulary readout NOT available from3rows. Official repo has no writing
helper; rawWU follows paper definition, unit-column normalization is our choice.
Reference: slop/research/2026-09-07_future-vjp-reference.md.

## Pending jobs and live followers

Update 2026-09-08 01:14, Codex/GPT-6: shared552 finished;553 SUCCESS105s.
Main read all40 ant future-coordinate outputs and all115 stdout lines.
Raw future L12C2 gives6,p6=.925624,p8=.031673 and ant/Insecta explanation32tokens;
L16C2 gives6,p6=.952399 but starts colloquial qualification. C4 early damages wording.
Rank4 projected variants never give6. L24C2/4 gives ant-like readout but remains8,
and C4 loops ant-spider. Diagnostic L12C2 lastpos35 ant logits23/25/32=
2.0258/1.9520/2.2040: no rise/fall, score0, despite ant6 behavior.
Long128 L12C2 ant confirmation queued566, follower11835,
out/2026-09-08_future-ant-L12-C2-long. swap_review auditing553 independently.
Cell735 still follows remaining554–562;563/564 followers38979/44997 still live.

Other repo552 was RUNNING at latest status; do not interfere. Our553–564 queued.
All commands pinned by pueue argv and output dirs; all use existing runner.

-553 ant /554 dog future-coordinate40conditions,32tokens:
 L12/16/20/24 x raw/rank4projected x C0/.5/1/2/4.
 Followers553=92560,554=71022.
-555–558 ant /559–562 dog template-scope condition27,4validation phrasings,
 max128tokens. These are reused validation prompts, not fresh untouched heldouts.
 Paths out/2026-09-07_template-band-ANIMAL-validation0..3.
 Followers555=16943,556=52401,557=65406,558=82486,559=34230,560=32203,
 561=60818,562=24786.
 functions exec cell735 follows ALL553–562; still live last observation.
-563 ant antennae0→2;564 dog tails0→1, same frozen band27,max128,
 with task-matched clean donor. Predeclared exact strings in
 slop/research/2026-09-07_animal-consequences.json.
 Followers563=38979,564=44997; not in735. Store consequence_followers has both.
 Paths out/2026-09-07_band-consequence-ant_antennae and ...-dog_tail.

Completed waiter cells692/721 can be discarded. Never restart jobs because an
observer times out; inspect same handle/state first.

## Corrections/tests/provenance

- Latest continuation reran `uv run --no-project /home/code/.cache/uv/environments-v2/oat-sweep-da08b15948b5bc08/bin/python -m scripts.test`: exit0, all16 checks passed (Codex/GPT-6). These are algebra/hook regressions, not evidence of coherent animal transfer.
- Normalized detector scoring and basis geometry previously differed; corrected
  normalization BEFORE vocabulary centering; regression passes.
- HF hidden-state capture could precede the edit at the exact patched layer.
  layer_hooks now prepend=True; regression passes. L24 peak25 readouts were later
  than edit so this does not explain their poor ant readout.
- VJP grad leaf is in-place requires_grad_(True), not detached replacement; the
  latter left captured tensors disconnected. Reviewer caught before GPU smoke.
- C0 exact logits/token identity and prefill/decode coverage asserted.
- Clamp coordinate/complement/idempotence, swap algebra/dtype traces tested.
- New result/condition logs include source SHA256, model, revision, commit;
  result records package versions. User doc changes make git dirty even if code clean.
- target_concept separated from answer digits; explicit --target-output and
  --target-prompt now override presets (for563/564). Reviewer found no remaining
  digit-to-animal coupling. --target defaults dog, always pass ant for ant work.
- Earlier527–535 heldouts failed argparse due pueue second shell parse. Correct
  pattern is quote ENTIRE command argument, preserving quotes around prompt.
  Retries538–545 succeeded; no negative model outcome attributed to failed argv.
- Pyarrow>=21 added via uv; existing8day supply-chain hold unchanged.

## Next action

Wait735 and consequence followers; inspect ALL new generations/readouts and controls.
Freeze useful conditions for confirmation; do not select a separate setting per prompt.
Ant readout and sustained reliability remain unresolved. If future swap is weak,
consider projecting the useful template difference into named future-J span, rather
than raw-vocabulary suppression span. Do not rename an alternative as suppressed-only.

Readout audit by svd_review (Codex/GPT-6): detector requires a rise23→25 AND fall25→32,
but band edits16–20 precede23. Missing ant may mean early-written or unsuppressed,
not absent. Condition27's top ` spinning` comes from unpatched position32 (score2.6699);
only33–35 patched, union takes maximum across all4. Next cheap diagnostic: fixed
ant/spider normalized centered logits at23/25/32 per patched position, rise/fall,
suppression score and vocabulary rank. Keep current readout unchanged while diagnosing;
do not silently remove source features by changing aggregation.

Implemented this diagnostic in oat_sweep.py (logging only): base/post-edit fixed
spider/dog/ant centered logits, rise/fall, exact existing score and rank with ties.
Main independently checked synthetic geometry/ranks/patch mask to1e-6; passed.
Initial test assertion inferred integer dtype for zero; corrected test, not production.
CLI --help and diff check pass. Queued runs will include it if started after this edit;
inspect code hashes rather than assume coverage. No new GPU run queued for logging.

Audits: template-transfer.md, template-independent.md, template-clamp.md in slop/audits.
swap_review appended scope audit to template-clamp.md (may need commit).
Scientist panel already ran two rounds via external-review-v2; /moa-scientist absent.
Reviews/corrections in slop/reviews; do not repeat withdrawn mathematical objections.
Journal has latest clamp/scope/future results. Keep single handover current.
