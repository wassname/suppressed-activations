# Job 143 fresh scientific review

## Result

The equal-distance Ant/Dog/Bird sweep does not establish semantic animal mapping.

| target | expected | observed |
|---|---:|---|
| Ant | 6 | 6 top; p(6)=0.6147, p(8)=0.0572 |
| Dog | 4 | 6 top; p(4)=0.1267 |
| Bird | 2 | 4/6 tied; p(2)=0.1127 |

The preregistered criterion was the 6/4/2 mapping with each expected-token effect above at least 31/32 random effects. The observed ranks were 30/32, 29/32, and 29/32.

All animal interventions matched the same residual distance, about 23.1858, and preserved residual norm, about 25.3632. However, C=1 is the exact coordinate exchange. Ant used C=8, Dog C=11.0575, and Bird C=11.6056. These are large extrapolations, and the perturbation is about 91% of the original residual norm.

The matched random controls test arbitrary norm-matched residual changes. They do not match the structured token-derived geometry. Random target tokens passed through the same projected-coordinate pipeline would be a closer null. Five of 32 random controls placed 6 first, and seed 0 placed 4 first.

Bird has a reporting tie: 4 and 6 have equal stored probability, 0.3064672, while the rendered table reports only 6 and greedy generation begins with 4.

The post-intervention selected tokens remain dominated by Spider/web vocabulary and do not visibly include ant, dog, or bird. These are recomputed selected tokens, not a validated decoder of latent thoughts. The generations establish a changed first token only. The Ant continuation exactly equals a no-intervention continuation with the first 6 forced, so later text is ordinary autoregressive continuation rather than independent evidence of persistent concept replacement.

The byte control remains unchanged but receives a fresh prompt-specific basis and only 5.8854 perturbation distance. It does not apply the same Spider-derived direction at equal magnitude.

Earliest unsupported causal link: projected source/target unembedding coordinates have not been shown to form a semantic Spider→Animal state change.

Cheapest next experiment: run Ant/Dog/Bird at C=1, without generation, and record p(2), p(4), p(6), and p(8). This tests the non-extrapolative coordinate exchange in three forwards. Target-specific diagonal changes would support semantics; shared movement would support generic digit perturbation.

Verdict: block any claim that job 143 confirms semantic mapping. The run is valid and informative as a negative result about the large-extrapolation implementation.

— reviewer subagent, fresh context
