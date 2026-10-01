---
preparation_contexts: 8
generation_trajectories: 10
max_new_tokens_per_condition: 32
---
# Indirect-description donor addition

Written by PI/OpenAI. Natural unrescaled donor difference, ordinary addition, no current-input lookahead. Literal-name donor retains its own natural norm; random matches the new norm. Norm/length differences remain confounds. Raw observations, not certified concept replacement.

| Property | Condition | Expected | Log-odds shift toward4/inside | Bare pair mass | Repeated-bigram rate |
|---|---|---|---:|---:|---:|
| legs | [Base](../2026-10-01_093718_jlens-one-pass/base/run.md) | 4 | 0.0000 | 0.9508 | 0.0323 |
| legs | [indirect-description donor](../2026-10-01_093718_jlens-one-pass/indirect-description-donor/run.md) | 8 | -0.1250 | 0.9525 | 0.0323 |
| legs | [literal-name donor control](../2026-10-01_093718_jlens-one-pass/literal-name-donor-control/run.md) | 8 | -0.3750 | 0.9450 | 0.0323 |
| legs | [matched-random delta](../2026-10-01_093718_jlens-one-pass/matched-random-delta/run.md) | control | 0.0000 | 0.9486 | 0.0323 |
| skeleton_body | [Base](../2026-10-01_093729_jlens-one-pass/base/run.md) |  inside | 0.0000 | 0.4801 | 0.0323 |
| skeleton_body | [indirect-description donor](../2026-10-01_093729_jlens-one-pass/indirect-description-donor/run.md) |  outside | 0.0000 | 0.4470 | 0.0323 |
| skeleton_body | [literal-name donor control](../2026-10-01_093729_jlens-one-pass/literal-name-donor-control/run.md) |  outside | -0.2500 | 0.4763 | 0.0323 |
| skeleton_body | [matched-random delta](../2026-10-01_093729_jlens-one-pass/matched-random-delta/run.md) | control | 0.0000 | 0.4576 | 0.0323 |
| arithmetic_control | [Base](../2026-10-01_093740_jlens-one-pass/base/run.md) | 4 | 0.0000 | 0.9857 | 0.0323 |
| arithmetic_control | [indirect-description donor](../2026-10-01_093740_jlens-one-pass/indirect-description-donor/run.md) | 4 | 0.0000 | 0.9852 | 0.0645 |

## legs: Base

Expected: 4. Exact32-token continuation:

```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

## legs: indirect-description donor

Expected: 8. Exact32-token continuation:

```text
4.
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 8.
Does the hypothesis
```

## legs: literal-name donor control

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
Hypothesis: The number of legs on the animal that barks and is called man's best friend is 2.
Is the hypothesis
```

## skeleton_body: Base

Expected:  inside. Exact32-token continuation:

```text
 inside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the outside.
Is the hypothesis true
```

## skeleton_body: indirect-description donor

Expected:  outside. Exact32-token continuation:

```text
 inside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the outside.
Is the hypothesis true
```

## skeleton_body: literal-name donor control

Expected:  outside. Exact32-token continuation:

```text
 outside.
Hypothesis: The skeleton of the animal that barks and is called man's best friend is on the inside.
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

## arithmetic_control: indirect-description donor

Expected: 4. Exact32-token continuation:

```text
4.
Hypothesis: An animal that barks is nearby.
Does the fact entail the hypothesis?

<think>

</think>

Yes, the fact
```

Positive shift favors4/inside; reverse animal targets8/outside favor negative shifts. Arithmetic should preserve4. Full condition logs contain exact input, prefilling/final readouts, top10 and coverage.
