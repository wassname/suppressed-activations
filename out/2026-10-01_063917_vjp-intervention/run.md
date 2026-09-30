---
preparation_contexts: 8
generation_trajectories: 8
max_new_tokens_per_condition: 32
---
# Fixed offline naming-VJP intervention

Written by PI/OpenAI. Natural projected pronoun scale; no current-input lookahead. Raw observations, not certified concept replacement.

| Property | Condition | Expected | Log-odds shift toward4/inside | Bare pair mass | Repeated-bigram rate |
|---|---|---|---:|---:|---:|
| legs | [Base](../2026-10-01_063938_jlens-one-pass/base/run.md) | 4 | 0.0000 | 0.9508 | 0.0323 |
| legs | [offline naming VJP](../2026-10-01_063938_jlens-one-pass/offline-naming-vjp/run.md) | 8 | 0.1250 | 0.9524 | 0.0323 |
| legs | [matched-random delta](../2026-10-01_063938_jlens-one-pass/matched-random-delta/run.md) | control | 0.1250 | 0.9524 | 0.0323 |
| skeleton_body | [Base](../2026-10-01_063949_jlens-one-pass/base/run.md) |  inside | 0.0000 | 0.4801 | 0.0323 |
| skeleton_body | [offline naming VJP](../2026-10-01_063949_jlens-one-pass/offline-naming-vjp/run.md) |  outside | -0.1250 | 0.4623 | 0.0323 |
| skeleton_body | [matched-random delta](../2026-10-01_063949_jlens-one-pass/matched-random-delta/run.md) | control | -0.1250 | 0.4687 | 0.0323 |
| arithmetic_control | [Base](../2026-10-01_063959_jlens-one-pass/base/run.md) | 4 | 0.0000 | 0.9857 | 0.0323 |
| arithmetic_control | [offline naming VJP](../2026-10-01_063959_jlens-one-pass/offline-naming-vjp/run.md) | 4 | 0.1250 | 0.9870 | 0.0323 |

## legs: Base

Expected: 4. Exact32-token continuation:

```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

## legs: offline naming VJP

Expected: 8. Exact32-token continuation:

```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Does the hypothesis
```

## legs: matched-random delta

Expected: control. Exact32-token continuation:

```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Does the hypothesis
```

## skeleton_body: Base

Expected:  inside. Exact32-token continuation:

```text
 inside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the outside.
Is the hypothesis true
```

## skeleton_body: offline naming VJP

Expected:  outside. Exact32-token continuation:

```text
 inside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the outside.
Is the hypothesis true
```

## skeleton_body: matched-random delta

Expected: control. Exact32-token continuation:

```text
 inside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the outside.
Is the hypothesis true
```

## arithmetic_control: Base

Expected: 4. Exact32-token continuation:

```text
4.
Hypothesis: An animal that barks is nearby.
Does the fact entail the hypothesis?

<think>
Thinking Process:

1.
```

## arithmetic_control: offline naming VJP

Expected: 4. Exact32-token continuation:

```text
4.
Hypothesis: An animal that barks is nearby.
Does the fact entail the hypothesis?

<think>
Thinking Process:

1.
```

Positive shift favors4/inside; reverse animal targets8/outside favor negative shifts. Arithmetic should preserve4. Full condition logs contain exact input, prefilling/final readouts, top10 and coverage.
