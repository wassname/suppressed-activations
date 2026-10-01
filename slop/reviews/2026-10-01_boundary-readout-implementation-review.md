# Boundary-readout implementation review

**No concrete blocker found for the declared six-case development run.** Static review plus supplied tiny-model logs—not independent execution or pretrained validation.

### Observed implementation

- `scripts/english/08_jlens_one_pass.py:689–700` selects template boundaries only: `"boundary": len(closed) - 1`. It asserts `input_ids[:len(closed)] == closed`, so this is the exact closed-user prefix, **not the last user word**. Neither gold aliases, language labels nor generated text select positions. The empty-user template supplies the fixed preclue header.
- Lines 676–686 and 1379–1399 apply J24, plain24/plain27 and mask-only J consistently. Half-erasure uses the same final-greedy direction; all heads receive `mask | output_mask | extension_mask`. Preclue therefore intentionally contains later-output/full-input mask information, explicitly disclosed in both preregistration and report—not an independent early causal measurement.
- Lines 405–421 capture full prefill states inside the generation call and assert one prefill plus cached decodes. Lines 1382–1384 assert final-position masked-score parity within that capture. Raw boundary/preclue heads, positions, prefixes, generations and full lists are saved.
- The default flag remains false; CLI forwards it through `main(**vars(...))`. The historical helper at `out/2026-10-01_145857_jlens-one-pass/source.py:1350–1364` uses the same normalization/half-erasure construction.
- `slop/audits/2026-10-01_boundary-readout-launcher.py` verifies source hashes and exact case equality: first four native cases, then first reciprocal translation cases. `data/english_boundary_readout_v1.json` declares indices `0,40` and the new native translation wrapper. No output-dependent replacement or v5 selection appears.
- Reporting includes all 180 rows and 72 fixed-position lists; unscored cases remain in denominators.

### Supplied validation evidence

`slop/audits/2026-10-01_boundary-readout-smoke.log:511,1024` reports for seeds 0/1:

> “132 old rows exact +48 boundary/preclue rows; exact states/full generations, one-pass coverage, cached no-forwards … raw-head reconstruction, corrupt-prefix rejection.”

The smoke script implements those assertions. `slop/audits/2026-10-01_boundary-launcher-smoke.log` now reports `"stage": "completed"`, `"actual_forwards": 192`, `"generated_tokens": 192`, and:

> “PASS actual immutable-path coordinator …180 rows,72 fixed-position lists…”

### Residual limits / disconfirming checks

These are random CPU models with identity J: they test plumbing, not learned-J discrimination or pretrained GPU numerical parity. Raw-head reconstruction reuses the helper under review; an independent nonidentity-J calculation would strengthen it. The supplied tests compare branches of the current source, not every historical/default configuration; no complete diff was supplied.

Before scientific interpretation, require the pretrained run’s coverage/parity assertions and inspect all lists, including nuage’s canonical scoreability limitation. Unexpected parity failures would disprove implementation equivalence. Plain-head ties, output leakage or preclue-only hits would weaken mechanistic claims without constituting software failures.

This is a **same-family static review**, not cross-family corroboration. Two translations share cloud; the wrapper changes historical conditions. No pretrained boundary output is available here. Both research goals remain open; v5 remains unrun.

— **PI/OpenAI**