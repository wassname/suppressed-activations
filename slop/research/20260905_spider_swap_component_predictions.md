# Spider swap-component predictions

Question: does the C=1 probability shift come from the common Spider side of the coordinate operation or from target-specific Ant, Dog, and Bird sides?

The spider prompt, rank-16 subspace, L26 final position, token variants, and norm restoration remain fixed from job 144. For each pair, split the C=1 coordinate delta into its source-coordinate component and target-coordinate component. Six forwards record changes in p(2), p(4), p(6), and p(8). No generation or dose tuning is needed for this diagnostic.

| possibility | prior after job 144 | expected observation |
|---|---:|---|
| common Spider component explains the effect | 70% | source components reproduce the shared p(4) rise; target components are smaller or lack a 6/4/2 diagonal |
| target additions carry weak animal semantics | 25% | target components show Ant→6, Dog→4, Bird→2 diagonal selectivity |
| both components are needed nonlinearly | 20% | neither component resembles the combined edit, despite their residual deltas summing before norm restoration |

The result that keeps semantic replacement alive is a target-component diagonal. A common source-component pattern explains job 144 without animal replacement.

Written by PI/gpt-5.4.
