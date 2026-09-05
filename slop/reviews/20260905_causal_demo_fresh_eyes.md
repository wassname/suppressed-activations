Plan mode's ExitPlanMode tool isn't available in this session, so here's the review directly.

**Fresh-eyes review of `figs/causal_demo.png`** (image + README "A causal component replacement" → "Limits" + `scripts/demo.py` + `data/causal_demo.json`)

**1. Causal claim.** Replacing an 8-dim subspace (picked by the rise-then-fall LM-head criterion) of the residual at layers 23–30, last prompt position, on **one** held-in sample, flips the top next token from `心` to `学校` and moves `log p(学校) − log p(心)` from −12.83 to +0.12 — matches `data/causal_demo.json` exactly (`base`: −12.828125, `replace`: 0.125). README already scopes this correctly:
> "This shows a causal effect on this sample, not transfer to a new prompt."

**2. Label leakage / control mismatch.** No leakage: `source_selected_tokens` (heart, hearts, Heart, -heart, Cards, jantung, cards, cardiac) and `target_selected_tokens` (school, schools, scho, Schools, szko, School, المدرسة, عودة) never contain the actual answer tokens `心`/`学校`. But **the figure under-discloses this list** — panel a shows only 5 of 8 per side, silently dropping `jantung, cards, cardiac` and `School, المدرسة, عودة`, with no "top 5 of 8" note. The dropped `عودة` ("return", off-concept) is the exact noise token already flagged in your own memory (`project_causal_demo_selection_effect.md`). Cutting to 5 makes the basis look cleaner than the JSON shows. Random/remove controls themselves are legitimate (random matches perturbation norm via `matched_random_rotation`; remove only zeroes the source's own subspace).

**3. Prompt/expected-change/operation/metric clarity.** Clear and internally consistent (prompt pair, `心→学校`, L23–30, the `h'=norm(...)` equation all match `demo.py`). One gap: the dramatic log-odds swing masks a thin absolute margin — `replace` row has `p_target=0.1245` vs `p_source=0.1099`, a ~0.015 win over a flattened distribution (`kl_from_clean: 1.345`), with English `school` (0.10) still in the top-5 too. The 32-seed random band (−13.67 to −11.66) does show this is well outside chance, but a reader scanning only the ratio number could overrate how confident the resulting answer is.

**4. Clipping/collision/contradiction in the PNG.** None found — panel d's 32 gray points, labeled points, and dashed x=0 line don't overlap or collide; `remove`'s −9.77 label matches JSON's −9.765625 exactly.

**5. Strongest confound.** `replace` grafts a subspace derived from an entirely separate forward pass (the `Schule` prompt). The `random` control matches perturbation norm but still draws from the *same* target residual, only rotating which directions pass through — this rules out "any norm-matched perturbation does it" but not the sharper alternative that the effect comes from injecting **any semantically-loaded chunk of the target's late-layer residual** (e.g. a generic top-PCA subspace), rather than specifically the rise-then-fall "suppressed" subspace. No such control exists in this artifact. README's Limits section already names the adjacent, softer version of this:
> "This is a diagnostic result. It does not yet show that the subspace causes hidden English computation or suppression."
> "The causal example was selected because both hidden English words rank first. It does not estimate how often the replacement works across prompts."

No files were edited. Review notes saved at `/home/code/.claude/plans/fresh-eyes-scientific-and-visual-mossy-cocoa.md`.
