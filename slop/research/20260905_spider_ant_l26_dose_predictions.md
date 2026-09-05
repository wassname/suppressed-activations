# Spider→Ant L26 dose predictions

Question: can one application at residual L26 turn the stable p6 increase into a specific `8`→`6` answer change before the distribution degrades?

The method and prompt stay fixed. Every operation acts only at L26. The primary condition swaps the projected lowercase-space token pair (` spider`/` ant`) at the final prompt position. Diagnostics compare the mean of four variants, the preceding ` is` position, and suppressed-subspace ranks 8, 16, 32, and 64. C=1 is the exact two-coordinate swap. C>1 extrapolates beyond the swap. The run measures both raw and residual-norm-restored operations. The predeclared primary rank-8 condition is compared with 32 random rotations per positive dose, matched for residual norm and perturbation norm. Any larger-rank candidate requires a later matched-control confirmation.

| option | expected metric change | what separates it |
|---|---|---|
| positive L26 dose | 6-vs-8 log odds rise with C before KL rises sharply | targeted effect exceeds the 32 matched random rotations |
| negative L26 dose | 6-vs-8 log odds fall | sign reversal supports the Spider→Ant interpretation |
| rank 8→64 | more of the target Ant direction survives projection | improvement grows before unrelated directions dominate |
| final vs preceding position | locate whether the concept is causal where detected or one token earlier | one position gives a larger stable odds change |
| norm restoration | delays generic degradation at high C | raw output degrades before restored output at similar semantic effect |
| generic digit perturbation | p6 may rise, but not beyond matched random changes | digit-conditional distribution and random controls |

| possibility | prior | expected observation |
|---|---:|---|
| useful local Ant steering exists at L26 | 45% | a positive dose makes `6` top, preserves a distributed next-token distribution, and beats at least 31/32 matched random changes |
| direction has weak specific influence but cannot flip the answer cleanly | 35% | positive doses improve 6-vs-8 odds, then degrade or saturate while `8` remains top |
| L26 movement is a generic perturbation | 15% | matched random rotations often equal or exceed the targeted log-odds change |
| implementation or numerical bug | 5% | C=0 differs from clean, C=1 fails to swap coordinates, or random rotations fail norm/distance checks |

The idea is not rejected if this one layer fails. Another implementation can intervene once on a learned layer-weighted aggregate, or use the target token direction only rather than an equal coordinate exchange.

A credible positive result requires all of: top `6`, a coherent 64-token continuation, no concentrated/collapsed next-token distribution, and a larger 6-vs-8 log-odds change than at least 31/32 matched random rotations at that dose. No README claim changes before those observations exist.

## Result

Several conditions changed the first token from `8` to `6`. The best smaller-dose row was lowercase-space rank 16, final position, norm-restored C=8: p6=.61466, p8=.05717, KL=2.26093, and entropy=1.44536. The preceding position did nothing. Rank 32 never produced top `6`.

The preregistered lowercase rank-8 primary at C=12 produced top `6`, p6=.34397, and p8=.14339, but exceeded only 30/32 matched random effects. Two random controls also produced stronger top-`6` changes. The 31/32 specificity requirement was contradicted.

All top-`6` continuations were byte-identical because the intervention stops after the first generated token. Their coherence is self-conditioning evidence, not independent evidence of Ant semantics. See [`job_132.md`](../audits/job_132.md) and [`out/2026-09-05_191959_spider-ant/log.md`](../../out/2026-09-05_191959_spider-ant/log.md).

Written by PI/gpt-5.4.
