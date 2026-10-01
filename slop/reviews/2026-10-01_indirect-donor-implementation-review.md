# Indirect-donor implementation review

**Verdict:** No blocking defect found for the frozen launcher configuration. One conditional exception-cleanup issue remains in the shared preparation helper. This is implementation review, not scientific or goal signoff.

Reviewed the supplied diff, relevant main-path interactions, scoped demo helpers, data, launcher, smoke source, all supplied logs, hook-capture implementation, preregistration, design advice, AGENTS instructions, and ML-debug skill. No commands, model execution, edits, or delegation performed.

## Verified by inspection and supplied evidence

- **Capture and sign:** `scripts/english/08_jlens_one_pass.py:569–612` captures `res[block + 1][-1].float()` and averages four states per animal. At block15 this is residual16. The explicit descriptions contain neither animal names nor evaluated answers; all eight end in `. It`. The final token is asserted against tokenized `" It"`.
- **Addition and schedule:** `scripts/english/08_jlens_one_pass.py:1479–1518,1572–1668` constructs spider-minus-dog, requires reverse mode, and applies it only at the last prompt position, then every cached decode with scale `.25`. The exact float32 decode operation is `selected + phase_scale * (edited - selected)`, followed by model-dtype casting—not necessarily bitwise identical to precomputing `.25 * delta`.
- **Controls:** Main selects Base/new donor/natural literal donor/new-norm random for each property, and Base/new donor for arithmetic: ten trajectories. The literal checkpoint is hash-checked and not rescaled. Random is seeded once per construction and fixed across positions; the launcher checks identical vectors across properties. The additional two literal conditions were disclosed prospectively.
- **No current-input preparation or observer feedback:** The donor branch sets `cases=[]`, bypassing readout-generation preparation. Neither reflection nor country-swap target probing is enabled. The block23 observer appends readout words and returns no replacement. Norm/head readout calculations are not additional transformer forwards.
- **Metric sign:** `answer_log_odds_shift` favors `4`/`inside`; negative movement favors the reverse animal targets `8`/`outside`. Both main and launcher reports explain this. Arithmetic correctly retains expected answer `4`.
- **Retention:** Completed preparation contexts are saved individually; completed generation states and accumulated `interventions.json` are saved after each trajectory. There is no promise of retaining the currently interrupted generation.
- **Actual-forward instrumentation:** The launcher wrapper calls the original loader, adds a read-only model prehook, and records phase, sequence length, and grad mode. Its return is implicitly `None`. It compares actual call counts and lengths against condition coverage.

The supplied smoke log states, separately for seeds0 and1:

> “10 trajectories and320 tokens, no extra eval forwards/gradients; unchanged weights/foreign hooks; identical vectors across properties; natural literal control and matched random; exact requested/BF16 states; interruption retains3 completed contexts”

The fixture code supports those assertions, including independent block15 observation of post-cast states. These are tiny random CPU-model checks, not pretrained behavior.

## Conditional finding: preparation hook survives an exception

**Location:** `/workspace/2026/suppressed-activations/scripts/demo.py:70–79`

**Observed code:**
```python
handle = final_norm.register_forward_pre_hook(...)
with torch.no_grad():
    output = model(...)
handle.remove()
```

**Affected input:** Any donor preparation forward that raises after hook registration.

**Inference:** Removal is skipped on an exception, leaving this helper-owned final-norm prehook attached if the caller retains/reuses the model. This is distinct from the legitimate persistent Transformers capture hooks. It is not a blocker for the present launcher, which does not recover and reuse the failed preparation model.

**Evidence limitation:** The smoke interruption raises *before* calling the fourth `trajectory`; it proves completed-context retention, not cleanup during a failed trajectory.

**Discriminating check:** Inject an exception inside `model(...)`, catch it while retaining the model, and compare final-norm prehook identities before/after. A retained helper hook confirms the issue; unchanged identities disprove it. Exception-safe removal would address it without changing scientific settings.

## Failure history and evidence limits

- `smoke.initial.log` shows preparation returning `None`; the reviewed main now returns `out`.
- `smoke.hook-order.log` compares saved original states against a foreign hook that executes after the prepended editor. Current comparison uses saved post-cast states, consistent with `layer_hooks(... prepend=True)`.
- `smoke.hook-ownership.log` assumes a single hook. The supplied Transformers implementation explicitly installs capture hooks lazily and keeps them installed. Current smoke compares hook identities against the post-preparation baseline. Neither historical failure establishes a production hook leak.
- `readout-regression.log` reports “44 rows/36 originals exact” for each seed. This supports the exercised readout/replay paths; it does not independently establish every historical algorithm or an unhooked-versus-Base equivalence test.
- `launcher-check.json` reports `"pins_match": true` and the actual prehook fixture returning `None` for positional/keyword inputs. It also explicitly reports `"launcher_end_to_end_executed": false`. I did not recompute hashes or inspect out-of-scope fixture dependencies.
- CPU smoke does not establish GPU numerical behavior, peak memory, or completion within300s. The production launcher's saved-state checks are therefore meaningful remaining validation, not already completed evidence.

## ML-debug notes

| Check | Evidence or remaining uncertainty |
|---|---|
| Configuration and denominator | Two tiny-model seeds; eight new preparation contexts and ten32-token trajectories per seed. No training or optimizer schedule. |
| Contract SHOULD checks | Smoke asserts capture/means/common token, requested/post-cast states, fixed controls, coverage, no extra evaluation forwards, and no gradients. |
| Null/baseline interpretation | Random-model continuations are visibly nonsensical; no scientific performance number is claimed. Base and matched random are implemented controls, not evidence of pretrained transfer. |
| Full sample inspection | Read all supplied continuations and failures. Example preparation input: `'A field note describes an animal that wraps captured insects in silk. It'`; the subsequent tiny-model legs Base begins `'体味 GUIDE Рецеп.dtype…'`. This only tests plumbing. |
| Competing explanations for eventual behavior | Correct addition may fail to transfer; magnitude/prefix-length differences may explain apparent gains; measurement or GPU-path faults remain possible. Preregistration assigns rough planning weights, not posterior estimates. |
| Cheapest discriminators | Existing production forward trace and exact saved-state reconstruction distinguish missed/misapplied edits from correctly applied ineffective edits. Full continuations distinguish affirmed answers from later hypotheses. |
| Runtime | Check artifact reports78s for tiny main plus readout regression; pretrained stage timing and memory remain unknown. |
| Independent review | This is the requested same-family review. No further reviewer was launched. |

Natural norm and prefix-length confounds, ambiguity of descriptions, and one random direction remain disclosed limitations. They do not invalidate this fixed implementation test, but prevent attributing success solely to semantic alignment or claiming a null distribution.

— PI/OpenAI