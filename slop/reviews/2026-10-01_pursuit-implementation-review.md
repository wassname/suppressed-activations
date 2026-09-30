# Implementation review

No blocker found for the frozen eight-case cached experiment. This is static review plus inspection of supplied CPU evidence, not a scientific result or production-run certification.

Read completely: both allowed AGENTS.md files, the three skills, scripts `01_detector_baselines_and_pair_transfer.py`, `03_selector_search.py`, `04_erase_and_language_pairs.py`, `08_jlens_one_pass.py`, v4 data, frozen contract, preregistration, diff, and both check scripts/logs. No commands, inference, edits, or delegation performed. Launcher does not yet exist and was not reviewed. Fresh context, same provider/model family; not cross-family independence.

## Observed implementation

In `scripts/english/08_jlens_one_pass.py`:

- Lines 81–141 implement unit directions, positive greedy projections, repeated-token accumulation, post-decomposition masks and cardinality-matched controls. Line 111 uses `"coefficients[token] += amount"`, rather than overwriting repeated selections.
- Lines 648–651 construct the specified effective unembedding and J orientation: `"j_dictionary = unit_dictionary(effective @ J)"`.
- Lines 743–777 check cache prompt alignment, last-state equality and tokenization; transformer forward guards are installed.
- Lines 893–910 use each diagnostic’s consumed prefix, residual24, and same-position final-layer output mask. Unmasked active atoms are preserved separately.
- Lines 956–1039 score actual returned membership. AUROC gives half credit to ties, including negative infinity. Lines 1129–1139 preserve full case denominators and separate undefined AUROC counts.

These match the frozen algorithm. Erasure and contrast remain separate controls.

## Evidence and residual risks

1. **Tests discriminate several likely implementation bugs.** The helper log reports `"PASS ties, repeated atoms, exact-zero exclusion without tiny-norm cutoff..."`. Its independent NumPy loop checks selection, accumulation and reconstruction. The smoke log reports `"42 baseline rows exact"` for each seed and `"no scoring forwards"`. Guards are exercised, not merely reported as counters.

2. **Scoring validation is incomplete, not an observed scoring defect.** `slop/audits/2026-10-01_matching-pursuit-check.py:104` tests `"((values['pursuit'][0] == values['pursuit'][3]).float() * .5)"`, not production AUROC execution. `slop/audits/2026-10-01_pursuit-main-smoke.py:73` compares baseline rows against the same current implementation. All smoke joint counts are zero. Therefore these checks would not reliably detect a scorer that always rejects genuine recoveries. A fixture with known positive membership, said/input leakage, and tied inactive labels through the production scoring path would resolve this uncertainty.

3. **Extreme finite states can invalidate normalization.** `scripts/english/08_jlens_one_pass.py:102` records `"float(residual.norm())"` in float32; line 125 divides by it without checking positivity/finiteness. Very small nonzero states can underflow that norm; large finite states can overflow it. This could produce nonfinite or zero normalized active scores. The tiny-norm test covers dictionary vectors, not tiny states. Replaying identity-dictionary states near `1e-30` and `1e20` would check this inference. Ordinary cached residuals are unlikely to reach these scales; their actual norms were not reviewed.

Production GPU behavior, memory/time limits, cache contents, immutable launch provenance, prior168-row parity and semantic exclusions remain unverified. The logs explicitly say production parity is pending.

Signed: PI/OpenAI, reviewer-openai.