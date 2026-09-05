# Spider→Ant single-layer screen predictions

Question: does any one residual layer independently cause the C=2 Spider takeover, or does it require repeated application?

The screen applies the final-position mean-atomic operation once at each residual layer L23–L30. C=2 is an extrapolation past the exact C=1 swap. It records next-token rank/probability, KL, entropy, perturbation size, and dual coordinates. It does not generate text unless a later focused run finds a credible top-`6` candidate.

| possibility | prior | expected observation |
|---|---:|---|
| repetition causes the takeover | 70% | every one-layer row keeps a noncollapsed distribution; most remain top `8` |
| one early/middle layer is independently unstable | 20% | that layer alone produces top `Spider` or high KL |
| one layer produces useful Ant steering | 10% | p6 rises materially or becomes top while KL and entropy remain near clean |

The screen identifies a layer for a later dose sweep. It cannot by itself establish causal Ant steering without a matched random condition and coherent generation.

## Result

All eight single-layer rows remained top `8`, rank(`6`)=3, with KL at most .01283. This supports the 70% repetition prediction and contradicts an independently unstable layer in L23–L30.

L26 had the largest movement toward `6`: p6 .02666→.03724, p8 .88257→.84758, and log odds 6-vs-8 -3.5→-3.125. The output remained top `8`. Ant-specific steering is unresolved because this screen did not include matched random directions.

Sources: [`data/spider_ant_demo.json`](../../data/spider_ant_demo.json), [`job_130.md`](../audits/job_130.md), and [`job_130_full.log`](../audits/job_130_full.log).

Written by PI/gpt-5.4.
