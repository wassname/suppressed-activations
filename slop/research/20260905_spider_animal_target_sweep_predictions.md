# Spider animal-target sweep predictions

Question: does the rank-16 L26 edit carry target-animal semantics, or does this spider prompt merely tend to change from 8 to 6 under a large perturbation?

The source prompt, rank-16 suppressed subspace, L26 final position, residual-norm restoration, and Spider source token stay fixed. Three single-token targets are fixed before the run: ` ant`→6 legs, ` dog`→4 legs, and ` bird`→2 legs. Each target strength is calibrated without another model forward so its achieved residual perturbation norm matches the Ant C=8 distance. The same 32 random rotations provide the null at that physical distance.

| possibility | prior | expected observation |
|---|---:|---|
| target-animal semantics | 40% | Ant/Dog/Bird make 6/4/2 top respectively; each source coordinate falls and its target coordinate rises; expected-token effects exceed at least 31/32 random effects |
| prompt-specific digit perturbation | 50% | several targets produce the same digit, unrelated digits, or no stable mapping to 6/4/2 |
| calibration or coordinate bug | 10% | achieved distances differ materially, residual norm changes, or coordinate orientation is wrong |

The strongest result is the three-way mapping, not any one target. A failure of Bird alone may reflect the word’s polysemy; a consistent 6/4/2 pattern is hard to explain through one accidental 6-favoring direction.

Written by PI/gpt-5.4.
