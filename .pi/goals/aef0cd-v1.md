# Hidden-concept readout and one-pass intervention

## Loop statement

You are an autonomous agent. Your task is to understand and advance the user's goals, and show them in an easy to understand and easy to verify way that you have done that. Your job is to get back on track, keep moving towards the goals, and keep refining and reducing uncertainty in the user's goals. This is a reminder: your immediate task now is to reread your goals file and get back on track. As a result of this, briefly update the busy user (in plain language, with reminded context) on what you have done since they last talked with respect to their highest goal, what you will do next, and anything you need from them.

Diagnostics must guide the next attempt at the goal. Completing experiments or fixing supporting code is not goal completion.

## User-visible result

README.md shows a reproducible method that finds what the model thinks but does not say, transfers from translation to English-only tasks, and changes the hidden concept coherently within one inference pass.

## User voice

- In reply to inspecting English failures and reproducing the edit crash:
  > ok sure but do'nt forget the goal, it could be a distaction side track
- On experiment size:
  > sure keep trying... er I would think your jobs couldbe a quite fast... just a few generaitons are enougth to get a measure.
- On autonomous work:
  > anyway don't stop, jsut be considering. ttyl gn
- Confirming that both English-only readout and coherent one-pass intervention are required:
  > 1 y
- Approving reusable offline preparation, without a preliminary pass over the current input or later-layer information at the edit:
  > 2 y reusable offline . y
- Approving local GPU only, no paid services, short jobs initially targeting five minutes, and continuing until stopped:
  > 3 y
- Approving the proposed focus reminder appended to the Loop statement:
  > 4 y

## Goals

1. [/] goal: Find hidden concepts with a frozen readout that generalises to English-only tasks.
   - references: scripts/english/04_erase_and_language_pairs.py, 06_twohop_english.py; pinned Wendler data and cached TwoHopFact; Qwen3.5-4B at the recorded revision.
   - subtle failure mode: translation-language separation or word removal scores well without distinguishing hidden thought from speech in English.
   - discriminator: README examples and fixed-set results show hidden-concept recovery with input/output exclusion, compared with equally filtered plain-lens controls; language labels are used only for scoring.
   - tasks:
     1. [x] Inspect four previously correct English cases to choose the next method change; preserve frozen-method results separately from diagnostic selection.
     2. [/] Iterate on small tests, then evaluate the frozen method on unseen English examples and translation pairs; report selection and denominators.
   - evidence: (empty until sign-off)
2. [/] goal: Change a hidden concept coherently during one inference pass.
   - references: suppressed_activation_subspace.py, scripts/demo.py, 07_edit_language_pairs.py; Gurnee et al. Jacobian-lens intervention as a reference, not an assumed implementation match.
   - subtle failure mode: editing uses later-layer information from a separate pass, or merely changes an answer token without changing the hidden concept coherently.
   - discriminator: executable intervention trace shows only information available at each edited layer; fixed-pair outputs show intended concept changes with coherence and matched controls in README.md.
   - tasks:
     1. [/] Develop an intervention using reusable offline preparation only; no preliminary pass over the current input or access to layers after the edit.
     2. [/] Test a few paired examples with exact inputs, readouts, continuations and controls; expand only when useful, recording any departure from reference code.
   - evidence: (empty until sign-off)

## Resources

- Checked: coi-91cea783-1, local RTX 3090 with 24 GiB; 15.5 GiB in use at inspection. Shared GPU uses pueue default, one parallel job; do not reorder others' work.
- Checked: local Qwen cache directory, TwoHopFact CSV and Wendler French CSV exist; prior runs loaded the pinned model. Local inference needs no paid API credentials.
- Approved: local GPU only, no paid services; short experiments initially targeting five-minute jobs. No total time cap specified; continue until stopped. Use completion-triggered notifications, not recurring status spam.
- Approved: reusable offline calibration/transforms or donor activations; current-input inference and intervention remain one pass.

## Out of scope

- Broad sweeps, infrastructure cleanup, or repairing the old two-pass edit unless it directly informs these goals. Negative findings do not complete either goal.
- Publishing or pushing new material without editorial approval during this plan. README edits must preserve the user's prose.

## Log

