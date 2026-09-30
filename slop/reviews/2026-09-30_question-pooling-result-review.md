## Independent audit — PI/OpenAI

`R = out/2026-09-30_185058_jlens-one-pass/`.

**Result:** the frozen pooling test fails its screen; neither subtraction benefit nor semantic isolation is established.

### Observed controls
Across all72 pooled rows, alias-checked joint counts are:

| Representation | Matched | Mismatched | Unsubtracted | Last |
|---|---:|---:|---:|---:|
| J24 |3/8|5/8|5/8|4/8|
| plain24 |0/8|0/8|0/8|1/8|
| plain27 |4/8|4/8|4/8|5/8|

`R/summary.json`: incumbent half-erased plain27 remains6/8; all AUROC denominators are8. The24 last-control top32 lists reproduce their printed probability-contrast counterparts. This is inspection, not an independent execution.

### Findings
1. **Semantic input exclusion is not scored for these English cases.** `R/source.py:616` uses `"input_word" ... else set()`; none of these cases supplies that field. Thus `"input_hits": []` proves nothing. Every winner pass has a definite input leak: December/Thursday/violin retain `" capitals"` from the demonstration’s *capital*; autumn retains `" leaf"`/`"树叶"` from *leaves*. December additionally retains `" Januari"` despite saying January. See `R/run.md` pooled-plain27 lists and `R/pool_components.json:7874,7898,26797,44380`. Symmetric semantic review could challenge these readings, but lexical passes cannot certify exclusion.

2. **Peak provenance contradicts a uniform clue-localization explanation.** `R/verification.json` records J24 December peaking at `" after"`, before Christmas; `" population"` peaks at position12 (`" The"`) with identical0.678586 probability across seven cases. These are pre-clue associations, not identified bridge computation. Conversely, hydrogen peaks at `" element"` and plain27 fall at `" leaves"`: some peaks genuinely align with clues. Attribution to demonstration influence remains untested, not proven.

3. **Recovery and ranking are different.** Plain27 Hamlet newly retrieves `" Ham"` but still leaks Shakespeare; mismatched/unsubtracted hydrogen retrieves hydrogen while retaining gas. Plain27 triangle loses top32 recovery despite pooled scores being pointwise no smaller than last-position scores (`R/source.py:298–303`). Competitor amplification—not necessarily erased hidden information—explains that possibility. Thursday J24’s strongest variant is itself suppressed:0.181327−0.181834<0.

4. **Verification is bounded.** The checker validates supplied components, not independently reconstructed vocabulary-wide maxima/top32. Offline reconstruction would distinguish implementation error from the observed ranking mechanism; no such computation was performed here.

Reject this configuration without posthoc window selection. These eight development prompts do not disprove position-sensitive readout generally.