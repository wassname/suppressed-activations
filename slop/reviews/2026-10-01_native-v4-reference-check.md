# Native-v4 nearest-reference check

— PI/OpenAI

## Result

The bare J readout matches the cached reference’s transport orientation and norm/head ordering. **Adding activation centering or a transport bias would be a new method, not restoration of a missing reference operation.**

No concrete **executed readout bug** is demonstrated by the supplied scope. This is not zero-bug certification: no execution traces, saved tensors, runtime model implementation, or numerical reference comparison were inspected.

## Feature comparison

Paths below are relative to `/workspace/2026/suppressed-activations/`.

| Feature | Cached reference evidence | Our evidence | Assessment |
|---|---|---|---|
| J orientation | `.local/reference/jacobian-lens/jlens/lens.py:143`: `return residual @ J_bar.T` | `scripts/english/08_jlens_one_pass.py:884`: `transported = h.float() @ matrix.T if use_j else h.float()` | Same row-vector transport. |
| Centering / transport bias | `lens.py:139–143` transports directly; `:209–213` then calls `model.unembed(residual)` | `08_jlens_one_pass.py:883–885` does the same | Neither subtracts an activation mean nor adds an affine transport intercept. |
| Layer convention | `lens.py:195–205` records requested blocks and final block `model.n_layers - 1` | `08_jlens_one_pass.py:404–413,857,1025` captures block outputs under residual index `block + 1`, and uses `lens["J"][read_block]` | Internally consistent: J key 23 acts on block-23 output, called residual24. Reference recorder implementation is outside scope, so hook semantics are not independently verified. |
| Final residual | `lens.py:215`: `model.unembed(select(final_layer))` | `08_jlens_one_pass.py:1063` applies norm/head to `res[32][-1]`; `scripts/demo.py:69–80` captures final norm **input**, replacing the normalized final hidden-state entry | No apparent double-normalization in these paths. Runtime hidden-state conventions remain unverified. |
| Token position | `lens.py:203–205` selects explicit sequence positions; default is all positions | `08_jlens_one_pass.py:408–410` saves first-call states; `:1025,1059,1063` reads their last position | Our ordinary readout is **last-prefill-position**, not final-decode-position. Native chat therefore reads the end of the rendered generation prompt. This is a position choice, not demonstrated indexing error. |
| Norm and unembedding | `hf.py:166–173` casts to head dtype, applies final norm, then LM head; optionally softcaps logits | `08_jlens_one_pass.py:883–885` casts to head dtype, applies actual norm and actual head | Same core ordering; head/norm biases, if present, are retained through module calls. Our function lacks reference softcapping. Impact is conditional on runtime configuration, not established here. |
| Input encoding | `hf.py:101–110,157–161` defaults to conditional BOS forcing and tokenizer special-token behavior, with truncation | `08_jlens_one_pass.py:925–934,1018` renders native chat, then uses `add_special_tokens=False` | Not an exact end-to-end reproduction. Actual token-ID differences require tokenizer/runtime evidence. |
| Suppression modifications | `lens.py:209–215` returns ordinary lens/model logits | `08_jlens_one_pass.py:1063–1088,1177–1191` adds output masking, contrasts and normalized-state output-direction erasure | Deliberate additional methods. Official bare J transport does not itself promise input/said exclusion. |

The explicit gain expression at `08_jlens_one_pass.py:858`, `gain = 1.0 + model.model.norm.weight.float()`, is not used by the ordinary `readout()` normalization: that calls the actual norm module. Thus it is not evidence of a missing gain or bias in native-v4’s bare J readout.

## Concrete bug search and uncertainty

**Observed source limitation, not a newly demonstrated execution bug:** `08_jlens_one_pass.py:1048` extracts actual output labels with:

> `actual_words = sorted(set(re.findall(r"[^\W_]+", scoring_text.lower())))`

Punctuation/markup is excluded. The report explicitly states this at `:1401`: “Actual pass uses lexical words … ignoring punctuation.” The supplied research note (`slop/research/2026-10-01_after-native-v4-question.md:9`) reports that “violin's actual bold markup remain[s].”

Affected inputs are continuations containing markup or other non-word output pieces. Such leaks need not fail the lexical joint metric. This would be a bug **if that metric were represented as complete said-output exclusion**; the inspected code instead documents its narrower meaning. The research note is secondary evidence, not independently checked execution output.

Other live explanations remain:

- Runtime capture/tokenization mismatch: untested by this static comparison.
- Evaluation incompleteness: directly supported by lexical-only scoring, but its full measured impact is unknown.
- Answer-category association rather than hidden-identity selectivity: plausible, not established by code.
- Genuine method limitations or other unknown implementation errors: not ruled out.

## Reference availability and reproduction limits

Both requested cached reference files were available and read completely, as were both scripts, the research note, root instructions, global instructions, and ml-debug skill. No commands, edits, network requests, model inference, or delegation were performed.

The local files carry Anthropic copyright notices; the script cites reference revision `581d398613e5602a5af361e1c34d3a92ea82ba8e` at `08_jlens_one_pass.py:34`. Cache checkout provenance was not independently verified. Reference fitting/hooks, checkpoint contents, tokenizer/model configuration, and native-v4 raw artifacts were outside this bounded comparison. The script itself notes at `:1778` that the model revision used for fitting is not recorded in the checkpoint.

No run-level ml-debug metric validation is claimed: full logs, null/baseline measurements, seed spread, timing/memory and runtime traces were unavailable within scope. No numerical diagnosis probabilities are justified from this evidence.

## Discriminating checks—not executed

1. On identical saved residuals, compare official `transport`/`unembed` against our bare `readout`. Agreement would reject orientation/norm ordering as the cause; divergence would localize a real mismatch before adding centering.
2. Compare captured final raw residual → norm/head logits with the same prefill’s model logits; verify block-23 capture and token IDs against the reference recorder/encoder. This could disprove the static layer/position agreement.
3. Inspect runtime softcap configuration. A non-null value would establish an omitted reference operation; its numerical effect still needs measurement.
4. Audit lexical passes against exact generated token pieces and semantic equivalents, separately. This tests whether a scorer limitation—not transport failure—explains apparent exclusion success.

The research note’s classification of content-free subtraction and inverse-affine residuals as **new methods** is supported by the inspected reference. This comparison does not establish which next method would work.