# Research journal

## 2026-09-06 -- Causal replacement depends on prompt format and token aggregation

This entry records the search for a spider-to-dog causal replacement that changes both the answer and the recomputed readout.

| model input and method | decoded answer | p(4) | p(8) | exact donor-readout overlap |
|---|---:|---:|---:|---:|
| raw Base | 8 | 0.056421 | 0.882568 | not applicable |
| raw, union, L24, last four source tokens, C=2 | 4 | 0.477770 | 0.421631 | 5/8 |
| raw, union, L24+L26, final source token, C=2 | 4 | 0.687441 | 0.252896 | 4/8 |
| user-message chat template, best tested L24 readout | 8 | about 0.000001 | about 0.0006 | 5/8 |

`p(4)` and `p(8)` are next-token probabilities at the first generation boundary. The exact-overlap column counts identical entries shared by the causal and unmodified donor top-eight readouts. Evidence: [raw layer combinations](out/2026-09-06_211653_layer-combo-raw/run.md), [chat layer combinations](out/2026-09-06_211800_layer-combo-chat-fact/run.md), and [default replication](out/2026-09-06_213629_causal-demo/conditions/000_default_default/run.md).

The raw L24, last-four, C=2 continuation was:

```text
4.
Hypothesis: The animal that spins webs has 4 legs.
Is the hypothesis entailed by the fact?

<think>
Thinking Process
```

The corresponding recomputed readout was:

```python
['狗粮', '吠', 'สุนัข', ' собаки', ' canine', ' собак', ' perros', ' cão']
```

The hard-min persistent selector returned arbitrary-looking vocabulary because sparse nonnegative scores tied at zero. Replacing it with mean score times positive-position fraction removed the hard tie, but all tested persistent conditions still answered 8. The union selector reproduced the dog-like readout and answer change. Evidence: [hard-min run](out/2026-09-06_213326_persistent-direction-raw/run.md) and [soft-persistence run](out/2026-09-06_213454_persistent-direction-raw/run.md).

My read: it is very probable that the extra instruction and chat response format changed which state exists at the first generation boundary. It is likely that the union captures useful token-specific directions which the tested persistence reductions discard. A chat template with an assistant-prefilled partial fact is the next discriminator because it uses the official template while preserving digit-first completion.

The current evidence supports the raw union intervention and leaves the chat-template demonstration unresolved.

<!-- Written by Codex/gpt-5.6-sol. -->

## 2026-09-06 -- Assistant-prefill chat crosses at moderate strength

This entry resolves the earlier chat-template question with an assistant-prefill format.

| C | first answer | p(4) | p(8) | exact donor-readout overlap |
|---:|---:|---:|---:|---:|
| 2.0 | 8 | 0.373941 | 0.544081 | 3/8 |
| 2.5 | 4 | 0.684335 | 0.196065 | 4/8 |
| 3.0 | 4 | 0.809186 | 0.066422 | 5/8 |
| 4.0 | 4 | 0.824805 | 0.019398 | 6/8 |

Here, `C` scales the constructed component replacement, and `p(4)` and `p(8)` are next-token
probabilities at the first generation boundary. Every condition used the tokenizer's chat template
for extraction and generation, with the incomplete fact as an assistant-message prefill. Evidence:
[job 405 run table](out/2026-09-06_220932_chat-strength/run.md) and
[C=2.5 condition log](out/2026-09-06_220932_chat-strength/conditions/001_strength_C=2.5/run.md).

The continuation at the smallest measured crossing was:

```text
4.

**Explanation:**
The animal that spins webs is the **spider**. Spiders belong to the class *Arachnida*, which is
```

The recomputed readout at that condition was:

```python
['狗粮', '吠', 'สุนัข', ' собаки', '养犬', ' собак', ' perros', ' dogg']
```

My read: C=2.5 is a better notebook setting than the C=2 prior because it is the smallest tested
value that changes the greedy answer while retaining a grammatical, on-topic continuation. This is
a selected single-prompt result, so it does not show that the method transfers a reusable dog
concept rather than a target-answer state.

The assistant-prefill chat demonstration now changes both the answer and the suppressed readout.

<!-- Written by Codex/gpt-5.6-sol. -->

## 2026-09-06 -- Executed notebook reproduces the chat intervention

This entry records the final notebook execution rather than the preceding sweep.

| condition | first answer | p(4) | p(8) | suppressed readout |
|---|---:|---:|---:|---|
| Base | 8 | 0.028546 | 0.945299 | web-related |
| Causal intervention | 4 | 0.701417 | 0.200959 | dog-related |

The causal table reports `delta log p(4)=+3.202` and `delta log p(8)=-1.548` relative to Base.
Both continuations contain exactly thirty-two generated tokens. They begin with the different
answers and then identify the unchanged subject as a spider. Evidence: [executed
notebook](nbs/demo.ipynb) from pueue job 406.

My read: the notebook is a successful single-example causal demonstration under the requested
L24, final-four-token prior, with C increased from the unsuccessful value of two to the smallest
tested crossing at two and a half. The causal interpretation remains limited by configuration
selection on this prompt and by the possibility that the intervention transfers an answer state
rather than animal identity.

The public notebook now contains the complete result needed to inspect this example.

<!-- Written by Codex/gpt-5.6-sol. -->

## 2026-09-07 -- Fixed spider-to-ant transfer fails

This entry tests whether the selected spider-to-dog configuration transfers to an ant donor.

| condition | first token | p(6) | p(8) | swap log-odds change |
|---|---:|---:|---:|---:|
| Base | 8 | 0.015245 | 0.943160 | 0.000 |
| C=2 | 8 | 0.008095 | 0.935690 | -0.625 |
| C=2.5 | 8 | 0.007667 | 0.886223 | -0.625 |
| C=3 | 8 | 0.006092 | 0.797945 | -0.750 |
| C=4 | 2 | 0.004487 | 0.403940 | -0.375 |

The swap log-odds change is the intervention-induced change in `log p(6) - log p(8)`.
The fixed held-out condition is C=2.5; the other rows are a diagnostic strength sweep. The
unmodified donor readout was `['Social', 'social', ' vor', 'V', ' vaya', 'ocial', ' sociales',
' división']`. Evidence: [job 485 run table](out/2026-09-07_182300_chat-ant-strength/run.md)
and [fixed C=2.5 condition](out/2026-09-07_102128_chat-ant-heldout/conditions/000_default_default/run.md).

The clean donor generated `6.` followed by an explanation that identified the animal as an ant,
with `p(6)=0.899812`. Evidence: [job 487 donor check](out/2026-09-07_183000_chat-ant-donor-check/conditions/000_default_default/run.md).

My read: the current spider-to-dog demo is probably pair-specific. The ant result is more
consistent with a detector that selected an unrelated subspace than with an intervention that was
only too weak, because every tested strength reduced the target answer probability even though the
clean donor answered correctly. The donor readout may encode the prompt's social-colony feature
rather than the answer, so a different ant wording could distinguish prompt-specific detector
failure from a broader lack of transfer. That would be a new development test rather than part of
this held-out result.

An earlier raw-prompt L26, final-token, C=4 condition did generate 6 with `p(6)=0.487144` and
`p(8)=0.379388`. That configuration differs on prompt format, layer, token range, and strength, so
it shows that the ant target can work under another selected configuration but does not rescue the
fixed transfer test. Evidence: [earlier causal confirmation](out/2026-09-05_211609_causal-confirmation/result.json).

The fixed configuration does not produce a working ant demonstration.

<!-- Written by Codex/gpt-5.6-sol. -->

## 2026-09-07 -- Token-persistent SVD changes digits mainly through source removal

This experiment tests a suppressed subspace shared across past tokens.

Thin SVD combines per-token suppressed spaces separately for source and donor. Their shared span receives a fixed projected difference of mean residuals. The corrected runner captures readouts during actual generation, and checks exact zero-strength identity. It completed 208 development conditions across rank, strength, detector depth, layer bands, continued generation, donor wording, token windows, and controls. [Complete evidence and code audit](slop/audits/2026-09-07_svd-token-persistence.md).

The final separation at retained rank 1, L24, four tokens, C=12 gave these measured values:

```text
source_remove: p6=0.7933498024940491, swap_log_odds_shift=6.125
difference:    p6=0.6720733046531677, swap_log_odds_shift=5.375
target_add:    p6=0.01483974326401949, swap_log_odds_shift=0.0
```

The score is the change in log probability ratio of six versus eight, in nats. [Job 500](out/2026-09-07_190240_svd-ant-parts/run.md). Removal and combined edits both generate six then explain that the animal is a spider. Continued edits often generate social-related content instead of ants. A matched-size random edit and some dog-directed settings also generate six. Dog rank 4 at C=8 does give a dog-related readout and p4=0.862182. These are selected development results, not generalization estimates.

My interpretation: source removal probably explains the apparent ant transfer at the selected setting, because removal alone is stronger and donor addition alone has no log-odds effect. The SVD construction itself passes the tested projector and hook invariants. The next useful change should improve donor concept extraction; increasing strength has already exposed the wrong social feature. Reward-hacking and ground-truth pass counts are not defined for this inference experiment, so digit matches are not relabelled as semantic passes.

The code and full continuations are ready for review, while coherent ant concept replacement remains unresolved.

<!-- Written by Codex/GPT-6. -->

## 2026-09-07 -- Continuous steering from the last three prompt tokens

This rerun corrects the earlier prompt-only interpretation.

Wassname specified prompt slice `-3:` and steering through all generated tokens. Jobs 504
and 505 each completed 45 conditions with last-three prefill positions `[33,34,35]`,
31 steered decode calls, and exactly 32 output tokens. Prefill predicts the first output;
the decode calls predict the remaining outputs. Coverage and zero-strength identity are
asserted. Both prefill and final-decode readouts are saved. The new default is continuous
steering; the instruction is recorded in AGENTS.md.

For spider-to-ant, the expected answer is six rather than Base's eight, with coherent
ant content. Five conditions start with six, but none identifies an ant coherently.
Rank-one combined C=12 produces:

```text
6.

**Explanation:**
The animal that spins social or hunting social networks is the **social network** (a type of social network). However, the
```

Source: [continuous ant sweep](out/2026-09-07_191511_svd-ant-continuous-last3/run.md).

For spider-to-dog, the expected answer is four with coherent dog content. Two conditions
start with four but repeat the bark token. Rank-four combined C=8 produces:

```text
4.

**Explanation:**
The animal that is most famously known for spinning dog吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠
```

Source: [continuous dog sweep](out/2026-09-07_191640_svd-dog-continuous-last3/run.md).
Rank-two combined C=8 instead names dog but answers eight. Independent Codex/GPT-6 review
read all continuations and confirmed coverage; no condition established both correct
donor-directed answer and coherent donor explanation. Each job took about eighty seconds.
The synthetic SVD and hook tests passed in the experiment's cached Python environment.

My interpretation: continuous steering has clear semantic effects, but the fixed displacement
is too disruptive at strengths that change the digit in these settings. Ant donor-only
steering still targets social content. This does not show all continuous interventions fail.
Jobs 507 and 508 test intermediate strengths with exactly the same continuous coverage.
Reward-hacking and ground-truth pass counts are undefined here; digit matches are not
semantic passes.

The main continuous comparison is complete, and intermediate strengths remain under test.

<!-- Written by Codex/GPT-6. -->

## 2026-09-07 - Intermediate continuous strengths completed

The pending intermediate-strength runs finished before the named-coordinate swap tests.

Job 507, dog rank four C=5, logs `p_target=0.5034767985343933` and
`p_source=0.39210814237594604`. Its entire continuation is:

```text
4.

**Explanation:**
The animal that spins webs is the **dog** (or more accurately, the **dog** in the context of the id
```

Source: [dog refinement](out/2026-09-07_192255_svd-dog-continuous-refine/result.json).
Job 508, ant rank one C=10, logs `p_target=0.5622626543045044` and produces:

```text
6.

**Explanation:**
The animal that spins social or hunting webs is the **social spider** (specifically the genus *Araneus*, such
```

Source: [ant refinement](out/2026-09-07_192327_svd-ant-continuous-refine/result.json).
All eighteen continuations were inspected. These are selected development conditions,
not held-out results. Both retain the previous last-three-prompt plus continuous-decode
coverage. Reward-hacking count `hack_s` and ground-truth count `gt_s` are not defined
for this inference experiment; digit matches are not counted as semantic passes.

My interpretation: the dog refinement shows partial semantic transfer without immediate
repetition, but its explanation remains truncated and asserts a web-spinning dog. Ant
still produces social content rather than an ant identity. This is more specific evidence
than the earlier statement about the initial coarse grid.

Named-coordinate swaps are now being tested separately from fixed donor displacements.

<!-- Written by Codex. -->

## 2026-09-07 - Named-coordinate swaps measured

Named-coordinate swaps change the readout and animal words more readily than they produce a consistent explanation.

Jobs 512 and 513 used Qwen3.5-4B at L24, last three prompt tokens plus all cached
generation steps. Each tested raw and persistent-space-projected named directions
at C=0,.25,.5,1,2,4. C=1 is exact coordinate exchange; larger values extrapolate,
without residual renormalization. These are unembedding-derived directions, not
the paper's future-Jacobian estimator. Code commit: `325d005`.

Raw ant C4 readout:

