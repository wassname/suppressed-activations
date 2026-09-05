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

Written by PI/gpt-5.4.
