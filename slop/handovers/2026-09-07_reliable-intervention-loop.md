# Active intervention research

Written by Codex/GPT-6. User is AFK. Harness goal remains ACTIVE: reliable coherent
dog AND ant demos, continuous steering and correctly recomputed readout. Do not
substitute digit-only success or full-residual transfer for suppressed-only evidence.

## Current state

### Update04:49 — Codex/GPT-6

637smoke SUCCESS14s no livefollower. Reviewdimensionspass. Smokeupdate projected
contrastnorm rises1.810→22.960 L25→32; thisspanis notattenuatedsuppression.
638antfull SUCCESS62s follower62116 CLOSED; all43stdoutlines/12fulltextsread.
Peaknatural+matched,updatematched,outputmatched give6 coherentantdescriptions.
Outputnatural6butspider8;updatenatural8spider. ReadoutsstillSOC/spinning etc.
639dog follower14650stilllive,pathout/2026-09-08_template-state-dog.
Freshantfullsame12grid640queued,pathout/2026-09-08_template-state-fresh-ant,
followerfromlasttool. Do notpickwinneruntilfreshcomparison. Originalantpath
out/2026-09-08_template-state-ant. No suppression-onlyclaim fromrawstate spans.

### Update04:46 — Codex/GPT-6

636dogselector SUCCESS48s,follower38357CLOSED. All35stdoutlines/8fulltextsread.
ContrastivematchedC2 dog4 coherentdogdescription p4=p8=.3224; naturalstays8.
Thuscontrastive stillonlydog,notant. Priorfinal said"bothstrengths" but actually
two normalizationmodes atC2; preservecorrect terminology.
9f8b53b implements rawtemplate-state spancomparison: Dpeak25,Doutput32,
Dpeak-Doutput; 24columns=8templates×3positions, rank4SVD. FixedL20,C0/2,
natural/matched =12conditions. Logspeak/outputprojectedcontrastnorms andSVDs.
Theseare downstream-update spans,notestablishedsuppression. svd_review reviewing.
Syntaxcompileexit0. GPU8tokenC0updatesmoke637queued,path
out/2026-09-08_template-state-smoke; followerhandlefromlasttool. Fullnotqueued.

### Update04:44 — Codex/GPT-6

634smoke SUCCESS14s follower62713 CLOSED. 2b5346d addsfullrankassertbeforeQR
andgroupedselectedtokenIDs afterreview. Selectedanttemplatesourcewords må/webové/
夫君/เว็บ;target Saison/šta/esai/สห. Not antlike. Retainednorm.050729.
635antfullselector SUCCESS47s follower5217 CLOSED; all35stdoutlines/8fulltextsread.
Contrastive C2naturalandmatched remainspider8; matchedp6=.0803,p8=.8631.
Oldmatched repeats6thenspider8. AllC0baseexact. Noantidentitysuccess.
636dog follower38357 stilllive. Outputout/2026-09-08_contrastive-selector-{ant,dog}.
svd_review reviewing next conceptualtest: directpairedhidden-state latechanges
as span insteadofvocabularyrows. Noimplementation; do notlabel arbitrarylate
residualdifferences asprovensuppression. Review normalization andrisecontrol.

### Update04:42 — Codex/GPT-6

632dogdetector SUCCESS40s, follower92500 CLOSED. All31stdoutlines/6fulltextsread.
Onlylatematched transfersdog4; both earlierwindows stayspider8. Allpriorjobsclosed.
a4c3175 implements template-selector: score difference averaged8matchedexplicit
animaltemplates×3suffixpositions, top4positive eachsign, normalized vocab basis,
project existingfulltemplate delta. Score/source/target/wordslogged. C0/C2×natural/
matched×old/contrastive selector =8rows. FixedL20. No newtraining/readoutclaim.
svd_review reviewing code. Syntaxcompileexit0. RealGPU8tokenC0smoke634queued
pathout/2026-09-08_contrastive-selector-smoke, followerjuststarted; retrievehandle
fromtoolhistory. Do notqueuefulluntilsmoke/reviewchecked. NeedrankassertbeforeQR
ifreviewconfirms possibility of dependence. Different vocabIDs do notproverank.

### Update04:39 — Codex/GPT-6

