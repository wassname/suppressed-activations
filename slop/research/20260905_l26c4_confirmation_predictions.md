# Fixed L26/C4 confirmation predictions

Job 149 selected one candidate from the rank-8 layer/dose screen. This run fixes that candidate before new controls are measured.

## Fixed operation

- model and tokenizer: `Qwen/Qwen3.5-4B` at revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`
- extraction: normalized LM-head rise-and-fall at L23/L25/L32, rank 8
- intervention: one edit at residual L26 and the final source-prompt token
- dose: C=4 with residual-norm restoration
- source prompt: `Fact: The number of legs on the animal that spins webs is `
- animal targets: the exact Ant and Dog prompts from job 149
- no fallback to another prompt, layer, rank, dose, position, or seed

## Predictions

| possibility | prior after job 149 | expected observation |
|---|---:|---|
| target components carry specific information beyond a large perturbation | 45% | Ant raises log p(6)/p(8) and Dog raises log p(4)/p(8) above at least 95% of 256 distance-matched random rotations |
| the operation mainly transfers an answer/completion state | 70% | `three plus three` and `two plus two` target components reproduce much of the Ant and Dog digit movement |
| the final-token site matters | 70% | the same operation at the penultimate Spider token has a smaller expected-digit log-odds change |
| the effect is prompt-specific rather than generic | 70% | analogous Ant/Dog operations leave the byte prompt's top answer at 8 |
| the intervention changes only the first sampled digit | 80% | each targeted continuation matches the corresponding forced-first-token continuation after the first token |

The animal-target result is confirmatory only for the frozen first-token effect. Animal semantics require stronger animal-target effects than answer-only controls. Report the exact random percentiles and all controls even if the predictions fail. C=4 is an extrapolation, not an exact replacement.

Written by PI/gpt-5.4.
