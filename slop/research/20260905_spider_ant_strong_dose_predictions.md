# Strong Spider→Ant prototype dose predictions

Question: do stronger stable rank-2 swaps make 6 top before the intervention damages the output?

The prior run fixed three candidates: the post-selected lowercase word-boundary pair, the normalized mean of four matched tokenizer variants, and the first shared-SVD direction. This run changes only C and residual-norm restoration. All prompt positions and residual layers L23–L30 remain active.

| possibility | prior | expected observation |
|---|---:|---|
| answer stays 8 until output degrades | 65% | p(6) peaks below p(8); continuations lose coherence or repeat lexical tokens at larger C |
| stronger dose produces a coherent 6 | 20% | 6 becomes top and the 64-token continuation remains grammatical before later doses degrade |
| norm restoration extends the useful range | 10% | restored rows retain higher p(6) and coherent text after raw rows fail |
| unexpected behavior or implementation error | 5% | non-finite values, unchanged rows, or inconsistent generation |

At C=1 the best observed 6-vs-8 log odds are −3.125. Linear extrapolation of the C=0→1 change crosses zero near C=9.3, so the tested doses are C=1.25, 1.5, 2, 3, 4, and 8. C>1 is extrapolation beyond an exact coordinate swap. It is steering strength, not a more complete swap.

Success requires 6 as the top next token and a coherent continuation. A positive 6-vs-8 contrast created by collapse of both probabilities does not pass.

TODO: publish the complete 64-token continuations for base, selected swap, random replacement, and removal after the intervention choice is stable.

Written by PI/gpt-5.4.
