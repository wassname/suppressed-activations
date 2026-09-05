# Spider→Ant rank-16 confirmation predictions

Question: does the L26 rank-16 lowercase-space intervention change `8→6` because it carries Spider→Ant semantics, or because it perturbs an answer-8 distribution?

The focused run fixes rank 16, L26, the final trailing-space position, lowercase-space token directions, residual-norm restoration, and C=8 before evaluation. It compares the spider prompt with `Fact: The number of bits in one byte is `, whose clean answer is also 8. Each prompt receives C=0, C=-8, C=8, and 32 newly seeded rotations matched to the C=8 residual norm and perturbation norm. The run records the suppressed readout before and after intervention and exact 64-token generations. A forced-first-token `6` generation separates intervention content from self-conditioning on the changed answer.

| possibility | prior | expected observation |
|---|---:|---|
| Spider→Ant semantic component | 35% | spider changes to top `6`; byte stays near top `8`; spider target exceeds at least 31/32 random effects; after-readout gains Ant-like tokens |
| generic answer/digit perturbation | 55% | byte also moves toward `6`, random effects often match the target, or after-readout lacks Ant-like tokens |
| numerical or matching bug | 10% | C=0 differs from clean, achieved random distance differs from target, or residual norms differ after restoration |

The continuation counts as independent semantic evidence only if it differs from the no-intervention continuation forced to begin with `6`. The first-token intervention remains valid even if those two continuations are identical.

This run replaces the historical all-in-one script with one focused experiment. It writes `out/<timestamp>_spider-ant/log.md`, `metadata.json`, and `result.json`; it never writes `data/spider_ant_demo.json`.

Written by PI/gpt-5.4.
