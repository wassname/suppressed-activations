# Coordinate prerequisite audit — PI/OpenAI

Paths below use `R = out/2026-09-30_163330_jlens-one-pass/`.

**Conclusion:** This candidate fails its frozen prerequisite; coherent one-pass dog→spider replacement remains untested. No arithmetic/sign bug is apparent in the inspected validation path.

### Strongest findings

1. **Ordering does not establish transferable centering.** `R/result.json` records `"ordered_pairs": 8`, but `"corrected_brackets": 2` and `"candidate_passes_prerequisite": false`. Both successes end in donor-reference token `" It"`; all six other pairs put **both** animals above zero. For example, corrected explicit-1 margins are dog `0.72695`, spider `1.37374`. A negative-side dog→spider reflection would therefore leave that dog final state unchanged. This is a mathematical consequence, not an observed intervention.

   `R/config.json` says “ordering without bracketing implicates centering.” That supports context-dependent offsets, **not** an adequate direction or a repair by one global center. Already, corrected indirect-3 dog `1.23035` exceeds explicit-0 spider `0.03998`; no shared scalar threshold separates these observations. Countercheck: recompute these extrema from saved states.

2. **Embedding subtraction removes only the direct embedding term.** `R/source.py:62–65` computes `"corrected = raw + (reference_embedding - embeddings.float()) @ direction"`. Equal terminal embeddings necessarily preserve paired differences; reference-token equality is likewise algebraic, not independent semantic validation. Contextual token effects through preceding blocks remain. Lexical/context associations could produce 8/8 ordering without a causal concept variable. Distinguishing evidence would require held-out context controls and ultimately coherent cross-property causal outcomes—not supplied here.

3. **Corrected validation is not a corrected intervention implementation.** `R/source.py`’s intervention hook calls `"reflect_donor_side(selected, donor_center, donor_direction)"`, whose margin is raw `(h-center)@direction`; no embedding correction enters it. Any later reuse of `--donor-reflection` would test the old coordinate, not this candidate. Static check: trace every intervention margin computation. This does not invalidate the current noninterventional result.

### Scope and verification limits

`R/source.py` dispatches validation then `return`s before lens loading/generation; capture hooks do not replace activations. `R/samples.jsonl` records sixteen single-forward samples; `R/run.md` explicitly says “This is not causal success.”

`R/verification.json`’s `"PASS"` concerns cached reconstruction, not model execution authenticity or semantics. The checker reuses saved states/embeddings; I did not independently execute hashes or tensor reconstruction. Read all requested artifacts, complete source, helper, AGENTS.md and ml-debug skill. No commands, inference, edits, or generation performed.

**Not goal sign-off.**