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

554 also SUCCESS103s; main read all40 dog outputs and115 stdout lines.
L12rawC2 gives4 but clue distortion; L16rawC2 gives4/dog with qualification;
L24projectedC2 gives4/domestic dog/Canis explanation at32tokens (p4=.616533).
Several other conditions give6 (wrong dog target) or invent dog-spiders.
Long128 confirmations567 L16rawC2 follower8840,568 L24projectedC2 follower20868.
Paths out/2026-09-08_future-dog-L16-raw-C2-long and ...-L24-projected-C2-long.
Only555–562 remain in735;563/564 and566–568 use their separate followers.

555–558 ant band validations finished; all4 full outputs read by main.
val0 p6=.964258 gives ant6 then drifts to silkworm/tarantula (128cap).
val1 p6=.688673 gives sustained ant6 (128cap; calls Formicidae an order).
val2 p6=.942440 gives coherent ant6,109tokens natural EOS.
val3 p6=.304752 vs p8=.391309 stays spider8,117tokens EOS.
Thus3/4 first-answer switches, not reliable4/4. Remaining735 followers559–562.
Scope band grid only tested C up to.5 (not1); modest stronger band doses remain
untested and could address val3, but may worsen val0 drift. Await dog/long results.

559/560 dog val0/1 read: both4/dog, but invent idiom/meme explanations forwebs,
128cap; p4=.949692/.737952. Not a clean general demonstration.
New template-band-strength grid (commit0fadf74): sameL16–20,last3+decode,no norms;
C0,.5,.625,.75,1,1.5,2. All128tokens. CLI/diffcheck pass; existing pipeline unchanged.
Queued570 ant original follower80392;571 ant val3 follower30357;
572 dog original follower64341;573 dog val3 follower40209.
Paths out/2026-09-08_band-strength-{ant,dog}-{original,validation3}.
These are adaptive followups, not untouched tests. Explicit source argv quoted as1command.

561/562 dog val2/3 read: both4,dog; val2 starts correction at128cap, val3 explains
hypothetical/riddle and dogs not spinningwebs,128cap. All4dog counts switch, notallclean.
735 follower cell COMPLETED; never wait it again.
563 antennae control INVALID: base8 (expected0), clean ant donor10 (expected2),
intervened6 and leg explanation. Do not attribute failure specifically to steering.
Future-gated grid added3e670ae: L12raw/L16raw/L24rank4 x C1/2 x gateFalse/True,
continuous128. Existing16CPUtests andCLI pass; reviewer confirms gate algebra.
Gate acts on signed coordinate dominance, not known conceptpresence; fewer edits is
a competing explanation. Cachedtokens are different states, not one repeatedstate.
Queued575 ant follower7882 and576 dog follower4586, out/2026-09-08_future-gated-{ant,dog}.

564 tail control finished: base0 correct (p0=.40254), clean dog donor0 WRONG
(expected1,p1=.13930); intervention0 (p1=.04971), dog/riddle explanation then
re-evaluation. Thus both attempted consequence tasks fail clean-donor first-answer
prerequisite. Do not infer concept-specific failure from them; preserve fulloutputs.
564 follower44997 completed. Exec842 may still await other follower polls; inspect
before reusing11835/8840/20868/80392/30357/64341/40209/7882/4586.

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

592–595 ant band-strength index2 (L16–20 C.625) and596–599 dog future-template
index15 (full template L20 C2, no future fitting) queued for existing validation
phrasings0–3,128tokens, explicit all-ones attention. Frozen animal-specific settings,
not fresh heldouts or shared default. Followers byjob:
592=92176,593=34001,594=76956,595=29739,596=64648,597=58987,598=20681,599=89293.
590/591 followers1150/23333 still live. -- Codex/GPT-6

588 smoke PASSED all5layers positions33–35,7decodecalls,zero norm, C0identity;
full21line log read.590 ant/591 dog band-clamp sweeps queued. Follow them next.
All prior jobs through588 completed, no live old follower handles. -- Codex/GPT-6

02:06 update, Codex/GPT-6: IMPORTANT correction: old pad=tokenizerEOS248046 while
modelEOS248044 caused HF auto attention mask to hide user-turn im_end position13.
CPU exact mask test old=[13] masked, new=[]; read installed generation/utils.py
798–805.57a3898 fixed BOTH attention and stopping;4a9c8c0 now passes explicit ones.
Earlier termination-only interpretation was wrong. Pre57a3898 cross-run comparisons
are attention-confounded. Raw future rows barely changed (cos>.9999997), but
suppressed basis IDs/eigenvalues changed enough to alter projected dog result.
Preserve old results, do not blame max_new_tokens for first-logit changes.

583 ant gatedL12C2 completes126tokens6/ant;584 dog projectedL24C2 completes137tokens
8/spider, not4. Main read both full outputs and37-line logs.586/587 full future
template grids complete, main read all48 outputs and83-line logs each. Projection
does not improve identity/coherence: matched ant can give6 but explain spider8;
dog projections yield6/2 or loops. Full unprojected dogL20C2 gives4/dog and naturally
finishes, p4=.841981; ant same condition drifts to bees. Independent audit requested.
All their follower handles CLOSED. New template-band-clamp comparison uses existing
clamp vs additive, L16–20, C0/.25/.5/.625/.75/1, no normrestore, continuous.
Smoke588 index6(clampC0), max8 queued, follower20137. Full grid NOT queued yet.

