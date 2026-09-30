# Prospective VJP implementation review

**Verdict:** one definite failure-artifact retention defect in the reviewed source. No additional blocking mathematical or evaluation-isolation defect found in the fixed launcher path. This is not scientific validation or goal signoff.

Reviewed source identity supplied by parent: `95be8e43d032cd0ef27798c56051c24a86f9ff38eccb0b971d74059c7b88a41a`. No commands, inference, edits, network access, or delegation performed.

## Definite finding

### Completed preparation contexts are lost on interruption

**Path:** `scripts/english/08_jlens_one_pass.py:638–665`

Observed code accumulates completed results in memory:

> `gradients.append(gradient.cpu()); states.append(state.cpu())`

The first checkpoint write occurs only after all eight backwards:

> `torch.save({"gradients": gradients, "states": states, ...}, out / "vjp.pt")`

This conflicts with `slop/audits/2026-10-01_vjp-preregistration.md`:

> “Save complete partial artifacts on failure.”

**Affected inputs:** any preparation where an exception, OOM, or timeout occurs after one completed context but before final saving. Earlier gradients, states, naming logits, and records disappear. Evaluation likewise saves local states only after a complete trajectory.

**Consequence:** a bounded, first full-size backward attempt can fail without retaining the evidence needed to locate its failure. This is a blocker for the promised partial-artifact contract, not evidence against the scientific proposal.

**Discriminating check:** interrupt preparation after a completed context and verify its exact gradient, activation, token IDs, logits, and completion count remain readable. Separately interrupt a generation if “complete partial artifacts” includes in-progress trajectories.

Parent acknowledges this defect and reports a retention repair underway. That repair was not reviewed here.

## Verified implementation structure

- **Gradient location and contrast:** `naming_vjp` attaches a detached, gradient-enabled block15 output; differentiates actual final-position `z_spider − z_dog`; then selects the earlier `It` position. The naming suffix remains downstream of that activation. Parameters are frozen, and the normal model suffix/head supplies logits—not a lens approximation.
- **Token alignment:** preparation requires single-token names and ` It`, and asserts the complete prefix remains an exact prefix of the suffixed tokenization.
- **Projection:** `u = mean(g)/norm(mean(g))`, `D = mean_spider − mean_dog`, and `delta = (D @ u)u` match the proposal. Positive coefficient is required; no sign rescue occurs. The projection norm bound is asserted.
- **Scale provenance:** donor JSON reports natural difference norm `1.4303362369537354`. Configuration pins the templates and donor SHA. I did not independently inspect or hash the binary donor checkpoint.
- **Isolation:** preparation returns before evaluation setup. VJP evaluation has empty standalone-readout cases and no current-input preparatory forward or backward. Base affects reported differences only. The block23 observer returns no replacement and does not control editing.
- **Budget:** the configuration contains four templates × two animals. Launcher requests three leg trajectories, three skeleton trajectories, and two arithmetic trajectories: eight total, at most256 generated tokens.
- **Schedule and exact reconstruction:** production computes float32 `h + delta`, then on decode `h + 0.25*((h + delta) − h)`, then casts to model BF16. The launcher reconstructs this same operation order—not merely the algebraically equivalent expression—and checks exact saved requested/post-cast states. Saved float32 copies preserve BF16 source values exactly.
- **Hook ownership:** supervisor authorized additional reads of `scripts/demo.py` and `suppressed_activation_subspace.py`. `layer_hooks` removes its own handles in `finally`; it does not clear unrelated hooks. `replace_output` preserves tuple tails.
- **Metrics:** positive log-odds shift favors `4`/`inside`; reverse animal success therefore favors a negative shift. Arithmetic expects `4` in both conditions. Repetition uses generated non-special token IDs. Exact continuations, top10 probabilities, prefill/final readouts, and coverage are retained after completed conditions.

## Nonblocking reporting and provenance caveats

1. **Preparation failure discovery:** launcher writes the preparation directory into `pipeline.json` only after `main` returns. A failed preparation can leave the master record at `preflight` without a direct link to its child artifacts.
2. **Schema clarity:** condition frontmatter interpolates `coordinate_kind: None` for VJP, which is a string rather than YAML null. Coverage also calls legacy J-coordinate diagnostics `edit_basis_coordinates_*`, although those coordinates do not define the VJP edit. Neither changes the intervention, but downstream readers should not interpret them as VJP coordinates.
3. **Standalone entry point versus fixed launcher:** evaluation checks checkpoint revision/block/pass status but does not independently enforce the preregistered configuration hash. The fixed launcher supplies the stronger source/config/donor/helper hash chain. Claims of a frozen recipe should cite that launcher, not arbitrary `--vjp-checkpoint` usage.
4. **Timeout:** the launcher itself has no deadline. Supervisor supplied a planned outer `timeout --signal=TERM --kill-after=15s 300 …` invocation through pueue default. Submission and actual enforcement remain unverified.

## Test evidence and scientific limits

I read the complete initial log and test fixture. The log identifies source `8911bc…`, not the current source, and reports:

> `finite difference=0.94395876, autograd=0.94402778`  
> `finite difference=1.5431009, autograd=1.543159`

It also reports:

> `PASS BF16 full main:8 offline backwards,8 generation trajectories, no eval gradients/extra forward pass, unchanged weights, identical frozen vector/schedule, matched random,32-token coverage and exact post-cast states; arithmetic expects4`

These are tiny-model implementation checks. Synthetic donors were deliberately aligned with the tiny-model gradient. They do not establish a positive pretrained coefficient, useful magnitude, coherent behavior, or full-size backward capacity.

The original fixture does not exercise nonpositive orientation, interrupted preparation, or early EOS in this VJP path. The launcher’s exact reconstruction assertions were read, not executed by this reviewer. Parent subsequently reported new regression completion, but I did not inspect those new logs and do **not** certify those regressions or the pending retention repair.

### ML-debug disposition

- **Observed:** initial tiny finite-difference agreement and positive-path pipeline coverage; no pretrained VJP results.
- **Unknown:** actual4B backward support, peak memory/runtime, coefficient, applied BF16 effect, and semantic outcomes.
- **Competing explanations for future outcomes:** naming bias, weak/nontransferring projected scale, implementation/casting error, or useful cross-property influence. No outcome-based probabilities are justified yet.
- **Null/control interpretation:** Base and one fixed norm-matched random direction contextualize behavior; one random seed is not a significance estimate. Arithmetic preservation is a separate diagnostic.
- **Required readout remains open:** observer outputs use prompt masking, not demonstrated spoken-word exclusion. A changed name/readout or digit does not demonstrate referent replacement.
- **Next distinguishing evidence:** retain preparation/failure artifacts, then inspect all two property attempts and arithmetic continuations under the unchanged recipe. No parameter or recipe optimization follows from these tests.

This is fixed contrast addition, not literal hidden-component replacement. Both research goals remain open.

— PI/OpenAI