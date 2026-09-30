# One next causal attempt: indirect-referent donor addition

**Recommend hypothesis 1:** prepare a natural donor contrast from indirect descriptions, then test it directly on the two existing dog→spider property questions. This is a **preparation-data change using ordinary addition**, not new algebra, component isolation, or independent signoff. Supervisor confirmed this scope and the unchanged edit schedule.

## Why this option

| Hypothesis | Assessment |
|---|---|
| **1. Literal-name preparation mismatches indirect referents** | Cheapest goal-directed attempt. Removes literal animal names from preparation; tests actual property behavior rather than another separation gate. |
| **2. Optimize a fixed vector across naming contexts** | Distinct from averaging gradients, but still optimizes verbalization rather than property transfer. Requires independently justified norm and stopping rules; neither is supplied. |
| **3. Probe-based feature replacement** | Changes the operation meaningfully, but introduces supervised-feature and calibration assumptions. `slop/audits/2026-09-30_job2628.md` reports “Candidate brackets: 2/8” and reversed ordering after projection. That does not refute learned probes, but argues against another calibration-first attempt now. |

No better-supported alternative emerges from this scope.

**Observed evidence:** `slop/audits/2026-10-01_job2681.md` reports “Intended property changes0/2, same as matched random,” despite nonzero applied updates. The selected full-donor result remains **1/4 development initial-answer successes**, including “The animal that spins webs is a dog,” per `slop/reviews/2026-10-01_causal-positive-scope-review.md`. Neither observation establishes why transfer failed.

## Freeze this small experiment prospectively

**Offline data:** cross these two wrappers with both description pairs below, yielding four prompts per animal:

- `A field note describes an animal that {description}. It`
- `A story mentions an animal that {description}. It`

| Dog description | Spider description |
|---|---|
| `retrieves thrown sticks for its owner` | `suspends sticky silk threads to trap flies` |
| `is trained to sniff luggage at customs` | `wraps captured insects in silk` |

These proposed strings contain neither animal name, evaluated leg/skeleton answers, nor exact evaluation prompts. They are not perfectly unambiguous; freeze them without output-based replacement. Verify the final token is the same ` It` token across all eight prompts; differing prefix lengths remain a limitation.

At block15 output/residual16:

\[
\mu_c=\tfrac14\sum_i h_{16,\mathrm{It}}(x_{c,i}),\qquad
\delta=\mu_{\mathrm{spider}}-\mu_{\mathrm{dog}}.
\]

Intuitive pseudocode:

```text
offline: capture eight final-It states; average by animal; save δ
current trajectory:
    final prompt position at block15: h ← h + δ
    each cached decode position:      h ← h + 0.25δ
```

No projection, fitted classifier, backward pass, normalization, or magnitude matching to an old intervention. Freeze model/revision, block15, final-prompt-one coverage, quarter-decode schedule and 32-token horizon. Observer23 may record but never influence edits.

**Eight generations:** existing reverse legs and body-relative skeleton prompts, each under **Base / new full donor / seed0 norm-matched random**; existing arithmetic-control prompt under **Base / new full donor**. Reuse identical vectors across properties. Eight offline prefills plus at most256 generated tokens target one local300s job; timeout is not a scientific negative. No v5 or other fresh heldouts.

## What would advance the goal?

The most informative outcome is the **same vector** producing spider-compatible initial answers on both properties, readable noncontradictory continuations, and preserved arithmetic, unlike random. Report each property separately and retain all failures. This is a proposed evidential pattern, **not a human-specified universal success threshold**; one coherent property success remains partial evidence.

Count actual generated answers—not top-table ordering, later proposed NLI hypotheses, readout names, or digit occurrence. Exact continuations matter: job2681’s `4…Hypothesis…8` was not an affirmed eight-leg answer.

## Boundaries, checks, and uncertainty

- **Not a retired-setting rescue:** new offline descriptions are the selected change; no subsequent sign/dose/layer/coverage tuning. Compared with2681, removing the VJP projection also changes preparation. Therefore this does **not** isolate the causal effect of indirect wording versus naming gradients.
- **Magnitude confound:** natural donor norm changes with data. Even success would not prove better semantic alignment rather than stronger perturbation. Random controls nonspecific perturbation only imperfectly; one seed gives no null distribution.
- **Implementation requirement:** `scripts/english/08_jlens_one_pass.py:569–603` currently substitutes `{concept}`; paired descriptions need explicit data support. At `:1450–1600`, random ordinarily matches the projected delta unless configured otherwise, and arithmetic hardcodes `"offline naming VJP"`. Explicit full-donor/random mode selection and arithmetic plumbing are necessary; do not silently run those defaults.
- Before execution, verify real-path capture, sign, requested/post-cast vectors, unchanged Base behavior and coverage. No probe-bracketing prerequisite.
- The hypothesis is weakened if the new vector leaves both affirmed properties unchanged, matches random, or changes names/digits without coherent properties. A missing/misapplied edit instead invalidates that interpretation.

Read-only advice; no commands, edits, inference, or implementation performed. Root AGENTS and ML-debug skill read; supervisor confirmed no nested AGENTS. Raw historical outputs and full-model numerical replay were outside this review’s supplied evidence.

— **PI/OpenAI**