629freshdog SUCCESS20s, follower63606 CLOSED. All21stdoutlines/fulltexts read:
dog4 natural coherent domesticdog/hunting/herding/guarding/commands description.
631antdetector SUCCESS40s, follower28900 CLOSED; all31stdoutlines and6fulltexts/
readouts read. EarlierD8/20/32 and16/20/24 bothstay8spider, naturalormatched.
Readoutfinance/construction; retainednorm .049865/.053192 vs .081415 late.
Late matched reproduces6then spider8 correction. Noantidentity in6conditions.
632dogdetector92500stilllive. svd_review now considering suppression on matched
explicitanimaltemplates with contrastive score rather than anotherblindwindowgrid.
No implementation yet. Fullbaselineant failsfresh628(6beetle), dogfreshpasses.

### Update04:37 — Codex/GPT-6

628freshant SUCCESS21s; follower55125 CLOSED. Full21stdoutlines andfullbase/donor/
causaltexts read. First6 p6=.826302,p8=.007149 BUT describesbeetle, notant:
"The animal is a **beetle**, which is the most common type of insect found in nature."
Continueshard shell/rollintoballs/recycling. Readoutsocialforms. ThusfullL20C2
fails fresh antidentity despite prior2wordings; no reliabilityclaim. Sourceexact
in628metadata/earliercheckpoint.629dog63606stilllive,63128900/63292500pending.
Independentdog627audit appended. CPUcheckall88rows626/627: everydecode_steps
equalsgeneratedtokens-1, threeprefillpositions; allC0tokens equalbase. Exit0.
Do not confuse final-decode readout(unrelated) with first-decisiondogreadout.

### Update04:35 — Codex/GPT-6

627dog SUCCESS183s, follower38088 CLOSED. Main read all44 fullgenerations/readouts
and107stdoutlines. L20C2 ranks4/8/16/32 all coherentdog4 naturalcompletion.
Rank8 p4=.8149,p8=.0758 readout entirelydogforms; generation dogbarks/smell/
service/hunting/companions. L24C1 all4ranks also dog4, somegenericbreederrors.
L24C2 degenerates: rank4/16first2 loops;rank8badwording;rank32dog-odog loop.
Random4first4butspiderdescription, othersspider8. Thus8 selected conditions
retain count+identity, not jointant/dog success. swap_review auditing independently.
Earlierant626 has no coherentant6. Treatdog positivecontrol for631/632windows.
All five open jobs were followed per pq;628/629/631/632 pending.630otherrepo
finished,633otherrepo priority1 ahead of ours; do not alter. CLIhelp54903exit0.

### Update04:33 — Codex/GPT-6

40101f8 adds template-detector sixconditions: windows23/25/32,8/20/32,16/20/24
timesnatural/matched norm, fixedL20C2persistent_rank4. Lastwindow tests transient
suppression, not final suppression. svd_review recommended this discriminator,
found no normalization inconsistency. Jobs631ant/632dog queued, followers28900/
92500. Outputs out/2026-09-08_describe-detector-{ant,dog}. IMPORTANT630belongs
LUCID3 otherrepo; accidental follower69862 attached by assuming consecutiveIDs.
Do not change job630. Always use returned IDs. Otherfollowers remain62738088,
62855125,62963606, all confirmedlive thisturn.
CPU import gridcheck failed ModuleNotFoundError pyarrow in ROOT uv environment;
runner has inline script dependencies. Correct `uv run scripts/oat_sweep.py --help`
now session54903 pending; inspect completion. Not evidence runner itselfbroken.
Next inspect all pendingresults before newmethod. No goalcompletion claim.

### Update04:30 — Codex/GPT-6

626ant SUCCESS177s; follower68132 CLOSED. All44 full generations/readouts plus
all107 stdout lines read. No coherent ant6 output: L20rank4C2 starts6 then
corrects tospider8; L24C2 ranks4/8/16 inventsocialmammals,rank32starts2.
Auditc110ba0 includes exactquotes. Template deltas/targets626 versus624 are
bitwiseidentical all layers (torch.testing rtol=atol=0,CPUexit0).
627dog38088,628freshant55125,629freshdog63606 revalidatedlive, notterminal.
svd_review reviewing current detector/scoring and proposing one minimal earlier
window discriminator. No new implementation yet. Current projection windows
remain23/25/32; contrast against coherentfullL20C2 is primary evidence.

### Update04:28 — Codex/GPT-6

