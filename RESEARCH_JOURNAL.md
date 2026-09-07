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

The score is the change in log probability ratio of six versus eight, in nats. [Job 500](out/2026-09-07_svd-ant-parts/run.md). Removal and combined edits both generate six then explain that the animal is a spider. Continued edits often generate social-related content instead of ants. A matched-size random edit and some dog-directed settings also generate six. Dog rank 4 at C=8 does give a dog-related readout and p4=0.862182. These are selected development results, not generalization estimates.

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

Source: [continuous ant sweep](out/2026-09-07_svd-ant-continuous-last3/run.md).

For spider-to-dog, the expected answer is four with coherent dog content. Two conditions
start with four but repeat the bark token. Rank-four combined C=8 produces:

```text
4.

**Explanation:**
The animal that is most famously known for spinning dog吠吠吠吠吠吠吠吠吠吠吠吠吠吠吠
```

Source: [continuous dog sweep](out/2026-09-07_svd-dog-continuous-last3/run.md).
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

Source: [dog refinement](out/2026-09-07_svd-dog-continuous-refine/result.json).
Job 508, ant rank one C=10, logs `p_target=0.5622626543045044` and produces:

```text
6.

**Explanation:**
The animal that spins social or hunting webs is the **social spider** (specifically the genus *Araneus*, such
```

Source: [ant refinement](out/2026-09-07_svd-ant-continuous-refine/result.json).
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

Sources: [ant grid](out/2026-09-07_coordinate-swap-ant/run.md),
[dog grid](out/2026-09-07_coordinate-swap-dog/run.md),
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

Sources: [ant grid](out/2026-09-07_template-contrast-ant/run.md),
[dog grid](out/2026-09-07_template-contrast-dog/run.md).
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
