# Task2657 read-only review

PI/OpenAI, same-family reviewer.

Coverage: complete `console.log` (110 lines), `case_comparison.md` (244), `source.py` (1531), `launcher.py`, `run.md` (2134), selection, verification, checker, job metadata, prior contract, both AGENTS and four allowed skills. Raw records/diagnostics were only sampled; their complete token inventories were read through `case_comparison.md`. `readout.json` received a targeted check. No commands, inference runs, edits, or independent numerical recomputation.

Paths below are relative to `/workspace/2026/suppressed-activations/`; `R` means `out/2026-10-01_032642_jlens-one-pass/`.

## Verdict

Numerical advancement is **not satisfied**. `R/pursuit_selection.json` reports `"paired_gains": []`, `"paired_losses": [0]`, and `"net_paired_gain": -1`. J24 has 3/8 versus matched unit-dot 4/8. No new gain candidate exists. Keep controls unchanged; promote none.

| Stage | Observed | Assessment |
|---|---|---|
| Execution | Job Success; launcher 42.73 seconds | Completed cached scoring |
| Decomposition | Unmasked positive greedy projections; masks afterwards | Source matches specified algorithm |
| Verification | 168 old rows, 120 new rows, 40 decompositions | Recorded PASS, bounded below |
| Advancement | Positive paired gain required; observed −1 | Not met |

## All-case comparison

Each cell is frozen alias joint success for **pursuit/raw-dot matched/unit-dot matched**, not semantic accuracy (`R/run.md`, `R/case_comparison.md`).

| Case | J24 | plain24 | plain27 |
|---|---|---|---|
| December | 0/1/1 | 0/0/0 | 0/1/1 |
| Thursday | 1/1/1 | 0/0/0 | 1/1/1 |
| autumn | 0/0/0 | 0/0/1 | 1/1/1 |
| apple | 0/0/0 | 0/0/0 | 0/0/0 |
| violin | 1/1/1 | 0/0/1 | 0/1/1 |
| Hamlet | 0/0/0 | 0/0/0 | 0/0/0 |
| hydrogen | 0/0/0 | 0/0/0 | 0/0/0 |
| triangle | 1/1/1 | 0/1/1 | 0/1/1 |

Thus pursuit loses December at J24; autumn/violin/triangle against plain24 unit-dot; December/violin/triangle against both plain27 matched controls.

Semantic interpretation of the quoted inventories:

- **December:** J24 loses explicit December. Plain27 retains ambiguous `"_Dec"` and `" Boxing"`, not a certified recovery. Passing controls contain `" Januari"`: January meaning survives.
- **Thursday:** J24 clearly returns `" Thursday"`; plain27 also does, but `"FR"`/`"금"` are ambiguous possible Friday fragments. Neither gains over its control.
- **autumn:** J24/plain24 pursuit lacks clear autumn. Plain27’s `"Aut"` is a prefix hit, not unambiguous autumn; its inventory mainly names spring/summer. Passing plain controls retain `" vinter"` (winter).
- **apple:** J24 `" Apfel"` is defensible apple recovery, missed by frozen aliases, but `"红色"` leaks red. Plain27 likewise returns apple and red; plain24 lacks clear apple.
- **violin:** J24 returns violin but `" عائلة"` means family, also spoken. Plain24 loses violin; plain27 retains violin but leaks `" wood"`. Baseline `"the woodwind family"` is incorrect: expected strings. Keep this case, but do not claim successful reasoning.
- **Hamlet:** All representations retain Shakespeare; `"Ghost"`, `" Claud"`, and revenge are associations, not clear Hamlet recovery.
- **hydrogen:** No clear hydrogen; state words dominate, including gas/vapor.
- **triangle:** J24 returns triangle but `" drie"` means three. Plain pursuits retain triangle variants and literal `"3"`, explaining their failures.

These are semantic annotations, not rescoring.

## Diagnostics and remaining checks

`R/case_comparison.md` shows pre-clue `" violin"` and `"三角"` already present; triangle is therefore not temporally new. Other priors include January, Lundi, Christmas/leaves, banana/raspberry, Shakespe, and Liquid. Early inventories mostly repeat the Japan/Tokyo prefix. Absence from these finite inventories does not establish necessity.

No confirmed pursuit arithmetic bug emerged. `R/verification.json` reports maximum residual error `7.38e-6`, but explicitly excludes `"independent full-vocabulary dictionary/greedy-step optimality"`. Independently recomputing every greedy argmax would test that remaining possibility. Multilingual/prefix scoring limitations are observed, not evidence of broken decomposition. AUROC near 0.5 is compatible with inactive-label ties; it is not chance-calibrated semantic accuracy.