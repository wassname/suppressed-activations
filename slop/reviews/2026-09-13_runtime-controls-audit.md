# Runtime-controls audit update — cached/uncached equivalence rebuilt and executed

Author: PI/glm-5p3-flash (implementation worker f15929b4). Supervisor owns goal status.
This replaces — does not patch — the vacuous section 3 of the previous
`scripts/runtime_controls.py` (empty hooks, `max_new_tokens=1`, no cached decode,
unused `res1/logits1`) and removes the docstring's unimplemented "positive pinned
reference" claim. Spec: `slop/2026-09-13_runtime-controls-spec.md` (batchwork).

## What was executed (all through production code paths)

1. `scripts/runtime_controls.py` on `wassname/qwen3-5lyr-tiny-random`, CPU, bf16 and
   fp32 (`.local/verify_logs/runtime-controls/tiny-cpu.txt`, `tiny-cpu-fp32.txt`;
   `out/2026-09-13_runtime-controls-qwen3-5lyr-tiny-random/result.json`).
2. Same on `Qwen/Qwen3.5-4B`, GPU (pueue 1272; `4b-gpu.txt`;
   `out/2026-09-13_runtime-controls-Qwen3.5-4B/result.json`), control layer 26,
   control rank 256, C=8 (a mechanics control, not a scientific condition).
3. Pinned positive reference re-executed via the exact existing path
   `scripts/confirm_causal_demo.py` (main worktree, pueue 1268, 154.8s):
   `out/2026-09-13_072434_causal-confirmation/`.

## Observed results (quoted from saved output)

Tiny bf16 CPU:

> 3. cached/uncached teacher-forced equivalence (n=6, decode_steps=5): per-step rel
> logit delta max 6.38e-02, rel hidden delta max 2.62e+00, tol_rel 8.11e-01 OK;
> argmax match 6/6 (no flips); first-token shift vs clean 1.88e+00 (nonzero) OK
> probes: wrong-mask rel delta 6.99e+00, no-hook rel delta 6.99e+00 (both must
> exceed tol_rel 8.11e-01) OK

fp32 tiny: per-step rel delta max 7.64e-06, argmax 6/6 — mask/placement logic is
exact in fp32; bf16 residuals are rounding, not logic.

Qwen3.5-4B GPU (corrected runs, unique per-attempt result dirs):

> pueue 1289 — L26 random-basis cache-mechanics control (rank 256, C=8), PASS:
> 3. cached/uncached teacher-forced equivalence (n=6, decode_steps=5): per-step rel
> logit delta max 1.53e-01 (null max 1.24e-01), rel hidden delta max 1.42e-01
> (null max 1.69e-01), tol = 2x max null (fixed, not widened) = 2.48e-01 OK;
> argmax match 5/6 (tie flip at step 2: gap within measured step delta — consistent
> with rank uncertainty, NOT proof of numerics-only); first-token shift 1.71e+01 OK
> probes: wrong-mask rel 8.50e+00, no-hook rel 8.50e+00 OK
> pueue 1290 — L26 C=1.5 rank 4, FAILED marginal:
> AssertionError: cached/uncached final hidden diverge at decode-5: rel 3.399e-01 >
> tol 3.386e-01 (logit per-step asserts passed within the same 2x-null bound)
> pueue 1291 — actual 4B site h1 (L1), C=1.5 rank 4, FAILED:
> AssertionError: intervention did not move the first-token logits beyond numerics:
> shift 1.562e-01 vs clean null 1.250e-01 (per-step logit+hidden equivalence asserts
> all passed within 2x-null before this check)

Scope of these controls: RANDOM-basis cache-mechanics controls through the production
hooks — NOT the actual trajectory-basis/bank-construction integration; sites actually
exercised: residual L26 and L1 on Qwen3.5-4B (36 layers), L1/L2 on the tiny model.
No multi-layer interval hooks tested. 1289 logit control (0.153) EXCEEDS its null
(0.124); it passes the fixed 2x-null criterion, it is not below-null. 1290's
marginal hidden exceedance (1.004x tol at decode-5, weakest intervention) and 1291's
undetectable intervention (shift 1.25x null at L1) are labeled HYPOTHESES (numerics
floor / intervention-too-weak-to-test), not conclusions; neither run is counted as a
pass and no tolerance was widened after seeing them.

