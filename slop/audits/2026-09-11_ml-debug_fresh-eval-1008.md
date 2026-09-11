# ml-debug audit: fresh-set evaluation batch 1008 (corrected)

Primary last experiment: task 1008 (fresh-set evaluation of the frozen L20 C1.5 candidate; 12
questions x candidate/C0/random-C1.5, one model load via `--batch-spec`). Inference, not
training; optimizer/gradient rows are N/A. Raw per-cell artifacts:
`out/2026-09-10_eval-{candidate,C0,random}-C1.5-*/result.json` (36 cells). Adjudication
(human-read full continuations + verbatim quotes, all machine-verified as substrings):
`slop/eval_fresh_adjudications.json`. This file corrects the first audit (`a2a27b5`) per a
second review.

## Resolved config (as the runner wrote it)

From `out/2026-09-10_eval-candidate-C1.5-legs-L1-dog/result.json`:
model Qwen/Qwen3.5-4B rev 851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a, torch 2.13.0,
transformers 5.16.1, accelerate 1.14.0, pyarrow 25.0.1, git v0.1.1-394-gb488cc0. Sweep
`span-correction-sweep` index 3: detector_layers (18,20,32), rank 8, persistent_rank 4,
intervention_layer (20,), intervention_positions 3, readout_positions 4, strength 1.5,
template_contrast=True, template_state_span="attenuation", delta_component "difference",
span_correction=True, continue_generation=True. **match_component_norm=True is in the config but
the `span_corrected_delta` branch (scripts/demo.py) never reads it** — so there is NO effective
component-norm matching and NO residual renormalization; the equation is
`h' = h + C(delta - U U^T h)`, raw. Label applied: "no matching effectively", not config
semantics. C0 = index 0; random = index 7 (`inspan_seed0_C1.5`).
12 questions x 3 conditions = 36 cells; max_new_tokens 128; prefill wrapper "Answer the question
with the answer first. Then describe the animal in three sentences.".

## Log line count

The pueue task log for 1008 is short (the runner prints one line per cell write; the real data is
per-cell result.json). Raw evidence is per-cell. The runner's aggregate stdout ends with the
last-cell run.md render; there is no monolithic training log. Ground truth is the 36 result.json
files (each with its own resolved config, rendered inputs, readouts, top-token tables, generation
token ids + text, intervention_record with prefill positions and per-step decode_trace).

## SHOULD lines and observations (no retrospective fiction)

Manifest (slop/2026-09-10_eval_manifest.md rev 4, hash 62d96b70…) written before the run.
- SHOULD: every question's source and donor prompt share the last-3 tokens (runner assertion).
  Observed: all 36 cells wrote without the shared-suffix assertion failing; per-entry
  `suffix_shared_last3` True in the manifest entry file.
- SHOULD: C=0 gives exact base identity. Observed: all 12 C0 cells have swap_log_odds_shift == 0.0
  (verified 12/12 exact).
- SHOULD: full per-call arrays recorded. Observed (verified, not assumed): candidate
  legs-L1-dog has prefill_positions [46,47,48], decode_steps 65, generated_tokens 66, and
  replacement_trace length 66 (== prefill(1) + decode(65)), decode_steps == generated-1. The two
  128-token cells are capped-at-cap (prefill [42,43,44], decode_steps 127, generated 128).

No unexplained expectation is asserted as fact. Anything not measured is `TODO validate`.

## The numbers vs nulls/floors (per-cell sources)

Primary semantic success = answer AND persistent identity AND coherence; formatting is separate.

| metric | candidate C1.5 ↑ | matched-random C1.5 ↑ | floor/reference ↑ |
|---|---:|---:|---:|
| primary (all three) | **6/12** | 1/12 | C0 = 0 movement |
| answer | 7/12 | 4/12 | |
| identity | 9/12 | 1/12 | |
| coherence | 6/12 | 7/12 | |

Per type (candidate): legs **4/4**; naming 2/4 (dog rows clean, both ant rows loop); property 0/4.
Per animal (candidate): **dog 4/6**, **ant 2/6** (dog = name-N1/N2-dog + legs-L1/L2-dog = 4;
ant = legs-L1/L2-ant = 2; the other 4 dog or ant rows fail primary).
Capped at 128: candidate 3 cells (`name-N1-ant`, `name-N2-ant`, `prop-P1-spinneret-ant`),
random 4 cells (those 3 + `prop-P1-spinneret-dog`).

### Per-condition (candidate), sorted by swap log-odds movement

Cell links are direct artifact paths. Every numeral here is read from that file.

