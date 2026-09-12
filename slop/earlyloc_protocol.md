# Resolved protocol: direct early-location comparison + the next rank algebra (saved before implementation)

2026-09-12, PI[glm-5p3-flash]. User: "test my ideas properly" (AFK, proceed autonomously in
scope). Supervisor queue-review before GPU.

## Part 1: early-location comparison (increment selector, temporal top8, anchor 25)

Frozen: increment trajectory selector; temporal top8 per prompt; joint removal (v
contained asserted); donor anchor h25 FIXED (frozen at decode offset-1); C=1.5; last-3
prefill + every decode; the exact original 12 dev questions + wrappers; the exact-input
bank for preflight. Selection is from LATE trajectory windows — NOT fitted at the
intervention site.

DECLARED CONDITION LIST (12 conditions × 12 questions = 144 cells, one model load):

| # | condition | site | injected vector | purpose |
|---|---|---|---|---|
| 1-4 | imported-v25@h1/h2/h3/h8 | h1/h2/h3/h8 | Pd d25 (the late-built component imported) | the SITE axis (one-at-a-time) |
| 5-7 | site-rescaled@h1/h2/h3 | h1/h2/h3 | v_site direction rescaled to ‖v25_o‖ | SIZE controls (import vs mere upscaling) |
| 8 | v8-replay@h8 | h8 | Pd d8 | baseline verification vs 1194/1208 |
| 9-12 | C0@h1/h2/h3/h8 | h1/h2/h3/h8 | none (identity) | zero-strength per tested site |

h8 references: 1194's v25-imported/v8-rescaled/v8-replay arms (hash/text equality required
before interpreting differences). Success = correct facts + persistent identity +
coherence; off-target/false facts/repetition counted separately; a wrong fact with spider
identity is an EFFECT (not "inert"). Actual normalized edit sizes measured per condition.

## Part 2: the next comparison's exact algebra (CORRECTED per supervisor: complete-edit
## narrowing = BOTH source and donor temporal bases truncated)

At ONE predeclared fixed early site (h1 — predeclared, not chosen per rank):

    U_s^k, U_d^k = the FULL supported source/donor temporal SVD bases truncated at
                   k in {1, 2, 4, 8, full}   # 'full' = the actual support (not 8)
    P_joint(k) = support-filtered span([U_s^k | U_d^k])  # BOTH sides narrow
    v_k = U_d^k (U_d^kᵀ d25)
    h' = h + C(v_k − P_joint(k) h)                       # C = 1.5 fixed

'k' = the PER-SIDE TEMPORAL rank (the actual joint rank measured per cell, not total rank
k). Both the removal and the injection narrow together; containment holds (v_k in the
joint span). k8-at-h1 REPLAYS the earlyloc imported-h1 arm (not 1194's h8). This is a
complete-edit content/size comparison — no isolated-rank causality claim. NOT queued.

## Checks (real-path, before queue)

- h8 baseline: hashes/texts vs 1194 (v8-replay) and 1208 (imported arm) — verify BEFORE
  interpreting differences.
- Runtime vector/projector algebra asserts (containment, rescale cos/norm) — in-run.
- EOS-aware outputs; per-row paired verdicts; spec contracts (expected_strength/condition/
  selector/site/anchor) validated pre-model; tiny dispatch smoke with the actual path.
