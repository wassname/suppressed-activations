## Review

- **Correct:** Plain prose identifies the direction of the intervention and fixed input: “replace the suppressed component selected from the spider prompt with the component selected from a dog prompt. The input stays unchanged” (`README.md:146-148`; `nbs/demo.ipynb:353-355`).
- **Correct:** The causal output is explicitly labeled “Readout after intervention” (`README.md:156-159`; `nbs/demo.ipynb:380-383`). The notebook recomputes it from `changed_residuals` before decoding `changed_selected` (`nbs/demo.ipynb:430-441`), so it is not the donor readout.
- **Correct:** Base and Causal intervention present parallel input, readout, 32-token generation, and top-10 table fields. The displayed generations match (`README.md:120-128`, `162-170`; `nbs/demo.ipynb:290-298`, `386-394`), and the notebook asserts both token counts (`nbs/demo.ipynb:251`, `450`).
- **Correct:** The causal table includes `Δ log p` (`README.md:173-184`; `nbs/demo.ipynb:397-400`), computed against `source['logits']` (`nbs/demo.ipynb:471`).
- **Correct:** Base `8` and causal `4` are bold; alternative Base `4` and causal `8` are italic (`README.md:133-134`, `175-176`; `nbs/demo.ipynb:303-304`, `399-400`).
- **Correct:** No misleading causal overclaim found. Both artifacts disclose that `C=1` is the constructed replacement, while displayed `C=4` is an extrapolation and does not establish dog-identity transfer (`README.md:202-206`; `nbs/demo.ipynb:14-16`).

- **Finding: P1 — README and notebook numeric strings are not byte-for-byte identical.** The README uses Unicode minus U+2212, e.g. `−0.125` and `−1.088` (`README.md:133`, `176`), while the executed notebook uses ASCII hyphen-minus U+002D, `-0.125` and `-1.088` (`nbs/demo.ipynb:303`, `400`). The quantities otherwise agree, as do the input, readout, generation, and donor-prompt strings. Smallest fix: normalize negative signs in the README tables to the notebook’s ASCII output, or make the notebook formatter emit U+2212 and re-execute it.

- **Merge verdict: BLOCK** — criterion 6’s explicit byte-for-byte requirement is unmet.

**Signed:** reviewer — fresh-reader comprehension review

## Resolution

The README tables now use the notebook's ASCII minus signs. `just notebook-check && just check` passes after this local correction.

— PI/gpt-5.4
