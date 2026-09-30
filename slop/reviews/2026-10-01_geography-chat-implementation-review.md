# Geography-chat implementation review

**Verdict:** No blocking defect found in the fixed four-prompt launch path. The extension preserves completion defaults and keeps generation, readout selection, and evaluation labels separate. This is a same-family static review, not scientific or goal signoff.

— PI/OpenAI

## Evidence reviewed

Read the complete current and archived source, all enumerated data/audit/test files, applicable AGENTS.md files, and the ML-debug skill. No commands, inference, edits, discovery, or network requests were performed.

The smoke logs identify the requested source SHA:
`8703a56f4313e673eb19f891b97eb3cbb247818187aa321e9f75130b3fc3b868`.
I did not independently calculate it.

### Implementation checks

- **Old defaults:** `scripts/english/08_jlens_one_pass.py:402–418` retains eight-token greedy cached generation unless explicitly overridden. With `eos_token_id=None`, no EOS override is passed. The prior source has the same capture logic and fixed eight-token call.
- **Native rendering/EOS:** `scripts/english/08_jlens_one_pass.py:701–707,785–802` explicitly enables the native no-thinking template and combines tokenizer/model EOS IDs. Preflight records IDs `[248044,248046]` and matching rendered/native tokenization. Completion mode does not inherit these overrides.
- **Same-generation capture:** At `:408–410`, `"if not coverage[residual_index]"` saves only the first call's states. Coverage requires one full prefill followed by `n-1` single-token calls. Readouts and output erasure consume those saved prefill states, not final decode states.
- **Raw versus scoring text:** At `:896–904`, raw decoding is retained, while chat evaluation alone uses `"skip_special_tokens=True"`. Masks and erasure use the prompt and initial final-layer logits; generated words do not select readout tokens.
- **Partner labels:** At `:1116–1122`, partner aliases only query ranks from the already-computed `z`; they do not alter scores, masks, or selection.
- **Four trajectories / 72 rows:** The launcher invokes `main` once with four frozen cases, half-erasure, mask1 and cap32. Eighteen method rows per case give 72; uniqueness and trajectory coverage are asserted. No replay, pursuit, calibration, intervention, or alternative-primary selection is requested. The four reported methods are explicitly fixed.
- **Selection limits:** Preregistration explicitly states geography-based posthoc task selection, corpus overlap, two dependent pairs, and possible direct city–continent association. It does not claim unseen concepts, causal necessity, universal success, or completed goals.

## Observed test evidence and limitations

`slop/audits/2026-10-01_chat-main-smoke.log` reports, for both seeds:

> “native chat,32-token full main, exact raw/scoring text, same-prefill states, early EOS override, coverage, owned hooks,36 replay rows exact, unchanged parameters/defaults”

The test uses real tiny random BF16 Qwen models and the pinned tokenizer. Its early-stop check makes the first generated token an EOS; this verifies stopping mechanics, not a naturally generated protocol EOS.

`slop/audits/2026-10-01_chat-legacy-main.log` reports:

> “72 baseline rows exact, unchanged parameters/IDs/states, no scoring forwards”

**Nonblocking coverage gap:** `slop/audits/2026-10-01_pursuit-main-smoke.py` creates cached trajectories using the current `generate_readout`, then compares current and archived **replay scoring**. Thus this proves legacy scorer parity on those fixtures, not independently old-versus-new fresh generation parity. Static comparison shows the default generation call is equivalent. A direct comparison of both helpers on the same tiny model would close this gap; differing IDs, coverage, or saved states would disprove default parity.

`slop/audits/2026-10-01_chat-legacy-scorer.log` includes:

> “PASS actual production scorer: genuine recovery, said/input leaks, tied inactive/active AUROC, undefined/spoken-hidden rejection, zero-return control despite rank0”

These fixtures support metric mechanics, not pretrained semantic performance.

## Required follow-through and residual risks

No mandatory source fix identified before these four generations.

Before presenting a demo, complete the preregistered symmetric semantic review of all returned entries and full continuations. Lexical answer presence is not correctness or instruction adherence; prefix-label hits are not necessarily country identities. The launcher appropriately leaves reviewed metrics unset and sets `"semantic_review_pending": True`.

Remaining evidence limits:

- No pretrained outputs or full-size GPU timing/memory evidence exist in this review.
- The launcher’s four-case postprocessing was inspected statically; the native smoke exercises two cases.
- The supplied preflight log contains the successful run, not the two earlier failures. Their history is documented but not independently verified here.
- The additional authorized diff path was unavailable; complete source files were compared instead.
- Queue timeout enforcement and launcher-hash freezing are not demonstrated by these files.
- AUROC and lexical passes can reflect masking, prefix ambiguity, or input association. Neither establishes a necessary hidden reasoning step.