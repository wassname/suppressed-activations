# Native-coordinate implementation review

**Verdict: no demonstrated blocker in the frozen native-country path.** Same-family static review only—not execution certification or scientific signoff.

Read the complete supplied diff, both changed files, root `AGENTS.md`, ml-debug skill, both contract documents, and country configuration files. No processes or edits performed.

## Observed implementation

- **Correct raw-coordinate operator.** `scripts/english/08_jlens_one_pass.py:51–53` computes `"coordinates = h.float() @ inverse.T"` followed by `(coordinates.flip(-1) - coordinates) @ vectors.T`. At `:1797–1810`, columns are `(rows @ J_edit).T`, with `rows = W[...] * gain`; raw mode retains these without normalization. `coordinate_swap_bases` checks finite columns, numerical rank and pseudoinverse identity. The additional unit basis is saved but is not an executed native condition.
- **Correct schedule and controls.** At `:1957–1976`, random magnitude is calculated from the raw-J candidate on `selected`, its **own current state**, before `"phase_scale = decode_scale if calls else 1.0"`. Native configuration asserts decode `.25`; prefill is full strength. Reverse does not negate the exchange. Plain uses its own raw basis.
- **No preparation or future feedback in this path.** Raw mode empties standalone benchmark cases (`:1105–1107`), excludes preparatory arguments, and has no donor checkpoint. The launcher’s donor preparation is guarded by `"if not raw_coordinate_exchange"` (`slop/audits/2026-10-01_chat-causal-launcher.py:65`). Observer `:2030–2032` only appends readouts and implicitly returns `None`. Post-condition target prefill is guarded by `"if donor_reflection or country_swap"` (`08:2089`), neither true for the supplied country-properties/arithmetic cases.
- **Capture and mathematical assertions are coherent.** `08:1986–2007` captures before/requested/applied states once per coordinate call; the second capture branch explicitly excludes coordinate mode. Expected decode coordinates interpolate rather than fully flip. Requested orthogonal error and BF16 coordinate bounds are checked.
- **Coverage and persistence are present.** `08:2044–2047` checks edit/readout counts against generated tokens and singleton cached calls. The launcher independently checks transformer-call lengths, gradients disabled, assistant suffix, and total calls (`:98–114`). Per-condition state tensors and incremental `interventions.json` retain complete capped token IDs/text, readouts, norms and coverage; unique condition `run.md` files retain complete continuations. Basis inputs, singular values and the random direction are saved.
- **Exact reference checks exist.** Launcher `:85–86` compares `"token_ids","generation","input_repr","top10","prefill_readout"` by exact equality. This is stronger than text-only parity, but does not compare the entire logit distribution.

## Missing evidence and residual risks

The supplied report attests exact leading-space IDs **22466/6124**, learned-basis preflight, and two-seed tiny BF16 core tests with independent float64 reconstruction and unhooked Base parity. I did not independently inspect their logs or execute them.

The initial launcher Base-parity failure and its proposed vocabulary-size explanation are **reported**, not independently diagnosed here. Corrected launcher and old animal/country regressions remain **unverified** in this review. Minimal next check: retain successful corrected end-to-end traces and exact parity assertions; if parity still fails, compare identical model/tokenizer fixture dimensions, logits and readouts before attributing it to the editor. No production change is justified merely by the reported fixture mismatch.

Persistence occurs after each completed trajectory: interruption inside generation can lose that trajectory’s in-memory states. Reference reproducibility also depends on retaining the external reference artifacts and pinning relevant inputs in the actual manifest, which was not supplied for inspection.

ML-debug conclusion: semantic outcomes, null/control comparisons, full production samples, timing and memory remain unknown. Correct coordinate math cannot establish hidden-country replacement; lexical answer steering, disruption, or no effect remain possible. Judge both properties from all complete continuations, not Stock/Tok odds.

— **PI/OpenAI**