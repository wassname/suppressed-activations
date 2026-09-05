# Pre-run scientific and code review

## Review

### Correct

- **Residual-layer indexing is internally consistent.** `trajectory()` replaces the post-final-norm hidden state with the final norm’s raw input (`scripts/confirm_causal_demo.py:60-70`), yielding residual indices where index 26 is residual L26. The intervention reads `residuals[26]` and hooks decoder block 25’s output (`scripts/confirm_causal_demo.py:228-233`), which is the same residual stream location. Extraction at L23/L25/L32 is performed through indexed residuals (`scripts/confirm_causal_demo.py:80-86`, `suppressed_activation_subspace.py:21`).

- **Tensor shapes align.** Extraction supplies `[1, layers, d]`; the returned basis is reduced to `[d, 8]`; source and target states are `[d]`; and the hook reshapes the patch to `[1, 1, d]` (`scripts/confirm_causal_demo.py:80-90`, `scripts/confirm_causal_demo.py:178-183`, `suppressed_activation_subspace.py:37-42`). This is coherent for the fixed batch size of one.

- **Fixed-condition integrity is preserved.** Model revision, prompts, extraction layers, rank, L26 intervention, C4 dose, and final-token primary site are constants and recorded in metadata (`scripts/confirm_causal_demo.py:22-44`, `scripts/confirm_causal_demo.py:348-365`). There is no fallback or adaptive candidate selection.

- **Controls address the stated alternatives.**
  - C0 and C1 are evaluated alongside C4 (`scripts/confirm_causal_demo.py:386-397`).
  - Penultimate-token C4 uses the corresponding penultimate source residual and hook position (`scripts/confirm_causal_demo.py:228`, `scripts/confirm_causal_demo.py:399-400`).
  - Byte-source C4 re-extracts the byte source state and basis (`scripts/confirm_causal_demo.py:402-403`).
  - Arithmetic 6/4 targets test answer-only transfer (`scripts/confirm_causal_demo.py:406-409`).
  - Targeted and forced-first-token generations retain exact token IDs, permitting after-first-token comparison (`scripts/confirm_causal_demo.py:439-488`, `scripts/confirm_causal_demo.py:514`).

- **The random-control construction matches each primary C4 patch’s FP32 chord distance and residual norm.** The primary perturbation norm is taken from the completed norm-restored patch (`scripts/confirm_causal_demo.py:156-165`, `scripts/confirm_causal_demo.py:416-423`). `matched_random_rotation()` constructs a tangent-sphere rotation and asserts both norm and chord distance (`suppressed_activation_subspace.py:99-112`). Separate Ant and Dog distances are used.

- **Successful-run artifacts are substantially complete.** `result.json` contains prompts/tokenizations, selected vocabulary rows, every condition, all 256×2 random-control metrics and seeds, summaries, and generation token IDs/text (`scripts/confirm_causal_demo.py:491-519`). The rendered log includes primary effects, controls, random percentiles, and continuations.

### Findings

- **P1 — “Exact 64-token” generation is not guaranteed and can abort the entire run after all expensive computation.**  
  The prediction requires continuation comparison (`slop/research/20260905_l26c4_confirmation_predictions.md:23`), while the report labels these “Exact 64-token continuations.” However, `max_new_tokens=64` and `max_new_tokens=63` are only upper bounds, and EOS remains active through `pad_token_id=tokenizer.eos_token_id` (`scripts/confirm_causal_demo.py:194-220`). Any one of the 14 generations may stop early. The subsequent assertion (`scripts/confirm_causal_demo.py:489`) then fails before completed metadata, `result.json`, or the final log are written (`scripts/confirm_causal_demo.py:495-519`).  
  **Smallest fix:** set `min_new_tokens=MAX_NEW_TOKENS` in `generate()` and `min_new_tokens=MAX_NEW_TOKENS - 1` in `forced_generation()`, while retaining the assertion.

- **P2 — Distance matching is asserted before, not after, the actual BF16 intervention cast.**  
  Primary geometry and random rotations are calculated in FP32 (`scripts/confirm_causal_demo.py:156-172`, `scripts/confirm_causal_demo.py:418-423`), but every inserted patch is converted to the model hidden-state dtype in the hook (`scripts/confirm_causal_demo.py:182`). Consequently, the asserted FP32 chord distances in `suppressed_activation_subspace.py:109-112` are not necessarily the exact distances applied by the BF16 model, and realized distances are neither checked nor recorded. The discrepancy should be small, but “distance-matched” is currently exact only in pre-cast geometry.  
  **Smallest fix:** compute and store the primary and per-random realized perturbation norms after conversion to the hook dtype, and assert/report an explicit matching tolerance.

### Residual risks

- Runtime was not executed, so compatibility of the pinned model’s architecture/API and actual EOS behavior remains unverified.
- Verification was intentionally restricted to the three requested files; the pinned model implementation and prior results were not consulted.

### Merge verdict: **BLOCK**

Fix exact-length generation before the confirmation run. The BF16 realized-distance issue is a reportable precision caveat rather than a primary scientific blocker.