```python
[' ant', ' Ant', 'Ant', '.ant', ' ANT', '_ant', '抗', ' antim']
```

Its full continuation:

```text
8.

**Explanation:**
The animal that spins webs is an **ant**. Ants belong to the class *Insecta* (insects).
```

Expected ant answer was6, not8. No ant condition produced6 first. Dog produced4
in three conditions, but each continuation mixed dog with spider. Raw dog C2:

```text
4.

**Explanation:**
The animal that spins webs is a **dog** (specifically, a spider). Spiders are classified as arachn
```

This row has p4=0.4633 versus base0.0285 and log-odds movement+3.625 nats.
All twenty-four generations were inspected; samples above are selected to show
the mismatch between numerical and semantic effects, not held-out successes.

Sources: [ant grid](out/2026-09-07_210840_coordinate-swap-ant/run.md),
[dog grid](out/2026-09-07_210919_coordinate-swap-dog/run.md),
[complete audit](slop/audits/2026-09-07_named-coordinate-swap.md).
Independent review confirmed C0 identity, three prefill positions and thirty-one
decode calls, and float32 coordinate algebra. Post-cast coordinates were not
logged. Runs took about half a minute each, excluding queue time.
Reward-hacking `hack_s` and ground-truth `gt_s` are undefined for this experiment;
digit matches are not counted as semantic passes.

My interpretation: named directions avoid the social-feature problem for raw ant
steering, but their word-level effects do not yet give consistent downstream
computation. Earlier-layer intervention is a useful next discriminator; dynamic
swapping can also reverse target-dominant coordinates and needs a separate control.

The measured improvement is in named readout and animal wording, not reliable concept replacement.

<!-- Written by Codex. -->

## 2026-09-07 - Earlier layers, matched templates, and a detector geometry fix

The active research now tests intervention timing and how the concept direction is estimated.

Jobs 516/517 test raw coordinate swaps at L4,8,12,16,20,24. Jobs 518/519 test
source-dominant-only swaps at single layers and five-layer bands. Jobs 520/521
test averaged activation differences from eight template pairs differing only in
the animal name, with no answer digits or leg-count task in extraction. All retain
last-three-prompt and continuous-decode steering. Each condition will save its full
generation. These jobs were queued, not completed, when this entry was written.

The scientist panel (Kimi, DeepSeek, Grok, Inkling) favored matched-template contrasts
before future-effect VJPs after a correction round. Several first-round mathematical
criticisms were withdrawn. [Brief, corrections and review decisions](slop/handovers/2026-09-07_reliable-intervention-loop.md)
preserve what was accepted and rejected. Panel agreement is advice, not an experiment.

A separate code review confirmed that normalized suppression scoring and basis
construction used different vector directions. For unembedding rows `(2,0),(0,1)`
and unit gain, scoring token zero uses `(.5,-.5)` but the old basis uses `(1,-.5)`.
For residual `(1,2)`, their projections are `(-.5,.5)` and zero, respectively.
Basis construction now applies normalization before centering when the scoring flag
requests it. The default unnormalized branch is unchanged.

The new regression output is:

```text
PASS: normalized detector spans resist row scaling and match scored directions
```

Source: [test](scripts/test.py), [implementation](suppressed_activation_subspace.py).
This fix changes projected intervention geometry; raw named-swap vectors are unchanged.
Queued projected-template conditions will use the corrected basis and record its geometry
and executed commit. The prior projected L24 results remain historical measurements.

My interpretation: consistent scored directions are necessary for our claimed detector
subspace, but whether this repair improves animal transfer remains unmeasured. The
next decision should follow the queued generations. Reward-hacking and semantic pass
counts are not yet measured for these jobs.

The goal remains reliable concept transfer, with independent prompt checks after candidate selection.

<!-- Written by Codex/GPT-6. -->

## 2026-09-07 - Matched-template directions change both animal answers

Jobs 516–521 completed. Earlier raw swaps (L4–24, C0–4) and one-sided
single-layer/band swaps (C0–2) did not produce an ant six-leg answer.
One-sided dog L24 C2 generated four and dog, followed by a invented dog named
"Web". This is a change from the ordinary swap's dog/spider mixture, not yet
evidence of a coherent full explanation. Stronger raw doses C6–32 are queued
as jobs 522/523 because early C4 conditions remained fluent and weak.

Matched-template mean differences give a more useful result. At the SAME L24,
C1, full-residual setting (condition 52), ant p6=0.977210 and dog p4=0.920561.
Base p6=0.015245, p4=0.028481, p8=0.943160. The ant generation is:

```text
6.

**Explanation:**
The animal that spins webs is the **ant** (specifically, ants are known for their ability to carry heavy loads and
```

The dog generation is:

```text
4.

**Explanation:**
The animal that spins webs is the **dog** (specifically, the dog is a common animal associated with barking and
```

These are selected 32-token continuations, both unfinished. All 136 template-grid
generations were inspected, grouping identical strings without dropping conditions.
Ant readout remains mostly unrelated (`división`, `سبق`, `пропо`, `spinning`,
`SOC`, `ิตร`, `ปั่น`, `отрица`); dog readout includes `Dog`, `dog`, and dog-related
forms. This does NOT establish the suppressed-subspace hypothesis: the successful
condition uses the full activation difference, without suppression projection.
The rank-four projected ant conditions did not change the first answer to six.

Sources: [ant grid](out/2026-09-07_223632_template-contrast-ant/run.md),
[dog grid](out/2026-09-07_223845_template-contrast-dog/run.md).
Jobs 526–535 freeze condition 52 for each animal: a 128-token continuation on the
selection prompt plus the four predeclared held-out prompts at 32 tokens.
Steering stays on throughout. No separate condition selection per held-out prompt.
Tests passed, including exact coordinate equations, continuous-hook coverage and
normalized basis geometry. A fresh reviewer is auditing template extraction and
readout provenance. Matched-random controls at this selected L24 C1 setting and
other animal consequences remain missing evidence.

Interpretation: estimating directions from matched activations appears more useful
than using vocabulary vectors for this selected prompt. Longer continuations and
held-out results can still overturn that impression; no reliable-demo claim yet.

<!-- Written by Codex/GPT-6. -->

## 2026-09-07 - Frozen template direction transfers, but long text still fails

Jobs538–545 test the same L24 C1 full-residual template direction on all four
predeclared prompts for each animal. Every base answers8 and names spider;
all four ant runs answer6 and name ant, and all four dog runs answer4 and name dog.
Ant p6=.734–.962; dog p4=.708–.919. These are32-token outputs, not complete
explanations. All were read. Jobs527–535's heldout attempts had failed before
inference due to shell quoting; retries preserve the exact strings and setting.

Twelve selected-setting norm-matched random controls per animal all answer8.
Ant max random p6=.160, dog max random p4=.356. Equal-norm projection into the
detected persistent space does not recover ant6 at ranks4/8/16/32; dog can reach4
but text degrades. That failure is not simply smaller projected displacement.

The128-token selected-prompt test exposes the short-output limit. Ant says
`Formicidae` and `six legs` but adds false nesting claims and a beetle aside.
Dog repeats `The animal that spins webs is the **dog**? No.` Its repeated-bigram
fraction is .488. Neither receives a sustained-coherence pass. Ant's recomputed
readout remains poor even at the final patched prompt position.

Interpretation: the matched-template estimator transfers count and named identity
more reliably than our earlier vocabulary direction on these prompts. It does
not yet establish coherent concept replacement or validate suppression selection.
Jobs547/548 test a bounded coordinate update throughout128tokens, with a clean
donor intervention control. This should distinguish continued excessive edits
from retained source-clue conflict, although template-coordinate syntax dependence
is a competing explanation. Exact clamp geometry and cached-decode tests pass.

[Full audit, controls and links](slop/audits/2026-09-07_template-transfer.md).
No public result or notebook was promoted. Goal remains active.

<!-- Written by Codex/GPT-6. -->

## 2026-09-07 - Earlier distributed edits produce a complete ant explanation

Job549 condition27 applies half a matched-template difference at each layer
L16–20, last three prompt tokens and every generated token. It answers6 with
p6=.963228 and p8=.015569, names ant, describes colonies and Hymenoptera, and
ends naturally after110tokens. Each of the five layers records109 decode calls.
The recomputed suppressed readout remains mostly `spinning`, `división`, `SOC`
and other non-ant words. This remains a full-residual intervention, not proof
of suppressed-only causal transfer.

```text
6.

**Explanation:**
The animal that spins webs is the **ant**. Ants are social insects that live in colonies and are known for their ability to carry heavy loads, build complex structures, and communicate through chemical signals. They are part of the Hymenoptera order, which also includes bees and wasps. Ants are characterized by their distinct body structure, consisting of a head, thorax, and abdomen, and they have six legs, which are adapted for their active lifestyle and role in the colony.<|im_end|>
<|endoftext|>
```

Same condition in dog job550 gives4, p4=.927658, dog-like readout and a consistent
dog/four-leg explanation, followed by a conditional aside; it is truncated at128.
All64 scope-grid generations were read. Editing all prompt-content positions
did not consistently improve text; dog band/all/C.5 repeats whereas last3/C.5
does not. Candidate selection is not a reliability result. Jobs555–562 freeze
condition27 on the same four validation phrasings per animal for up to128tokens.
These phrasings have already been used on the earlier template method.

Clamps547/548 do not solve both demos. Dog L24 C1 reduces repeated bigrams from
.488 (additive) to .055 and coherently states `dogs do not spin webs`; ant still
circles around the incompatible clue. Clean dog receives nonzero clamp edits at
every position, despite readable text. Thus the threshold is not an established
semantic detector. The clean ant donor itself includes false12-leg insect claims;
ordinary base-model factual errors must not be conflated with induced loops.
[Independent clamp audit](slop/audits/2026-09-07_template-clamp.md).

Job551 implements actual corpus-averaged future-effect VJPs from the reference,
not template differences. Sixteen seeded random WikiText2 records use the official
assistant-prefill template, with content truncated before rendering. Raw penultimate
residual31 is differentiated against L12/16/20/24 for three vocabulary rows.
Finite differences at epsilon.125/.5 are8.219/8.200 versus autograd8.279; epsilon2
is less linear at6.199. Split-half direction cosines are.881–.980. These checks
support implementation plausibility, not semantic usefulness. Full sweeps553/554
are queued. Corpus, masks, vectors and diagnostics are saved in the job directory.

Reference review also caught a hook-order problem: built-in hidden-state capture
could precede edits at the exact patched layer. Production edit hooks now prepend;
a regression test verifies post-edit capture. For fitting, the earliest source
becomes a grad leaf in place so captured tensors remain connected. Selected L24
readouts use peakL25, so this issue does not explain their poor ant readout.

Sources: [ant scope](out/2026-09-07_231638_template-scope-ant/run.md),
[dog scope](out/2026-09-07_231958_template-scope-dog/run.md),
[future-estimator smoke](out/2026-09-07_232317_future-vjp-smoke/future_lens.json).
Scope runs took200/199seconds; clamps188/187seconds; future smoke33seconds.
Goal remains active: long validation and meaningful ant readout remain unresolved.

<!-- Written by Codex/GPT-6. -->

## 2026-09-07 -- Longer future-effect swaps expose explanation failures

Longer continuations separate answer changes from sustained concept changes.

The ant future-effect swap at L12, C2 starts with the intended answer but later says:

> only ants (and some spiders, though spiders are arachnids with four legs) are known for constructing and spinning webs.

Source: [long ant result](out/2026-09-08_012648_future-ant-L12-C2-long/result.json), job566.
This is not a clean ant explanation. The dog L16 C2 continuation likewise enters
a repeated correction loop. These runs used the same official assistant-prefill
template and continuous steering through the generated continuation.

Source-dominant gating means skipping the swap when the target coordinate already
exceeds the source coordinate. In the paired gated dog run at L24, rank4, C2, the
model instead says:

> it is important to clarify a common misconception: **dogs do not spin webs.**

Source: [gated dog result](out/2026-09-08_013202_future-gated-dog/result.json), job576,
condition011. It sustains dog/four-leg discussion with a qualification, unlike the
lower-layer correction loops. The explanation still reaches the token cap.
All paired ant and dog outputs were read by the main agent and an independent
reviewer. [Complete audit](slop/audits/2026-09-07_template-clamp.md).
The audit verifies patch coverage and gate equations, but these runs have no
fresh zero-strength or random-direction controls. Reward-hacking count `hack_s`
and ground-truth pass count `gt_s` are not measured by this causal-demo task;
neither is inferred from the first answer or repetition metric.

Interpretation, Codex/GPT-6: I think it is probable that avoiding some unnecessary
updates improves selected explanations, because paired outputs differ despite
identical first-answer probabilities. It is not a general cure: lower-layer dog
runs still loop. A coherent qualification is not equivalent to invented biology,
but neither establishes reliable transfer across prompts.

The stronger-band jobs failed before intervening with `KeyError: 16`. The new grid
was omitted from template fitting. The fix is committed in f54cad7, and fitting
now follows selected configuration fields in 759e6e3. Original full crash logs
are preserved in [the crash audit directory](slop/audits/2026-09-08_band-strength-crash).
New jobs578 to581 rerun those conditions; their outcomes remain pending here.

