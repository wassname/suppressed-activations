# Spider animal exact-swap predictions

Question: at the C=1 swap endpoint, do projected Ant, Dog, and Bird directions produce target-specific movement toward 6, 4, and 2?

The spider prompt, rank-16 suppressed subspace, L26 final position, source token, target token variants, and norm restoration remain unchanged from job 143. C=1 exchanges the two coordinates before restoring the residual norm. This run adds three forwards and records p(2), p(4), p(6), and p(8). It does not tune C separately per target.

| possibility | prior after job 143 | expected C=1 matrix |
|---|---:|---|
| weak target-animal semantics | 25% | each target's expected digit gains more than the other two targets' expected digits |
| shared digit perturbation | 55% | Ant, Dog, and Bird move the same digit most, or show no diagonal pattern |
| effect only exists under large extrapolation | 20% | every C=1 row remains close to clean |

The result that would keep the semantic hypothesis alive is a diagonal pattern in probability change, not necessarily a top-1 answer change. Shared movement or negligible movement lowers it.

Written by PI/gpt-5.4.