- PI/OpenAI: user approved the plan. Starting the four-case diagnostic; no goal completed. Frozen-method evaluation remains separate from diagnostic selection.
- PI/OpenAI: job 2516 attempted the first four saved answer-correct English cases, four forward passes and zero generations, with a five-minute hard cap. Predictions: masking failure improves unmasked ranks; location failure exposes the bridge at another layer/position. Original ranks must reproduce. AST and alias-provenance checks passed.
- PI/OpenAI: 2516 timed out (exit 124) with an empty complete log and no diagnostic directory, before main produced artifacts. No scientific result. CPU trace identified Transformers' recursive model-source scan.
- PI/OpenAI: verified all 2,637 Transformers Python source files identical in RAM copy; AutoModel/AutoTokenizer import succeeded in 88.11s. Job 2517 retries the unchanged four-case diagnostic using that copy, offline model loading and the same five-minute cap. Completion follower proc_0091.
- PI/OpenAI: 2517 completed in 241s (44.73s inside main). All four frozen ranks reproduced. `out/2026-09-30_075901_twohop-four-case-diagnostic/result.json`: Congo is rank 0 in the plain lens at L24–27, but rank 849 after rise-and-fall; Iceland's output mask removes its name. Bulgaria/Iceland best-anywhere rank 0 was generic `republic`, not evidence of their identities. Diagnostic task complete, goals still open.
- PI/OpenAI: next method is the official reusable J-lens, read and edited at a fixed intermediate layer without later-layer information. Checkpoint revision 16a01f309fcec900fdcec3f4cd5b64f3d00e4d5a downloaded; SHA256 1f9a8f8fd593f0ffec1a9640993257ca4560f8ae3e5602315643d5cc6818534e verified. CPU weights-only check confirmed width 2560, 1000 prompts, block indices 0–30. Reference code revision 581d398613e5602a5af361e1c34d3a92ea82ba8e.
- PI/OpenAI: CPU checks passed for coordinate exchange, orthogonal preservation and swap involution (seeds 0/1). Job 2521 tests midpoint block 15, four explicit-country readouts, and same-pass spider/dog swapping against plain-lens and matched-random controls; final three prompt positions and all decode steps, at most 128 generated tokens, five-minute cap. Completion follower proc_8ba8. This is one pilot configuration, not a success-rate claim.
- PI/OpenAI: 2521 succeeded. `out/2026-09-30_081403_jlens-one-pass/interventions.json`: J-lens changed 8→4 (p4 0.056→0.566, log-odds shift +3.25), plain/random retained 8. All conditions covered 32 calls, prefill delta norm 0.149 for J/random. Country readout 0/4; spider readout punctuation. One selected pair is insufficient for goal 2, and goal 1 is not met.
- PI/OpenAI: 2523 compares raw versus unit-direction readout at the same midpoint/last position and k, with equally normalised plain-lens control. Five forwards, zero generation, five-minute cap; follower proc_793a. This changes one axis to align readout with the unit vectors already used for intervention.
- PI/OpenAI: 2523 completed; raw and unit-normalised J-lens both recover 0/5 at the midpoint final position. Unit normalisation replaces punctuation with city/president/number words but not the target concepts. `out/2026-09-30_082225_jlens-one-pass/run.md`; model compute/main took 16.83s. Hypothesis insufficient, not a goal result.
- PI/OpenAI: 2526 now compares max log-probability across prompt positions against final-position readout, raw J versus raw plain lens. Uses the five cached midpoint activation tensors; zero model forwards/generations, five-minute cap. Follower proc_18c7. No layer, k, or token-mask change.
- PI/OpenAI: 2526 completed in 60s (7.86s main). Pooling recovers Congo at rank 2 at prefix `The country with Brazzav`; other concepts remain outside top32 (Iceland 60, Bulgaria 942, Turkey 5010, spider 427). No goal completed. `out/2026-09-30_082747_jlens-one-pass/readout.json`.
- PI/OpenAI: 2528 changes only the readout/edit layer to block 23 (residual 24), retaining raw last-position scores, k=32, prompt mask, swap strength and continuous final-three-position coverage. Default remains midpoint block15; other variants are not combined. Four country readouts and four 32-token conditions, five-minute cap; follower proc_d5bd.
- PI/OpenAI: 2528 finished in 40s. At residual24, source readout begins `spiders, spider, 蜘蛛`; after J swap it begins `dog, dogs, dog, Dog`, but still answers8 (p4=0.342; shift+2.25). Country readout 1/4, tied with plain lens. This locates a readable downstream state but does not improve the successful earlier edit.
- PI/OpenAI: 2531 keeps edit16 and observes24 in the same pass, with observer output never used for editing. Four fixed new English prompts add a small readout check; max160 generated tokens, five-minute cap, follower proc_6b4a. Removed concluded diagnostic CLI branches; historical code remains in git.
- PI/OpenAI: readout exclusion caveat: spider's block23 readout includes `eight` although the literal output token is `8`. Do not treat a numeric-token-only exclusion score as semantic answer exclusion; inspect number-word aliases separately before claiming the goal.
- PI/OpenAI: 2531 reproduced the early 8→4 change while later readout still contains spiders (rank1) and dogs (rank29). On four new simple English cases J readout passes bird only by the literal metric; the currency baseline answers `100% gold`, so not all probes establish the intended reasoning. Plural `dogs` at rank7 also exposes a singular-only scoring limitation. Do not call this complete concept replacement.
- PI/OpenAI: 2533 reverse test stayed4: p8 0.0072→0.0082, shift -0.125 nats (desired reverse sign, tiny effect). 2536 now changes only prompt coverage to all positions, matching the reference, on the same dog input; follower proc_f48e.
- PI/OpenAI: next readout candidate, separate from editing: subtract a reusable offline forecast of next-token probabilities from J-lens probabilities at the same layer. Use generic WikiText activation pairs, no task/language labels. Check forecast agreement on held-out calibration records against the plain lens before interpreting it. Cached corpus extraction is CPU-only (proc_53c3), with the existing eight-day package-age hold intact.
- PI/OpenAI: 2536 also stayed4, p8=0.00821. Full batch evidence committed f1a9786; both goals remain open. Read-only reviewer flagged intended-vs-actual output scoring, probability calibration, and an oracle control. Implemented actual-word scoring, finite top32 membership, separate alias scores, token-pair AUROC, held-out KL/final-position accuracy, and explicitly non-deployable J-minus-final control. Affine algebra passed identity and held-out synthetic-map tests at seeds0/1.
- PI/OpenAI: 2539 queued at commit45724a4:32 generic WikiText calibration records and4 validation records, eight existing development probes, no interventions, at most32 generated scoring tokens, five-minute cap; follower proc_526c. This is one learned output forecast, not language-labelled training. Reviewer artifact: slop/reviews/2026-09-30_offline-forecast-review.md. It can distinguish a poor forecast from a poor probability-subtraction rule; it cannot establish either goal by itself.
- PI/OpenAI: 2539 completed111s. Forecast vs plain on512 held-out prefix positions: argmax agreement46.1% vs7.0%, KL1.624 vs8.132 nats. Actual-output joint recovery is4/8 for raw J, J-minus-forecast and J-minus-final oracle (3/7 when intended answers appear), versus1/8 plain. Thus no recovery gain on these development prompts, despite improved forecasting. Artifacts committed in d11369a.
- PI/OpenAI: 2541 tests those frozen readouts on16 new English prompts in data/english_hidden_words_v1.json, with the reference factual prefix and no trailing space. Labels/aliases fixed before the run, all failures retained; no refit of forecast.pt. Follower proc_5200. 2542 separately tests reverse editing at residual24, changing only layer versus2533; follower proc_c038. Both queued normally with five-minute caps, no queue reordering. No goals completed.
- PI/OpenAI: 2541 failed a scoring assertion, not model inference. CPU reproduction on the pinned tokenizer found six shared `Bra` variants between Brazil and Brasília; all other15 cases had disjoint canonical labels. Fixed scorer to exclude ambiguous prefixes from both label classes without removing them from readouts, and to fail when the hidden concept is actually said. Dataset, model, checkpoint and readout rule unchanged. Retry2548 (ac074cc), follower proc_4234. Completed cases now persist immediately.
- PI/OpenAI: 2542 reverse at residual24 still answers4; J swap_log_odds_shift=0, p8=0.00723. Its readout removes dogs without elevating spider. That suggests checking word-form and direction-normalisation effects before another layer search; it does not establish the cause. Both goals remain open.
- PI/OpenAI: 2548 completed79s. On16 fixed English probes, raw J and J-minus-forecast each pass4/16, plain3/16; on12 expected-answer cases, both J variants and plain pass2/12. Raw J finds a hidden alias in10/12, but eight also contain spoken words. Forecast often predicts function words on these factual prompts despite its generic-text validation improvement. Evidence committed4c7a27a.
- PI/OpenAI: reread scope: goal1 permits end-of-pass readout; only goal2 forbids information after an earlier edit. Job2554 tests J24 with the established final-layer word mask against equally masked plain24/27 on the now-observed16 probes, readout only (proc_20ba). This must never be presented as usable for an earlier intervention.
- PI/OpenAI: separate proposed intervention variant exchanges raw lens numerators via the dual basis, rather than unit-direction coordinates. A CPU algebra check timed out120s with no output; no causal GPU run of this variant is queued. Traced retry proc_afdf will identify startup versus algebra delay. Code commit4c7a27a records both variants; goal2 remains unfinished.
- PI/OpenAI:2554 completed242s: final-layer top20 mask gives J5/16 vs plain27 4/16 (5/12 vs4/12 expected-answer cases), but excludes several unspoken hidden country names.2555 completed96s: raw singular scores exchange after casting, yet reverse remains4, shift0. CPU assertions printed PASS twice but process timed out during/after final cleanup; do not count its command as successful. Full audits appended to slop/audits/2026-09-30_status.md.
- PI/OpenAI:2560 changed only mask cap20→1: J9/16 vs plain27 8/16; on12 expected answers8/12 vs7/12.2561 changed only singular→plural raw-score directions at24: spiders now ranks3 and dogs leaves top32, but initial answer still4, shift0. Readout change is not coherent causal replacement. Both complete logs were read (33/33 and41/41 lines).
- PI/OpenAI: froze data/english_hidden_words_v2.json at4d24e61:16 new concepts, same prefix and scoring, no output-based selection. Job2566 tests unchanged J24/k32/greedy-next-token mask vs equally filtered plain24/27, five-minute cap, follower proc_6d4f. This is the next generalisation check; v1 is development data now. Goal2 next needs a broader representation/control rather than more lexical spelling variants; reusable offline donor contrasts are within the approved scope, but are a method change that must be reported, not presumed goal completion.

