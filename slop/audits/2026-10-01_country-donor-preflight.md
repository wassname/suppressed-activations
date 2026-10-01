# Country-donor launch checks

— PI/OpenAI. No pretrained country result yet.

- `country-donor-preflight.log`: eight generic and three evaluation chat renders agree with tokenizer IDs. Both bare capitals and currency codes use two tokens; code/reports now label first-token probabilities only. Config strings are fixed before outputs.
- `country-donor-smoke.log`: real tiny BF16 Qwen, seeds0/1, eight preparation forwards and nine trajectories each; signed raw means, random norms, exact requested/applied/downstream states, coverage, suffix, EOS, arithmetic expectations, unchanged weights/hooks/defaults.39s.
- `country-animal-regression.log`: existing animal fixture passes seeds0/1, twelve trajectories, early EOS and interruption retention.55s. This checks legacy mechanics, not pretrained equivalence.
- `country-launcher-smoke.log`: the actual shared launcher passes both animal and country families, four fresh tiny model loads each; respectively392/384 and296/288 total forwards/generated tokens.43s. Retained fixtures are named in the logs.
- `slop/reviews/2026-10-01_country-donor-implementation-review.md`: same-family static reviewer found no concrete blocker; explicitly did not attest an absent production manifest. Parent will pin the selected config, donor config, launcher,08 and imports before submission, and hold working helper/data inputs unchanged through execution. Immutable source/launcher copies do not sandbox subsequent imports.

Pseudocode: D=mean(Japan)−mean(Sweden) from eight generic prefills. For current Sweden input addD at block15/final prompt position; reverse adds−D. Subsequent decode updates use0.25D. No current-input calibration, backward pass or observer feedback. Base/random use the same full generation path; no answer logits processor.

Options: keep animal settings (already2706:0/2 joint changes); test unchanged addition on another family (chosen); fitted context transport or changed position (deferred, would alter mechanism). Country norms/context also change, so no isolated family-effect claim.

Predictions: donor-specific full capital+code changes support this bounded transfer; first-prefix shifts alone are too weak; identical Base/donor outputs reject this exact setting; random or arithmetic changes weaken specificity. Plausible explanations before running: task-specific donor mismatch likely65%, weak natural update plausible40%, numerical/provenance bug remote10%, unknown20% (nonexclusive rough bets). Tiny tests constrain numerical mistakes but not semantic alignment. No learning-rate/loss/gradient schedule applies. No success-rate threshold is imposed on this one selected pair.

Plan: one default-queue job, external300s timeout, four fresh pretrained model loads and at most296 forwards. Inspect every full continuation and all conditions. More than eight preparation forwards or unexplained current-input calls blocks interpretation. No dose/layer/k/window rescue and no v5 use.