The next test restricts the fixed template difference to the future-effect span,
with natural and norm-matched projections, to separate magnitude loss from a
direction mismatch. This is an alternative subspace test, not suppressed-only evidence.

<!-- Written by Codex/GPT-6. -->

## 2026-09-07 -- Corrected chat attention changes the extracted subspace

The earlier stopping fix also changed prompt attention.

Independent CPU reproduction of the installed Transformers mask function:

```text
old masked_positions [13]
new masked_positions []
```

Source: [mask audit and exact test](slop/audits/2026-09-07_template-clamp.md).
The old call set padding to tokenizer EOS, the chat-message ending, while retaining
the model's different end-of-text EOS. Automatic mask construction therefore hid
the user-turn ending. The corrected padding and EOS in 57a3898 restored attention
to that token; 4a9c8c0 makes the all-ones mask explicit for unpadded prompts.

The selected projected dog run changed its first answer after this fix. Its saved
future-effect directions were nearly unchanged, but its selected suppression
tokens and persistence values changed. The full comparison is in the audit.
The first-token change must not be attributed to a longer continuation limit.

Interpretation, Codex/GPT-6: my previous termination-only statement was wrong.
The simple stopping test omitted the padding-token-in-prompt case. Earlier outputs
remain observations, but comparisons across this fix include an attention change.
Current validation uses the corrected mask consistently for both animal tasks.

The attention correction needs to remain part of every future result's provenance.

<!-- Written by Codex/GPT-6. -->

## 2026-09-07 -- Describing the animal gives coherent full-template continuations

Asking for an animal description avoids the reconciliation seen in these explanation runs.

Jobs622 to625 use full template differences at L20, C=2, on the original and
previously tested alternate spider wording. Steering covers the last three prompt
tokens and every decode step until natural completion. Extraction retains
`Complete the following fact, then explain your answer.` Evaluation uses
`Complete the following fact. Then describe the animal in three sentences.`
Both use the official assistant-prefill template and corrected attention mask.

The original ant continuation begins:

> 6.
>
> The ant is a tiny, hardworking insect known for its incredible ability to carry objects many times its own size.

The original dog continuation begins:

> 4.
>
> The animal is a domestic dog, a loyal companion known for its ability to run, fetch, and sit.

Sources: [ant full demo](out/2026-09-08_042138_wrapper-ant-original-fixed-extraction/conditions/015_future_template_L20_full_C2.0/run.md),
[dog full demo](out/2026-09-08_042159_wrapper-dog-original-fixed-extraction/conditions/015_future_template_L20_full_C2.0/run.md).
All four full outputs, controls, coverage and instruction provenance were inspected
by the main agent and independent reviewer; [audit](slop/audits/2026-09-07_template-clamp.md).
The alternate wording also completes target descriptions without identity reversals.
The ant suppressed readout remains social vocabulary, while dog has dog vocabulary.
These are full-residual edits, not evidence that the suppressed subspace is sufficient.
`hack_s` (reward-hacking count) and `gt_s` (ground-truth pass count) are not defined
or logged for this inference experiment; no such scores are inferred from fluency.

Interpretation, Codex/GPT-6: explanation demand probably contributed to the earlier
reconciliation, because keeping template extraction fixed and changing evaluation
instruction gives relevant target descriptions. This is a reused development pair,
not held-out reliability. Tensor equality across extraction runs is not yet checked.
The next projection sweep tests whether this continuation improvement survives
restriction to the detected persistent subspace; its selected basis still depends
on the evaluation prompts.

The coherent baseline makes the unresolved subspace and readout tests easier to interpret.

<!-- Written by Codex/GPT-6. -->

## 2026-09-07 -- Attenuation-selected steering transfers, but ant identity calibration shifts

The restricted intervention gives coherent animal descriptions while its readout remains unvalidated.

The fixed method selects four raw-residual directions whose paired template contrast loses squared magnitude from layer 25 to 32. It fits this span on four explicit-name template pairs, then projects the mean difference from all eight pairs into it. At layer 20, strength 2, the projected displacement is scaled to the full difference norm. Steering covers the final three prompt positions and every decode step. This is attenuation of a contrast in fixed coordinates, not yet proof of suppressed semantic information.

Job 651, original ant, reports:

> p_target: 0.9717682600021362
> p_source: 0.010795370675623417

Its full output begins:

> 6.
>
> The ant is a tiny insect known for its remarkable ability to carry objects many times its own weight.

The next sentences describe colonies, pheromones, soil aeration and seed dispersal. [Full ant evidence](out/2026-09-08_045830_clean-identity-ant/conditions/007_template_attenuation_attenuation_matchedTrue_C2.0/run.md).

Job 652, original dog, reports:

> p_target: 0.7863069176673889

Its output begins `4.` and describes a dog, smell, play and commands. [Full dog evidence](out/2026-09-08_045852_clean-identity-dog/conditions/007_template_attenuation_attenuation_matchedTrue_C2.0/run.md). Jobs 653 and 654 keep the configuration fixed on rephrased sources and produce coherent dog and ant descriptions respectively: [dog](out/2026-09-08_050217_attenuation-fresh-dog/run.md), [ant](out/2026-09-08_050237_attenuation-validation-ant/run.md). Adding the clean identity diagnostic leaves original generation tokens and target probabilities exactly unchanged from the prior attenuation runs, checked by JSON equality.

The clean identity diagnostic measures signed distance from the midpoint of explicit-name template centroids, with positive meaning target. All four held-out named-template pairs separate for both animals. These are correlated template pairs, not independent token examples. For the implicit ant task, clean spider scores are `[-0.3352128267288208, 0.3261594772338867, 0.5017805099487305]`: two positions are wrongly target-positive. Matching the extraction instruction still gives `[-0.2423253059387207, 0.31994643807411194, 0.38094115257263184]`. [Instruction-control evidence](out/2026-09-08_050412_identity-instruction-ant/result.json). The instruction difference does not suffice to explain the failure. The independent subspace reviewer found no dimension or ordering bug and confirmed the split, while noting explicit lexical identity is an alternative explanation for named-template separation.

`hack_s` (reward-hacking count) and `gt_s` (ground-truth pass count) are not defined for these inference runs. Coherent descriptions do not establish a valid suppressed readout. The static and transported vocabulary-component decoders also fail clean ant identity; no intervened classifier movement is counted as independent evidence because steering uses the same contrast.

Interpretation, Codex/GPT-6: a reusable animal contrast is probable, given the coherent continuations across rephrasings. Absolute ant identity calibration across explicit names and implicit descriptions is not established. Testing direct animal naming without a leg-count question is the next behavioral discriminator.

Jobs 656 and 657 test direct naming with the same fixed intervention. Ant produces ` **spider**.` and describes eight legs. Dog produces ` **dog**.` but repeats attempted corrections, including `*(Okay, I am stuck in a loop. Let me think clearly.` [Ant naming](out/2026-09-08_050520_attenuation-name-ant/result.json), [dog naming](out/2026-09-08_050543_attenuation-name-dog/result.json). The independent continuation reviewer confirmed both failures. Next we vary intervention depth and prompt coverage while retaining continuous decode steering; this tests whether unedited source context reintroduces the contradiction.

Generation transfer and readout validity remain separate claims.

<!-- Written by Codex/GPT-6. -->

## 2026-09-07 -- Select the steering subspace at the layer where it is applied

Selecting directions locally changed dog naming from a correction loop to a coherent description.

Job 662 compares subspaces selected at L20 or L25, with both interventions applied at L20. Here a subspace is a set of residual-stream directions; the selector chooses four directions where the template contrast loses squared magnitude between the selection layer and L32. Both conditions use Qwen3.5-4B, the same template-averaged dog-minus-spider difference, C=2, the last three prompt positions, and continuous steering through generation. Projected differences are scaled to the same full-difference norm; the residual itself is not renormalized. The paired configs differ only in the selection layer.

The source asks to name the animal that spins webs. The L20-selected condition starts:

>  **dog**.
>
> Description:
> The dog is a domesticated canine that has been raised by humans for thousands of years to serve as a loyal companion, a working partner, and a family member.

It continues with commands, emotions and companionship, then ends normally. The L25-selected condition also names dog, but repeatedly restarts its correction and ends at the token limit with:

