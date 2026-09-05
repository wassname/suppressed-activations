# Causal translation demo predictions

Question: does replacing the `heart` prompt's rank-8 suppressed component with the `seat` prompt's component move the Chinese next token from 心 toward 座?

| condition | expected next-token result | result that rejects the interpretation |
|---|---|---|
| base | 心 is top-1 | baseline misses 心 |
| own-subspace replacement, C=1 | p(座)/p(心) increases; preferably 座 is top-1 | no larger shift than matched random |
| matched-random replacement | no systematic preference for 座 | it shifts toward 座 as much as the own subspace |
| own-subspace removal | p(心) falls without incoherent continuation | effect is only residual-norm loss or generic KL |
| dose sweep | negative and positive C move away from and toward 座 before incoherence | only extreme doses move, or both signs move the same way |

Likely failure (45%): rank 8 contains hidden English but its whole projected component also holds prompt-template content. Subtle failure (25%): repeated replacement during generation causes drift that is absent from the first-token test. Bug (20%): hook layer indexing or Qwen cache behavior differs between forward and generation. Clean success (10%): C=1 makes 座 top-1 and random does not.

Written by PI/gpt-5.4.