Per-condition generation lengths in the pinned reference (from token IDs, both runs
identical): every condition generates exactly 64 tokens (14 conditions, no early
EOS): spider_clean, spider_ant_C4, spider_dog_C4, both random-distance seeds,
byte_*, two_plus_two_C4, three_plus_three_C4, target cleans, forced_4/forced_6.
The AGENTS.md README template shows 32 tokens per condition; the pinned script's
actual output is 64 tokens per condition.

Pinned reference reproduction (old → new):

| condition | p(8) old | p(8) new | p(expected) old | p(expected) new | top old | top new |
|---|---|---|---|---|---|---|
| spider_clean | 0.882568 | 0.882568 | — | — | 8 | 8 |
| dog_C0 | 0.882568 | 0.882568 | 0.056421 | 0.056421 | 8 | 8 |
| dog_C1 | 0.846871 | 0.845521 | 0.089260 | 0.089117 | 8 | 8 |
| dog_C4 | 0.297255 | 0.316969 | 0.490091 | 0.461188 | 4 | 4 |
| ant_C4 | 0.379388 | 0.382575 | 0.487144 | 0.491236 | 6 | 6 |

All 64-token generations byte-identical to the pinned run (spider_clean and
spider_dog_C4 verified equal). Clean and C0 exact; C1 agrees to ~1e-3; C4 drifts up
to 0.03 abs on dog_C4, exceeding the spec's declared 1e-3. The drift grows with C
(C1 1e-3 → C4 0.03), consistent with perturbation-amplified bf16 numerics at the
largest dose, not with code drift; the replacement/subspace core files did change
between v0.1.1-59 and v0.1.1-353 (b80c238, bbb83bc, …), so a small code-drift
contribution cannot be excluded. Honest verdict: the qualitative positive reference
(top token 4, byte-identical continuation, 21/256 → 18/256 matched-random below
dog percentile 0.90) reproduces on current code; the quantitative dog_C4
probabilities reproduce only to ~0.03, and my 1e-3 tolerance was set without a
scale — corrected expectation: exact for clean/C0, ~1e-3 at C1, ~0.03 at C4.

## ml-debug form for the control run