| cell | swap log-odds ↑ | p(target) ↑ | answer token | censor ↑(0=no) | primary? |
|---|---:|---:|---|---:|---|
| [`name-N2-dog`](out/2026-09-10_eval-candidate-C1.5-name-N2-dog/result.json) | +24.03 | 0.017 | 狗(Dog) | EOS | ✔ |
| [`name-N1-dog`](out/2026-09-10_eval-candidate-C1.5-name-N1-dog/result.json) | +23.43 | 0.008 | 狗(Dog) | EOS | ✔ |
| [`name-N1-ant`](out/2026-09-10_eval-candidate-C1.5-name-N1-ant/result.json) | +16.56 | 0.005 | — | 128 | ✘ |
| [`name-N2-ant`](out/2026-09-10_eval-candidate-C1.5-name-N2-ant/result.json) | +16.20 | 0.004 | — | 128 | ✘ |
| [`legs-L1-dog`](out/2026-09-10_eval-candidate-C1.5-legs-L1-dog/result.json) | +10.75 | 0.939 | 4 | EOS | ✔ |
| [`legs-L2-dog`](out/2026-09-10_eval-candidate-C1.5-legs-L2-dog/result.json) | +10.50 | 0.969 | 4 | EOS | ✔ |
| [`legs-L2-ant`](out/2026-09-10_eval-candidate-C1.5-legs-L2-ant/result.json) | +10.38 | 0.989 | 6 | EOS | ✔ |
| [`legs-L1-ant`](out/2026-09-10_eval-candidate-C1.5-legs-L1-ant/result.json) | +9.62 | 0.987 | 6 | EOS | ✔ |
| [`prop-P2-liveyoung-dog`](out/2026-09-10_eval-candidate-C1.5-prop-P2-liveyoung-dog/result.json) | +0.12 | 0.004 | — | EOS | ✘ |
| [`prop-P2-liveyoung-ant`](out/2026-09-10_eval-candidate-C1.5-prop-P2-liveyoung-ant/result.json) | +0.00 | 0.001 | No | EOS | ✘ |
| [`prop-P1-spinneret-ant`](out/2026-09-10_eval-candidate-C1.5-prop-P1-spinneret-ant/result.json) | +0.03 | 0.000 | — | 128 | ✘ |
| [`prop-P1-spinneret-dog`](out/2026-09-10_eval-candidate-C1.5-prop-P1-spinneret-dog/result.json) | −1.53 | 0.000 | — | EOS | ✘ |

### Representative full input and output sample (legs-L1-dog, candidate)

Rendered source input (from `rendered_inputs.source.rendered`):
```
<|im_start|>user
Answer the question with the answer first. Then describe the animal in three sentences.<|im_end|>
<|im_start|>assistant
<think>
```
Base (clean source) continuation ends:
```
8

The spider is an arachnid that typically has eight legs, distinguishing it from insects which have six. These appendages are used for walking, sensing vibrations, and manipulating silk threads to build intricate webs. Despite their small size, spiders are powerful predators capable of injecting venom to subdue their prey.<|im_end|>
```
Intervention continuation ends:
```
4

The animal is a dog, a popular domesticated breed known for its loyalty and friendly demeanor. Dogs typically have a thick coat of fur that comes in various colors and textures to suit different climates. They are excellent companions for families and often serve as working animals in roles such as hunting, herding, and assistance.<|im_end|>
```

## Measured peak GPU memory

`peak_gpu_memory_bytes`: candidate legs-L1-dog 14,024,784,384 = 13.06 GiB; random
prop-P1-spinneret-dog 14,083,030,528 = 13.12 GiB. (Same card, one model load + 36 cells;
no OOM — the earlier notebook autograd OOM was a notebook-only defect, not this batch.)

## Coverage (inspected, not assumed)

Verified per-cell arrays (see SHOULD row): prefill_positions length = 3; decode_steps =
generated_tokens − 1; replacement_trace length = decode_steps + 1 (prefill + decode). For the
capped cells decode_steps = 127, generated = 128, prefill 3 positions. The confidence in "all 36
cells wrote coverage" is high for the sampled cells; the runner asserts covered per cell.

## Competing hypotheses (with rough credence, evidence both ways)

1. **The candidate genuinely carries answer+identity on legs and dog-naming; property and
   ant-naming are the open failures.** Credence ~0.5. For: the 6 primary cells (4 legs + 2
   naming) are coherent with the correct animal; C0 identity is exact; the fresh questions were
   never run before. Against: the matched-random control at 1.2-2.6x larger total-applied-norm
   still produces some dog leg digits (legs-L1/L2-dog random: shift +12.50/+12.81, first '4',
   but identity 'cow'), so the legs *digit* is not direction-specific — only the *animal* is.
