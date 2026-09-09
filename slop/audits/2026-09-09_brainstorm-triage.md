# Brainstorm triage vs code + selected comparison (2026-09-09, PI/OpenAI)

Both r2 reviews read in full (kimi M1–M6, glm M1–M6, neither picks a winner).
Code checks below are against HEAD a49e4cf (hashes in `2026-09-09_runner-code-sha256.txt`).

## Code verdicts on reviewer sub-claims

- Hook off-by-one (kimi partial-review suspicion): RESOLVED, no bug. `demo.py layer_hooks`
  registers on `blocks[layer]`; `hook_for` reads `target_residuals[block+1]`, which matches
  `trajectory()` residual indexing (hidden_states[l] = post-block-(l-1)). Consistent.
- Decode coverage (glm M3 core): CONFIRMED. `active_positions = 1 if hidden.shape[1] == 1`,
  so cached decode patches only the newest token; prefill patches last 3. All decode-step
  records (N-1 steps) check out; this part of M3 stands.
- Position hardcoding (glm M3 sub-question): RESOLVED, positions computed per tokenization.
  CPU audit (`slop/research/2026-09-09_position_audit.py`, project tokenizer, exact prompt
  builder) reproduces recorded spans exactly: legs [42,43,44], naming [40,41,42].
- Patched-token identity: patched prefill tokens decode to `['Answer', ':', ' ']` in ALL FOUR
  fixed conditions. Identical final token IDs rule out a different lexical edit span only —
  not context-dependent representation at those positions, nor source/donor alignment. So
  lexical-span misalignment is out for the fixed runs; representation/alignment variants of
  M3 plus decode-only-1-token and premise-conflict (M5) remain live.
- E form (glm M1): approximately right, exact form differs. `oat_sweep.attenuation_basis`
  uses `cross_position_covariance(peakJ) - cross_position_covariance(outputJ)` (Gram/len when
  tokens=None), not raw Gram difference. Sign-flip variant = bottom eigenvectors; feasible.
- Dual-basis feasibility (kimi M1): BETTER than stated. Original vocab detector still in code
  (`suppressed_activation_scores` = centered min(relu(rise), relu(fall))) AND exposed as
  existing sweep `template_detector_configs` (early/peak/late × matched). No reimplementation
  needed; needs template forward passes (GPU, no generation for the angle check itself).
- Random-norm control: documented design (`matched_random_rotation` matches residual norm AND
  perturbation distance with assert_close). Not a bug. Its weakness is semantic, shown below.

## CPU check B: string semantics separates selected from random perfectly (done)

16 recorded matched-random rows (`out/2026-09-08_134200_matched-random-band-{dog,ant}`):
both selected rows donor-words True + spider False (2/2); ALL 16 random rows donor-words
False + spider True (0/16) — while digit S_swap does NOT separate (dog seeds 2/3/6 beat
selected +4.375 yet describe spiders; dog seeds 002/003/006 emit '4.' first, then spider).
Ant seed007 loops under a RANDOM span: correction attractors are not unique to selected
edits. Crude substring scorer only — preliminary string signal, not semantic validation.

## Selected construction comparison (GPU-gated, PREPARED not queued)

**`--sweep template-detector --condition-index 2` on both fixed naming prompts**
(launchers `2026-09-09_detector-c2-{dog,ant}-name.sh`, prompt argv byte-verified).
Condition 2 = `D8_20_32_matchedFalse`: original vocab-rise-and-fall detector, fixed-delta
operation at single layer L20, strength 2.0, match_component_norm False.
One justified common default: window (8,20,32) preserves the peak-20 and output-32 anchors
of the successful local-dog edit while changing selector family; matchedFalse mirrors the
failing band's norm rule so transfer cannot be attributed to norm matching.
Explicit differences vs the failing band construction (NOT an isolated basis test):
selector family (vocab detector vs contrast-energy attenuation), operation (fixed-delta vs
synchronized shared replacement), edit layers (L20 alone vs L22/23/24), windows/anchors.
Same: template_contrast, persistent_rank 4, strength 2.0, prompts/wrapper, continuous steer.
Asymmetric interpretation: coherent transfer motivates isolating the responsible difference
next; looping/correction does NOT establish M3/M5 and does NOT rule out selector problems.

Predeclared full-continuation rubric (judge meaning, not first digit): Transfer = donor
animal stays the described subject through sentence 3 with no spider-identity claim and no
wait/incorrect/mistake/restart loop phrases. Partial = donor first token but spider body,
or donor body with a factual defect (quote defect verbatim, e.g. leg-count errors).
Fail = spider throughout or loop. Factual check on all identity/property claims.

## Prepared while GPU unavailable (no runner edits)

- CPU audit script + string scorer above (rerunnable; evidence, not verdict).
- Queued historical repro 862/863 (verified launchers) must run first on the frozen runner.
- Sign-flip-E and descriptor-span variants need small code additions: explicitly DEFERRED
  until after repro results, to preserve the frozen-runner comparison.
