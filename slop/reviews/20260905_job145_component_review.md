# Job 145 component review

The six preregistered C=1 one-coordinate interventions completed at the fixed spider prompt, rank-16 subspace, L26 final position, with separate norm restoration.

| pair | source-only Δp(2), Δp(4), Δp(6), Δp(8) | target-only Δp(2), Δp(4), Δp(6), Δp(8) |
|---|---|---|
| Spider–Ant | +.001826, +.006865, -.000270, -.008937 | +.000627, +.013464, +.015736, -.031203 |
| Spider–Dog | +.000821, +.006874, -.000266, -.008806 | -.000230, +.022871, +.006402, -.030106 |
| Spider–Bird | +.001818, +.006805, -.000295, -.009760 | +.000696, +.014113, +.006666, -.023296 |

The source-only rows are nearly identical. They confirm a common p(4)-up, p(8)-down pattern, but target-only Δp(4) is larger for every pair, so source removal does not explain most of the combined effect.

The target-only matrix has a weak across-target diagonal: Ant has the largest Δp(6), Dog the largest Δp(4), and Bird the largest Δp(2) by only .000068 over Ant. Within rows, Ant→6 and Dog→4 are selective. Bird→2 is not: its Δp(4) is about twenty times its Δp(2).

The two residual deltas sum before norm restoration. The observed interventions are separately norm-restored and therefore are not additive components of the final residual or probability effect. For Ant, combined Δp(4)=.031637 while the separate effects sum to .020329. For Dog these are .042720 and .029745.

Cheapest next experiment: first-token-only target-coordinate strength sweeps, with fixed prompt, basis, layer, position, and norm restoration. Success for Dog is a unique top 4 with p(4)>p(8) and p(4)>p(6). Generate only once at the smallest successful strength.

Verdict: valid diagnostic. It supports a common source pattern and weak target-conditioned structure, but no robust 8→4 result yet.

— reviewer subagent, fresh context