2. **The candidate-vs-random gap is confounded by the random control being 1.2-2.6x LARGER
   magnitude; a larger perturbation can destroy coherence, which would inflate the candidate's
   apparent advantage.** Credence ~0.5 that 6-vs-1 is not yet a clean-controlled estimate. For:
   total_applied_norm ratio per pairing is 1.17-2.60 (legs-L2-ant 456 vs 1187 = 2.60; name-N2-ant
   1322 vs 1548 = 1.17), and total norm depends on output length (candidate legs-L1-dog 66 tokens
   vs random 73; candidate ant 128 vs random 128), so the two conditions are not equal-magnitude
   and not matched in trajectory. Against (why it is not decisive): a larger random perturbation
   that still fails to attach the correct animal is weak evidence, but it does not prove the
   candidate helper is confounded — the direction-specific identity carry is not explained by
   magnitude alone. The honest position: the 6-vs-1 gap is direction-specific and NOT yet
   magnitude-controlled; the separating test is per-call matched magnitude.
3. **The `first_answer` field is an unreliable proxy.** Credence ~0.9. Evidence: name-N1-dog has
   first_answer=None yet the continuation begins `狗 (Dog)`; prop-P2-liveyoung-dog has
   first_answer='0' yet the prose is unambiguously correct; the adjudication used the full text
   precisely because of this.
4. **Residual harness/per-cell bug.** Credence ~0.1. Nothing found; all 36 cells wrote, all quotes
   are exact substrings, C0 identity exact. The flagged failures have clear textual reasons
   (repetition loop; fabricated "ants have spinnerets"; "the dog does not give birth to live
   young"), which are properties of the model output, not the harness.
5. **Unknown / untested mechanism.** Credence ~0.05: whether a lower C, a wider token window, or a
   different construction would rescue ant-naming or property is untested; the mechanism by which
   the candidate attaches animal identity but not the property answer is observed, not explained.

The two dominant, mutually-incompatible readings (1 vs 2) share a cheap discriminating test.

## Cheapest separating test

Per-call magnitude-matched rerun: for each pairing, set the random control's per-call edit norm to
equal the candidate's, holding the reference trajectory/length policy fixed (declare which
trajectory is the reference and how length is handled, because total norm depends on output
length). Compare primary on legs-dog/legs-ant and name-dog cells. If the candidate still beats the
random at matched per-call magnitude, (2) is rejected and (1) strengthens. If the gap collapses,
the apparent advantage was mostly magnitude. This is NOT an authorization to run yet — it is the
test the evidence points to, to be run only with the intended common-subspace construction.

## ex A: options considered (retrospective; no pre-run dated source exists for the 1008 batch)

The manifest/plan recorded the candidate-vs-random design; the options below are reconstructed
from the plan's scope, not a contemporaneous pre-run table. Marked retrospective.

| option | metric it should influence | direction | what separates it |
|---|---|---|---|
| candidate L20 C1.5 span-correction | primary | correct on legs/naming | the recovered reference |
| C0 identity control | zero movement | no change | the null |
| in-span random same C | should not carry identity | small / wrong animal | direction-specific vs not |
| (prior) synchronized donor updating | identity persistence | reduced distortion, no transfer | different equation |

## ex B: predictions (retrospective, not a contemporaneous pre-run record)

No dated pre-run prediction file exists for batch 1008; the predictions below are reconstructed
from the plan and are labelled retrospective, not "before run". Observed values are quoted from the
artifacts.

| risky part | retrospective expected | observed | buggy? | metric exists |
|---|---|---|---|---|
| candidate transfers legs answer+identity | 4/4 coherent dog/ant legs | 4/4 (legs-L1/L2-dog/ant primary) | no | adjudication |
| random matches candidate | random primary ~ candidate | random 1/12 vs candidate 6/12 | magnitude mismatch noted | primary |
| property does not transfer | 0/4 coherent | 0/4 | two cells show answer/identity contradiction | adjudication |

## ex C: second cause for the same number

The candidate's 6/12 could be (a) a direction-specific carry or (b) an artifact of the random
condition being 1.2-2.6x larger and self-incoherent. These are not separated; the separating test
above is the per-call magnitude-matched rerun. I do not assert 6-vs-1 is a clean controlled
estimate.

## ex D: rows before an "impossible" value

