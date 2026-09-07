# Active intervention research

Written by Codex/GPT-6. Goal remains active: get reliable concept intervention,
with recomputed suppressed readout and coherent target consequences. Do not call
word substitution alone success. Prompt stays implicit spider; ant expects6,
dog expects4. Steering covers last3 prompt tokens and all32 output predictions.

Earlier completed: jobs538–545. Fixed template-contrast condition52 (L24 C1 full
residual mean difference) changes all4 predeclared heldout prompts to6 for ant and4
for dog, with target identities in32tokens. Ant readout still poor. Long128tokens
on selection prompt: ant gives Formicidae/6legs but false nesting claim and beetle
aside; dog repeats "dog? No". Do NOT call short successes sustained coherence.

Current code: `42524d3`. User changes README.md/.gitignore are untouched.
Research code in scripts/oat_sweep.py and scripts/demo.py; no public demo promoted.

Completed GPU jobs (default lane):

- 516 `coordinate-layer`, ant, out/2026-09-07_coordinate-layer-ant
- 517 `coordinate-layer`, dog, out/2026-09-07_coordinate-layer-dog
- 518 `coordinate-band`, ant, out/2026-09-07_coordinate-band-ant
- 519 `coordinate-band`, dog, out/2026-09-07_coordinate-band-dog
- 520 `template-contrast`, ant, out/2026-09-07_template-contrast-ant
- 521 `template-contrast`, dog, out/2026-09-07_template-contrast-dog

Each command is `uv run scripts/oat_sweep.py --sweep NAME --target ANIMAL
--prompt-mode chat-assistant-prefill --output-dir PATH`. 516/517 each36 conditions:
L4,8,12,16,20,24 x C0,.25,.5,1,2,4, raw named swaps. 518/519 each45:
source-dominant-only swaps at five single layers and four five-layer bands,
C0,.25,.5,1,2. 520/521 each68: eight matched explicit-animal templates without
leg counts, averaged target-source last3 suffix activations; six single layers,
full residual or persistent-space projected, C0,.5,1,2,4, plus8 matched randoms
at L16 C2. C1 in this method is the unnormalized mean matched-template difference.

Tests passed for nonorthogonal swaps, norm preservation, one-sided idempotence,
untouched prefixes, continuous decode; config counts checked. Template extraction
asserts exact same last3 token IDs. GPU execution remains unverified until jobs run.
New coordinate traces include after_model_dtype to audit bf16 realization.

The preceding shared GPU training job was515; do not interrupt other repo jobs.
User explicitly said: don't check every minute, attach followers and wait for end.
Follower exec session IDs:516=58379,517=89924,518=35363,519=92974,
520=90065,521=13699. Revalidate handles on continuation, don't restart jobs on timeout.

Scientist panel completed two rounds: KimiK3, DeepSeekV4Pro, Grok4.5, Inkling.
All artifacts in slop/reviews/intervention_*.md, brief and corrections same folder.
Round1 contained false objections (reflection nonorthogonality, nonorthonormal
projectors, missing C0/stale readouts). Round2 withdrew them. All favored matched
template contrasts before VJPs. Accepted: cross-task/held-out checks and fresh random
controls for selected conditions; static unembedding may not encode causal concept.
Rejected: QR-renaming named coordinates, stopping decode steering, using global
hidden cosine as semantic proof, arbitrary norm thresholds, DeepSeek's example
templates containing leg-count answers, unit-length C without a natural dose scale.

Next after results: inspect every generation and trace, compare actual joint
identity/count consistency. Use good conditions on predeclared held-out phrasings
and other consequences; add matched random controls at the selected layer/dose.
If none, adapt the next method using evidence, not a generic null verdict. Promising
untried mechanisms: dynamic per-generated-token suppression space (shadow forward),
layer-specific future-effect VJPs, matched-template coordinate clamping.

Before GPU execution: fixed normalized detector/basis geometry mismatch. Scored
direction is gain-weighted row normalized BEFORE vocabulary centering; basis now
matches. Tests verify invariance to positive row scaling and a two-dimensional
counterexample. Raw named directions unchanged. Projected queued runs use corrected
bases (`basis_geometry` diagnostic). Journal contains proof and limitations.

Added --source-prompt and --condition-index to rerun a fixed sweep condition on new
phrasing without selecting per-prompt settings. Four held-out prompts predeclared
in slop/research/2026-09-07_heldout-intervention-prompts.json before new outputs seen.
Wait orchestration cell635 follows all six job sessions until completion; it may
remain active across assistant actions. Never restart jobs due to an expired observer.

Update after jobs516–545:
- Strong raw swaps522/523 C6–32 did reach6 for ant, but mostly spider/6 or
  taxonomy errors. Dog strong swaps often6 (not expected4), then lexical loops.
  All72 generations read. Mere weakness is not enough to explain these failures.
- Template520/521: same condition52 gives ant p6=.977210, dog p4=.920561.
  This is FULL residual, not suppressed-only. All136 generations read/reviewed.
- Projection536/537: rescale projected delta to full-delta norm; ant remains8
  or becomes2, dog4 but worse text. Ant retained fraction .198–.278 at ranks4–32.
  All12 norm-matched randoms per animal remain8 (selected L24 C1 control).
- Long526/531: full128token continuations expose ant drift and dog loops.
- Heldout527–530/532–535 FAILED argparse before inference: pueue reparsed
  unquoted prompt. Requeued entire command as one shell-quoted string;538–545
  succeed. Prompts/trailing spaces exact. No model/config change for retry.