> *(Okay, I am stuck in a loop. Let me think clearly.

Both records contain exactly:

```text
"perturbation_norm": 18.939538955688477
```

This is the aggregate norm of the edit across the patched prompt positions, not the residual norm. Sources: [local selection, condition 003](out/2026-09-08_051304_attenuation-local-dog/conditions/003_attenuation_local_peak20_positions3_matchedTrue_C2.0/run.md), [late selection, condition 011](out/2026-09-08_051304_attenuation-local-dog/conditions/011_attenuation_local_peak25_positions3_matchedTrue_C2.0/run.md), and [raw paired records](out/2026-09-08_051304_attenuation-local-dog/result.json). The full continuations, settings and decode coverage are retained there. `hack_s` (reward-hacking count) and `gt_s` (ground-truth pass count) are not defined for this inference experiment; naming the desired animal alone would miss the correction-loop failure.

Interpretation, Codex/GPT-6: I think direction quality, rather than edit magnitude alone, probably explains this paired improvement because the applied norms and other settings match. A plausible mechanism is that directions selected in a later representation are poorly suited to an earlier layer. This does not prove that mechanism, establish the best layer generally, or validate the suppressed readout. The local ant naming tests still produce bee or spider rather than ant; see the [follow-up evidence](slop/audits/2026-09-07_attenuation-naming.md).

My working prior is to select the subspace where it will be applied, then test transfer to other prompts and concepts.

<!-- Written by Codex/GPT-6 at wassname's request. -->

## 2026-09-08 -- Updating donor coordinates preserves ant identity in a selected condition

Updating the donor state during generation changed an inconsistent ant intervention into a consistent ant description.

Job 743 uses Qwen3.5-4B with a raw rank-four contrast-attenuation subspace selected and applied at L24, C=2, the last three prompt positions and every generated token. Contrast attenuation selects directions whose donor-minus-source squared magnitude decreases toward the final layer; it is not the vocabulary rise-and-fall detector. Both conditions replace coordinates in the same selected subspace without norm matching or residual renormalization. The synchronized donor consumes the source-selected generated tokens with its own cache; the frozen donor reuses its final prompt coordinates.

The frozen condition produces:

```text
6.

The animal is a spider, a member of the class Insecta (though technically an arthropod, not an insect). It possesses a unique body structure divided into two main sections: the head and thorax, and the abdomen. Spiders are famous for their ability to produce silk from specialized glands to create nests, traps, or shelter.<|im_end|>
```

The synchronized condition produces:

```text
6.

The animal is an ant, a small insect known for its six legs and distinct body segments. They are incredibly social creatures that live in large colonies and communicate through chemical signals called pheromones. Despite their tiny size, ants are powerful workers capable of carrying objects many times their own weight.<|im_end|>
```

Source: [complete paired ant records](out/2026-09-08_131500_synchronized-attenuation-ant/result.json), conditions 005 and 011. Both use the unchanged spider question and have identical first-token probabilities. The full logs include exact rendered chat inputs and continuous-hook coverage. With the same settings, dog condition 011 starts with `2.` before describing a dog, so the paired dog task still fails: [dog records](out/2026-09-08_131500_synchronized-attenuation-dog/result.json). The suppressed vocabulary readout is not validated. `hack_s` (reward-hacking count) and `gt_s` (ground-truth pass count) are not defined for these inference runs; neither is inferred from the target digit.

Interpretation, Codex/GPT-6: updating donor coordinates probably helps preserve ant identity in this selected configuration, because the fixed-span, fixed-strength pair differs only in how donor states evolve after prefill. This does not establish transfer to other prompts or both animals. Nearby layer and strength tests are queued for both animals with the same grid; the research plan retains readout and held-out checks.

The useful distinction is between changing the first answer and keeping the intended animal throughout the continuation.

<!-- Written by Codex/GPT-6. -->

## 2026-09-08 -- Repair the user-message intervention boundary

The user-message path did not apply the requested instruction or select the actual generation boundary.

The CPU check of the runner and pinned tokenizer printed:

```text
{'animal': 'spider', 'user_end': 20, 'generation_end': 29, 'patched_suffix': [271, 248069, 271]}
{'animal': 'dog', 'user_end': 20, 'generation_end': 29, 'patched_suffix': [271, 248069, 271]}
{'animal': 'ant', 'user_end': 20, 'generation_end': 29, 'patched_suffix': [271, 248069, 271]}
```

Source: [boundary check and exact rendering](docs/slop/audits/2026-09-08_151441_user-message-boundary-check.md). `user_end` is the exclusive end of user text; `generation_end` is the full prompt length. The runner now passes the supplied instruction and extracts and patches at the full prompt end. The shared helper retains its user-text boundary for other callers. The assistant-prefill path is unchanged.

Interpretation, Codex: question placement is a plausible cause of some bad clean controls. The completed [wrapper audit](docs/slop/audits/2026-09-08_150650_question-wrapper-jobs759-764.md) quotes a continuation saying the question was not provided, although it appeared in the assistant prefill. The new boundary check does not establish that moving the question repairs the behavior. This comparison also changes extraction positions, so it is a role-and-boundary repair rather than a wrapper-only test.

The next decision requires clean answers from the repaired path before we judge the intervention.

## 2026-09-09 -- span-correction 912+919 family: identity transfers, bound attributes lag

This entry records the span-correction family (batchwork shared-model-batch branch): the
construction that first transferred animal identity coherently, then exposed that bound
attributes do not follow it. Evidence and interpretation are separated.

Context / Methods. Model Qwen/Qwen3.5-4B rev 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a.
Construct: span_corrected_delta, L20, attenuation detector, continuous steering. In the
U-span the edit is P h' = (1-C) P h + C (mu_target - mu_spider), so C=2 is an affine
reflection of P h about the template delta. Pueue tasks: 912 (naming, dog+ant C0/C2),
919 (legs+property, dog+ant C0/C2/random). Result files (batchwork, each `result.json` holds the rows with `generation.text`,
`first_token`, `bare_answer_mass`, `repeated_bigram_fraction`, and `intervention_record`):
- naming: `[out/2026-09-09_span-corr-dog-C2/result.json](batchwork/out/2026-09-09_span-corr-dog-C2/result.json)`, `[..-ant-C2/result.json](batchwork/out/2026-09-09_span-corr-ant-C2/result.json)`
- legs: `[out/2026-09-09_span-legs-dog-C2/result.json](batchwork/out/2026-09-09_span-legs-dog-C2/result.json)`, `[..-dog-rand/result.json](batchwork/out/2026-09-09_span-legs-dog-rand/result.json)`, `[..-ant-C2/result.json](batchwork/out/2026-09-09_span-legs-ant-C2/result.json)`, `[..-ant-rand/result.json](batchwork/out/2026-09-09_span-legs-ant-rand/result.json)`
- property: `[out/2026-09-09_span-prop-dog-C2/result.json](batchwork/out/2026-09-09_span-prop-dog-C2/result.json)`, `[..-ant-C2/result.json](batchwork/out/2026-09-09_span-prop-ant-C2/result.json)`, plus the `-rand` files.
Words like `first`, `r2`, `answer` below are fields in those files.

Naming (912): both animals named coherently to EOS, no correction loop. C=0 identity held
(steered == Base). Random-control naming applied norms were ~8x larger (208.5 vs 26.8) and
produced garbage, so the random cell is a conservative disruption check there.

Legs (919), C=2:
- ant: first="6", coherent red-ant colony text. Fully correct: identity and digit.
- dog: first="2", but text says "The animal is a dog... Dogs typically have four legs...
  standard number of legs for a dog is four, not two" -- identity moved, digit wrong, and the
  text self-contradicts the leading answer.

Legs (919), random control, the guard datum:
- dog-RAND: first="4", but text says "The animal is known as a spider" -- the digit moved to
  the correct target value while identity stayed spider. Digit movement and identity movement
  are therefore separable; scoring digit-only would have called this random cell a success.
- ant-RAND: first="8", spider text (no transfer).

Property (919), C=2 (spin=True in dog row is a prompt-restatement artifact, not spider
identity):
- dog: first="No", but text says "The animal that spins webs is a dog... Dogs are mammals" --
  named dog, stated mammal, but answered "No" to "is it a mammal". Contradiction.
- ant: first="No", names ant, then loops (r2=0.370): "Unlike ants, the ant is a tiny, black
  insect..." -- named ant, but answered "No" to a yes-antennae question and repeated.

Interpretation (my read, calibrated): the conclusion that the construction transfers animal
identity but not bound attributes is *probable*, not certain, because in property dog the text
states the attribute correctly (mammal) while the leading token is wrong, and in legs dog the
text self-corrects the digit. The most consistent story is that the subspace carries a
name/concept pointer without attribute bindings, so the name follows but the numeric/class
answer token does not; the legs-dog-RAND cell (digit moved, spider kept) shows the two are not
mechanically linked. The alternative read, that the C=2 reflection overshoots attribute
coordinates enough to break them, is also *plausible*; the two are distinguished by whether a
C=1 (P h' = delta, no reflection) cell keeps the digit while losing the identity -- the next
bounded test being considered.

This does not establish cross-question persistence. Reserved evaluation strings were not used.

## 2026-09-10 -- bounded test (926): C-sweep shows digit transfer peaks at C=1, degrades at C=2

This entry records the discriminating C-sweep (pueue 926) on the span-correction family,
run to separate the name-pointer-without-bindings hypothesis from the C=2 reflection
over-shoot hypothesis. The over-shoot hypothesis was supported for the digit; the answer
head on property/mirror questions kept a source binding. Evidence and interpretation are
separated; the isolated worktree path prefix is `batchwork/`.

Context / Methods. Model Qwen/Qwen3.5-4B rev 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a.
Construct span-correction, L20, span-correction-sweep config (C-sweep plus in-span random).
Pueue task 926. C mapping in outdir names: `-C0`=0.0, `-C1`=0.5, `-C2`=1.0, `-C3`=1.5,
`-C4`=2.0. Result files:
`batchwork/out/2026-09-10_csweep-legs-{dog,ant}-C*/result.json`,
`batchwork/out/2026-09-10_csweep-prop-{dog,ant}-C*/result.json`,
`batchwork/out/2026-09-10_inspan-legs-{dog,ant}-C*/result.json`,
`batchwork/out/2026-09-10_mirror-prop-ant-C*/result.json`.
Answer readings are answer-position logits (`p_source`, `p_target`) and `top_tokens`, not
only sampled first tokens.

C-sweep legs (digit attribute; source=8): first token and p_target for the target digit.

| C | dog first | dog p(4) | ant first | ant p(6) |
|---|---|---|---|---|
| 0.0 | 8 | 0.046 | 8 | 0.028 |
| 0.5 | 4 | 0.486 | 8 | 0.393 |
| 1.0 | 4 | 0.990 | 6 | 0.963 |
| 1.5 | 4 | 0.969 | 6 | 0.982 |
| 2.0 | 2 | 0.491 | 6 | 0.712 |

In-span random control (randn projected into U then norm-matched to delta): dog C=1.0
first=`4` p_tgt=0.960 but text says "the animal is a domestic cat" (not dog); dog C=2.0
first=`4`; ant C=1.0 first=`8` p_src=0.873 (spider, no transfer); ant C=2.0 first=`8`
p_src=0.732.

Mirror property (eight-legs; source spider=Yes, target ant=No): C=2.0 first=` Yes`
p_src=0.003, text "the ant ... possesses eight legs". Answer head returned source-correct
`Yes`, not target `No`.

Property Yes/No logits: p_source and p_target are ~0.000 for every property cell, so the
Yes/No answer-position logits are degenerate; sampled first token is unreliable there.

Interpretation (my read, calibrated): the C-sweep shows digit transfer peaks at C=1.0-1.5
and degrades at C=2.0, so I think the C=2 reflection over-shoots the digit coordinate,
which is *probable* (maybe 0.8) given the clean peak-then-degrade curve and the reproduced
`2` at C=2.0. The property/mirror cells returned source-correct answers at C=2.0, which is
*probable* evidence that the yes/no answer head retains a source (spider) binding even at
C=2. The in-span random control moving dog to `4` but yielding a cat, while ant stays
`8` from random, is strong evidence that the dog digit readout is a generic/promiscuous
effect (4 is the modal animal leg count) rather than a bound dog attribute, *likely* 0.7;
ant is the direction-specific case. So neither offered mechanism is complete: over-shoot
accounts for the digit C=2 degradation, spider-binding accounts for the source-correct
property/mirror answers, and dog digit promiscuity is a separate general-readout effect.

This does not establish cross-question persistence; the reserved evaluation strings were
not used, and the mirror eight-legs prompt is a new development prompt.

## 2026-09-10 -- M2-to-H3 reversal: source-binding is not out-of-span (instrument artifact)

This entry corrects an earlier reading of the property source-binding. The span-correction
subspace (identity/prose contrast, L20 peak / L32 output attenuation, rank 4) was initially
judged to carry the yes/no decision direction only ~3-5%, which was taken as evidence the
decision lives outside the subspace. A separate activation-space probe found that judgment
was a wrong-instrument artifact; the correction and the evidence are recorded here.

Context / Methods. Model Qwen/Qwen3.5-4B rev 851bf6e806. Two projection ratios computed on
the real model via `batchwork/scripts/m2_projection.py` (weight-space) and
`batchwork/scripts/answer_position_probe.py` (activation-space). d_answer (weight) =
unembedding(Yes) - unembedding(No). d_act (activation) = mean L20 answer-position (last-1)
residual, target minus spider, averaged over the project templates. U = the span-correction
attenuation span (rank 4).

| target | weight-space d_answer ratio | activation-space d_act ratio |
|---|---|---|
| dog | 0.0326 | 0.8417 |
| ant | 0.0410 | 0.8486 |

Interpretation (my read, calibrated): the earlier near-zero weight-space ratio (0.03-0.04)
was a wrong-instrument artifact, *very probable* (0.85). The activation-space decision
direction (the L20 answer-position residual, target minus spider) is ~84% inside the U-span
for both animals, so the identity-prose subspace DOES carry the answer direction. This
reverses the earlier "decision out-of-span / M2 confirmed" reading. The source-binding is
therefore not that the subspace lacks the answer; it is that the identity-prose delta may not
point along d_act (cos checks being measured) or the answer-position residual is driven
differently. The next discriminator (task 933) measures cos(delta, d_act) and the
displacement of the answer-position residual along d_act under the C-steered patch, for
prop-dog C=1.5 and prop-ant C=1.0 (positive control).

This does not establish cross-question persistence. Reserved evaluation strings were not used.

## 2026-09-10 -- correction: H3 reversal was a circular-dependency artifact; M2 re-confirmed

The preceding H3-to-M2 reversal entry stands on an invalid number. A supervisor audit
caught that d_act in the projection probe was computed from the SAME naming
CONCEPT_TEMPLATES as the prose delta, so d_act == delta_full and the "84% in-span" /
"cos == inspan" equality was a circular artifact. The correct measurement uses d_act from
clean forward passes of the PROPERTY prompts (spider vs target), with delta unchanged.

Context / Methods. Model Qwen/Qwen3.5-4B rev 851bf6e806. Fixed
`batchwork/scripts/answer_position_probe.py` (d_act now from property prompts; a
`circular_check_cos_eq_inspan` flag asserts the two are no longer equal). Corrected
results: dog ref (c=1.5) cos(delta,d_act)=0.0748, d_act_inspan=0.0965,
displacement/d_act_norm=0.1416; ant (c=1.0) cos=0.0317, d_act_inspan=0.0488,
displacement=0.0656.

Interpretation (my read, calibrated): M2 is re-confirmed on valid grounds, *very probable*
(0.85). The yes/no answer direction is near-zero in-span for both animals (~5-10%), the prose
delta does not align with it (cos ~0.03-0.08), and the C-patch displaces the answer residual
toward target by only ~6-14%. The earlier "84% in-span => M2 was an artifact" conclusion is
withdrawn. Notably ant has LOWER in-span/cos/displacement than dog yet transfers, so the tiny
in-span fraction is not what separates ant (flips) from dog (doesn't) - the read-out location
(H5: patch attended-but-unpatched Question/Is positions) or later-layer composition (H2) is
the more likely discriminator.

Reserved evaluation strings were not used.

## 2026-09-10 -- two-site decoupled answer-C sweep (task 937): prop-ant clean transfer, prop-dog numeral near-miss

Context / Methods. Model Qwen/Qwen3.5-4B rev 851bf6e806. Two-site edit: L20 identity-site
span-correction fixed at `strength=1.5`; L26 answer-site patched with the raw answer-direction
`d_act` scaled by a decoupled `answer_patch_strength`. 8 cells (prop-dog + prop-ant x C
{0.05,0.15,0.3,0.6}) queued as pueue task 937 via
`uv run --offline scripts/oat_sweep.py --batch-spec slop/two_site_strength_batch.json` (Success).
Full continuations decoded with the pinned tokenizer from `rows[0].generation.token_ids`.

Evidence (verbatim, from `batchwork/out/2026-09-10_two-site-str-{cell}/result.json`):

| cell | C | first_token | r2 | continuation (to EOS) |
|---|---|---|---|---|
| prop-ant | 0.05 | ` Yes` | 0.031 | `Yes. The ant is a small, social insect that lives in colonies and communicates through chemical signals. It possesses two distinct types of antennae... the queen to the colony.` (66 tok) |
| prop-ant | 0.15 | ` Yes` | 0.027 | `Yes. The ant is a small, social insect known for its ability to communicate through pheromones and its highly developed sense of smell...` (76 tok) |
| prop-ant | 0.3/0.6 | `1` | 0.030/0.029 | `1. 2. 3. The ant is a small, social insect...` |
| prop-dog | 0.05/0.15 | ` No` | 0.014 | `No. The animal that spins webs is a dog, which is a domesticated breed of canine... Dogs are mammals...` |
| prop-dog | 0.3/0.6 | `1` | 0.059/0.065 | `1. Yes, the animal that spins webs is a mammal. 2. It is a domesticated dog... 3. It enjoys playing fetch...` |

Read / interpretation (calibrated): the decision rule asked whether some C rescues coherence for
BOTH animals. **prop-ant C=0.05 and C=0.15 are clean PASSES** (correct `Yes` first token, r2~0.03,
fully coherent ant-identity prose to EOS) - the first clean property transfer in this project, and
new since the prior "no clean property cell" record. **prop-dog has NO clean `Yes`-first-token cell**:
C=0.05/0.15 leave the answer at `No` (self-contradictory with the dog prose), C=0.3/0.6 produce correct
Yes+dog content but with a leading numeral `1` (numbered-list marker), so the strict first-token test
fails. Strictly, the "both animals" condition is NOT met, which by the letter points to the freeze
branch; but the prop-ant clean pass and the prop-dog numeral near-miss are materially new and should
be weighed by the supervisor before freezing. `bare_answer_mass` (p(4)+p(8)) is a legs/arithmetic
metric and is NOT informative for these Yes/No property prompts; r2 is the repetition diagnostic
(<0.2 everywhere).

Reserved evaluation strings were not used (dev property prompts only).

-- PI[Kimi K3] (worker, evidence only; supervisor decision pending)


## 2026-09-11 -- Resume common-subspace research after user clarification

Wassname clarified the intended intervention and reopened the research.

Evidence from this conversation, quoted from wassname:

> subspace A on token 1 and subspace B on token 2, we use union(A,B) for both but for N tokens. Or a soft union for example PCA top 8 or something

> doesn't need to be causal to learn, jsut a table or something can help, or swep

Code inspected: `../suppressed-activations-batchwork/suppressed_activation_subspace.py:160` defines `token_persistent_subspace`. It concatenates orthonormal per-token bases, takes their singular value decomposition, and retains the requested number of supported directions. This combines subspaces, unlike selecting a direction by cosine agreement of projected activation vectors. The recent rank-one activation-pair experiments do not settle the clarified construction.

Interpretation (PI/OpenAI): my earlier summary conflated these constructions and made causal proof too much of a requirement. Descriptive layer/token comparisons can reveal useful differences without establishing their cause. Token-history dependence is also plausible: appending the same generated token to spider and donor prompts does not make their preceding contexts or hidden states equal. Feeding an edited spider answer into the donor can itself change the donor state.

Action: resumed the existing worker session for the new common-subspace goal, with prior-result recovery, full-union versus truncated-basis interventions, and layer/token tables through the existing runner. No new experimental result is claimed in this entry. The old evaluation remains historical evidence and is now exposed for further development. See `.pi/plan/01a089da-912f-70d6-b080-547acdbb4dd9-main.md`, the new common-subspace goal, and `slop/audits/2026-09-10_supervisor-final-review.md` for the previous bounded outcome.

The next comparison must test the intended shared basis rather than reject it using a different construction.

-- PI/OpenAI

## 2026-09-11 — Task 938: final narrow two-site calibration -> freeze branch (PI[Kimi K3])

Evidence (out/2026-09-10_twosite-narrow-*/result.json, batchwork commit c04fc06; code+spec 2bf8a16):
- prop-ant C=0.2: first `' Yes'`, coherent ant prose 88 tok, r2=0.070. C=0.25: `' Yes'`, 66 tok to EOS, r2=0.047. With 937 (C=0.05/0.15): prop-ant 4/4 clean passes across 0.05-0.25.
- prop-dog C=0.2: first `'1'`, prose "No, … is not a mammal; it is a domesticated dog" — answer stuck at source. C=0.25: first `'1'`, top-2 tie ` Yes`/`1` (0.2151), prose still "No". No clean Yes-first pass at any C in {0.05,0.15,0.2,0.25,0.3,0.6,1.5}.
- r2 recording: no -1 placeholder in any 937/938 result.json; `repeated_bigram_fraction` populated. Only -1s are seed sentinels. Real quirk: `bare_answer_mass` rendered under "p(Yes)+p(No)" header — label issue only.

Interpretation: no single C passes both animals -> supervisor decision rule says FREEZE branch. Two-site rule frozen (L20 span-correction C=1.5 + L26 d_act; property at prop-ant C=0.15). prop-dog property = partial/non-transferring: probability mass moves toward ` Yes` (tie at C=0.25) but the model never commits to Yes-first coherent prose. Next: reserved-string evaluation + notebook finalization with property labelled partial.


## 2026-09-29 -- Language-agnostic selector search: 92/120 isolate the hidden English word

Pueue 2437, [`out/2026-09-29_115749_selector-search/run.md`](out/2026-09-29_115749_selector-search/run.md). Qwen3.5-4B, 120 Wendler de->zh 4-shot prompts, last token.
Pass = best English-answer token rank < 32, best Chinese and German ranks >= 32. 42 selectors
(layer triples, per-token peak over 24-30, prompt-word exclusion); chosen on even prompts, reported on odd.

| selector | even (select) | odd (report) | overall |
|---|---:|---:|---:|
| peak_any e22 p24-30, minus prompt words | 46/60 | 46/60 | 92/120 |
| rise_fall 22/27/32 (repo) | 30/60 | 26/60 | 56/120 |

Winner: English is the top-1 token in 61/120 prompts, top-5 in 89/120; fixed 45 and broke 9 of the repo
method's prompts. Of 28 failures, 8 are German/English identical spellings masked by the prompt-word rule
(hand, sand, ball, gold, version, talent, generation, person); others are low English rank (lake, pond, spring).

Interpretation (Claudypoo[opus-4.8]): most of the gain is removing input words, a rule that uses only the
prompt text. In an all-English setting it will also remove a hidden word that appears in the prompt, so it
finds "thought, not read, not said". Next test: the frozen winner on English two-hop prompts.

## 2026-09-29 -- Frozen selector transfers to unseen language pairs; embedding erasure does not remove input words

Pueue 2446, [`out/2026-09-29_132506_erase-language-pairs/run.md`](out/2026-09-29_132506_erase-language-pairs/run.md). Pairs with no English or Chinese at either end (Qwen trains mostly
on en+zh). Hidden = English or Chinese answer word; pass = hidden rank < 32, input and output ranks >= 32.
Dev de->fr, test fr->ru, ru->fr, de->ru, ru->de, fr->de, fixed before the run. de->zh is reference only.

| selector | de->fr (dev) | fr->ru | ru->fr | de->ru | ru->de | fr->de |
|---|---:|---:|---:|---:|---:|---:|
| 03 winner (peak_any, prompt words removed), frozen from de->zh | 64/76 | 64/78 | 71/78 | 67/88 | 75/88 | 64/76 |
| rise_fall 22/27/32 (repo) | 44/76 | 43/78 | 45/78 | 48/88 | 55/88 | 37/76 |
| peak_any, input embeddings erased | 39/76 | 52/78 | 46/78 | 52/88 | 52/88 | 37/76 |
| plain logit lens L27 | 14/76 | 11/78 | 9/78 | 15/88 | 10/88 | 14/76 |

- Latent language: English peaks at p 0.49-0.59 (L27-28); Chinese 0.09-0.13; input <= 0.04.
- Counting Chinese as hidden adds at most 2 passes per pair (English-only table in run.md).
- Winner failures are now mostly the output word inside the top 32 (6-15 per pair); input errors are 0.
- Erasure of the prompt's layer-0 embeddings leaves the input word (29-31 of 76 on dev). CPU check: after a
  quote mark the prompt tokenizes "Herz" as 'Her'+'z', while the selected token is ' Herz'; embedding cosine
  between them is -0.05 to 0.35, so erasing the pieces barely touches the whole-word direction.
- A first run erased g*W_t instead of W_t (bug; logit_t = u.W_t); fixed, results above are from the fixed run.

Interpretation (Claudypoo[opus-4.8]): the regex rule works because it matches whole words across tokenizations;
a token-embedding erase would need the word-level direction, which is assembled after layer 0.

## 2026-09-29 -- Removing read and said words: 95% on unseen language pairs

Pueue 2455, [`out/2026-09-29_132506_erase-language-pairs/run.md`](out/2026-09-29_132506_erase-language-pairs/run.md).
"Said" = the model's own greedy answer up to the closing quote; its words are removed like prompt words.

| selector | de->fr (dev) | 5 test pairs |
|---|---:|---:|
| peak_any, prompt and said words removed (dev winner) | 74/76 | 386/408 |
| peak lens L27, prompt and said words removed | 72/76 | 386/408 |
| peak_any, prompt words removed (03 winner) | 64/76 | 341/408 |
| peak_any, prompt words erased (re-tokenized first tokens) | 60/76 | 328/408 |
| rise_fall 22/27/32 (repo) | 44/76 | 228/408 |

- Said text is the correct translation in 86-92% of prompts and never the English word, so removal
  does not pass by deleting an English answer.
- Output-word leaks drop to 0-1 per pair for the dev winner; the remaining failures are hidden-word misses.
- With both removals the plain lens puts the hidden word at rank 1 in 61/76 dev prompts vs 52/76 for peak_any.

Interpretation (Claudypoo[opus-4.8]): in translation, "thought" is close to "top logit-lens words minus
read minus said"; rise-and-fall adds little once both removals exist. This may be too easy a setting:
the English-only two-hop test is where a hidden word could also appear in the prompt or answer.

## 2026-09-30 -- Same-pass editing is not yet reliable concept replacement

The selected spider edit changes the answer, but the reverse dog edit does not.

Evidence, from the J-lens swap rows in each run.md:

| input and edit | swap_log_odds_shift | p4 | p8 | source |
|---|---:|---:|---:|---|
| spider, early edit and later observation | 3.25 | 0.565529 | 0.343011 | [2531](out/2026-09-30_083832_jlens-one-pass/run.md) |
| dog, same edit | -0.125 | 0.946402 | 0.00818798 | [2533](out/2026-09-30_084536_jlens-one-pass/run.md) |
| dog, all prompt positions | -0.125 | 0.949041 | 0.00821081 | [2536](out/2026-09-30_084850_jlens-one-pass/run.md) |

`swap_log_odds_shift` is the change in log odds favouring 4 over 8, in nats. A negative value is desired on the reverse dog input. These are selected development inputs, not a fixed-set generalisation estimate. Each condition generates 32 tokens with continuous steering. The edit uses residual 16, and the later readout uses residual 24 without feeding back into the edit. Plain and matched-random controls retain the base answer. Source and full checks: [audit](slop/audits/2026-09-30_status.md), code commit `f1a9786`.

The later spider readout after editing begins `claws, spiders, paw`, not dog. Reverse editing still starts with 4 and only changes the later proposed hypothesis. `hack_s` (reward-hacking count) and `gt_s` (general capability pass count) were not measured; this pilot has no such benchmark. The exact continuations remain in the source reports.

Interpretation (PI/OpenAI): partial animal-feature movement is plausible; a clean identity replacement is not established. The reverse test makes a generic leg-count bias more plausible, but does not identify the cause. Offline output forecasting is now being tested for the separate readout goal, with a final-layer oracle used only to check the subtraction rule, not as an admissible method.

Both readout generalisation and reliable concept replacement remain open.

## 2026-09-30 -- Donor steering and output-alias leakage

The donor method changes the reverse answer, while a readout audit weakens the apparent English result.

Evidence from the selected reverse donor experiment:

| condition                        |   swap_log_odds_shift |        p4 |         p8 |   bare_answer_mass |        r2 |
|:---------------------------------|----------------------:|----------:|-----------:|-------------------:|----------:|
| Base                             |                 0     | 0.943579  | 0.00720431 |           0.950783 | 0.0322581 |
| J-projected donor contrast       |                -5.25  | 0.0983349 | 0.143076   |           0.241411 | 0.0322581 |
| full donor contrast              |                -9.25  | 0.0115834 | 0.920186   |           0.931769 | 0         |
| norm-matched full donor contrast |                -3.75  | 0.516155  | 0.167571   |           0.683727 | 0.0322581 |
| matched-random delta             |                 0.375 | 0.935038  | 0.00490663 |           0.939945 | 0         |

Source: [2575 complete log](out/2026-09-30_105749_jlens-one-pass/console.log), source commit179b65b. Negative shift favours8 over4; answer mass is p4+p8; r2 is repeated-bigram fraction. Full contrast starts8 with a spider/web readout; J projection starts6, despite its negative shift. Full contrast changes about65% of prefill residual norm, whereas the random comparison changes32%. Four generic templates per animal supply reusable donor means; no question, answer label or preparatory pass over the experimental input is used. Independent formula and coverage checks pass. General capability and reward-hacking counts were not measured.

The fixed English replay reports:

```text
| [end-pass J-lens](readout.json)  | 10/16                  |    0.833 | 8/11                     | 11/16            |          0 |
| [end-pass plain27](readout.json) | 6/16                   |    0.842 | 5/11                     | 7/16             |          0 |
```

Columns are declared-alias joint pass, token-pair AUROC, pass among expected-answer matches, literal joint pass and unscored count. Source: [2577 complete log](out/2026-09-30_110305_jlens-one-pass/console.log). All80 rows reproduce the earlier generations and rankings. Manual inspection then finds Berlin/柏林, Vienna/维也纳, Bangkok/曼谷 and kitten/小猫 leaks in J passes. The fresh reviewer also finds Athens/雅典 in plain27. These scores therefore do not measure exhaustive semantic output exclusion; remaining multilingual and word-fragment cases are unverified. [Review](slop/reviews/2026-09-30_donor-readout-review.md).

The same frozen readout ties masked plain24 at33/40 on the translation test, versus28/40 for plain27; see [2570](out/2026-09-30_104102_jlens-one-pass/console.log). Translation roles deliberately distinguish language forms of one meaning. Removing all semantic synonyms would remove its intended English intermediate too.

Interpretation (PI/OpenAI): I consider distributed animal-feature transfer plausible, but the unequal control magnitude and single relation leave identity replacement unresolved. Lexical readout recovery is real under the declared scoring rule; its stronger semantic interpretation is contradicted by the retained answer translations. Neither is goal completion.

Queued tests2579/2580/2581 compare donor/full-norm projected/random edits, hold the donor fixed on skeleton placement, and reverse its direction. Test2584 instead removes the predicted output-token component in normalised readout space, with unchanged lexical-mask controls and disclosed posthoc alias annotations. This is a method change, not another held-out evaluation. An article or word fragment can be the selected output token, so the run logs that token and the realised post-cast score. All use the shared default GPU queue without reordering other work.

The next evidence must improve the method, not merely complete another diagnostic.

## 2026-09-30 -- Frozen English comparison; property transfer still missing

PI/OpenAI. The frozen half-erasure J readout retains a lexical advantage on16 new targets:

```text
| [end-pass erased0.5 J-lens](readout.json)  | 10/16                  |    0.915 | 8/13                     | 10/16            |          1 |
| [end-pass erased0.5 plain27](readout.json) | 4/16                   |    0.889 | 3/13                     | 6/16             |          1 |
```

Source: [2590](out/2026-09-30_125330_jlens-one-pass/console.log). Columns are declared-alias joint pass, AUROC, expected-answer subset, literal pass, unscored. Strength0.5 was selected from0/0.5/1 on v2 before freezing v3; all16 remain in the denominator, including unscorable numeric10. Mask-only J passes11/16, so erasure is not shown necessary. `oceans` surviving input `ocean` demonstrates incomplete input exclusion; these are lexical scores, not a semantic guarantee. On the previously used translation test the same method ties half plain24 at33/40, versus31/40 half plain27; [2591](out/2026-09-30_125500_jlens-one-pass/run.md). Repeated concepts are not independent cases.

Readout states now come from the scoring generation's prefill.128 older English rows and240 older translation rows reproduce their generations/rankings exactly; this is not bitwise hidden-tensor parity. [Blind development review](slop/reviews/2026-09-30_half-erasure-blind-review.md) found no definite answer leak among half-J's11 v2 passes, but retained ambiguous young-animal words and missed fragments/translations. Same model family; no independent semantic success-rate certification.

Selected causal progress does not survive the next checks. At final-position-only prefill, full noun donor changes spider8→4 and continues `The animal that spins webs is a dog.` ([2592](out/2026-09-30_125606_jlens-one-pass/run.md)). Reverse remains4; body-property edits remain outside/inside instead of exchanging them ([2600](out/2026-09-30_132742_jlens-one-pass/run.md), [2598](out/2026-09-30_131556_jlens-one-pass/run.md)). Both clean property answers are correct. Last-three-position edits can flip both leg answers but damage text; a single changed digit is insufficient.

Same-token donors use the original four generic templates plus `. It`, eight inputs with identical paired final token1049. Their natural contrast norm is1.430336; testing at the old6.901978 norm isolates direction from size, not an unscaled replacement. Forward full contrast generates4 but repeats questions, r2=.354839 versus Base.032258. Reverse projected contrast generates8 with p8=.642038 versus random.007853, yet produces the malformed `How many legs does the spider that lives in the web of the spider's home is there?` Full contrast still gives4. [2603 forward](out/2026-09-30_133833_jlens-one-pass/run.md), [reverse](out/2026-09-30_133853_jlens-one-pass/run.md). Base/random controls reproduce the old donor outputs and scores exactly. These are selected development conditions, not a fixed-set success rate. General-capability and reward-hacking counts remain unmeasured.

[Reference review](slop/reviews/2026-09-30_reference-intervention-comparison.md) confirms readout orientation/indexing and admissible offline timing, but distinguishes fixed addition from the paper's coordinate swap and two-token projection from its sparse J-space decomposition. The causal paper results are on Anthropic models; the released Qwen lens is not proof of Qwen causal replication. It identifies large asymmetric injection during every decode step as a plausible cause, not an established diagnosis.2611 now changes only decode scale to0 on the reverse pronoun case, an explicitly labelled prompt-only diagnostic. First-token scores must reproduce and decode deltas must be zero; improved grammar would motivate a bounded continuous update rather than repeated fixed addition. This control alone cannot complete the continuous-intervention goal.

Runtime note:2596/2597 timed out before any condition completed; shared-import retry2600 succeeded.2598 timed out after all scientific artifacts persisted, so its result was checked rather than rerun. Current tokenizer `all_special_ids` omits backend-special im_start; r2 now excludes all backend-special IDs too (old affected row .033333→.034483, no generation change). Generation still uses the pinned model EOS248044, not tokenizer chat-end248046; this policy is recorded, not silently changed.

Full per-job evidence and hypotheses: [audit](slop/audits/2026-09-30_status.md). Both goals remain open. README remains an unpublished editorial draft.


## 2026-09-30 — Semantic audit narrows readout; answer changes still do not transfer

— PI/OpenAI

Observed: blinded v3 annotation (all48 rows/1536 entries) gives half-J7/16, half-plain24 2/16, half-plain27 0/16 for hidden recovery with no observed definite input/answer leak. All seven J passes are geography. The posthoc full-English-alias wrong-country control gives7/8 correct memberships versus10/56 wrong assignments, not56 independent prompts. Sources: `slop/reviews/2026-09-30_v3-semantic-review.md`, `out/2026-09-30_125330_jlens-one-pass/geography_wrong_label_control.json`.

Observed: eight non-geography cases were committed at1c72344 before2615. The unchanged half-J method is3/8 lexically, AUROC.856807, versus plain27 6/8,.898877 and plain24 1/8,.813996. Seven baselines match frozen answers; violin says “the woodwind family.” These are not semantic success counts: e.g. plain27 apple still shows `poisoning`, `白雪`, `:red`. Root `out/2026-09-30_142814_jlens-one-pass/`; full31-line log and source4fc70e4 verified. This weakens any general J-lens advantage.

Observed: reverse pronoun-donor quarter decode2612 keeps p8=.642038 and a grammatical NLI continuation; initial probabilities exactly match full-decode133853. Its later hypothetical4 is not an initial-answer reversal. On skeleton2614, the same projected edit reads `spider` but still answersinside (poutside.199712 vsBase.225063). Full donor answersoutside (.240546) but keepslegs4. Thus neither intervention succeeds on both properties. Directories142712 and142748 contain all4×32-token conditions and coverage, odds/mass/r2 verification. Prompt-only2611 at140958 was a diagnostic, not continuous success.

Observed: coordinate swaps at intermediate residual20 (2619;150940/150958, source9cba28e) exchange the local coordinates but retain8 and4. J forward shift+1.375, reverse0. Local J readout remains punctuation; plain controls have different magnitudes. Eight32-token conditions, all3-position prefill/31 decode calls and metrics checked. The later NLI hypothesis8 in the reverse run is not a successful initial answer.

Observed:2621 rescored v4 saved prefill states at24c6faf, with a hook forbidding transformer forwards. All fields of88 old rows replay exactly. Signed logit contrast is0/8 for J24/plain24/plain27; negative-final control also0/8; cyclic mismatched-final J is2/8. Probability contrast J remains4/8, plain27 5/8. Lists contain topic words (`Months`, `Days`) and fragments. Source `out/2026-09-30_151032_jlens-one-pass/`; component logits/log-probabilities and cutoff ties saved. Same-family review `slop/reviews/2026-09-30_logit-contrast-design.md` predicted denominator-driven artifacts; this is development, not holdout evidence.

Interpretation/next: grammar was partly damaged by repeated constant additions, but grammatical changed digits are insufficient. Pause reranker expansion while advisor dialogue chooses a bounded causal change: locally conditional donor-coordinate reflection, with clean source/target signed-margin diagnostics. Generic donor-centre domain mismatch is an explicit possible failure, not something to fix by tuning against these prompts. README remains an unapproved draft; both goals remain open.

## 2026-09-30 — Generic donor midpoint fails the clean-question sign test

— PI/OpenAI

Job2625 completed94s, source86445f1. At residual16/final position, clean dog/spider margins are1.081535/1.153284 for legs and1.194581/1.415897 for skeleton. Both species lie on the side designated spider, so conditional reflection applies zero before each initial answer. Outputs remain4/inside and exactly match Base generations. Later8/7 reflection calls do update, with fold/coverage/precision checks passing. Natural addition still answers4 on legs andoutside on skeleton; its skeleton continuation explicitly saysdog. No same-method concept transfer.

Interpretation: the stored generic midpoint is not a valid source/target boundary for these last-position question states. Positive target-minus-source ordering survives, so this does not establish that the direction is useless. No threshold or dose will be fitted against these four prompts. Raw layer16 tensors were not saved; numerical auditing uses the frozen source and recorded margins/deltas.

Evidence: `out/2026-09-30_155111_jlens-one-pass/`, `out/2026-09-30_155140_jlens-one-pass/`; complete37-line log, source, job metadata and verification saved. Detailed audit: `slop/audits/2026-09-30_job2625.md`. Fresh advisor workflow timed out awaiting a reply; its partial recommendation is not a completed review. The same-role fallback completed and specified one small generic validation. Both goals remain open; README unchanged in this step.

## 2026-09-30 — Direct embedding subtraction leaves context-dependent coordinate offsets

— PI/OpenAI

Job2627, sourceefd41dc, completed30s with16 generic prefills and no generations. Raw and corrected coordinates each separate2/8 dog/spider pairs at zero, both endingin ` It`; all8 have the expected within-pair ordering. Direct-embedding subtraction shifts other endings by at most about.015 without fixing any sign. Sources: `out/2026-09-30_163330_jlens-one-pass/{run.md,samples.jsonl,states.pt,verification.json}`. Full66-line console read; float64 reconstruction of every saved coordinate differs by at most1.53e-6.

A posthoc bound shows no single cutoff can fix these16 observations along this axis: corrected maxdog1.230348>minspider.039979. Pooled AUROC=.6875, not64 independent comparisons. The eight generic pairs now become development data. No causal test of this correction will run.

Fresh reviewerda59a1aa found no apparent arithmetic/sign bug and warns that the current intervention hook still uses the raw coordinate; validation of a formula alone never installs it in editing. Advisor487d6e80 and parent approved one new candidate: remove the seven-dimensional span of centered generic pair means from the old donor direction, center on their mean, validate on8 new generic pairs, and only on8/8 separation test both causal properties within one300s job. Training midpoint invariance is algebraic, not validation. Exact contract: `slop/reviews/2026-09-30_context-invariant-coordinate-decision.md`. Not implemented or run yet; both goals remain open.

## 2026-09-30 -- Context projection fails the new generic contexts

The fitted coordinate did not transfer to the new generic sentences.

Job2628 ran source4348227. The log reports:

> Candidate brackets: 2/8; raw: 0/8; candidate ordered: 7/8. Required:8/8 candidate brackets.

Here bracketing means dog margin below zero and spider margin above zero. Source: `out/2026-09-30_172257_jlens-one-pass/run.md:299`. The strict prerequisite stopped all causal generations. Independent least-squares reconstruction and retokenization passed; maximum margin error was1.06e-6. For the field/explicit/description pair, the projection removed a positive class-gap component of.203491, leaving -.038110 before unit normalization, reversing the raw ordering. Source: the same run's `verification.json`. These are dependent context pairs, not independent concepts.

Interpretation: my read is that this frozen projection overfits the generic contexts and can remove useful class discrimination. The saved-state calculation makes an arithmetic explanation unlikely, but it does not establish that the removed part is a general semantic feature. Training midpoint cancellation was constructed; high retained direction norm did not protect this pair's ordering. Neither hack_s (reward-hacking count) nor gt_s (ground-truth task passes) was measured: this prerequisite had no causal or task-scoring stage.

Next: one positive token-KL contribution readout on cached English examples, with matched plain-lens and mismatched-final controls, rather than another cutoff adjustment. Exact prospective contract: `slop/reviews/2026-09-30_after-projection-next-test.md`. No new inference queued at this entry. Audit: `slop/audits/2026-09-30_job2628.md`.

-- PI/OpenAI

Both research goals remain open.

## 2026-09-30 -- Probability weighting did not improve hidden-word recovery

The readout still confuses hidden concepts with words it will say.

Job2630, source091de02, reused the eight v4 development states and generations. Its fixed selection result says:

```json
"matched_counts": {"plain27": 5, "J-lens": 4, "plain24": 0},
"selected_representation": "plain27",
"selected_mismatched_count": 5,
"n": 8,
"numeric_screen_passed": false
```

Source: `out/2026-09-30_175925_jlens-one-pass/token_kl_selection.json`. Joint recovery here means a hidden alias is present while actual-output words and declared answer aliases are absent. It is not semantic accuracy. The incumbent half-erased plain27 remains6/8. Independent checking reproduced168 old rows and48 new component/scoring records. All eight J candidate lists have0/32 tokens with intermediate probability below1e-5; signed contrast previously had29/32 on Hamlet. These counts come from the run's `verification.json` and2621's audit. No fitting or new model forwards occurred. Neither hack_s nor gt_s is defined for this readout-only test.

Interpretation: my read is that probability weighting corrected the rare-token diagnostic but not the research failure. Matching the wrong final distribution gives the same pass vectors for J and plain27. Fresh review also finds January represented by `Januari`, winter by `vinter`, and emitted `wind` surviving inside a counted violin pass. Thus lexical counts overstate exclusion, not merely understate recovery. A plausible next cause is that the bridge appears at an earlier question position, while the final position mostly represents the answer.

Next: one question-span pooling test with the same probability-excess score and final-last comparator, equally pooled plain controls, and a strict generated-ID/last-state replay check. No parameter sweep. Audit: `slop/audits/2026-09-30_job2630.md`; approved contract: `slop/reviews/2026-09-30_after-token-kl-next-test.md`.

-- PI/OpenAI

Both research goals remain open.

## 2026-09-30 -- Pooling adds generic priors instead of improving joint recovery

Question-position pooling did not improve the readout.

Job2637, sourcea53ba01, reports:

```json
"pooled_counts": {"plain27": 4, "J-lens": 3, "plain24": 0},
"selected_representation": "plain27",
"selected_last_count": 5,
"selected_mismatched_count": 4,
"selected_unsubtracted_count": 4,
"n": 8,
"numeric_screen_passed": false
```

Source: `out/2026-09-30_185058_jlens-one-pass/pool_selection.json`. All8 generations/64tokens and last states match the old baseline exactly;168 old rows and96 new component/scorer records reconstruct in that run's `verification.json`. This is still development. Neither hack_s nor gt_s is measured in this readout-only test.

The peak record for J's population token gives `"p_peak": 0.678586483001709`, `"position": 12`, `"input_piece": " The"`: only the common prefix and `Fact: The` have been consumed. The December peak occurs after `month immediately after`, before Christmas. These are normalized lens scores, not calibrated probabilities of thoughts. Fresh review6df6e4ed finds an input leak in every selected plain27 lexical pass, including capitals from the demonstration's capital and leaf from leaves. It also explains that pooling can increase every token's score yet worsen a hidden token's rank by increasing competitors more.

Interpretation: my read is that maximum pooling rewards generic priors as well as clue-dependent information. This is not a span-boundary error: the saved offsets independently retokenize correctly. It also does not prove the model lacks the bridge; hydrogen peaks after element but is crowded out. The frozen pooled method is rejected without selecting a narrower window.

Next: one cached final-position test of J's orthogonal polar factor, with original-J/plain controls and a fixed early-prefix comparison, rather than another pooling score. This removes unequal singular-value gains, not noise or semantic errors by assumption. Exact contract: `slop/reviews/2026-09-30_after-pooling-next-test.md`; audit: `slop/audits/2026-09-30_job2637.md`. No next code or run at this entry.

-- PI/OpenAI

Both research goals remain open.

## 2026-09-30 -- Polar transport fails the development screen

Removing the lens's unequal gains did not improve the fixed readout.

Job2642/source0ae6378, `out/2026-09-30_205519_jlens-one-pass/polar_selection.json`:

```json
 "counts": {
  "Q excess": 1,
  "original-J excess": 4,
  "plain24 excess": 1,
  "plain27 excess": 5,
  "mismatched excess": 1,
  "unsubtracted": 1,
  "early-prefix excess": 0
 },
 "n": 8,
 "exact_prior_rows": 168,
 "incumbent_half_plain27": 6,
```

Counts are lexical hidden-alias recovery with actual/declared answer exclusion, not semantic certification. Q is the orthogonal polar factor of J, with positive probability excess against the final next-token distribution. Its sole pass is Thursday. Saved full-vocabulary scores, masks and ranking reconstruct; independent CPU singular-value decomposition agrees with Q to maximum absolute error1.86e-9 (`verification.json`). No new inference was performed. Neither hack_s nor gt_s is measured by this readout test.

Interpretation: my read is that removing unequal gains probably exposes unhelpful directions or discards useful weighting: most Q lists are formatting and multilingual fragments. This is not isolated causally. The violin list still contains the broader Chinese term 提琴; missing English aliases cannot establish missing semantic information. High AUROC against spoken-word variants is also insufficient: triangle scores.99858 unsubtracted yet misses the hidden label in top32. Fresh review27e293e9 supports the negative result while disclosing incomplete source coverage.

Next is one raw-coordinate Italy-to-Japan intervention across capital and currency questions, not another Q adjustment. The same rule must work on both; wrong baselines remain invalid cases, not replaceable prompts. Reserved output-matched readout examples stay unrun. Audit and exact contract: `slop/audits/2026-09-30_job2642.md`, `slop/reviews/2026-09-30_after-polar-next-test.md`.

-- PI/OpenAI

Both research goals remain open.


## 2026-09-30 -- Country coordinates change while answers remain unchanged

The fixed country intervention did not change either initial answer.

From `out/2026-10-01_001654_country-swap/pipeline.json`:

```json
"base_initial_text": " Rome.",
"primary_initial_text": " Rome.",
"primary_exceeds_random_bare_log_odds": true
```

```json
"base_initial_text": " the Euro.",
"primary_initial_text": " the Euro.",
"primary_exceeds_random_bare_log_odds": true
```

Both source answers are correct. Every condition retains exactly its Base's32 generated IDs (`compact_conditions.json`). Primary target recovery is0/2 properties of one selected country pair. The primary bare-answer log-odds shifts are+0.0625/+0.25 nats versus random-0.0625/0. Currency begins with an article and capitalized Euro, so lowercase bare-token probabilities do not score the emitted answer directly. NLI hypotheses are propositions under consideration, not independently endorsed beliefs. Neither `hack_s` nor `gt_s` is a defined metric in this inference-only assay; no training occurred.

Independent saved-tensor reconstruction reports `"max_requested_state_error": 2.8172245652990924e-07` in master `verification.json`. Requested updates, BF16 casts, bases, pinned parameters, token decoding, coverage and scalar metrics reconstruct; full model probabilities and semantics are not independently reproduced. Task2648 took52.460s; follower9005s includes queue wait. The two property roots are001715 and001732 on2026-10-01 local time. Full audit: `slop/audits/2026-10-01_job2648.md`.

Interpretation: my read is that these two coordinates are probably insufficient to change the country here, or later computation restores source information. A missing hook or erased update is less likely after tensor reconstruction. This does not reject all country editing or show that the country is absent internally.

Next is one cached nonnegative matching-pursuit readout: subtract each explained token-direction component before choosing the next. Equal-cardinality controls separate this from merely returning fewer words; fixed pre-clue states test temporal clue association. The prospective contract is `slop/reviews/2026-10-01_after-country-next-test.md`; nothing new is queued yet. Earlier failed gates remain closed, and existing partial geography evidence keeps its stated limitations.

-- PI/OpenAI

Both research goals remain open.

## 2026-10-01: matching pursuit adds no hidden-concept recovery

Task2657 finished47.657s after two allocation failures and one startup timeout; those earlier attempts produced no scores. The completed run's `out/2026-10-01_032642_jlens-one-pass/pursuit_selection.json` reports:

```json
"primary_count": 3,
"cardinality_matched_unit_dot_count": 4,
"paired_gains": [],
"paired_losses": [0],
"net_paired_gain": -1
```

These are frozen alias joint counts on eight reused v4 cases, not semantic accuracy. Matching pursuit loses December; plain24/plain27 pursuit score0/8 and2/8 versus their matched unit-dot controls3/8 and5/8. All168 old rows reproduce. Independent CPU reconstruction covers40 selected-direction traces and120 new rows, with maximum residual difference7.38e-6; it does not reconstruct every greedy competitor.

All three counted J passes have identifiable leaks: Thursday also returns Russian day (`День`); violin returns Arabic family (`عائلة`); triangle returns Dutch three (`drie`). These annotations do not alter the frozen counts. Violin already appears before its identifying clue, and its cached answer is incorrectly woodwind. Fresh same-family review agrees the advancement condition fails. Complete examples, priors and controls: the run's `case_comparison.md`. Audit: `slop/audits/2026-10-01_job2657.md`.

The first December allocation is January, followed by Months. My interpretation is that fixed earlier coefficients may remove useful correlated directions, but the evidence does not establish that mechanism. The next single test allows active coefficients to decrease as well as increase: explicitly specified nonnegative gradient pursuit, not a claimed reproduction of unpublished solver code. Better reconstruction alone will not qualify; it must improve paired semantic recovery and add a clue-associated recovery. The matching-pursuit configuration is retired, v5 is unrun, and both goals remain open.

-- PI/OpenAI

## 2026-09-30 UTC -- Revising coefficients does not add a joint recovery

The revised decomposition fits activations better without finding another hidden concept cleanly.

Job2668, `out/2026-10-01_045248_jlens-one-pass/gradient_pursuit_selection.json`:

```json
"primary_count": 3,
"cardinality_matched_unit_dot_count": 4,
"paired_gains": [],
"paired_losses": [0],
"net_paired_gain": -1,
"new_vs_native_matching_pursuit": []
```

These count frozen lexical joint passes across eight cached development prompts. The comparator uses the same J dictionary with direct unit-dot scores. `fit_comparison.json` records `"mean_remaining_energy_gp": 0.8774855734542512` versus `"mean_remaining_energy_mp": 0.8976442322274167`; smaller means less unexplained squared activation norm. The independent checker confirms1173 updates with decreasing coefficients across40 decompositions and288 exact old rows, within its stated selected-support scope. The model was not trained and no new continuations were generated. Seven cached answers match intended aliases; violin incorrectly answers woodwind and remains in the denominator.

My interpretation is that reconstruction alone probably misses the required distinction between hidden content and speech. Persistent examples include Apfel alongside red, and triangle alongside Dutch three. The changed violin list drops an old family leak, but violin already appears before its clue; no new recovery follows. This rejects the specified solver and budget, not all sparse methods. Full evidence and competing explanations: `slop/audits/2026-10-01_job2668.md`.

Next is a small transfer test of the earlier frozen half-erasure rule, whose reviewed successes were restricted to geography. It will use native chat and different countries sharing a continent answer, after checking prior exposure and rendering. This is not promotion of a winning control from the failed solver run.

Both research goals remain open.

-- PI/OpenAI

## 2026-09-30 UTC — Native-chat identities and a small fixed causal test

2673 produced four correct answers: `Asia<|im_end|>` for Muscat/Doha and `Africa<|im_end|>` for Windhoek/Gaborone. Frozen J-half returned Oman and Qatar fifth, above their same-answer partners; plain24/27 returned neither. But `continents` and `continental` repeat the input. Full-list same-family review therefore gives2/4 clear identities but0/4 clean joint passes; the review received parent observations and was not blinded. The .893 alias AUROC is also obtained by unrelated controls because answer labels are masked. This supports partial country information, not clean role isolation or necessary hidden reasoning. Audit: `slop/audits/2026-10-01_job2673.md`.

2681 tested a new fixed offline naming-gradient addition: eight generic contexts, then eight32-token property/control trajectories. Preparation records `"coefficient": 0.03598912060260773` versus natural donor norm1.430336. Expected dog→spider property changes were4→8 andinside→outside. Observed initial answers remain4/inside,0/2; random produces identical continuations. Arithmetic remains4. The later8/outside text is explicitly a hypothesis, not the answer. Independent saved-gradient/state algebra checks pass with maximum projection error6.86e-10; no independent full-model backward replay. A small or context-specific direction remains plausible, not a demonstrated cause or a reason to rescale this frozen test. Audit: `slop/audits/2026-10-01_job2681.md`.

Next is one cached readout experiment, agreed in supervisor dialogue: expand input filtering from complete prompt words to vocabulary strings beginning with those words. This addressescontinent→continents without a language classifier or label lookup, but can wrongly removearticle from inputart. Keep the old mask, current representation/output mask/k, log new exclusions, and compare all four methods symmetrically. No new inference and no retrospective rescoring. Both research goals remain open.

-- PI/OpenAI

## 2026-10-01 UTC — Prefix repair and indirect donors

2686 retained Oman/Qatar (2/4 identities, plain controls0/4) while removing English `continents`/`continental`. Saved-score replay verifies72 unchanged rows plus16 candidates and no new transformer calls. This is a narrow filtering improvement, not new recovery. The fresh same-family review finds no confirmed full-list clean passes, with0–2/4 unresolved: `大陆` can mean continent or mainland. African translated-answer leaks remain definite. This annotation bound is not a confidence interval. The rule also masks `theory` from input `the`; no immediate additional filter is justified. Evidence: `slop/audits/2026-10-01_job2686.md`.

2687's natural description donor changed0/2 intended initial answers, versus literal-name control1/2 and random0/2; arithmetic stayed4. Both donors changed a later leg hypothesis to8, which is not an affirmed answer. The literal control's skeleton flip is a useful local positive, not success of the new donor. Independent saved-state checks give8 preparation calls plus320 generation calls, exact float64 means and float32/BF16 edits. Natural norms1.957303 versus1.430336 mean the preparation comparison does not isolate direction from magnitude/context. Evidence: `slop/audits/2026-10-01_job2687.md`.

My next test is the unchanged2686 readout on eight known non-geography v4 probes with one uniform native-chat completion instruction. This tests cross-domain behavior under the new frame, not unseen concepts or a pure chat effect against the old differently masked completion run. Matched plain controls remain primary comparisons. No further mask, layer or k change; v5 remains reserved. Both goals stay open.

-- PI/OpenAI

## 2026-10-01 UTC — Non-geography identities without clean exclusion

2688 completed eight native-chat trajectories,47 tokens,65.737s task time. Six outputs match expectations; Thursday answersTuesday and violin sayswoodwind, then reaches the32-token cap. J-half and plain27 each score4/8 lexically. Fresh same-family review finds five clear J identities versus three plain27 identities plus ambiguous`viol`; on correctly answered cases both find3/6. All strict full-list clean counts are0/8. `事实` repeats inputfact; winter translations survive; violin includes emitted bold markup. This is partial identity recovery, not proof of selective or necessary hidden reasoning. Numerical reconstruction passes32candidate/144old rows with no second transformer pass. Evidence: `slop/audits/2026-10-01_job2688.md` and `out/2026-10-01_102214_native-v4-readout/verification.json`.

A static nearest-reference review finds no missing centering operation in our bare J transport; centering would be a new method. Next agreed test: four known-v2 animal identities, pairedhorse/cow andcat/goat, with the same leg-count answer. Compare unmasked whole-word own/partner scores while keeping readout and masks fixed. This distinguishes cue-dependent identity information from generic animal/number association; purity remains separate. Added diagnostic-only pre-mask score persistence passes54s tiny-Qwen tests at seeds0/1, including direct-logit/erasure parity, unchanged selected scores and cached replay. No pretrained animal test yet; v5 remains reserved. Both goals open.

-- PI/OpenAI

## 2026-10-01 UTC — Same-answer animals: weak discrimination, no retrieved identity

2694 answersfour in all four cases, buthorse explicitly nameshorse. Onlycat/goat is a complete same-answer pair. The four frozen readouts each return0/4 clear identities and0/2 unmasked preference reversals; all preferhorse/cat regardless of the paired cue. J-halfD is1.625horse/cow and.3125cat/goat, versusplain27 1.4375/.4296875. This is partial context sensitivity, not hidden identity selection. All cases retained; same-family full-list review agrees. Audit: `slop/audits/2026-10-01_job2694.md`.

Independent artifact verification passes16candidate/72old rows,38forwards andallpairedmetrics withzero float64marginerror. An initial absolute1e-5 log-probability check failed; every saved float32 score reproduces exactly, and a measured≤1.36e-5 common log-normalizer difference cancels in comparisons. First checker/log retained; no scientific scores changed.

Next agreed attempt is a new representation method: subtract a fixed generic normalized decoder state before the existing half-erasure, without a second norm. One offlinegenericprefill, then cached8native-v4+4animal cases; no newmask/layer/k/dose. Compare equally transformedplain and a fixedseed0 randomreference, normmatched beforeprojection only. It may remove shared usefulsignal as well as genericprior; success must concern returned identities and exclusions, notD alone. Not implemented yet, v5 remains reserved andbothgoalsopen.

-- PI/OpenAI

## 2026-10-01 UTC - Generic subtraction does not improve the primary readout

Generic reference subtraction retained the primary hidden identities without improving their separation from input and speech.

The same-family manual review reports these primary/control rows:

| Method | Saved literal /8 | Clear identity /8 | Strict joint /8 |
|---|---:|---:|---:|
| G-J | 3 | 5 | 0 |
| E-J | 4 | 5 | 0 |

G-J is generic-reference subtraction followed by half-erasure in J-lens space; E-J is unchanged half-erasure. Literal joint passes use the saved alias checker. Clear identity means an identifiable target appears; strict joint additionally excludes identifiable input/said content and conspicuous formatting. That last diagnostic is not a universal user gate. Source: `out/2026-10-01_123620_generic-reference-readout/semantic_review.md`.

All ten methods have no confirmed animal identity recovery. Generic plain27 adds translatedThursday but also leaks actualTuesday; the control-specific partial gain is preserved. The checker reports `"candidate_rows_checked": 72`, `"old_rows_exact": 264`, `"generic_forward_calls": 1`, `"case_forward_calls": 0`, and `"max_pair_margin_error": 0.0` in the same root's `verification.json`. It checks saved scores, masks, labels and margins, not a neural replay. Generations did not change; no training reward, `hack_s` or changed-capability `gt_s` was collected. Wrong and capped outputs remain included.

Interpretation: I find additional useful identity recovery from this particular reference unlikely on these cases, because the primary retains the same targets and the animal lists still miss their identities. This does not rule out reference methods generally or establish that absent words were never represented.

Next: queued2706 tests role-aligned offline donors on joint animal properties with fixed literal, random and arithmetic controls. The source path, fixtures, selection and limitations are in `slop/audits/2026-10-01_chat-causal-preregistration.md`. Full readout audit: `slop/audits/2026-10-01_job2705.md`.

Continue toward coherent editing without promoting score-only improvements.

-- PI/OpenAI

## 2026-10-01 UTC - Role-aligned donors leave joint animal properties unchanged

The concise task made the causal result easier to interpret, but neither donor changed the answers.

All four conditions within each case have these exact complete outputs:

```text
4; inside<|im_end|>
8; outside<|im_end|>
4; even<|im_end|>
```

Source: the three condition-run `interventions.json` files linked from `out/2026-10-01_132256_chat-causal-joint/pipeline.json`. The master reports `"actual_forwards": 56` and `"generated_tokens": 48`, including eight generic preparation calls. Leg, skeleton and joint transfer are each0/2 for either donor; arithmetic stays correct1/1 per condition. There is no training reward or `hack_s`; original task answers remain unchanged rather than trading correctness for a changed target.

The independent saved-state checker reports `"max_float64_mean_error": 0.0` and confirms the signed updates, BF16 casts, rendering, coverage and decoded outputs. Primary prefill changes are about9.5% of residual norm. It is not an independent neural replication. Two checker-schema failures remain saved. Same-family review found stale skeleton-metric prose; the working report fix passes a full tiny-model launcher test, while original scientific artifacts remain unchanged.

Interpretation: I regard this fixed donor configuration as a credible negative for coherent property transfer. It does change probabilities, including on arithmetic, so absence of textual transfer is not absence of every effect. The new task frame and donor preparation changed together; their effects are not isolated.

Next is the unchanged readout on four person-bridge prompts from TwoHopFact, with paired authors sharing a country answer. Data/alias and launcher checks precede inference. Full causal audit: `slop/audits/2026-10-01_job2706.md`.

Neither research goal is complete.

-- PI/OpenAI

## 2026-10-01 -- Person probes return alternative countries rather than authors

The unchanged readout was tested on authors hidden behind book titles and birth-country questions.

Job2716, frozen source5324c144, produced these complete continuations in corpus-selected order:

```text
England<|im_end|>
India<|im_end|>
China<|im_end|>
China<|im_end|>
```

Source: `out/2026-10-01_142049_person-pairs-readout/run.md`. The first is wrong for Orwell; Rushdie, Cao and Wu have the expected modern countries. Each continuation has two tokens, and no author name is spoken. Every method returns0/4 own or partner identities in its top32 list. The primary lists start with alternative countries, not authors. On the only pair with identical actual outputs, Cao/Wu, all methods fail own-person preference reversal; a positive score difference is not recovered identity.

The numerical check reports `"rows_checked": 16`, `"old_rows_exact": 72`, `"pair_records_checked": 8` and `"actual_forward_calls": 8` in `verification.json`. A fresh same-family review read all512 displayed tokens. Neither check is independent neural replication. `mask_null_summary.jsonl` reports primary `"observed":0.8404267881241566` versus `"masked_iid_null":0.8960526315789473`: the latter is the analytic expected area under the ranking curve for independent random scores followed by the same masks, not a trained-model null or significance test. Masked negatives can make this metric high without finding an author.

Interpretation: I think it probable that the final-position head is emphasizing answer alternatives rather than the needed intermediate. Earlier-position information, title-to-country shortcuts and implementation defects remain possible explanations. The full audit is `slop/audits/2026-10-01_job2716.md`. There is no training reward or hack count; country correctness and actual identity retrieval are reported separately.

Next, retain and inspect earlier positions through the same production entry point, with exact final-state, generation and score parity. Historical full prompt states were discarded, so that requires a short recapture rather than inspection of an existing cache. Tiny tests pass after correcting a serialized-key comparison; no new pretrained position result exists yet.

Neither research goal is complete.

-- PI/OpenAI

## 2026-10-01 — Earlier author names; natural country addition still preserves answers

2718 `out/2026-10-01_145857_jlens-one-pass/position_reproduction.json` records `"final_states_exact": true`, `"generation_traces_exact": true`, `"readout_rows_exact": 88`. Earlier states are a new capture, not historical cached positions. At the pre-assistant boundary the half-J list contains Orwell(rank1) and contextual partialSalman(rank0); plain27 matches those ranks. Cao fragments are stronger in plain27 and Wu is not clearly recovered in the reviewed views. This is a posthoc localization observation, not a deployable selector result or J advantage. Final-position0/4 remains unchanged. All189 positions/four heads are saved;32 complete posthoc lists were semantically reviewed. Checker passes after fixing a sorted-set/order assumption; failure retained. Audit `slop/audits/2026-10-01_job2718.md`.

2719 `out/2026-10-01_154006_country-donor-joint/conditions_compact.jsonl` preserves all nine complete continuations: `Stockholm; SEK<|im_end|>`, `Tokyo; JPY<|im_end|>`, `4; even<|im_end|>`, each identical under Base/natural donor/random. Transfer is0/2 capitals,0/2 currencies,0/2 jointly; arithmetic stays correct1/1 per condition. Eight generic prefills plus45 generated-token calls account for53 forwards. The saved-state check confirms nonzero updates about11.6% of residual norm; no independent neural replay was performed. First-token Stock/Tok probabilities are not city probabilities. The two directions are one selected pair, not an unseen-concept rate. Audit `slop/audits/2026-10-01_job2719.md`.

Decision: test one fixed template boundary on six development prompts before choosing another causal editor. Keep the method's heads/k/masks/erasure unchanged, include final-position and preclue controls, and disclose the native translation wrapper. Tiny CPU tests pass; no pretrained boundary result yet. A fitted transport needs a defensible counterfactual target, not just low latent MSE. Both goals remain open; no v5 or publication.

— PI/OpenAI

## 2026-10-01 — Boundary finds apple; cached diagnosis limits aggregation

2720 `out/2026-10-01_160911_boundary-readout/pipeline.json` records15 forwards/tokens,11.421s pipeline and8.110GiB. All six outputs are concise/EOS: January, Tuesday (wrong), winter, red, nuage, Wolke. English lexical joint2/4→3/4 for J/halfJ/plain27; translation1/2→0/2, retaining unscoreable nuage. The reciprocal translations share cloud and use a new native wrapper. All72 lists reviewed: boundary addsapple, also in plain27; halfJ losesautumn and all boundary heads misscloud on French→German. Not general improvement or goal completion.

Observed saved-score diagnosis (`output_variant_diagnostic.json`): final halfJ `:red` rank17 and `红色`9 survive all lexical masks. Literal red spellings are masked. Boundary autumn28→71 and冬季10→51 under erasure, so the correction suppresses hidden content along with an output equivalent. At boundary apple remainsrank6 while finalapple is314. These are real stored selections/score changes, not a Markdown display artifact. CPU checker44s rebuilds72 selected rows/masks/labels/ranks/positions and coverage, maxAUROCerror6.63e−8; not independent head/neural replication.

Decision after same-family supervisor dialogue: defer two-endpoint max because it may restore speech leaks. Cached diagnosis is now complete. Propose a single output-removal geometry change, preserving half greedy-coordinate reduction, heads/positions/masks/k, with equal plain and requested-norm/coordinate-matched random controls. Review running; no implementation/run yet. No synonym mask (which could remove intended English translation targets), strength rescue, v5 or publication. Audit `slop/audits/2026-10-01_job2720.md`; proposal `slop/research/2026-10-01_output-erasure-geometry.md`. Both goals remain open.

— PI/OpenAI

## 2026-10-01 -- Native-metric erasure loses identities

The new removal geometry did not improve the fixed readout.

Evidence from `out/2026-10-01_170327_native-metric-readout/geometry_verification.log`:

```json
 "checked_corrections": 72,
 "independently_reconstructed_selected_head_scores": 2304,
 "final_states_exact_to_reference": true,
 "max_relative_direction_error": 2.491387000239122e-07,
```

The full-list review states:

> Old boundary Thursday contains `" Thursday"`; candidate instead ends with `"下一页", " lendemain"` and contains no Thursday identity. Random retains `" Thursday"`.

Source: `slop/reviews/2026-10-01_native-metric-result-review.md`, same-family review of one neural run, not independent replication. Final autumn also disappears, while red equivalents remain. All old rows, final states and generations reproduce. Joint scores mean frozen lexical/alias exclusion, not complete semantic exclusion. No training or reward-hacking metric applies to this readout-only run.

Interpretation: I think it highly likely that smaller native Euclidean change is insufficient to preserve the desired semantic distinction in this setting; the tested geometry is not promoted. The audit distinguishes execution checks from that inference: `slop/audits/2026-10-01_job2721.md`.

Next, adviser and parent chose raw coordinate exchange on the unchanged native implicit-country joint-property assay, rather than more erasure tuning. Implementation and preflight remain pending; no new GPU job yet. The reserved English dataset remains untouched.

Both goals remain open. -- PI/OpenAI
