# Experiment2650 review

PI/OpenAI; fresh same-family review, not cross-family independence.

Coverage: read all 14 permitted files completely, including the 15-line console, both complete source versions, instructions, preregistration and test scripts. No commands, model inference, edits or additional reads. Test outputs, launcher internals, imported helpers and cached scientific data were outside this review.

1. **Observed failure:** `out/2026-10-01_013615_jlens-one-pass/console.log:11-15` records failure at `"j_dictionary = unit_dictionary(effective @ J)"`, specifically the float64 norm operation: `"Tried to allocate 4.74 GiB"` with `"3.72 GiB ... free"`. `job.json` records exit1. This is dictionary-construction failure before scoring; no scientific scores exist. The allocator’s fragmentation suggestion does not establish fragmentation as the cause.

2. **Repair preserves the mathematical experiment:** `scripts/english/08_jlens_one_pass.py:81-94` now uses `"range(0, len(vectors), 4096)"`. It retains rowwise float64 norms, float32 atoms, exact-zero exclusion and division by1 for zero rows. Construction still uses `"effective = W.float() * gain"` and `"unit_dictionary(effective @ J)"`. No change to directions, pursuit steps, masks or controls is apparent. GPU bitwise equivalence remains unverified. The boundary/zero/tiny-row assertions in `slop/audits/2026-10-01_matching-pursuit-check.py` can detect normalization discrepancies; their execution is pending evidence.

3. **Capacity remains unvalidated:** chunking does not remove full-size effective/projected matrices, both atom dictionaries, model weights or whole-matrix finite checks. `nonnegative_matching_pursuit` also checks all atoms on each call. Zero transformer forwards does not mean negligible memory or runtime. CPU/tiny-width checks cannot establish production GPU capacity or completion within300s.

4. **Interpretation limits:** preregistration requires exact168-row historical parity, same-cardinality comparisons and symmetric semantic review. These remain unobserved. Sparse coefficients are not probabilities; lexical recovery or pre-clue absence alone does not prove hidden reasoning or causal necessity.

Decision: no static blocker found to one scientifically unchanged retry with this repair and the existing300s+15s bound. Pending repair checks must not be described as passed. Completed checks plus bounded GPU execution can resolve numerical/capacity uncertainty; no sweep or method change is warranted by this failure.