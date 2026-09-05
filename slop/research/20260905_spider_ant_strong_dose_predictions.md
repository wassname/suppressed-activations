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

## Result

The leading prediction was supported. No tested method made `6` top. Every method still answered `8` at C=1.5, then changed directly to top `Spider` at C=2. The best coherent row was `mean_atomic`, raw C=1.25: `p6=0.03834`, `p8=0.87266`, and log odds −3.125. Residual-norm restoration reduced the numerical collapse at C=2 but did not preserve the task: restored mean C=2 had `p6=1.36e-7`, `p8=9.33e-8`, and top `Spider`.

The full continuation was useful. At mean C=1.5, the model first answered `8`, then wrote a hypothesis containing `6`, rejected it, and returned to `8`. At C≥2 it began with `Spider` and often reinterpreted the prompt as if `Spider` occupied the answer slot.

The result is a credible negative for this all-position, L23–L30 dose grid. It does not reject a localized intervention. The next test should first log pre/post Spider and Ant coordinates, output KL, and perturbation size, then densely scan C=1.5–2.0 at only the detected prompt position.

Evidence: [`job_125.md`](../audits/job_125.md), [`job_125_full.log`](../audits/job_125_full.log), and [`data/spider_ant_demo.json`](../../data/spider_ant_demo.json).

Written by PI/gpt-5.4.
