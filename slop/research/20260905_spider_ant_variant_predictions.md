# Spider→Ant matched-token-variant predictions

Question: does one joint coordinate swap over matched atomic spelling variants work better than the canonical single `Spider`↔` Ant` swap?

Qwen tokenizes newline-prefixed words as a separate newline token followed by the ordinary word token, so `\nAnt` does not define another LM-head row. The joint swap uses every clear atomic source-target pair available in both concepts:

| source row | target row |
|---|---|
| `Spider` | `Ant` |
| ` Spider` | ` Ant` |
| ` spider` | ` ant` |
| ` spiders` | ` ants` |

The script projects all eight rows into each prompt-position suppressed subspace. It solves their coordinates jointly with one pseudoinverse and swaps each adjacent pair simultaneously. Layers, positions, normalization variants, and C∈{1,2} remain unchanged.

| possibility | prior | expected observation |
|---|---:|---|
| variant coverage recovers the semantic swap | 25% | matched C=1 raises 6-vs-8 odds substantially beyond the single pair and makes 6 top |
| variants add a larger but insufficient Ant-directed perturbation | 40% | p(6) rises more than the single pair but 8 remains top |
| projected rows are redundant or poorly conditioned | 25% | effect is similar, weaker, or unstable; C=2 degrades |
| implementation error | 10% | paired-coordinate identity or output shapes fail before model interpretation |

A successful result needs a coherent C=1 continuation beginning with 6. A larger p(6) without a top-token change is partial evidence only. C=2 degradation does not count as a stronger semantic swap.

TODO: after this run stabilizes, put the complete 64-token base, swap, random-replacement, and removal continuations in the README so lexical leakage and repetition remain visible.

## Result from job 123

The four-pair C=1 swap collapses both answer probabilities and makes `Web` top in every
position and normalization variant. For normalized directions at all prompt positions,
p(6) changes from 0.0267 to 1.73e-8 and p(8) changes from 0.8826 to 4.10e-9. The positive
6-vs-8 log odds are therefore misleading: 6 fell by 14.25 log units while 8 fell further.
The continuation begins `Web-spinning spiders have 8 legs.`

This rejects the joint pseudoinverse formulation, not the token-variant idea. Eight projected
variant rows fill the rank-8 suppressed subspace and are likely nearly dependent, so their
coordinate exchange can have a large operator norm. The next test uses each pair separately
and rank-2 mean or first-SVD prototypes.

## Result from job 124

The diagnosis is strongly supported: the normalized eight-row matrix has condition number
1,403 at the final prompt position. The rank-2 alternatives remain coherent.

At C=1, the lowercase word-boundary pair ` spider`↔` ant` gives the largest observed shift:
p(6)=0.0379, p(8)=0.8632, and Δlog p(6)=+0.353 nats. This pair was selected after comparing
four, so it is not a reusable default. The normalized mean and first shared-SVD directions
agree closely: both give p(6)=0.0337 and Δlog p(6)=+0.235 nats. Every method still answers 8.

The aggregate methods show that token variants can be pooled without collapse, but they do not
produce a semantic Spider→Ant answer swap. The next run tests stronger doses of the lowercase,
mean, and SVD directions, with and without residual-norm restoration.

Written by PI/gpt-5.4.
