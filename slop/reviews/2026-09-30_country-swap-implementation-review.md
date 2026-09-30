## Bounded implementation review

No blocking defect found in the supplied country-swap diff and affected code. This is implementation review, not scientific or goal signoff.

Observed:
- `scripts/english/08_jlens_one_pass.py:51–69,1012–1030` implements raw coordinates through `pinv(V)`, not raw-score exchange. Unit J and raw plain use separate bases/inverses; finite/rank checks and inverse consistency checks are present.
- `:1114–1160` uses each condition’s current state, records requested/applied BF16 updates, and checks coordinate errors against rounding bounds.
- `:1182–1247` caps each condition at 32 tokens, asserts prefill/decode coverage, and places the clean-target prefill after all five conditions. Target observations do not feed editing.
- Gain construction, `"1.0 + model.model.norm.weight.float()"` at `:560`, agrees with the supplied Qwen source at `/dev/shm/suppressed-import-7ac02bf/transformers/models/qwen3_5/modeling_qwen3_5.py:736`. The gain audit does not establish a cause of historical failures.

### Actionable reporting correction
` scripts/english/08_jlens_one_pass.py:1264` describes the basis using `"@ J16"`, whereas construction indexes `lens["J"][15]` via `block_index=15`. Write `J[15] (block15/output residual16)` to remove indexing ambiguity. A documented one-based naming convention could explain this, but none appears in the supplied contract.

### Required launcher conditions
The reviewed entry point runs **one property per invocation**. The separate launcher must freeze source/helpers and run capital then currency, both with `--prompt-positions 1`, within **one shared 300-second TERM deadline plus 15-second kill grace**, without retries/rescue configurations. Assert all six frozen token strings before either property; main checks only its current answer pair. Preserve both output directories and failed/partial artifacts.

### Coverage limits
Read the complete supplied test and log; did not execute them. The log states `"PASS main seed0/capital"` and corresponding currency/seed1 passes, ending `"CPU random-model smoke only; no 4B scientific outcome."` Tests exercise real tiny BF16 Qwen main, independent algebra, Base token replay, own-state random scaling, casts, coverage and hook ownership. EOS is disabled, so early-stop behavior is not tested. Full-size GPU numerics, rank, runtime and semantics remain unverified. The launcher was not supplied. One random direction cannot establish strong specificity.

— PI/OpenAI