2026-09-08 01:58 update, Codex/GPT-6:578–582 completed successfully. Main read
all28 band-strength outputs and complete33-line stdout per job. Ant C.625 switches
original and validation3 to6/ant, both terminate; taxonomy/silk rationalizations
remain. C.75 original says six legs ON EACH SIDE. Dog C.625 original gives4 but
loops conditional animal examples, including humans4. Stronger1.5/2 gives1 or2
and severe repetition. Thus stronger band fixes one weak first answer, not joint
coherence. Reviewer swap_review completing audit in template-clamp.md.
Ant finalprompt C.625 fixed logits23/25/32=.572/2.002/2.344: no fall, score0;
validation3 likewise1.015/2.055/2.499. Missing ant readout follows the criterion,
not demonstrated absent ant. Full curves logged, do not silently retune readout.

582 real projected-C0 smoke passed identity and positions33–35+7decodecalls.
L16 ant future projection retains norm fraction.086176. Full24-condition grids
queued586 ant and587 dog, followers40181/38992. Compare full/projected/matched
without renaming as suppressed-only.583/584 long gated remain followed61408/28332.
All old578–582 follower handles are CLOSED. Earlier pending notes below stale.

Stopping audit, Codex/GPT-6: local pinned config text_config.eos_token_id248044 is
`<|endoftext|>`, but tokenizer eos248046 is `<|im_end|>` (pad248044). Both generate
paths previously passed only pad=eos and inherited model endoftext stopping.
Scope-ant condition27 ends `[39585,13,248046,198,248044]`, proving post-message
newline/endoftext generation. Both paths now stop on either marker and use actual
pad id. The initial termination-only interpretation is withdrawn; see mask correction above.
Independent actual Transformers5.16.1 tiny-GPT2 CPU check by continuous_review passed:
forced old output `[3,4,im_end,7,endoftext]` becomes `[3,4,im_end]`, identical prefix.
Preserve old logs. All seven followers remain live, no restarted jobs this turn.

Queued583 ant future-gated index3 (L12 raw C2 gateTrue) and584 dog index11
(L24 rank4 C2 gateTrue) for256 tokens, to test whether selected coherent passages
finish or reverse after the128 cap. These are configuration-selected development
checks, not shared-setting or heldout validation. -- Codex/GPT-6
Followers583=61408,584=28332. All seven pending followers verified live this turn.
348aba0 adds all-layer fixed ant/dog/spider curves to the existing named diagnostic,
without changing the detector triple or steering. Independent CPU check by svd_review
passes triple equivalence, rise/fall, ranks and patch flags. Future-template QR
projection also independently matches pseudoinverse geometry; matched norm passes.
Real projected-C0 smoke582 remains pending behind other repo job577 and band jobs.

Update 01:43 — Codex/GPT-6: 759e6e3 adds future-template projection comparison.
Predeclared: L16/20 × full/projected/norm-matched × C0/.5/1/2, both animals,
last3+all generated tokens. Project the fixed template donor−source difference
into the QR span of spider/target future-VJP columns. No dynamic swapping.
Prediction: if future span retains useful causal content, natural projection moves
the target; matched projection distinguishes weak magnitude from wrong direction.
Risk: tiny retained norm makes matching extreme; fraction is logged, no hidden restore.
Not suppressed-only evidence. Independent design review by svd_review recommends this
small comparison, warns additive pressure can still loop and span retains common features.
Config predicates now control fitting directly, removing duplicated sweep-name lists.
Real C0 projected smoke queued582, follower84568; main grid NOT YET queued.
578–581 followers still live. Review all stronger-band results before selecting defaults.

Update 2026-09-08 01:34 — Codex/GPT-6: supersedes pending jobs below.
566–568 finished. Ant L12 raw C2 starts6/ant but later says spiders have four legs;
dog L16 raw C2 loops correcting its dog riddle; dog L24 projected C2 sustains4/dog
but adds a spider8 versus dog4 conditional explanation. All were capped128.
575 ant gated finished: L16 C2 gating removes the ungated spider6 correction loop,
but adds false honeycomb/spinning claims; L12 C2 gated is more consistent ant6.
No clean general result yet. Full12 ant outputs read; independent review requested.
576 dog gated is followed by existing session4586.

570–573 all crashed before interventions, identical `KeyError: 16`: new
template-band-strength grid was omitted from the template-fitting predicate.
Fixed in f54cad7; all16 CPU tests pass. Original full crash logs committed under
slop/audits/2026-09-08_band-strength-crash. `pueue restart` created NEW jobs578–581
(not reuse of old IDs). Followers:578=15540,579=16983,580=81138,581=72077.
Await these followers, inspect all generated text. User README/.gitignore untouched.

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