| row | answer |
|---|---|
| log length; config as logged | tiny: 6 stdout lines each dtype; 4B: 7 lines (pueue 1272). Config in each `result.json`: layer 26 (4B), rank 256, C=8, positions=3, n=6, git v0.1.1-554-g820e2a7-dirty. |
| SHOULD vs observed | SHOULD: cached decode must actually run and the intervention must be nonzero — observed decode_steps=5 asserted, recorded perturbation_norm > 0, first-token shift 17.1 vs null 0.125. SHOULD: uncached reference must edit prompt-last3 AND all generated positions — asserted `prefill_positions == range(c_end-3, c_end+n)`. |
| null for every cited number | tol_rel and first-shift threshold are calibrated in-run by the clean no-hook cached-vs-recompute null on the same model/step (4B null: rel 0.06–0.12, abs step-0 0.125). No threshold was set without that scale. |
| init/demo | Identity control is the zero-edit demo: rel 0.00, logits bitwise-equal on 4B; different-position donor control applies edit 80.06 (hook fires). |
| dummy | C0 (zero-strength) is the dummy: bitwise logits equality. |
| baseline comparison | Pinned reference IS the baseline comparison (table above). |
| schedule | Not applicable: inference only. |
| full sample viewed | 4B control generation text is `(//)( (` — garbage by design (random rank-256 basis at C=8); semantics are covered by the pinned reference, not this control. |
| worst step | 1290 decode-5 hidden (1.004x tol, FAILED — preserved); 1291 first-shift (1.25x null, FAILED — intervention undetectable at L1/rank4). |
| surprises | (1) My first reference build anchored the extended mask at `content_end-1`, silently editing n extra PROMPT positions instead of generated ones; fp32 equivalence caught it at step 0 (rel 0.167). (2) My first C0 harness bug ran C0 at strength 1.5; the bitwise assertion caught it. Both were my bugs, both caught by the controls they were testing. (3) 4B random-basis C=1.5 moves logits only 2× the null — rank/C raised for the 4B control. |
| missing trust evidence | Logit control at 1289 (0.153) exceeds null (0.124) — passes only the fixed 2x-null criterion. L1/L26 random-basis controls only; no trajectory-basis/bank integration. Multi-layer interval hooks untested. Sequential full read of pueue 1230/1254 logs still not done (supervisor side). No independent fresh-eyes reviewer has read the rewritten control yet. |
| diagnoses with % | Placement/cache bug as the cause of early repetition: now unlikely (~15%) for single-layer L26 mechanics — fp32 exact, corrected bf16 hidden control (0.142) below its null (0.169), probes discriminate; this is a hypothesis-bearing observation, not proof. 1290 decode-5 hidden marginal failure: HYPOTHESIS numerics-floor (~70%, untested by a precision intervention). 1291: L1/rank4 intervention is too weak to test at all (shift 1.25x null). Multi-layer interval hooks carry residual untested risk. |
| fresh subagent | Not run — worker is not permitted to spawn (spawn budget 0); requested for supervisor integration. |
| cheapest next discriminator | ONE diagnostic, supervisor's choice: (a) 4B L1 with rank 256/C8 to make the h1 intervention testable above the null, or (b) 4B L26 replay in fp32 for a zero-null equivalence reference. Multi-layer intervals deprioritized per supervisor. |
| wall-clock | 4B control ~65 s including load; pinned reference 154.8 s; tiny CPU ~30 s per dtype. |

## Boundary

No scientific sweep run or claimed. Production sweep code untouched this session
except the `runtime_controls.py` rewrite. Main README/notebook untouched.
-- PI[glm-5p3-flash]

## Addendum: ACTUAL trajectory-built spec diagnostic (supervisor-directed, 2026-09-13)

One exact row: task-1230 condition `v25imported_h1_C1.5` (common-basis-earlyloc),
run through the REAL `run_with_bundle` construction with an observing spy capturing
the actually-built common_specs (no rederivation), then the corrected
cached-vs-uncached teacher-forced comparison reusing those specs.

