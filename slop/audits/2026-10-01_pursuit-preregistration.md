# Cached nonnegative matching pursuit

— PI/OpenAI

Frozen scientific contract: `slop/reviews/2026-10-01_after-country-next-test.md`. One local default-queue job, TERM at300s plus15s kill grace. Eight existing v4 cases, zero transformer forwards, zero new generations. Both research goals remain open; this is development, not held-out evidence. No layer/k/dose/window search or alternate-control promotion.

## Method and discriminator

Independently ranked, correlated token directions may repeat the same component. Test whether removing each explained component exposes a more useful inventory:

```text
D[t] = unit((W[t] * final_norm_gain) @ J23)
r = residual24_last; a = zeros(vocabulary)
repeat at most32 times:
    t = argmax(D @ r)                 # lowest token ID breaks ties
    if D[t] @ r <= 0: stop
    amount = D[t] @ r
    a[t] += amount
    r -= amount * D[t]
return positive a after prompt and greedy-final-token masks
```

This is matching pursuit, not the paper's gradient pursuit, orthogonal matching pursuit, NNLS, or a learned sparse autoencoder. Repeats are allowed; earlier coefficients are not refitted. No labels, language filter, prompt mask or answer mask enters decomposition. J24 is the sole primary; plain24/plain27 use the same pursuit with effective-unembedding directions. Exactly zero dictionary norms are excluded and logged; nonfinite values abort. Scores divide accumulated coefficients by the original state norm; they are not probabilities. Inactive/masked scores are negative infinity, with AUROC ties0.5; recovery uses actual returned-set membership.

Controls use raw/unit-dot rankings at each representation's own postmask cardinality, including zero, and also full32. Raw-dot scores are computed as unit-dot times original column norm (float64 multiplication); this equals unnormalized directional dot product up to floating-point normalization error. Previous168 readout rows must reproduce exactly, including the6/8 half-erased plain27 incumbent. These previous formulas remain separate controls, not inputs to pursuit.

| Possibility | Distinguishing observation |
|---|---|
| Component removal helps | Positive paired gain over same-cardinality unit-dot; at least one new reviewed clue-associated recovery |
| Shorter lists alone help | Gain disappears against same-cardinality controls |
| Generic prior dominates | New final hit was already an active atom before the identifying clue |
| Implementation error | Independent reconstruction, old-row parity, masks/cardinality or zero-forward assertions fail |

Rough pre-result predictions:20% chance of meeting the advancement screen; overlapping risks of semantic priors/leaks60%, unhelpful greedy decomposition50%, implementation/scoring error10%, unknown20%. These are subjective, uncalibrated bets. No fitting, learning rate, gradient or seed search exists. Seeds0/1 test algebra/tiny fixtures, not research variability.

## Diagnostics and advancement

Use2637 full-prefill cache, with exact token IDs, offsets and last-state parity. Keep the third question token and the eight fixed pre-clue positions from the contract. Re-tokenize and require each clue once; its preceding token must contain no clue characters. Diagnostics use their own consumed-prefix mask and same-position final-layer greedy mask. Save both masked inventories and unmasked positive atoms: a masked-out prior atom must not masquerade as a new concept. Compare coefficients only after dividing by original state norm.

Numerical prerequisite: primary joint count exceeds its same-cardinality unit-dot count. Then review primary/control gains and losses symmetrically. Advancement also requires positive semantic net gain and at least one reviewed new final recovery absent from both unmasked diagnostic inventories; no definite input/said leak in counted passes. Token aliases provide candidate membership only; semantic review must examine raw words, prompts and actual continuations. Report all plain/full32/incumbent results even if this passes. Initial answer correctness and unscoreable cases remain visible in the fixed denominator8.

This supports temporal clue association only, not counterfactual necessity. Frozen output-matched v5 remains unrun until numerical and semantic prerequisites pass. Old failed gates stay retired; the prior7/8 heuristic is not retrospectively changed or presented as the user's requirement.

## Evidence before queueing

Core helpers passed independent float64 reconstruction and seeds0/1, including repeated atoms, ties, tiny norms, zero states, no-positive stopping and nonfinite rejection (`2026-10-01_matching-pursuit-core-check.log`). Extended scoring and full-main tiny BF16 Qwen checks passed at seeds0/1 (final chain25s, now preserved as `2026-10-01_matching-pursuit-check.before-batching.log` and `2026-10-01_pursuit-main-smoke.before-batching.log`). Both logs pin source SHA a7e7da2daf3ac8945a5056335e2fea92893e01eda4c091de47989a442cbaa167. Each tiny main run preserved42 baseline rows and exact cached IDs/states, exercised zero-forward guards and checked matched cardinalities. These are random-model smoke results, not scientific performance. Cache hashes are in `2026-10-01_pursuit-cache-sha256.json`. Launcher syntax/fixed invocation, five helper hashes and v4 hash passed parent checks; the full launcher has not run. Expected artifacts: sparse coefficients/step traces/residual norms, masks/cardinalities, full-vocabulary scores, cached-state provenance and exact old-row parity. Full neural probability reproduction is not established by these checks.

