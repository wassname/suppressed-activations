## Implementation review

No blocking defect found in the supplied scope. This is not goal sign-off.

### Observed

- `scripts/english/08_jlens_one_pass.py:294–321,550–552`: `"orthogonal = left @ right"` and `"h.float() @ matrix.T"` implement the contracted orientation. Float64 SVD rejects zero/rank-deficient matrices using the specified relative threshold; no determinant correction.
- `scripts/english/08_jlens_one_pass.py:736–756,783–786`: early control uses `"prior_position = first[2]"` from saved question positions, with asserted `Fact`, `:`, ` The`/` In`. Q, original-J, plains and early control share final-LAST subtraction and current-case masks; mismatch changes only the comparator. Normalization precedes masking; positive eligibility and stable token-ID ordering are preserved.
- `scripts/english/08_jlens_one_pass.py:747–756,824–837`: full probabilities, masks, signed excess and tracked label components are persisted. Labels enter evaluation/recording, not score construction. Existing erasure rows remain separate, not composed with Q.
- `slop/audits/2026-09-30_polar-readout-launcher.py`: `"counts['Q excess']>=7"` is combined with strict superiority to all four required comparators and strict early-prefix improvement for counted passes. Q remains fixed; incumbent parity and unchanged generations/168 prior rows are asserted.
- `slop/audits/2026-09-30_polar-main-smoke.log` records both seeds passing: `"full main, real tiny BF16 Qwen prefills/decode cache"`. Factor/readout logs also pass both seeds. I read these logs; I executed nothing.

### Limitations / remaining checks

Production 4B SVD, GPU numerics, prior-row parity and deadline compliance remain unverified. Launcher contains no timeout itself; verify the external 300-second TERM/15-second kill wrapper before execution. Successful production replay would resolve these runtime uncertainties.

Smoke uses two cases and substituted tiny weights; it cannot establish semantic recovery. Early-prefix controls miss later topic priors, and lexical exclusion misses synonyms/later speech. Blinded semantic review and frozen output-matched substitutions remain necessary.

— PI/OpenAI