- PI/OpenAI:2566 failed because `foal` has no eligible vocabulary prefix. Scorer-only repair95c4c2d retains all16 prompts and marks unsupported labels explicitly;2567 succeeded, literal J11/16 versus plain27 7/16. A valid `colt` response need not match the frozen `foal` answer label.
- PI/OpenAI:2570 evaluates the same J24/k32/greedy mask on six translation pairs, eight prompts each. Five test pairs give J33/40, plain24 33/40, plain27 28/40. Concepts recur across pairs; these are prompts, not40 independent concepts. `nuage` is unscorable and remains in the denominator.
- PI/OpenAI:2577 replay0ca72ad exactly reproduced all80 readout rows from2567 (prompts, generations, top32, literal and alias scores). Requiring predeclared answer aliases reduces J to10/16 and plain27 to6/16; AUROC0.833 versus0.842. Inspecting all32 tokens then found four additional definite translated-answer leaks in J (柏林,维也纳,曼谷,小猫) and one in plain27. Therefore semantic exclusion is at most6/16 versus5/16 under these checks, not established by the original headline. Posthoc annotations are separate in data/english_v2_answer_alias_audit.json; coverage remains incomplete.
- PI/OpenAI:2573 extracted eight frozen generic donor prompts at block15, difference norm6.901978; no question or answer labels.2575 full donor contrast changes dog4 to8 with p8=0.920186 and a spider/web readout, but applied prefill norm is65%; J-projected contrast answers6 at32% norm. The original random control matched the smaller projection, not full contrast. This is a new donor method, not a reproduced coordinate swap or completed goal.
- PI/OpenAI:2579/2580/2581 queued immutable3494ae7 source: compare full/J-projected/random at the full donor norm; reverse legs, new reverse skeleton inside-to-outside property, then forward legs. Same donor/checkpoint, block15, last3 plus decode,32 tokens per condition; one random seed. Followers proc_10e6/proc_ae4b/proc_84b7. All goals remain open.
- PI/OpenAI:next readout test removes the normalised readout activation's component along the model's predicted output-token row. No language labels or extra model are used. A global synonym filter was considered but would erase the intended hidden English translation too; translation-role isolation and English bridge-concept exclusion are different criteria. Test projection against unchanged masked J/plain readouts on the observed v2 set with the disclosed four-alias audit; this is development, not another held-out result. Fresh read-only review315512f2 is running on code and prior artifacts through the configured OpenAI-Codex reviewer.

## Interview

### 2026-09-30 07:42

> 1 y
> 2 y reusable offline . y
> 3 y
> 4 y