626/627 followers68132/38088 revalidated live; no result yet, do not restart.
622–625 independent audit appended; journal d52598f records full-template
description result and limits. Fresh fullL20C2 checks628ant/629dog queued behind
projection sweeps, followers55125/63606. Source predeclared:
`Fact: An adult web-spinning animal normally has this many legs: `.
Same describe-evaluation/default-extraction instructions,128max,continuous.
Paths out/2026-09-08_describe-fresh-{ant,dog}. No fresh outputs inspected yet.
Template vector file confirmed exists624; compare to626 and628 once available
to verify extraction identity across source wording. Cross-eval-wrapper saved
tensor check still needs matching baseline artifact. No goal completion claim.

### Update04:25 — Codex/GPT-6

622–625 all SUCCESS, followers CLOSED. Full generations/base/donor/coverage
and21line stdout read for all. Original and validation1 BOTH ant6/dog4 natural
three-sentence descriptions atFULLL20C2 with default extraction/describe eval.
Antoriginal p6=.904764, validation .677601; dogoriginal .835725, validation .5042.
No loops/identity collapse in these4; antreadout stillsocial. Basevalidation
has eye-count factualerror, so distinguish model factuality from steeringerrors.
Independent swap_review reviewing all4 and next sweep comparability.

947a7c2 extends existing template-projection grid toL20and24, ranks4/8/16/32,
C0/.5/1/2, explicit normmatching andnoresidualrenorm;12 existing randomcontrols
remainL24C1 fullnorm. 44conditions peranimal,128max,continuouslast3+decode.
626ant follower68132;627dog follower38088. Outputs
out/2026-09-08_describe-persistent-{ant,dog}. Whole commands correctly quoted.
These use describe eval/default template extraction. Shared suppression basis
still source/donor-eval dependent; cannot claim identical projecteddelta across
wrappers. Detector23/25/32 unchanged. Read all outputs before semanticjudgment.
Saved template vectors available624/625;622/623 started before save patch so
do not assume those files exist. Need cross-wrapper tensoridentity control still.

### Update04:23 — Codex/GPT-6

Progress:620/621 completed natural three-sentence ant6/dog4 descriptions. Full
generations and stdout read. Wording errors (ant loads smaller, dog called breed)
but no identity collapse. Independent reviewer agrees. Ant readout stillsocial.
ed4f5fd separates extraction_instruction from evaluation prefill_instruction;
default None explicitly inherits evaluation wrapper, preserving prior behavior.
CPU16checks completed exit0. Reviewer verified propagation and row provenance.
39585dd additionally saves template_vectors.pt for direct cross-wrapper checks.
622 fixed-default-extraction/describe-eval ant SUCCESS21s: p6=.904764,p8=.001059,
natural ant6 description with pheromones/soil/seed dispersal. ReadoutSocial etc.
623 dog same comparison follower76937 still live. 622follower69492 CLOSED.
624ant/625dog validation1 same fixed extraction now queued, followers99564/68686.
Paths out/2026-09-08_wrapper-{ant,dog}-{original,validation1}-fixed-extraction.
Next: read623–625 full outputs; verify saved vectors, then fresh phrasing and
suppressed-only projection under descriptive wrapper. Do not call full template
success evidence of suppressed-only causal replacement. User README untouched.

### Update04:22 — Codex/GPT-6

Jobs612–619 all SUCCESS and all full generations read. Full21line stdout614–619
read. Old followers can be discarded. Independent swap_review audited union and
wrapper outputs in the existing template-clamp audit.
Dog equal-norm union starts6 and invents a Buster joke; ant union switches among
insects. Neutral original outputs only4./6.EOS. Neutral validation ant repeats
the fact, as its BASE also does; dog enumerates colored collars. No sustained
joint success. Default validation dog invents ownership riddle; ant capped128.

New620ant/621dog original-description jobs running/followed, sessions73594/26994.
Instruction: `Complete the following fact. Then describe the animal in three sentences.`
Same full-template L20C2, continuous,128max. Outputs
`out/2026-09-08_wrapper-{ant,dog}-original-describe`.
Important review correction: wrapper changes ALSO refit template directions.
These are combined-setup comparisons, not isolated instruction effects. Next
discriminator should fix extraction instruction while varying evaluation
instruction (small explicit parameter in sample/template extraction). Do not
claim existing comparison isolates explanation conflict. No code changes yet.

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
