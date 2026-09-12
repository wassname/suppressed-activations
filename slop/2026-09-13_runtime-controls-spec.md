# Spec: genuine cached-vs-uncached runtime control (rewrite of scripts/runtime_controls.py section 3)

Author: PI/glm-5p3-flash. Replaces the vacuous section 3 confirmed in
`slop/reviews/2026-09-13_full-ml-debug.md` follow-up: the old check called
`generate_with_first_logits` with EMPTY hooks and `max_new_tokens=1` (no cached decode
occurred) and asserted only the first token, while computing `res1/logits1` and never
using them. The docstring also claimed a "positive pinned reference" that was not
implemented. Both false claims are removed.

## What the new controls must prove

1. **Identity (zero-delta):** with `common_replace`, `v = P_s h` taken from the SAME
   state, SAME position, SAME layer, the production hook's net edit
   `C (P_d d − P_s h)` is exactly zero: logits bitwise/allclose equal AND recorded
   `perturbation_norm == 0`. A donor state from a DIFFERENT position of the same prompt
   is NOT identity and must produce a nonzero delta and changed logits (hook-fires
   control, so the identity assertion cannot pass vacuously through a missing hook).
2. **C0 equality:** strength 0 leaves logits bitwise unchanged (kept from the old script).
3. **Cached vs uncached teacher-forced equivalence over prefill + >=3 cached decode
   steps, with a REAL nonzero intervention:**
   - Cached path: production `generate_with_first_logits` with production
     `intervention_hooks` (`common_replace`, `positions=3`, per-position prefill specs,
     frozen `decode_src`/`decode_proj`), donor states end-aligned from a different
     (donor) prompt, strength 1.5. Assert `record[fall]["decode_steps"] >= 3` (cached
     decode actually happened) and recorded `perturbation_norm > 0`.
   - Uncached reference: one teacher-forced full-history forward (`use_cache=False`)
     over prompt + the cached run's own generated tokens. The edit mask MUST be the
     last-3 ORIGINAL prompt positions AND ALL generated positions at the same hook
     layer (contiguous slice `[content_end-3 : content_end+N]`), reusing the production
     hook through `positions=3+N, source_position=content_end-1` with per-position specs
     extended by the frozen decode spec — NOT merely the last 3 of the growing sequence.
   - Per-step comparison: cached `scores[j]` vs uncached logits row
     `content_end-1+j`, and cached decode-step final-norm inputs vs the uncached final
     residual at position `content_end-1+j`, for every step j. No sampling drift
     (greedy; the uncached path teacher-forces the cached tokens).
   - Tolerance: calibrated inside the run by a clean (no-hook) cached-vs-recompute
     measurement on the same model; the intervention comparison asserts
     `max_abs_delta <= max(1e-4, 10 x clean_delta)`. The measured clean delta and
     tolerance are printed and saved.
   - Discrimination probes (must FAIL = large delta if the mask or hook is wrong):
     (a) wrong-mask reference (edits only the last 3 of the growing history) must
     MISmatch the cached intervened run; (b) no-hook clean forward must MISmatch the
     cached intervened run. These make "wrong mask" and "missing hook mutation" fail
     loudly instead of passing an equivalence that cannot distinguish them.

## Models

- Tiny first, CPU: `wassname/qwen3-5lyr-tiny-random` (existing default).
- Then the actual pinned 4B integration on the default GPU via pueue:
  `Qwen/Qwen3.5-4B` with `SUPPRESSED_CONTROL_LAYER=26` (production L26), same controls.
  The tiny model does not exercise the real hybrid cache; only the 4B run covers it.

## Positive pinned reference (separate GPU job, exact existing path)

`scripts/confirm_causal_demo.py` in the MAIN worktree, unpinned inputs unchanged:
Qwen/Qwen3.5-4B rev `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`, spider source, dog
target, intervention layer 26, rank 8, strength 4.0, prefill-only single-position patch.
Verification target from the pinned source of truth
`out/2026-09-05_211609_causal-confirmation/result.json`: clean `p(8)=0.882568`;
dog_C4 `p(4)=0.490091`, `p(8)=0.297255`, top token `4`. Tolerance: exact re-execution
on the same GPU/torch is expected to be near-bitwise; accept abs diff <= 1e-3 on the
three probabilities and require top-token `4` in dog_C4. No random fallback, no new test
prompt, no substitution of a fresh demonstration.

## Boundaries

- No scientific rank/dose sweep. No new research claims. Runtime GPU controls only;
  unique output dirs, code hashes, full logs; existing pueue queue, `default` group.
- Evidence: full stdout saved under `.local/verify_logs/runtime-controls/`.
