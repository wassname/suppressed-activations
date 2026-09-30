# Cached positive token-KL readout comparison

-- PI/OpenAI

Purpose: test hidden-not-said readout, not another geometric prerequisite. Settled advisor/supervisor contract: `slop/reviews/2026-09-30_after-projection-next-test.md`.

One score, no tuned strength: normalize intermediate/final logits over the entire vocabulary, then rank positive contributions p_R*max(log(p_R)-log(p_F),0). Compute their logs to avoid underflow. Ineligible tokens get minus infinity; stable descending sort breaks ties by token ID. Unchanged prompt/greedy1 masks, residual24 J versus plain24/27, k32. Half-erasure and probability-excess remain separate controls, not combined terms.

Only data: all8 cached v4 cases from `out/2026-09-30_142814_jlens-one-pass`. They are development data, already examined. Zero transformer forwards, generations or calibration; model and backbone guards reject a forward. No generated text/labels enter ranking. Existing aliases and actual-output scoring remain unchanged; two ineligible AUROC labels tie at.5. Retain unscoreable cases and wrong baseline answers.

Matched and cyclic-next-case final distributions for each representation use CURRENT-case masks. Save components for selected and scored tokens, masks, eligibility/ties, actual top32, alias joint recovery/AUROC and denominator. Diagnostic signed/excess ranks count strictly greater scores; new-method membership uses stable finite top32, not those optimistic ranks.

Selection fixed before replay: maximum alias-checked joint count; ties plain27 > J24 > plain24. Numeric screen requires at least7/8 and strictly exceeds its own mismatched control. Incumbent halfplain27 must reproduce6/8. A screen pass is not success: symmetric blinded semantic review must find no definite input/said leak among its counted passes before freezing for new examples. Do not switch to another winner after failed semantic review. Ceiling/all3 perfect or matched-near-mismatched needs comparator diagnosis, not a subtraction-benefit claim.

Options: signed contrast alone has already scored0/8; rare-token denominator effects were visible. This score weights surprise by intermediate probability. A reference sparse-decomposition/clamp reproduction would require unresolved dictionary/clamp/normalization choices, so it is deferred rather than silently approximated. No new centering/rank/dose work on the rejected donor candidate.

Pre-run predictions (nonexclusive rough bets):
- Probability weighting reduces rare-token dominance (~75%): fewer selected J tokens below p_J=1e-5 than signed contrast, especially Hamlet (previously29/32). This alone is not recovery.
- A representation reaches the7/8 numeric screen (~25%): plausible but multi-token spoken content remains a major obstacle.
- Remaining input/said alias leaks (~75%): inspect all tokens against exact inputs/generations, not just the literal score.
- Comparator dependence is weak (~35%): matched and mismatched results are similar; then do not infer final-state contrast is doing the work.
- Implementation fault (~5%): old readouts change, self-comparison yields finite candidates, normalization follows masking, or a transformer call is attempted. Unknown causes remain (~10%).

SHOULD: replayed generations and old methods exactly match saved controls; self-comparison has no eligible tokens; logs expose tiny-p_Q promotion rather than calling it automatically useful. TODO validate: improve joint hidden recovery/said exclusion, not just remove rare fragments.

CPU production-helper/comparison-loop checks pass seeds0/1: direct positive-contribution equivalence, eligibility/masks, identical transforms on all3 representations and mismatches, old-score and label/text invariance, additive-logit invariance, self-zero, underflow-safe ranking, stable ties, fewer than32 eligible entries and AUROC ineligible tie=.5. The production rejection callback blocks a model forward. These are scorer/guard tests, not a full transformer smoke; full replay still needs numerical and old-row comparison afterwards.

Cost: one default-lane local job, outer `timeout --signal=TERM --kill-after=15s 300`, imports included. Immutable main, launcher and v4 config copied from the committed source. No repeat/configuration search within this attempt. Both goals remain open; no README/publication change.
