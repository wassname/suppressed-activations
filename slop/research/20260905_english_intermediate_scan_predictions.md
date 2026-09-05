# English indirect-reasoning scan predictions

Question: does the fixed L22/L27/L32 LM-head rise-and-fall score recover an unspoken English intermediate outside translation when computed separately for every prompt and token position?

| rule | prediction | result that rejects it as the lead demo |
|---|---|---|
| final prompt position | likely misses spider again; may recover simpler country or shape intermediates | no hidden concept enters top 32 |
| maximum over prompt positions | may recover an intermediate written before the final position | only prompt words or output answers improve |
| remove prompt-token IDs | should expose concepts that are absent from the text without using answer labels | rankings improve only because an observed spelling variant was removed |

The fixed extraction layers remain L22 early, L27 peak, and L32 output. The scan evaluates hidden-concept ranks only after the target-free score is computed. A candidate pair advances only if both clean answers are correct and both hidden concepts enter rank 32 under the same rule.

Likely outcomes: 45% one non-translation family yields a usable pair; 30% the ordinary LM head does not expose indirect intermediates; 15% only an all-position extension works; 10% unknown or implementation error. The next run does not intervene, so it cannot establish causality.

## Result from job 84

No prompt passed the predeclared criterion. The clean spider, ant, triangle, and square answers were correct, but the best unspoken ranks were 210198, 2213, 22698, and 51717. The closest apparent hit was Canada at rank 20, but the model's clean top token was `1` rather than Ottawa. Source: [`../audits/job_84_full.log`](../audits/job_84_full.log).

> legs hidden=spider expected=8 top='8' rank_final=72303 rank_any=210202 rank_unspoken=210198
>
> capital hidden=Canada expected=Ottawa top='1' rank_final=167 rank_any=20 rank_unspoken=20

My read: the all-position extension did not recover an English indirect intermediate. It often promoted task words such as `web`, `capital`, `elements`, and `planet`; these are morphological or semantic prompt echoes rather than the withheld entity. This makes the prompt-position hypothesis unlikely under the current unnormalized vocabulary score.

The next cheapest test is row-norm normalization of the same LM-head directions and one global layer rule fit on a held-in family. This targets a concrete confound: high-norm vocabulary rows can dominate a raw dot-product ranking. If hidden-concept ranks remain far outside 32, the ordinary LM head probably lacks the sensitivity needed for this demo.

Job 85 found that row normalization at L23/L25/L32 moves `spider` to rank 6, compared with rank 34 for raw logits. `ant` remains rank 14798 and the held-out shape concepts remain above rank 66000. I therefore fixed L23/L25/L32 from the spider/ant layer search and scanned new animal descriptions for a second concept. A target advanced only if its clean answer was correct and its hidden animal ranked at most 32.

Job 86 crashed on `firefly`, which has no single-token vocabulary variant. The deterministic tokenizer reproduction and audit are in [`../audits/job_86.md`](../audits/job_86.md). Job 87 prevalidated atomic concepts and reran the unchanged score. Dog ranked 4 and cat ranked 21; both clean answers were `4`. Seven of nine held-out concepts failed the joint criterion. The fixed detector therefore found two held-out samples, not a global animal subspace. See [`english_animal_target_scan.json`](english_animal_target_scan.json) and [`../audits/job_87.md`](../audits/job_87.md).

The next test freezes spider as source and dog as target. It asks whether replacing the separately extracted spider component with the dog component changes the answer from `8` toward `4` more than rank- and norm-matched random replacements. Readout success alone is not causal evidence.

Written by PI/gpt-5.4.
