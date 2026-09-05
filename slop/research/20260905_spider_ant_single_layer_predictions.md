# Single-layer Spider→Ant prediction

Question: does C=2 collapse because it is applied at eight layers, or because the mean Spider/Ant direction itself writes `Spider`?

This run keeps the selected final prompt position, mean of four atomic token variants, and C=2. It applies the operation only once, at residual L30. It records the next-token distribution, KL, entropy, perturbation size, and dual coordinates. All previous rows are rerun unchanged for artifact continuity.

| possibility | prior | expected observation |
|---|---:|---|
| repeated over-relaxation caused the collapse | 75% | L30-only C=2 keeps a healthy distribution and top `8`; coordinate magnitude remains ordinary |
| the one-step direction causes lexical takeover | 20% | L30-only C=2 produces top `Spider` or another inserted token with high KL |
| one-step operation produces top `6` | 5% | `6` wins with noncollapsed probability and ordinary entropy |

The first condition is a diagnostic success, not a causal Ant success. A causal success still requires top `6`, increased Ant/decreased Spider readout, and coherent generation.

## Result

The leading prediction was supported. One C=2 operation at L30 changes the mean source/target dual coordinates from `[3.111, -0.163]` to `[-3.437, 6.385]`, exactly the expected −3 contrast, but leaves the output healthy and nearly unchanged: top `8`, `p6=0.02669`, `p8=0.88391`, and KL=0.000160.

The same C=2 operation repeated at L23–L30 produced top `Spider`, KL=76.46, and L30 coordinates near `[504, -501]`. Repeated over-relaxation explains that collapse. The one-layer result does not produce `6`; it only rejects L30 as the independent cause of the collapse.

See [`job_129.md`](../audits/job_129.md), [full log](../audits/job_129_full.log), and the [fresh review](../reviews/20260905_job129_single_layer_review.md).

Next: apply C=2 separately at L23–L29. If those outputs also remain healthy, repetition is the clear cause; any top `6` row identifies a layer for a local dose sweep.

Written by PI/gpt-5.4.
