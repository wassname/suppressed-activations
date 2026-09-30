# Offline naming gradients, fixed one-pass contrast addition

Written by PI/OpenAI before any pretrained preparation or evaluation for this proposal. Adopt `slop/reviews/2026-10-01_next-causal-attempt.md` exactly: eight generic naming forward/backward calls, then eight short generations. Readout2673 is independent and cannot select the vector or settings.

## Method and information boundary

Use the existing pinned Qwen3.5-4B and block15 output (residual16). For each of the four existing pronoun templates and both animals, append ` is called a`. Example: `The animal is a dog. It is called a`. Differentiate the final logit for ` spider` minus that for ` dog` with respect to the earlier ` It` activation. Token IDs/prefix alignment must be verified, not approximated by fragments. Model parameters are frozen; backward computation occurs only in this reusable offline stage, through the real model suffix and final normalization.

```python
g = mean(grad(z_spider - z_dog, h16_at_It) for context in eight_generic_contexts)
u = g / norm(g)
D = existing_mean_spider_at_It - existing_mean_dog_at_It
a = dot(D, u)
delta = a * u
h16_test_final_prompt += delta
h16_test_each_decode += 0.25 * delta
```

No learned model parameters or optimizer. Record every gradient, source activation, token sequence, two naming logits, gradient norm, coefficient and projection fraction. If a is nonpositive, preserve the preparation artifacts and fail before evaluation; no sign/dose rescue. The natural donor difference has prior measured norm1.430336. Projecting it sets residual-unit scale and bounds delta's norm by that value. This may be too small to change behavior; it is not a reason to silently restore the larger noun-donor norm.

Config `data/dog_spider_vjp_v1.json`, SHAa1b1431045979b7490500b882662b8bb368bc368ea98b3291f89a763c08117f9, pins templates and original natural pronoun donor checkpoint SHA572a99a9705f68e6dd6ffee87f6940a1b7bef3636527b66a1efec3fdf85744c5. The donor's historical rescaled evaluation is not its stored natural magnitude.

At evaluation: fixed vector only, final prompt position and all decode calls, block23 read-only observer. No naming suffix, gradient, preliminary current-input pass, Base feedback or later-layer feedback. This is contrast addition, not literal component replacement or an exact reproduction of the reference paper.

## Fixed eight conditions

- Existing dog leg prompt: Base, VJP addition, seed0 norm-matched random. Expected4 to8.
- Existing dog body-relative skeleton prompt: the same three conditions. Expectedinside tooutside.
- `Fact: An animal that barks is nearby. The sum of 2 and 2 is `: Base and identical VJP addition; both should answer4.

Exact property strings come from08's existing RELATIONS. One fixed random vector, same absolute requested norm and schedule across properties. Applied BF16 norms can differ; save before/requested/applied states at every call. All continuations greedy and capped at32, with actual EOS counts. No forced words or repetition processor. The old global-J comparisons remain historical context, not a matched superiority claim. No new dose/layer/coverage search. These are development animal/property cases, not unseen-pair rates.

Report target-answer movement/2 property attempts, exact continuation coherence, arithmetic preservation and readouts separately. One selected success is partial evidence with its denominator; a common two-property change plus intact arithmetic would support broader concept-level influence. A digit or animal name alone is insufficient. Do not interpret later NLI questions as affirmed facts. No universal-success requirement and no claim of uniquely isolated mediation.

## Options and predictions

| Option | Intended distinguishing observation | Decision |
|---|---|---|
| Context-specific offline gradients | Same vector affects property-appropriate answers, beyond name emission | One test |
| Another generic probe threshold | Separates generic contexts but may retain the old domain shift | Defer |
| More retired J/dose/coverage variations | Could repeat a selected flip without resolving common property influence | Do not reopen |

Planning weights from the advisor, not measurements:45% naming/readout movement without property transfer;25% negligible effect;15% useful cross-property transfer;10% implementation/casting/scoring error;5% other. Naming-only outputs favor the first explanation; unchanged answers with nonzero applied states favor weak/mismatched direction; malformed arithmetic indicates off-target damage. The actual behavior may not follow these categories.

SHOULD: frozen preparation is reused unchanged across properties, no evaluation backward calls, and random has the same requested norm. TODO validate: concept-specific derivatives transfer better than a generic naming bias. No predicted numerical success rate or statistical significance threshold is set from two dependent cases and one random seed.

## Checks already executed

At source8911bc887445d1d5fe8711e8f4a6664092cfb0610f5db2d0115484f190b7e2e9, the full CPU test completed41s. Float32 hybrid-Qwen finite differences vs autograd: seed0 .94395876/.94402778, seed1 1.5431009/1.543159. The BF16 full-main fixture executes eight genuine backwards followed by eight generation trajectories, checks no evaluation gradients/extra passes, identical delta/schedule,32-token coverage, matched random norms, exact post-cast states and unchanged parameters. Synthetic donors are deliberately aligned to the tiny-model gradient for positive-path coverage; this is not scientific calibration evidence. Source/log: `slop/audits/2026-10-01_vjp-check.py`, `.log`. The nonpositive orientation failure is present in production but not yet exercised by this fixture.

Real full-size backward support/memory remains unknown. One pueue-default job,300s TERM plus15s grace, no reordering. Retain each completed generic context and completed generation trajectory on failure. An interrupted backward or an in-progress generation may not have a completed artifact. A timeout/unsupported backward path is not0/2. Use the existing08 entry point for preparation and all conditions; no parallel inference implementation. Both goals remain open.

Pre-launch update, PI/OpenAI: the same-family review found that completed naming contexts were saved only after all eight backwards. Source8767a29aa90ce13624ee6a64802eea4a14014287b2b49164116600b4590048fd now saves each context independently; no inference calculation changed. The43s full CPU check passed, including negative coefficient rejection and an injected interruption after three contexts with all three gradients recovered exactly. Complete states and records are readable in those artifacts; the partial fixture explicitly compares gradients, not every metadata field. Review was on source95be8e43, so this small retention repair is parent-verified, not independently accepted. At95be8e43, the118s VJP/chat/legacy chain passed both chat seeds and72 exact baseline scoring rows per seed; differences since then are preparation artifact writes only. The launcher assertions were reviewed statically, not executed end-to-end on a tiny model. Full-size backward and semantic behavior remain unknown.

Planned queue invocation: `env PYTHONPATH=/dev/shm/suppressed-import-7ac02bf HF_HUB_OFFLINE=1 timeout --signal=TERM --kill-after=15s 300 uv run --no-sync --offline python -u .local/queued/vjp.py .local/queued/08_vjp.py .local/queued/vjp.json`. No parameters changed from the prospective recipe.