Blocker found and fixed first: commit cc25c2b's complete_edit_bases refactor DELETED
the joint-support construction for non-complete arms — `rem_cols = ... else Pu`
crashed on undefined `Pu` at HEAD. Every `common_removal="joint"` k8-family condition
(including the user's h1 row) was unrunnable at HEAD. Pu restored verbatim from
cc25c2b^ (unit check: rank 16 from two rank-8 bases, containment 6e-7).

Actual captured spec (quoted from result.json):

> actual_basis_rank: 16 (NOT k8 — the built earlyloc h1 spec is rank 16; flags:
> selector increment, removal joint, anchor layer 25, detector layers 23/25/32)
> prefill: residual norm 3.9, applied edit 12.48, relative perturbation by position
> 2.814 / 4.217 / 2.409; decode: applied 5.45 per step, injection 3.6, span 0.1

Results (fp32 CPU after bf16-GPU OOM, task 1295):

> ACTUAL-SPEC CONTROL PASS (n=6, decode_steps=5): logit rel max 2.19e-05 (null
> 1.53e-05), hidden rel max 4.27e-05 (null 3.16e-05), argmax 6/6, first-token shift
> 1.40e+01; C0 with actual spec: bitwise OK

The same comparison in bf16 on GPU (task 1293) FAILED the hidden check (0.510 vs
0.397 tol = 2x null; logits within bounds): with the edit at 2.4-4.2x the residual
norm, bf16 cache-vs-recompute divergence exceeds the no-hook null — the fp32 run
localizes this to rounding amplification, not placement. Evidence chain: fp32 tiny
exact → fp32 4B actual-spec exact → bf16 4B amplified.

Production row reproduction: the diagnostic's own production run gives
`swap_log_odds_shift +3.891` IDENTICAL to the historical 1230 row; p_valid 0.0000 =
0.0000; r2 0.0001 = 0.0001; the second r2 differs 0.968 (diag) vs 0.965
(historical) — one bigram-level difference, cross-code-version (Pu restore between).

Scope note: this joins BANK CONSTRUCTION to the hook/cache path (actual trajectory
basis, actual donor vector) at sites {L1}; random-basis controls (1289-1291) remain
separately labeled. Multi-layer interval hooks still untested. HYPOTHESIS standing:
bf16 + huge-norm edits are the noise floor for any bf16-sweep interpretation;
not a conclusion about the repetition mechanism. -- PI[glm-5p3-flash]

## Corrections (supervisor review of the addendum, 2026-09-13)

1. **Row identity**: condition index 0 of common-basis-earlyloc is the NAME-dog row
   (the pDog/pSpider table row: 'Which animal is known for spinning webs to catch
   insects... called'), NOT the legs-dog row. The diagnostic exercised the name-dog
   pair; labels corrected in the script and here.
2. **Rank 16 is the JOINT rank of 8+8**, not a "not-k8" anomaly: the built h1 spec's
   basis is the joint support of the top8 source and top8 donor bases.
3. **dtype/device confound**: the fp32 run changed DEVICE (GPU→CPU) AND rebuilt
   bank/bases separately. The earlier "localized to rounding amplification" claim is
   withdrawn; the supported claim is narrower: the same-spec cached-vs-uncached
   internal check passes on CPU fp32; bf16-vs-fp32 row differences cannot be assigned
   to dtype alone.
4. **Row reproduction, by dtype (separately labeled)**: bf16/GPU historical
   `swap_log_odds_shift` +3.891 vs fp32/CPU rebuilt +4.987 — a 1.1-nat difference
   across dtype+device+basis rebuild, reported as separate rows, not one.
5. **Repetition persists in fp32** (verified from saved token IDs): fp32 name-dog h1
   continuation is 32 tokens `'::::::::::::::::::::::::::,:,,,\n'` (token 25 repeated,
   r2 0.839); the bf16/GPU historical row is the same colon-degenerate continuation
   (88 tokens of ':'). Inference (strong, pending full-text read which these token-ID
   dumps ARE): bf16 cache mismatch alone cannot explain this row's repetition.
6. **Effective tolerance floor**: printed "2x null" was a false label in fp32 — the
   1e-3 floor dominates (null ~1.5e-5). The script now logs the effective floor
   explicitly; no tuning.
7. **Failure exit code**: the script caught AssertionError and exited 0; fixed —
   re-raises after saving, so the queue shows FAILED. First-divergence save now
   captures the ACTUAL failing check's step/tensors (hidden failures save the failing
   decode step's hidden pair; logit failures the failing step's logits; step defaults
   removed).
8. **Probes**: the actual-spec script contains NO wrong-mask/no-hook probes; earlier
   audit wording claiming probes for the actual-spec run is retracted — probes are
   implemented in the random-basis control (runtime_controls.py) only.
9. **Regression added**: tests/test_joint_support.py (3 passed) — the restored
   joint_support path (rank/orthonormality/containment) plus the complete-mode Pj
   selection; the cc25c2b break is exactly the missing-old-path-test failure mode.

## Smallest actual scientific next step (PROPOSED, not queued)

Restore the user's actual goal with the verified production mutation: run the
LEGS-dog pair (not name-dog) with the genuine full-supported complete-edit candidate
through the production function — one row, exact production construction, mutated by
the verified `joint_support`/complete path, swap/p_valid/r2 + per-step norms + exact
strings per the AGENTS causal-demo layout. NOT a dose-ladder default, NOT random
basis, NOT multi-layer expansion. Awaiting supervisor go.

-- PI[glm-5p3-flash]
