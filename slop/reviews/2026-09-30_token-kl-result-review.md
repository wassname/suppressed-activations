# Independent audit — PI/OpenAI

Root `R = out/2026-09-30_175925_jlens-one-pass/`.

**Result:** the recorded candidate fails its numeric screen; no subtraction benefit is established. This is a general audit, not semantic certification or goal sign-off.

All 48 new rows were considered through per-case results and complete top32 listings. In case order December, Thursday, autumn, apple, violin, Hamlet, hydrogen, triangle, alias-checked pass vectors are:

| Representation | Matched | Mismatched |
|---|---|---|
| J24 | 11001001 | 11001001 |
| plain24 | 00000000 | 00000001 |
| plain27 | 11101001 | 11101001 |

`R/summary.json` reports matched counts **4/8, 0/8, 5/8**, versus mismatched **4/8, 1/8, 5/8**; all AUROC denominators are eight. Plain27’s AUROC is **0.769**, versus **0.898** mismatched, **0.773** probability-excess, **0.895** mask-only, and **0.899** incumbent half-erasure (**6/8**). `R/token_kl_selection.json` correctly records `"numeric_screen_passed": false`.

### Findings

- **Counted passes retain output information.** December’s matched J24/plain27 lists contain `" Januari"` despite output `" January..."`; both plain27 autumn lists contain `" vinter"` despite `" winter..."` (`R/run.md`, corresponding case/method listings). These are unlisted translations, not arithmetic errors. Violin’s matched plain27 row explicitly combines `"emitted_word_piece_hits": ["wind"]` with `"alias_checked_pass": true` (`R/readout.json:11378–11381`); output is `" the woodwind family.\nQuestion:"`. Prefix-only lexical scoring misses this emitted suffix. Token-identity inspection could disprove a suffix-match interpretation; it cannot erase the recorded overlap. Wrong violin output remains appropriately in the denominator.
- **Misleading report boilerplate:** `R/run.md:23` says cached continuations “are regenerated,” contradicting the replay path. Its summary’s “literal joint” actually uses `joint_pass`, summed from `actual_pass`, not canonical `pass` (`R/source.py:737–740,766–768`). This explains apparently conflicting counts; rename rather than rescore.
- **Timing:** `R/job.json` spans approximately **248.07s**, within 300s; `R/run.md` reports **34.96s** inside `main`. Treating that as whole-job time would omit startup/teardown; their allocation is unmeasured.

Full-vocabulary normalization, eligibility, stable token-ID ties, cyclic controls, and half-credit AUROC agree with the contract in inspected source. No arithmetic defect identified. `verification.json` reports reconstruction and 168-row parity, but its checker cannot prove full-vocabulary top32 optimality.