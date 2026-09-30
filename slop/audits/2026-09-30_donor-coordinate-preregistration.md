# Preregistered donor coordinate prerequisite

— PI/OpenAI

Question: does subtracting the known direct token embedding make the existing generic donor midpoint usable across eight new matched contexts? No generation, editing, refit, threshold search or layer/position search. The existing inference entry point owns the implementation and logging; there is no separate production probe pipeline.

Reference: recovered advisor `61585f07-53c2-4f3c-a54a-ef321b20e4f0`, `slop/reviews/2026-09-30_reflection-result-review.md`. Its conclusion is limited: “This rejects the frozen center on these contexts, not the direction.” Same-family advice, not goal sign-off. Installed Qwen uses unscaled input embeddings and additive residual connections; removing that direct contribution does not remove context-dependent token effects.

The frozen data are `data/donor_coordinate_validation_v1.json`: explicit/indirect referents crossed with four endings, eight pairs/16 prefills. Exact strings are in that file; the third ending deliberately retains its trailing space. Indirect referents have different token lengths, which remain a confound for interpreting a positive result. Labels score the states; none fit the coordinate. The same paired final token makes its embedding correction identical for dog and spider.

```text
u = unit(mean_spider - mean_dog)
c = (mean_spider + mean_dog) / 2
raw = (h - c) @ u
candidate = raw + (embedding_It - embedding_current) @ u
```

One new candidate; raw is the unchanged control. No parameters are learned. “Current” is the processed input token, not a future prediction. For a later causal test only, the residual displacement would be `-2*min(candidate,0)*u`, not subtraction of the embedding from the residual itself. This prerequisite computes coordinates only.

| option | predicted diagnostic | decision |
|---|---|---|
| raw midpoint | reproduces token1049 identity and exposes context shift | control, no unchanged causal rerun |
| embedding subtraction | may improve source<0<target; pair ordering must be unchanged | test this single candidate |
| different direction/position/preparation | could repair ordering or contextual effects | deferred; no retrospective selection |

Predictions and scale:
- SHOULD: pair differences are unchanged, within2e-5 numerical tolerance; any discrepancy is an implementation/matching failure. CPU seeds0/1 already passed this algebra.
- SHOULD: on current token1049, raw/candidate margins are exactly equal; its embedding difference is identically zero.
- TODO validate: candidate dog<0<spider for all8 pairs. The 8/8 prerequisite is a prospectively chosen engineering requirement, not a significance threshold derived from a random-null distribution. Random-null rate is unmeasured; no statistical superiority claim follows.
- Generic donor endpoints are±.715169; previous question margins were positive for both species. Zero is the midpoint definition, not a newly selected numerical cutoff.
- Direct-embedding offset contributes materially: plausible (~50%); predicts shared shifts toward correct bracketing for non-It endings but no change in ordering. Contextual residual mismatch persists: plausible (~70%); predicts continued sign failures despite exact subtraction. These hypotheses overlap.
- Ordering fails on implicit referents: plausible (~35%); then embedding subtraction cannot repair it. A token/position/axis implementation defect: remote (~5%); exact paired-difference and reference-token checks, raw tensor replay and CPU smoke address it. Unknown causes remain possible (~10%). These are judgments, not measured frequencies.

Decision fixed before inference: only8/8 corrected brackets permits one corrected-reflection test on both causal properties, with unchanged layer16, final-position prefill, continuous unit-strength updates and Base/raw/corrected/random comparisons. Any failure blocks that candidate's causal run. Ordering failure versus ordering-without-bracketing distinguishes direction/context from centering; it does not select a new center. Earlier positions are saved for diagnosis but cannot become a retrospectively selected primary result.

Implementation/tests: `scripts/english/08_jlens_one_pass.py --validate-donor-coordinates-json data/donor_coordinate_validation_v1.json`. Existing model loading, revision pins and `layer_hooks` are reused; branch returns before lens loading, standalone readouts and interventions. Save all-position raw residual16 and embedding tensors, exact token IDs/strings, coordinate tensors, complete JSONL samples and source hashes. CPU algebra directly loads the production helper; real tiny hybrid-Qwen smoke exercises the validation function, pinned tokenizer, all16 prefills, I/O, independent float64 reconstruction and hook cleanup. Synthetic smoke numbers are not scientific results.

Three ways a positive result could mislead: surface-name discrimination rather than hidden concept transfer (explicit/indirect split); prompt length/wording confounds (recorded lengths, no causal interpretation); coordinate separation without causal sufficiency (require subsequent same-method8/outside and coherent continuations). Passing this prerequisite does not complete either user goal.

Budget: existing local GPU default queue only, one job,300s cap excluding wait,16 prefills and0 generated tokens. Peak inference memory and elapsed time are logged. No optimizer, learning-rate schedule, loss or gradients apply. Full post-run ml-debug form belongs with the measured result; unobserved results are not filled from expectation.

Smoke development: first tiny-model run executed16 prefills, then failed while rendering `run.md` because the test put its output under `/tmp`, outside the production function's project-relative output contract. Exact failure: `ValueError: '/tmp/donor-smoke-it603cxr/run.md' is not in the subpath of '/workspace/2026/suppressed-activations'`. Saved first-failure log. Corrected the test fixture to use a temporary `.local/` directory; production output semantics and coordinate code were unchanged. Rerun covers seeds0/1. Process proc_88d8 exited0 after58s; log line252 says `PASS tiny hybrid Qwen seed=0: 16 real prefills, no generation, full I/O, independent float64 projection and hook cleanup`; line504 repeats this for seed1. Production helper algebra also passes both seeds. AST comparison confirms all pre-existing helpers remain unchanged; only main dispatch/logging and the two new validation helpers changed. These random-model fixtures are runtime tests, not a calibrated scientific null.
