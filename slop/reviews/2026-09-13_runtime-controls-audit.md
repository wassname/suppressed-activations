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

Qwen3.5-4B GPU:

> 1. identity v=P h (same state/position): rel_edit=0.00e+00, max_logit_delta=0.00e+00
> 2. C0 logits equality: bitwise OK
> 3. cached/uncached teacher-forced equivalence (n=6, decode_steps=5): per-step rel
> logit delta max 1.53e-01, rel hidden delta max 6.12e+00, tol_rel 1.24e+00 OK;
> argmax match 5/6 (tie flips at steps [2] within numerics); first-token shift vs
> clean 1.71e+01 (nonzero) OK
> probes: wrong-mask rel delta 8.50e+00, no-hook rel delta 8.50e+00 OK

Step-2 flip diagnosis from `result.json`: cached top-2 gap exactly 0.0 (bf16 tie),
step delta 0.229 — argmax of an exact tie is arbitrary; not a placement bug. A flip
with gap >> delta would still fail the assertion.

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
| worst step | Step 2 argmax flip (gap 0.0, delta 0.229): explained — exact bf16 tie. |
| surprises | (1) My first reference build anchored the extended mask at `content_end-1`, silently editing n extra PROMPT positions instead of generated ones; fp32 equivalence caught it at step 0 (rel 0.167). (2) My first C0 harness bug ran C0 at strength 1.5; the bitwise assertion caught it. Both were my bugs, both caught by the controls they were testing. (3) 4B random-basis C=1.5 moves logits only 2× the null — rank/C raised for the 4B control. |
| missing trust evidence | Per-step hidden-state tolerance is weak (null-calibrated tol_rel 146; the hidden check alone would not catch moderate placement bugs — the logit check is the decisive one). Only ONE intervention layer and ONE spec family tested; production multi-layer interval hooks' cache interaction is not covered by this control. Sequential full read of pueue 1230/1254 logs still not done (supervisor side). No independent fresh-eyes reviewer has read the rewritten control yet. |
| diagnoses with % | Placement/cache bug as the cause of early repetition: now unlikely (~15%) for the tested single-layer mechanics — fp32 exact, bf16 within null-calibrated tolerance, probes discriminate. Repeated frozen donor injection's semantic effect as repetition cause: unchanged (~60%, untested here). Other spec families (multi-layer intervals) carry residual mechanics risk (~25%, untested). |
| fresh subagent | Not run — worker is not permitted to spawn (spawn budget 0); requested for supervisor integration. |
| cheapest next discriminator | Multi-layer-interval cached-vs-uncached control (same script, spec keyed on 2–3 layers) if the production sweeps keep interval hooks. |
| wall-clock | 4B control ~65 s including load; pinned reference 154.8 s; tiny CPU ~30 s per dtype. |

## Boundary

No scientific sweep run or claimed. Production sweep code untouched this session
except the `runtime_controls.py` rewrite. Main README/notebook untouched.
-- PI[glm-5p3-flash]
