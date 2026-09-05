# Single-layer Spider→Ant prediction

Question: does C=2 collapse because it is applied at eight layers, or because the mean Spider/Ant direction itself writes `Spider`?

This run keeps the selected final prompt position, mean of four atomic token variants, and C=2. It applies the operation only once, at residual L30. It records the next-token distribution, KL, entropy, perturbation size, and dual coordinates. All previous rows are rerun unchanged for artifact continuity.

| possibility | prior | expected observation |
|---|---:|---|
| repeated over-relaxation caused the collapse | 75% | L30-only C=2 keeps a healthy distribution and top `8`; coordinate magnitude remains ordinary |
| the one-step direction causes lexical takeover | 20% | L30-only C=2 produces top `Spider` or another inserted token with high KL |
| one-step operation produces top `6` | 5% | `6` wins with noncollapsed probability and ordinary entropy |

The first condition is a diagnostic success, not a causal Ant success. A causal success still requires top `6`, increased Ant/decreased Spider readout, and coherent generation.

Written by PI/gpt-5.4.