Fresh reviewer78b61f78 found no blocker, but noted missing positive scorer fixtures and extreme-state norm risks (`slop/reviews/2026-10-01_pursuit-implementation-review.md`). Parent then executed the actual production scoring loop on known-positive, said/input-leaking, tied, undefined and empty-return cases. The extreme-state test reproduced float32 norm0 at1e-30 and infinity at1e20; norm calculation and coefficient normalization now use float64, with finite positive-score assertions. Both updated test suites passed. No production state is claimed to have these extreme scales. Reviewer saw the earlier version, not these repairs or the later launcher. Same model family; no cross-family independence claimed.

## Pre-run ml-debug record

| Check | Evidence or pending observation |
|---|---|
| Complete logs/config | Read9-line helper/scorer log and204-line tiny-main log; source SHA above. New4B run pending. |
| Expected behavior | Nonnegative coefficients, reconstruction, cardinality parity and zero scoring forwards checked; no predicted semantic count asserted. |
| Metric scale/null | Frozen incumbent6/8; actual pursuit/unit-dot counts unknown. Inactive-vs-inactive AUROC=.5 and empty return fails retrieval in production scorer fixture. No unconditional random-vocabulary joint floor claimed. |
| Init/base/held-out | No fitting or updates. Tiny random generations are nonsensical; v4 is reused development; v5 unrun. |
| Dummy/control | Same-cardinality raw/unit-dot and plain pursuit. Controls' scientific outcomes pending. |
| Schedule/loss/gradient | None: fixed greedy32-step decomposition, not training. |
| Complete sample | Two full tiny generations per seed and method tables in smoke log; scientific cached generations will be retained unchanged. |
| Surprise/alternate cause | Float32 state norm0/inf was reproduced and repaired. Shorter lists or lexical priors could still create apparent gains. |
| Missing trust evidence | Production GPU/time/memory, full-size old-row parity and symmetric semantic review. |
| Diagnoses | Component redundancy, shorter-list shortcut, generic prior, implementation/scoring error; overlapping pre-result probabilities above, no identified scientific cause. |
| Fresh review | “No blocker found for the frozen eight-case cached experiment.” Same-family static review; two edge-case gaps addressed afterwards. |
| Cheapest discriminator | The one fixed cached run, equal cardinalities and pre-clue inventories. No next causal run is hidden in this job. |
| Runtime/resources | Final CPU chain25s; production bounded TERM300s+15s grace. Global GPU peak will be recorded; no per-stage GPU estimate claimed. |

A negative result would reject this greedy32-step configuration, not sparse representations generally. A positive alias result can still reflect partial-token matches, translated input/answer leaks, or topic priors; semantic review remains necessary.


## Submission

Queued2650 from96bd601 on default (one parallel), behind existing2646/2649. Native followerproc_460e. MainSHAa7e7da2daf3ac8945a5056335e2fea92893e01eda4c091de47989a442cbaa167; launcherSHAb3f699fc8005d0f2b84d796ff4cae85cf789e35fb8083fd43bba507a1183855f; dataSHAf7e253176a60ab43d99b019d2b84fbec97cde0ba4df6c08b172d7c7f8f3a2173. Exact metadata: `2026-10-01_job2650-queued.json` (environment omitted).

```sh
env PYTHONPATH=/dev/shm/suppressed-import-7ac02bf HF_HUB_OFFLINE=1 timeout --signal=TERM --kill-after=15s 300 uv run --no-sync --offline python -u .local/queued/pursuit_96bd601.py .local/queued/08_pursuit_96bd601.py .local/queued/english_v4_96bd601.json
```

Snapshots are read-only. No outcome observed at submission. — PI/OpenAI

## Resource repair after2650

Task2650 failed34.718s before scoring: dictionary norm computation requested4.74GiB with3.72GiB free. This is not0/8 and does not judge the method. Audit: `2026-10-01_job2650.md`. Unit normalization now processes4096 rows at a time, retaining float64 norms/division and full float32 dictionaries. SourceSHA28ee6d7b2108eb0ee3244894d4d8cc318261e4fc10c3a102c1f7a2bfa9ff6451. No layer, k, precision, mask, scoring or control change.

Updated helper/scorer and tiny-main checks passed36s at seeds0/1.8197-row dense/batched normalization is bitwise equal on CPU, including boundary, zero and tiny rows. GPU capacity and bitwise parity remain untested. Fresh review8200c458 found no static blocker to one scientifically unchanged bounded retry. Those logs are now preserved as `.before-bounded-checks.log`; `.before-batching.log` preserves the original checks. — PI/OpenAI

## Second resource repair after2653

2653 failed9.656s before scoring at the remaining full-dictionary finite check (608MiB requested,163MiB free). Audit: `2026-10-01_job2653.md`. Input/output finite checks are now tiled too; J is constructed first without keeping the full effective matrix across both constructors. The repeated pursuit-time full-matrix check is removed: dictionaries are validated on construction and projection vectors remain checked. No scientific change; full dictionaries and precision retained.

CPU dense parity, allocation-bound instrumentation, production scorer fixtures and tiny full-main checks passed seeds0/1 in39s, sourceSHA886566778004d6a47229210b3a69fc7ce797095a329b6030c954095dac94a05e. Current `.log` files contain this evidence. Fresh reviewer53d54258 found no static blocker; production GPU capacity remains unknown. The independent artifact checker is prepared and syntax-checked, not executed; it will reconstruct selected directions and saved-score rankings, not every unselected greedy competitor. — PI/OpenAI
