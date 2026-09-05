# Localized Spider→Ant predictions

Question: does the mean of matched Spider/Ant tokenizer variants produce a coherent `6` when applied only where the rise-and-fall readout selected `Spider`, rather than at every prompt token?

The extraction rule remains L23/L25/L32, rank 8, normalized LM-head rows. The intervention remains residual layers L23–L30. This run changes the position mask from all 14 prompt tokens to only the selected final position. It tests the mean prototype at C ∈ {1, 1.5, 2, 3, 4, 6, 8, 10}, with and without residual-norm restoration. C>1 is steering past a full coordinate exchange.

| possibility | prior | expected observation |
|---|---:|---|
| localized intervention raises p6 but never flips | 45% | `p6` rises smoothly while `8` remains top through the coherent range |
| localized intervention produces coherent `6` | 25% | `6` becomes top with ordinary entropy before lexical takeover |
| localization only delays collapse | 25% | top token changes from `8` to `Spider`, `Web`, or another inserted word before `6` wins |
| implementation or direction error | 5% | source coordinate fails to fall or target coordinate fails to rise at C=1 |

Success requires all of: `6` is top, its absolute probability is not collapsed, the output KL is finite and below the lexical-takeover rows, the Spider coordinate falls while the Ant coordinate rises, and a 64-token continuation remains coherent. The script records pre/post coordinates and perturbation/residual norm at every intervened layer. It generates 64 tokens only for a row that makes `6` top.

A positive 6-vs-8 contrast with another top token does not pass.

## Result

Localization did not produce `6`. At C=1, the operation exactly exchanges the two dual coordinates at all eight intervened layers, but the next token remains `8`: `p6=0.03361`, `p8=0.86692`, and KL=0.00139. C=1.5 remains top `8`. At C=2 the top token changes directly to `Spider`; raw rank(6)=248274 and restored rank(6)=22.

The coordinate log explains the abrupt failure. One exchange changes the coordinate difference by a factor of `1 - 2C`. C=2 therefore flips and triples it at each layer. Across eight layers, the raw C=2 coordinates grow to about `[504, -501]` at L30. Norm restoration bounds the residual norm but does not stop the coordinate pair from dominating its direction.

The first prediction is supported only at C=1. The coherent-`6` prediction is contradicted. The “localization only delays collapse” prediction is supported. The implementation exchanges numeric coordinates correctly; it has not shown that these coordinates are a causal Ant concept.

Jobs 127 and 128 have identical scientific log lines. Job 128 overwrote the fixed-path artifact and therefore records a dirty tree. See [`job_127.md`](../audits/job_127.md), [`job_128.md`](../audits/job_128.md), and the [fresh review](../reviews/20260905_jobs127_128_localized_review.md).

Next: apply C=2 at one layer only. A healthy L30-only output would confirm that repeated over-relaxation caused the collapse; immediate `Spider` would implicate the direction itself.

Written by PI/gpt-5.4.