- Per-position readouts now logged so union cannot hide an unpatched earlier
  token. Ant heldout0 final-position readout itself is poor, not prefix leakage.

RUNNING/QUEUED:547 ant,548 dog `template-clamp`, max128tokens,16conditions each.
L12/16/20/24 x C0/.25/.5/1. v=unit matched-template mean difference;
t=mean target activation dot v; edit h+=C*relu(t-h.dot(v))*v.
Still last3+all decode, not stopping steering. Each condition also applies clamp
to clean donor and saves full generation and per-token coordinate deficit/norm.
C1 idempotence/complement/decode tests passed. Reviewer warned threshold can track
syntax/residual scale; donor preservation is the discriminator. Do not call J-lens.
Followers:547 session17674;548 session43993. Other repo job546 is not ours.
Finished wait cells673/685 can be discarded; earlier cells635 may be stale.

Next: audit all clamp outputs incl clean donor. If useful freeze a common setting,
test heldouts at128tokens. If not, consider smaller template shifts across layers
and all content positions (source clue KV may cause correction loops), then
future-effect VJP/different direction estimator. Keep goal active. Journal needs
post-heldout/long/projection entry; model-generated false taxonomy must stay visible.

Further queued work (all blocked behind other repo546 at last status; do not interrupt):
-549/550 ant/dog template-scope,32conditions each,128tokens: L16/20/24 x
  last3/all-content x C0/.5/1/2; band16–20 x last3/all x C0/.125/.25/.5.
  Followers549=37509,550=36756. Tests compare retained source clue context and
  smaller distributed edits. All generation remains steered.
-551 future-coordinate condition0 smoke, ant: actual contracted mean-J estimator,
  not a template difference. Corpus cached WikiText2 train Arrow path in argv;
  random seed0 samples16 eligible>=600character records, truncate CONTENT to128,
  official assistant-prefill render, content mask afterfirst16 and beforelast.
  Penultimate raw residual31, source12/16/20/24. Three sequential VJPs of RAW
  spider/dog/ant unembedding rows. Target positions SUM, source positions MEAN,
  prompts MEAN (no division by remaining futurecount). Official SHA581d398.
  Firstprompt firstword finite differences eps.125/.5/2 logged; must inspect
  agreement before full40condition sweep. No claim of full-vocabulary J readout.
  Follower551=82436. On success future_lens.json and future_lens_vectors.pt
  contain fitted diagnostics and directions. No full future sweep queued yet.

Reference reviewer found hook ordering bug before GPU smoke: HF persistent capture
can run before later intervention hooks. `layer_hooks` now uses prepend=True so
exact edited layer is captured AFTER edit. Regression passes. fit grad_leaf uses
in-place requires_grad_(True), not detach/replace, matching official hook. Previous
selectedL24 detectorpeak25 is later than edit and this does not explain antreadout.
See slop/research/2026-09-07_future-vjp-reference.md for exact code citations.
New dependency pyarrow>=21 installed via uv with existing8day hold unchanged.

Journal now has heldout/long/projection entry and full audit at
slop/audits/2026-09-07_template-transfer.md; independent review also committed.
Active wait cell692 follows547/548 only; scope/future followers need orchestration
if waiting. Latest meaningful result: all8heldout short count+identity pass, no
sustained coherence or ant readout claim. Keep researching, userAFK.

LATEST:547–551 all SUCCESS; cells692/721 terminal. All32 clamp source and32donor
generations plus all64scope generations read. Clamp ant stillloops; dogL24C1
readable qualified explanation (acknowledges dogs don't spin webs), repeat.055
vs additive.488. Clean dog edited at100% positions so threshold not semantic detector.

Scope condition27 is best common candidate: bandL16–20, last3, C.5 perlayer,
full template delta. Ant p6=.963228, coherent ant/Hymenoptera/sixlegs explanation
ENDS NATURALLY after110tokens, all5layers109decodecalls. Dogp4=.927658, dog/fourlegs
through128tokens with conditional aside, no loop. Ant suppression readout stillpoor.
All-content edits do not consistently help. Journal has full110token ant quote.

Future smoke551 PASSES backward; FD8.219/8.200 at eps.125/.5 vsgrad8.279 (~1%);
eps2 nonlinear6.199. Split-halfcos.881–.980. Reviewer verifiesmask22..148 of150
renderedtokens, rawresidual31, source-mean/target-sum. Corpus NOT animal-free:
one seeded randomrecord discusses jumping spiders. Do not remove/cherry-pick it.
No official WRITING helper in repo; rawWU follows paper definition, unitcolumn
normalization is our additional choice, not independently verified official practice.

NEW queued/followed jobs:
-553/554 future-coordinate ant/dog40conditions (L12/16/20/24 x raw/rank4projected
  x C0/.5/1/2/4),32tokens. Follow553=92560,554=71022.
-555–558 ant,559–562 dog: template-scope condition27, same4validation phrasings,
  max128tokens, frozen common setting. Not fresh untouched prompts: these were
  previously used on L24 template method. Paths template-band-ANIMAL-validation0..3.
  Followers555=16943,556=52401,557=65406,558=82486,559=34230,560=32203,
  561=60818,562=24786. functions store future_band_followers contains all10.
Other repo552 may precede these; don't interfere. Need attach waiter tothesehandles.

Next review long validation and future grids, compare readouts. Possible next
direction if future swap weak: project useful template delta into named future-J
span instead of raw-vocab suppressed span; assess exact normalization choices.
Do not narrow goal to count-only or call full-residual success suppressed-only.
