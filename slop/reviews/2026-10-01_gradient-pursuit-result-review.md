# Job2668 result audit

Signed: PI/OpenAI. Same-family, read-only review; no execution or fresh numerical recomputation.

Paths below are relative to `/workspace/2026/suppressed-activations/`; `R` denotes `out/2026-10-01_045248_jlens-one-pass/`.

## Result

The frozen advancement criterion fails. `R/gradient_pursuit_selection.json` reports `"primary_count": 3`, matched unit-dot count 4, `"paired_gains": []`, `"paired_losses": [0]`, and no new recoveries versus native matching pursuit. Keep the recorded scores unchanged; neither unseen evaluation nor goal completion follows.

Controls agree with this narrow conclusion: GP plain24 is 0/8 versus matched unit-dot 3/8; GP plain27 is 2/8 versus 5/8. The separate half-erasure plain27 incumbent is 6/8 lexically, not a replacement primary.

## All eight cases

Observed in `R/case_comparison.md`, including complete candidate, matched-dot, native-MP lists and both unmasked priors:

| Hidden target | GP J24 observation |
|---|---|
| December | Fails; lost versus dot. Dot contains December but also `" Januari"` (January). |
| Thursday | Passes lexically; `" Thursday"` and `" Thurs"` appear, alongside `" День"` (day), an input equivalent. |
| autumn | Fails; lacks the target and contains `" vinter"` (winter). |
| apple | Fails; `" Apfel"` identifies apple, but `"红色"` repeats the red answer and `"白雪"` overlaps Snow White. |
| violin | Passes lexically, but cached answer is incorrectly `"the woodwind family"`; violin already appears before the Holmes clue. |
| Hamlet | Fails; `" Shakespeare"` remains. `" HAM"` is an ambiguous fragment, not demonstrated Hamlet recovery. |
| hydrogen | Fails; `" Gas"` remains and hydrogen is absent. |
| triangle | Passes lexically despite `" drie"` (three), matching both input and answer; `" Triangle"` already appears pre-clue. |

These are semantic annotations, not a rescored success rate. Symmetric control inspection also finds January leakage in December dot controls, winter leakage in autumn dot controls, and broad instrument inventories before concept-specific evidence. Plain27 autumn’s counted recovery includes `"Aut"`, illustrating the scorer’s prefix ambiguity. Multilingual exclusion coverage remains incomplete.

## Numerical mechanism and limits

`R/fit_comparison.json` reports J24 remaining energy 0.87749 for GP versus 0.89764 for MP, with 237 coefficient-decreasing updates. The sampled December trace visibly decreases January’s coefficient. This supports coefficient revision and improved fitting, not retrieval.

`R/verification.json` reports 288 unchanged prior rows, 96 new rows and 40 decompositions checked; maximum residual error is approximately 8.91e-7. Reading the complete checker confirms reconstruction of selected directions, restricted gradients, line searches, coefficients, rankings and lexical scores.

Its stated limit is decisive: `"Final ranks reconstruct saved scores, not independently derived logits."` It does not independently establish full-vocabulary greedy optimality or diagnostic output-mask derivation. Zero observed boundary hits leave production boundary behavior unexercised.

A full-dictionary independent replay could disprove numerical-path concerns; a frozen symmetric semantic annotation could resolve disputed equivalences. Neither was performed here. The preregistered lexical failure already settles non-advancement.

Coverage: complete source, launcher, checker, console, both case-comparison files and compact result artifacts; sampled large JSON traces and partial `run.md`. All eight displayed cases/controls/priors were inspected, but not every raw numerical record.