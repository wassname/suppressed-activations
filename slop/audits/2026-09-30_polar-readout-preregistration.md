# One cached polar-factor readout

— PI/OpenAI. Frozen before production outcome. Contract: `slop/reviews/2026-09-30_after-pooling-next-test.md`.

Goal: recover a hidden English concept while excluding input and actual output, not just make a numerical transform pass tests. Pooling is retired: selected plain27 fell5→4/8, tied mismatch/unsubtracted; its four lexical passes leak input. Earlier generic peaks can precede identifying clues.

## Method and decision

Compute the full-rank polar factor of J24: float64 SVD `J = U @ diag(s) @ Vh`, then `Q = U @ Vh`. Reject nonfinite or numerically rank-deficient J (`s_min <= eps64*d*s_max`); no null-space extension, truncation, determinant correction, spectral power or tuning. Apply Q in float32, then the original BF16 final norm/head. Q preserves Euclidean geometry before floating-point/casting error; that does not establish semantic preservation. This is an experimental departure, not reference reproduction.

```python
p_Q = head(final_norm((h_last.float() @ Q.T).bfloat16())).softmax(-1)
score = p_Q - p_final_last
rank = stable_descending(score.masked_fill(prompt_mask | greedy1_mask | (score <= 0), -inf))[:32]
```

Q is the sole candidate. Seven branches: Q excess, original-J excess, plain24 excess, plain27 excess, Q cyclic-mismatched excess, Q unsubtracted, and Q early-prefix excess. All normalize the full vocabulary before the same masks. The early control uses the third fully-contained question token from2637's saved offsets; assert decoded pieces `Fact`, `:`, ` The`/` In`. It uses each case's own final-LAST comparator and masks, not a position-local comparator. It misses later topic priors. Other seven v4 hidden-alias sets are evaluation-only negatives, not topic-matched tests. Label/text mutations do not change candidate scores in the CPU check.

Promising requires >=7/8 alias-checked joint, strictly more than original-J, both plains and Q mismatch, and a strictly larger maximum eligible hidden score than early-prefix for every counted pass. Preserve the6/8 half-plain27 incumbent. Require symmetric blinded semantic review before new examples; no definite input/said leak among counted passes. Then freeze for output-matched clue substitutions. Unsubtracted parity precludes a subtraction-benefit claim. Failed candidate: no spectrum/layer/window rescue or alternate winner.

## Execution and evidence

One default-queue local GPU replay,300s TERM +15s kill grace. No production transformer forwards, new generations or calibration. Reuse `out/2026-09-30_185058_jlens-one-pass/` states, spans and eight generations. Model/backbone guards reject inference. Existing168 rows must exactly reproduce2621; traces and last states must match2637. Separate erasure controls remain for parity and are never composed with Q.

Save Q/spectrum/rank/reconstruction/orthogonality metadata and identities, raw signed excess/eligibility for every selected and scoring-label token, masks, early prefixes, wrong-label ranks and full-versus-early maxima/margins. Also save complete vocabulary probability tensors per case, enabling independent vocabulary-wide score/rank reconstruction rather than only subset checks. This does not independently prove the model-weight transport itself. Pin/copy five imported helpers before and after the main. Candidate Q, its source J and model/lens revisions are recorded; the lens fitting-model revision remains unknown.

## Checks before the production run

- Algebra, seeds0/1: known polar factor with repeated positive singular values, positive scale invariance, norm preservation, reflection retained, rank-deficient/zero rejection. Process17ed succeeded22s.
- Actual branch with real tiny BF16 Qwen norm/head and pinned tokenizer, seeds0/1: all eight spans including In, seven branches, full probability I/O, exact old control scores, label invariance, masks/ties/empty eligibility and forward guards. First fixture failed `NameError: name 'mask' is not defined`; production defines mask. Failure preserved; fixed fixture passed both seeds in36s (f6e9).
- Full main, seeds0/1: real tiny32-layer BF16 Qwen generates/captures two toy cases, then production main replays with real norm/head/scoring/I/O and no scoring forwards.28 methods ×2 cases; exact cached IDs/states. CPU-only device adapters, tiny model/checkpoint loaders, unchanged arithmetic. Processd600 succeeded25s. Both scored/unscoreable paths occur. Toy multilingual nonsense is expected, not semantic evidence; full log103lines read.
- Fresh read-only implementation review1a7dc84e is pending. No implementation defect is inferred from a passing smoke. Full-size SVD, production parity, latency/VRAM and semantic results remain unknown.

## ml-debug pre-run form

- Options: repeat pooling rejected by joint/control evidence; sparse clamp deferred because algorithmic choices remain; polar chosen as one representation hypothesis. No new fit or generated cohort.
- Prediction: Q may remove dominant gains but also amplify relative noise in small-singular directions. Rough prior:20% chance of improving the frozen joint screen, not a calibrated probability. No claim that orthogonality implies hidden-concept recovery.
- Config/SHOULD: `SHOULD: old168 rows and cached IDs/states are identical` from unchanged production scoring and no inference. `TODO validate: Q improves joint recovery and exceeds the early-prefix control.` Observations pending.
- Null/scale: last-position J4/8, plain241/8, plain275/8; incumbent6/8, all development. >=7 is a fixed improvement screen, not a power-derived significance threshold. Random semantic performance unmeasured. Prefix/mismatch/unsubtracted provide diagnostic controls, not independent examples.
- Init/demo: no updates. Actual v4 baseline violin is ` the woodwind family.\nQuestion:` and remains wrong/included. Exact eight samples remain in2637/readout.json; no generated-string changes. Toy init sample seed0 December is ` такому Ziel开水 unfavorableতারodik_hdl医养`; no inference about the real model follows.
- Training loss/LR/gradients: not applicable. Held-out comparison: not run; v4 is repeatedly inspected development.
- Surprises:2637 population peak.678586 occurs after common Fact:The, before clues; explained as a possible generic-prior competitor, not proof the demonstration causes it. Q is a new hypothesis about representation, not a proven fix.
- Diagnoses (overlapping rough credences): arithmetic/indexing bug5% after CPU checks but before4B; eval blind spots>95% (observed capital/capitals and translated answers); generic/late topic shortcut70% (pre-clue peaks, not specific to the new unrun Q); unknown20%. Strong contrary evidence for a universal implementation failure: exact old rows/span checks and reference orientation agreement. No outcome yet distinguishes representation noise from useful gain removal.
- Cheapest discriminator: this one zero-inference replay. True useful recovery must exceed equally scored plain/J, mismatched and early-prefix controls, then survive semantic review. Another way to score well is generic topic membership; early control cannot eliminate that, hence future output-matched substitutions remain required.
- Missing evidence: full-size parity/finite SVD, exact vocabulary ranking, semantic audit and unseen clue-specificity; all are planned in dependency order. No broad conclusion if this fixed implementation fails.
- Time/VRAM: production pending. Smoke25s, branch36s, algebra22s are separate CPU processes. No paid compute. Remaining limits and fresh-review findings will be appended after the actual run.

## Post-result status (not preregistered knowledge)

Job2642/source0ae6378 failed its fixed screen: Q1/8, originalJ4/8, plain275/8; own mismatch/unsubtracted1/8. Source/cache/span/168 old-row parity and full-vocabulary reconstruction passed; independent CPU SVD agrees within1.86e-9. Task55.55s/main22.43s; peak GPU memory unrecorded. Fresh review supports this negative result but is not complete source/semantic certification. Retired without retuning; v5 remains unrun. Full evidence: `slop/audits/2026-09-30_job2642.md`. Both goals remain open. — PI/OpenAI