No spike. The 128-token cells are capped by the configured max; preceding rows show bigram 0.65
(repetition loop) rather than a sudden collapse. first_answer=None is a parser behavior (CJK or a
list answer), not an impossible number.

## ex E: reference implementation (recovered prior common-subspace construction)

`token_persistent_subspace` (suppressed_activation_subspace.py) and the prior `svd-*` family
(oat_sweep.py). Feature comparison:

| feature | prior (svd-ant-parts, job 500) | this candidate | same? |
|---|---|---|---|
| selector | token-persistent SVD (avg projector span) | template-attenuation rank-4 | no |
| equation | projected token-mean residual difference | h + C(delta − U U^T h) | no |
| layer | L24 | L20 | no |
| donor term | token-mean donor/source residual difference | template-contrast attenuation delta | no |
| C0 identity | asserted | asserted | yes |
| match_component_norm | unused effectively | unused effectively | yes |

## ex F: external review

A single-model blind review (GLM 5.3 Flash via pirev, a read-only reviewer different from the
writer family) was requested with the artifact facts only. Verdict:
PENDING / to be merged when the trace lands (`slop/reviews/2026-09-11_glm-5.3-flash_blind_review_fresh_eval.md`).
The earlier code review (shared-coordinate replacement) was done in the prior session and is
unchanged for this runtime.

## ex G: what else could score well on the headline

The candidate's legs primary could be gamed by prior knowledge (model defaults dog=4/ant=6) or a
trivially available digit. Counterevidence: C0 leaves the base answer (8); the random control
gives the digit for dog rows but the wrong animal; the fresh questions were never run before. The
6/12 is not explained by "the model always answers 4/6", because C0 and naming/property do not.

## ex H: the scale first

Floor C0 = 0 movement; reference random = 1/12. 6/12 is read against those. No threshold set
without this table.

## ex I: three ways the result is false

1. **Magnitude confound** (the random condition is 1.2-2.6x larger; a larger perturbation can
   destroy coherence, inflating the candidate's edge). Supported by the documented norm ratios; the
   separating test is per-call matched magnitude. This is not "none supported".
2. **Proxy scoring** (first_answer/adjudication mismatch). The adjudication uses full text and
   quotes; re-check one quote against the saved text (verified this audit).
3. **Question-set leakage** (the "fresh" set is not fresh). The manifest audited every string
   against saved prompt inputs; re-audit the manifest entry list if in doubt.

These are not all equally supported: (1) is supported by the norm data; (2) is mitigated but not
absent; (3) is mitigated by the audit. The remaining uncertainty concentrates on (1).

## ex J: one implementation is not the idea

The proposal being tested (a common per-token subspace) is not the candidate rule. The candidate
is the recovered L20 C1.5 span-correction reference; the common-subspace proposal is the next
construction to compare. A property-limited candidate result is not a verdict on the
common-subspace idea.

## Wall-clock, memory, and duration

task 1008 start 17:56:13 end 18:01:55 (about 5m42s), 36 cells, one model load, peak GPU ~13.1 GiB.
The loop would shorten by (already) batching one load and by precomputing the adjudication record.

## Direct sources for the numerals above

- primary/answer/identity/coherence counts, per-type and per-animal: derived from
  `slop/eval_fresh_adjudications.json` rows (aggregated in-notebook).
- swap-log-odds, p(target), answer token, censor, total_applied_norm, generated_tokens:
  each `out/2026-09-10_eval-candidate-C1.5-*/result.json` (read directly).
- C0 shift 0.0: each `out/2026-09-10_eval-C0-*/result.json` row's `swap_log_odds_shift`.
- peak GPU: `peak_gpu_memory_bytes` in the cited result.json.
- rendered input: `rendered_inputs.source.rendered`.
- coverage arrays: `intervention_record[layer].{prefill_positions,decode_steps,replacement_trace}`.

## One coherent decision from this audit

The candidate produces a direction-specific primary advantage (6/12 vs random 1/12), but the
matched-random control is not magnitude-matched (1.2-2.6x larger total norm, and total norm
depends on trajectory length), so the gap is not yet a fully controlled estimate. The dominant
alternative reading is the magnitude confound (hypothesis 2), and the cheapest separating test is
a per-call magnitude-matched comparison. This is the immediate evidence-driven next step and is
the natural contrast for the Goal 3 common-subspace construction; it is not authorized as a
standalone magnitude-only rerun ahead of that construction.

## TODO validate

- Per-call matched-magnitude comparison (needs the common-subspace construction or a designated
  reference trajectory policy).
- Whether a lower C or wider token window would change ant-naming/property (untested).
- The blind-review verdict (PENDING; merge on completion).
